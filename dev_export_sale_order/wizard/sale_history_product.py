# -*- coding: utf-8 -*-
##############################################################################
#
#    DevIntelle Solution(Odoo Expert)
#    Copyright (C) 2015 Devintelle Soluation (<http://devintellecs.com/>)
#
##############################################################################


from odoo.tools.misc import xlwt
from io import BytesIO
from odoo import fields, models, _
from xlwt import easyxf
from datetime import datetime

class sale_product_history_excel_wizard(models.TransientModel):
    _name ='sale.product.history.excel'

    def sale_product_history_excel(self):
        sale_ids = self._context.get('active_ids')
        sale_order_obj = self.env['sale.order']
        i = 0
        workbook = xlwt.Workbook()
        worksheet = []
        for l in range(0, len(sale_ids)):
            worksheet.append(l)
        for sale_order in sale_order_obj.browse(sale_ids):
            import base64

            filename = 'Sale_Order_Exported.xls'
            worksheet[i] = workbook.add_sheet(sale_order.name)
            worksheet[i].col(0).width = 30 * 30
            worksheet[i].col(1).width = 60 * 60
            worksheet[i].col(2).width = 90 * 90
            worksheet[i].col(3).width = 50 * 50
            worksheet[i].col(4).width = 50 * 50
            worksheet[i].col(5).width = 80 * 80
            worksheet[i].col(6).width = 60 * 60
            counter = 2

            header_style = easyxf('font:height 300;pattern: pattern solid, fore_color 0x3F; align: horiz center;font:bold True;')
            sub_header = easyxf('font:height 210;pattern: pattern solid, fore_color silver_ega;font:bold True;')
            content = easyxf('font:height 200;')

            heading = ''
            if sale_order.state in ['draft', 'sent']:
                heading = 'Quotation' + ' (' + str(sale_order.name) + ')'
            if sale_order.state not in ['draft', 'sent']:
                heading = 'Sale Order' + ' (' + str(sale_order.name) + ')'
            worksheet[i].write_merge(counter, 3, counter, 3, heading, header_style)
            counter += 3

            worksheet[i].write(counter, 1, 'Customer', sub_header)
            worksheet[i].write(counter, 2, sale_order.partner_id.name or '', content)
            n_final_date = ' '

            if sale_order.date_order:
                final_date = datetime.strptime(str(sale_order.date_order), '%Y-%m-%d %H:%M:%S').date()
                n_final_date = final_date.strftime('%m-%d-%Y')
            worksheet[i].write(counter, 5, 'Order Date', sub_header)
            worksheet[i].write(counter, 6, n_final_date, content)
            counter += 1
            worksheet[i].write(counter, 2, sale_order.partner_id.street or '', content)
            counter += 1
            worksheet[i].write(counter, 2, sale_order.partner_id.street2 or '', content)
            counter += 1
            worksheet[i].write(counter, 2, sale_order.partner_id.city or '', content)
            counter += 2

            worksheet[i].write(counter, 0, 'No', sub_header)
            worksheet[i].write(counter, 1, 'Code', sub_header)
            worksheet[i].write(counter, 2, 'Product', sub_header)
            worksheet[i].write(counter, 3, 'Quantity', sub_header)
            worksheet[i].write(counter, 4, 'Uom', sub_header)
            worksheet[i].write(counter, 5, 'Price', sub_header)
            worksheet[i].write(counter, 6, 'Subtotal', sub_header)
            counter += 1

            number = 1
            for vals in sale_order.order_line:
                worksheet[i].write(counter, 0, number, content)
                worksheet[i].write(counter, 1, vals.product_id.default_code or '', content)
                worksheet[i].write(counter, 2, vals.product_id.name or '', content)
                worksheet[i].write(counter, 3, vals.product_uom_qty or '', content)
                worksheet[i].write(counter, 4, vals.product_uom.name or '', content)
                worksheet[i].write(counter, 5, "%.2f" % vals.price_unit or '', content)
                worksheet[i].write(counter, 6, "%.2f" % vals.price_subtotal or '', content)
                counter += 1
                number += 1

            counter += 1
            worksheet[i].write(counter, 5, 'Untaxed Amount', sub_header)
            worksheet[i].write(counter, 6, "%.2f" % sale_order.amount_untaxed or '', content)
            counter += 1
            worksheet[i].write(counter, 5, 'Tax Amount', sub_header)
            worksheet[i].write(counter, 6, "%.2f" % sale_order.amount_tax or '', content)
            counter += 1
            worksheet[i].write(counter, 5, 'Total', sub_header)
            worksheet[i].write(counter, 6, "%.2f" % sale_order.amount_total or '', content)
            i += 1

        fp = BytesIO()
        workbook.save(fp)

        export_id = self.env['sale.product.excel'].create({'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
        fp.close()

        return {
            'view_mode': 'form',
            'res_id': export_id.id,
            'res_model': 'sale.product.excel',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'target': 'new',
        }


     
sale_product_history_excel_wizard()


class sale_product_excel(models.TransientModel):
    _name= "sale.product.excel"

    excel_file = fields.Binary('Excel File')
    file_name = fields.Char('Excel File', size=64)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
