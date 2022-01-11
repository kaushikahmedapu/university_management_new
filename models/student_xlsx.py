from odoo import models

class StudentXlsx(models.AbstractModel):
    _name = 'report.university_management.student_excle'
    _inherit = 'report.report_xlsx.abstract' 
    def generate_xlsx_report(self, workbook, data, partners):
        sheet= workbook.add_worksheet('Card')
        f1= workbook.add_format({'font_size':16, 'align': 'vcenter', 'bold': True})
        f2= workbook.add_format({'font_size':14, 'align': 'vcenter'})
        sheet.write(2, 2, 'Name', f1)
        sheet.write(2, 3, 'ID', f1)
        sheet.write(2, 4, 'Dept', f1)
        aa = 3
        for obj in partners:

            # student_excle = obj.name
            # # One sheet by partner

            

            sheet.write(aa, 2, obj.name, f2)
            sheet.write(aa, 3, obj.stu_id_num, f2)
            sheet.write(aa, 4, obj.department_id.name, f2)
            aa = aa +1


# class FormXlsx(models.AbstractModel):
#     _name = 'report.school_management.report_school_excle'
#     _inherit = 'report.report_xlsx.abstract'

#     def generate_xlsx_report(self, workbook, data, partners):
#         sheet = workbook.add_worksheet('Form')
#         f1 = workbook.add_format(
#             {'font_size': 16, 'align': 'vcenter', 'bold': True})
#         f2 = workbook.add_format({'font_size': 14, 'align': 'vcenter'})
#         sheet.write(2, 2, 'reference Number', f1)
#         sheet.write(2, 3, 'Student Name', f1)
#         sheet.write(2, 4, 'Date', f1)
#         # sheet.write(2, 5, 'State', f1)
#         count = 3
#         for obj in partners:
#             sheet.write(count, 2, obj.reference_number, f2)
#             sheet.write(count, 3, obj.state, f2)
#             sheet.write(count, 4, obj.date.strftime('%d-%m-%Y'), f2)
#             # sheet.write(count, 5, obj.state, f2)
#             count = count + 1





        # bold = workbook.add_format({'bold': True})
        # sheet.write(0, 0, obj.name, bold)