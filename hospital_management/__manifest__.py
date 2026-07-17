{
    'name': 'Hospital Management',
    'version': '18.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Manage patients, doctors, departments and appointments',
    'description': """
Hospital Management System
==========================
This module helps hospitals manage their daily operations:

* Patients (personal & medical information)
* Doctors (specialties, departments)
* Departments (hospital structure)
* Appointments (scheduling with a state workflow)

Every form view includes a chatter for messages, followers and activities.
    """,
    'author': 'Rakan Jaradat',
    'website': '',
    'license': 'LGPL-3',
    # 'mail' is required for the chatter (mail.thread / mail.activity.mixin)
    'depends': ['base', 'mail'],
    'data': [
        # security must load before anything that uses the models
        'security/ir.model.access.csv',
        # master data (sequences) before views
        'data/sequence_data.xml',
        # views define the actions, so they load before the menus that use them
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/appointment_views.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
