from odoo import fields, models


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # appointments are displayed by their patient's name
    _rec_name = 'patient_id'
    _order = 'appointment_date desc'

    patient_id = fields.Many2one('hospital.patient', string='Patient',
                                 required=True, tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor',
                                required=True, tracking=True)
    # follows the selected doctor's department automatically
    department_id = fields.Many2one(related='doctor_id.department_id',
                                    string='Department', store=True)
    appointment_date = fields.Datetime(string='Appointment Date', required=True,
                                       default=fields.Datetime.now, tracking=True)
    reason = fields.Text(string='Reason for Visit')
    prescription = fields.Text(string='Prescription')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    # called by the buttons in the form view header
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
