{
    'name': 'Hospital Management',
    'version': '18.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Manage patients, doctors, departments and appointments',
    'description': """
Hospital Management
===================
* Patient, Doctor, Appointment and Department models
* List and form views for each model, with a menu to reach them
* Chatter (messages, followers, activities) on every form view
    """,
    'author': 'Rami Jaradat',
    'license': 'LGPL-3',
    # 'mail' is required for the chatter (mail.thread / mail.activity.mixin)
    'depends': ['base', 'mail'],
    'data': [
        # security must load before anything that uses the models
        'security/ir.model.access.csv',
        # views define the actions, so they load before the menus that use them
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/appointment_views.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True,
}
