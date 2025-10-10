import streamlit as st
import json
import os
from datetime import datetime
import io
import contextlib

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
    
    return dersler

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
    
    return testler

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
    
    return bulmacalar

def ilerleme_kaydet():
    """İlerleme verilerini kaydeder"""
    json_dosya_kaydet("data/ilerleme.json", st.session_state.ilerleme)

def ilerleme_yukle():
    """İlerleme verilerini yükler"""
    ilerleme_verisi = json_dosya_yukle("data/ilerleme.json")
    if ilerleme_verisi:
        st.session_state.ilerleme = ilerleme_verisi

# Kod Sandbox fonksiyonu
def kod_sandbox():
    st.markdown("<h1 class='main-header'>💻 Python Kod Sandbox</h1>", unsafe_allow_html=True)
    st.write("Kodunu yaz ve çalıştır! Hataları gör, öğren!")
    
    # Eğer derslerden kod geldiyse onu göster
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
    
    # Kod editörü
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
                # Çıktıyı yakala
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
    
    # Çıktıyı göster
    if st.session_state.last_output:
        st.subheader("📤 Çıktı:")
        if "HATA:" in st.session_state.last_output:
            st.error(st.session_state.last_output)
        else:
            st.success(st.session_state.last_output)
    
    # Hızlı örnek kodlar
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
          "seviye": "başlangıç",
          "ders_icerik": {...},
          "kod_ornekleri": [...],
          "video_link": "..."
        }
        """)
    return

# Ders istatistikleri
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

# Dersleri göster
for ders in dersler_listesi:
    konu_id = ders.get('konu_id', 0)
    konu_baslik = ders.get('konu_baslik', 'İsimsiz Ders')
    aciklama = ders.get('aciklama', '')
    seviye = ders.get('seviye', 'başlangıç')
    video_link = ders.get('video_link', '')
    video_suresi = ders.get('video_suresi', '')
    
    # Tamamlanmış mı kontrol et
    tamamlandi = konu_id in st.session_state.ilerleme['tamamlanan_dersler']
    icon = "✅" if tamamlandi else "📌"
    
    with st.expander(f"{icon} {konu_baslik} - {seviye.title()}", expanded=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**📝 Açıklama:** {aciklama}")
            if video_suresi:
                st.write(f"**🎬 Süre:** {video_suresi}")
            if video_link:
                st.write(f"**🔗 Video:** [YouTube'da İzle]({video_link})")
        
        with col2:
            if tamamlandi:
                st.success("✅ Tamamlandı")
            else:
                if st.button("✓ Tamamla", key=f"tamam_ders_{konu_id}"):
                    if konu_id not in st.session_state.ilerleme['tamamlanan_dersler']:
                        st.session_state.ilerleme['tamamlanan_dersler'].append(konu_id)
                        st.session_state.ilerleme['basari_puani'] += 10
                        ilerleme_kaydet()
                        st.rerun()
        
        # Ders içeriği detayları
        if 'ders_icerik' in ders:
            icerik = ders['ders_icerik']
            st.subheader("📚 Ders İçeriği")
            
            if isinstance(icerik, dict):
                if 'detayli_aciklama' in icerik:
                    st.write(icerik['detayli_aciklama'])
                if 'ana_kavramlar' in icerik:
                    st.write("**🎯 Ana Kavramlar:**")
                    for kavram in icerik['ana_kavramlar']:
                        st.write(f"  • {kavram}")
            else:
                st.write(icerik)
        
        # Kod örnekleri
        if 'kod_ornekleri' in ders:
            st.subheader("💻 Kod Örnekleri")
            for idx, ornek in enumerate(ders['kod_ornekleri']):
                if isinstance(ornek, dict):
                    st.write(f"**{ornek.get('baslik', f'Örnek {idx+1}')}**")
                    if 'aciklama' in ornek:
                        st.write(ornek['aciklama'])
                    st.code(ornek.get('kod', ''), language='python')
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if st.button(f"🚀 Sandbox'ta Dene", key=f"dene_{konu_id}_{idx}"):
                            st.session_state.deneme_kodu = ornek.get('kod', '')
                            st.session_state.current_page = "💻 Kod Sandbox"
                            st.success("🎯 Kod Sandbox'a yönlendiriliyor...")
                            st.rerun()
                else:
                    st.code(ornek, language='python')
        
        # Pratik alıştırmalar
        if 'pratik_alistirmalar' in ders:
            st.subheader("✏️ Pratik Alıştırmalar")
            for idx, alistirma in enumerate(ders['pratik_alistirmalar']):
                st.write(f"{idx+1}. {alistirma}")

testler_listesi = tum_testleri_yukle()

if not testler_listesi:
    st.warning("📂 Henüz test içeriği yüklenmemiş.")
    st.info("""
    **Test eklemek için:**
    1. `data/testler/` klasörü oluştur
    2. JSON formatında test dosyalarını ekle
    3. Örnek format için derslerdeki test_sorulari yapısını kullan
    """)
    return

# Test istatistikleri
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

# Testleri göster
for test_data in testler_listesi:
    test_id = test_data.get('konu_id', 0)
    konu = test_data.get('konu_baslik', 'İsimsiz Test')
    sorular = test_data.get('test_sorulari', [])
    
    if not sorular:
        continue
    
    cozuldu = test_id in st.session_state.ilerleme['cozulen_testler']
    icon = "✅" if cozuldu else "📝"
    
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
        
        # Aktif test ise soruları göster
        if st.session_state.aktif_test == test_id:
            st.subheader("🎯 Test Soruları")
            
            for idx, soru_data in enumerate(sorular):
                st.write(f"**Soru {idx+1}:** {soru_data.get('soru', '')}")
                
                secenekler = soru_data.get('secenekler', [])
                dogru_cevap = soru_data.get('cevap', '')
                
                # Kullanıcı cevabı
                cevap = st.radio(
                    "Cevabınız:",
                    secenekler,
                    key=f"soru_{test_id}_{idx}",
                    index=None
                )
                
                if cevap:
                    st.session_state.test_cevaplari[idx] = cevap[0]  # A, B, C, D
                
                st.markdown("---")
            
            # Test gönderme
            if len(st.session_state.test_cevaplari) == len(sorular):
                if st.button("📤 Testi Gönder", type="primary", key=f"gonder_{test_id}"):
                    dogru_sayisi = 0
                    for idx, soru_data in enumerate(sorular):
                        if st.session_state.test_cevaplari.get(idx) == soru_data.get('cevap'):
                            dogru_sayisi += 1
                    
                    # Sonuçları kaydet
                    st.session_state.test_sonuclari[test_id] = dogru_sayisi
                    if test_id not in st.session_state.ilerleme['cozulen_testler']:
                        st.session_state.ilerleme['cozulen_testler'].append(test_id)
                        st.session_state.ilerleme['basari_puani'] += dogru_sayisi * 5
                    
                    ilerleme_kaydet()
                    st.session_state.aktif_test = None
                    st.session_state.test_cevaplari = {}
                    st.rerun()

bulmacalar_listesi = tum_bulmacalari_yukle()

if not bulmacalar_listesi:
    st.warning("📂 Henüz bulmaca içeriği yüklenmemiş.")
    st.info("""
    **Bulmaca eklemek için:**
    1. `data/bulmacalar/` klasörü oluştur
    2. JSON formatında bulmaca dosyalarını ekle
    3. Örnek format için derslerdeki bulmacalar yapısını kullan
    """)
    return

# Bulmaca istatistikleri
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

# Bulmacaları göster
for bulmaca_data in bulmacalar_listesi:
    bulmaca_id = bulmaca_data.get('konu_id', 0)
    konu = bulmaca_data.get('konu_baslik', 'İsimsiz Bulmaca')
    bulmacalar = bulmaca_data.get('bulmacalar', [])
    
    if not bulmacalar:
        continue
    
    cozuldu = bulmaca_id in st.session_state.ilerleme['cozulen_bulmacalar']
    icon = "✅" if cozuldu else "🧩"
    
    with st.expander(f"{icon} {konu} - {len(bulmacalar)} bulmaca", expanded=False):
        for idx, bulmaca in enumerate(bulmacalar):
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
            
            # Çözüm alanı
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
                        st.success("🎉 Tebrikler!


st.rerun()
                
                st.markdown("---")

# İlerleme fonksiyonu
def ilerleme():
    st.markdown("<h1 class='main-header'>📊 Öğrenme İlerlemen</h1>", unsafe_allow_html=True)
    st.write("Ne kadar yol kat ettiğini gör, hedeflerine ulaş!")
    
    # İlerleme verilerini yükle
    ilerleme_yukle()
    
    # Genel istatistikler
    st.subheader("📈 Genel İstatistikler")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric(
            "📚 Tamamlanan Dersler",
            len(st.session_state.ilerleme['tamamlanan_dersler'])
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric(
            "🎯 Çözülen Testler",
            len(st.session_state.ilerleme['cozulen_testler'])
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric(
            "🧩 Çözülen Bulmacalar",
            len(st.session_state.ilerleme['cozulen_bulmacalar'])
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric(
            "💻 Kod Denemeleri",
            st.session_state.ilerleme['toplam_kod_denemesi']
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Başarı puanı
    st.subheader("⭐ Başarı Puanın")
    basari_puani = st.session_state.ilerleme.get('basari_puani', 0)
    
    # Progress bar
    max_puan = 1000  # Örnek maksimum puan
    progress = min(basari_puani / max_puan, 1.0)
    st.progress(progress)
    st.write(f"**{basari_puani} / {max_puan}** puan")
    
    # Seviye sistemi
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
    
    # Detaylı analiz
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Ders İlerlemesi")
        dersler = tum_dersleri_yukle()
        if dersler:
            toplam_ders = len(dersler)
            tamamlanan = len(st.session_state.ilerleme['tamamlanan_dersler'])
            yuzde = int((tamamlanan / toplam_ders * 100)) if toplam_ders > 0 else 0
            
            st.metric("İlerleme", f"%{yuzde}")
            st.progress(yuzde / 100)
            st.write(f"{tamamlanan} / {toplam_ders} ders tamamlandı")
        else:
            st.info("Henüz ders yüklenmemiş")
    
    with col2:
        st.subheader("🎯 Test Başarısı")
        if st.session_state.test_sonuclari:
            toplam_dogru = sum(st.session_state.test_sonuclari.values())
            toplam_soru = len(st.session_state.test_sonuclari) * 3  # Ortalama 3 soru varsayımı
            basari_orani = int((toplam_dogru / toplam_soru * 100)) if toplam_soru > 0 else 0
            
            st.metric("Başarı Oranı", f"%{basari_orani}")
            st.progress(basari_orani / 100)
            st.write(f"{toplam_dogru} doğru cevap")
        else:
            st.info("Henüz test çözülmemiş")
    
    st.markdown("---")
    
    # Aktivite geçmişi
    st.subheader("📅 Son Aktiviteler")
    st.info("""
    **🎯 Sonraki Hedefler:**
    - Tamamlanmayan dersleri bitir
    - Tüm testleri çöz
    - Bulmacalara göz at
    - Kod Sandbox'ta pratik yap
    """)
    
    # İstatistikleri sıfırlama
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
    
    tab1, tab2, tab3 = st.tabs(["📁 Dosya Yönetimi", "🎨 Görünüm", "ℹ️ Hakkında"])
    
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
        
        st.subheader("📤 Veri Dışa Aktarma")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 İlerlememi Yedekle", use_container_width=True):
                yedek_veri = {
                    "ilerleme": st.session_state.ilerleme,
                    "test_sonuclari": st.session_state.test_sonuclari,
                    "tarih": datetime.now().isoformat()
                }
                json_str = json.dumps(yedek_veri, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 İndir",
                    data=json_str,
                    file_name=f"python_journey_yedek_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 İstatistikleri Dışa Aktar", use_container_width=True):
                istatistik_veri = {
                    "toplam_ders": len(tum_dersleri_yukle()),
                    "tamamlanan_ders": len(st.session_state.ilerleme['tamamlanan_dersler']),
                    "cozulen_test": len(st.session_state.ilerleme['cozulen_testler']),
                    "cozulen_bulmaca": len(st.session_state.ilerleme['cozulen_bulmacalar']),
                    "kod_denemesi": st.session_state.ilerleme['toplam_kod_denemesi'],
                    "basari_puani": st.session_state.ilerleme['basari_puani']
                }
                json_str = json.dumps(istatistik_veri, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 İndir",
                    data=json_str,
                    file_name=f"istatistikler_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
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
    
    with tab2:
        st.subheader("🎨 Görünüm Ayarları")
        
        st.write("**📱 Tema Seçimi**")
        tema = st.selectbox(
            "Tema",
            ["Açık", "Koyu", "Sistem Varsayılanı"],
            index=0
        )
        st.info(f"🎯 {tema} teması seçildi (Streamlit ayarlarından değiştirilebilir)")
        
        st.markdown("---")
        
        st.write("**🔤 Yazı Boyutu**")
        yazi_boyutu = st.slider("Yazı Boyutu", 12, 20, 14)
        st.info(f"Yazı boyutu: {yazi_boyutu}px (Yakında uygulanacak)")
        
        st.markdown("---")
        
        st.write("**🎭 Görünüm Özellikleri**")
        animasyon = st.checkbox("Animasyonları Aç", value=True)
        ses = st.checkbox("Ses Efektleri", value=False)
        bildirim = st.checkbox("Bildirimler", value=True)
        
        if st.button("💾 Ayarları Kaydet"):
            st.success("✅ Ayarlar kaydedildi!")
    
    with tab3:
        st.subheader("ℹ️ Python Journey Hakkında")
        
        st.markdown("""
        ### 🐍 Python Journey v2.0
        
        **Özellikler:**
        - 💻 Canlı Kod Sandbox
        - 📚 İnteraktif Dersler
        - 🎯 Mini Testler
        - 🧩 Kod Bulmacaları
        - 📊 İlerleme Takibi
        - 📁 JSON Tabanlı İçerik Sistemi
        
        **Kullanım:**
        1. JSON formatında ders içerikleri yükle
        2. Dersleri takip et ve öğren
        3. Testlerle bilgini pekiştir
        4. Bulmacalarla pratik yap
        5. Kod Sandbox'ta dene
        
        **JSON Format Örnekleri:**
        
        📚 **Ders Formatı:**
```json
        {
          "konu_id": 1,
          "konu_baslik": "Stringler",
          "aciklama": "Metin işlemleri",
          "seviye": "başlangıç",
          "video_link": "https://youtube.com/...",
          "video_suresi": "35:12",
          "ders_icerik": {
            "detayli_aciklama": "...",
            "ana_kavramlar": ["..."]
          },
          "kod_ornekleri": [
            {
              "baslik": "Örnek 1",
              "kod": "print('Merhaba')",
              "aciklama": "..."
            }
          ],
          "test_sorulari": [...],
          "bulmacalar": [...]
        }
{
          "konu_id": 1,
          "konu_baslik": "Stringler Testi",
          "test_sorulari": [
            {
              "soru": "Python'da string nasıl tanımlanır?",
              "secenekler": ["A) '...'", "B) ...", "C) ...", "D) ..."],
              "cevap": "A",
              "aciklama": "...",
              "zorluk": "kolay"
            }
          ]
        }

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
**Geliştirici:** Okan
    **Versiyon:** 2.0
    **Tarih:** 2024
    
    ---
    
    💡 **İpucu:** JSON dosyalarını `data/` klasörü altında organize edin:
    - `data/dersler/` - Ders içerikleri
    - `data/testler/` - Test soruları
    - `data/bulmacalar/` - Bulmacalar
    - `data/ilerleme.json` - İlerleme verileri
    """)
    
    st.success("🚀 Öğrenmeye devam et!")

st.markdown("---")

# Hoş geldin mesajı
st.success("👋 **Python öğrenme yolculuğuna hoş geldin!**")

# Hızlı istatistikler
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

# Özellikler
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

# Hızlı başlangıç
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

# Son aktiviteler
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

# Motivasyon mesajı
st.info("""
💡 **İpucu:** Python öğrenmek bir maraton, sprint değil. Her gün biraz pratik yap, 
kod yaz, hata yap, öğren! Başarı senin olacak! 🚀
""")
