import datetime
import json
import os
from typing import Dict, List, Tuple

class TesKesehatan:
    def __init__(self):
        self.data_pengguna = {}
        self.hasil_analisis = {}
        
    def bersihkan_layar(self):
        """Membersihkan layar konsol"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def tampilkan_header(self, judul):
        """Menampilkan header yang rapi"""

        print("=" * 50)
        print(f"{judul:^50}")
        print("=" * 50)
    
    def input_angka(self, prompt, min_val=None, max_val=None):
        """Validasi input angka"""
        while True:
            try:
                nilai = float(input(prompt))
                if min_val is not None and nilai < min_val:
                    print(f"Nilai minimal adalah {min_val}")
                    continue
                if max_val is not None and nilai > max_val:
                    print(f"Nilai maksimal adalah {max_val}")
                    continue
                return nilai
            except ValueError:
                print("Harap masukkan angka yang valid!")
    
    def kumpulkan_data_dasar(self):
        """Mengumpulkan data dasar pengguna"""
        self.tampilkan_header("DATA DASAR PENGUNA")
        
        self.data_pengguna['nama'] = input("Nama Lengkap: ")
        self.data_pengguna['tanggal'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("\n--- Data Fisik ---")
        self.data_pengguna['usia'] = self.input_angka("Usia (tahun): ", 1, 120)
        self.data_pengguna['jenis_kelamin'] = self.pilih_jenis_kelamin()
        self.data_pengguna['berat'] = self.input_angka("Berat Badan (kg): ", 20, 300)
        self.data_pengguna['tinggi'] = self.input_angka("Tinggi Badan (cm): ", 100, 250)
        
        print("\n--- Kontak Darurat ---")
        self.data_pengguna['kontak_darurat'] = input("Nomor Kontak Darurat: ")
    
    def pilih_jenis_kelamin(self):
        """Memilih jenis kelamin"""
        while True:
            print("Jenis Kelamin:")
            print("1. Laki-laki")
            print("2. Perempuan")
            pilihan = input("Pilih (1/2): ")
            if pilihan == '1':
                return 'Laki-laki'
            elif pilihan == '2':
                return 'Perempuan'
            else:
                print("Pilihan tidak valid!")
    
    def hitung_bmi(self) -> Tuple[float, str]:
        """Menghitung BMI dan kategori"""
        tinggi_m = self.data_pengguna['tinggi'] / 100
        bmi = self.data_pengguna['berat'] / (tinggi_m ** 2)
        
        if bmi < 18.5:
            kategori = "Kurus"
            risiko = "Rendah"
            rekomendasi = "Perbanyak asupan kalori dan protein, konsultasi dengan ahli gizi"
        elif 18.5 <= bmi < 25:
            kategori = "Normal"
            risiko = "Rendah"
            rekomendasi = "Pertahankan pola makan sehat dan olahraga teratur"
        elif 25 <= bmi < 30:
            kategori = "Gemuk"
            risiko = "Sedang"
            rekomendasi = "Kurangi asupan kalori, tingkatkan aktivitas fisik"
        else:
            kategori = "Obesitas"
            risiko = "Tinggi"
            rekomendasi = "Segera konsultasi dengan dokter, diet terkontrol, olahraga rutin"
        
        return bmi, kategori, risiko, rekomendasi
    
    def hitung_kebutuhan_kalori(self) -> float:
        """Menghitung kebutuhan kalori harian (Harris-Benedict)"""
        if self.data_pengguna['jenis_kelamin'] == 'Laki-laki':
            bmr = 88.362 + (13.397 * self.data_pengguna['berat']) + \
                  (4.799 * self.data_pengguna['tinggi']) - (5.677 * self.data_pengguna['usia'])
        else:
            bmr = 447.593 + (9.247 * self.data_pengguna['berat']) + \
                  (3.098 * self.data_pengguna['tinggi']) - (4.330 * self.data_pengguna['usia'])
        
        # Aktifitas
        print("\n--- Tingkat Aktivitas Fisik ---")
        print("1. Sedentary (jarang olahraga)")
        print("2. Ringan (olahraga 1-3 hari/minggu)")
        print("3. Sedang (olahraga 3-5 hari/minggu)")
        print("4. Berat (olahraga 6-7 hari/minggu)")
        print("5. Sangat Berat (olahraga 2x sehari)")
        
        aktivitas = self.input_angka("Pilih tingkat aktivitas (1-5): ", 1, 5)
        
        faktor_aktivitas = [1.2, 1.375, 1.55, 1.725, 1.9]
        kebutuhan_kalori = bmr * faktor_aktivitas[int(aktivitas) - 1]
        
        return kebutuhan_kalori
    
    def kuesioner_gaya_hidup(self) -> Dict:
        """Kuesioner gaya hidup dan kebiasaan"""
        self.tampilkan_header("KUESIONER GAYA HIDUP")
        
        gaya_hidup = {}
        
        print("\n--- Kebiasaan Makan (1-5, 1=Jarang, 5=Sangat Sering) ---")
        gaya_hidup['sayur_buah'] = self.input_angka("Konsumsi sayur dan buah: ", 1, 5)
        gaya_hidup['makan_cepat'] = self.input_angka("Konsumsi makanan cepat saji: ", 1, 5)
        gaya_hidup['minum_manis'] = self.input_angka("Konsumsi minuman manis: ", 1, 5)
        gaya_hidup['sarapan'] = self.input_angka("Frekuensi sarapan pagi: ", 1, 5)
        
        print("\n--- Aktivitas Fisik ---")
        gaya_hidup['olahraga'] = self.input_angka("Frekuensi olahraga per minggu: ", 0, 14)
        gaya_hidup['waktu_duduk'] = self.input_angka("Rata-rata duduk per hari (jam): ", 0, 24)
        
        print("\n--- Kebiasaan Lain ---")
        gaya_hidup['merokok'] = input("Apakah merokok? (y/n): ").lower() == 'y'
        if gaya_hidup['merokok']:
            gaya_hidup['rokok_perhari'] = self.input_angka("Jumlah rokok per hari: ", 1, 100)
        
        gaya_hidup['alkohol'] = input("Konsumsi alkohol? (y/n): ").lower() == 'y'
        gaya_hidup['tidur'] = self.input_angka("Rata-rata jam tidur per malam: ", 0, 24)
        
        print("\n--- Kesehatan Mental ---")
        gaya_hidup['stres'] = self.input_angka("Tingkat stres (1-10): ", 1, 10)
        gaya_hidup['istirahat'] = self.input_angka("Kualitas istirahat (1-10): ", 1, 10)
        
        return gaya_hidup
    
    def cek_gejala(self) -> List[str]:
        """Memeriksa gejala yang dialami"""
        self.tampilkan_header("PEMERIKSAAN GEJALA")
        
        gejala_list = []
        gejala_mapping = {
            '1': ('Demam', 1),
            '2': ('Batuk', 1),
            '3': ('Sesak napas', 2),
            '4': ('Nyeri dada', 3),
            '5': ('Pusing', 1),
            '6': ('Mual', 1),
            '7': ('Kelelahan ekstrem', 2),
            '8': ('Penurunan berat badan drastis', 3),
            '9': ('Nyeri sendi', 1),
            '10': ('Gangguan penglihatan', 3)
        }
        
        print("Gejala yang dialami (pilih angka, pisahkan dengan koma):")
        for key, (gejala, _) in gejala_mapping.items():
            print(f"{key}. {gejala}")
        
        pilihan = input("\nMasukkan pilihan (contoh: 1,3,5) atau kosongkan jika tidak ada: ")
        
        if pilihan.strip():
            pilihan_list = [p.strip() for p in pilihan.split(',')]
            for p in pilihan_list:
                if p in gejala_mapping:
                    gejala_list.append(gejala_mapping[p][0])
        
        return gejala_list
    
    def analisis_risiko(self, gaya_hidup: Dict, gejala: List[str]) -> Dict:
        """Menganalisis risiko kesehatan berdasarkan gaya hidup dan gejala"""
        skor_risiko = 0
        faktor_risiko = []
        rekomendasi_khusus = []
        
        # Analisis BMI
        bmi, kategori, risiko_bmi, rekom_bmi = self.hitung_bmi()
        if kategori in ["Gemuk", "Obesitas"]:
            skor_risiko += 2
            faktor_risiko.append("Berat badan berlebih")
        elif kategori == "Kurus":
            skor_risiko += 1
            faktor_risiko.append("Berat badan kurang")
        
        # Analisis gaya hidup
        if['sayur_buah'] < 3:
            skor_risiko += 1
            faktor_risiko.append("Kurang konsumsi sayur/buah")
            rekomendasi_khusus.append("Tingkatkan konsumsi sayur dan buah minimal 5 porsi per hari")
        
        if['makan_cepat'] > 3:
            skor_risiko += 1
            faktor_risiko.append("Konsumsi junk food berlebihan")
            rekomendasi_khusus.append("Kurangi makanan cepat saji maksimal 1x per minggu")
        
        if['minum_manis'] > 3:
            skor_risiko += 1
            faktor_risiko.append("Konsumsi gula berlebihan")
            rekomendasi_khusus.append("Batasi minuman manis maksimal 2x per minggu")
        
        if['olahraga'] < 3:
            skor_risiko += 1
            faktor_risiko.append("Kurang aktivitas fisik")
            rekomendasi_khusus.append("Lakukan olahraga minimal 150 menit per minggu")
        
        if['waktu_duduk'] > 8:
            skor_risiko += 1
            faktor_risiko.append("Gaya hidup sedentary")
            rekomendasi_khusus.append("Selingi duduk dengan berdiri setiap 30 menit")
        
        if['merokok']:
            skor_risiko += 3
            faktor_risiko.append("Perokok aktif")
            rekomendasi_khusus.append("Pertimbangkan program berhenti merokok")
        
        if['tidur'] < 7:
            skor_risiko += 1
            faktor_risiko.append("Kurang tidur")
            rekomendasi_khusus.append("Usahakan tidur 7-9 jam per malam")
        
        if['stres'] > 7:
            skor_risiko += 2
            faktor_risiko.append("Stres tinggi")
            rekomendasi_khusus.append("Lakukan teknik relaksasi seperti meditasi atau yoga")
        
        # Analisis gejala
        gejala_berat = ['Sesak napas', 'Nyeri dada', 'Gangguan penglihatan']
        for g in gejala:
            if g in gejala_berat:
                skor_risiko += 3
                faktor_risiko.append(f"Gejala {g}")
        
        # Tentukan tingkat risiko
        if skor_risiko <= 3:
            tingkat_risiko = "Rendah"
            tindakan = "Pertahankan gaya hidup sehat"
        elif 4 <= skor_risiko <= 7:
            tingkat_risiko = "Sedang"
            tindakan = "Perbaiki pola hidup, konsultasi jika perlu"
        else:
            tingkat_risiko = "Tinggi"
            tindakan = "Segera konsultasi dengan dokter"
        
        return {
            'skor_risiko': skor_risiko,
            'tingkat_risiko': tingkat_risiko,
            'faktor_risiko': faktor_risiko,
            'rekomendasi_khusus': rekomendasi_khusus,
            'tindakan': tindakan
        }
    
    def generate_laporan(self, bmi_info: Tuple, kalori: float, gaya_hidup: Dict, 
                        gejala: List[str], analisis: Dict):
        """Generate laporan kesehatan lengkap"""
        self.bersihkan_layar()
        self.tampilkan_header("LAPORAN KESEHATAN PRIBADI")
        
        bmi, kategori, risiko_bmi, rekom_bmi = bmi_info

        print(f"\nNama: {self.data_pengguna['nama']}")
        print(f"Tanggal Pemeriksaan: {self.data_pengguna['tanggal']}")
        print(f"Usia: {self.data_pengguna['usia']} tahun")
        print(f"Jenis Kelamin: {self.data_pengguna['jenis_kelamin']}")
        print(f"Berat Badan: {self.data_pengguna['berat']} kg")
        print(f"Tinggi Badan: {self.data_pengguna['tinggi']} cm")
        print(f"Kontak Darurat: {self.data_pengguna['kontak_darurat']}")
        
        print("\n" + "=" * 50)
        print("HASIL ANALISIS KESEHATAN".center(50))
        print("=" * 50)
        
        # Bagian BMI
        print(f"\n1. INDEKS MASSA TUBUH (BMI):")
        print(f"   BMI: {bmi:.1f}")
        print(f"   Kategori: {kategori}")
        print(f"   Risiko: {risiko_bmi}")
        print(f"   Rekomendasi: {rekom_bmi}")
        
        # Bagian Kalori
        print(f"\n2. KEBUTUHAN KALORI HARIAN:")
        print(f"   Estimasi kebutuhan kalori: {kalori:.0f} kalori/hari")
        
        # Bagian Gaya Hidup
        print(f"\n3. ANALISIS GAYA HIDUP:")
        print(f"   Konsumsi sayur/buah: {'✓' if gaya_hidup['sayur_buah'] >= 3 else '✗'}")
        print(f"   Frekuensi olahraga: {gaya_hidup['olahraga']}x/minggu")
        print(f"   Merokok: {'Ya' if gaya_hidup['merokok'] else 'Tidak'}")
        print(f"   Jam tidur: {gaya_hidup['tidur']} jam/malam")
        print(f"   Tingkat stres: {gaya_hidup['stres']}/10")
        
        # Bagian Gejala
        if gejala:
            print(f"\n4. GEJALA YANG DILAPORKAN:")
            for g in gejala:
                print(f"   - {g}")
        
        # Bagian Analisis Risiko
        print(f"\n5. ANALISIS RISIKO KESEHATAN:")
        print(f"   Skor Risiko: {analisis['skor_risiko']}")
        print(f"   Tingkat Risiko: {analisis['tingkat_risiko']}")
        
        if analisis['faktor_risiko']:
            print(f"   Faktor Risiko:")
            for fr in analisis['faktor_risiko']:
                print(f"   - {fr}")
        
        # Bagian Rekomendasi
        print(f"\n6. REKOMENDASI UMUM:")
        print(f"   {rekom_bmi}")
        
        if analisis['rekomendasi_khusus']:
            print(f"\n7. REKOMENDASI KHUSUS:")
            for i, rek in enumerate(analisis['rekomendasi_khusus'], 1):
                print(f"   {i}. {rek}")
        
        print(f"\n8. TINDAKAN YANG DISARANKAN:")
        print(f"   {analisis['tindakan']}")
        
        print("\n" + "=" * 50)
        print("CATATAN PENTING:".center(50))
        print("=" * 50)
        print("""
1. Hasil ini adalah estimasi dan tidak menggantikan konsultasi dokter
2. Jika mengalami gejala berat, segera hubungi dokter
3. Lakukan pemeriksaan kesehatan berkala setiap 6-12 bulan
4. Hasil ini hanya untuk referensi pribadi
        """)
        
        # Simpan ke file
        self.simpan_ke_file(bmi, kategori, kalori, analisis)
    
    def simpan_ke_file(self, bmi, kategori, kalori, analisis):
        """Menyimpan hasil ke file JSON"""
        laporan = {
            'data_pengguna': self.data_pengguna,
            'hasil': {
                'bmi': float(bmi),
                'kategori_bmi': kategori,
                'kebutuhan_kalori': float(kalori),
                'analisis_risiko': analisis
            }
        }
        
        filename = f"laporan_kesehatan_{self.data_pengguna['nama'].replace(' ', '_')}.json"
        
        with open(filename, 'w') as f:
            json.dump(laporan, f, indent=4)
        
        print(f"\n✅ Laporan telah disimpan ke file: {filename}")
    
    def jalankan_tes(self):
        """Menjalankan seluruh proses tes kesehatan"""
        self.bersihkan_layar()
        self.tampilkan_header("TES KESEHATAN LENGKAP")
        
        print("Selamat datang di Program Tes Kesehatan Lengkap!")
        print("Program ini akan membantu Anda menilai kondisi kesehatan.\n")
        
        input("Tekan Enter untuk melanjutkan...")
        
        # Langkah 1: Kumpulkan data dasar
        self.kumpulkan_data_dasar()
        
        # Langkah 2: Hitung BMI
        bmi_info = self.hitung_bmi()
        
        # Langkah 3: Hitung kebutuhan kalori
        kebutuhan_kalori = self.hitung_kebutuhan_kalori()
        
        # Langkah 4: Kuesioner gaya hidup
        gaya_hidup = self.kuesioner_gaya_hidup()
        
        # Langkah 5: Cek gejala
        gejala = self.cek_gejala()
        
        # Langkah 6: Analisis risiko
        analisis = self.analisis_risiko(gaya_hidup, gejala)
        
        # Langkah 7: Tampilkan laporan
        self.generate_laporan(bmi_info, kebutuhan_kalori, gaya_hidup, gejala, analisis)
        
        print("\n" + "=" * 50)
        print("TERIMA KASIH TELAH MENGGUNAKAN LAYANAN INI".center(50))
        print("=" * 50)


def main():
    """Fungsi utama"""
    program = TesKesehatan()
    
    try:
        program.jalankan_tes()
        
        while True:
            ulangi = input("\nApakah Anda ingin melakukan tes lagi? (y/n): ").lower()
            if ulangi == 'y':
                program = TesKesehatan()  # Reset objek
                program.jalankan_tes()
            elif ulangi == 'n':
                print("\nTerima kasih! Jaga selalu kesehatan Anda.")
                break
            else:
                print("Pilihan tidak valid!")
                
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna.")
    except Exception as e:
        print(f"\nTerjadi kesalahan: {str(e)}")
        print("Silakan jalankan program kembali.")


if __name__ == "__main__":
    main()