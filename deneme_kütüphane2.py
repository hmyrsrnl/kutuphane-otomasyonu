class Node: 
    def __init__(self, anahtar, değer, ödünç=False):
    #bir düğümüm baştaki özelliklerini tanimlamak için kullanilir
    #oop yapisindaki constructor mantıği 
        self.anahtar = anahtar 
        self.değer = değer
        self.ödünç = ödünç
        self.next = None
  
class HashTable: 
    def __init__(self, kapasite):
    #hash table için baştaki özelliklerini tanimlar
        self.kapasite = kapasite 
        self.size = 0
        self.table = [None] * kapasite #çakişma durumu için kapasite kadar liste oluşturuyoruz
        #pythonda liste oluşturmak için [] kullanilir
  
    def _hash(self, anahtar): 
    #hash fonksiyonu için indexin nasil belirlenecegini tanimlar
        return hash(anahtar) % self.kapasite
  
    def insert(self, anahtar, değer, ödünç=False):
    #hash table içine key-value değeri eklemek için
        index = self._hash(anahtar) 
        #hash fonksiyonuna göre indexler belirleniyor
        if self.table[index] is None: #eğer o değer boşsa
            self.table[index] = Node(anahtar, değer, ödünç) #yeni bir düğüm oluşturur
            self.size += 1
        else: 
            current = self.table[index] #dizideki ilk düğümü bul
            #current ifadesi linked list içindeki node'lari dolaşirkenşuanda bulunan dügümü ifade eder
            while current: 
                if current.anahtar == anahtar: #key mevcutsa
                    current.değer = değer #güncelleme yap
                    current.ödünç = ödünç #güncelleme yap
                    return
                current = current.next #sonraki düğüme geç
            new_node = Node(anahtar, değer) #key yoksa yeni düğüm oluştur
            new_node.next = self.table[index] #yeni düğümü mevcut listeye bağla
            self.table[index] = new_node #yeni düğümü başa yerleştir
            self.size += 1
  
    def search(self, anahtar): 
        index = self._hash(anahtar) 
        current = self.table[index]
        while current: #bağli listedeki düğümleri tara
            if current.anahtar == anahtar: 
                return current
            current = current.next #sonraki düğüme geç
        raise KeyError(anahtar) #özel bir hata oluşturmak için 
  
    def remove(self, anahtar): 
        index = self._hash(anahtar) 
        #bağlantılı listedeki önceki düğümü tutmak için previous, şu anki düğümü tutmak için current
        previous = None #current düğümdem bir önceki düğüm için
        current = self.table[index] 
        while current: 
            if current.anahtar == anahtar: #anahtar şuanki anahtara eşitse
                if previous: 
                    previous.next = current.next
                    #şuanki düğümü silmek için yukardaki atama yapılır
                else: 
                    self.table[index] = current.next
                    #silinen node listenin ortasinda veya sonundaysa eşitlemesiyle silinen düğüm atlanir
                self.size -= 1
                #düğüm silininse tablodaki öge sayisi azalir
                return
            previous = current #düğüm silindikten sonra previous currenti tutar
            current = current.next #currente bir sonraki düğümü atar, bir sonraki düğüme geçer
        raise KeyError(anahtar) 
  
    def __len__(self): #boyutu veya uzunlugu döndüren fonksiyon
        return self.size #size değerine döndürür
  
    def __contains__(self, anahtar): #'in' ile bir öğe kontrolü yapılırken çalışır
        try: 
            self.search(anahtar) #search fonksiyonunu çağirir
            return True
        except KeyError: 
            return False

    def kullanici_ekleme(self,kullanici_tc,kullanici_şifre):
        if kullanici_tc in self: #self hash tablosunu temsil ediyor
        #in operatörü contains fonksiyonunu çağirir, kullanici tcnin self nesnesinin içinde mi diye bakilir
            print("Bu kullanici zaten mevcut")
        else: #kullani kayitli değilse
            self.insert(kullanici_tc, kullanici_şifre)
            #insert fonksiyonu çağirilir ve ekleme yapılır
            print(f"{kullanici_tc} TC numarali kişi kaydedildi!")
            
    def kullanici_girişi(self,kullanici_tc, kullanici_şifre):
        try:
            kayitli_kullanici = self.search(kullanici_tc) #tcye göre arama yapilir ve değeri kaydedilir
            if kayitli_kullanici.değer == kullanici_şifre:
                print(f"{kullanici_tc} numarali kullanici başariyla giriş yapti.")
                return True
            else:
                print("Hatali şifre girdiniz.")
                return False
        except KeyError:
            print("Kullanici bulunamadi!")
            return False
        
    def kitap_ekleme(self, kitap_ad, kitap_yazar):
        if kitap_ad in self:
            print("Bu kitap zaten mevcut.")
        else:
            self.insert(kitap_ad, kitap_yazar, ödünç=False)
            print(f" {kitap_ad} kitap kütüphaneye eklendi.")

    def kitap_arama(self, kitap_ad):
        try:
            kitap = self.search(kitap_ad)
            print(f"Kitap bulundu:\nKitap adi:{kitap.anahtar}\nKitap yazari: {kitap.değer}")
        except KeyError:
            print("Kitap bulunamadi.")

    def kitap_odunc_al(self, kullanici_tc, kitap_ad):
        if kullanici_tc not in self:
            print("Bu kullanici sistemde kayitli değil.")
            return
        try:
            kitap = self.search(kitap_ad)
            if kitap.ödünç:
                print("Bu kitap zaten ödünç alinmiş.")
            else:
                kitap.ödünç = True
                print(f"{kullanici_tc} numarali kullanici, {kitap.anahtar} adli kitabi ödünç aldi.")
        except KeyError:
            print("Kitap bulunamadi.")

    def kitap_iade_et(self, kullanici_tc, kitap_ad):
        if kullanici_tc not in self:
            print("Bu kullanici sistemde kayitli değil.")
            return
        try:
            kitap = self.search(kitap_ad)
            if not kitap.ödünç:
                print(f"Bu kitap ödünç alinmamiş.")
            else:
                kitap.ödünç = False 
                print(f"{kullanici_tc} numarali kullanici, {kitap.anahtar} adli kitabi iade etti.")
        except KeyError:
            print("Kitap bulunamadi.")

def main():
    ht = HashTable(10)
    giriş_yapan_kullanici = None

    while True:
        print("\n1. Kayit ol")
        print("2. Giriş yap")
        print("3. Kitap ekle")
        print("4. Kitap ara")
        print("5. Kitap ödünç al")
        print("6. Kitap iade et")
        print("7. Çikiş yap")

        seçim = input("Seçiminizi yapin (1/2/3/4/5/6/7):")

        if seçim == "1":
            kullanici_tc = input("TC numaranizi girin:")
            şifre = input("Şifrenizi girin:")
            ht.kullanici_ekleme(kullanici_tc,şifre)
                
        elif seçim == "2":
            kullanici_tc = input("TC numaranizi girin:")
            şifre = input("Şifrenizi girin:")
            if ht.kullanici_girişi(kullanici_tc,şifre):
                giriş_yapan_kullanici = kullanici_tc
            else:
                giriş_yapan_kullanici = None
    
        elif seçim == "3":
            kitap_ad = input("Kitabin adini girin:")
            kitap_yazar = input("Kitap yazarini girin: ")
            ht.kitap_ekleme(kitap_ad, kitap_yazar)
            
        elif seçim == "4":
            kitap_ad = input("Aramak istediğiniz kitabin adini girin:")
            ht.kitap_arama(kitap_ad)
            
        elif seçim == "5":
            kitap_ad = input("Ödünç almak istediğiniz kitabin adini girin:")
            kullanici_tc = input("TC numaranizi girin: ")
            ht.kitap_odunc_al(kullanici_tc, kitap_ad)
        
        elif seçim == "6":
            kitap_ad = input("İade etmek istediğiniz kitabin adini girin:")
            kullanici_tc = input("TC numaranizi girin: ")
            ht.kitap_iade_et(kullanici_tc, kitap_ad)
        
        elif seçim == "7":
            print("Çikiş yapiliyor...")
            break

        else:
            print("Geçersiz seçim yapidi.")

main()
