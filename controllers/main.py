from odoo import models, fields, api,  _
from odoo import http
from odoo.http import request
class Student(http.Controller):

    @http.route('/student', type='http', auth='public', website=True)
    def student_details(self , **kwargs):
         student_details = request.env['uni.student'].sudo().search([])
        #  print("################################################DADA###############################3")
         return request.redirect('/web#action=404&model=uni.student&view_type=list&cids=1&menu_id=263') 