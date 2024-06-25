from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        user = super(ResUsers, self).create(vals)
        group_mahasiswa = self.env.ref('unsikaabsen.group_mahasiswa')
        if group_mahasiswa:
            group_mahasiswa.users = [(4, user.id)]
        return user
