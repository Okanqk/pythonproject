# app.py - DÜZELTİLMİŞ VE GELİŞTİRİLMİŞ
import streamlit as st
import json
import os
from datetime import datetime
import io
import contextlib

# Sayfa ayarı
st.set_page_config(page_title="Python Journey", page_icon="🐍", layout="wide")

# Başlık
st.title("🐍 Python Journey - Python Öğreniyorum!")
st.write("Python'ı yaparak öğren - Kendi öğrenme aracını kendin yap!")

# Session state initialization
if 'deneme_kodu' not in st.session_state:
    st.session_state.deneme_kodu = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Ana Sayfa"

# Sidebar menü
st.sidebar.title("📚 Öğrenme Yolculuğu")
menu = st.sidebar.selectbox(
    "Modül Seç:",
    ["🏠 Ana Sayfa", "💻 Kod Sandbox", "📖 Dersler", "🎯 Testler", "🎮 Bulmacalar", "📊 İlerlemem"]
)

# KOD SANDBOX FONKSİYONU - GÜNCELLENMİŞ
def kod_sandbox():
    st.header("💻 Python Kod Sandbox")
    st.write("Kodunu yaz ve çalıştır! Hataları gör, öğren!")
    
    # Eğer derslerden kod geldiyse onu göster, yoksa default
    if st.session_state.deneme_kodu:
        default_code = st.session_state.deneme_kodu
        st.success("🎯 Derslerden kod yüklendi! Hemen dene...")
    else:
        default_code = '''# Örnek kod - değiştirebilirsin
isim = "Ahmet"
yas = 30

print(f"Merhaba {isim}!")
print(f"Yaşın: {yas}")

# Toplama işlemi
sayi1 = 10
sayi2 = 20
toplam = sayi1 + sayi2
print(f"Toplam: {toplam}")'''
    
    # Kod editörü
    user_code = st.text_area("Python Kodunuz:", value=default_code, height=300)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🚀 Kodu Çalıştır", type="primary"):
            try:
                # Çıktıyı yakala
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    exec(user_code)
                
                st.success("✅ Kod başarıyla çalıştı!")
                st.session_state.last_output = output.getvalue()
                
            except Exception as e:
                st.error(f"❌ Hata oluştu: {str(e)}")
                st.session_state.last_output = None
    
    with col2:
        if st.button("🧹 Temizle"):
            st.session_state.last_output = None
            st.session_state.deneme_kodu = ""
            st.rerun()
    
    # Çıktıyı göster
    if 'last_output' in st.session_state and st.session_state.last_output:
        st.subheader("📤 Çıktı:")
        st.code(st.session_state.last_output)
    
    # Örnek kodlar
    with st.expander("📚 Hızlı Örnek Kodlar"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Değişkenler Örneği"):
                st.session_state.deneme_kodu = '''# Değişkenler ve veri tipleri
isim = "Ayşe"
yas = 25
boy = 1.65
ogrenci = True

print(f"İsim: {isim}")
print(f"Yaş: {yas}")
print(f"Boy: {boy}")
print(f"Öğrenci mi: {ogrenci}")'''
                st.rerun()
            
            if st.button("Listeler Örneği"):
                st.session_state.deneme_kodu = '''# Liste işlemleri
sayilar = [1, 2, 3, 4, 5]
print("Liste:", sayilar)

# Eleman ekle
sayilar.append(6)
print("Append sonrası:", sayilar)

# For döngüsü
print("Elemanlar:")
for sayi in sayilar:
    print(f"- {sayi}")'''
                st.rerun()
        
        with col2:
            if st.button("Fonksiyon Örneği"):
                st.session_state.deneme_kodu = '''# Fonksiyon tanımlama
def selam_ver(isim):
    return f"Merhaba {isim}!"

def topla(a, b):
    return a + b

# Fonksiyonları kullan
print(selam_ver("Mehmet"))
print("Toplam:", topla(5, 3))'''
                st.rerun()
            
            if st.button("Koşul Örneği"):
                st.session_state.deneme_kodu = '''# If-else koşulları
not = 85

if not >= 90:
    print("AA - Mükemmel!")
elif not >= 80:
    print("BA - Çok iyi!")
elif not >= 70:
    print("BB - İyi!")
else:
    print("Çalışman lazım!")

print(f"Notun: {not}")'''
                st.rerun()
    
    return user_code

# DERSLER FONKSİYONU - GÜNCELLENMİŞ
def dersler():
    st.header("📖 Python Dersleri")
    st.write("Adım adım Python öğren!")
    
    ders_listesi = [
        {
            "baslik": "1. Değişkenler ve Veri Tipleri",
            "aciklama": "Python'da veri saklamayı öğren",
            "icerik": """
            **Değişkenler** veri saklamak için kullanılır:
            ```python
            isim = "Ahmet"      # String (metin)
            yas = 25            # Integer (tam sayı)  
            boy = 1.75          # Float (ondalıklı)
            ogrenci = True      # Boolean (True/False)
            ```

            **Kurallar:**
            - Değişken isimleri harf veya _ ile başlar
            - Türkçe karakter kullanabilirsin
            - Büyük/küçük harf duyarlı
            """,
            "ornek": "isim = 'Ayşe'\nyas = 20\nprint(f'{isim} {yas} yaşında')"
        },
        {
            "baslik": "2. Print ve Input - f-string MÜTHİŞ!", 
            "aciklama": "Ekrana yazdırma ve kullanıcıdan veri alma",
            "icerik": """
            **Print fonksiyonu** ekrana yazdırır:
            ```python
            print("Merhaba Dünya!")
            print("İsim:", isim)                    # Virgül ile
            print("Yaş: " + str(yas))               # Eski yöntem
            print(f"Hoş geldin {isim}!")            # f-string (EN İYİSİ!)
            ```

            **f-string AVANTAJLARI:**
            - ✅ Okuması kolay
            - ✅ Hızlı
            - ✅ Değişkenleri direkt kullan
            - ✅ İşlem yapabilirsin: {yas + 5}
            
            **Input fonksiyonu** kullanıcıdan veri alır:
            ```python
            isim = input("İsminiz: ")
            yas = int(input("Yaşınız: "))  # Sayıya çevir
            ```
            """,
            "ornek": "isim = input('İsminizi girin: ')\nyas = int(input('Yaşınız: '))\nprint(f'Hoş geldin {isim}! {yas} yaşındasın ve {yas + 10} yılında 10 yaş daha büyük olacaksın!')"
        },
        {
            "baslik": "3. Listeler ve Döngüler",
            "aciklama": "Veri koleksiyonları ve tekrarlı işlemler",
            "icerik": """
            **Listeler** birden fazla veriyi saklar:
            ```python
            meyveler = ["elma", "armut", "çilek"]
            sayilar = [1, 2, 3, 4, 5]
            karisik = ["ali", 25, True, 1.75]
            ```

            **For Döngüsü** ile listede gezin:
            ```python
            for meyve in meyveler:
                print(f"Meyve: {meyve}")
            
            for i in range(5):          # 0'dan 4'e
                print(f"Sayı: {i}")
            
            for i in range(1, 6):       # 1'den 5'e  
                print(f"Sayı: {i}")
            ```
            """,
            "ornek": "meyveler = ['elma', 'armut', 'çilek', 'muz']\nprint('Meyve Listesi:')\nfor meyve in meyveler:\n    print(f'- {meyve}')\n\nprint('\\\\n1-10 arası sayılar:')\nfor i in range(1, 11):\n    print(i)"
        }
    ]
    
    for ders in ders_listesi:
        with st.expander(f"📚 {ders['baslik']}", expanded=False):
            st.write(ders['aciklama'])
            st.markdown(ders['icerik'])
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"💻 Deneme →", key=f"deneme_{ders['baslik']}"):
                    st.session_state.deneme_kodu = ders['ornek']
                    st.session_state.current_page = "💻 Kod Sandbox"
                    st.success("🎯 Kod Sandbox'a yönlendiriliyorsunuz...")
                    st.rerun()

# YENİ EKLENEN TESTLER BÖLÜMÜ
def testler():
    st.header("🎯 Python Testleri")
    st.write("Öğrendiklerini test et, küçük ama önemli detayları pekiştir!")
    
    st.info("**💡 Önemli Bilgi:** Bu testlerde küçük ama kritik detayları ölçüyoruz!")
    
    test_listesi = [
        {
            "soru": "1. Hangisi f-string için DOĞRU değil?",
            "secenekler": [
                "A) print(f\"Merhaba {isim}\")",
                "B) print(f\"Yaş: {yas + 5}\")", 
                "C) print(f\"Sonuç: {10 + 20}\")",
                "D) print(f\"İsim: isim\")"
            ],
            "cevap": "D",
            "aciklama": "f-string'te değişkenleri {} içinde yazmalısın. D seçeneğinde {isim} yerine sadece isim yazılmış!"
        },
        {
            "soru": "2. Hangisi liste oluşturur?",
            "secenekler": [
                "A) liste = (1, 2, 3)",
                "B) liste = [1, 2, 3]",
                "C) liste = {1, 2, 3}",
                "D) liste = '1,2,3'"
            ],
            "cevap": "B", 
            "aciklama": "Listeler köşeli parantez [] ile oluşturulur. A=tuple, C=set, D=string"
        },
        {
            "soru": "3. Input'tan gelen veri hangi tiptedir?",
            "secenekler": [
                "A) Her zaman integer",
                "B) Her zaman string", 
                "C) Kullanıcıya bağlı",
                "D) Her zaman float"
            ],
            "cevap": "B",
            "aciklama": "Input fonksiyonu her zaman string döndürür! Sayıya çevirmek için int() veya float() kullanmalısın."
        },
        {
            "soru": "4. Hangisi değişken ismi olarak GEÇERLİDİR?",
            "secenekler": [
                "A) 1sayi",
                "B) sayi-1", 
                "C) _sayi",
                "D) sayi bir"
            ],
            "cevap": "C",
            "aciklama": "Değişken isimleri sayıyla başlayamaz (A), tire içeremez (B), boşluk içeremez (D). Alt çizgi (_) kullanabilirsin."
        }
    ]
    
    score = 0
    user_answers = {}
    
    for i, test in enumerate(test_listesi):
        st.subheader(f"Test {i+1}")
        st.write(f"**{test['soru']}**")
        
        user_answer = st.radio(
            f"Seçenekler (Test {i+1}):",
            test['secenekler'],
            key=f"test_{i}"
        )
        
        user_answers[i] = user_answer[0]  # A, B, C, D
        
        # Cevap kontrolü butonu
        if st.button(f"Cevabı Kontrol Et → Test {i+1}", key=f"check_{i}"):
            if user_answers[i] == test['cevap']:
                st.success("✅ DOĞRU! Harikasın!")
                score += 1
            else:
                st.error(f"❌ YANLIŞ! Doğru cevap: {test['cevap']}")
            
            st.info(f"**💡 Açıklama:** {test['aciklama']}")
    
    # Sonuçları göster
    if st.button("📊 Test Sonuçlarını Gör"):
        st.subheader("Test Sonuçları")
        st.write(f"**Puanın: {score}/{len(test_listesi)}**")
        
        if score == len(test_listesi):
            st.balloons()
            st.success("🎉 MÜKEMMEL! Tüm soruları doğru bildin!")
        elif score >= len(test_listesi) / 2:
            st.warning("👍 İYİ! Devam et, daha iyi olacaksın!")
        else:
            st.info("💪 BİRAZ DAHA ÇALIŞ! Dersleri tekrar et ve tekrar dene.")

# BULMACALAR FONKSİYONU  
def bulmacalar():
    st.header("🎮 Python Bulmacaları")
    st.write("Becerilerini test et, problem çöz!")
    
    bulmaca_listesi = [
        {
            "soru": "1'den 10'a kadar sayıları yazdıran programı yaz",
            "ipucu": "for döngüsü ve range() fonksiyonunu kullan",
            "cozum": "for i in range(1, 11):\n    print(i)"
        },
        {
            "soru": "İki sayıyı toplayan fonksiyon yaz", 
            "ipucu": "def kullanarak fonksiyon tanımla",
            "cozum": "def topla(a, b):\n    return a + b"
        },
        {
            "soru": "Listedeki en büyük sayıyı bulan kodu yaz",
            "ipucu": "max() fonksiyonunu veya for döngüsünü kullan",
            "cozum": "sayilar = [3, 7, 2, 9, 1]\nprint(max(sayilar))"
        }
    ]
    
    for i, bulmaca in enumerate(bulmaca_listesi):
        with st.expander(f"🧩 Bulmaca {i+1}: {bulmaca['soru']}"):
            st.write("**İpucu:**", bulmaca['ipucu'])
            
            cozum_goster = st.checkbox(f"Çözümü Göster - Bulmaca {i+1}", key=f"cozum_{i}")
            if cozum_goster:
                st.code(bulmaca['cozum'])
                if st.button(f"Bu Kodu Denemek İçin Tıkla - Bulmaca {i+1}", key=f"deneme_bulmaca_{i}"):
                    st.session_state.deneme_kodu = bulmaca['cozum']
                    st.session_state.current_page = "💻 Kod Sandbox"
                    st.success("Kod Sandbox'a yönlendiriliyorsunuz!")
                    st.rerun()

# İLERLEME FONKSİYONU  
def ilerleme():
    st.header("📊 Öğrenme İlerlemen")
    st.write("Ne kadar yol kat ettiğini gör!")
    
    # Basit ilerleme takibi
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💻 Kod Denemeleri", "5+")
    with col2:
        st.metric("📚 Tamamlanan Dersler", "3")
    with col3: 
        st.metric("🎯 Test Puanı", "0/4 (Test et!)")
    
    st.info("""
    **🎯 Sonraki Adımlar:**
    1. Kod Sandbox'ta daha fazla deneme yap
    2. Tüm dersleri tamamla  
    3. Testleri çöz ve puanını gör
    4. Bulmacaları çöz
    5. Kendi mini projelerini yap
    """)

# ANA SAYFA
if menu == "🏠 Ana Sayfa":
    st.header("Python Öğrenme Yolculuğuna Hoş Geldin Okan!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**💻 Kod Sandbox**\n→ Kodunu dene\n→ Hataları gör\n→ Öğren!")
    with col2:
        st.info("**📖 Interaktif Dersler**\n→ Adım adım Python\n→ Canlı örnekler\n→ Sandbox'a tek tık!")
    with col3:
        st.info("**🎯 Mini Testler**\n→ Kritik detayları ölç\n→ Bilgini pekiştir\n→ Puanını gör!")
    
    st.success("🚀 **Başlamak için soldaki menüden bir modül seç!**")

elif menu == "💻 Kod Sandbox":
    kod_sandbox()

elif menu == "📖 Dersler":
    dersler()

elif menu == "🎯 Testler":
    testler()

elif menu == "🎮 Bulmacalar":
    bulmacalar()

elif menu == "📊 İlerlemem":
    ilerleme()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**🐍 Python Journey v1.1**
Geliştiren: Okan
Her gün 1 saat kodla!
→ Öğren
→ Uygula  
→ Test et
→ Geliş!
""")
