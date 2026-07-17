from odoo import api, fields, models


class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'
    # inheriting these two mixins is what makes the chatter work on the form view
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, copy=False, tracking=True,
                       help='Short unique code for the department, e.g. CARD for Cardiology.')
    sequence = fields.Integer(string='Sequence', default=10,
                              help='Used to order departments in list views.')
    head_doctor_id = fields.Many2one('hospital.doctor', string='Head of Department',
                                     tracking=True,
                                     domain="[('department_id', '=', id)]")
    doctor_ids = fields.One2many('hospital.doctor', 'department_id', string='Doctors')
    doctor_count = fields.Integer(string='Doctor Count', compute='_compute_doctor_count')
    appointment_ids = fields.One2many('hospital.appointment', 'department_id',
                                      string='Appointments')
    appointment_count = fields.Integer(string='Appointment Count',
                                       compute='_compute_appointment_count')
    description = fields.Html(string='Description')
    color = fields.Integer(string='Color')
    active = fields.Boolean(default=True,
                            help='Archive a department instead of deleting it.')

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'The department code must be unique!'),
    ]

    @api.depends('doctor_ids')
    def _compute_doctor_count(self):
        for department in self:
            department.doctor_count = len(department.doctor_ids)

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for department in self:
            department.appointment_count = len(department.appointment_ids)

    def action_view_doctors(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Doctors',
            'res_model': 'hospital.doctor',
            'view_mode': 'list,form',
            'domain': [('department_id', '=', self.id)],
            'context': {'default_department_id': self.id},
        }

    def action_view_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('department_id', '=', self.id)],
        }
