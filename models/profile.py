from odoo import fields, models, api, _
from odoo.exceptions import UserError

class UniProfile(models.Model):
    _name = 'uni.profile'
    _description = 'Student information.'
    

    profile_name = fields.Char(string='Student Profile Name')
    profile_id_num = fields.Char(string='Profile ID')
    student_profile= fields.Many2one('uni.student', string = 'Profile')
    
