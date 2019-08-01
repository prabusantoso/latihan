# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Patner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("instuktur")
    session_ids = fields.Many2many('training.sesi', string="Menghadiri Sesi",readonly=True)

