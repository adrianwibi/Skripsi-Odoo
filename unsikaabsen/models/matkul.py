from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, AccessError

class Matkul(models.Model):
   _name = 'unsikaabsen.matkul'
   _description = 'Mata Kuliah'

   name = fields.Char(string='Nama Mata Kuliah')
   description = fields.Text(string='Keterangan')
   
   dosen_id = fields.Many2one(
       string='Dosen Pengampu',
       comodel_name='res.partner',
   )
   
   @api.model
   def create(self, vals):
      # Check if the user is not in the 'dosen' group and it's not a system operation
      if not self.env.user.has_group('unsikaabsen.group_dosen') and self.env.user.id != 1:
         raise AccessError("Hanya dosen yang bisa membuat mata kuliah.")
      return super(Matkul, self).create(vals)

   def write(self, vals):
      # Check if the user is not in the 'dosen' group and it's not a system operation
      if not self.env.user.has_group('unsikaabsen.group_dosen') and self.env.user.id != 1:
         raise AccessError("Hanya dosen yang bisa mengubah mata kuliah.")
      return super(Matkul, self).write(vals)
   