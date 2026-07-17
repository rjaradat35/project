from odoo import fields, models


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    image = fields.Image(string='Photo')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', tracking=True)
    specialization = fields.Selection([
        ('general', 'General Medicine'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('dermatology', 'Dermatology'),
        ('surgery', 'Surgery'),
        ('emergency', 'Emergency'),
    ], string='Specialization', tracking=True)
    department_id = fields.Many2one('hospital.department', string='Department',
                                    tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id',
                                      string='Appointments')
    note = fields.Text(string='Notes')
