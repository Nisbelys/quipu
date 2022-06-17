# -*- coding: utf-8 -*-
from odoo import models,fields, api
from odoo.tools.misc import get_lang

import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_invoice_sent_quipu8(self):
        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
        lang = False
        if template:
            lang = template._render_lang(self.ids)[self.id]
        if not lang:
            lang = get_lang(self.env).code
        compose_form = self.env.ref('account.account_invoice_send_wizard_form', raise_if_not_found=False)
        ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            # For the sake of consistency we need a default_res_model if
            # default_res_id is set. Not renaming default_model as it can
            # create many side-effects.
            default_res_model='account.move',
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='manual',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            model_description=self.with_context(lang=lang).type_name,
            force_email=True,
            active_ids=[self.id]
        )
        sent_obj = self.env['account.invoice.send'].with_context(**ctx).create({'composition_mode':'mass_mail'})
        sent_obj.send_and_print_action()
        return True


class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'
    
    @api.model
    def _auto_send_and_print(self):
        #invoices = self.env['account.move'].search([('state','=','posted'),('move_type','in',['out_invoice','out_refund']),('id','in',[848,849])])
        active_ids = self._context.get('active_ids', False)        
        if not active_ids:
            domain = [('state','=','posted'),('move_type','in',['out_invoice','out_refund']),('is_move_sent','!=',True)]        
            active_ids = self.env['account.move'].search(domain).ids
        _logger.info('Total Factura: %s'%active_ids)
        
        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
        lang = False
        lang = get_lang(self.env).code
        _logger.info('template: %s'%template)
        ctx = dict(
            default_model='account.move',
            #default_res_ids=active_ids,
            default_res_model='account.move',
            #default_use_template=bool(template),
            #default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            #model_description=invoices[0].with_context(lang=lang).type_name,
            force_email=True,
            active_model='account.move',
            active_ids = active_ids
            )            

        model_sap = self.with_context(**ctx).create({'composition_mode':'mass_mail'})
        _logger.info('Envio: %s'%model_sap.subject)
        model_sap.send_and_print_action()

class ContractContract(models.Model):
    _inherit = 'contract.contract'

    sale_type_id = fields.Many2one(
        comodel_name="sale.order.type",
        string="Sale Type",
        store=True,
        ondelete="restrict",
        copy=True,
    )
  
    l10n_pe_edi_operation_type = fields.Selection(
        [
            ("1", "INTERNAL SALE"),
            ("2", "EXPORTATION"),
            ("3", "NON-DOMICILED"),
            ("4", "INTERNAL SALE - ADVANCES"),
            ("5", "ITINERANT SALE"),
            ("6", "GUIDE INVOICE"),
            ("7", "SALE PILADO RICE"),
            ("8", "INVOICE - PROOF OF PERCEPTION"),
            ("10", "INVOICE - SENDING GUIDE"),
            ("11", "INVOICE - CARRIER GUIDE"),
            ("12", "SALES TICKET - PROOF OF PERCEPTION"),
            ("13", "NATURAL PERSON DEDUCTIBLE EXPENSE"),
        ],
        string="Transaction type",
        help="Default 1, the others are for very special types of operations, do not hesitate to consult with us for more information",
        default="1"
    )    

    @api.depends("partner_id", "company_id")
    def _compute_sale_type_id(self):
        # If create invoice from sale order, sale type will not computed.
        if not self.env.context.get("default_move_type", False) or self.env.context.get(
            "active_model", False
        ) in ["sale.order", "sale.advance.payment.inv","contract.contract"]:
            return
        self.sale_type_id = self.env["sale.order.type"]
        for record in self:
            if record.move_type not in ["out_invoice", "out_refund"]:
                record.sale_type_id = self.env["sale.order.type"]
                continue
            else:
                record.sale_type_id = record.sale_type_id
            if not record.partner_id:
                record.sale_type_id = self.env["sale.order.type"].search(
                    [("company_id", "in", [self.env.company.id, False])], limit=1
                )
            else:
                sale_type = (
                    record.partner_id.with_company(record.company_id).sale_type
                    or record.partner_id.commercial_partner_id.with_company(
                        record.company_id
                    ).sale_type
                )
                if sale_type:
                    record.sale_type_id = sale_type    

    def _recurring_create_invoice(self, date_ref=False):
        moves = super(ContractContract, self)._recurring_create_invoice(date_ref)
        for move in moves:
            move.action_post()
            move.with_context(quipu8_mail_sent=True).action_invoice_sent_quipu8()
        return moves                    

    def _prepare_invoice(self, date_invoice, journal=None):
        invoice_vals, move_form = super(ContractContract, self)._prepare_invoice(date_invoice, journal)
        invoice_vals['sale_type_id'] = self.sale_type_id.id
        invoice_vals['l10n_pe_edi_operation_type'] = self.l10n_pe_edi_operation_type
        return invoice_vals, move_form
    