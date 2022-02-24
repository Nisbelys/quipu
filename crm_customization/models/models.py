# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rescompany(models.Model):
	_inherit = "res.company"

	pestana_notas = fields.Boolean('Pestaña notas', default=False)
	pestana_informacion_adicional = fields.Boolean('Pestaña notas', default=False)



class resconfig(models.TransientModel):
	_inherit = "res.config.settings"

	pestana_notas = fields.Boolean(related="company_id.pestana_notas", readonly=False)
	pestana_informacion_adicional = fields.Boolean(related="company_id.pestana_informacion_adicional", readonly=False)

class CrmLead(models.Model):
	_inherit = "crm.lead"

	pestana_notas = fields.Boolean(related="company_id.pestana_notas")
	pestana_informacion_adicional = fields.Boolean(related="company_id.pestana_informacion_adicional")
