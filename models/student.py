from re import template
from odoo import fields, models, api, _
from odoo.exceptions import UserError

class UniStudent(models.Model):
    _name = 'uni.student'
    _description = 'Student information.'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Student Name')
    stu_id_num = fields.Char(string='Student ID')
    credit_earn = fields.Integer(string='Credit Earned', compute='_get_credit')
    photo = fields.Binary(string="Photo", attachment=True,tracking=True)
    prm = fields.Many2one('res.users', string = 'PRM')
    email = fields.Char(string='Email')
    course_ids = fields.Many2many('uni.course', string='Courses',tracking=True)
    department_id = fields.Many2one('uni.department', string='Department', domain=[('engr_dept','=',True)])
    faculty_assign_line = fields.One2many('uni.student.line', 'faculty_assign_id', string='Faculty Assign Line')

    f_id = fields.Many2one('uni.faculty', string='New faculty')
   

    def check_orm(self):
        #ORM
        all_data = self.env['uni.course'].search([('credit_hour','=',3)])
        for data in all_data:
            print(data.course_name)

        raise UserError(_(all_data))

    def check_sql(self): 
        # SQL
        self.env.cr.execute(""" select credit_hour from uni_course; """,)
        sql_data = self.env.cr.fetchall()

        raise UserError(_(sql_data))
    def test_student(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/student',
            'target': 'current',
            'target': 'self',
            'context': self._context, 
        }

    def test_student_action(self):
        # self.ensure_one()
        # action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_journal_line")
        # action['context'] = dict(self.env.context)
        # action['context']['form_view_initial_mode'] = 'edit'
        # action['context']['view_no_maturity'] = False
        # action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        # action['res_id'] = self.copy().id
        # return action
        self.ensure_one()
        mass_mailing_copy = self.copy()
        # if mass_mailing_copy:
        #     context = dict(self.env.context)
        #     context['form_view_initial_mode'] = 'edit'
        #     return {
        #         'type': 'ir.actions.act_window',
        #         'view_mode': 'form',
        #         'res_model': 'mailing.mailing',
        #         'res_id': mass_mailing_copy.id,
        #         'context': context,
        #     }
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",mass_mailing_copy)
        return mass_mailing_copy
        

    # def action_id_card(self):
    #     # print("sending email")
    #     if self.email:
    #         temp_id = self.env.ref('university_management.student_email_template').id
    #         print("############################################################################temp",temp_id)
    #         aaa=self.env['mail.template'].browse(temp_id).send_mail(self.id, force_send=True)
    #         print("######################################",aaa)

    def calculate_credit(self):
        total_credit = 0
        all_data = self.env['uni.course'].search([('id','in',self.course_ids.ids)])
        for data in all_data:
            total_credit += data.credit_hour

        return total_credit

    def _get_credit(self):
        for item in self:
            item.credit_earn = item.calculate_credit()

    @api.model
    def test_student_cron(self):
        print("####################################kaushik###################################")
        rrr = self.env['uni.student'].sudo().search([('email','!=', False)])
        print("####################################kaushik###################################\n",rrr)
        for rec in rrr:
            print("########################################bhai###############################\n")
            temp_id = self.env.ref('university_management.student_email_template').id
            print("############################################################################\ntemp",temp_id)
            # aaa=self.env['mail.template'].browse(temp_id).sudo().send_mail(self.id, force_send=True)
            try:
                aaa=self.env['mail.template'].browse(temp_id).sudo().send_mail(rec.id, force_send=True)
            except MailDeliveryException as e:
                _logger.warning('MailDeliveryException while sending digest %d. Digest is now scheduled for next cron update.', self.id)
            # print("#####################lllllllllllllllll#################\n",aaa)
    
    def write(self, vals):
        cv = "<b>" + _("The ordered quantity has been updated.") + "</b><ul>"
        if 'name' in vals:
            new = vals
            print("#################NEW#################################",new)
            # cv = "<b>" + _("The ordered quantity has been updated.") + "</b><ul>"
            matcha =new.get('name')
            # print("*********************************",matcha)
            dd=self.env['uni.student'].browse()
            # print("##################################################",dd)
            old=self.name
            print("#############old##############",old)
            cv+=("Name Changed:"+" "+old+" to "+" "+matcha)
            self.message_post(body=cv)
        if 'stu_id_num' in vals:
            new = vals
            print("#################NEW#################################",new)
            # cv = "<b>" + _("The ordered quantity has been updated.") + "</b><ul>"
            matcha =new.get('stu_id_num')
            # print("*********************************",matcha)
            dd=self.env['uni.student'].browse()
            # print("##################################################",dd)
            old=self.stu_id_num
            print("#############old##############",old)
            cv+=("Roll Changed:"+" "+old+" to "+" "+matcha+"<br>")
            self.message_post(body=cv)
        
        res = super(UniStudent, self).write(vals)
        return res


    # def _update_line_quantity(self, values):
    #     orders = self.mapped('order_id')
    #     for order in orders:
    #         order_lines = self.filtered(lambda x: x.order_id == order)
    #         msg = "<b>" + _("The ordered quantity has been updated.") + "</b><ul>"
    #         for line in order_lines:
    #             msg += "<li> %s: <br/>" % line.product_id.display_name
    #             msg += _(
    #                 "Ordered Quantity: %(old_qty)s -> %(new_qty)s",
    #                 old_qty=line.product_uom_qty,
    #                 new_qty=values["product_uom_qty"]
    #             ) + "<br/>"
    #             if line.product_id.type in ('consu', 'product'):
    #                 msg += _("Delivered Quantity: %s", line.qty_delivered) + "<br/>"
    #             msg += _("Invoiced Quantity: %s", line.qty_invoiced) + "<br/>"
    #         msg += "</ul>"
    #         order.message_post(body=msg

class UniStudentLine(models.Model):
    _name = 'uni.student.line'
    _description = 'Student faculty information.'

    faculty_id = fields.Many2one('uni.faculty', string='Faculty Name')
    faculty_assign_id = fields.Many2one('uni.student', string='Assign ID')
    quantity = fields.Integer(string='Quantity')
