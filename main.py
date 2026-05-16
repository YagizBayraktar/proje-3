"""
╔══════════════════════════════════════════════════════════════════╗
║                3D BASKI ATÖLYE PRO v4.0  —                       ║
║                                                                  ║
║                Yağız BAYRAKTAR                                   ║
╚══════════════════════════════════════════════════════════════════╝

YENİ ÖZELLİKLER (60+):
 1. PyQt6 tabanlı modern arayüz
 2. Tema sistemi (Koyu/Açık/Neon/Kırmızı/Okyanus/Orman/Gün Batımı/Mor)
 3. Canlı filament fiyat güncelleme (web'den çek)
 4. Barkod / QR kod üretici
 5. Fatura oluşturma & PDF export
 6. Müşteri sadakat puanı sistemi
 7. Proje şablonları
 8. Çoklu yazıcı profili
 9. Bakım takvimi & uyarılar
10. Sarf malzeme takibi (nozul, tabla vb.)
11. Filament nem/kuru tutma takibi
12. Renk paleti yöneticisi
13. Üretim hattı (Kanban) görünümü
14. Takvim ve randevu sistemi
15. Müşteri mesajlaşma notu
16. Çoklu para birimi desteği
17. KDV hesaplama
18. İndirim kuponu sistemi
19. Toplu fiyat güncelleme
20. Proje çoğaltma (kopyala)
21. Gelişmiş arama & filtre
22. Sütun sıralaması
23. Favori projeler
24. Proje etiket sistemi
25. Resim ekleme (proje fotoğrafı)
26. Çoklu döviz kuru
27. Yazıcı sıcaklık profilleri
28. Katman kalınlığı hesaplama
29. Dolgu oranı maliyet etkisi
30. Destek malzemesi hesabı
31. Post-processing maliyeti
32. Kargo fiyat hesaplama
33. Sipariş durumu takibi
34. E-posta şablonları
35. SMS şablonları
36. WhatsApp mesaj şablonu
37. Sosyal medya paylaşım notu
38. Ürün katalog oluşturucu
39. Fiyat listesi yazdırma
40. Haftalık/Aylık/Yıllık raporlar
41. Kar-zarar grafiği
42. Filament tüketim tahmini
43. Yazıcı kullanım süresi takibi
44. Elektrik faturası simülatörü
45. ROI (Yatırım getirisi) hesaplama
46. Rakip fiyat takibi notu
47. Müşteri doğum günü hatırlatma
48. VIP müşteri kategorisi
49. Toplu sipariş indirimi
50. Sezon kampanya yönetimi
51. Stok alarm sistemi
52. Otomatik yedekleme
53. Veri içe aktarma (CSV)
54. Çoklu kullanıcı desteği
55. Kullanıcı rol sistemi (Admin/Çalışan)
56. İşlem geçmişi ve geri alma
57. Gerçek zamanlı dashboard
58. Mini POS (satış noktası)
59. Müşteri kartı yazdırma
60. Kâr marjı simülatörü
61. Filament marka karşılaştırma
62. Yazıcı enerji raporu
63. Stok değer grafiği
64. Hedef & performans takibi
65. Not şifresi (güvenli notlar)
"""

import sys, os, json, csv, math, hashlib, random, shutil
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox,
    QListWidget, QListWidgetItem, QTabWidget, QScrollArea, QFrame,
    QSplitter, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog, QInputDialog,
    QProgressBar, QSlider, QCheckBox, QSpinBox, QDoubleSpinBox,
    QDateEdit, QCalendarWidget, QGroupBox, QRadioButton, QButtonGroup,
    QSizePolicy, QStackedWidget, QToolButton, QMenu, QStatusBar,
    QTreeWidget, QTreeWidgetItem, QColorDialog, QFontDialog,
    QSystemTrayIcon, QAbstractItemView
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QDate, QSize, QRect,
    QPropertyAnimation, QEasingCurve, QPoint, QSettings
)
from PyQt6.QtGui import (
    QIcon, QFont, QColor, QPalette, QPainter, QPen, QBrush,
    QLinearGradient, QRadialGradient, QPixmap, QAction,
    QKeySequence, QShortcut, QCursor, QFontMetrics
)

# ═══════════════════════════════════════════════════════════════
#  DOSYA YOLLARI
# ═══════════════════════════════════════════════════════════════
DATA_DIR      = Path("atolye_data")
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE    = DATA_DIR / "users.json"
PROJECTS_FILE = DATA_DIR / "projects.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
STOCK_FILE    = DATA_DIR / "stock.json"
SALES_FILE    = DATA_DIR / "sales.json"
EXPENSES_FILE = DATA_DIR / "expenses.json"
CUSTOMERS_FILE= DATA_DIR / "customers.json"
TASKS_FILE    = DATA_DIR / "tasks.json"
NOTES_FILE    = DATA_DIR / "notes.json"
LOG_FILE      = DATA_DIR / "activity_log.json"
BACKUP_DIR    = DATA_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)
TEMPLATES_FILE= DATA_DIR / "templates.json"
MAINTENANCE_FILE = DATA_DIR / "maintenance.json"
CAMPAIGNS_FILE= DATA_DIR / "campaigns.json"
ORDERS_FILE   = DATA_DIR / "orders.json"
PRINTERS_FILE = DATA_DIR / "printers.json"

# ═══════════════════════════════════════════════════════════════
#  TEMA SİSTEMİ
# ═══════════════════════════════════════════════════════════════
THEMES = {
    "🌑 Karanlık": {
        "bg":        "#0D0F14",
        "card":      "#161B22",
        "sidebar":   "#0F1117",
        "border":    "#21262D",
        "accent":    "#00D4FF",
        "accent2":   "#7B2FFF",
        "success":   "#00E676",
        "danger":    "#FF1744",
        "warning":   "#FFD600",
        "text":      "#C9D1D9",
        "text_dim":  "#8B949E",
        "input_bg":  "#1C2333",
        "header":    "#00D4FF",
        "btn_text":  "#FFFFFF",
    },
    "☀️ Açık": {
        "bg":        "#F0F2F5",
        "card":      "#FFFFFF",
        "sidebar":   "#E8EAF0",
        "border":    "#D0D7DE",
        "accent":    "#0969DA",
        "accent2":   "#6639BA",
        "success":   "#1A7F37",
        "danger":    "#CF222E",
        "warning":   "#9A6700",
        "text":      "#1F2328",
        "text_dim":  "#636C76",
        "input_bg":  "#F6F8FA",
        "header":    "#0969DA",
        "btn_text":  "#FFFFFF",
    },
    "🔴 Kırmızı": {
        "bg":        "#0A0000",
        "card":      "#1A0505",
        "sidebar":   "#0D0202",
        "border":    "#3D0A0A",
        "accent":    "#FF4444",
        "accent2":   "#FF8800",
        "success":   "#00FF88",
        "danger":    "#FF0000",
        "warning":   "#FFAA00",
        "text":      "#FFD0D0",
        "text_dim":  "#AA7777",
        "input_bg":  "#2A0808",
        "header":    "#FF4444",
        "btn_text":  "#FFFFFF",
    },
    "🌊 Okyanus": {
        "bg":        "#020B18",
        "card":      "#071B2E",
        "sidebar":   "#041224",
        "border":    "#0A3050",
        "accent":    "#00B4D8",
        "accent2":   "#0077B6",
        "success":   "#80FFDB",
        "danger":    "#FF6B6B",
        "warning":   "#FFD166",
        "text":      "#CAF0F8",
        "text_dim":  "#5A8A99",
        "input_bg":  "#071E35",
        "header":    "#00B4D8",
        "btn_text":  "#FFFFFF",
    },
    "🌲 Orman": {
        "bg":        "#020A02",
        "card":      "#071407",
        "sidebar":   "#041004",
        "border":    "#0A2E0A",
        "accent":    "#00E676",
        "accent2":   "#00897B",
        "success":   "#CCFF90",
        "danger":    "#FF6B6B",
        "warning":   "#FFD600",
        "text":      "#CCFFCC",
        "text_dim":  "#4A7A4A",
        "input_bg":  "#071407",
        "header":    "#00E676",
        "btn_text":  "#000000",
    },
    "🌅 Gün Batımı": {
        "bg":        "#0A0508",
        "card":      "#1A0D15",
        "sidebar":   "#0D0810",
        "border":    "#3D1030",
        "accent":    "#FF6B6B",
        "accent2":   "#FF8E53",
        "success":   "#51CF66",
        "danger":    "#FF1744",
        "warning":   "#FFD43B",
        "text":      "#FFE0CC",
        "text_dim":  "#AA6680",
        "input_bg":  "#200D18",
        "header":    "#FF6B6B",
        "btn_text":  "#FFFFFF",
    },
    "💜 Mor": {
        "bg":        "#080512",
        "card":      "#120A20",
        "sidebar":   "#0A0618",
        "border":    "#2A1050",
        "accent":    "#BD93F9",
        "accent2":   "#FF79C6",
        "success":   "#50FA7B",
        "danger":    "#FF5555",
        "warning":   "#FFB86C",
        "text":      "#F8F8F2",
        "text_dim":  "#6272A4",
        "input_bg":  "#1A1030",
        "header":    "#BD93F9",
        "btn_text":  "#FFFFFF",
    },
    "⚡ Neon": {
        "bg":        "#000000",
        "card":      "#0A0A0A",
        "sidebar":   "#050505",
        "border":    "#1A1A1A",
        "accent":    "#00FFFF",
        "accent2":   "#FF00FF",
        "success":   "#00FF00",
        "danger":    "#FF0000",
        "warning":   "#FFFF00",
        "text":      "#FFFFFF",
        "text_dim":  "#888888",
        "input_bg":  "#111111",
        "header":    "#00FFFF",
        "btn_text":  "#000000",
    },
}

# ═══════════════════════════════════════════════════════════════
#  FİLAMENT & YAZICI VERİLERİ
# ═══════════════════════════════════════════════════════════════
FILAMENT_DATA = {
    # PLA
    "eSUN PLA": {"fiyat": 650, "kategori": "PLA", "marka": "eSUN"},
    "Sunlu PLA": {"fiyat": 600, "kategori": "PLA", "marka": "Sunlu"},
    "Bambu PLA": {"fiyat": 1200, "kategori": "PLA", "marka": "Bambu Lab"},
    "Polymaker PLA": {"fiyat": 900, "kategori": "PLA", "marka": "Polymaker"},
    "Creality PLA": {"fiyat": 750, "kategori": "PLA", "marka": "Creality"},
    "Anycubic PLA": {"fiyat": 700, "kategori": "PLA", "marka": "Anycubic"},
    "Elegoo PLA": {"fiyat": 680, "kategori": "PLA", "marka": "Elegoo"},
    "Prusa PLA": {"fiyat": 1300, "kategori": "PLA", "marka": "Prusa"},
    "Flashforge PLA": {"fiyat": 800, "kategori": "PLA", "marka": "Flashforge"},
    # PLA+
    "eSUN PLA+": {"fiyat": 800, "kategori": "PLA+", "marka": "eSUN"},
    "Sunlu PLA+": {"fiyat": 750, "kategori": "PLA+", "marka": "Sunlu"},
    "Bambu PLA+": {"fiyat": 1350, "kategori": "PLA+", "marka": "Bambu Lab"},
    "Polymaker PLA+": {"fiyat": 1000, "kategori": "PLA+", "marka": "Polymaker"},
    "Creality PLA+": {"fiyat": 850, "kategori": "PLA+", "marka": "Creality"},
    # PETG
    "eSUN PETG": {"fiyat": 900, "kategori": "PETG", "marka": "eSUN"},
    "Sunlu PETG": {"fiyat": 850, "kategori": "PETG", "marka": "Sunlu"},
    "Bambu PETG": {"fiyat": 1300, "kategori": "PETG", "marka": "Bambu Lab"},
    "Polymaker PETG": {"fiyat": 1200, "kategori": "PETG", "marka": "Polymaker"},
    "Creality PETG": {"fiyat": 950, "kategori": "PETG", "marka": "Creality"},
    "Anycubic PETG": {"fiyat": 900, "kategori": "PETG", "marka": "Anycubic"},
    # ABS
    "eSUN ABS": {"fiyat": 800, "kategori": "ABS", "marka": "eSUN"},
    "Sunlu ABS": {"fiyat": 780, "kategori": "ABS", "marka": "Sunlu"},
    "Bambu ABS": {"fiyat": 1200, "kategori": "ABS", "marka": "Bambu Lab"},
    "Polymaker ABS": {"fiyat": 1100, "kategori": "ABS", "marka": "Polymaker"},
    # ASA
    "eSUN ASA": {"fiyat": 1100, "kategori": "ASA", "marka": "eSUN"},
    "Bambu ASA": {"fiyat": 1500, "kategori": "ASA", "marka": "Bambu Lab"},
    "Polymaker ASA": {"fiyat": 1400, "kategori": "ASA", "marka": "Polymaker"},
    # TPU
    "eSUN TPU": {"fiyat": 1200, "kategori": "TPU", "marka": "eSUN"},
    "Sunlu TPU": {"fiyat": 1100, "kategori": "TPU", "marka": "Sunlu"},
    "Bambu TPU": {"fiyat": 1700, "kategori": "TPU", "marka": "Bambu Lab"},
    "Polymaker TPU": {"fiyat": 1600, "kategori": "TPU", "marka": "Polymaker"},
    # Nylon
    "eSUN Nylon": {"fiyat": 1700, "kategori": "Nylon", "marka": "eSUN"},
    "Bambu Nylon": {"fiyat": 2600, "kategori": "Nylon", "marka": "Bambu Lab"},
    "Polymaker Nylon": {"fiyat": 2400, "kategori": "Nylon", "marka": "Polymaker"},
    # PC
    "eSUN PC": {"fiyat": 2200, "kategori": "PC", "marka": "eSUN"},
    "Bambu PC": {"fiyat": 3200, "kategori": "PC", "marka": "Bambu Lab"},
    # Özel
    "eSUN Silk PLA": {"fiyat": 950, "kategori": "Özel", "marka": "eSUN"},
    "Sunlu Silk PLA": {"fiyat": 900, "kategori": "Özel", "marka": "Sunlu"},
    "eSUN Wood PLA": {"fiyat": 1100, "kategori": "Özel", "marka": "eSUN"},
    "eSUN CF PLA": {"fiyat": 1600, "kategori": "CF", "marka": "eSUN"},
    "Polymaker CF": {"fiyat": 2000, "kategori": "CF", "marka": "Polymaker"},
    "eSUN PVA": {"fiyat": 1600, "kategori": "Destek", "marka": "eSUN"},
    "eSUN HIPS": {"fiyat": 850, "kategori": "Destek", "marka": "eSUN"},
    "Bambu Support": {"fiyat": 1400, "kategori": "Destek", "marka": "Bambu Lab"},
    # Resin
    "Elegoo Resin Std": {"fiyat": 400, "kategori": "Resin", "marka": "Elegoo"},
    "Elegoo Resin ABS-Like": {"fiyat": 550, "kategori": "Resin", "marka": "Elegoo"},
    "Anycubic Resin Std": {"fiyat": 380, "kategori": "Resin", "marka": "Anycubic"},
    "Anycubic Resin Plant-Based": {"fiyat": 650, "kategori": "Resin", "marka": "Anycubic"},
}

PRINTER_DATA = {
    "Bambu Lab": {
        "A1 Mini": {"watt": 150, "bed": "220x220", "type": "FDM"},
        "A1": {"watt": 300, "bed": "256x256", "type": "FDM"},
        "P1P": {"watt": 1000, "bed": "256x256", "type": "FDM"},
        "P1S": {"watt": 1000, "bed": "256x256", "type": "FDM"},
        "X1 Carbon": {"watt": 1000, "bed": "256x256", "type": "FDM"},
        "X1E": {"watt": 1400, "bed": "256x256", "type": "FDM"},
        "H2D": {"watt": 2200, "bed": "350x320", "type": "FDM"},
        "P2S": {"watt": 1000, "bed": "256x256", "type": "FDM"},
    },
    "Creality": {
        "Ender 3 V3 SE": {"watt": 350, "bed": "220x220", "type": "FDM"},
        "Ender 3 V3 KE": {"watt": 350, "bed": "220x220", "type": "FDM"},
        "Ender 3 S1 Pro": {"watt": 350, "bed": "220x220", "type": "FDM"},
        "K1": {"watt": 350, "bed": "220x220", "type": "FDM"},
        "K1 Max": {"watt": 1000, "bed": "300x300", "type": "FDM"},
        "K2 Plus": {"watt": 1000, "bed": "350x350", "type": "FDM"},
        "CR-10 Max": {"watt": 600, "bed": "450x450", "type": "FDM"},
        "Halot-One": {"watt": 50, "bed": "130x82", "type": "MSLA"},
    },
    "Anycubic": {
        "Kobra 2 Neo": {"watt": 250, "bed": "220x220", "type": "FDM"},
        "Kobra 2 Pro": {"watt": 300, "bed": "220x220", "type": "FDM"},
        "Kobra 2 Max": {"watt": 500, "bed": "420x420", "type": "FDM"},
        "Kobra 3": {"watt": 300, "bed": "220x220", "type": "FDM"},
        "Kobra S1": {"watt": 1000, "bed": "300x300", "type": "FDM"},
        "Photon Mono M3": {"watt": 140, "bed": "180x163", "type": "MSLA"},
        "Photon Mono 4 Ultra": {"watt": 160, "bed": "196x122", "type": "MSLA"},
    },
    "Elegoo": {
        "Neptune 4": {"watt": 300, "bed": "225x225", "type": "FDM"},
        "Neptune 4 Pro": {"watt": 350, "bed": "225x225", "type": "FDM"},
        "Neptune 4 Max": {"watt": 500, "bed": "420x420", "type": "FDM"},
        "Mars 4 Ultra": {"watt": 80, "bed": "153x77", "type": "MSLA"},
        "Saturn 4 Ultra": {"watt": 170, "bed": "218x123", "type": "MSLA"},
        "Jupiter 12K": {"watt": 260, "bed": "304x171", "type": "MSLA"},
    },
    "Prusa": {
        "MK4S": {"watt": 180, "bed": "250x210", "type": "FDM"},
        "XL": {"watt": 1000, "bed": "360x360", "type": "FDM"},
        "MINI+": {"watt": 120, "bed": "180x180", "type": "FDM"},
        "SL1S SPEED": {"watt": 150, "bed": "127x80", "type": "MSLA"},
    },
    "Flashforge": {
        "Adventurer 5M": {"watt": 350, "bed": "220x220", "type": "FDM"},
        "Adventurer 5M Pro": {"watt": 350, "bed": "220x220", "type": "FDM"},
        "Creator 4": {"watt": 800, "bed": "400x350", "type": "FDM"},
        "Guider 3 Ultra": {"watt": 750, "bed": "330x330", "type": "FDM"},
    },
    "Artillery": {
        "Sidewinder X3 Pro": {"watt": 450, "bed": "300x300", "type": "FDM"},
        "Genius Pro": {"watt": 350, "bed": "220x220", "type": "FDM"},
        "Hornet": {"watt": 200, "bed": "220x220", "type": "FDM"},
    },
    "Voron": {
        "Voron 0.2": {"watt": 250, "bed": "120x120", "type": "FDM"},
        "Voron Trident": {"watt": 800, "bed": "300x300", "type": "FDM"},
        "Voron 2.4": {"watt": 1200, "bed": "350x350", "type": "FDM"},
    },
    "BambuLab AMS": {
        "AMS Lite": {"watt": 20, "bed": "N/A", "type": "AMS"},
        "AMS Pro": {"watt": 30, "bed": "N/A", "type": "AMS"},
    },
}

# ═══════════════════════════════════════════════════════════════
#  YARDIMCI FONKSİYONLAR
# ═══════════════════════════════════════════════════════════════
def load_json(path, default):
    try:
        if Path(path).exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_settings():
    return load_json(SETTINGS_FILE, {
        "elektrik_fiyati": 1.73,
        "low_stock_threshold": 500,
        "theme": "🌑 Karanlık",
        "currency": "TL",
        "kdv_rate": 20,
        "backup_enabled": True,
    })

def save_settings(s):
    save_json(SETTINGS_FILE, s)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def load_users():
    return load_json(USERS_FILE, [])

def save_users(u):
    save_json(USERS_FILE, u)

def u_load(filepath, user):
    all_d = load_json(filepath, [])
    return [x for x in all_d if x.get("owner") == user]

def u_save(filepath, user, items):
    all_d = load_json(filepath, [])
    others = [x for x in all_d if x.get("owner") != user]
    save_json(filepath, others + items)

def log_activity(user, action, detail=""):
    logs = load_json(LOG_FILE, [])
    logs.append({
        "owner": user, "action": action, "detail": detail,
        "tarih": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    })
    logs = logs[-1000:]
    save_json(LOG_FILE, logs)

def calc_cost(gram, filament_name, hours, brand, model):
    fil = FILAMENT_DATA.get(filament_name, {"fiyat": 600})
    kg_price = fil["fiyat"]
    f_cost = (gram / 1000) * kg_price
    watt = PRINTER_DATA.get(brand, {}).get(model, {}).get("watt", 150)
    e_use = (watt / 1000) * hours
    e_price = get_settings().get("elektrik_fiyati", 1.73)
    e_cost = e_use * e_price
    total = f_cost + e_cost
    return round(total, 2), round(f_cost, 2), round(e_cost, 2), watt, round(e_use, 3)

def do_backup():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bdir = BACKUP_DIR / ts
    bdir.mkdir()
    for f in DATA_DIR.glob("*.json"):
        shutil.copy(f, bdir / f.name)

# ═══════════════════════════════════════════════════════════════
#  STİL YÖNETİCİSİ
# ═══════════════════════════════════════════════════════════════
class StyleManager:
    _theme = THEMES["🌑 Karanlık"]

    @classmethod
    def set_theme(cls, name):
        cls._theme = THEMES.get(name, THEMES["🌑 Karanlık"])

    @classmethod
    def t(cls, key):
        return cls._theme.get(key, "#FFFFFF")

    @classmethod
    def get_app_stylesheet(cls):
        T = cls._theme
        return f"""
        QMainWindow, QDialog {{
            background: {T['bg']};
        }}
        QWidget {{
            background: transparent;
            color: {T['text']};
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 13px;
        }}
        QLabel {{
            color: {T['text']};
            background: transparent;
        }}
        QPushButton {{
            background: {T['accent2']};
            color: {T['btn_text']};
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background: {T['accent']};
        }}
        QPushButton:pressed {{
            background: {T['border']};
        }}
        QPushButton.danger {{
            background: {T['danger']};
        }}
        QPushButton.success {{
            background: {T['success']};
            color: #000;
        }}
        QPushButton.flat {{
            background: transparent;
            color: {T['text']};
            border: 1px solid {T['border']};
        }}
        QPushButton.flat:hover {{
            background: {T['input_bg']};
        }}
        QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox, QDateEdit {{
            background: {T['input_bg']};
            color: {T['text']};
            border: 1px solid {T['border']};
            border-radius: 8px;
            padding: 6px 10px;
            selection-background-color: {T['accent']};
        }}
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {T['accent']};
        }}
        QComboBox {{
            background: {T['input_bg']};
            color: {T['text']};
            border: 1px solid {T['border']};
            border-radius: 8px;
            padding: 6px 10px;
        }}
        QComboBox::drop-down {{
            border: none;
            width: 24px;
        }}
        QComboBox QAbstractItemView {{
            background: {T['card']};
            color: {T['text']};
            border: 1px solid {T['border']};
            selection-background-color: {T['accent2']};
        }}
        QTabWidget::pane {{
            border: 1px solid {T['border']};
            background: {T['card']};
            border-radius: 8px;
        }}
        QTabBar::tab {{
            background: {T['input_bg']};
            color: {T['text_dim']};
            padding: 8px 16px;
            margin-right: 2px;
            border-radius: 6px 6px 0 0;
        }}
        QTabBar::tab:selected {{
            background: {T['accent2']};
            color: {T['btn_text']};
        }}
        QScrollArea {{
            border: none;
            background: transparent;
        }}
        QScrollBar:vertical {{
            background: {T['input_bg']};
            width: 8px;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {T['border']};
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {T['accent']};
        }}
        QTableWidget {{
            background: {T['card']};
            color: {T['text']};
            border: 1px solid {T['border']};
            border-radius: 8px;
            gridline-color: {T['border']};
        }}
        QTableWidget::item {{
            padding: 6px;
        }}
        QTableWidget::item:selected {{
            background: {T['accent2']};
        }}
        QHeaderView::section {{
            background: {T['input_bg']};
            color: {T['accent']};
            padding: 8px;
            border: 1px solid {T['border']};
            font-weight: bold;
        }}
        QFrame.card {{
            background: {T['card']};
            border: 1px solid {T['border']};
            border-radius: 12px;
        }}
        QFrame.sidebar {{
            background: {T['sidebar']};
            border-right: 1px solid {T['border']};
        }}
        QListWidget {{
            background: {T['card']};
            color: {T['text']};
            border: 1px solid {T['border']};
            border-radius: 8px;
        }}
        QListWidget::item:selected {{
            background: {T['accent2']};
        }}
        QProgressBar {{
            background: {T['input_bg']};
            border: 1px solid {T['border']};
            border-radius: 4px;
            text-align: center;
        }}
        QProgressBar::chunk {{
            background: {T['accent']};
            border-radius: 4px;
        }}
        QCheckBox::indicator {{
            width: 16px; height: 16px;
            border: 2px solid {T['border']};
            border-radius: 3px;
        }}
        QCheckBox::indicator:checked {{
            background: {T['accent']};
            border-color: {T['accent']};
        }}
        QGroupBox {{
            color: {T['accent']};
            border: 1px solid {T['border']};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 8px;
            font-weight: bold;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            padding: 0 8px;
        }}
        QStatusBar {{
            background: {T['sidebar']};
            color: {T['text_dim']};
        }}
        QMenuBar {{
            background: {T['sidebar']};
            color: {T['text']};
        }}
        QMenuBar::item:selected {{
            background: {T['accent2']};
        }}
        QMenu {{
            background: {T['card']};
            color: {T['text']};
            border: 1px solid {T['border']};
        }}
        QMenu::item:selected {{
            background: {T['accent2']};
        }}
        QToolTip {{
            background: {T['card']};
            color: {T['text']};
            border: 1px solid {T['accent']};
            border-radius: 4px;
            padding: 4px;
        }}
        QCalendarWidget {{
            background: {T['card']};
            color: {T['text']};
        }}
        QCalendarWidget QAbstractItemView {{
            selection-background-color: {T['accent2']};
            color: {T['text']};
        }}
        QTreeWidget {{
            background: {T['card']};
            color: {T['text']};
            border: 1px solid {T['border']};
            border-radius: 8px;
        }}
        QSplitter::handle {{
            background: {T['border']};
        }}
        """

SM = StyleManager

# ═══════════════════════════════════════════════════════════════
#  ÖZEL WİDGETLER
# ═══════════════════════════════════════════════════════════════
class KPICard(QFrame):
    def __init__(self, icon, label, value, color=None, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setMinimumHeight(100)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        icon_lbl = QLabel(icon)
        icon_lbl.setFont(QFont("Segoe UI Emoji", 22))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        name_lbl = QLabel(label)
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setStyleSheet(f"color: {SM.t('text_dim')}; font-size: 11px;")

        val_lbl = QLabel(value)
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        val_lbl.setFont(QFont("Courier New", 15, QFont.Weight.Bold))
        c = color or SM.t("text")
        val_lbl.setStyleSheet(f"color: {c}; font-size: 15px; font-weight: bold;")

        layout.addWidget(icon_lbl)
        layout.addWidget(name_lbl)
        layout.addWidget(val_lbl)
        self.val_lbl = val_lbl
        self.setStyleSheet(f"QFrame {{ background: {SM.t('card')}; border: 1px solid {SM.t('border')}; border-radius: 12px; }}")


class NavButton(QPushButton):
    def __init__(self, icon, text, parent=None):
        super().__init__(f" {icon}  {text}", parent)
        self.setCheckable(True)
        self.setMinimumHeight(44)
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {SM.t('text')};
                border: none;
                border-radius: 10px;
                text-align: left;
                padding-left: 16px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {SM.t('input_bg')};
            }}
            QPushButton:checked {{
                background: {SM.t('accent2')};
                color: {SM.t('btn_text')};
                font-weight: bold;
            }}
        """)


class SectionHeader(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        self.setStyleSheet(f"color: {SM.t('accent')}; border-bottom: 2px solid {SM.t('accent')}; padding-bottom: 4px;")


class StyledButton(QPushButton):
    def __init__(self, text, style="primary", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(38)
        colors = {
            "primary": (SM.t("accent2"), SM.t("accent")),
            "success": (SM.t("success"), "#00C060"),
            "danger":  (SM.t("danger"),  "#C62828"),
            "warning": (SM.t("warning"), "#E6C000"),
            "flat":    (SM.t("input_bg"), SM.t("border")),
        }
        bg, hover = colors.get(style, colors["primary"])
        tc = "#000" if style in ("success","warning") else SM.t("btn_text")
        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: {tc};
                border: none;
                border-radius: 8px;
                padding: 6px 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: {hover}; }}
            QPushButton:pressed {{ opacity: 0.8; }}
        """)


class CardFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {SM.t('card')};
                border: 1px solid {SM.t('border')};
                border-radius: 12px;
            }}
        """)


class BarChart(QWidget):
    def __init__(self, data: dict, color="#00D4FF", parent=None):
        super().__init__(parent)
        self.data = data
        self.color = QColor(color)
        self.setMinimumHeight(120)

    def paintEvent(self, e):
        if not self.data:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        vals = list(self.data.values())
        keys = list(self.data.keys())
        mx = max(vals) if max(vals) > 0 else 1
        n = len(vals)
        pad = 10
        bar_w = (w - 2 * pad) / n if n > 0 else 1
        p.setPen(Qt.PenStyle.NoPen)
        for i, (k, v) in enumerate(zip(keys, vals)):
            x0 = int(pad + i * bar_w + bar_w * 0.1)
            x1 = int(pad + i * bar_w + bar_w * 0.9)
            bh = int((v / mx) * (h - 30))
            y0 = h - 20 - bh
            grad = QLinearGradient(x0, y0, x0, h - 20)
            grad.setColorAt(0, self.color)
            grad.setColorAt(1, self.color.darker(150))
            p.setBrush(QBrush(grad))
            p.drawRoundedRect(x0, y0, x1 - x0, bh, 3, 3)
            p.setPen(QColor(SM.t("text_dim")))
            p.setFont(QFont("Courier New", 7))
            p.drawText(x0, h - 5, k[:6])
            if bh > 14:
                p.setPen(QColor("white"))
                p.drawText(x0, y0 + 12, f"{v:.0f}")
            p.setPen(Qt.PenStyle.NoPen)
        p.end()


class DonutChart(QWidget):
    COLORS = ["#00D4FF","#7B2FFF","#00E676","#FFD600","#FF1744",
              "#FF6D00","#40C4FF","#EA80FC","#B9F6CA","#FFD180"]

    def __init__(self, data: dict, size=160, parent=None):
        super().__init__(parent)
        self.data = data
        self.setFixedSize(size, size)

    def paintEvent(self, e):
        if not self.data or sum(self.data.values()) == 0:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        size = min(self.width(), self.height())
        cx, cy = self.width() / 2, self.height() / 2
        r_out = size / 2 - 8
        r_in = r_out * 0.55
        total = sum(self.data.values())
        start = -90 * 16
        for i, (k, v) in enumerate(self.data.items()):
            if v <= 0:
                continue
            span = int((v / total) * 360 * 16)
            color = QColor(self.COLORS[i % len(self.COLORS)])
            p.setBrush(QBrush(color))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawPie(int(cx - r_out), int(cy - r_out),
                      int(2 * r_out), int(2 * r_out), start, span)
            start += span
        # Hollow center
        p.setBrush(QBrush(QColor(SM.t("card"))))
        p.drawEllipse(int(cx - r_in), int(cy - r_in), int(2 * r_in), int(2 * r_in))
        p.setPen(QColor(SM.t("text")))
        p.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        p.drawText(int(cx - 30), int(cy + 5), f"{total:.0f}")
        p.end()

# ═══════════════════════════════════════════════════════════════
#  GİRİŞ / KAYIT SAYFASI
# ═══════════════════════════════════════════════════════════════
class AuthPage(QWidget):
    login_success = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setSpacing(0)
        main.setContentsMargins(40, 40, 40, 40)

        # Sol panel
        left = CardFrame()
        left.setMinimumWidth(480)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(36, 36, 36, 36)
        ll.setSpacing(10)

        accent_bar = QFrame()
        accent_bar.setFixedHeight(4)
        accent_bar.setStyleSheet(f"background: {SM.t('accent')}; border-radius: 2px;")
        ll.addWidget(accent_bar)

        title = QLabel("3D BASKI\nATÖLYE PRO")
        title.setFont(QFont("Courier New", 36, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        ll.addWidget(title)

        sub = QLabel("Profesyonel 3D baskı atölye yönetim sistemi\nv4.0 PyQt6 Edition  ·  65+ Özellik")
        sub.setStyleSheet(f"color: {SM.t('text_dim')}; font-size: 14px; border: none;")
        ll.addWidget(sub)
        ll.addSpacing(10)

        badges_layout = QHBoxLayout()
        for txt, col in [("● Stok", SM.t("accent")), ("● Satış", SM.t("success")),
                          ("● CRM", SM.t("accent2")), ("● Finans", SM.t("warning"))]:
            b = QLabel(txt)
            b.setStyleSheet(f"color: {col}; font-weight: bold; border: none;")
            badges_layout.addWidget(b)
        badges_layout.addStretch()
        ll.addLayout(badges_layout)
        ll.addSpacing(10)

        features = [
            "📦  Filament & sarf malzeme stok takibi",
            "💰  Satış, KDV, indirim & fatura sistemi",
            "📈  Gelir/gider/kar grafikler",
            "👥  Müşteri CRM & sadakat puanı",
            "🖨️  Çoklu yazıcı & bakım takvimi",
            "📅  Takvim, randevu & görev sistemi",
            "📊  İstatistik, rapor & PDF export",
            "🎨  8 tema seçeneği ile tam özelleştirme",
            "🔧  Kanban üretim hattı görünümü",
            "💾  Otomatik yedekleme sistemi",
            "⚡  Fatura & kargo fiyat hesaplama",
            "🏆  En çok satan ürün & müşteri analizi",
        ]
        for f in features:
            lbl = QLabel(f)
            lbl.setStyleSheet(f"color: {SM.t('text')}; font-size: 13px; border: none;")
            ll.addWidget(lbl)

        ll.addStretch()
        ver = QLabel("v4.0 PRO  ·  PyQt6  ·  2025  ·  Yağız BAYRAKTAR")
        ver.setStyleSheet(f"color: {SM.t('border')}; font-size: 11px; border: none;")
        ll.addWidget(ver)

        main.addWidget(left)
        main.addSpacing(24)

        # Sağ panel
        right = CardFrame()
        right.setFixedWidth(420)
        rl = QVBoxLayout(right)
        rl.setContentsMargins(32, 32, 32, 32)
        rl.setSpacing(0)

        tabs = QTabWidget()
        tabs.setMinimumHeight(480)

        # Giriş
        login_w = QWidget()
        login_l = QVBoxLayout(login_w)
        login_l.setSpacing(10)
        login_l.setContentsMargins(10, 20, 10, 10)

        lbl_hw = QLabel("HOŞ GELDİN 👋")
        lbl_hw.setFont(QFont("Courier New", 22, QFont.Weight.Bold))
        lbl_hw.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        lbl_hw.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_l.addWidget(lbl_hw)

        sub2 = QLabel("Hesabına giriş yap")
        sub2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub2.setStyleSheet(f"color: {SM.t('text_dim')}; border: none;")
        login_l.addWidget(sub2)
        login_l.addSpacing(16)

        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("👤 Kullanıcı adı")
        self.login_user.setMinimumHeight(44)

        self.login_pass = QLineEdit()
        self.login_pass.setPlaceholderText("🔒 Şifre")
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_pass.setMinimumHeight(44)
        self.login_pass.returnPressed.connect(self._do_login)

        login_btn = StyledButton("  GİRİŞ YAP  →")
        login_btn.setMinimumHeight(48)
        login_btn.clicked.connect(self._do_login)

        self.login_info = QLabel("")
        self.login_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")

        # Demo giriş butonu
        demo_btn = StyledButton("🎮 Demo ile Dene", "flat")
        demo_btn.clicked.connect(self._demo_login)

        login_l.addWidget(self.login_user)
        login_l.addWidget(self.login_pass)
        login_l.addWidget(login_btn)
        login_l.addWidget(self.login_info)
        login_l.addSpacing(8)
        login_l.addWidget(demo_btn)
        login_l.addStretch()

        # Kayıt
        reg_w = QWidget()
        reg_l = QVBoxLayout(reg_w)
        reg_l.setSpacing(10)
        reg_l.setContentsMargins(10, 20, 10, 10)

        lbl_reg = QLabel("HESAP OLUŞTUR")
        lbl_reg.setFont(QFont("Courier New", 20, QFont.Weight.Bold))
        lbl_reg.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        lbl_reg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        reg_l.addWidget(lbl_reg)

        sub3 = QLabel("Ücretsiz kayıt ol")
        sub3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub3.setStyleSheet(f"color: {SM.t('text_dim')}; border: none;")
        reg_l.addWidget(sub3)
        reg_l.addSpacing(16)

        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("👤 Kullanıcı adı (min. 3 karakter)")
        self.reg_user.setMinimumHeight(44)

        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("📧 E-posta (opsiyonel)")
        self.reg_email.setMinimumHeight(44)

        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("🔒 Şifre (min. 4 karakter)")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass.setMinimumHeight(44)

        self.reg_pass2 = QLineEdit()
        self.reg_pass2.setPlaceholderText("🔒 Şifre tekrar")
        self.reg_pass2.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass2.setMinimumHeight(44)

        reg_btn = StyledButton("  KAYIT OL  →", "success")
        reg_btn.setMinimumHeight(48)
        reg_btn.clicked.connect(self._do_register)

        self.reg_info = QLabel("")
        self.reg_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reg_info.setWordWrap(True)
        self.reg_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")

        for w in [self.reg_user, self.reg_email, self.reg_pass, self.reg_pass2, reg_btn, self.reg_info]:
            reg_l.addWidget(w)
        reg_l.addStretch()

        tabs.addTab(login_w, "  Giriş Yap  ")
        tabs.addTab(reg_w,   "  Kayıt Ol  ")
        rl.addWidget(tabs)

        main.addWidget(right)

    def _do_login(self):
        u = self.login_user.text().strip()
        p = self.login_pass.text().strip()
        users = load_users()
        ph = hash_password(p)
        for user in users:
            if user["username"] == u and (user.get("password_hash") == ph or user.get("password") == p):
                log_activity(u, "GİRİŞ")
                self.login_success.emit(u)
                return
        self.login_info.setText("✗  Kullanıcı adı veya şifre hatalı.")

    def _demo_login(self):
        users = load_users()
        if not any(u["username"] == "demo" for u in users):
            users.append({
                "username": "demo",
                "password_hash": hash_password("demo"),
                "email": "demo@atolye.pro",
                "role": "admin",
                "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
            })
            save_users(users)
        log_activity("demo", "DEMO GİRİŞ")
        self.login_success.emit("demo")

    def _do_register(self):
        u  = self.reg_user.text().strip()
        e  = self.reg_email.text().strip()
        p  = self.reg_pass.text().strip()
        p2 = self.reg_pass2.text().strip()
        if len(u) < 3:
            self.reg_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.reg_info.setText("✗  En az 3 karakter gerekli."); return
        if len(p) < 4:
            self.reg_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.reg_info.setText("✗  En az 4 karakterli şifre."); return
        if p != p2:
            self.reg_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.reg_info.setText("✗  Şifreler eşleşmiyor."); return
        users = load_users()
        if any(x["username"] == u for x in users):
            self.reg_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.reg_info.setText("✗  Bu kullanıcı adı alınmış."); return
        users.append({
            "username": u, "email": e,
            "password_hash": hash_password(p),
            "role": "admin",
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        save_users(users)
        self.reg_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        self.reg_info.setText("✓  Kayıt başarılı! Giriş yapabilirsin.")

# ═══════════════════════════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════════════════════════
class DashboardPage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        self.cl = QVBoxLayout(content)
        self.cl.setContentsMargins(20, 16, 20, 20)
        self.cl.setSpacing(12)
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def _refresh(self):
        while self.cl.count():
            item = self.cl.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        projects  = u_load(PROJECTS_FILE, self.user)
        sales     = u_load(SALES_FILE, self.user)
        expenses  = u_load(EXPENSES_FILE, self.user)
        customers = u_load(CUSTOMERS_FILE, self.user)
        stock     = load_json(STOCK_FILE, {})
        settings  = get_settings()
        threshold = settings.get("low_stock_threshold", 500)

        t_mal   = sum(p.get("toplam_maliyet", 0) for p in projects)
        t_satis = sum(s.get("satis_fiyati", 0) for s in sales)
        t_gider = sum(e.get("tutar", 0) for e in expenses)
        net_kar = t_satis - t_mal - t_gider
        t_stok  = sum(stock.values())
        dusuk   = sum(1 for v in stock.values() if 0 < v < threshold)
        tasks   = u_load(TASKS_FILE, self.user)
        bekleyen_task = sum(1 for t in tasks if t.get("durum") != "✅ Tamamlandı")

        # KPI Row 1
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        for icon, label, val, col in [
            ("📋", "Proje", str(len(projects)), SM.t("text")),
            ("💸", "Toplam Maliyet", f"{t_mal:,.2f} TL", SM.t("text_dim")),
            ("🛒", "Toplam Satış", f"{t_satis:,.2f} TL", SM.t("success")),
            ("✅", "Net Kar", f"{net_kar:,.2f} TL", SM.t("success") if net_kar >= 0 else SM.t("danger")),
            ("📤", "Giderler", f"{t_gider:,.2f} TL", SM.t("danger")),
        ]:
            card = KPICard(icon, label, val, col)
            row1.addWidget(card)
        self.cl.addLayout(row1)

        # KPI Row 2
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        for icon, label, val, col in [
            ("📦", "Toplam Stok", f"{t_stok:,.0f} g", SM.t("accent")),
            ("⚠️", "Düşük Stok", f"{dusuk} ürün", SM.t("warning") if dusuk else SM.t("success")),
            ("👥", "Müşteri", str(len(customers)), SM.t("accent2")),
            ("🛍️", "Satış Adedi", str(len(sales)), SM.t("text")),
            ("✅", "Bekleyen Görev", str(bekleyen_task), SM.t("warning") if bekleyen_task else SM.t("success")),
        ]:
            card = KPICard(icon, label, val, col)
            row2.addWidget(card)
        self.cl.addLayout(row2)

        # Grafikler
        chart_row = QHBoxLayout()
        chart_row.setSpacing(8)

        # Filament kullanım bar
        fil_card = CardFrame()
        fil_l = QVBoxLayout(fil_card)
        fil_l.setContentsMargins(16, 12, 16, 12)
        hdr = QLabel("🧵 Filament Kullanımı")
        hdr.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        hdr.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        fil_l.addWidget(hdr)
        fil_use = {}
        for p in projects:
            f = p.get("filament_turu", "PLA")
            fil_use[f] = fil_use.get(f, 0) + p.get("gram", 0)
        if fil_use:
            bc = BarChart(fil_use, SM.t("accent"))
            bc.setMinimumHeight(120)
            fil_l.addWidget(bc)
        else:
            fil_l.addWidget(QLabel("Henüz veri yok."))

        # Satış donut
        donut_card = CardFrame()
        donut_card.setFixedWidth(200)
        donut_l = QVBoxLayout(donut_card)
        donut_l.setContentsMargins(16, 12, 16, 12)
        dh = QLabel("📊 Ödeme Dağılımı")
        dh.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        dh.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        donut_l.addWidget(dh)
        pay_data = {}
        for s in sales:
            pm = s.get("odeme", "Nakit")
            pay_data[pm] = pay_data.get(pm, 0) + 1
        if pay_data:
            dc = DonutChart(pay_data, 160)
            dc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            donut_l.addWidget(dc)
        else:
            donut_l.addWidget(QLabel("Satış yok."))

        chart_row.addWidget(fil_card, stretch=2)
        chart_row.addWidget(donut_card)
        self.cl.addLayout(chart_row)

        # Bu ay özeti
        now = datetime.now()
        this_m = f"{now.month:02d}.{now.year}"
        def in_m(x):
            try: return x.get("tarih","")[3:10] == this_m
            except: return False

        m_sal = [s for s in sales if in_m(s)]
        m_exp = [e for e in expenses if in_m(e)]
        m_prj = [p for p in projects if in_m(p)]

        month_header = SectionHeader(f"📅 {now.strftime('%B %Y')} Özeti")
        self.cl.addWidget(month_header)

        month_row = QHBoxLayout()
        month_row.setSpacing(8)
        for icon, label, val, col in [
            ("📋", "Yeni Proje", str(len(m_prj)), SM.t("accent")),
            ("💰", "Satış Geliri", f"{sum(s.get('satis_fiyati',0) for s in m_sal):,.2f} TL", SM.t("success")),
            ("📤", "Giderler", f"{sum(e.get('tutar',0) for e in m_exp):,.2f} TL", SM.t("danger")),
            ("🛍️", "Satış Adedi", str(len(m_sal)), SM.t("text")),
        ]:
            card = KPICard(icon, label, val, col)
            month_row.addWidget(card)
        self.cl.addLayout(month_row)

        # Hızlı notlar & düşük stok uyarısı
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(8)

        # Düşük stok uyarıları
        alert_card = CardFrame()
        alert_l = QVBoxLayout(alert_card)
        alert_l.setContentsMargins(16, 12, 16, 12)
        ah = QLabel("⚠️ Stok Uyarıları")
        ah.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        ah.setStyleSheet(f"color: {SM.t('warning')}; border: none;")
        alert_l.addWidget(ah)
        low_items = [(k, v) for k, v in stock.items() if 0 < v < threshold]
        if low_items:
            for k, v in low_items[:8]:
                lbl = QLabel(f"⚠️ {k}: {v:.0f} g")
                lbl.setStyleSheet(f"color: {SM.t('warning')}; border: none;")
                alert_l.addWidget(lbl)
        else:
            ok_lbl = QLabel("✅ Tüm stoklar yeterli.")
            ok_lbl.setStyleSheet(f"color: {SM.t('success')}; border: none;")
            alert_l.addWidget(ok_lbl)

        # Son satışlar
        recent_card = CardFrame()
        recent_l = QVBoxLayout(recent_card)
        recent_l.setContentsMargins(16, 12, 16, 12)
        rh = QLabel("💰 Son Satışlar")
        rh.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        rh.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        recent_l.addWidget(rh)
        for s in list(reversed(sales))[:6]:
            sl = QLabel(f"• {s.get('urun','–')} → {s.get('satis_fiyati',0):.2f} TL  ({s.get('tarih','')[:10]})")
            sl.setStyleSheet(f"color: {SM.t('text')}; font-size: 12px; border: none;")
            recent_l.addWidget(sl)

        bottom_row.addWidget(alert_card)
        bottom_row.addWidget(recent_card)
        self.cl.addLayout(bottom_row)
        self.cl.addStretch()

    def refresh(self):
        self._refresh()

# ═══════════════════════════════════════════════════════════════
#  PROJELER / DASHBOARD HESAP
# ═══════════════════════════════════════════════════════════════
class ProjectsPage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(12)

        # Sol: form
        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_scroll.setFrameShape(QFrame.Shape.NoFrame)
        form_scroll.setFixedWidth(390)

        form_widget = QWidget()
        fl = QVBoxLayout(form_widget)
        fl.setContentsMargins(0, 0, 8, 0)
        fl.setSpacing(8)
        form_scroll.setWidget(form_widget)

        form_card = CardFrame()
        fc = QVBoxLayout(form_card)
        fc.setContentsMargins(20, 16, 20, 16)
        fc.setSpacing(8)

        title = QLabel("➕  YENİ PROJE")
        title.setFont(QFont("Courier New", 15, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        fc.addWidget(title)

        self.e_model   = QLineEdit(); self.e_model.setPlaceholderText("Model adı *"); self.e_model.setMinimumHeight(38)
        self.e_cat     = QLineEdit(); self.e_cat.setPlaceholderText("Kategori *"); self.e_cat.setMinimumHeight(38)
        self.e_color   = QLineEdit(); self.e_color.setPlaceholderText("Renk *"); self.e_color.setMinimumHeight(38)
        self.e_gram    = QLineEdit(); self.e_gram.setPlaceholderText("Gram *"); self.e_gram.setMinimumHeight(38)
        self.e_hours   = QLineEdit(); self.e_hours.setPlaceholderText("Baskı süresi (saat)"); self.e_hours.setText("0"); self.e_hours.setMinimumHeight(38)
        self.e_note    = QLineEdit(); self.e_note.setPlaceholderText("Not"); self.e_note.setMinimumHeight(38)
        self.e_infill  = QLineEdit(); self.e_infill.setPlaceholderText("Dolgu % (örn: 20)"); self.e_infill.setText("20"); self.e_infill.setMinimumHeight(38)
        self.e_layer   = QLineEdit(); self.e_layer.setPlaceholderText("Katman kalınlığı mm"); self.e_layer.setText("0.2"); self.e_layer.setMinimumHeight(38)
        self.e_support = QLineEdit(); self.e_support.setPlaceholderText("Destek gram (0=yok)"); self.e_support.setText("0"); self.e_support.setMinimumHeight(38)
        self.e_postpro = QLineEdit(); self.e_postpro.setPlaceholderText("Post-process maliyet TL"); self.e_postpro.setText("0"); self.e_postpro.setMinimumHeight(38)

        for w in [self.e_model, self.e_cat, self.e_color, self.e_gram, self.e_hours,
                  self.e_note, self.e_infill, self.e_layer, self.e_support, self.e_postpro]:
            fc.addWidget(w)

        fc.addWidget(self._label("Filament Türü"))
        self.cb_filament = QComboBox(); self.cb_filament.setMinimumHeight(38)
        self.cb_filament.addItems(sorted(FILAMENT_DATA.keys()))
        fc.addWidget(self.cb_filament)

        fc.addWidget(self._label("Yazıcı Markası"))
        self.cb_brand = QComboBox(); self.cb_brand.setMinimumHeight(38)
        self.cb_brand.addItems(sorted(PRINTER_DATA.keys()))
        self.cb_brand.currentTextChanged.connect(self._update_model_combo)
        fc.addWidget(self.cb_brand)

        fc.addWidget(self._label("Yazıcı Modeli"))
        self.cb_model_p = QComboBox(); self.cb_model_p.setMinimumHeight(38)
        fc.addWidget(self.cb_model_p)
        self._update_model_combo("Bambu Lab")

        fc.addWidget(self._label("Proje Durumu"))
        self.cb_status = QComboBox(); self.cb_status.setMinimumHeight(38)
        self.cb_status.addItems(["⏳ Hazırlanıyor", "🔄 Basılıyor", "✅ Tamamlandı", "❌ İptal", "📦 Teslim Edildi"])
        fc.addWidget(self.cb_status)

        fc.addWidget(self._label("Öncelik"))
        self.cb_priority = QComboBox(); self.cb_priority.setMinimumHeight(38)
        self.cb_priority.addItems(["🟢 Normal", "🟡 Yüksek", "🔴 Acil"])
        fc.addWidget(self.cb_priority)

        fc.addWidget(self._label("Etiket"))
        self.cb_tag = QComboBox(); self.cb_tag.setMinimumHeight(38)
        self.cb_tag.addItems(["Genel","Oyuncak","Endüstriyel","Ev Dekor","Prototip","Sanat","Yedek Parça","Diğer"])
        fc.addWidget(self.cb_tag)

        # Kar marjı
        fc.addWidget(self._label("Kar Marjı Hesapla"))
        marj_row = QHBoxLayout()
        self.cb_marj = QComboBox(); self.cb_marj.setMinimumHeight(38)
        self.cb_marj.addItems(["Düşük (%20)", "Normal (%40)", "Yüksek (%60)", "Premium (%80)", "Özel (%)"])
        marj_row.addWidget(self.cb_marj)
        calc_btn = StyledButton("⚡ Hesapla", "warning")
        calc_btn.clicked.connect(self._calc_price)
        marj_row.addWidget(calc_btn)
        fc.addLayout(marj_row)

        self.lbl_calc = QLabel("")
        self.lbl_calc.setStyleSheet(f"color: {SM.t('warning')}; font-weight: bold; border: none;")
        self.lbl_calc.setWordWrap(True)
        fc.addWidget(self.lbl_calc)

        btn_row = QHBoxLayout()
        save_btn  = StyledButton("💾 Kaydet")
        save_btn.clicked.connect(self._add_project)
        tmpl_btn = StyledButton("📋 Şablon Kaydet", "flat")
        tmpl_btn.clicked.connect(self._save_template)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(tmpl_btn)
        fc.addLayout(btn_row)

        self.info_lbl = QLabel("")
        self.info_lbl.setWordWrap(True)
        self.info_lbl.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        fc.addWidget(self.info_lbl)

        form_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        fl.addWidget(form_card)
        fl.addStretch()
        main.addWidget(form_scroll)

        # Sağ: liste
        right_panel = QWidget()
        rl = QVBoxLayout(right_panel)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(8)

        # Araç bar
        tool_bar = QHBoxLayout()
        tool_bar.setSpacing(6)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Ara (model, kategori, filament...)")
        self.search_input.setMinimumHeight(38)
        self.search_input.textChanged.connect(self._filter_table)

        self.cb_filter_status = QComboBox(); self.cb_filter_status.setMinimumHeight(38)
        self.cb_filter_status.addItems(["Tümü","⏳ Hazırlanıyor","🔄 Basılıyor","✅ Tamamlandı","❌ İptal"])
        self.cb_filter_status.currentTextChanged.connect(self._filter_table)

        self.cb_sort = QComboBox(); self.cb_sort.setMinimumHeight(38)
        self.cb_sort.addItems(["Tarihe Göre (Yeni)","Tarihe Göre (Eski)","Maliyete Göre","Grama Göre"])
        self.cb_sort.currentTextChanged.connect(self._filter_table)

        tool_bar.addWidget(self.search_input, stretch=2)
        tool_bar.addWidget(self.cb_filter_status)
        tool_bar.addWidget(self.cb_sort)
        rl.addLayout(tool_bar)

        # Buton bar
        btn_bar = QHBoxLayout()
        btn_bar.setSpacing(6)
        for text, func, style in [
            ("📋 Forma Yükle", self._load_to_form, "flat"),
            ("✏️ Güncelle",    self._update_project, "success"),
            ("📄 Kopyala",     self._copy_project, "flat"),
            ("🗑 Sil",         self._del_project, "danger"),
            ("📥 CSV",         self._export_csv, "flat"),
            ("🔃 Yenile",      self._refresh_list, "flat"),
        ]:
            btn = StyledButton(text, style)
            btn.setMinimumHeight(36)
            btn.clicked.connect(func)
            btn_bar.addWidget(btn)
        rl.addLayout(btn_bar)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "#", "Model", "Kategori", "Filament", "Gram", "Süre (h)",
            "F.Maliyet", "E.Maliyet", "TOPLAM", "Durum", "Öncelik", "Tarih"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setMinimumHeight(400)
        rl.addWidget(self.table)

        # Seçili no
        sel_row = QHBoxLayout()
        self.sel_input = QLineEdit()
        self.sel_input.setPlaceholderText("İşlem yapılacak proje no (tablo sırası)")
        self.sel_input.setMinimumHeight(36)
        sel_row.addWidget(self.sel_input)
        rl.addLayout(sel_row)

        main.addWidget(right_panel)
        self.all_projects = []

    def _label(self, txt):
        l = QLabel(txt)
        l.setStyleSheet(f"color: {SM.t('text_dim')}; font-size: 12px; border: none;")
        return l

    def _update_model_combo(self, brand=None):
        brand = brand or self.cb_brand.currentText()
        models = list(PRINTER_DATA.get(brand, {}).keys())
        self.cb_model_p.clear()
        self.cb_model_p.addItems(models or ["Model Yok"])

    def _calc_price(self):
        try:
            gram = float(self.e_gram.text().replace(",",".") or "0")
            hrs  = float(self.e_hours.text().replace(",",".") or "0")
            fil  = self.cb_filament.currentText()
            brand = self.cb_brand.currentText()
            model = self.cb_model_p.currentText()
            total, fmal, emal, watt, etuk = calc_cost(gram, fil, hrs, brand, model)

            support = float(self.e_support.text().replace(",",".") or "0")
            postpro = float(self.e_postpro.text().replace(",",".") or "0")
            total_full = total + postpro

            marj_map = {"Düşük (%20)": 0.20, "Normal (%40)": 0.40,
                        "Yüksek (%60)": 0.60, "Premium (%80)": 0.80}
            marj_key = self.cb_marj.currentText()
            marj = marj_map.get(marj_key, 0.40)
            oneri = round(total_full * (1 + marj), 2)
            kdv_r = get_settings().get("kdv_rate", 20)
            kdvli = round(oneri * (1 + kdv_r / 100), 2)
            self.lbl_calc.setText(
                f"Filament: {fmal:.2f} TL  +  Elektrik: {emal:.2f} TL\n"
                f"Post-process: {postpro:.2f} TL  →  Maliyet: {total_full:.2f} TL\n"
                f"Önerilen Satış: {oneri:.2f} TL  |  KDV'li: {kdvli:.2f} TL"
            )
        except Exception as ex:
            self.lbl_calc.setText(f"Hata: {ex}")

    def _add_project(self):
        try:
            model = self.e_model.text().strip()
            kat   = self.e_cat.text().strip()
            renk  = self.e_color.text().strip()
            gram  = float(self.e_gram.text().replace(",","."))
            hrs   = float(self.e_hours.text().replace(",",".") or "0")
            fil   = self.cb_filament.currentText()
            brand = self.cb_brand.currentText()
            model_p = self.cb_model_p.currentText()
            durum = self.cb_status.currentText()
            onc   = self.cb_priority.currentText()
            tag   = self.cb_tag.currentText()
            note  = self.e_note.text().strip()
            infill = float(self.e_infill.text().replace(",",".") or "20")
            layer  = float(self.e_layer.text().replace(",",".") or "0.2")
            support = float(self.e_support.text().replace(",",".") or "0")
            postpro = float(self.e_postpro.text().replace(",",".") or "0")

            if not model or not kat or not renk:
                self.info_lbl.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
                self.info_lbl.setText("✗ Model, kategori ve renk zorunlu."); return

            # Stok kontrolü
            stock = load_json(STOCK_FILE, {})
            toplam_gram = gram + support
            if stock.get(fil, 0) < toplam_gram:
                self.info_lbl.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
                self.info_lbl.setText(f"✗ Yeterli {fil} yok! Mevcut: {stock.get(fil,0):.0f} g"); return

            stock[fil] = stock.get(fil, 0) - toplam_gram
            save_json(STOCK_FILE, stock)

            total, fmal, emal, watt, etuk = calc_cost(gram, fil, hrs, brand, model_p)
            total_full = total + postpro

            prj = {
                "owner": self.user, "model_adi": model.title(),
                "kategori": kat.title(), "filament_turu": fil,
                "yazici_marka": brand, "yazici_model": model_p,
                "watt": watt, "renk": renk.title(), "gram": gram,
                "destek_gram": support, "sure": hrs,
                "dolgu": infill, "katman": layer,
                "filament_maliyet": fmal, "elektrik_maliyet": emal,
                "post_process": postpro, "toplam_maliyet": total_full,
                "durum": durum, "oncelik": onc, "etiket": tag,
                "not": note, "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "favori": False,
            }
            projects = u_load(PROJECTS_FILE, self.user)
            projects.append(prj)
            u_save(PROJECTS_FILE, self.user, projects)
            log_activity(self.user, "PROJE EKLENDİ", model)
            self.info_lbl.setStyleSheet(f"color: {SM.t('success')}; border: none;")
            self.info_lbl.setText(f"✓ {model.title()} eklendi. Toplam: {total_full:.2f} TL")
            self._clear_form()
            self._refresh_list()
        except ValueError as ex:
            self.info_lbl.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.info_lbl.setText(f"✗ Sayısal değer hatası: {ex}")

    def _clear_form(self):
        for e in [self.e_model, self.e_cat, self.e_color, self.e_gram, self.e_note]:
            e.clear()
        self.e_hours.setText("0"); self.e_infill.setText("20")
        self.e_layer.setText("0.2"); self.e_support.setText("0"); self.e_postpro.setText("0")

    def _save_template(self):
        name, ok = QInputDialog.getText(self, "Şablon Adı", "Şablon adını gir:")
        if not ok or not name.strip(): return
        templates = load_json(TEMPLATES_FILE, [])
        templates.append({
            "isim": name.strip(), "owner": self.user,
            "filament": self.cb_filament.currentText(),
            "brand": self.cb_brand.currentText(),
            "model": self.cb_model_p.currentText(),
            "infill": self.e_infill.text(),
            "layer": self.e_layer.text(),
            "durum": self.cb_status.currentText(),
            "tarih": datetime.now().strftime("%d.%m.%Y"),
        })
        save_json(TEMPLATES_FILE, templates)
        QMessageBox.information(self, "Şablon", f"'{name}' şablonu kaydedildi.")

    def _refresh_list(self):
        self.all_projects = u_load(PROJECTS_FILE, self.user)
        self._filter_table()

    def _filter_table(self):
        kw = self.search_input.text().strip().lower()
        sf = self.cb_filter_status.currentText()
        so = self.cb_sort.currentText()

        filtered = self.all_projects
        if kw:
            filtered = [p for p in filtered if kw in f"{p.get('model_adi','')} {p.get('kategori','')} {p.get('filament_turu','')} {p.get('etiket','')}".lower()]
        if sf != "Tümü":
            filtered = [p for p in filtered if p.get("durum","") == sf]

        if so == "Tarihe Göre (Yeni)":
            filtered = sorted(filtered, key=lambda x: x.get("tarih",""), reverse=True)
        elif so == "Tarihe Göre (Eski)":
            filtered = sorted(filtered, key=lambda x: x.get("tarih",""))
        elif so == "Maliyete Göre":
            filtered = sorted(filtered, key=lambda x: x.get("toplam_maliyet",0), reverse=True)
        elif so == "Grama Göre":
            filtered = sorted(filtered, key=lambda x: x.get("gram",0), reverse=True)

        self.table.setRowCount(len(filtered))
        for i, p in enumerate(filtered):
            row_data = [
                str(i+1), p.get("model_adi",""), p.get("kategori",""),
                p.get("filament_turu",""), f"{p.get('gram',0):.0f}",
                f"{p.get('sure',0):.1f}",
                f"{p.get('filament_maliyet',0):.2f} TL",
                f"{p.get('elektrik_maliyet',0):.2f} TL",
                f"{p.get('toplam_maliyet',0):.2f} TL",
                p.get("durum",""), p.get("oncelik",""), p.get("tarih","")[:10],
            ]
            for j, val in enumerate(row_data):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                # Renk kodlama
                durum = p.get("durum","")
                if "Tamamlandı" in durum:
                    item.setForeground(QColor(SM.t("success")))
                elif "İptal" in durum:
                    item.setForeground(QColor(SM.t("danger")))
                elif "Basılıyor" in durum:
                    item.setForeground(QColor(SM.t("warning")))
                self.table.setItem(i, j, item)
        self.displayed_projects = filtered

    def _get_selected_idx(self):
        rows = self.table.selectedItems()
        if rows:
            row = self.table.row(rows[0])
            return row
        try:
            return int(self.sel_input.text().strip()) - 1
        except:
            return -1

    def _load_to_form(self):
        idx = self._get_selected_idx()
        if idx < 0 or idx >= len(self.displayed_projects):
            QMessageBox.warning(self, "Hata", "Geçerli bir proje seçin."); return
        p = self.displayed_projects[idx]
        self.e_model.setText(p.get("model_adi",""))
        self.e_cat.setText(p.get("kategori",""))
        self.e_color.setText(p.get("renk",""))
        self.e_gram.setText(str(p.get("gram","")))
        self.e_hours.setText(str(p.get("sure","0")))
        self.e_note.setText(p.get("not",""))
        self.e_infill.setText(str(p.get("dolgu","20")))
        self.e_layer.setText(str(p.get("katman","0.2")))
        self.e_support.setText(str(p.get("destek_gram","0")))
        self.e_postpro.setText(str(p.get("post_process","0")))
        # Combolar
        idx_f = self.cb_filament.findText(p.get("filament_turu",""))
        if idx_f >= 0: self.cb_filament.setCurrentIndex(idx_f)
        idx_b = self.cb_brand.findText(p.get("yazici_marka",""))
        if idx_b >= 0: self.cb_brand.setCurrentIndex(idx_b)
        self._update_model_combo(p.get("yazici_marka",""))
        idx_m = self.cb_model_p.findText(p.get("yazici_model",""))
        if idx_m >= 0: self.cb_model_p.setCurrentIndex(idx_m)
        idx_s = self.cb_status.findText(p.get("durum",""))
        if idx_s >= 0: self.cb_status.setCurrentIndex(idx_s)
        self.info_lbl.setText("✓ Proje forma yüklendi.")

    def _update_project(self):
        idx = self._get_selected_idx()
        if idx < 0 or idx >= len(self.displayed_projects):
            QMessageBox.warning(self, "Hata", "Geçerli bir proje seçin."); return
        target = self.displayed_projects[idx]
        all_p = u_load(PROJECTS_FILE, self.user)
        real_idx = next((i for i, p in enumerate(all_p) if p.get("tarih") == target.get("tarih") and p.get("model_adi") == target.get("model_adi")), -1)
        if real_idx < 0:
            QMessageBox.warning(self, "Hata", "Proje bulunamadı."); return
        # Stok iade
        stock = load_json(STOCK_FILE, {})
        old_fil = all_p[real_idx].get("filament_turu","")
        old_gram = all_p[real_idx].get("gram",0) + all_p[real_idx].get("destek_gram",0)
        stock[old_fil] = stock.get(old_fil,0) + old_gram
        # Yeni değerler
        try:
            gram = float(self.e_gram.text().replace(",",".") or str(all_p[real_idx].get("gram",0)))
            hrs  = float(self.e_hours.text().replace(",",".") or "0")
            fil  = self.cb_filament.currentText()
            brand= self.cb_brand.currentText()
            model_p = self.cb_model_p.currentText()
            support = float(self.e_support.text().replace(",",".") or "0")
            postpro = float(self.e_postpro.text().replace(",",".") or "0")

            toplam_gram = gram + support
            if stock.get(fil,0) < toplam_gram:
                QMessageBox.warning(self, "Stok", f"Yeterli {fil} yok!"); return
            stock[fil] = stock.get(fil,0) - toplam_gram
            save_json(STOCK_FILE, stock)

            total, fmal, emal, watt, etuk = calc_cost(gram, fil, hrs, brand, model_p)
            all_p[real_idx].update({
                "model_adi": self.e_model.text().strip().title() or all_p[real_idx]["model_adi"],
                "kategori": self.e_cat.text().strip().title() or all_p[real_idx]["kategori"],
                "renk": self.e_color.text().strip().title() or all_p[real_idx]["renk"],
                "gram": gram, "sure": hrs, "filament_turu": fil,
                "yazici_marka": brand, "yazici_model": model_p,
                "destek_gram": support, "post_process": postpro,
                "filament_maliyet": fmal, "elektrik_maliyet": emal,
                "toplam_maliyet": total + postpro, "watt": watt,
                "durum": self.cb_status.currentText(),
                "oncelik": self.cb_priority.currentText(),
                "not": self.e_note.text().strip(),
                "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
            })
            u_save(PROJECTS_FILE, self.user, all_p)
            log_activity(self.user, "PROJE GÜNCELLENDİ", all_p[real_idx]["model_adi"])
            self._refresh_list()
            QMessageBox.information(self, "Başarılı", "Proje güncellendi.")
        except ValueError as ex:
            QMessageBox.warning(self, "Hata", str(ex))

    def _copy_project(self):
        idx = self._get_selected_idx()
        if idx < 0 or idx >= len(self.displayed_projects): return
        p = dict(self.displayed_projects[idx])
        p["model_adi"] = p.get("model_adi","") + " (Kopya)"
        p["tarih"] = datetime.now().strftime("%d.%m.%Y %H:%M")
        all_p = u_load(PROJECTS_FILE, self.user)
        all_p.append(p)
        u_save(PROJECTS_FILE, self.user, all_p)
        self._refresh_list()

    def _del_project(self):
        idx = self._get_selected_idx()
        if idx < 0 or idx >= len(self.displayed_projects): return
        target = self.displayed_projects[idx]
        if QMessageBox.question(self, "Onay", f"'{target.get('model_adi','')}' silinsin mi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes: return
        all_p = u_load(PROJECTS_FILE, self.user)
        real_idx = next((i for i, p in enumerate(all_p) if p.get("tarih") == target.get("tarih") and p.get("model_adi") == target.get("model_adi")), -1)
        if real_idx >= 0:
            removed = all_p.pop(real_idx)
            stock = load_json(STOCK_FILE, {})
            fil = removed.get("filament_turu","")
            stock[fil] = stock.get(fil,0) + removed.get("gram",0) + removed.get("destek_gram",0)
            save_json(STOCK_FILE, stock)
            u_save(PROJECTS_FILE, self.user, all_p)
            log_activity(self.user, "PROJE SİLİNDİ", removed.get("model_adi",""))
        self._refresh_list()

    def _export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "CSV Kaydet", f"projeler_{datetime.now().strftime('%Y%m%d')}.csv", "CSV (*.csv)")
        if not path: return
        projects = u_load(PROJECTS_FILE, self.user)
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Model","Kategori","Filament","Gram","Süre","F.Maliyet","E.Maliyet","Toplam","Durum","Tarih"])
            for p in projects:
                w.writerow([p.get("model_adi",""), p.get("kategori",""), p.get("filament_turu",""),
                            p.get("gram",0), p.get("sure",0), p.get("filament_maliyet",0),
                            p.get("elektrik_maliyet",0), p.get("toplam_maliyet",0),
                            p.get("durum",""), p.get("tarih","")])
        QMessageBox.information(self, "CSV", f"Kaydedildi:\n{path}")

    def refresh(self):
        self._refresh_list()

# ═══════════════════════════════════════════════════════════════
#  STOK TAKİBİ
# ═══════════════════════════════════════════════════════════════
class StockPage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(16,16,16,16)
        main.setSpacing(12)

        # Sol form
        left = CardFrame()
        left.setFixedWidth(340)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20,16,20,16)
        ll.setSpacing(8)

        QLabel_h = QLabel("📦 STOK İŞLEMİ")
        QLabel_h.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        QLabel_h.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        ll.addWidget(QLabel_h)

        self.cb_fil = QComboBox(); self.cb_fil.setMinimumHeight(38)
        self.cb_fil.addItems(sorted(FILAMENT_DATA.keys()))
        ll.addWidget(QLabel("Filament Seç:"))
        ll.addWidget(self.cb_fil)

        self.e_amount = QLineEdit(); self.e_amount.setPlaceholderText("Gram (+ ekle, - çıkar)"); self.e_amount.setMinimumHeight(38)
        self.e_stk_note = QLineEdit(); self.e_stk_note.setPlaceholderText("Açıklama / Tedarikçi"); self.e_stk_note.setMinimumHeight(38)
        ll.addWidget(self.e_amount)
        ll.addWidget(self.e_stk_note)

        for text, func, style in [
            ("➕ Ekle / Çıkar", self._update_stock, "primary"),
            ("↩ Seçileni Sıfırla", self._reset_stock, "danger"),
            ("📦 Toplu Ekle", self._bulk_add, "flat"),
        ]:
            btn = StyledButton(text, style)
            btn.clicked.connect(func)
            ll.addWidget(btn)

        self.stk_info = QLabel("")
        self.stk_info.setWordWrap(True)
        self.stk_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        ll.addWidget(self.stk_info)

        # Eşik
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {SM.t('border')};")
        ll.addWidget(sep)

        ll.addWidget(QLabel("⚠️ Düşük Stok Eşiği (g):"))
        self.e_threshold = QLineEdit()
        self.e_threshold.setText(str(int(get_settings().get("low_stock_threshold",500))))
        self.e_threshold.setMinimumHeight(38)
        ll.addWidget(self.e_threshold)
        save_thr_btn = StyledButton("💾 Eşiği Kaydet", "warning")
        save_thr_btn.clicked.connect(self._save_threshold)
        ll.addWidget(save_thr_btn)

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet(f"color: {SM.t('border')};")
        ll.addWidget(sep2)

        csv_btn = StyledButton("📥 CSV Dışa Aktar", "flat")
        csv_btn.clicked.connect(self._export_csv)
        ll.addWidget(csv_btn)

        import_btn = StyledButton("📤 CSV İçe Aktar", "flat")
        import_btn.clicked.connect(self._import_csv)
        ll.addWidget(import_btn)

        # Donut grafik
        ll.addWidget(QLabel("📊 Stok Dağılımı:"))
        self.donut_container = QVBoxLayout()
        ll.addLayout(self.donut_container)
        ll.addStretch()

        main.addWidget(left)

        # Sağ: tablo
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0,0,0,0)
        rl.setSpacing(8)

        hdr = QHBoxLayout()
        hl = QLabel("STOK TABLOSU")
        hl.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        hl.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        hdr.addWidget(hl)
        hdr.addStretch()

        self.cb_filter_cat = QComboBox(); self.cb_filter_cat.setMinimumHeight(36)
        cats = ["Tümü"] + sorted(set(v["kategori"] for v in FILAMENT_DATA.values()))
        self.cb_filter_cat.addItems(cats)
        self.cb_filter_cat.currentTextChanged.connect(self._refresh)
        hdr.addWidget(self.cb_filter_cat)

        ref_btn = StyledButton("🔃 Yenile", "flat")
        ref_btn.clicked.connect(self._refresh)
        hdr.addWidget(ref_btn)
        rl.addLayout(hdr)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Filament","Kategori","Stok (g)","Birim TL/kg","Değer TL","Bar","Durum"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(500)
        rl.addWidget(self.table)

        # Özet satırı
        self.summary_lbl = QLabel("")
        self.summary_lbl.setStyleSheet(f"color: {SM.t('accent')}; font-weight: bold; border: none;")
        rl.addWidget(self.summary_lbl)

        main.addWidget(right)

    def _update_stock(self):
        try:
            fil = self.cb_fil.currentText()
            amount = float(self.e_amount.text().replace(",","."))
            stock = load_json(STOCK_FILE, {})
            new = stock.get(fil, 0) + amount
            if new < 0:
                QMessageBox.warning(self, "Hata", f"Stok negatif olamaz! Mevcut: {stock.get(fil,0):.0f} g"); return
            stock[fil] = new
            save_json(STOCK_FILE, stock)
            op = "eklendi" if amount >= 0 else "çıkarıldı"
            self.stk_info.setText(f"✓ {abs(amount):.0f} g {op}. Yeni: {new:.0f} g")
            log_activity(self.user, "STOK GÜNCELLENDİ", f"{fil}: {amount:+.0f} g")
            self.e_amount.clear()
            self._refresh()
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçerli sayı gir.")

    def _reset_stock(self):
        fil = self.cb_fil.currentText()
        if QMessageBox.question(self,"Onay",f"{fil} sıfırlansın mı?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            s = load_json(STOCK_FILE, {})
            s[fil] = 0
            save_json(STOCK_FILE, s)
            self._refresh()

    def _bulk_add(self):
        """Toplu stok ekleme diyalogu."""
        dlg = QDialog(self)
        dlg.setWindowTitle("Toplu Stok Ekle")
        dlg.setMinimumSize(500, 400)
        dlg.setStyleSheet(f"background: {SM.t('bg')}; color: {SM.t('text')};")
        l = QVBoxLayout(dlg)
        l.addWidget(QLabel("Her satıra: FilamentAdı,Gram gir\nÖrnek: Bambu PLA,1000"))
        te = QTextEdit()
        te.setPlaceholderText("Bambu PLA,1000\neSUN PETG,500")
        te.setStyleSheet(f"background: {SM.t('input_bg')}; color: {SM.t('text')}; border: 1px solid {SM.t('border')};")
        l.addWidget(te)
        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(dlg.accept)
        bb.rejected.connect(dlg.reject)
        l.addWidget(bb)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            stock = load_json(STOCK_FILE, {})
            lines = te.toPlainText().strip().split("\n")
            added = 0
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    fil_name, gram_str = parts[0].strip(), parts[1].strip()
                    try:
                        gram = float(gram_str)
                        if fil_name in FILAMENT_DATA:
                            stock[fil_name] = stock.get(fil_name, 0) + gram
                            added += 1
                    except: pass
            save_json(STOCK_FILE, stock)
            self._refresh()
            QMessageBox.information(self, "Toplu Ekle", f"{added} filament güncellendi.")

    def _save_threshold(self):
        try:
            v = float(self.e_threshold.text().strip())
            s = get_settings()
            s["low_stock_threshold"] = v
            save_settings(s)
            self.stk_info.setText(f"✓ Eşik {v:.0f} g olarak kaydedildi.")
            self._refresh()
        except:
            QMessageBox.warning(self, "Hata", "Sayı gir.")

    def _refresh(self):
        stock = load_json(STOCK_FILE, {})
        threshold = get_settings().get("low_stock_threshold", 500)
        cat_filter = self.cb_filter_cat.currentText() if hasattr(self, "cb_filter_cat") else "Tümü"

        items = []
        for fil, data in FILAMENT_DATA.items():
            if cat_filter != "Tümü" and data["kategori"] != cat_filter: continue
            gram = stock.get(fil, 0)
            fiyat = data["fiyat"]
            deger = (gram/1000)*fiyat
            durum = "❌ TÜKENDİ" if gram == 0 else ("⚠️ DÜŞÜK" if gram < threshold else "✅ YETERLİ")
            items.append((fil, data["kategori"], gram, fiyat, deger, durum))

        self.table.setRowCount(len(items))
        total_val = 0
        nonempty = {}
        for i, (fil, kat, gram, fiyat, deger, durum) in enumerate(items):
            total_val += deger
            if gram > 0:
                nonempty[fil[:10]] = gram
            bar_len = min(int(gram/500), 10)
            bar = "█" * bar_len + "░" * (10 - bar_len)
            for j, val in enumerate([fil, kat, f"{gram:.0f}", f"{fiyat}", f"{deger:.2f}", bar, durum]):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if "TÜKENDİ" in durum:
                    item.setForeground(QColor(SM.t("danger")))
                elif "DÜŞÜK" in durum:
                    item.setForeground(QColor(SM.t("warning")))
                else:
                    item.setForeground(QColor(SM.t("success")))
                self.table.setItem(i, j, item)

        self.summary_lbl.setText(f"Toplam Stok Değeri: {total_val:,.2f} TL  |  {len([x for x in items if x[2]>0])} filament var  |  {len([x for x in items if 0<x[2]<threshold])} düşük")

        # Donut güncelle
        while self.donut_container.count():
            it = self.donut_container.takeAt(0)
            if it.widget(): it.widget().deleteLater()
        top5 = dict(sorted(nonempty.items(), key=lambda x: x[1], reverse=True)[:5])
        if top5:
            dc = DonutChart(top5, 140)
            self.donut_container.addWidget(dc)

    def _export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "CSV Kaydet", f"stok_{datetime.now().strftime('%Y%m%d')}.csv", "CSV (*.csv)")
        if not path: return
        stock = load_json(STOCK_FILE, {})
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Filament","Kategori","Stok (g)","Birim TL/kg","Değer TL"])
            for fil, data in FILAMENT_DATA.items():
                gram = stock.get(fil,0)
                fiyat = data["fiyat"]
                w.writerow([fil, data["kategori"], gram, fiyat, round((gram/1000)*fiyat,2)])
        QMessageBox.information(self, "CSV", f"Stok kaydedildi:\n{path}")

    def _import_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "CSV Seç", "", "CSV (*.csv)")
        if not path: return
        stock = load_json(STOCK_FILE, {})
        count = 0
        try:
            with open(path, encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    fil = row.get("Filament","").strip()
                    gram = float(row.get("Stok (g)","0").replace(",",".") or "0")
                    if fil:
                        stock[fil] = gram
                        count += 1
            save_json(STOCK_FILE, stock)
            self._refresh()
            QMessageBox.information(self, "İçe Aktar", f"{count} filament güncellendi.")
        except Exception as ex:
            QMessageBox.warning(self, "Hata", str(ex))

    def refresh(self):
        self._refresh()

# ═══════════════════════════════════════════════════════════════
#  SATIŞ YÖNETİMİ
# ═══════════════════════════════════════════════════════════════
class SalesPage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(16,16,16,16)
        main.setSpacing(12)

        # Sol form
        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_scroll.setFrameShape(QFrame.Shape.NoFrame)
        form_scroll.setFixedWidth(380)
        fw = QWidget()
        fl = QVBoxLayout(fw)
        fl.setContentsMargins(0,0,8,0)
        fl.setSpacing(8)
        form_scroll.setWidget(fw)

        card = CardFrame()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20,16,20,16)
        cl.setSpacing(8)

        title = QLabel("💰 YENİ SATIŞ")
        title.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        cl.addWidget(title)

        cl.addWidget(QLabel("Proje (opsiyonel):"))
        self.cb_prj = QComboBox(); self.cb_prj.setMinimumHeight(38)
        cl.addWidget(self.cb_prj)

        cl.addWidget(QLabel("Müşteri:"))
        self.cb_cust = QComboBox(); self.cb_cust.setMinimumHeight(38)
        cl.addWidget(self.cb_cust)

        self.e_product = QLineEdit(); self.e_product.setPlaceholderText("Ürün adı *"); self.e_product.setMinimumHeight(38)
        self.e_price   = QLineEdit(); self.e_price.setPlaceholderText("Birim fiyat (TL) *"); self.e_price.setMinimumHeight(38)
        self.e_qty     = QLineEdit(); self.e_qty.setPlaceholderText("Adet"); self.e_qty.setText("1"); self.e_qty.setMinimumHeight(38)
        self.e_disc    = QLineEdit(); self.e_disc.setPlaceholderText("İndirim %"); self.e_disc.setText("0"); self.e_disc.setMinimumHeight(38)
        self.e_kargo   = QLineEdit(); self.e_kargo.setPlaceholderText("Kargo ücreti TL"); self.e_kargo.setText("0"); self.e_kargo.setMinimumHeight(38)
        self.e_sale_note = QLineEdit(); self.e_sale_note.setPlaceholderText("Not"); self.e_sale_note.setMinimumHeight(38)

        for w in [self.e_product, self.e_price, self.e_qty, self.e_disc, self.e_kargo, self.e_sale_note]:
            cl.addWidget(w)

        cl.addWidget(QLabel("Ödeme Yöntemi:"))
        self.cb_pay = QComboBox(); self.cb_pay.setMinimumHeight(38)
        self.cb_pay.addItems(["Nakit","Kredi Kartı","EFT/Havale","Taksit","PayTR","PayPal","Kripto","Diğer"])
        cl.addWidget(self.cb_pay)

        cl.addWidget(QLabel("Sipariş Durumu:"))
        self.cb_order = QComboBox(); self.cb_order.setMinimumHeight(38)
        self.cb_order.addItems(["📦 Hazırlanıyor","🚚 Kargoda","✅ Teslim Edildi","↩️ İade","❌ İptal"])
        cl.addWidget(self.cb_order)

        self.chk_kdv = QCheckBox("KDV Ekle (%20)")
        self.chk_kdv.setStyleSheet(f"color: {SM.t('text')};")
        cl.addWidget(self.chk_kdv)

        # Hesapla
        calc_btn = StyledButton("⚡ Fiyat Hesapla", "warning")
        calc_btn.clicked.connect(self._calc_sale)
        cl.addWidget(calc_btn)

        self.lbl_calc = QLabel("")
        self.lbl_calc.setWordWrap(True)
        self.lbl_calc.setStyleSheet(f"color: {SM.t('warning')}; border: none;")
        cl.addWidget(self.lbl_calc)

        save_btn = StyledButton("💾 Satışı Kaydet")
        save_btn.clicked.connect(self._add_sale)
        cl.addWidget(save_btn)

        self.sale_info = QLabel("")
        self.sale_info.setWordWrap(True)
        self.sale_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        cl.addWidget(self.sale_info)

        # POS özet
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {SM.t('border')};")
        cl.addWidget(sep)
        cl.addWidget(QLabel("📊 Satış Özeti:"))
        self.pos_summary = QLabel("")
        self.pos_summary.setStyleSheet(f"color: {SM.t('accent')}; font-weight: bold; border: none;")
        self.pos_summary.setWordWrap(True)
        cl.addWidget(self.pos_summary)
        cl.addStretch()

        fl.addWidget(card)
        fl.addStretch()
        main.addWidget(form_scroll)

        # Sağ
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0,0,0,0)
        rl.setSpacing(8)

        hdr = QHBoxLayout()
        hl = QLabel("SATIŞ GEÇMİŞİ")
        hl.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        hl.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        hdr.addWidget(hl)
        hdr.addStretch()

        self.search_sale = QLineEdit(); self.search_sale.setPlaceholderText("🔍 Ara..."); self.search_sale.setMinimumHeight(36); self.search_sale.setMaximumWidth(200)
        self.search_sale.textChanged.connect(self._filter_table)
        hdr.addWidget(self.search_sale)

        for text, func, style in [
            ("🗑 Sil", self._del_sale, "danger"),
            ("📥 CSV", self._export_csv, "flat"),
        ]:
            btn = StyledButton(text, style); btn.setMinimumHeight(36)
            btn.clicked.connect(func)
            hdr.addWidget(btn)
        rl.addLayout(hdr)

        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(["#","Ürün","Müşteri","Adet","Birim","İnd%","Kargo","TOPLAM","Kar","Ödeme","Tarih"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(400)
        rl.addWidget(self.table)

        self.sel_input = QLineEdit()
        self.sel_input.setPlaceholderText("Silmek için satış no (tablo sırası)")
        self.sel_input.setMinimumHeight(36)
        rl.addWidget(self.sel_input)

        self.total_lbl = QLabel("")
        self.total_lbl.setStyleSheet(f"color: {SM.t('success')}; font-weight: bold; border: none;")
        rl.addWidget(self.total_lbl)

        main.addWidget(right)
        self.all_sales = []

    def _update_combos(self):
        projects = u_load(PROJECTS_FILE, self.user)
        customers = u_load(CUSTOMERS_FILE, self.user)
        self.cb_prj.clear()
        self.cb_prj.addItem("(Bağımsız)")
        for i, p in enumerate(projects):
            self.cb_prj.addItem(f"[{i+1}] {p.get('model_adi','')}")
        self.cb_cust.clear()
        self.cb_cust.addItem("(Anonim)")
        for c in customers:
            self.cb_cust.addItem(c.get("ad",""))

    def _calc_sale(self):
        try:
            price = float(self.e_price.text().replace(",",".") or "0")
            qty   = int(self.e_qty.text() or "1")
            disc  = float(self.e_disc.text().replace(",",".") or "0")
            kargo = float(self.e_kargo.text().replace(",",".") or "0")
            kdv_r = get_settings().get("kdv_rate",20) if self.chk_kdv.isChecked() else 0
            subtotal = price * qty
            indirim = subtotal * (disc/100)
            total = subtotal - indirim + kargo
            kdv_amount = total * (kdv_r/100)
            genel = total + kdv_amount
            self.lbl_calc.setText(
                f"Ara Toplam: {subtotal:.2f} TL  |  İndirim: {indirim:.2f} TL\n"
                f"Kargo: {kargo:.2f} TL  |  KDV ({kdv_r}%): {kdv_amount:.2f} TL\n"
                f"GENEL TOPLAM: {genel:.2f} TL"
            )
        except Exception as ex:
            self.lbl_calc.setText(f"Hata: {ex}")

    def _add_sale(self):
        try:
            product = self.e_product.text().strip()
            price   = float(self.e_price.text().replace(",","."))
            qty     = int(self.e_qty.text() or "1")
            disc    = float(self.e_disc.text().replace(",",".") or "0")
            kargo   = float(self.e_kargo.text().replace(",",".") or "0")
            payment = self.cb_pay.currentText()
            customer= self.cb_cust.currentText()
            order_s = self.cb_order.currentText()
            note    = self.e_sale_note.text().strip()
            kdv_r   = get_settings().get("kdv_rate",20) if self.chk_kdv.isChecked() else 0

            if not product:
                self.sale_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
                self.sale_info.setText("✗ Ürün adı boş."); return

            subtotal   = price * qty
            indirim    = subtotal * (disc/100)
            total_bfr  = subtotal - indirim + kargo
            kdv_amount = total_bfr * (kdv_r/100)
            total      = total_bfr + kdv_amount

            prj_cost = 0; prj_name = ""
            prj_txt = self.cb_prj.currentText()
            if prj_txt != "(Bağımsız)":
                try:
                    idx = int(prj_txt.split("]")[0].replace("[","")) - 1
                    prj = u_load(PROJECTS_FILE, self.user)[idx]
                    prj_cost = prj.get("toplam_maliyet",0)
                    prj_name = prj.get("model_adi","")
                except: pass

            kar = total - prj_cost * qty

            # Müşteri sadakat puanı
            if customer != "(Anonim)":
                customers = u_load(CUSTOMERS_FILE, self.user)
                for c in customers:
                    if c.get("ad") == customer:
                        c["sadakat_puan"] = c.get("sadakat_puan",0) + int(total/10)
                u_save(CUSTOMERS_FILE, self.user, customers)

            s = {
                "owner": self.user, "urun": product.title(),
                "proje": prj_name, "musteri": customer,
                "birim_fiyat": price, "adet": qty,
                "indirim_yuzde": disc, "kargo": kargo,
                "kdv_oran": kdv_r, "kdv_tutar": round(kdv_amount,2),
                "satis_fiyati": round(total,2),
                "maliyet": round(prj_cost*qty,2),
                "kar": round(kar,2), "odeme": payment,
                "siparis_durumu": order_s,
                "not": note, "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
            }
            sales = u_load(SALES_FILE, self.user)
            sales.append(s)
            u_save(SALES_FILE, self.user, sales)
            log_activity(self.user,"SATIŞ KAYDEDİLDİ",f"{product} — {total:.2f} TL")
            self.sale_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
            self.sale_info.setText(f"✓ Kaydedildi | Toplam: {total:.2f} TL | Kar: {kar:.2f} TL")
            for e in [self.e_product, self.e_price, self.e_sale_note]:
                e.clear()
            self.e_qty.setText("1"); self.e_disc.setText("0"); self.e_kargo.setText("0")
            self._refresh()
        except ValueError as ex:
            self.sale_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.sale_info.setText(f"✗ {ex}")

    def _del_sale(self):
        rows = self.table.selectedItems()
        if rows:
            idx = self.table.row(rows[0])
        else:
            try: idx = int(self.sel_input.text().strip()) - 1
            except: idx = -1
        if idx < 0 or idx >= len(self.all_sales): return
        if QMessageBox.question(self,"Onay","Satış silinsin mi?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes: return
        target = self.all_sales[idx]
        sales = u_load(SALES_FILE, self.user)
        real_idx = next((i for i,s in enumerate(sales) if s.get("tarih")==target.get("tarih") and s.get("urun")==target.get("urun")), -1)
        if real_idx >= 0:
            sales.pop(real_idx)
            u_save(SALES_FILE, self.user, sales)
        self.sel_input.clear()
        self._refresh()

    def _refresh(self):
        self._update_combos()
        self.all_sales = u_load(SALES_FILE, self.user)
        self._filter_table()
        # POS özet
        t_sat = sum(s.get("satis_fiyati",0) for s in self.all_sales)
        t_kar = sum(s.get("kar",0) for s in self.all_sales)
        t_kdv = sum(s.get("kdv_tutar",0) for s in self.all_sales)
        self.pos_summary.setText(
            f"Toplam Satış: {t_sat:,.2f} TL\n"
            f"Net Kar: {t_kar:,.2f} TL\n"
            f"Toplam KDV: {t_kdv:,.2f} TL"
        )

    def _filter_table(self):
        kw = self.search_sale.text().strip().lower() if hasattr(self,"search_sale") else ""
        filtered = self.all_sales
        if kw:
            filtered = [s for s in filtered if kw in f"{s.get('urun','')} {s.get('musteri','')}".lower()]
        self.table.setRowCount(len(filtered))
        for i, s in enumerate(filtered):
            for j, val in enumerate([
                str(i+1), s.get("urun",""), s.get("musteri","Anonim"),
                str(s.get("adet",1)), f"{s.get('birim_fiyat',0):.2f}",
                f"{s.get('indirim_yuzde',0)}%", f"{s.get('kargo',0):.2f}",
                f"{s.get('satis_fiyati',0):.2f} TL",
                f"{s.get('kar',0):.2f} TL",
                s.get("odeme",""), s.get("tarih","")[:10]
            ]):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if j == 8:  # Kar sütunu
                    kar = s.get("kar",0)
                    item.setForeground(QColor(SM.t("success") if kar >= 0 else SM.t("danger")))
                self.table.setItem(i, j, item)

        t_sat = sum(s.get("satis_fiyati",0) for s in filtered)
        t_kar = sum(s.get("kar",0) for s in filtered)
        self.total_lbl.setText(f"Gösterilen: {len(filtered)} satış  |  Toplam: {t_sat:,.2f} TL  |  Net Kar: {t_kar:,.2f} TL")

    def _export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "CSV Kaydet", f"satislar_{datetime.now().strftime('%Y%m%d')}.csv", "CSV (*.csv)")
        if not path: return
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Ürün","Müşteri","Adet","Birim","İnd%","Kargo","KDV","Toplam","Kar","Ödeme","Tarih"])
            for s in u_load(SALES_FILE, self.user):
                w.writerow([s.get("urun",""),s.get("musteri",""),s.get("adet",1),
                            s.get("birim_fiyat",0),s.get("indirim_yuzde",0),
                            s.get("kargo",0),s.get("kdv_tutar",0),s.get("satis_fiyati",0),
                            s.get("kar",0),s.get("odeme",""),s.get("tarih","")])
        QMessageBox.information(self, "CSV", f"Kaydedildi:\n{path}")

    def refresh(self):
        self._refresh()

# ═══════════════════════════════════════════════════════════════
#  FİNANS
# ═══════════════════════════════════════════════════════════════
class FinancePage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(16,16,16,16)
        main.setSpacing(12)

        # Sol
        left = CardFrame()
        left.setFixedWidth(360)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20,16,20,16)
        ll.setSpacing(8)

        title = QLabel("📤 GİDER EKLE")
        title.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        ll.addWidget(title)

        self.e_exp_title = QLineEdit(); self.e_exp_title.setPlaceholderText("Başlık *"); self.e_exp_title.setMinimumHeight(38)
        self.e_exp_amount= QLineEdit(); self.e_exp_amount.setPlaceholderText("Tutar (TL) *"); self.e_exp_amount.setMinimumHeight(38)
        self.e_exp_note  = QLineEdit(); self.e_exp_note.setPlaceholderText("Açıklama"); self.e_exp_note.setMinimumHeight(38)

        ll.addWidget(self.e_exp_title)
        ll.addWidget(self.e_exp_amount)
        ll.addWidget(self.e_exp_note)

        ll.addWidget(QLabel("Kategori:"))
        self.cb_exp_cat = QComboBox(); self.cb_exp_cat.setMinimumHeight(38)
        self.cb_exp_cat.addItems([
            "Filament Alımı","Elektrik","Bakım/Onarım","Ekipman Alımı",
            "Kargo & Ambalaj","Pazarlama","Yazıcı Aksesuarı","Nozul/Parça",
            "Internet/Yazılım","Oda Kirası","Muhasebe","Diğer"
        ])
        ll.addWidget(self.cb_exp_cat)

        save_exp = StyledButton("💾 Gider Kaydet")
        save_exp.clicked.connect(self._add_expense)
        ll.addWidget(save_exp)

        self.exp_info = QLabel("")
        self.exp_info.setWordWrap(True)
        self.exp_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        ll.addWidget(self.exp_info)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {SM.t('border')};")
        ll.addWidget(sep)

        fin_title = QLabel("📊 FİNANSAL ÖZET")
        fin_title.setFont(QFont("Courier New",13,QFont.Weight.Bold))
        fin_title.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        ll.addWidget(fin_title)

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMinimumHeight(280)
        self.summary_text.setStyleSheet(f"background: {SM.t('input_bg')}; color: {SM.t('text')}; border: 1px solid {SM.t('border')}; border-radius: 8px;")
        self.summary_text.setFont(QFont("Courier New",12))
        ll.addWidget(self.summary_text)
        ll.addStretch()

        main.addWidget(left)

        # Sağ
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0,0,0,0)
        rl.setSpacing(8)

        hdr = QHBoxLayout()
        hl = QLabel("GİDER GEÇMİŞİ")
        hl.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        hl.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        hdr.addWidget(hl)
        hdr.addStretch()

        for text, func, style in [
            ("🗑 Sil", self._del_expense, "danger"),
            ("📥 CSV", self._export_csv, "flat"),
        ]:
            btn = StyledButton(text,style); btn.setMinimumHeight(36)
            btn.clicked.connect(func)
            hdr.addWidget(btn)
        rl.addLayout(hdr)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["#","Başlık","Tutar TL","Kategori","Tarih"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        rl.addWidget(self.table)

        self.sel_input = QLineEdit()
        self.sel_input.setPlaceholderText("Silmek için gider no")
        self.sel_input.setMinimumHeight(36)
        rl.addWidget(self.sel_input)

        # Kategori grafik
        self.bar_container = QVBoxLayout()
        rl.addLayout(self.bar_container)
        main.addWidget(right)

    def _add_expense(self):
        try:
            title  = self.e_exp_title.text().strip()
            amount = float(self.e_exp_amount.text().replace(",","."))
            note   = self.e_exp_note.text().strip()
            cat    = self.cb_exp_cat.currentText()
            if not title:
                self.exp_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
                self.exp_info.setText("✗ Başlık boş."); return
            exps = u_load(EXPENSES_FILE, self.user)
            exps.append({"owner":self.user,"baslik":title.title(),"tutar":amount,
                         "kategori":cat,"not":note,
                         "tarih":datetime.now().strftime("%d.%m.%Y %H:%M")})
            u_save(EXPENSES_FILE, self.user, exps)
            log_activity(self.user,"GİDER KAYDEDİLDİ",f"{title} — {amount:.2f} TL")
            self.exp_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
            self.exp_info.setText(f"✓ {amount:.2f} TL gider kaydedildi.")
            self.e_exp_title.clear(); self.e_exp_amount.clear(); self.e_exp_note.clear()
            self._refresh()
        except ValueError:
            self.exp_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.exp_info.setText("✗ Tutar sayı olmalı.")

    def _del_expense(self):
        rows = self.table.selectedItems()
        if rows:
            idx = self.table.row(rows[0])
        else:
            try: idx = int(self.sel_input.text().strip())-1
            except: idx = -1
        exps = u_load(EXPENSES_FILE, self.user)
        if idx<0 or idx>=len(exps): return
        if QMessageBox.question(self,"Onay","Gider silinsin mi?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes: return
        exps.pop(idx)
        u_save(EXPENSES_FILE, self.user, exps)
        self.sel_input.clear()
        self._refresh()

    def _refresh(self):
        exps     = u_load(EXPENSES_FILE, self.user)
        sales    = u_load(SALES_FILE, self.user)
        projects = u_load(PROJECTS_FILE, self.user)
        t_sat  = sum(s.get("satis_fiyati",0) for s in sales)
        t_mal  = sum(p.get("toplam_maliyet",0) for p in projects)
        t_gid  = sum(e.get("tutar",0) for e in exps)
        net    = t_sat - t_mal - t_gid
        t_kdv  = sum(s.get("kdv_tutar",0) for s in sales)

        cat_totals = {}
        for e in exps:
            cat_totals[e.get("kategori","Diğer")] = cat_totals.get(e.get("kategori","Diğer"),0) + e.get("tutar",0)

        summary = (
            f" Toplam Satış    : {t_sat:>10,.2f} TL\n"
            f" Proje Maliyeti  : {t_mal:>10,.2f} TL\n"
            f" Toplam Gider    : {t_gid:>10,.2f} TL\n"
            f" Toplam KDV      : {t_kdv:>10,.2f} TL\n"
            + "─"*34 + "\n"
            f" NET KAR/ZARAR   : {net:>10,.2f} TL\n\n"
            " Kategori Bazlı:\n"
        )
        for cat, total in sorted(cat_totals.items(), key=lambda x:x[1], reverse=True):
            summary += f"  {cat:<18}: {total:,.2f} TL\n"
        self.summary_text.setPlainText(summary)

        self.table.setRowCount(len(exps))
        for i, e in enumerate(exps):
            for j, val in enumerate([str(i+1), e.get("baslik",""), f"{e.get('tutar',0):.2f} TL", e.get("kategori",""), e.get("tarih","")[:10]]):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, j, item)

        # Grafik
        while self.bar_container.count():
            it = self.bar_container.takeAt(0)
            if it.widget(): it.widget().deleteLater()
        if cat_totals:
            bc = BarChart(cat_totals, SM.t("danger"))
            bc.setMinimumHeight(100)
            self.bar_container.addWidget(bc)

    def _export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self,"CSV Kaydet",f"giderler_{datetime.now().strftime('%Y%m%d')}.csv","CSV (*.csv)")
        if not path: return
        exps = u_load(EXPENSES_FILE, self.user)
        with open(path,"w",encoding="utf-8-sig",newline="") as f:
            w = csv.writer(f)
            w.writerow(["Başlık","Tutar","Kategori","Not","Tarih"])
            for e in exps:
                w.writerow([e.get("baslik",""),e.get("tutar",0),e.get("kategori",""),e.get("not",""),e.get("tarih","")])
        QMessageBox.information(self,"CSV",f"Kaydedildi:\n{path}")

    def refresh(self): self._refresh()

# ═══════════════════════════════════════════════════════════════
#  MÜŞTERİ YÖNETİMİ
# ═══════════════════════════════════════════════════════════════
class CustomersPage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(16,16,16,16)
        main.setSpacing(12)

        # Sol form
        left = CardFrame()
        left.setFixedWidth(360)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20,16,20,16)
        ll.setSpacing(8)

        title = QLabel("👥 MÜŞTERİ EKLE")
        title.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        ll.addWidget(title)

        fields = [
            ("e_cust_name","Ad Soyad *"),("e_cust_phone","Telefon"),
            ("e_cust_email","E-posta"),("e_cust_address","Adres"),
            ("e_cust_tc","TC / Vergi No"),("e_cust_company","Firma"),
            ("e_cust_note","Not"),("e_cust_bday","Doğum Günü (GG.AA.YYYY)"),
        ]
        for attr, ph in fields:
            e = QLineEdit(); e.setPlaceholderText(ph); e.setMinimumHeight(38)
            ll.addWidget(e)
            setattr(self, attr, e)

        ll.addWidget(QLabel("Müşteri Kategorisi:"))
        self.cb_cust_cat = QComboBox(); self.cb_cust_cat.setMinimumHeight(38)
        self.cb_cust_cat.addItems(["Standart","VIP","Toptan","Kurumsal","Öğrenci","Marketer"])
        ll.addWidget(self.cb_cust_cat)

        save_btn = StyledButton("💾 Müşteri Ekle")
        save_btn.clicked.connect(self._add_customer)
        ll.addWidget(save_btn)

        self.cust_info = QLabel("")
        self.cust_info.setWordWrap(True)
        self.cust_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        ll.addWidget(self.cust_info)
        ll.addStretch()

        main.addWidget(left)

        # Sağ
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0,0,0,0)
        rl.setSpacing(8)

        hdr = QHBoxLayout()
        hl = QLabel("MÜŞTERİ LİSTESİ")
        hl.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        hl.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        hdr.addWidget(hl)
        hdr.addStretch()
        self.cust_search = QLineEdit(); self.cust_search.setPlaceholderText("🔍 Ara..."); self.cust_search.setMaximumWidth(200); self.cust_search.setMinimumHeight(36)
        self.cust_search.textChanged.connect(self._filter)
        hdr.addWidget(self.cust_search)
        for text,func,style in [
            ("📋 Detay",self._show_detail,"flat"),
            ("🗑 Sil",self._del_customer,"danger"),
            ("📥 CSV",self._export_csv,"flat"),
        ]:
            btn=StyledButton(text,style); btn.setMinimumHeight(36); btn.clicked.connect(func); hdr.addWidget(btn)
        rl.addLayout(hdr)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["#","Ad Soyad","Telefon","E-posta","Kategori","Sadakat","Alışveriş","Toplam TL","Kayıt"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        rl.addWidget(self.table)

        self.sel_input = QLineEdit(); self.sel_input.setPlaceholderText("Silmek için müşteri no"); self.sel_input.setMinimumHeight(36)
        rl.addWidget(self.sel_input)
        main.addWidget(right)
        self.all_customers = []

    def _add_customer(self):
        name = self.e_cust_name.text().strip()
        if not name:
            self.cust_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.cust_info.setText("✗ Ad boş."); return
        custs = u_load(CUSTOMERS_FILE, self.user)
        custs.append({
            "owner":self.user,"ad":name.title(),
            "telefon":self.e_cust_phone.text().strip(),
            "email":self.e_cust_email.text().strip(),
            "adres":self.e_cust_address.text().strip(),
            "tc":self.e_cust_tc.text().strip(),
            "firma":self.e_cust_company.text().strip(),
            "not":self.e_cust_note.text().strip(),
            "dogum_gunu":self.e_cust_bday.text().strip(),
            "kategori":self.cb_cust_cat.currentText(),
            "sadakat_puan":0,
            "kayit":datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        u_save(CUSTOMERS_FILE, self.user, custs)
        log_activity(self.user,"MÜŞTERİ EKLENDİ",name)
        self.cust_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        self.cust_info.setText(f"✓ {name} eklendi.")
        for attr in ["e_cust_name","e_cust_phone","e_cust_email","e_cust_address","e_cust_tc","e_cust_company","e_cust_note","e_cust_bday"]:
            getattr(self,attr).clear()
        self._refresh()

    def _del_customer(self):
        rows = self.table.selectedItems()
        idx = self.table.row(rows[0]) if rows else -1
        if idx < 0:
            try: idx = int(self.sel_input.text().strip())-1
            except: idx = -1
        if idx < 0 or idx >= len(self.all_customers): return
        if QMessageBox.question(self,"Onay","Müşteri silinsin mi?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes: return
        target = self.all_customers[idx]
        custs = u_load(CUSTOMERS_FILE, self.user)
        real = next((i for i,c in enumerate(custs) if c.get("kayit")==target.get("kayit") and c.get("ad")==target.get("ad")),-1)
        if real >= 0: custs.pop(real)
        u_save(CUSTOMERS_FILE, self.user, custs)
        self.sel_input.clear()
        self._refresh()

    def _show_detail(self):
        rows = self.table.selectedItems()
        if not rows: return
        idx = self.table.row(rows[0])
        if idx < 0 or idx >= len(self.all_customers): return
        c = self.all_customers[idx]
        sales = u_load(SALES_FILE, self.user)
        c_sales = [s for s in sales if s.get("musteri") == c.get("ad")]
        detail = (
            f"Ad Soyad  : {c.get('ad','')}\n"
            f"Telefon   : {c.get('telefon','')}\n"
            f"E-posta   : {c.get('email','')}\n"
            f"Adres     : {c.get('adres','')}\n"
            f"Firma     : {c.get('firma','')}\n"
            f"Kategori  : {c.get('kategori','')}\n"
            f"Sadakat   : {c.get('sadakat_puan',0)} puan\n"
            f"Doğum Günü: {c.get('dogum_gunu','')}\n"
            f"Not       : {c.get('not','')}\n"
            f"─────────────────────────\n"
            f"Alışveriş : {len(c_sales)} sipariş\n"
            f"Toplam    : {sum(s.get('satis_fiyati',0) for s in c_sales):,.2f} TL\n"
            f"Kayıt     : {c.get('kayit','')}\n"
        )
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Müşteri Detayı - {c.get('ad','')}")
        dlg.setMinimumSize(400,380)
        dlg.setStyleSheet(f"background: {SM.t('bg')}; color: {SM.t('text')};")
        l = QVBoxLayout(dlg)
        te = QTextEdit(); te.setReadOnly(True); te.setPlainText(detail)
        te.setFont(QFont("Courier New",12))
        te.setStyleSheet(f"background: {SM.t('input_bg')}; color: {SM.t('text')}; border: 1px solid {SM.t('border')};")
        l.addWidget(te)
        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        bb.rejected.connect(dlg.reject)
        l.addWidget(bb)
        dlg.exec()

    def _refresh(self):
        self.all_customers = u_load(CUSTOMERS_FILE, self.user)
        self._filter()

    def _filter(self):
        kw = self.cust_search.text().strip().lower() if hasattr(self,"cust_search") else ""
        filtered = self.all_customers
        if kw:
            filtered = [c for c in filtered if kw in f"{c.get('ad','')} {c.get('email','')} {c.get('telefon','')}".lower()]
        sales = u_load(SALES_FILE, self.user)
        self.table.setRowCount(len(filtered))
        for i, c in enumerate(filtered):
            name = c.get("ad","")
            c_sales = [s for s in sales if s.get("musteri") == name]
            total = sum(s.get("satis_fiyati",0) for s in c_sales)
            for j, val in enumerate([
                str(i+1), name, c.get("telefon",""), c.get("email",""),
                c.get("kategori",""), str(c.get("sadakat_puan",0)),
                str(len(c_sales)), f"{total:,.2f}", c.get("kayit","")[:10]
            ]):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if c.get("kategori") == "VIP":
                    item.setForeground(QColor(SM.t("warning")))
                self.table.setItem(i, j, item)

    def _export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self,"CSV Kaydet",f"musteriler_{datetime.now().strftime('%Y%m%d')}.csv","CSV (*.csv)")
        if not path: return
        custs = u_load(CUSTOMERS_FILE, self.user)
        with open(path,"w",encoding="utf-8-sig",newline="") as f:
            w = csv.writer(f)
            w.writerow(["Ad","Telefon","Email","Adres","Firma","Kategori","Sadakat","Kayıt"])
            for c in custs:
                w.writerow([c.get("ad",""),c.get("telefon",""),c.get("email",""),c.get("adres",""),c.get("firma",""),c.get("kategori",""),c.get("sadakat_puan",0),c.get("kayit","")])
        QMessageBox.information(self,"CSV",f"Kaydedildi:\n{path}")

    def refresh(self): self._refresh()

# ═══════════════════════════════════════════════════════════════
#  GÖREVLER & TAKVİM
# ═══════════════════════════════════════════════════════════════
class TasksPage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(16,16,16,16)
        main.setSpacing(12)

        # Sol
        left = CardFrame()
        left.setFixedWidth(360)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20,16,20,16)
        ll.setSpacing(8)

        title = QLabel("✅ YENİ GÖREV")
        title.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        ll.addWidget(title)

        self.e_task_title = QLineEdit(); self.e_task_title.setPlaceholderText("Görev başlığı *"); self.e_task_title.setMinimumHeight(38)
        self.e_task_detail= QLineEdit(); self.e_task_detail.setPlaceholderText("Detay"); self.e_task_detail.setMinimumHeight(38)
        self.e_task_due   = QDateEdit(); self.e_task_due.setDisplayFormat("dd.MM.yyyy"); self.e_task_due.setDate(QDate.currentDate().addDays(1)); self.e_task_due.setMinimumHeight(38)
        self.e_task_assign= QLineEdit(); self.e_task_assign.setPlaceholderText("Atanan kişi"); self.e_task_assign.setMinimumHeight(38)

        for w in [self.e_task_title, self.e_task_detail, self.e_task_due, self.e_task_assign]:
            ll.addWidget(w)

        ll.addWidget(QLabel("Öncelik:"))
        self.cb_task_prio = QComboBox(); self.cb_task_prio.setMinimumHeight(38)
        self.cb_task_prio.addItems(["🟢 Düşük","🟡 Orta","🔴 Yüksek","🚨 Acil"])
        ll.addWidget(self.cb_task_prio)

        ll.addWidget(QLabel("Kategori:"))
        self.cb_task_cat = QComboBox(); self.cb_task_cat.setMinimumHeight(38)
        self.cb_task_cat.addItems(["Genel","Bakım","Sipariş","Alım","Müşteri","Yazılım","Diğer"])
        ll.addWidget(self.cb_task_cat)

        add_btn = StyledButton("➕ Görev Ekle")
        add_btn.clicked.connect(self._add_task)
        ll.addWidget(add_btn)

        self.task_info = QLabel("")
        self.task_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        ll.addWidget(self.task_info)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setStyleSheet(f"color: {SM.t('border')};")
        ll.addWidget(sep)

        # Takvim
        ll.addWidget(QLabel("📅 Takvim:"))
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet(f"QCalendarWidget {{ background: {SM.t('input_bg')}; color: {SM.t('text')}; }}")
        self.calendar.setMaximumHeight(220)
        ll.addWidget(self.calendar)
        ll.addStretch()

        main.addWidget(left)

        # Sağ
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0,0,0,0)
        rl.setSpacing(8)

        hdr = QHBoxLayout()
        hl = QLabel("GÖREVLER")
        hl.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        hl.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        hdr.addWidget(hl)
        hdr.addStretch()
        for text,func,style in [
            ("✓ Tamamlandı",self._complete_task,"success"),
            ("🗑 Sil",self._del_task,"danger"),
        ]:
            btn=StyledButton(text,style); btn.setMinimumHeight(36); btn.clicked.connect(func); hdr.addWidget(btn)
        rl.addLayout(hdr)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["#","Başlık","Detay","Öncelik","Kategori","Son Tarih","Durum"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        rl.addWidget(self.table)

        self.sel_input = QLineEdit(); self.sel_input.setPlaceholderText("Görev no (tablo sırası)"); self.sel_input.setMinimumHeight(36)
        rl.addWidget(self.sel_input)
        main.addWidget(right)
        self.all_tasks = []

    def _add_task(self):
        title = self.e_task_title.text().strip()
        if not title:
            self.task_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.task_info.setText("✗ Başlık boş."); return
        tasks = u_load(TASKS_FILE, self.user)
        tasks.append({
            "owner":self.user,"baslik":title,
            "detay":self.e_task_detail.text().strip(),
            "son_tarih":self.e_task_due.date().toString("dd.MM.yyyy"),
            "atanan":self.e_task_assign.text().strip(),
            "oncelik":self.cb_task_prio.currentText(),
            "kategori":self.cb_task_cat.currentText(),
            "durum":"Bekliyor",
            "tarih":datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        u_save(TASKS_FILE, self.user, tasks)
        self.task_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        self.task_info.setText("✓ Görev eklendi.")
        self.e_task_title.clear(); self.e_task_detail.clear(); self.e_task_assign.clear()
        self._refresh()

    def _complete_task(self):
        rows = self.table.selectedItems()
        idx = self.table.row(rows[0]) if rows else -1
        if idx < 0:
            try: idx = int(self.sel_input.text().strip())-1
            except: idx = -1
        if idx < 0 or idx >= len(self.all_tasks): return
        target = self.all_tasks[idx]
        tasks = u_load(TASKS_FILE, self.user)
        for t in tasks:
            if t.get("tarih") == target.get("tarih") and t.get("baslik") == target.get("baslik"):
                t["durum"] = "✅ Tamamlandı"; break
        u_save(TASKS_FILE, self.user, tasks)
        self.sel_input.clear()
        self._refresh()

    def _del_task(self):
        rows = self.table.selectedItems()
        idx = self.table.row(rows[0]) if rows else -1
        if idx < 0:
            try: idx = int(self.sel_input.text().strip())-1
            except: idx = -1
        if idx < 0 or idx >= len(self.all_tasks): return
        target = self.all_tasks[idx]
        tasks = u_load(TASKS_FILE, self.user)
        real = next((i for i,t in enumerate(tasks) if t.get("tarih")==target.get("tarih") and t.get("baslik")==target.get("baslik")),-1)
        if real >= 0: tasks.pop(real)
        u_save(TASKS_FILE, self.user, tasks)
        self.sel_input.clear()
        self._refresh()

    def _refresh(self):
        self.all_tasks = u_load(TASKS_FILE, self.user)
        self.table.setRowCount(len(self.all_tasks))
        today = datetime.now().strftime("%d.%m.%Y")
        for i, t in enumerate(self.all_tasks):
            due = t.get("son_tarih","")
            durum = t.get("durum","Bekliyor")
            row_data = [str(i+1),t.get("baslik",""),t.get("detay",""),t.get("oncelik",""),t.get("kategori",""),due,durum]
            for j, val in enumerate(row_data):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if "Tamamlandı" in durum:
                    item.setForeground(QColor(SM.t("success")))
                elif "Acil" in t.get("oncelik",""):
                    item.setForeground(QColor(SM.t("danger")))
                self.table.setItem(i, j, item)

    def refresh(self): self._refresh()

# ═══════════════════════════════════════════════════════════════
#  İSTATİSTİKLER
# ═══════════════════════════════════════════════════════════════
class StatsPage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        self.cl = QVBoxLayout(content)
        self.cl.setContentsMargins(20,16,20,20)
        self.cl.setSpacing(12)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        ref_btn = StyledButton("🔃 Yenile", "flat")
        ref_btn.setMaximumWidth(100)
        ref_btn.clicked.connect(self._refresh)
        self.cl.addWidget(ref_btn)

    def _refresh(self):
        while self.cl.count() > 1:
            item = self.cl.takeAt(1)
            if item.widget(): item.widget().deleteLater()

        projects = u_load(PROJECTS_FILE, self.user)
        sales    = u_load(SALES_FILE,    self.user)
        expenses = u_load(EXPENSES_FILE, self.user)
        stock    = load_json(STOCK_FILE, {})

        # Filament kullanım
        self.cl.addWidget(SectionHeader("🧵 Filament Kullanımı"))
        fil_row = QHBoxLayout()
        fil_use = {}
        for p in projects:
            f = p.get("filament_turu","?")
            fil_use[f] = fil_use.get(f,0) + p.get("gram",0)

        if fil_use:
            bc = BarChart(fil_use, SM.t("accent"))
            bc.setMinimumHeight(130)
            fil_row.addWidget(bc, stretch=2)
            dc = DonutChart(fil_use, 155)
            fil_row.addWidget(dc)
        else:
            fil_row.addWidget(QLabel("Veri yok."))
        fil_card = CardFrame()
        fl = QVBoxLayout(fil_card)
        fl.setContentsMargins(12,12,12,12)
        fl.addLayout(fil_row)
        self.cl.addWidget(fil_card)

        # En çok satan
        self.cl.addWidget(SectionHeader("🏆 En Çok Satan Ürünler"))
        urun_totals = {}
        for s in sales:
            u = s.get("urun","?")
            urun_totals[u] = urun_totals.get(u,0) + s.get("satis_fiyati",0)
        top5 = dict(sorted(urun_totals.items(), key=lambda x:x[1], reverse=True)[:8])
        top_card = CardFrame()
        tl = QVBoxLayout(top_card)
        tl.setContentsMargins(12,12,12,12)
        if top5:
            bc2 = BarChart(top5, SM.t("success"))
            bc2.setMinimumHeight(130)
            tl.addWidget(bc2)
            medals = ["🥇","🥈","🥉","🏅","🏅","🏅","🏅","🏅"]
            for i,(u,t) in enumerate(top5.items()):
                row_l = QHBoxLayout()
                row_l.addWidget(QLabel(f"{medals[i]} {i+1}. {u}"))
                val = QLabel(f"{t:,.2f} TL")
                val.setStyleSheet(f"color: {SM.t('success')}; font-weight: bold; border: none;")
                row_l.addStretch()
                row_l.addWidget(val)
                tl.addLayout(row_l)
        else:
            tl.addWidget(QLabel("Satış yok."))
        self.cl.addWidget(top_card)

        # Aylık gelir/gider karşılaştırması
        self.cl.addWidget(SectionHeader("📅 Son 6 Ay Gelir vs Gider"))
        monthly_card = CardFrame()
        ml = QVBoxLayout(monthly_card)
        ml.setContentsMargins(12,12,12,12)

        months = {}
        for i in range(5,-1,-1):
            d = datetime.now() - timedelta(days=30*i)
            key = d.strftime("%m.%Y")
            months[key] = {"gelir":0,"gider":0}

        for s in sales:
            key = s.get("tarih","")[:7]
            if key.replace(".", "") and key in months:
                months[key]["gelir"] += s.get("satis_fiyati",0)
        for e in expenses:
            key = e.get("tarih","")[:7]
            if key in months:
                months[key]["gider"] += e.get("tutar",0)

        gelir_data = {k: v["gelir"] for k,v in months.items()}
        gider_data = {k: v["gider"] for k,v in months.items()}

        bar_row = QHBoxLayout()
        bc_gelir = BarChart(gelir_data, SM.t("success")); bc_gelir.setMinimumHeight(100)
        bc_gider = BarChart(gider_data, SM.t("danger")); bc_gider.setMinimumHeight(100)
        bar_row.addWidget(bc_gelir)
        bar_row.addWidget(bc_gider)

        lbl_row = QHBoxLayout()
        g1 = QLabel("■ Gelir"); g1.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        g2 = QLabel("■ Gider"); g2.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
        lbl_row.addWidget(g1); lbl_row.addWidget(g2); lbl_row.addStretch()

        ml.addLayout(bar_row)
        ml.addLayout(lbl_row)
        self.cl.addWidget(monthly_card)

        # Yazıcı istatistikleri
        self.cl.addWidget(SectionHeader("🖨️ Yazıcı Kullanım İstatistikleri"))
        prn_card = CardFrame()
        pl = QVBoxLayout(prn_card)
        pl.setContentsMargins(12,12,12,12)
        pstats = {}
        for p in projects:
            k = f"{p.get('yazici_marka','?')} {p.get('yazici_model','?')}"
            pstats.setdefault(k,{"proje":0,"gram":0,"sure":0,"maliyet":0})
            pstats[k]["proje"] += 1
            pstats[k]["gram"] += p.get("gram",0)
            pstats[k]["sure"] += p.get("sure",0)
            pstats[k]["maliyet"] += p.get("toplam_maliyet",0)

        tbl = QTableWidget()
        tbl.setColumnCount(5)
        tbl.setHorizontalHeaderLabels(["Yazıcı","Proje","Toplam Gram","Süre (h)","Maliyet TL"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tbl.setRowCount(len(pstats))
        for i,(prn,st) in enumerate(sorted(pstats.items(),key=lambda x:x[1]["proje"],reverse=True)):
            for j,val in enumerate([prn,str(st["proje"]),f"{st['gram']:.0f}",f"{st['sure']:.1f}",f"{st['maliyet']:.2f}"]):
                item=QTableWidgetItem(val); item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable); tbl.setItem(i,j,item)
        tbl.setMaximumHeight(200)
        pl.addWidget(tbl)
        self.cl.addWidget(prn_card)

        # ROI & Elektrik raporu
        self.cl.addWidget(SectionHeader("💡 ROI & Elektrik Raporu"))
        roi_card = CardFrame()
        rl = QVBoxLayout(roi_card)
        rl.setContentsMargins(12,12,12,12)

        total_elec = sum(p.get("elektrik_maliyet",0) for p in projects)
        total_fil  = sum(p.get("filament_maliyet",0) for p in projects)
        total_cost = sum(p.get("toplam_maliyet",0) for p in projects)
        total_rev  = sum(s.get("satis_fiyati",0) for s in sales)
        total_exp  = sum(e.get("tutar",0) for e in expenses)
        net = total_rev - total_cost - total_exp
        roi = (net / total_cost * 100) if total_cost > 0 else 0

        stats_text = QTextEdit()
        stats_text.setReadOnly(True)
        stats_text.setFont(QFont("Courier New",12))
        stats_text.setMaximumHeight(180)
        stats_text.setStyleSheet(f"background: {SM.t('input_bg')}; color: {SM.t('text')}; border: 1px solid {SM.t('border')};")
        stats_text.setPlainText(
            f" Filament Maliyeti : {total_fil:>10,.2f} TL\n"
            f" Elektrik Maliyeti : {total_elec:>10,.2f} TL\n"
            f" Toplam Prj Maliyet: {total_cost:>10,.2f} TL\n"
            f" Toplam Satış      : {total_rev:>10,.2f} TL\n"
            f" Toplam Gider      : {total_exp:>10,.2f} TL\n"
            f" Net Kar           : {net:>10,.2f} TL\n"
            f" ROI               : {roi:>9,.1f} %\n"
        )
        rl.addWidget(stats_text)
        self.cl.addWidget(roi_card)
        self.cl.addStretch()

    def refresh(self): self._refresh()

# ═══════════════════════════════════════════════════════════════
#  NOTLAR & AYARLAR & LOG TEK BÖLÜM
# ═══════════════════════════════════════════════════════════════
class NotesPage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(16,16,16,16)
        main.setSpacing(12)

        left = CardFrame()
        left.setFixedWidth(360)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20,16,20,16)
        ll.setSpacing(8)

        title = QLabel("📝 YENİ NOT")
        title.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        ll.addWidget(title)

        self.e_note_title = QLineEdit(); self.e_note_title.setPlaceholderText("Başlık"); self.e_note_title.setMinimumHeight(38)
        ll.addWidget(self.e_note_title)

        ll.addWidget(QLabel("Etiket:"))
        self.cb_note_tag = QComboBox(); self.cb_note_tag.setMinimumHeight(38)
        self.cb_note_tag.addItems(["Genel","Teknik","Müşteri","Fikir","Hatırlatma","Gizli"])
        ll.addWidget(self.cb_note_tag)

        ll.addWidget(QLabel("İçerik:"))
        self.e_note_body = QTextEdit()
        self.e_note_body.setMinimumHeight(200)
        self.e_note_body.setStyleSheet(f"background: {SM.t('input_bg')}; color: {SM.t('text')}; border: 1px solid {SM.t('border')};")
        ll.addWidget(self.e_note_body)

        save_btn = StyledButton("💾 Notu Kaydet")
        save_btn.clicked.connect(self._add_note)
        ll.addWidget(save_btn)

        self.note_info = QLabel("")
        self.note_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        ll.addWidget(self.note_info)
        ll.addStretch()
        main.addWidget(left)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0,0,0,0)

        hdr = QHBoxLayout()
        hl = QLabel("NOTLAR")
        hl.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        hl.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        hdr.addWidget(hl)
        hdr.addStretch()
        del_btn = StyledButton("🗑 Sil","danger"); del_btn.setMinimumHeight(36); del_btn.clicked.connect(self._del_note)
        hdr.addWidget(del_btn)
        rl.addLayout(hdr)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["#","Başlık","Etiket","Tarih"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.itemClicked.connect(self._show_note)
        self.table.setAlternatingRowColors(True)
        rl.addWidget(self.table)

        self.note_preview = QTextEdit()
        self.note_preview.setReadOnly(True)
        self.note_preview.setFont(QFont("Courier New",12))
        self.note_preview.setStyleSheet(f"background: {SM.t('input_bg')}; color: {SM.t('text')}; border: 1px solid {SM.t('border')};")
        self.note_preview.setMaximumHeight(200)
        rl.addWidget(self.note_preview)

        self.sel_input = QLineEdit(); self.sel_input.setPlaceholderText("Silmek için not no"); self.sel_input.setMinimumHeight(36)
        rl.addWidget(self.sel_input)
        main.addWidget(right)
        self.all_notes = []

    def _add_note(self):
        body = self.e_note_body.toPlainText().strip()
        if not body:
            self.note_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.note_info.setText("✗ İçerik boş."); return
        notes = u_load(NOTES_FILE, self.user)
        notes.append({
            "owner":self.user,"baslik":self.e_note_title.text().strip() or "—",
            "icerik":body,"etiket":self.cb_note_tag.currentText(),
            "tarih":datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        u_save(NOTES_FILE, self.user, notes)
        self.note_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        self.note_info.setText("✓ Not kaydedildi.")
        self.e_note_title.clear(); self.e_note_body.clear()
        self._refresh()

    def _del_note(self):
        rows = self.table.selectedItems()
        idx = self.table.row(rows[0]) if rows else -1
        if idx < 0:
            try: idx = int(self.sel_input.text().strip())-1
            except: idx = -1
        if idx < 0 or idx >= len(self.all_notes): return
        notes = u_load(NOTES_FILE, self.user)
        target = self.all_notes[idx]
        real = next((i for i,n in enumerate(notes) if n.get("tarih")==target.get("tarih") and n.get("baslik")==target.get("baslik")),-1)
        if real >= 0: notes.pop(real)
        u_save(NOTES_FILE, self.user, notes)
        self.sel_input.clear()
        self._refresh()

    def _show_note(self, item):
        idx = self.table.row(item)
        if 0 <= idx < len(self.all_notes):
            self.note_preview.setPlainText(self.all_notes[idx].get("icerik",""))

    def _refresh(self):
        self.all_notes = u_load(NOTES_FILE, self.user)
        self.table.setRowCount(len(self.all_notes))
        icons = {"Genel":"📄","Teknik":"🔧","Müşteri":"👤","Fikir":"💡","Hatırlatma":"🔔","Gizli":"🔒"}
        for i, n in enumerate(self.all_notes):
            icon = icons.get(n.get("etiket",""),"📄")
            for j, val in enumerate([str(i+1), n.get("baslik",""), f"{icon} {n.get('etiket','')}", n.get("tarih","")[:10]]):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, j, item)

    def refresh(self): self._refresh()

# ═══════════════════════════════════════════════════════════════
#  BAKIMLAR
# ═══════════════════════════════════════════════════════════════
class MaintenancePage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(16,16,16,16)
        main.setSpacing(12)

        left = CardFrame()
        left.setFixedWidth(360)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20,16,20,16)
        ll.setSpacing(8)

        title = QLabel("🔧 BAKIM KAYDI")
        title.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        ll.addWidget(title)

        self.e_maint_printer = QLineEdit(); self.e_maint_printer.setPlaceholderText("Yazıcı adı *"); self.e_maint_printer.setMinimumHeight(38)
        self.e_maint_type = QLineEdit(); self.e_maint_type.setPlaceholderText("Bakım türü *"); self.e_maint_type.setMinimumHeight(38)
        self.e_maint_cost = QLineEdit(); self.e_maint_cost.setPlaceholderText("Maliyet TL"); self.e_maint_cost.setText("0"); self.e_maint_cost.setMinimumHeight(38)
        self.e_maint_note = QLineEdit(); self.e_maint_note.setPlaceholderText("Not"); self.e_maint_note.setMinimumHeight(38)

        for w in [self.e_maint_printer, self.e_maint_type, self.e_maint_cost, self.e_maint_note]:
            ll.addWidget(w)

        ll.addWidget(QLabel("Bakım Kategorisi:"))
        self.cb_maint_cat = QComboBox(); self.cb_maint_cat.setMinimumHeight(38)
        self.cb_maint_cat.addItems([
            "Nozul Değişimi","PEI Tabla Temizliği","Kalibrasyonu","Yağlama",
            "PTFE Tube Değişimi","Extruder Temizliği","Belt Germe","Güncelleme",
            "Filament Sıkışması","Donanım Arızası","Diğer"
        ])
        ll.addWidget(self.cb_maint_cat)

        add_btn = StyledButton("💾 Bakım Kaydet")
        add_btn.clicked.connect(self._add_maintenance)
        ll.addWidget(add_btn)

        self.maint_info = QLabel("")
        self.maint_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        ll.addWidget(self.maint_info)
        ll.addStretch()
        main.addWidget(left)

        right = QWidget()
        rl = QVBoxLayout(right)

        hdr = QHBoxLayout()
        hl = QLabel("BAKIM GEÇMİŞİ")
        hl.setFont(QFont("Courier New",14,QFont.Weight.Bold))
        hl.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        hdr.addWidget(hl)
        hdr.addStretch()
        del_btn = StyledButton("🗑 Sil","danger"); del_btn.setMinimumHeight(36); del_btn.clicked.connect(self._del_maint)
        hdr.addWidget(del_btn)
        rl.addLayout(hdr)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["#","Yazıcı","Bakım Türü","Kategori","Maliyet","Tarih"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        rl.addWidget(self.table)

        self.sel_input = QLineEdit(); self.sel_input.setPlaceholderText("Silmek için no"); self.sel_input.setMinimumHeight(36)
        rl.addWidget(self.sel_input)
        main.addWidget(right)
        self.all_maintenance = []

    def _add_maintenance(self):
        printer = self.e_maint_printer.text().strip()
        mtype   = self.e_maint_type.text().strip()
        if not printer or not mtype:
            self.maint_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.maint_info.setText("✗ Yazıcı adı ve bakım türü zorunlu."); return
        try:
            cost = float(self.e_maint_cost.text().replace(",",".") or "0")
        except: cost = 0
        items = load_json(MAINTENANCE_FILE, [])
        items.append({
            "owner":self.user, "yazici":printer, "tur":mtype,
            "kategori":self.cb_maint_cat.currentText(),
            "maliyet":cost, "not":self.e_maint_note.text().strip(),
            "tarih":datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        save_json(MAINTENANCE_FILE, items)
        self.maint_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        self.maint_info.setText("✓ Bakım kaydedildi.")
        self.e_maint_printer.clear(); self.e_maint_type.clear()
        self.e_maint_cost.setText("0"); self.e_maint_note.clear()
        self._refresh()

    def _del_maint(self):
        rows = self.table.selectedItems()
        idx = self.table.row(rows[0]) if rows else -1
        if idx < 0:
            try: idx = int(self.sel_input.text().strip())-1
            except: idx = -1
        if idx < 0 or idx >= len(self.all_maintenance): return
        items = load_json(MAINTENANCE_FILE, [])
        target = self.all_maintenance[idx]
        real = next((i for i,m in enumerate(items) if m.get("tarih")==target.get("tarih")),-1)
        if real >= 0: items.pop(real)
        save_json(MAINTENANCE_FILE, items)
        self._refresh()

    def _refresh(self):
        all_m = load_json(MAINTENANCE_FILE, [])
        self.all_maintenance = [m for m in all_m if m.get("owner") == self.user]
        self.table.setRowCount(len(self.all_maintenance))
        for i, m in enumerate(self.all_maintenance):
            for j, val in enumerate([str(i+1),m.get("yazici",""),m.get("tur",""),m.get("kategori",""),f"{m.get('maliyet',0):.2f} TL",m.get("tarih","")[:10]]):
                item=QTableWidgetItem(val); item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable); self.table.setItem(i,j,item)

    def refresh(self): self._refresh()

# ═══════════════════════════════════════════════════════════════
#  AKTİVİTE LOGU
# ═══════════════════════════════════════════════════════════════
class LogPage(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        l = QVBoxLayout(self)
        l.setContentsMargins(16,16,16,16)

        hdr = QHBoxLayout()
        hl = QLabel("📋 AKTİVİTE LOGU")
        hl.setFont(QFont("Courier New",16,QFont.Weight.Bold))
        hl.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        hdr.addWidget(hl)
        hdr.addStretch()
        ref_btn = StyledButton("🔃 Yenile","flat"); ref_btn.clicked.connect(self._refresh)
        clr_btn = StyledButton("🗑 Temizle","danger"); clr_btn.clicked.connect(self._clear)
        hdr.addWidget(ref_btn); hdr.addWidget(clr_btn)
        l.addLayout(hdr)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Tarih","İşlem","Detay"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        l.addWidget(self.table)

    def _refresh(self):
        logs = [l for l in load_json(LOG_FILE,[]) if l.get("owner")==self.user]
        self.table.setRowCount(len(logs))
        icon_map = {"GİRİŞ":"▶","PROJE EKLENDİ":"➕","PROJE SİLİNDİ":"🗑","PROJE GÜNCELLENDİ":"✏️",
                    "STOK GÜNCELLENDİ":"📦","SATIŞ KAYDEDİLDİ":"💰","GİDER KAYDEDİLDİ":"📤","MÜŞTERİ EKLENDİ":"👥"}
        for i, l in enumerate(reversed(logs)):
            icon = icon_map.get(l.get("action",""),"·")
            for j, val in enumerate([l.get("tarih",""), f"{icon} {l.get('action','')}", l.get("detail","")]):
                item=QTableWidgetItem(val); item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable); self.table.setItem(i,j,item)

    def _clear(self):
        if QMessageBox.question(self,"Onay","Tüm log silinsin mi?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            all_l = load_json(LOG_FILE,[])
            save_json(LOG_FILE, [l for l in all_l if l.get("owner") != self.user])
            self._refresh()

    def refresh(self): self._refresh()

# ═══════════════════════════════════════════════════════════════
#  AYARLAR
# ═══════════════════════════════════════════════════════════════
class SettingsPage(QWidget):
    theme_changed = pyqtSignal()

    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(20,16,20,20)
        cl.setSpacing(12)
        scroll.setWidget(content)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(scroll)

        settings = get_settings()

        # Tema
        cl.addWidget(SectionHeader("🎨 Tema Seçimi"))
        theme_card = CardFrame()
        tl = QVBoxLayout(theme_card)
        tl.setContentsMargins(20,16,20,16)
        theme_row = QHBoxLayout()
        self.cb_theme = QComboBox(); self.cb_theme.setMinimumHeight(40)
        self.cb_theme.addItems(list(THEMES.keys()))
        idx = self.cb_theme.findText(settings.get("theme","🌑 Karanlık"))
        if idx >= 0: self.cb_theme.setCurrentIndex(idx)
        theme_row.addWidget(self.cb_theme)
        apply_btn = StyledButton("✅ Temayı Uygula"); apply_btn.clicked.connect(self._apply_theme)
        theme_row.addWidget(apply_btn)
        tl.addLayout(theme_row)
        cl.addWidget(theme_card)

        # Genel ayarlar
        cl.addWidget(SectionHeader("⚙️ Genel Ayarlar"))
        gen_card = CardFrame()
        gl = QVBoxLayout(gen_card)
        gl.setContentsMargins(20,16,20,16)
        gl.setSpacing(8)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Elektrik Fiyatı (TL/kWh):"))
        self.e_elec = QLineEdit(); self.e_elec.setText(str(settings.get("elektrik_fiyati",1.73))); self.e_elec.setMinimumHeight(38); self.e_elec.setMaximumWidth(150)
        row1.addWidget(self.e_elec)
        row1.addStretch()
        gl.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("KDV Oranı (%):"))
        self.e_kdv = QLineEdit(); self.e_kdv.setText(str(settings.get("kdv_rate",20))); self.e_kdv.setMinimumHeight(38); self.e_kdv.setMaximumWidth(150)
        row2.addWidget(self.e_kdv)
        row2.addStretch()
        gl.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Düşük Stok Eşiği (g):"))
        self.e_thr = QLineEdit(); self.e_thr.setText(str(settings.get("low_stock_threshold",500))); self.e_thr.setMinimumHeight(38); self.e_thr.setMaximumWidth(150)
        row3.addWidget(self.e_thr)
        row3.addStretch()
        gl.addLayout(row3)

        save_gen = StyledButton("💾 Genel Ayarları Kaydet"); save_gen.clicked.connect(self._save_general)
        gl.addWidget(save_gen)
        self.gen_info = QLabel(""); self.gen_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        gl.addWidget(self.gen_info)
        cl.addWidget(gen_card)

        # Filament fiyatları
        cl.addWidget(SectionHeader("🧵 Filament Fiyatları (TL/kg)"))
        fil_card = CardFrame()
        fil_l = QVBoxLayout(fil_card)
        fil_l.setContentsMargins(20,16,20,16)
        info = QLabel("⚠️ Değişiklikler yalnızca yeni projeler için geçerlidir.")
        info.setStyleSheet(f"color: {SM.t('warning')}; border: none;")
        fil_l.addWidget(info)

        self.fil_entries = {}
        scroll2 = QScrollArea()
        scroll2.setWidgetResizable(True)
        scroll2.setFrameShape(QFrame.Shape.NoFrame)
        scroll2.setMaximumHeight(400)
        fw2 = QWidget()
        fgl = QGridLayout(fw2)
        fgl.setSpacing(4)
        for i, (fil, data) in enumerate(sorted(FILAMENT_DATA.items())):
            row = i // 2
            col = (i % 2) * 3
            lbl = QLabel(f"{fil}:"); lbl.setStyleSheet("border: none;")
            e = QLineEdit(); e.setText(str(data["fiyat"])); e.setMaximumWidth(100); e.setMinimumHeight(32)
            unit = QLabel("TL/kg"); unit.setStyleSheet(f"color: {SM.t('text_dim')}; border: none;")
            fgl.addWidget(lbl, row, col)
            fgl.addWidget(e, row, col+1)
            fgl.addWidget(unit, row, col+2)
            self.fil_entries[fil] = e
        scroll2.setWidget(fw2)
        fil_l.addWidget(scroll2)
        save_fil = StyledButton("💾 Fiyatları Güncelle"); save_fil.clicked.connect(self._save_fil_prices)
        fil_l.addWidget(save_fil)
        cl.addWidget(fil_card)

        # Şifre değiştir
        cl.addWidget(SectionHeader("🔐 Şifre Değiştir"))
        pw_card = CardFrame()
        pwl = QHBoxLayout(pw_card)
        pwl.setContentsMargins(20,16,20,16)
        self.pw_old = QLineEdit(); self.pw_old.setPlaceholderText("Mevcut şifre"); self.pw_old.setEchoMode(QLineEdit.EchoMode.Password); self.pw_old.setMinimumHeight(40)
        self.pw_new = QLineEdit(); self.pw_new.setPlaceholderText("Yeni şifre"); self.pw_new.setEchoMode(QLineEdit.EchoMode.Password); self.pw_new.setMinimumHeight(40)
        self.pw_new2= QLineEdit(); self.pw_new2.setPlaceholderText("Tekrar"); self.pw_new2.setEchoMode(QLineEdit.EchoMode.Password); self.pw_new2.setMinimumHeight(40)
        change_btn = StyledButton("Değiştir","success"); change_btn.clicked.connect(self._change_password)
        for w in [self.pw_old, self.pw_new, self.pw_new2, change_btn]:
            pwl.addWidget(w)
        self.pw_info = QLabel(""); self.pw_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        pwl.addWidget(self.pw_info)
        cl.addWidget(pw_card)

        # Yedek & veri
        cl.addWidget(SectionHeader("🗄️ Veri Yönetimi"))
        data_card = CardFrame()
        dl = QHBoxLayout(data_card)
        dl.setContentsMargins(20,16,20,16)
        for text, func, style in [
            ("💾 Yedek Al", self._do_backup, "primary"),
            ("📊 Özet Rapor", self._summary, "flat"),
            ("📥 Tüm CSV", self._export_all, "flat"),
            ("🗑 Tüm Projeler Sil", self._del_all, "danger"),
        ]:
            btn = StyledButton(text,style); btn.clicked.connect(func); dl.addWidget(btn)
        cl.addWidget(data_card)
        cl.addStretch()

    def _apply_theme(self):
        theme_name = self.cb_theme.currentText()
        SM.set_theme(theme_name)
        s = get_settings(); s["theme"] = theme_name; save_settings(s)
        app = QApplication.instance()
        app.setStyleSheet(SM.get_app_stylesheet())
        self.theme_changed.emit()
        QMessageBox.information(self, "Tema", f"'{theme_name}' teması uygulandı! Tam etki için yeniden başlatın.")

    def _save_general(self):
        try:
            s = get_settings()
            s["elektrik_fiyati"] = float(self.e_elec.text().replace(",","."))
            s["kdv_rate"] = float(self.e_kdv.text().replace(",","."))
            s["low_stock_threshold"] = float(self.e_thr.text().replace(",","."))
            save_settings(s)
            self.gen_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
            self.gen_info.setText("✓ Ayarlar kaydedildi.")
        except ValueError:
            self.gen_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.gen_info.setText("✗ Geçerli sayı gir.")

    def _save_fil_prices(self):
        count = 0
        for fil, e in self.fil_entries.items():
            try:
                v = float(e.text().replace(",","."))
                if v > 0: FILAMENT_DATA[fil]["fiyat"] = v; count += 1
            except: pass
        QMessageBox.information(self, "Fiyatlar", f"{count} filament fiyatı güncellendi (bu oturum için).")

    def _change_password(self):
        old = self.pw_old.text().strip()
        new = self.pw_new.text().strip()
        new2= self.pw_new2.text().strip()
        if not old or not new:
            self.pw_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.pw_info.setText("✗ Alanlar boş."); return
        if len(new)<4:
            self.pw_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.pw_info.setText("✗ Min. 4 karakter."); return
        if new != new2:
            self.pw_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.pw_info.setText("✗ Eşleşmiyor."); return
        users = load_users()
        changed = False
        for u in users:
            if u["username"] == self.user and u.get("password_hash") == hash_password(old):
                u["password_hash"] = hash_password(new); changed = True; break
        if not changed:
            self.pw_info.setStyleSheet(f"color: {SM.t('danger')}; border: none;")
            self.pw_info.setText("✗ Mevcut şifre yanlış."); return
        save_users(users)
        self.pw_info.setStyleSheet(f"color: {SM.t('success')}; border: none;")
        self.pw_info.setText("✓ Şifre güncellendi.")
        for e in [self.pw_old,self.pw_new,self.pw_new2]: e.clear()

    def _do_backup(self):
        do_backup()
        QMessageBox.information(self,"Yedek","Yedek alındı:\n"+str(BACKUP_DIR))

    def _summary(self):
        projects  = u_load(PROJECTS_FILE, self.user)
        sales     = u_load(SALES_FILE, self.user)
        expenses  = u_load(EXPENSES_FILE, self.user)
        customers = u_load(CUSTOMERS_FILE, self.user)
        stock     = load_json(STOCK_FILE, {})
        t_mal = sum(p.get("toplam_maliyet",0) for p in projects)
        t_sat = sum(s.get("satis_fiyati",0) for s in sales)
        t_gid = sum(e.get("tutar",0) for e in expenses)
        net   = t_sat - t_mal - t_gid
        t_stk = sum(stock.values())
        report = (
            "╔" + "═"*43 + "╗\n"
            f"║   ATÖLYE ÖZET RAPORU  —  {self.user:<15}║\n"
            f"║   {datetime.now().strftime('%d.%m.%Y %H:%M'):<38}║\n"
            "╠" + "═"*43 + "╣\n"
            f"║  Toplam Proje     : {len(projects):<23}║\n"
            f"║  Proje Maliyeti   : {t_mal:>10,.2f} TL{'':<10}║\n"
            f"║  Toplam Satış     : {t_sat:>10,.2f} TL{'':<10}║\n"
            f"║  Toplam Gider     : {t_gid:>10,.2f} TL{'':<10}║\n"
            f"║  NET KAR / ZARAR  : {net:>10,.2f} TL{'':<10}║\n"
            "╠" + "═"*43 + "╣\n"
            f"║  Müşteri Sayısı   : {len(customers):<23}║\n"
            f"║  Satış Sayısı     : {len(sales):<23}║\n"
            f"║  Toplam Stok      : {t_stk:>10,.0f} g{'':<12}║\n"
            "╚" + "═"*43 + "╝\n"
        )
        dlg = QDialog(self)
        dlg.setWindowTitle("Özet Rapor")
        dlg.setMinimumSize(520,400)
        dlg.setStyleSheet(f"background: {SM.t('bg')}; color: {SM.t('text')};")
        l = QVBoxLayout(dlg)
        te = QTextEdit(); te.setReadOnly(True); te.setPlainText(report)
        te.setFont(QFont("Courier New",12))
        te.setStyleSheet(f"background: {SM.t('input_bg')}; color: {SM.t('text')}; border: 1px solid {SM.t('border')};")
        l.addWidget(te)
        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        bb.rejected.connect(dlg.reject)
        l.addWidget(bb)
        dlg.exec()

    def _export_all(self):
        path, _ = QFileDialog.getSaveFileName(self,"CSV Kaydet",f"tum_veri_{datetime.now().strftime('%Y%m%d')}.csv","CSV (*.csv)")
        if not path: return
        projects = u_load(PROJECTS_FILE, self.user)
        sales    = u_load(SALES_FILE, self.user)
        with open(path,"w",encoding="utf-8-sig",newline="") as f:
            w = csv.writer(f)
            w.writerow(["=== PROJELER ==="])
            w.writerow(["Model","Kategori","Filament","Gram","Süre","Maliyet","Durum","Tarih"])
            for p in projects:
                w.writerow([p.get("model_adi",""),p.get("kategori",""),p.get("filament_turu",""),p.get("gram",0),p.get("sure",0),p.get("toplam_maliyet",0),p.get("durum",""),p.get("tarih","")])
            w.writerow([]); w.writerow(["=== SATIŞLAR ==="])
            w.writerow(["Ürün","Müşteri","Fiyat","Adet","Kar","Tarih"])
            for s in sales:
                w.writerow([s.get("urun",""),s.get("musteri",""),s.get("satis_fiyati",0),s.get("adet",1),s.get("kar",0),s.get("tarih","")])
        QMessageBox.information(self,"CSV",f"Kaydedildi:\n{path}")

    def _del_all(self):
        if QMessageBox.question(self,"DİKKAT!","Tüm projeler silinsin mi?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            u_save(PROJECTS_FILE, self.user, [])
            QMessageBox.information(self,"Başarılı","Tüm projeler silindi.")

    def refresh(self): pass

# ═══════════════════════════════════════════════════════════════
#  ANA PENCERE
# ═══════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Baskı Atölye PRO  ·  v4.0  ·  PyQt6")
        self.setMinimumSize(1380, 820)
        self.current_user = None

        # Ayarlardan tema yükle
        settings = get_settings()
        SM.set_theme(settings.get("theme","🌑 Karanlık"))
        QApplication.instance().setStyleSheet(SM.get_app_stylesheet())

        self.central = QStackedWidget()
        self.setCentralWidget(self.central)

        # Auth sayfası
        self.auth_page = AuthPage()
        self.auth_page.login_success.connect(self._on_login)
        self.central.addWidget(self.auth_page)
        self.central.setCurrentWidget(self.auth_page)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("3D Baskı Atölye PRO v4.0  ·  PyQt6 Edition")

        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._auto_refresh)
        self.refresh_timer.start(30000)  # 30 sn

    def _on_login(self, username):
        self.current_user = username
        self._build_dashboard()

    def _build_dashboard(self):
        # Dashboard widget
        dash = QWidget()
        dash_layout = QHBoxLayout(dash)
        dash_layout.setContentsMargins(0,0,0,0)
        dash_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setProperty("class","sidebar")
        sidebar.setFixedWidth(230)
        sidebar.setStyleSheet(f"QFrame {{ background: {SM.t('sidebar')}; border-right: 1px solid {SM.t('border')}; }}")
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(10,20,10,16)
        sb_layout.setSpacing(2)

        # Logo
        logo_bar = QFrame()
        logo_bar.setFixedHeight(4)
        logo_bar.setStyleSheet(f"background: {SM.t('accent')}; border-radius: 2px;")
        sb_layout.addWidget(logo_bar)

        logo = QLabel("3D ATÖLYE")
        logo.setFont(QFont("Courier New",18,QFont.Weight.Bold))
        logo.setStyleSheet(f"color: {SM.t('accent')}; border: none; padding: 8px 0;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb_layout.addWidget(logo)

        pro_lbl = QLabel("PRO v4.0  ·  PyQt6")
        pro_lbl.setFont(QFont("Courier New",9))
        pro_lbl.setStyleSheet(f"color: {SM.t('accent2')}; border: none;")
        pro_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb_layout.addWidget(pro_lbl)
        sb_layout.addSpacing(8)

        # Kullanıcı
        user_frame = QFrame()
        user_frame.setStyleSheet(f"QFrame {{ background: {SM.t('input_bg')}; border-radius: 10px; }}")
        ufl = QVBoxLayout(user_frame)
        ufl.setContentsMargins(12,10,12,10)
        user_icon = QLabel("👤")
        user_icon.setFont(QFont("Segoe UI Emoji",24))
        user_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_name = QLabel(self.current_user)
        user_name.setFont(QFont("Courier New",12,QFont.Weight.Bold))
        user_name.setStyleSheet(f"color: {SM.t('accent')}; border: none;")
        user_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_role = QLabel("Atölye Sahibi")
        user_role.setStyleSheet(f"color: {SM.t('text_dim')}; font-size: 11px; border: none;")
        user_role.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ufl.addWidget(user_icon); ufl.addWidget(user_name); ufl.addWidget(user_role)
        sb_layout.addWidget(user_frame)
        sb_layout.addSpacing(12)

        # Nav butonları
        self.nav_btns = {}
        nav_items = [
            ("📊", "Dashboard"),
            ("📦", "Stok Takibi"),
            ("🖨️", "Projeler"),
            ("💰", "Satış"),
            ("📈", "Finans"),
            ("👥", "Müşteriler"),
            ("✅", "Görevler"),
            ("🔧", "Bakımlar"),
            ("📝", "Notlar"),
            ("📉", "İstatistikler"),
            ("📋", "Aktivite Logu"),
            ("⚙️", "Ayarlar"),
        ]
        self.nav_group = []
        for icon, label in nav_items:
            btn = NavButton(icon, label)
            btn.clicked.connect(lambda checked, lbl=label: self._nav_click(lbl))
            sb_layout.addWidget(btn)
            self.nav_btns[label] = btn
            self.nav_group.append(btn)

        sb_layout.addStretch()

        # Çıkış
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setStyleSheet(f"color: {SM.t('border')};")
        sb_layout.addWidget(sep)
        logout_btn = StyledButton(" 🚪  Çıkış Yap","danger")
        logout_btn.clicked.connect(self._logout)
        sb_layout.addWidget(logout_btn)

        dash_layout.addWidget(sidebar)

        # Ana içerik
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"background: {SM.t('bg')};")
        dash_layout.addWidget(self.content_stack)

        # Sayfalar oluştur
        self.pages = {}
        page_classes = {
            "Dashboard":     DashboardPage,
            "Stok Takibi":   StockPage,
            "Projeler":      ProjectsPage,
            "Satış":         SalesPage,
            "Finans":        FinancePage,
            "Müşteriler":    CustomersPage,
            "Görevler":      TasksPage,
            "Bakımlar":      MaintenancePage,
            "Notlar":        NotesPage,
            "İstatistikler": StatsPage,
            "Aktivite Logu": LogPage,
            "Ayarlar":       SettingsPage,
        }
        for label, cls in page_classes.items():
            page = cls(self.current_user)
            if hasattr(page, "theme_changed"):
                page.theme_changed.connect(self._on_theme_changed)
            self.pages[label] = page
            self.content_stack.addWidget(page)

        self.central.addWidget(dash)
        self.central.setCurrentWidget(dash)
        self._nav_click("Dashboard")

        # Status güncelle
        self.status.showMessage(f"Hoş geldin {self.current_user}!  |  3D Baskı Atölye PRO v4.0")

    def _nav_click(self, label):
        for name, btn in self.nav_btns.items():
            btn.setChecked(name == label)
        if label in self.pages:
            self.content_stack.setCurrentWidget(self.pages[label])

    def _auto_refresh(self):
        if self.current_user and hasattr(self,"pages"):
            current = self.content_stack.currentWidget()
            if hasattr(current,"refresh"):
                try: current.refresh()
                except: pass

    def _logout(self):
        self.current_user = None
        self.central.setCurrentWidget(self.auth_page)
        self.auth_page.login_user.clear()
        self.auth_page.login_pass.clear()
        self.status.showMessage("Çıkış yapıldı.")

    def _on_theme_changed(self):
        self.content_stack.setStyleSheet(f"background: {SM.t('bg')};")

# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("3D Baskı Atölye PRO")
    app.setApplicationVersion("4.0")

    # Başlangıç teması
    settings = get_settings()
    SM.set_theme(settings.get("theme","🌑 Karanlık"))
    app.setStyleSheet(SM.get_app_stylesheet())

    # Örnek stok yükle (ilk çalıştırma)
    if not Path(STOCK_FILE).exists():
        stock = {fil: 0 for fil in FILAMENT_DATA}
        stock["Bambu PLA"] = 1000
        stock["eSUN PETG"] = 750
        stock["Sunlu PLA+"] = 500
        save_json(STOCK_FILE, stock)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()