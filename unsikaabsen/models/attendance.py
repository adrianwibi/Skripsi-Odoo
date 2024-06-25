from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError, ValidationError, AccessError
from datetime import datetime, timedelta


class Attendance(models.Model):
    _name = 'unsikaabsen.attendance'
    _description = 'Absensi'
    _rec_name = 'name'

    name = fields.Char(string='Nama Kelas', readonly=True, compute='_compute_name', store=True)
    kelas_name = fields.Char(string='Nama Kelas')
    description = fields.Text(string='Catatan')
    start_date = fields.Datetime(string='Tanggal', required=True, default=fields.Datetime.now)
    duration = fields.Integer(string='Durasi Kelas (Jam)')
    number_of_seats = fields.Integer(string='Kapasitas Kelas')
    taken_seats = fields.Integer(string='Kursi Terisi', compute='_count_taken_seats')

    matkul_id = fields.Many2one('unsikaabsen.matkul', string='Mata Kuliah', required=True)
    dosen_id = fields.Many2one('res.partner', string='Dosen')
    document = fields.Binary(string='Materi')

    attendance_ids = fields.One2many('unsikaabsen.attendance.line', 'attendance_id', string='Absensi')

    @api.model
    def create(self, vals):
        if not self.env.user.has_group('unsikaabsen.group_dosen'):
            raise AccessError("Hanya dosen yang bisa membuat jadwal.")
        return super(Attendance, self).create(vals)

    @api.depends('kelas_name', 'matkul_id')
    def _compute_name(self):
        for rec in self:
            if rec.kelas_name and rec.matkul_id:
                rec.name = f"{rec.kelas_name} - {rec.matkul_id.name}"

    def action_absen(self):
            if self.env.user.has_group('unsikaabsen.group_mahasiswa'):
                # Menghitung jumlah siswa yang sudah absen
                num_absen = len(self.attendance_ids)
                if num_absen >= self.number_of_seats:
                    raise exceptions.ValidationError("Kelas ini sudah mencapai batas maksimum absensi.")

                # Memeriksa apakah mahasiswa sudah absen sebelumnya
                existing_absen = self.env['unsikaabsen.attendance.line'].search([
                    ('user_id', '=', self.env.user.id),
                    ('attendance_id', '=', self.id)
                ])
                if existing_absen:
                    raise exceptions.ValidationError("Anda hanya bisa absen sekali untuk setiap kelas.")

                # Menentukan state
                now = datetime.now()
                start = fields.Datetime.from_string(self.start_date)
                end = start + timedelta(hours=self.duration)

                if now < start:
                    state = 'terlalu_awal'
                elif start <= now <= end:
                    state = 'hadir'
                else:
                    state = 'terlambat'

                # Membuat record absensi baru
                self.env['unsikaabsen.attendance.line'].create({
                    'attendance_id': self.id,
                    'user_id': self.env.user.id,
                    'state': state,
                #  'image': self.env.context.get('image')  # Asumsikan gambar diambil dan dikirim melalui context
                })

    @api.onchange('matkul_id')
    def _onchange_matkul_id(self):
        if self.matkul_id:
            self.dosen_id = self.matkul_id.dosen_id.id


    @api.depends('attendance_ids', 'number_of_seats')
    def _count_taken_seats(self):
        for rec in self:
            if rec.number_of_seats:
                rec.taken_seats = len(rec.attendance_ids) / rec.number_of_seats * 100
            else:
                rec.taken_seats = 0


class AttendanceLine(models.Model):
   _name = 'unsikaabsen.attendance.line'
   _description = 'Absensi Mahasiswa'

   attendance_id = fields.Many2one('unsikaabsen.attendance', string='Attendance', required=True)
   user_id = fields.Many2one('res.users', string='Mahasiswa', required=True)
   absen_date = fields.Datetime(string='Tanggal Absen', default=fields.Datetime.now)
   state = fields.Selection([
      ('terlalu_awal', 'Terlalu Awal'),
      ('hadir', 'Hadir'),
      ('terlambat', 'Terlambat'),
      ('tidak_hadir', 'Tidak Hadir')
   ], string='Status Kehadiran', default='tidak_hadir')
   

