# app.py - TÜM UYGULAMA TEK DOSYADA
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

# Sidebar menü
st.sidebar.title("📚 Öğrenme Yolculuğu")
menu = st.sidebar.selectbox(
    "Modül Seç:",
    ["🏠 Ana Sayfa", "💻 Kod Sandbox", "📖 Dersler", "🎮 Bulmacalar", "📊 İlerlemem"]
)

# KOD SANDBOX FONKSİYONU
def kod_sandbox():
    st.header("💻 Python Kod Sandbox")
    st.write("Kodunu yaz ve çalıştır! Hataları gör, öğren!")
    
    # Varsayılan kod
    default_code = '''# Örnek kod - değiştirebilirsin
isim = "Ahmet"
yas = 30

print(f"Merhaba {isim}!")
print(f"Yaşın: {yas}")

# Toplama işlemi
sayi1 = 10
sayi2 = 20
toplam = sayi1 + sayi2
print(f"Toplam: {toplam}")

# Liste örneği
meyveler = ["elma", "armut", "çilek"]
for meyve in meyveler:
    print(f"Meyve: {meyve}")
'''
    
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
                st.session_state.example_code = '''# Değişkenler ve veri tipleri
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
                st.session_state.example_code = '''# Liste işlemleri
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
                st.session_state.example_code = '''# Fonksiyon tanımlama
def selam_ver(isim):
    return f"Merhaba {isim}!"

def topla(a, b):
    return a + b

# Fonksiyonları kullan
print(selam_ver("Mehmet"))
print("Toplam:", topla(5, 3))'''
                st.rerun()
            
            if st.button("Koşul Örneği"):
                st.session_state.example_code = '''# If-else koşulları
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
    
    # Örnek kodu text area'ya yükle
    if 'example_code' in st.session_state:
        return st.session_state.example_code
    
    return user_code

# DERSLER FONKSİYONU
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
            "baslik": "2. Print ve Input", 
            "aciklama": "Ekrana yazdırma ve kullanıcıdan veri alma",
            "icerik": """
            **Print fonksiyonu** ekrana yazdırır:
            ```python
            print("Merhaba Dünya!")
            print("İsim:", isim)
            print(f"Yaş: {yas}")  # f-string (modern)
            ```

            **Input fonksiyonu** kullanıcıdan veri alır:
            ```python
            isim = input("İsminiz: ")
            yas = int(input("Yaşınız: "))  # Sayıya çevir
            ```
            """,
            "ornek": "isim = input('İsminizi girin: ')\nprint(f'Hoş geldin {isim}!')"
        }
    ]
    
    for ders in ders_listesi:
        with st.expander(f"📚 {ders['baslik']}", expanded=True):
            st.write(ders['aciklama'])
            st.markdown(ders['icerik'])
            
            if st.button(f"Örneği Denemek İçin Tıkla → {ders['baslik']}"):
                st.session_state.deneme_kodu = ders['ornek']
                st.success("Örnek kodu Kod Sandbox'ta deneyebilirsin!")

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
            
            cozum_goster = st.checkbox(f"Çözümü Göster - Bulmaca {i+1}")
            if cozum_goster:
                st.code(bulmaca['cozum'])
                if st.button(f"Bu Kodu Denemek İçin Tıkla - Bulmaca {i+1}"):
                    st.session_state.deneme_kodu = bulmaca['cozum']
                    st.success("Kodu Kod Sandbox'ta deneyebilirsin!")

# İLERLEME FONKSİYONU  
def ilerleme():
    st.header("📊 Öğrenme İlerlemen")
    st.write("Ne kadar yol kat ettiğini gör!")
    
    # Basit ilerleme takibi
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💻 Kod Denemeleri", "5+")
    with col2:
        st.metric("📚 Tamamlanan Dersler", "2")
    with col3: 
        st.metric("🎮 Çözülen Bulmacalar", "3")
    
    st.info("""
    **🎯 Sonraki Adımlar:**
    1. Kod Sandbox'ta daha fazla deneme yap
    2. Tüm dersleri tamamla  
    3. Bulmacaları çöz
    4. Kendi mini projelerini yap
    """)

# ANA SAYFA
if menu == "🏠 Ana Sayfa":
    st.header("Python Öğrenme Yolculuğuna Hoş Geldin!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**💻 Kod Sandbox**\n→ Kodunu dene\n→ Hataları gör\n→ Öğren!")
    with col2:
        st.info("**📖 Interaktif Dersler**\n→ Adım adım Python\n→ Canlı örnekler\n→ Alıştırmalar")
    with col3:
        st.info("**🎮 Kod Bulmacaları**\n→ Eğlenceli challenge'lar\n→ Problem çözme\n→ Becerini test et")
    
    st.success("🚀 **Başlamak için soldaki menüden bir modül seç!**")

elif menu == "💻 Kod Sandbox":
    kod_sandbox()

elif menu == "📖 Dersler":
    dersler()

elif menu == "🎮 Bulmacalar":
    bulmacalar()

elif menu == "📊 İlerlemem":
    ilerleme()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**🐍 Python Journey v1.0**
Her gün 1 saat kodla!
→ Öğren
→ Uygula  
→ Tekrar et
→ Geliş!
""")
