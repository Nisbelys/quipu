# -*- coding: utf-8 -*-

from odoo import models, fields, api

class crm_boton_facturacion(models.Model):
	
	_inherit = 'crm.lead'

	#sale_amount_total = fields.Monetary(compute='_compute_sale_data_inv', string="Sum of Orders", help="Untaxed Total of Confirmed Orders", currency_field='company_currency')
	#sale_order_count = fields.Integer(compute='_compute_sale_data_inv', string="Number of Sale Orders")
	total_invoicedc = fields.Integer(compute='_compute_sale_data_inv', string="Total Invoiced")
	invoice_ids = fields.One2many('account.move', 'oportun_id', string='Orders')
	currency_id = fields.Many2one('res.currency', compute='_get_company_currency', readonly=True,
	    string="Currency", help='Utility field to express amount currency')

	def _get_company_currency(self):
		for partner in self:
			if partner.company_id:
				partner.currency_id = partner.sudo().company_id.currency_id
			else:
				partner.currency_id = self.env.company.currency_id

	def action_view_sale_invoice(self):
		action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
		action['context'] = {
	           'search_default_partner_id': self.partner_id.id,
	           'default_partner_id': self.partner_id.id,
	           'default_ooportun_id': self.id,
	           'default_move_type':'out_invoice',
	           'move_type':'out_invoice', 
	           'journal_type': 'sale', 
	           'search_default_unpaid': 1
	       }
		#action['domain'] = [('oportun_id', '=', self.id), ('state', 'in', ['draft', 'sent'])]		   
		orders = self.env['sale.order'].search([('opportunity_id','=',self.id)])		
		#quotations = self.mapped('invoice_ids').filtered(lambda l: l.state in ('draft', 'sent'))
		quotations = orders.mapped('invoice_ids').filtered(lambda l: l.state in ('draft', 'posted'))
		if len(quotations) == 1:
			action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
			action['res_id'] = quotations.id
		else:
			action['domain'] = [('id','in',quotations.ids),('state', 'in', ['draft', 'posted'])]
		return action					

	#@api.depends('order_ids.state', 'order_ids.currency_id', 'order_ids.amount_untaxed', 'order_ids.date_order', 'order_ids.company_id')	
	def _compute_sale_data_inv(self):
		for lead in self:
			total = 0.0
			quotation_cnt = 0
			sale_order_cnt = 0
			sale_order_obj = self.env['sale.order'].search([('opportunity_id','=',lead.id)])
			company_currency = lead.company_currency or self.env.company.currency_id
			for order in sale_order_obj:
				for inv in order.invoice_ids:
					if inv.state in ('draft', 'posted'):
						quotation_cnt += 1
					if inv.state not in ('draft', 'posted', 'cancel'):
						sale_order_cnt += 1
						total += inv.currency_id._convert(inv.amount_untaxed,company_currency, inv.company_id)
			#lead.sale_amount_total = total
			lead.total_invoicedc = quotation_cnt
			#lead.sale_order_count = sale_order_cnt

class crm_boton_facturacion(models.Model):
	_inherit = 'account.move'

	oportun_id = fields.Many2one('crm.lead', string='Orders')	        