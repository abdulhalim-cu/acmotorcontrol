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

db.define_table('Direction',
                Field('direction_type'),
                format="%(direction_type)s")

db.define_table('Control_Instruction',
                Field('device_ref_id', 'reference Device', label='Device ID'),
                Field('volt_flag', 'string', label='Voltage'),
                Field('curr_flag', 'string', label='Current'),
                Field('freq_flag', 'string', label='Frequency'),
                Field('onoff_flag', 'boolean', label='ON/OFF'),
                Field('off_flag', 'boolean', label='Off'),
                Field('rot_flag', 'string', label='Rotation'),
                Field('dir_flag', 'reference Direction', requires = IS_IN_DB(db, db.Direction.id,'%(direction_type)s')))
