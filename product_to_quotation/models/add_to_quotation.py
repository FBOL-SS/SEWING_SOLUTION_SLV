# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Mashood K.U (Contact : odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################
from odoo import models, fields, api, _


class AddToQuotation(models.Model):
    _inherit = 'product.product'

    def add_to_quot(self):
        active_id = self._context.get('active_id')
        quot_id = self.env['sale.order'].search([('id', '=', active_id)])
        name = self.product_tmpl_id.name_get()[0][1]
        if self.product_tmpl_id.description_sale:
            name += '\n' + self.product_tmpl_id.description_sale
        vals = [(0, 0, {'product_id': self.id, 'name': name})]
        quot_id.order_line = vals


class SmartButton(models.Model):
    _inherit = 'sale.order'

    add_to_quot_active = fields.Boolean(default=False)

    def action_view_products(self):
        return {
            'name': _('Product Variants'),
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'res_model': 'product.product',
            'type': 'ir.actions.act_window',
            'target': '_blank',
            'context': {'is_sale_view': True}
        }
