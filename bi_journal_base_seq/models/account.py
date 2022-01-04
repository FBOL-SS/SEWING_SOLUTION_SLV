# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError, ValidationError
import re



class AccountJournal(models.Model):
	_inherit = "account.journal"

	bi_sequence_id = fields.Many2one(comodel_name='ir.sequence',string="Entry Sequence", copy=False)
	bi_sequence_next_number = fields.Integer(string="Next Sequence Number", copy=False, default=1)
	bi_refund_sequence_id = fields.Many2one(comodel_name='ir.sequence',string="Credit Note Entry Sequence", copy=False)
	bi_refund_sequence_next_number = fields.Integer(string="Credit Note Next Number", copy=False ,default=1)

	def write(self,vals):
		res = super(AccountJournal, self).write(vals)
		if 'bi_sequence_next_number' in vals and self.type in ('sale', 'purchase'):
			for rec in self:
				if rec.bi_sequence_id:
					if rec.bi_sequence_id.use_date_range is True and len(rec.bi_sequence_id.date_range_ids) >=1:
						for i in rec.bi_sequence_id.date_range_ids:
							if i.date_from <= self.write_date.date() <= i.date_to:
								i.write({'number_next_actual': vals['bi_sequence_next_number']})
					else:
						rec.bi_sequence_id.write({'number_next_actual': vals['bi_sequence_next_number']})
		if 'bi_refund_sequence_next_number' in vals and self.type in ('sale', 'purchase'):
			for rec in self:
				if rec.bi_sequence_id:
					if rec.bi_refund_sequence_id.use_date_range is True and len(rec.bi_refund_sequence_id.date_range_ids) >=1:
						for i in rec.bi_refund_sequence_id.date_range_ids:
							if i.date_from <= self.write_date.date() <= i.date_to:
								i.write({'number_next_actual': vals['bi_refund_sequence_next_number']})
					else:
						rec.bi_refund_sequence_id.write({'number_next_actual': vals['bi_refund_sequence_next_number']})
		return res


class AccountMove(models.Model):
	_inherit = "account.move"


	custom_seq = fields.Boolean(default=False);

	def _compute_name(self):
		for rec in self:
			if rec.journal_id.type in ('sale','purchase') and rec.move_type in ('in_invoice','in_refund','out_invoice','out_refund') and rec.name in (False, '/'):
				rec.name = '/'
			else:
				super(AccountMove, self)._compute_name()


	def write(self,vals):
		if 'state' in vals:
			if vals['state'] in ('posted'):
				if self.journal_id.type in ('sale','purchase'):
					if self.move_type in ('out_invoice', 'in_invoice','out_receipt','in_receipt'):
						if not self.journal_id.bi_sequence_id:
							raise ValidationError('Add Sequence In Journal')
						else:
							if self.journal_id.bi_sequence_id and self.name in (False, '/'):
								main_seq =self.journal_id.bi_sequence_id.next_by_id()
								if main_seq:
									def_seq = main_seq.split("/")
									if self.journal_id.bi_sequence_id.prefix:
										prefix_split = self.journal_id.bi_sequence_id.prefix.split("/")
										new_seq = False
										flag = False
										count = 0
										for p_split in prefix_split:
											if '%(year)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+ str(self.date.year)
												else:
													new_seq = str(self.date.year)
											elif '%(y)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+self.date.strftime("%y")
												else:
													new_seq = self.date.strftime("%y")
											elif '%(month)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+str(self.date.month)
												else:
													new_seq = str(self.date.month)
											elif '%(day)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+str(self.date.day)
												else:
													new_seq = str(self.date.day)
											elif '%(doy)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+str(self.date.timetuple().tm_yday)
												else:
													new_seq = str(self.date.timetuple().tm_yday)
											elif '%(woy)s' == p_split:
												flag = True
												week_number = self.date.isocalendar()[1]
												if new_seq:
													new_seq = new_seq+'/'+str(week_number)
												else:
													new_seq = str(week_number)
											elif '%(weekday)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+str(self.date.weekday())
												else:
													new_seq = str(self.date.weekday())
											elif '' == p_split:
												if new_seq:
													new_seq = new_seq +'/'+ def_seq[count]
												else:
													new_seq = def_seq[count]
											else:
												if new_seq:
													new_seq = new_seq +'/'+ p_split
												else:
													new_seq = p_split
											count+=1
										if not flag:
											vals['name'] = main_seq
										else:
											vals['name'] = new_seq
									else:
										vals['name'] = main_seq	
								else:
									vals['name'] = main_seq
								if self.journal_id.bi_sequence_id.use_date_range is True and len(self.journal_id.bi_sequence_id.date_range_ids) >=1:
									for i in self.journal_id.bi_sequence_id.date_range_ids:
										if i.date_from <= self.write_date.date() <= i.date_to:
											self.journal_id.write({'bi_sequence_next_number': i.number_next_actual})
								else:
									self.journal_id.write({'bi_sequence_next_number':self.env['ir.sequence'].search([('id', '=', self.journal_id.bi_sequence_id.id)]).number_next_actual})
								vals["name"] = "'" + vals["name"] + "'"
					elif self.move_type in ('out_refund', 'in_refund'):
						if not self.journal_id.bi_refund_sequence_id:
							raise ValidationError('Add Refund/Credit Note Sequence In Journal')
						else:
							if self.journal_id.bi_refund_sequence_id and self.name in (False, '/'):
								main_seq =self.journal_id.bi_refund_sequence_id.next_by_id()
								if main_seq:
									def_seq = main_seq.split("/")
									if self.journal_id.bi_refund_sequence_id.prefix:
										prefix_split = self.journal_id.bi_refund_sequence_id.prefix.split("/")
										new_seq = False
										flag = False
										count = 0
										for p_split in prefix_split:
											if '%(year)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+ str(self.date.year)
												else:
													new_seq = str(self.date.year)
											elif '%(y)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+self.date.strftime("%y")
												else:
													new_seq = self.date.strftime("%y")
											elif '%(month)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+str(self.date.month)
												else:
													new_seq = str(self.date.month)
											elif '%(day)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+str(self.date.day)
												else:
													new_seq = str(self.date.day)
											elif '%(doy)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+str(self.date.timetuple().tm_yday)
												else:
													new_seq = str(self.date.timetuple().tm_yday)
											elif '%(woy)s' == p_split:
												flag = True
												week_number = self.date.isocalendar()[1]
												if new_seq:
													new_seq = new_seq+'/'+str(week_number)
												else:
													new_seq = str(week_number)
											elif '%(weekday)s' == p_split:
												flag = True
												if new_seq:
													new_seq = new_seq+'/'+str(self.date.weekday())
												else:
													new_seq = str(self.date.weekday())
											elif '' == p_split:
												if new_seq:
													new_seq = new_seq +'/'+ def_seq[count]
												else:
													new_seq = def_seq[count]
											else:
												if new_seq:
													new_seq = new_seq +'/'+ p_split
												else:
													new_seq = p_split
											count+=1
										if not flag:
											vals['name'] = main_seq
										else:
											vals['name'] = new_seq
									else:
										vals['name'] = main_seq
								else:
									vals['name'] = main_seq
								if self.journal_id.bi_refund_sequence_id.use_date_range is True and len(self.journal_id.bi_refund_sequence_id.date_range_ids) >=1:
									for i in self.journal_id.bi_refund_sequence_id.date_range_ids:
										if i.date_from <= self.write_date.date() <= i.date_to:
											self.journal_id.write({'bi_refund_sequence_next_number': i.number_next_actual})
								else:
									self.journal_id.write({'bi_refund_sequence_next_number':self.env['ir.sequence'].search([('id', '=', self.journal_id.bi_refund_sequence_id.id)]).number_next_actual})
								vals["name"] = "'" + vals["name"] + "'"
			elif vals['state'] in ('draft','cancel'):
				if self.journal_id.type in ('sale','purchase'):
					for rec in self:
						self.name = rec.name

		return super(AccountMove, self).write(vals)




class SequenceMixinInherit(models.AbstractModel):
	_inherit = 'sequence.mixin'
			

	def _constrains_date_sequence(self):
		for record in self:
			seq = record[record._sequence_field]
			prefix = re.search("'(.*)'", seq)
			if prefix:
				self.name = prefix.group(1)
				pass;
			else:
				return super(SequenceMixinInherit, record)._constrains_date_sequence()