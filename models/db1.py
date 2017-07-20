# -*- coding: utf-8 -*-

db.define_table('Device',
                Field('device_id', 'string'),
                Field('device_name', 'string'),
                Field('model', 'string'),
                Field('location', 'string')
               )

db.Device.device_id.requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(db, 'Device.device_id')]
db.Device.device_name.requires = IS_NOT_EMPTY()

db.define_table('User_Device',
                Field('user_ref_id', 'reference auth_user'),
                Field('device_ref_id', 'reference Device'))


db.define_table('Control_Instruction',
                Field('device_ref_id', 'reference Device'),
                Field('volt_flag', 'string'),
                Field('curr_flag', 'string'),
                Field('freq_flag', 'string'),
                Field('onoff_flag', 'boolean'),
                Field('off_flag', 'boolean'),
                Field('rot_flag', 'string'),
                Field('dir_flag', 'string'))
