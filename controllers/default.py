def index():
    if not auth.user:
        redirect(URL('user/login'))

    user_name = "%(username)s" % auth.user
    user_devices = db.executesql("SELECT Device.id, Device.device_id, Device.device_name, Device.model, Device.location, \
            User_Device.user_ref_id FROM Device INNER JOIN (auth_user INNER JOIN User_Device \
            ON auth_user.id = User_Device.user_ref_id) ON Device.id = User_Device.device_ref_id \
            WHERE (((auth_user.username)=%s))", user_name)

    return dict(user_devices=user_devices)

@auth.requires_login()
def add_device():
    if request.post_vars.submit:
        user_name = "%(username)s" % auth.user
        device_name = request.post_vars.devicename
        device_id = request.post_vars.deviceid
        device_loc = request.post_vars.location
        device_model = request.post_vars.model
        query = db.executesql("SELECT id FROM Device WHERE device_id=%s", device_id)
        if not query:
            db.executesql("INSERT INTO Device (device_id, device_name, model, location) VALUES(%s, %s, %s, %s)", \
                (device_id, device_name, device_model, device_loc))
            db.commit()
            device_ref_id = db.executesql("SELECT id FROM Device WHERE device_id=%s", device_id)
            if device_ref_id:
                user_ref_id = db.executesql("SELECT id FROM auth_user WHERE username=%s", user_name)
                db.executesql("INSERT INTO User_Device (user_ref_id, device_ref_id) VALUES(%s, %s)", (user_ref_id, device_ref_id))
                db.commit()
                db.executesql("INSERT INTO Control_Instruction (device_ref_id, volt_flag, curr_flag, \
                    freq_flag, onoff_flag, off_flag, rot_flag, dir_flag) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",\
                     (device_ref_id, '0', '0', '0', 0, 0, '0', '0'))
                db.commit()
    return dict()


@auth.requires_login()
def dev_control():
    if request.args(0, cast=int):
        #device_ref_id = request.args(0, cast=int)
        id = db.executesql("SELECT id FROM Control_Instruction WHERE device_ref_id = %s", request.args[0])
        if id:
            db.Control_Instruction.id.readable = db.Control_Instruction.id.writable = False
            db.Control_Instruction.device_ref_id.readable = db.Control_Instruction.device_ref_id.writable = False
            db.Control_Instruction.off_flag.readable = db.Control_Instruction.off_flag.writable = False
            form = SQLFORM(db.Control_Instruction, id[0][0], showid=False).process(next='index')
            return dict(form = form)
        else:
            return None


def get_instruction():
    if request.vars.deviceid:
        device_id = request.vars.deviceid
        device_info = db.executesql("SELECT Control_Instruction.volt_flag, Control_Instruction.curr_flag, \
            Control_Instruction.freq_flag, Control_Instruction.onoff_flag, Control_Instruction.rot_flag, \
            Direction.direction_type FROM Device INNER JOIN (Control_Instruction INNER JOIN Direction ON Direction.id = Control_Instruction.dir_flag) \
            ON (Device.id = Control_Instruction.device_ref_id) WHERE Device.device_id=%s", device_id)

        jsonlst = []
        for i in device_info:
            volt = i[0]
            curr = i[1]
            freq = i[2]
            onof = i[3]
            rota = i[4]
            dire = i[5]
            record = {"voltage" : volt, "current" : curr, "frquency" : freq, "onoff" : onof, "rotation" : rota, "direction": dire}
            jsonlst.append(record)
        return dict(device_info = jsonlst)
    else:
        return None

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
