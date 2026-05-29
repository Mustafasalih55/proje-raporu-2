BOSLUK_KARAKTERI = "#"

# Türkiye İl Plaka Kodları Sözlüğü
ILLER = {
    "01": "Adana", "02": "Adıyaman", "03": "Afyonkarahisar", "04": "Ağrı",
    "05": "Amasya", "06": "Ankara", "07": "Antalya", "08": "Artvin",
    "09": "Aydın", "10": "Balıkesir", "11": "Bilecik", "12": "Bingöl",
    "13": "Bitlis", "14": "Bolu", "15": "Burdur", "16": "Bursa",
    "17": "Çanakkale", "18": "Çankırı", "19": "Çorum", "20": "Denizli",
    "21": "Diyarbakır", "22": "Edirne", "23": "Elazığ", "24": "Erzincan",
    "25": "Erzurum", "26": "Eskişehir", "27": "Gaziantep", "28": "Giresun",
    "29": "Gümüşhane", "30": "Hakkari", "31": "Hatay", "32": "Isparta",
    "33": "Mersin", "34": "İstanbul", "35": "İzmir", "36": "Kars",
    "37": "Kastamonu", "38": "Kayseri", "39": "Kırklareli", "40": "Kırşehir",
    "41": "Kocaeli", "42": "Konya", "43": "Kütahya", "44": "Malatya",
    "45": "Manisa", "46": "Kahramanmaraş", "47": "Mardin", "48": "Muğla",
    "49": "Muş", "50": "Nevşehir", "51": "Niğde", "52": "Ordu",
    "53": "Rize", "54": "Sakarya", "55": "Samsun", "56": "Siirt",
    "57": "Sinop", "58": "Sivas", "59": "Tekirdağ", "60": "Tokat",
    "61": "Trabzon", "62": "Tunceli", "63": "Şanlıurfa", "64": "Uşak",
    "65": "Van", "66": "Yozgat", "67": "Zonguldak", "68": "Aksaray",
    "69": "Bayburt", "70": "Karaman", "71": "Kırıkkale", "72": "Batman",
    "73": "Şırnak", "74": "Bartın", "75": "Ardahan", "76": "Iğdır",
    "77": "Yalova", "78": "Karabük", "79": "Kilis", "80": "Osmaniye",
    "81": "Düzce"
}

def turkce_buyuk_harf(metin):
    """Türkçe karakterleri düzgün şekilde büyük harfe çevirir."""
    donusum = {"i": "İ", "ı": "I", "ş": "Ş", "ğ": "Ğ", "ü": "Ü", "ö": "Ö", "ç": "Ç"}
    sonuc = ""
    for karakter in metin:
        sonuc += donusum.get(karakter, karakter.upper())
    return sonuc

class PlakaKontrolMekanizmasi:
    def __init__(self, plaka_metni, gosterim_acik=True):
        self.ilk_girdi = plaka_metni
        self.serit_dizisi = list(plaka_metni) + [BOSLUK_KARAKTERI]
        self.okuma_kafasi = 0
        self.mevcut_asama = "adim_0"
        self.islem_sayaci = 0
        self.detaylari_yazdir = gosterim_acik

        self.onay_durumu = "TAMAMLANDI"
        self.hata_durumu = "REDDEDILDI"

        self.gecis_kurallari = {
            ("adim_0", "SAYI"): ("adim_1", "ILERI"),
            ("adim_1", "SAYI"): ("adim_2", "ILERI"),
            ("adim_2", "B_HARF"): ("adim_3", "ILERI"),
            ("adim_3", "B_HARF"): ("adim_4", "ILERI"),
            ("adim_4", "SAYI"): ("adim_5", "ILERI"),
            ("adim_5", "SAYI"): ("adim_6", "ILERI"),
            ("adim_6", "SAYI"): ("adim_7", "ILERI"),
            ("adim_7", "BOS"): ("TAMAMLANDI", "BEKLE"),
        }

        self.beklenti_listesi = {
            "adim_0": "1. sira: Rakam olmali",
            "adim_1": "2. sira: Rakam olmali",
            "adim_2": "3. sira: Buyuk harf olmali",
            "adim_3": "4. sira: Buyuk harf olmali",
            "adim_4": "5. sira: Rakam olmali",
            "adim_5": "6. sira: Rakam olmali",
            "adim_6": "7. sira: Rakam olmali",
            "adim_7": "Metin sonlanmis olmali",
        }

    def karakter_tipini_belirle(self, karakter):
        if karakter == BOSLUK_KARAKTERI:
            return "BOS"
        elif karakter.isdigit():
            return "SAYI"
        elif karakter.isalpha() and karakter.isupper() and len(karakter) == 1:
            return "B_HARF"
        elif karakter.isalpha() and karakter.islower() and len(karakter) == 1:
            return "K_HARF"
        else:
            return "GECERSIZ"

    def siradaki_karakteri_oku(self):
        if self.okuma_kafasi >= len(self.serit_dizisi):
            self.serit_dizisi.append(BOSLUK_KARAKTERI)
        return self.serit_dizisi[self.okuma_kafasi]

    def kafayi_hareket_ettir(self, yon_komutu):
        if yon_komutu == "ILERI":
            self.okuma_kafasi += 1
        elif yon_komutu == "GERI":
            self.okuma_kafasi -= 1
        elif yon_komutu == "BEKLE":
            pass

        if self.okuma_kafasi < 0:
            self.serit_dizisi.insert(0, BOSLUK_KARAKTERI)
            self.okuma_kafasi = 0

        if self.okuma_kafasi >= len(self.serit_dizisi):
            self.serit_dizisi.append(BOSLUK_KARAKTERI)

    def serit_gorunumu_olustur(self):
        hucreler = []
        indeks = 0
        while indeks < len(self.serit_dizisi):
            sembol = self.serit_dizisi[indeks]
            if indeks == self.okuma_kafasi:
                hucreler.append(f"<{sembol}>")
            else:
                hucreler.append(f" {sembol} ")
            indeks += 1
        return "".join(hucreler)

    def islem_detayini_yazdir(self, anlik_durum, okunan, k_tipi, yon, sonraki_durum):
        if not self.detaylari_yazdir:
            return
        beklenen_kural = self.beklenti_listesi.get(anlik_durum, "---")
        print(
            f"[{self.islem_sayaci:03d}] Aşama: {anlik_durum:<12} || Görülen: {okunan:<3} || "
            f"Kategori: {k_tipi:<8} || Kural: {beklenen_kural:<35} || Yön: {yon:<5} || "
            f"Hedef: {sonraki_durum:<12} || Şerit: {self.serit_gorunumu_olustur()}"
        )

    def sistemi_baslat(self):
        if self.detaylari_yazdir:
            print("\n*** Turing Makinesi: Plaka Denetim Sistemi ***")
            print("=" * 160)

        while True:
            if self.mevcut_asama == self.onay_durumu or self.mevcut_asama == self.hata_durumu:
                break

            anlik_durum = self.mevcut_asama
            okunan = self.siradaki_karakteri_oku()
            k_tipi = self.karakter_tipini_belirle(okunan)

            kombinasyon = (anlik_durum, k_tipi)
            if kombinasyon in self.gecis_kurallari:
                sonraki_durum, yon = self.gecis_kurallari[kombinasyon]
            else:
                sonraki_durum, yon = self.hata_durumu, "BEKLE"

            self.islem_detayini_yazdir(anlik_durum, okunan, k_tipi, yon, sonraki_durum)
            self.mevcut_asama = sonraki_durum
            self.kafayi_hareket_ettir(yon)
            self.islem_sayaci += 1

        if self.mevcut_asama == self.onay_durumu:
            if self.detaylari_yazdir:
                print("=" * 160)
                print("Çıktı: KABUL")
                il_kodu = self.ilk_girdi[:2]
                sehir_adi = turkce_buyuk_harf(ILLER.get(il_kodu, "Tanımsız İl Kodu"))
                print(f"{il_kodu}={sehir_adi}")
            return True

        if self.detaylari_yazdir:
            print("=" * 160)
            print("Çıktı: RED")
        return False


def tekli_sorgulama_yap():
    metin = input("Kontrol edilecek plakayı yazın: ").strip()

    mekanizma = PlakaKontrolMekanizmasi(metin, gosterim_acik=True)
    degerlendirme = mekanizma.sistemi_baslat()

    print("\n--- RAPOR ---")
    print(f"Girdi: {metin}")

    if degerlendirme:
        print("Çıktı: KABUL")
        il_kodu = metin[:2]
        sehir_adi = turkce_buyuk_harf(ILLER.get(il_kodu, "Tanımsız İl Kodu"))
        print(f"{il_kodu}={sehir_adi}")
    else:
        print("Çıktı: RED")


def toplu_denemeleri_baslat():
    dogru_plakalar = [
        "55KH652",
        "45KH897",
        "35IZ035",
        "06AA789",
        "01AD001",
    ]

    hatali_plakalar = [
        "1FB190",
        "100FB19",
        "35I0351",
        "35iz035",
    ]

    print("\n--- OTOMATİK TEST MODU ---")
    print("*" * 60)

    print("\n[+] Kurallara Uyan Plakalar")
    print("-" * 60)
    
    for plaka in dogru_plakalar:
        mekanizma = PlakaKontrolMekanizmasi(plaka, gosterim_acik=False)
        sonuc = mekanizma.sistemi_baslat()
        
        if sonuc:
            il_kodu = plaka[:2]
            sehir = turkce_buyuk_harf(ILLER.get(il_kodu, "Tanımsız İl Kodu"))
            print(f"Girdi: {plaka:<10} -> Çıktı: KABUL | {il_kodu}={sehir}")
        else:
            print(f"Girdi: {plaka:<10} -> Çıktı: RED")

    print("\n[-] Kurallara Uymayan Plakalar")
    print("-" * 60)

    for plaka in hatali_plakalar:
        mekanizma = PlakaKontrolMekanizmasi(plaka, gosterim_acik=False)
        sonuc = mekanizma.sistemi_baslat()
        yazdirilacak = "KABUL" if sonuc else "RED"
        print(f"Girdi: {plaka:<10} -> Çıktı: {yazdirilacak}")


def ana_menu():
    print("A - Manuel Plaka Girişi Yap")
    print("B - Otomatik Testleri Çalıştır")

    tercih = input("Lütfen bir harf seçin (A/B): ").strip().upper()

    if tercih == "A":
        tekli_sorgulama_yap()
    elif tercih == "B":
        toplu_denemeleri_baslat()
    else:
        print("Hatalı bir giriş yaptınız.")


if __name__ == "__main__":
    ana_menu()