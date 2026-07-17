from odoo import fields, models


class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'
    # these two mixins add the chatter (messages, followers, activities)
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    doctor_ids = fields.One2many('hospital.doctor', 'department_id',
                                 string='Doctors')
    description = fields.Text(string='Description')
