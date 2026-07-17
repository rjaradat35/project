from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'appointment_date desc'
    _rec_name = 'reference'

    reference = fields.Char(string='Reference', readonly=True, copy=False,
                            default='New')
    patient_id = fields.Many2one('hospital.patient', string='Patient',
                                 required=True, tracking=True, ondelete='restrict')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor',
                                required=True, tracking=True, ondelete='restrict')
    # follows the doctor automatically; stored so we can search & group by it
    department_id = fields.Many2one(related='doctor_id.department_id',
                                    string='Department', store=True, readonly=True)
    appointment_date = fields.Datetime(string='Appointment Date', required=True,
                                       tracking=True,
                                       default=fields.Datetime.now)
    duration = fields.Float(string='Duration (Hours)', default=0.5)
    reason = fields.Text(string='Reason for Visit', tracking=True)
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], string='Priority', default='0', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)
    # a few useful pieces of patient info shown directly on the appointment
    patient_age = fields.Integer(related='patient_id.age', string='Patient Age')
    patient_phone = fields.Char(related='patient_id.phone', string='Patient Phone')

    @api.constrains('duration')
    def _check_duration(self):
        for appointment in self:
            if appointment.duration <= 0:
                raise ValidationError('The duration must be greater than zero.')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'hospital.appointment') or 'New'
        return super().create(vals_list)

    def unlink(self):
        for appointment in self:
            if appointment.state not in ('draft', 'cancelled'):
                raise UserError(
                    'You can only delete draft or cancelled appointments.')
        return super().unlink()

    # ---- state workflow: called by the header buttons in the form view ----
    def action_confirm(self):
        for appointment in self:
            if appointment.appointment_date < fields.Datetime.now():
                raise UserError('You cannot confirm an appointment in the past.')
            appointment.state = 'confirmed'

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
