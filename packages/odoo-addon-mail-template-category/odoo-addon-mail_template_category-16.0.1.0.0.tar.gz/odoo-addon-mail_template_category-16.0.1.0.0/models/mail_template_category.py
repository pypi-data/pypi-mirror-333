from odoo import models, api, fields

class MailTemplateCategory(models.Model):
    _name = 'mail.template.category'
    _description = 'Mail Template Category'
    _inherit='res.partner.category'
    _order = 'name'
    _parent_store = True
