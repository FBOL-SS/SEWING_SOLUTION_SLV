# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError, ValidationError
import re
import logging

_logger = logging.getLogger(__name__)

class AccountJournal(models.Model):
    _inherit = "account.journal"

    bi_sequence_id = fields.Many2one(comodel_name='ir.sequence', string="Entry Sequence", copy=False)
    bi_sequence_next_number = fields.Integer(string="Next Sequence Number", copy=False, default=1)
    bi_refund_sequence_id = fields.Many2one(comodel_name='ir.sequence', string="Credit Note Entry Sequence", copy=False)
    bi_refund_sequence_next_number = fields.Integer(string="Credit Note Next Number", copy=False, default=1)

    def write(self, vals):
        res = super(AccountJournal, self).write(vals)
        if 'bi_sequence_next_number' in vals and self.type in ('sale', 'purchase'):
            for rec in self:
                if rec.bi_sequence_id:
                    if rec.bi_sequence_id.use_date_range is True and len(rec.bi_sequence_id.date_range_ids) >= 1:
                        for i in rec.bi_sequence_id.date_range_ids:
                            if i.date_from <= self.write_date.date() <= i.date_to:
                                i.write({'number_next_actual': vals['bi_sequence_next_number']})
                    else:
                        rec.bi_sequence_id.write({'number_next_actual': vals['bi_sequence_next_number']})
        if 'bi_refund_sequence_next_number' in vals and self.type in ('sale', 'purchase'):
            for rec in self:
                if rec.bi_refund_sequence_id:
                    if rec.bi_refund_sequence_id.use_date_range is True and len(rec.bi_refund_sequence_id.date_range_ids) >= 1:
                        for i in rec.bi_refund_sequence_id.date_range_ids:
                            if i.date_from <= self.write_date.date() <= i.date_to:
                                i.write({'number_next_actual': vals['bi_refund_sequence_next_number']})
                    else:
                        rec.bi_refund_sequence_id.write({'number_next_actual': vals['bi_refund_sequence_next_number']})
        return res


class AccountMove(models.Model):
    _inherit = "account.move"

    custom_seq = fields.Boolean(default=False)

    def _compute_name(self):
        for rec in self:
            if rec.journal_id.type in ('sale', 'purchase') and rec.move_type in ('in_invoice', 'in_refund', 'out_invoice', 'out_refund') and rec.name in (False, '/'):
                rec.name = '/'
            else:
                super(AccountMove, self)._compute_name()

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'posted':
            if self.journal_id.type in ('sale', 'purchase'):
                if self.move_type in ('out_invoice', 'in_invoice', 'out_receipt', 'in_receipt'):
                    if not self.journal_id.bi_sequence_id:
                        raise ValidationError('Add Sequence In Journal')
                    else:
                        if self.journal_id.bi_sequence_id and self.name in (False, '/'):
                            main_seq = self.journal_id.bi_sequence_id.next_by_id()
                            vals['name'] = main_seq
                        if self.journal_id.bi_sequence_id.use_date_range is True and len(self.journal_id.bi_sequence_id.date_range_ids) >= 1:
                            for i in self.journal_id.bi_sequence_id.date_range_ids:
                                if i.date_from <= self.write_date.date() <= i.date_to:
                                    self.journal_id.write({'bi_sequence_next_number': i.number_next_actual})
                        else:
                            self.journal_id.write({'bi_sequence_next_number': self.journal_id.bi_sequence_id.number_next_actual})
                elif self.move_type in ('out_refund', 'in_refund'):
                    if not self.journal_id.bi_refund_sequence_id:
                        raise ValidationError('Add Refund/Credit Note Sequence In Journal')
                    else:
                        if self.journal_id.bi_refund_sequence_id and self.name in (False, '/'):
                            main_seq = self.journal_id.bi_refund_sequence_id.next_by_id()
                            vals['name'] = main_seq
                        if self.journal_id.bi_refund_sequence_id.use_date_range is True and len(self.journal_id.bi_refund_sequence_id.date_range_ids) >= 1:
                            for i in self.journal_id.bi_refund_sequence_id.date_range_ids:
                                if i.date_from <= self.write_date.date() <= i.date_to:
                                    self.journal_id.write({'bi_refund_sequence_next_number': i.number_next_actual})
                        else:
                            self.journal_id.write({'bi_refund_sequence_next_number': self.journal_id.bi_refund_sequence_id.number_next_actual})
        elif 'state' in vals and vals['state'] in ('draft', 'cancel'):
            if self.journal_id.type in ('sale', 'purchase'):
                for rec in self:
                    self.name = rec.name

        return super(AccountMove, self).write(vals)


class SequenceMixinInherit(models.AbstractModel):
    _inherit = 'sequence.mixin'

    def _constrains_date_sequence(self):
        for record in self:
            seq = record[record._sequence_field]

            # Ensure seq is a valid string
            if not seq or not isinstance(seq, str):
                _logger.warning(f"Invalid sequence for record {record.id}: {seq}")
                continue  # Skip processing for invalid sequences

            prefix = re.search("'(.*)'", seq)
            if prefix:
                self.name = prefix.group(1)
            else:
                return super(SequenceMixinInherit, record)._constrains_date_sequence()
