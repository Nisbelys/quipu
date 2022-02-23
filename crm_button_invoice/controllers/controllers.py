# -*- coding: utf-8 -*-
# from odoo import http


# class CrmButtonInvoice(http.Controller):
#     @http.route('/crm_button_invoice/crm_button_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_button_invoice/crm_button_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_button_invoice.listing', {
#             'root': '/crm_button_invoice/crm_button_invoice',
#             'objects': http.request.env['crm_button_invoice.crm_button_invoice'].search([]),
#         })

#     @http.route('/crm_button_invoice/crm_button_invoice/objects/<model("crm_button_invoice.crm_button_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_button_invoice.object', {
#             'object': obj
#         })
