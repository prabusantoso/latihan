# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

# class training_odoo(models.Model):
#     _name = 'training_odoo.training_odoo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class Kursus(models.Model):
    _name = 'training.kursus'

    name = fields.Char(string="Judul", required=True)
    description = fields.Text()
    session_ids = fields.One2many('training.sesi', 'course_id', string="Sesi")
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Penanggung Jawab", index=True)
    
    _sql_constraints = [
                    ('name_description_cek', 'CHECK(name != description)', 'Judul kursus dan keterangan tidak boleh sama '),
                    ('name_unik', 'UNIQUE(name)', 'Judul kursus harus unik')
    ]
    
    
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count([('name', '=like', "Copy of {}%".format(self.name))]) # Searching judul kursus yang sama dan menyimpannya pada variable copied_count 
        
        if not copied_count: # Cek isi variable copied_count (hasil searching) 
            new_name = "Copy of {}".format(self.name) # Jika proses searching judul yang sama tidak ditemukan, maka judul baru akan dikasih imbuhan 'Copy of'
        else:
            new_name = "Copy of {} ({})".format(self.name, copied_count) # Jika proses searching judul yang sama ditemukan, maka judul baru akan dikasih imbuhan 'Copy of' dan angka terakhir duplicate
        
        default['name'] = new_name # Mereplace value field name dengan yang sudah di sesuaikan
        return super(Kursus, self).copy(default)



    
class Sesi(models.Model):
    _name = 'training.sesi'
    
    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Durasi Hari")
    seats = fields.Integer(string="Jumlah Kursi")
    instructor_id = fields.Many2one('res.partner', string="Instruktur", domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', "Pengajar")])
    course_id = fields.Many2one('training.kursus', ondelete='cascade', string="Kursus", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Peserta", domain=[('instructor', '=', False)])
    
    taken_seats = fields.Float(string="Kursi Terisi", compute='_taken_seats')
    
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats: # cek nilai field seats, jika 0 (false), maka masuk kondisi if 
                r.taken_seats = 0.0 # update field taken_seats menjadi 0
            else: # jika tidak masuk kondisi if
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats # update field taken_seats menjadi persentase dari jumlah peserta & kursi
    
                    
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats <= 0: # cek nilai field seats, jika dibawah 0 (negatif), maka masuk kondisi if
            return {
                    'value': {
                              'seats': len(self.attendee_ids) or 1 # mengisi field seats dengan nilai jumlah peserta atau 1
                              },
                    'warning': {
                                'title': "Nilai Jumlah Kursi Salah", # judul pop up
                                'message': "Jumlah Kursi Tidak Boleh Negatif" # pesan pop up
                                }
                    }
            
        if self.seats < len(self.attendee_ids): # cek nilai field seats (jumlah kursi) apakah lebih kecil dari field attendee_ids (jumlah peserta), jika iya maka masuk kondisi if
            return {
                    'value': {
                              'seats': len(self.attendee_ids) # mengisi field seats dengan nilai jumlah peserta
                              },
                    'warning': {
                                'title': "Peserta Terlalu Banyak", # judul pop up
                                'message': "Tambahkan Kursi atau Kurangi Peserta" # pesan pop up
                                }
                    }
            
                
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids: # Jika field instructor_id (Instruktur) diisi DAN instructor_id ada di tabel attendee_ids (Peserta), maka munculkan pesan error 
                raise exceptions.ValidationError("Seorang instruktur tidak boleh menjadi peserta")
    


    
    

    