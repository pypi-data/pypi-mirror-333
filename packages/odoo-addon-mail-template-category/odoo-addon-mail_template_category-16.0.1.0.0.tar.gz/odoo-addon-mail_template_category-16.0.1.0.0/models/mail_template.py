from odoo import models, api, fields

class MailTemplate(models.Model):
    _inherit = "mail.template"

    category = fields.Many2one('mail.template.category')
