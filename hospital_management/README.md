# Hospital Management

An Odoo 18 module to manage the day-to-day operations of a hospital.

## Features

* **Patients** — personal info, photo, blood group, allergies, medical history,
  age computed automatically from the date of birth, auto-generated reference
  (`PAT/00001`).
* **Doctors** — specialization, department, consultation fee, kanban view with
  photos, auto-generated reference (`DOC/00001`).
* **Departments** — hospital structure with head of department, list of
  doctors, and smart buttons showing doctor / appointment counts.
* **Appointments** — links a patient with a doctor, auto-generated reference
  (`APT/00001`), calendar view, priority, and a state workflow:
  `Draft → Confirmed → Done` (or `Cancelled`), driven by header buttons.
* **Chatter on every form view** — all four models inherit `mail.thread` and
  `mail.activity.mixin`, so users can log notes, send messages, add followers
  and schedule activities on any record. Important fields use `tracking=True`
  so changes are logged automatically in the chatter.

## Module structure

```
hospital_management/
├── __init__.py               # imports the models package
├── __manifest__.py           # module descriptor (name, depends, data files)
├── models/
│   ├── department.py         # hospital.department
│   ├── doctor.py             # hospital.doctor
│   ├── patient.py            # hospital.patient
│   └── appointment.py        # hospital.appointment (state workflow)
├── security/
│   └── ir.model.access.csv   # access rights (CRUD) for internal users
├── data/
│   └── sequence_data.xml     # ir.sequence records for PAT/DOC/APT references
└── views/
    ├── department_views.xml  # list, form, search + action
    ├── doctor_views.xml      # kanban, list, form, search + action
    ├── patient_views.xml     # list, form, search + action
    ├── appointment_views.xml # list, calendar, form, search + action
    └── menu_views.xml        # Hospital root menu + submenus
```

## Installation

1. Copy the `hospital_management` folder into your Odoo `addons` path.
2. Restart the Odoo server.
3. Activate developer mode, go to **Apps**, click **Update Apps List**.
4. Search for *Hospital Management* and click **Activate**.

A new **Hospital** app appears in the main menu with Appointments, Patients,
Doctors and a Configuration ▸ Departments menu.

## Requirements

* Odoo 18.0 (Community or Enterprise)
* Depends on the `base` and `mail` modules (both ship with Odoo).
