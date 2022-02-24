# -*- coding: utf-8 -*-
# from odoo import http


# class CrmCustomization(http.Controller):
#     @http.route('/crm_customization/crm_customization/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_customization/crm_customization/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_customization.listing', {
#             'root': '/crm_customization/crm_customization',
#             'objects': http.request.env['crm_customization.crm_customization'].search([]),
#         })

#     @http.route('/crm_customization/crm_customization/objects/<model("crm_customization.crm_customization"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_customization.object', {
#             'object': obj
#         })
