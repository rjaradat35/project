from datetime import date

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(string='Reference', readonly=True, copy=False,
                            default='New', help='Auto-generated patient reference.')
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
    emergency_contact_name = fields.Char(string='Emergency Contact')
    emergency_contact_phone = fields.Char(string='Emergency Phone')
    allergies = fields.Text(string='Allergies')
    medical_history = fields.Html(string='Medical History')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id',
                                      string='Appointments')
    appointment_count = fields.Integer(string='Appointment Count',
                                       compute='_compute_appointment_count')
    active = fields.Boolean(default=True)

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

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for patient in self:
            patient.appointment_count = len(patient.appointment_ids)

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for patient in self:
            if patient.date_of_birth and patient.date_of_birth > fields.Date.today():
                raise ValidationError('The date of birth cannot be in the future.')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'hospital.patient') or 'New'
        return super().create(vals_list)

    def action_view_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }
