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
                Field('direction_type', label='Direction'),
                format="%(direction_type)s")

db.define_table('Control_Instruction',
                Field('device_ref_id', 'reference Device'),
                Field('onoff_flag', 'boolean', label='Motor ON/OFF', comment='* Check for ON & Uncheck for OFF'),
                Field('volt_flag', 'string', label='Voltage'),
                Field('curr_flag', 'string', label='Current'),
                Field('rot_flag', 'string', label='Rotation', comment='* Insert only integer value [revolution per minute]'),
                Field('dir_flag', 'reference Direction', label='Direction', requires = IS_IN_DB(db, db.Direction.id,'%(direction_type)s')),
                Field('freq_flag', 'string', label='Frequency'),
                Field('off_flag', 'boolean', label='Off')
                )


db.define_table('Status',
                Field('device_ref_id', 'reference Device'),
                Field('created', 'datetime'),
                Field('last_ping','datetime', requires=IS_NOT_EMPTY()),
                Field('server_time','datetime', requires=IS_NOT_EMPTY()))