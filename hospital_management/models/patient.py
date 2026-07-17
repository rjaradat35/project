from datetime import date

from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    image = fields.Image(string='Photo')
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age',
                         help='Computed automatically from the date of birth.')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', tracking=True)
    blood_group = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'),
        ('o+', 'O+'), ('o-', 'O-'),
    ], string='Blood Group', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    address = fields.Text(string='Address')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id',
                                      string='Appointments')
    notes = fields.Text(string='Notes')

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            if patient.date_of_birth:
                dob = patient.date_of_birth
                patient.age = today.year - dob.year - (
                    (today.month, today.day) < (dob.month, dob.day))
            else:
                patient.age = 0
