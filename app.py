import streamlit as st
import json
import os
from datetime import datetime
import io
import contextlib
import zipfile
import shutil

# Sayfa yapılandırması
st.set_page_config(
    page_title="Python Journey",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .code-success {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .code-error {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Session state başlangıç değerleri
if 'deneme_kodu' not in st.session_state:
    st.session_state.deneme_kodu = ""
if 'last_output' not in st.session_state:
    st.session_state.last_output = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Ana Sayfa"
if 'ilerleme' not in st.session_state:
    st.session_state.ilerleme = {
        "tamamlanan_dersler": [],
        "cozulen_testler": [],
        "cozulen_bulmacalar": [],
        "toplam_kod_denemesi": 0,
        "basari_puani": 0
    }
if 'test_sonuclari' not in st.session_state:
    st.session_state.test_sonuclari = {}
if 'aktif_test' not in st.session_state:
    st.session_state.aktif_test = None
if 'test_cevaplari' not in st.session_state:
    st.session_state.test_cevaplari = {}

# JSON dosya yönetimi fonksiyonları
def json_dosya_yukle(dosya_yolu):
    """JSON dosyasını yükler"""
    try:
        if os.path.exists(dosya_yolu):
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return None
    except Exception as e:
        st.error(f"❌ Dosya yükleme hatası: {str(e)}")
        return None

def json_dosya_kaydet(dosya_yolu, veri):
    """JSON dosyasını kaydeder"""
    try:
        os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)
        with open(dosya_yolu, 'w', encoding='utf-8') as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"❌ Dosya kaydetme hatası: {str(e)}")
        return False

def tum_dersleri_yukle():
    """data/dersler klasöründeki tüm JSON dosyalarını yükler"""
    dersler = []
    dersler_klasoru = "data/dersler"
    
    if os.path.exists(dersler_klasoru):
        for dosya in sorted(os.listdir(dersler_klasoru)):
            if dosya.endswith('.json'):
                ders_verisi = json_dosya_yukle(os.path.join(dersler_klasoru, dosya))
                if ders_verisi:
                    dersler.append(ders_verisi)
    
    return list(reversed(dersler))

def tum_testleri_yukle():
    """data/testler klasöründeki tüm JSON dosyalarını yükler"""
    testler = []
    testler_klasoru = "data/testler"
    
    if os.path.exists(testler_klasoru):
        for dosya in sorted(os.listdir(testler_klasoru)):
            if dosya.endswith('.json'):
                test_verisi = json_dosya_yukle(os.path.join(testler_klasoru, dosya))
                if test_verisi:
                    testler.append(test_verisi)
    
    return list(reversed(testler))

def tum_bulmacalari_yukle():
    """data/bulmacalar klasöründeki tüm JSON dosyalarını yükler"""
    bulmacalar = []
    bulmacalar_klasoru = "data/bulmacalar"
    
    if os.path.exists(bulmacalar_klasoru):
        for dosya in sorted(os.listdir(bulmacalar_klasoru)):
            if dosya.endswith('.json'):
                bulmaca_verisi = json_dosya_yukle(os.path.join(bulmacalar_klasoru, dosya))
                if bulmaca_verisi:
                    bulmacalar.append(bulmaca_verisi)
    
    return list(reversed(bulmacalar))

def ilerleme_kaydet():
    """İlerleme verilerini kaydeder"""
    json_dosya_kaydet("data/ilerleme.json", st.session_state.ilerleme)

def ilerleme_yukle():
    """İlerleme verilerini yükler"""
    ilerleme_verisi = json_dosya_yukle("data/ilerleme.json")
    if ilerleme_verisi:
        st.session_state.ilerleme = ilerleme_verisi

def zip_yedek_olustur():
    """data klasörünün ZIP yedeklemesini oluşturur"""
    try:
        zip_dosya = f"python_journey_yedek_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        with zipfile.ZipFile(zip_dosya, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.exists('data'):
                for klasor, _, dosyalar in os.walk('data'):
                    for dosya in dosyalar:
                        dosya_yolu = os.path.join(klasor, dosya)
                        arcname = os.path.relpath(dosya_yolu, '.')
                        zipf.write(dosya_yolu, arcname)
        
        return zip_dosya
    except Exception as e:
        st.error(f"❌ ZIP yedek oluşturma hatası: {str(e)}")
        return None

def zip_yedek_geri_yukle(zip_dosya):
    """ZIP yedeklemesinden verileri geri yükler"""
    try:
        with zipfile.ZipFile(zip_dosya, 'r') as zipf:
            zipf.extractall('.')
        return True
    except Exception as e:
        st.error(f"❌ ZIP yedek geri yükleme hatası: {str(e)}")
        return False

# Kod Sandbox fonksiyonu
def kod_sandbox():
    st.markdown("<h1 class='main-header'>💻 Python Kod Sandbox</h1>", unsafe_allow_html=True)
    st.write("Kodunu yaz ve çalıştır! Hataları gör, öğren!")
    
    if st.session_state.deneme_kodu:
        default_code = st.session_state.deneme_kodu
        st.success("🎯 Derslerden kod yüklendi! Hemen dene...")
    else:
        default_code = '''# Python Sandbox - Kodunu buraya yaz!

# Örnek: Değişkenler
isim = "Ahmet"
yas = 25
print(f"Merhaba {isim}, yaşın {yas}")

# Örnek: Liste işlemleri
sayilar = [1, 2, 3, 4, 5]
toplam = sum(sayilar)
print(f"Sayılar: {sayilar}")
print(f"Toplam: {toplam}")

# Örnek: Döngü
for i in range(1, 6):
    print(f"Sayı: {i}")
'''
    
    user_code = st.text_area(
        "Python Kodunuz:",
        value=default_code,
        height=400,
        key="sandbox_editor"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🚀 Kodu Çalıştır", type="primary", use_container_width=True):
            try:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    exec(user_code, {'__builtins__': __builtins__})
                
                result = output.getvalue()
                st.session_state.last_output = result if result else "✅ Kod başarıyla çalıştı (çıktı yok)"
                st.session_state.ilerleme['toplam_kod_denemesi'] += 1
                ilerleme_kaydet()
                st.rerun()
                
            except Exception as e:
                st.session_state.last_output = f"HATA: {str(e)}"
                st.rerun()
    
    with col2:
        if st.button("🧹 Temizle", use_container_width=True):
            st.session_state.last_output = ""
            st.session_state.deneme_kodu = ""
            st.rerun()
    
    with col3:
        st.write("💡 Kod denemesi:", st.session_state.ilerleme['toplam_kod_denemesi'])
    
    if st.session_state.last_output:
        st.subheader("📤 Çıktı:")
        if "HATA:" in st.session_state.last_output:
            st.error(st.session_state.last_output)
        else:
            st.success(st.session_state.last_output)
    
    with st.expander("📚 Hızlı Örnek Kodlar"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔤 Değişkenler", use_container_width=True):
                st.session_state.deneme_kodu = '''# Değişkenler ve veri tipleri
isim = "Ayşe"
yas = 28
boy = 1.70
ogrenci = True

print(f"İsim: {isim}")
print(f"Yaş: {yas}")
print(f"Boy: {boy} m")
print(f"Öğrenci mi: {ogrenci}")

# Tip kontrolü
print(f"\\nİsim tipi: {type(isim)}")
print(f"Yaş tipi: {type(yas)}")
'''
                st.rerun()
            
            if st.button("📊 Listeler", use_container_width=True):
                st.session_state.deneme_kodu = '''# Liste işlemleri
meyveler = ["elma", "armut", "muz", "çilek"]
print("Meyveler:", meyveler)

# Eleman ekleme
meyveler.append("kiraz")
print("Append sonrası:", meyveler)

# Döngü ile yazdırma
print("\\nTüm meyveler:")
for meyve in meyveler:
    print(f"  - {meyve}")

# Liste uzunluğu
print(f"\\nToplam meyve: {len(meyveler)}")
'''
                st.rerun()
        
        with col2:
            if st.button("🔄 Döngüler", use_container_width=True):
                st.session_state.deneme_kodu = '''# For döngüsü
print("1'den 5'e kadar:")
for i in range(1, 6):
    print(f"Sayı: {i}")

# While döngüsü
print("\\nWhile döngüsü:")
sayi = 1
while sayi <= 5:
    print(f"Değer: {sayi}")
    sayi += 1

# Liste ile döngü
print("\\nRenkler:")
renkler = ["kırmızı", "mavi", "yeşil"]
for renk in renkler:
    print(f"  → {renk}")
'''
                st.rerun()
            
            if st.button("❓ Koşullar", use_container_width=True):
                st.session_state.deneme_kodu = '''# If-elif-else koşulları
not_degeri = 85

if not_degeri >= 90:
    harf_notu = "AA"
    durum = "Mükemmel!"
elif not_degeri >= 80:
    harf_notu = "BA"
    durum = "Çok iyi!"
elif not_degeri >= 70:
    harf_notu = "BB"
    durum = "İyi!"
elif not_degeri >= 60:
    harf_notu = "CB"
    durum = "Orta"
else:
    harf_notu = "FF"
    durum = "Çalışman lazım!"

print(f"Notun: {not_degeri}")
print(f"Harf notu: {harf_notu}")
print(f"Durum: {durum}")
'''
                st.rerun()
        
        with col3:
            if st.button("🔧 Fonksiyonlar", use_container_width=True):
                st.session_state.deneme_kodu = '''# Fonksiyon tanımlama
def selam_ver(isim):
    return f"Merhaba {isim}!"

def toplam_hesapla(a, b):
    return a + b

def carpim_tablosu(sayi):
    print(f"{sayi} çarpım tablosu:")
    for i in range(1, 11):
        print(f"{sayi} x {i} = {sayi * i}")

# Fonksiyonları kullan
print(selam_ver("Mehmet"))
print(f"Toplam: {toplam_hesapla(15, 7)}")
print()
carpim_tablosu(5)
'''
                st.rerun()
            
            if st.button("📖 Sözlükler", use_container_width=True):
                st.session_state.deneme_kodu = '''# Sözlük (Dictionary) işlemleri
kisi = {
    "isim": "Ali",
    "yas": 30,
    "sehir": "İstanbul",
    "meslek": "Mühendis"
}

print("Kişi Bilgileri:")
print(f"İsim: {kisi['isim']}")
print(f"Yaş: {kisi['yas']}")
print(f"Şehir: {kisi['sehir']}")

# Yeni eleman ekleme
kisi['email'] = "ali@email.com"

# Tüm anahtarlar
print("\\nTüm anahtarlar:", kisi.keys())
print("Tüm değerler:", kisi.values())
'''
                st.rerun()

# Dersler fonksiyonu
def dersler():
    st.markdown("<h1 class='main-header'>📖 Python Dersleri</h1>", unsafe_allow_html=True)
    st.write("Adım adım Python öğren! Her ders video eşliğinde, kod örnekleriyle.")
    
    dersler_listesi = tum_dersleri_yukle()
    
    if not dersler_listesi:
        st.warning("📂 Henüz ders içeriği yüklenmemiş.")
        st.info("""
        **Ders eklemek için:**
        1. `data/dersler/` klasörü oluştur
        2. JSON formatında ders dosyalarını ekle
        3. Örnek format:
```json
{
  "konu_id": 1,
  "konu_baslik": "Stringler",
  "aciklama": "Metin işlemleri",
  "seviye": "başlangıç"
}
```
        """)
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Toplam Ders", len(dersler_listesi))
    with col2:
        tamamlanan = len(st.session_state.ilerleme['tamamlanan_dersler'])
        st.metric("✅ Tamamlanan", tamamlanan)
    with col3:
        if len(dersler_listesi) > 0:
            yuzde = int((tamamlanan / len(dersler_listesi)) * 100)
            st.metric("📊 İlerleme", f"%{yuzde}")

    st.markdown("---")

    for idx, ders in enumerate(dersler_listesi):
        konu_id = ders.get('konu_id', idx)
        konu_baslik = ders.get('konu_baslik', 'İsimsiz Ders')
        aciklama = ders.get('aciklama', '')
        seviye = ders.get('seviye', 'başlangıç')
        
        tamamlandi = konu_id in st.session_state.ilerleme['tamamlanan_dersler']
        icon = "✅" if tamamlandi else "○"
        
        st.markdown(f"## {icon} {konu_baslik}")
        st.caption(f"Seviye: {seviye.title()}")
        
        with st.expander("📖 Dersi Aç", expanded=False):
            st.write(f"**📝 Açıklama:** {aciklama}")
            
            if 'video_link' in ders:
                st.markdown(f"🎥 **Video:** [{ders.get('video_suresi', 'İzle')}]({ders['video_link']})")
            
            ders_icerik = ders.get('ders_icerik', {})
            if ders_icerik:
                if 'detayli_aciklama' in ders_icerik:
                    st.markdown("### 📚 Detaylı Açıklama")
                    st.write(ders_icerik['detayli_aciklama'])
                
                if 'ana_kavramlar' in ders_icerik:
                    st.markdown("### 🔑 Ana Kavramlar")
                    for kavram in ders_icerik['ana_kavramlar']:
                        st.write(f"• {kavram}")
            
            kod_ornekleri = ders.get('kod_ornekleri', [])
            if kod_ornekleri:
                st.markdown("### 💻 Kod Örnekleri")
                for idx, ornek in enumerate(kod_ornekleri):
                    st.write(f"**{ornek.get('baslik', f'Örnek {idx+1}')}**")
                    if 'aciklama' in ornek:
                        st.info(ornek['aciklama'])
                    
                    kod = ornek.get('kod', '')
                    st.code(kod, language='python')
                    
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        if st.button(f"🚀 Çalıştır", key=f"kod_ornek_{konu_id}_{idx}"):
                            try:
                                output = io.StringIO()
                                with contextlib.redirect_stdout(output):
                                    exec(kod, {'__builtins__': __builtins__})
                                
                                result = output.getvalue()
                                if result:
                                    st.success(result)
                                else:
                                    st.success("✅ Kod başarıyla çalıştı (çıktı yok)")
                            except Exception as e:
                                st.error(f"❌ Hata: {str(e)}")
                    
                    with col2:
                        if st.button(f"📋 Sandbox'a Kopyala", key=f"kopyala_{konu_id}_{idx}"):
                            st.session_state.deneme_kodu = kod
                            st.success("✅ Kod Sandbox'a kopyalandı!")
                    
                    with col3:
                        if st.button(f"→ Sandbox'a Git", key=f"sandbox_git_{konu_id}_{idx}"):
                            st.session_state.deneme_kodu = kod
                            st.session_state.current_page = "💻 Kod Sandbox"
                            st.rerun()
            
            st.markdown("---")
            
            if tamamlandi:
                st.success("✅ Bu dersi tamamladın!")
            else:
                if st.button("✓ Dersi Tamamla", key=f"tamam_ders_{konu_id}", type="primary"):
                    if konu_id not in st.session_state.ilerleme['tamamlanan_dersler']:
                        st.session_state.ilerleme['tamamlanan_dersler'].append(konu_id)
                        st.session_state.ilerleme['basari_puani'] += 10
                        ilerleme_kaydet()
                        st.balloons()
                        st.rerun()

# Testler fonksiyonu
def testler():
    st.markdown("<h1 class='main-header'>🎯 Python Testleri</h1>", unsafe_allow_html=True)
    
    testler_listesi = tum_testleri_yukle()
    
    if not testler_listesi:
        st.warning("📂 Henüz test içeriği yüklenmemiş.")
        st.info("Test dosyalarını `data/testler/` klasörüne ekleyin.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Toplam Test", len(testler_listesi))
    with col2:
        cozulen = len(st.session_state.ilerleme['cozulen_testler'])
        st.metric("✅ Çözülen", cozulen)
    with col3:
        basari = st.session_state.ilerleme.get('basari_puani', 0)
        st.metric("⭐ Başarı Puanı", basari)

    st.markdown("---")

    for test_data in testler_listesi:
        test_id = test_data.get('konu_id', 0)
        konu = test_data.get('konu_baslik', 'İsimsiz Test')
        sorular = test_data.get('test_sorulari', [])
        
        if not sorular:
            continue
        
        cozuldu = test_id in st.session_state.ilerleme['cozulen_testler']
        icon = "✅" if cozuldu else "○"
        
        with st.expander(f"{icon} {konu} - {len(sorular)} soru", expanded=False):
            if cozuldu:
                st.success(f"✅ Bu test çözüldü! Skor: {st.session_state.test_sonuclari.get(test_id, 0)}/{len(sorular)}")
                if st.button(f"🔄 Tekrar Çöz", key=f"tekrar_{test_id}"):
                    st.session_state.aktif_test = test_id
                    st.session_state.test_cevaplari = {}
                    st.rerun()
            else:
                if st.button(f"▶️ Teste Başla", key=f"baslat_{test_id}", type="primary"):
                    st.session_state.aktif_test = test_id
                    st.session_state.test_cevaplari = {}
                    st.rerun()
            
            if st.session_state.aktif_test == test_id:
                st.subheader("🎯 Test Soruları")
                
                for idx, soru_data in enumerate(sorular):
                    st.write(f"**Soru {idx+1}:** {soru_data.get('soru', '')}")
                    
                    secenekler = soru_data.get('secenekler', [])
                    
                    cevap = st.radio(
                        "Cevabınız:",
                        secenekler,
                        key=f"soru_{test_id}_{idx}",
                        index=None
                    )
                    
                    if cevap:
                        st.session_state.test_cevaplari[idx] = cevap[0]
                    
                    st.markdown("---")
                
                if len(st.session_state.test_cevaplari) == len(sorular):
                    if st.button("📤 Testi Gönder", type="primary", key=f"gonder_{test_id}"):
                        dogru_sayisi = 0
                        for idx, soru_data in enumerate(sorular):
                            if st.session_state.test_cevaplari.get(idx) == soru_data.get('cevap'):
                                dogru_sayisi += 1
                        
                        st.session_state.test_sonuclari[test_id] = dogru_sayisi
                        if test_id not in st.session_state.ilerleme['cozulen_testler']:
                            st.session_state.ilerleme['cozulen_testler'].append(test_id)
                            st.session_state.ilerleme['basari_puani'] += dogru_sayisi * 5
                        
                        ilerleme_kaydet()
                        st.session_state.aktif_test = None
                        st.session_state.test_cevaplari = {}
                        st.rerun()

# Bulmacalar fonksiyonu
def bulmacalar():
    st.markdown("<h1 class='main-header'>🧩 Kod Bulmacaları</h1>", unsafe_allow_html=True)
    
    bulmacalar_listesi = tum_bulmacalari_yukle()
    
    if not bulmacalar_listesi:
        st.warning("📂 Henüz bulmaca içeriği yüklenmemiş.")
        st.info("Bulmaca dosyalarını `data/bulmacalar/` klasörüne ekleyin.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧩 Toplam Bulmaca", len(bulmacalar_listesi))
    with col2:
        cozulen = len(st.session_state.ilerleme['cozulen_bulmacalar'])
        st.metric("✅ Çözülen", cozulen)
    with col3:
        basari = st.session_state.ilerleme.get('basari_puani', 0)
        st.metric("⭐ Başarı Puanı", basari)

    st.markdown("---")

    for bulmaca_data in bulmacalar_listesi:
        bulmaca_id = bulmaca_data.get('konu_id', 0)
        konu = bulmaca_data.get('konu_baslik', 'İsimsiz Bulmaca')
        bulmacalar_list = bulmaca_data.get('bulmacalar', [])
        
        if not bulmacalar_list:
            continue
        
        cozuldu = bulmaca_id in st.session_state.ilerleme['cozulen_bulmacalar']
        icon = "✅" if cozuldu else "○"
        
        with st.expander(f"{icon} {konu} - {len(bulmacalar_list)} bulmaca", expanded=False):
            for idx, bulmaca in enumerate(bulmacalar_list):
                st.subheader(f"🎯 Bulmaca {idx+1}")
                st.write(f"**Görev:** {bulmaca.get('soru', '')}")
                
                if 'ipucu' in bulmaca:
                    with st.expander("💡 İpucu"):
                        st.info(bulmaca['ipucu'])
                
                if 'zorluk' in bulmaca:
                    zorluk_renk = {
                        'kolay': '🟢',
                        'orta': '🟡',
                        'zor': '🔴'
                    }
                    st.write(f"**Zorluk:** {zorluk_renk.get(bulmaca['zorluk'], '⚪')} {bulmaca['zorluk'].title()}")
                
                cozum_kodu = st.text_area(
                    "Çözümünüz:",
                    height=200,
                    key=f"bulmaca_{bulmaca_id}_{idx}"
                )
                
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if st.button(f"🚀 Çalıştır", key=f"calistir_bulmaca_{bulmaca_id}_{idx}"):
                        try:
                            output = io.StringIO()
                            with contextlib.redirect_stdout(output):
                                exec(cozum_kodu, {'__builtins__': __builtins__})
                            st.success("✅ Kod çalıştı!")
                            if output.getvalue():
                                st.code(output.getvalue())
                        except Exception as e:
                            st.error(f"❌ Hata: {str(e)}")
                
                with st.expander("🔍 Çözümü Gör"):
                    st.code(bulmaca.get('cozum', ''), language='python')
                    if st.button(f"✅ Çözdüm!", key=f"cozdum_{bulmaca_id}_{idx}"):
                        if bulmaca_id not in st.session_state.ilerleme['cozulen_bulmacalar']:
                            st.session_state.ilerleme['cozulen_bulmacalar'].append(bulmaca_id)
                            st.session_state.ilerleme['basari_puani'] += 15
                            ilerleme_kaydet()
                            st.success("🎉 Tebrikler!")
                            st.rerun()
                
                st.markdown("---")

# İlerleme fonksiyonu
def ilerleme():
    st.markdown("<h1 class='main-header'>📊 Öğrenme İlerlemen</h1>", unsafe_allow_html=True)
    st.write("Ne kadar yol kat ettiğini gör, hedeflerine ulaş!")
    
    ilerleme_yukle()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📚 Tamamlanan Dersler",
            len(st.session_state.ilerleme['tamamlanan_dersler'])
        )
    
    with col2:
        st.metric(
            "🎯 Çözülen Testler",
            len(st.session_state.ilerleme['cozulen_testler'])
        )
    
    with col3:
        st.metric(
            "🧩 Çözülen Bulmacalar",
            len(st.session_state.ilerleme['cozulen_bulmacalar'])
        )
    
    with col4:
        st.metric(
            "💻 Kod Denemeleri",
            st.session_state.ilerleme['toplam_kod_denemesi']
        )
    
    st.markdown("---")
    
    st.subheader("⭐ Başarı Puanın")
    basari_puani = st.session_state.ilerleme.get('basari_puani', 0)
    max_puan = 1000
    progress = min(basari_puani / max_puan, 1.0)
    st.progress(progress)
    st.write(f"**{basari_puani} / {max_puan}** puan")
    
    if basari_puani < 100:
        seviye = "🥉 Başlangıç"
    elif basari_puani < 300:
        seviye = "🥈 Orta"
    elif basari_puani < 600:
        seviye = "🥇 İleri"
    else:
        seviye = "💎 Uzman"
    
    st.info(f"**Mevcut Seviye:** {seviye}")
    
    st.markdown("---")
    
    with st.expander("⚠️ Tehlikeli Alan"):
        st.warning("Tüm ilerleme verilerini sıfırlayabilirsiniz")
        if st.button("🗑️ Tüm İlerlememi Sıfırla", type="secondary"):
            st.session_state.ilerleme = {
                "tamamlanan_dersler": [],
                "cozulen_testler": [],
                "cozulen_bulmacalar": [],
                "toplam_kod_denemesi": 0,
                "basari_puani": 0
            }
            st.session_state.test_sonuclari = {}
            ilerleme_kaydet()
            st.success("✅ İlerleme sıfırlandı!")
            st.rerun()

# Ayarlar fonksiyonu
def ayarlar():
    st.markdown("<h1 class='main-header'>⚙️ Ayarlar ve Veri Yönetimi</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📁 Dosya Yönetimi", "📋 Metin ile Yükleme", "💾 Yedekleme", "ℹ️ Hakkında"])
    
    # TAB 1: Dosya Yönetimi
    with tab1:
        st.subheader("📥 JSON Dosya Yükleme")
        st.write("Ders, test veya bulmaca içeriklerini JSON formatında yükle")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("**📚 Dersler**")
            ders_dosya = st.file_uploader("Ders JSON", type=['json'], key="ders_upload")
            if ders_dosya is not None:
                try:
                    veri = json.load(ders_dosya)
                    dosya_adi = ders_dosya.name
                    kayit_yolu = f"data/dersler/{dosya_adi}"
                    if json_dosya_kaydet(kayit_yolu, veri):
                        st.success(f"✅ {dosya_adi} yüklendi!")
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")
        
        with col2:
            st.info("**🎯 Testler**")
            test_dosya = st.file_uploader("Test JSON", type=['json'], key="test_upload")
            if test_dosya is not None:
                try:
                    veri = json.load(test_dosya)
                    dosya_adi = test_dosya.name
                    kayit_yolu = f"data/testler/{dosya_adi}"
                    if json_dosya_kaydet(kayit_yolu, veri):
                        st.success(f"✅ {dosya_adi} yüklendi!")
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")
        
        with col3:
            st.info("**🧩 Bulmacalar**")
            bulmaca_dosya = st.file_uploader("Bulmaca JSON", type=['json'], key="bulmaca_upload")
            if bulmaca_dosya is not None:
                try:
                    veri = json.load(bulmaca_dosya)
                    dosya_adi = bulmaca_dosya.name
                    kayit_yolu = f"data/bulmacalar/{dosya_adi}"
                    if json_dosya_kaydet(kayit_yolu, veri):
                        st.success(f"✅ {dosya_adi} yüklendi!")
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")
        
        st.markdown("---")
        
        st.subheader("📂 Yüklü Dosyalar")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**📚 Dersler:**")
            dersler = tum_dersleri_yukle()
            st.write(f"{len(dersler)} ders yüklü")
            if dersler:
                for ders in dersler:
                    st.write(f"  • {ders.get('konu_baslik', 'İsimsiz')}")
        
        with col2:
            st.write("**🎯 Testler:**")
            testler = tum_testleri_yukle()
            st.write(f"{len(testler)} test yüklü")
            if testler:
                for test in testler:
                    st.write(f"  • {test.get('konu_baslik', 'İsimsiz')}")
        
        with col3:
            st.write("**🧩 Bulmacalar:**")
            bulmacalar = tum_bulmacalari_yukle()
            st.write(f"{len(bulmacalar)} bulmaca yüklü")
            if bulmacalar:
                for bulmaca in bulmacalar:
                    st.write(f"  • {bulmaca.get('konu_baslik', 'İsimsiz')}")
    
    # TAB 2: Metin ile Yükleme
    with tab2:
        st.subheader("📋 JSON Metin ile Yükleme")
        st.write("JSON kodunu doğrudan yapıştırarak yükleme yapabilirsiniz")
        
        yp_secim = st.radio("Ne yüklemek istiyorsunuz?", ["📚 Ders", "🎯 Test", "🧩 Bulmaca"], horizontal=True)
        
        json_metni = st.text_area(
            "JSON İçeriğini yapıştırın:",
            height=400,
            placeholder='{"konu_id": 1, "konu_baslik": "..."}'
        )
        
        if st.button("✅ Yükle", type="primary", use_container_width=True):
            if json_metni.strip():
                try:
                    veri = json.loads(json_metni)
                    
                    if yp_secim == "📚 Ders":
                        dosya_adi = f"ders_{veri.get('konu_id', 'yeni')}.json"
                        kayit_yolu = f"data/dersler/{dosya_adi}"
                    elif yp_secim == "🎯 Test":
                        dosya_adi = f"test_{veri.get('konu_id', 'yeni')}.json"
                        kayit_yolu = f"data/testler/{dosya_adi}"
                    else:
                        dosya_adi = f"bulmaca_{veri.get('konu_id', 'yeni')}.json"
                        kayit_yolu = f"data/bulmacalar/{dosya_adi}"
                    
                    if json_dosya_kaydet(kayit_yolu, veri):
                        st.success(f"✅ {dosya_adi} başarıyla yüklendi!")
                        st.info(f"📂 Konumu: {kayit_yolu}")
                except json.JSONDecodeError as e:
                    st.error(f"❌ JSON Hatası: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")
            else:
                st.warning("⚠️ Lütfen JSON içeriği yapıştırın")
        
        st.markdown("---")
        st.subheader("📝 Örnek JSON Formatları")
        
        if st.checkbox("📚 Ders Örneğini Göster"):
            st.code('''
{
  "konu_id": 1,
  "konu_baslik": "Stringler",
  "aciklama": "Metin işlemleri",
  "seviye": "başlangıç",
  "video_link": "https://youtube.com/...",
  "video_suresi": "35:12",
  "ders_icerik": {
    "detayli_aciklama": "...",
    "ana_kavramlar": ["Kavram 1", "Kavram 2"]
  },
  "kod_ornekleri": [
    {
      "baslik": "Örnek 1",
      "kod": "print('Merhaba')",
      "aciklama": "Basit print örneği"
    }
  ]
}
            ''', language='json')
        
        if st.checkbox("🎯 Test Örneğini Göster"):
            st.code('''
{
  "konu_id": 1,
  "konu_baslik": "Stringler Testi",
  "test_sorulari": [
    {
      "soru": "Python'da string nasıl tanımlanır?",
      "secenekler": ["A) '...'", "B) ...", "C) ...", "D) ..."],
      "cevap": "A",
      "aciklama": "Stringler tırnak içine alınır",
      "zorluk": "kolay"
    }
  ]
}
            ''', language='json')
        
        if st.checkbox("🧩 Bulmaca Örneğini Göster"):
            st.code('''
{
  "konu_id": 1,
  "konu_baslik": "String Bulmacaları",
  "bulmacalar": [
    {
      "soru": "String'i tersten yazdırın",
      "ipucu": "[::-1] kullanabilirsiniz",
      "cozum": "kelime = 'python'\\nprint(kelime[::-1])",
      "zorluk": "kolay"
    }
  ]
}
            ''', language='json')
    
    # TAB 3: Yedekleme
    with tab3:
        st.subheader("💾 Yedekleme ve Geri Yükleme")
        st.write("Tüm verilerinizi ZIP dosyası olarak yedekleyin veya geri yükleyin")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Yedek Oluştur", use_container_width=True, type="primary"):
                zip_dosya = zip_yedek_olustur()
                if zip_dosya:
                    with open(zip_dosya, 'rb') as f:
                        st.download_button(
                            label="📥 Yedek İndir",
                            data=f,
                            file_name=zip_dosya,
                            mime="application/zip"
                        )
                    st.success(f"✅ Yedek oluşturuldu: {zip_dosya}")
        
        with col2:
            st.write("**📤 Yedekten Geri Yükle**")
            yuklenecek_zip = st.file_uploader("ZIP Dosyasını Seçin", type=['zip'], key="yedek_upload")
            if yuklenecek_zip is not None:
                if st.button("🔄 Geri Yükle", type="secondary", use_container_width=True):
                    try:
                        with open("temp_yedek.zip", "wb") as f:
                            f.write(yuklenecek_zip.getbuffer())
                        
                        if zip_yedek_geri_yukle("temp_yedek.zip"):
                            st.success("✅ Yedek başarıyla geri yüklendi!")
                            os.remove("temp_yedek.zip")
                            st.balloons()
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Hata: {str(e)}")
        
        st.markdown("---")
        st.info("""
        **💡 Bilgi:**
        - Yedek oluştur: Tüm data klasörünü ZIP'le
        - Geri yükle: Önceki yedekten tüm verileri geri al
        - Yedekler: İlerlemesi, dersler, testler ve bulmacalar dahil
        """)
    
    # TAB 4: Hakkında
    with tab4:
        st.subheader("ℹ️ Python Journey Hakkında")
        st.markdown("""
        ### 🐍 Python Journey v2.2
        
        **Son Güncellemeler:**
        - ✨ Derslerde anında kod çalıştırma
        - ✨ Ters sıralama (son yüklenenler üstte)
        - ✨ Sade ve temiz görünüm
        
        **Tüm Özellikler:**
        - 💻 Canlı Kod Sandbox
        - 📚 İnteraktif Dersler (derste doğrudan çalıştırma)
        - 🎯 Mini Testler
        - 🧩 Kod Bulmacaları
        - 📊 İlerleme Takibi
        - 📁 JSON Tabanlı İçerik Sistemi
        - 💾 Yedekleme Sistemi
        
        **Geliştirici:** Python Journey Team
        **Versiyon:** 2.2
        **Tarih:** 2024
        """)
        
        st.success("🚀 Öğrenmeye devam et!")

# Sidebar navigasyon
st.sidebar.title("🐍 Python Journey")

pages = {
    "🏠 Ana Sayfa": "ana_sayfa",
    "💻 Kod Sandbox": "kod_sandbox",
    "📖 Dersler": "dersler",
    "🎯 Testler": "testler",
    "🎮 Bulmacalar": "bulmacalar",
    "📊 İlerleme": "ilerleme",
    "⚙️ Ayarlar": "ayarlar"
}

selected_page = st.sidebar.radio("Sayfayı Seç:", list(pages.keys()))

# Ana sayfa içeriği
if selected_page == "🏠 Ana Sayfa":
    st.markdown("<h1 class='main-header'>🐍 Python Journey'e Hoş Geldin!</h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        dersler = tum_dersleri_yukle()
        st.metric("📚 Toplam Ders", len(dersler))
    
    with col2:
        testler = tum_testleri_yukle()
        st.metric("🎯 Toplam Test", len(testler))
    
    with col3:
        bulmacalar = tum_bulmacalari_yukle()
        st.metric("🧩 Toplam Bulmaca", len(bulmacalar))
    
    with col4:
        basari = st.session_state.ilerleme.get('basari_puani', 0)
        st.metric("⭐ Başarı Puanı", basari)
    
    st.markdown("---")
    
    st.subheader("🚀 Özellikler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **💻 Kod Sandbox**
        - Canlı Python editörü
        - Anında kod çalıştırma
        - Hata mesajlarıyla öğrenme
        - Örnek kod şablonları
        """)
        
        st.info("""
        **📖 İnteraktif Dersler**
        - Video eşliğinde öğrenme
        - Kod örnekleriyle pratik
        - JSON tabanlı içerik
        - Adım adım ilerleme
        """)
    
    with col2:
        st.info("""
        **🎯 Mini Testler**
        - Çoktan seçmeli sorular
        - Anında geri bildirim
        - Başarı takibi
        - Detaylı açıklamalar
        """)
        
        st.info("""
        **🎮 Kod Bulmacaları**
        - Eğlenceli challenge'lar
        - Zorluk seviyeleri
        - İpucu sistemi
        - Çözüm örnekleri
        """)
    
    st.markdown("---")
    
    st.subheader("⚡ Hızlı Başlangıç")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💻 Kod Dene", use_container_width=True, type="primary"):
            st.session_state.current_page = "💻 Kod Sandbox"
            st.rerun()
    
    with col2:
        if st.button("📖 Derslere Başla", use_container_width=True):
            st.session_state.current_page = "📖 Dersler"
            st.rerun()
    
    with col3:
        if st.button("🎯 Test Çöz", use_container_width=True):
            st.session_state.current_page = "🎯 Testler"
            st.rerun()
    
    with col4:
        if st.button("🧩 Bulmaca Çöz", use_container_width=True):
            st.session_state.current_page = "🎮 Bulmacalar"
            st.rerun()
    
    st.markdown("---")
    
    st.subheader("📊 İlerleme Özeti")
    
    tamamlanan_ders = len(st.session_state.ilerleme['tamamlanan_dersler'])
    cozulen_test = len(st.session_state.ilerleme['cozulen_testler'])
    cozulen_bulmaca = len(st.session_state.ilerleme['cozulen_bulmacalar'])
    kod_denemesi = st.session_state.ilerleme['toplam_kod_denemesi']
    
    if tamamlanan_ders == 0 and cozulen_test == 0 and cozulen_bulmaca == 0:
        st.info("🎯 **Henüz aktiviten yok!** Yukarıdaki butonlardan birini seçerek başla.")
    else:
        st.success(f"""
        **✨ Harika ilerliyorsun!**
        - ✅ {tamamlanan_ders} ders tamamlandı
        - ✅ {cozulen_test} test çözüldü
        - ✅ {cozulen_bulmaca} bulmaca çözüldü
        - ✅ {kod_denemesi} kod denemesi yapıldı
        """)
    
    st.markdown("---")
    
    st.info("""
    💡 **İpucu:** Python öğrenmek bir maraton, sprint değil. Her gün biraz pratik yap, 
    kod yaz, hata yap, öğren! Başarı senin olacak! 🚀
    """)

elif selected_page == "💻 Kod Sandbox":
    kod_sandbox()

elif selected_page == "📖 Dersler":
    dersler()

elif selected_page == "🎯 Testler":
    testler()

elif selected_page == "🎮 Bulmacalar":
    bulmacalar()

elif selected_page == "📊 İlerleme":
    ilerleme()

elif selected_page == "⚙️ Ayarlar":
    ayarlar()
