# app.py - ANA DOSYA
import streamlit as st
import json
import os
from datetime import datetime

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

# Ana sayfa
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
    st.info("🔧 **Kod Sandbox yakında eklenecek...**")
elif menu == "📖 Dersler":
    st.info("📚 **Dersler yakında eklenecek...**")
elif menu == "🎮 Bulmacalar":
    st.info("🎯 **Bulmacalar yakında eklenecek...**")
elif menu == "📊 İlerlemem":
    st.info("📈 **İlerleme takibi yakında eklenecek...**")
