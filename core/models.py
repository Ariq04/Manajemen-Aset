# core/models.py

class AsetIT:
    def __init__(self, id_aset, nama, status, lokasi, harga_awal, tgl_pembelian):
        self.id_aset = id_aset
        self.nama = nama
        self.status = status
        self.lokasi = lokasi
        self.__harga_awal = float(harga_awal)
        self.tgl_pembelian = str(tgl_pembelian)

    def get_harga(self):
        return self.__harga_awal

    def hitung_penyusutan(self, tahun_sekarang):
        try:
            umur = tahun_sekarang - int(self.tgl_pembelian.split('-')[0])
        except (ValueError, IndexError):
            umur = 0
        return (self.__harga_awal / 5) * umur

class Laptop(AsetIT):
    def __init__(self, id_aset, nama, status, lokasi, harga_awal, tgl_pembelian, ukuran_layar, tipe="Laptop", **kwargs):
        super().__init__(id_aset, nama, status, lokasi, harga_awal, tgl_pembelian)
        self.tipe = tipe
        self.ukuran_layar = ukuran_layar

    def hitung_penyusutan(self, tahun_sekarang):
        try:
            umur = tahun_sekarang - int(self.tgl_pembelian.split('-')[0])
        except (ValueError, IndexError):
            umur = 0
        nilai_penyusutan = (self.get_harga() / 4) * umur
        return max(0, nilai_penyusutan)

    def to_dict(self):
        return {
            'id_aset': self.id_aset, 'nama': self.nama, 'status': self.status,
            'lokasi': self.lokasi, 'harga_awal': self.get_harga(),
            'tgl_pembelian': self.tgl_pembelian, 'tipe': self.tipe,
            'ukuran_layar': self.ukuran_layar, 'kapasitas_ram': '',
            'jenis_tinta': '', 'kecepatan_cetak_ppm': ''
        }

class Server(AsetIT):
    def __init__(self, id_aset, nama, status, lokasi, harga_awal, tgl_pembelian, kapasitas_ram, tipe="Server", **kwargs):
        super().__init__(id_aset, nama, status, lokasi, harga_awal, tgl_pembelian)
        self.tipe = tipe
        self.kapasitas_ram = kapasitas_ram

    def hitung_penyusutan(self, tahun_sekarang):
        try:
            umur = tahun_sekarang - int(self.tgl_pembelian.split('-')[0])
        except (ValueError, IndexError):
            umur = 0
        nilai_penyusutan = (self.get_harga() / 7) * umur
        return max(0, nilai_penyusutan)

    def to_dict(self):
        return {
            'id_aset': self.id_aset, 'nama': self.nama, 'status': self.status,
            'lokasi': self.lokasi, 'harga_awal': self.get_harga(),
            'tgl_pembelian': self.tgl_pembelian, 'tipe': self.tipe,
            'ukuran_layar': '', 'kapasitas_ram': self.kapasitas_ram,
            'jenis_tinta': '', 'kecepatan_cetak_ppm': ''
        }

class Printer(AsetIT):
    def __init__(self, id_aset, nama, status, lokasi, harga_awal, tgl_pembelian, jenis_tinta, kecepatan_cetak_ppm, tipe="Printer", **kwargs):
        super().__init__(id_aset, nama, status, lokasi, harga_awal, tgl_pembelian)
        self.tipe = tipe
        self.jenis_tinta = jenis_tinta
        self.kecepatan_cetak_ppm = kecepatan_cetak_ppm

    def hitung_penyusutan(self, tahun_sekarang):
        try:
            umur = tahun_sekarang - int(self.tgl_pembelian.split('-')[0])
        except (ValueError, IndexError):
            umur = 0
        nilai_penyusutan = (self.get_harga() / 5) * umur
        return max(0, nilai_penyusutan)

    def to_dict(self):
        return {
            'id_aset': self.id_aset, 'nama': self.nama, 'status': self.status,
            'lokasi': self.lokasi, 'harga_awal': self.get_harga(),
            'tgl_pembelian': self.tgl_pembelian, 'tipe': self.tipe,
            'ukuran_layar': '', 'kapasitas_ram': '',
            'jenis_tinta': self.jenis_tinta, 'kecepatan_cetak_ppm': self.kecepatan_cetak_ppm
        }