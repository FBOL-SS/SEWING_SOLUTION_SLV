# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"
    
    weight = fields.Float(
        string="Weight",
        help="Weight in KG"

    )
    number_of_packages = fields.Float(
        string="Number Of Packages"
    )
    transporte_id = fields.Char(
        string="Medio de Transporte"
    )
    no_orden = fields.Char(
        string="Número de PO"
    )
    consignacion = fields.Char(
        string="ID de Consignación"
    )

