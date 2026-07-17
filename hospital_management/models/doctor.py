from odoo import api, fields, models


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(string='Reference', readonly=True, copy=False,
                            default='New', help='Auto-generated doctor reference.')
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
        ('radiology', 'Radiology'),
        ('surgery', 'Surgery'),
        ('emergency', 'Emergency'),
    ], string='Specialization', required=True, tracking=True)
    department_id = fields.Many2one('hospital.department', string='Department',
                                    tracking=True, ondelete='set null')
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    years_of_experience = fields.Integer(string='Years of Experience')
    consultation_fee = fields.Monetary(string='Consultation Fee',
                                       currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id',
                                      string='Appointments')
    appointment_count = fields.Integer(string='Appointment Count',
                                       compute='_compute_appointment_count')
    note = fields.Html(string='Internal Notes')
    active = fields.Boolean(default=True)

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for doctor in self:
            doctor.appointment_count = len(doctor.appointment_ids)

    @api.model_create_multi
    def create(self, vals_list):
        # assign the next number from the sequence defined in data/sequence_data.xml
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'hospital.doctor') or 'New'
        return super().create(vals_list)

    def action_view_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
        }
