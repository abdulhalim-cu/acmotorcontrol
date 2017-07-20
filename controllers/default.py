def index():
    if not auth.user:
        redirect(URL('user/login'))

    user_name = "%(username)s" % auth.user
    user_devices =db.executesql("SELECT Device.device_id, Device.device_name, Device.model, Device.location, \
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
