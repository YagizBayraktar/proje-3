"""
╔══════════════════════════════════════════════════════════════╗
║             3D BASKI ATÖLYE YÖNETİM SİSTEMİ  —               ║
║                  Yağız BAYRAKTAR                             ║
╚══════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
from tkinter import messagebox, colorchooser
import json, os, csv, io
from datetime import datetime, timedelta
import tkinter as tk
import math, random

# ══════════════════════════════════════════════════════════════
#  TEMA & RENK SİSTEMİ
# ══════════════════════════════════════════════════════════════

ACCENT      = "#00D4FF"   # parlak cyan
ACCENT2     = "#7B2FFF"   # derin mor
SUCCESS     = "#00E676"   # neon yeşil
DANGER      = "#FF1744"   # canlı kırmızı
WARNING     = "#FFD600"   # altın sarı
BG_DARK     = "#0D0F14"   # tam siyah-lacivert
BG_CARD     = "#161B22"   # kart zemin
BG_SIDEBAR  = "#0F1117"   # sidebar
BORDER      = "#21262D"   # ince çerçeve

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ══════════════════════════════════════════════════════════════
#  DOSYALAR
# ══════════════════════════════════════════════════════════════

USERS_FILE     = "users.json"
PROJECTS_FILE  = "projects.json"
SETTINGS_FILE  = "ayarlar.json"
STOCK_FILE     = "stock.json"
SALES_FILE     = "sales.json"
EXPENSES_FILE  = "expenses.json"
CUSTOMERS_FILE = "customers.json"
TASKS_FILE     = "tasks.json"
NOTES_FILE     = "notes.json"
LOG_FILE       = "activity_log.json"

# ══════════════════════════════════════════════════════════════
#  VERİ KATALOĞları
# ══════════════════════════════════════════════════════════════

FILAMENT_FIYATLAR = {
    # ───────── PLA ─────────
    "eSUN_PLA": 650,
    "Sunlu_PLA": 600,
    "Polymaker_PLA": 900,
    "Bambu_PLA": 1200,
    "Creality_PLA": 750,
    "Anycubic_PLA": 700,
    "Elegoo_PLA": 680,
    "Flashforge_PLA": 800,
    "Prusa_PLA": 1300,

    # ───────── PLA+ ─────────
    "eSUN_PLA_PLUS": 800,
    "Sunlu_PLA_PLUS": 750,
    "Polymaker_PLA_PLUS": 1000,
    "Bambu_PLA_PLUS": 1350,
    "Creality_PLA_PLUS": 850,
    "Anycubic_PLA_PLUS": 800,
    "Elegoo_PLA_PLUS": 780,

    # ───────── PETG ─────────
    "eSUN_PETG": 900,
    "Sunlu_PETG": 850,
    "Polymaker_PETG": 1200,
    "Bambu_PETG": 1300,
    "Creality_PETG": 950,
    "Anycubic_PETG": 900,
    "Elegoo_PETG": 850,

    # ───────── ABS ─────────
    "eSUN_ABS": 800,
    "Sunlu_ABS": 780,
    "Polymaker_ABS": 1100,
    "Bambu_ABS": 1200,
    "Creality_ABS": 850,
    "Anycubic_ABS": 800,

    # ───────── ASA ─────────
    "eSUN_ASA": 1100,
    "Sunlu_ASA": 1050,
    "Polymaker_ASA": 1400,
    "Bambu_ASA": 1500,
    "Creality_ASA": 1200,

    # ───────── TPU (esnek) ─────────
    "eSUN_TPU": 1200,
    "Sunlu_TPU": 1100,
    "Polymaker_TPU": 1600,
    "Bambu_TPU": 1700,
    "Creality_TPU": 1300,
    "Anycubic_TPU": 1200,

    # ───────── NYLON / PC ─────────
    "eSUN_NYLON": 1700,
    "Sunlu_NYLON": 1600,
    "Polymaker_NYLON": 2400,
    "Bambu_NYLON": 2600,
    "Creality_NYLON": 1800,

    "eSUN_PC": 2200,
    "Sunlu_PC": 2100,
    "Polymaker_PC": 3000,
    "Bambu_PC": 3200,

    # ───────── ÖZEL ─────────
    "eSUN_PVA": 1600,
    "Sunlu_PVA": 1500,

    "eSUN_WOOD": 1100,
    "Sunlu_WOOD": 1050,

    "eSUN_SILK_PLA": 950,
    "Sunlu_SILK_PLA": 900,

    "eSUN_CARBON_FIBER_PLA": 1600,
    "Polymaker_CARBON_FIBER": 2000,
    "eSUN_CARBON_FIBER_NYLON": 2800
}

YAZICI_KATALOGU = {
    "Bambu Lab": {
        "A1": 150,
        "A1 Mini": 130,
        "P1S": 180,
        "P1P": 170,
        "X1 Carbon": 220,
        "X1E": 230,
        "A1 Mini": 150,
        "A1": 300,
        "P1P": 350,
        "P1S": 350,
        "X1 Carbon": 500,
        "X1E": 550,
        "H2D": 800,
        "A1 Mini": 150,
        "A1": 300,   # ısınma anı pik, çalışma 100–250W

        "P1P": 1000,  # heatbed spike ~900-1000W
        "P1S": 1000,  # çalışma ~80–250W

        "X1 Carbon": 1000,
        "X1E": 1400,

        "H2D": 2200,  # yeni nesil büyük ısıtma sistemi (en yüksek Bambu)

        "H2S": 2000,
        "P2S": 1000
    },
    "Creality": {
        "Ender 3 V3 SE": 120,
        "Ender 3 V3 KE": 130,
        "Ender 3 S1": 120,
        "K1": 200,
        "K1C": 220,
        "K1 Max": 250,
        "Ender 2 Pro": 70,
        "Ender 3": 270,
        "Ender 3 Pro": 270,
        "Ender 3 V2": 270,
        "Ender 3 V2 Neo": 270,
        "Ender 3 S1": 350,
        "Ender 3 S1 Pro": 350,
        "Ender 3 S1 Plus": 350,
        "Ender 3 V3 SE": 350,
        "Ender 3 V3 KE": 350,
        "Ender 3 V3 Plus": 400,
        "Ender 5": 350,
        "Ender 5 Pro": 350,
        "Ender 5 Plus": 500,
        "CR-6 SE": 350,
        "CR-10": 360,
        "CR-10 V2": 360,
        "CR-10 V3": 360,
        "CR-10 Smart": 400,
        "CR-10 S5": 500,
        "CR-10 Max": 600,
        "K1": 350,
        "K1C": 350,
        "K1 Max": 1000,
        "K2 Plus": 1000,
        "K2 Max": 1200,
        "Sermoon D1": 350,
        "Sermoon V1": 200,
    },
    "Anycubic": {
        "Kobra 2 Neo": 130,
        "Kobra 2 Pro": 150,
        "Kobra 2 Max": 180,
        "Kobra 3": 200,
        "Kobra 2": 250,
        "Kobra 2 Neo": 250,
        "Kobra 2 Pro": 300,
        "Kobra 2 Plus": 400,
        "Kobra 2 Max": 500,
        "Kobra 3": 300,
        "Kobra 3 V2": 350,
        "Kobra 3 Combo": 350,
        "Kobra 3 Max": 450,
        "Kobra 3 S1": 700,
        "Kobra 3 S1 Max": 800,
        "Kobra S1": 1000,
        "Kobra S1 Max": 1200,
        "Kobra Go": 200,
        "Kobra": 250,
        "Mega S": 300,
        "Mega X": 400,
        "i3 Mega": 250,
        "Vyper": 350,
        "Photon (resin)": 40,
        "Photon Mono": 50,
        "Photon Mono 4K": 50,
        "Photon Mono X": 120,
        "Photon Mono M3": 140,
        "Photon M3 Plus": 144,
        "Photon Mono 4 Ultra": 160,
    },
    "ELEGOO": {
        "Neptune 4": 140,
        "Neptune 4 Pro": 150,
        "Neptune 4 Plus": 170,
        "Neptune 4 Max": 190,
        "Mars": 60,
        "Mars 2": 60,
        "Mars 2 Pro": 60,
        "Mars 3": 60,
        "Mars 3 Pro": 60,
        "Mars 4": 70,
        "Mars 4 Ultra": 80,
        "Mars 5": 80,
        "Mars 5 Ultra": 90,
        "Saturn": 120,
        "Saturn 2": 130,
        "Saturn 3": 140,
        "Saturn 3 Ultra": 150,
        "Saturn 4": 160,
        "Saturn 4 Ultra": 170,
        "Jupiter": 200,
        "Jupiter SE": 220,
        "Jupiter 6K": 250,
        "Jupiter 12K": 260,
        "Neptune 2": 150,
        "Neptune 2S": 150,
        "Neptune 3": 180,
        "Neptune 3 Pro": 220,
        "Neptune 3 Plus": 350,
        "Neptune 3 Max": 450,
        "Neptune 4": 300,
        "Neptune 4 Pro": 350,
        "Neptune 4 Plus": 400,
        "Neptune 4 Max": 500,
    },
    "Prusa": {
        "MK4S": 170,
        "XL": 280,
        "MINI+": 120,
        "Original Prusa MINI+": 120,
        "Original Prusa MINI": 120,
        "Original Prusa i3 MK3S+": 160,
        "Original Prusa i3 MK3S": 160,
        "Original Prusa MK4": 180,
        "Original Prusa MK4S": 180,
        "Original Prusa XL (tek kafalı)": 800,
        "Original Prusa XL (çok kafalı / tam yük)": 1000,
        "Prusa SL1": 150,
        "Prusa SL1S SPEED": 150,
        "Prusa CW1": 150,
        "Prusa CW1S": 150,
    },
    "Flashforge": {
        "Adventurer 5M": 180,
        "Adventurer 5M Pro": 200,
        "Adventurer 4": 190,
        "Adventurer 5M": 350,
        "Adventurer 5M Pro": 350,
        "Adventurer 4": 500,
        "Adventurer 3": 150,
        "Adventurer 3 Pro": 150,
        "Adventurer 3 Pro 2": 150,
        "Adventurer 3 Lite": 150,
        "Adventurer 3C": 150,
        "Adventurer 2": 60,
        "Adventurer 2 Lite": 60,
        "Finder": 100,
        "Finder 2.0": 100,
        "Creator Pro 2": 350,
        "Creator 3": 300,
        "Creator 3 Pro": 350,
        "Creator 4": 800,
        "Dreamer": 250,
        "Dreamer NX": 250,
        "Guider 2": 500,
        "Guider 2S": 600,
        "Guider 3": 650,
        "Guider 3 Ultra": 750,
    }
}

KAR_MARJI_ONERILERI = {
    "Düşük  (%20)": 0.20,
    "Normal (%40)": 0.40,
    "Yüksek (%60)": 0.60,
    "Premium(%80)": 0.80,
}

# ══════════════════════════════════════════════════════════════
#  YARDIMCI FONKSİYONLAR
# ══════════════════════════════════════════════════════════════

def ensure_file(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=2)

def load_json(path, default):
    ensure_file(path, default)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_stock():
    ensure_file(STOCK_FILE, {f: 0 for f in FILAMENT_FIYATLAR})
    return load_json(STOCK_FILE, {f: 0 for f in FILAMENT_FIYATLAR})

def save_stock(data): save_json(STOCK_FILE, data)

def adjust_stock(old_fil, old_g, new_fil, new_g):
    s = load_stock()
    s[old_fil] = s.get(old_fil, 0) + old_g
    if s.get(new_fil, 0) < new_g:
        return False
    s[new_fil] -= new_g
    save_stock(s)
    return True

def get_electric_price():
    return float(load_json(SETTINGS_FILE, {"elektrik_fiyati": 1.73}).get("elektrik_fiyati", 1.73))

def set_electric_price(p):
    s = load_json(SETTINGS_FILE, {"elektrik_fiyati": 1.73})
    s["elektrik_fiyati"] = p
    save_json(SETTINGS_FILE, s)

def get_low_stock_threshold():
    return float(load_json(SETTINGS_FILE, {"low_stock_threshold": 500}).get("low_stock_threshold", 500))

def set_low_stock_threshold(v):
    s = load_json(SETTINGS_FILE, {"elektrik_fiyati": 1.73})
    s["low_stock_threshold"] = v
    save_json(SETTINGS_FILE, s)

def toplam_maliyet_hesapla(gram, filament, saat, marka, model):
    filament = filament.upper()
    kg_fiyat  = FILAMENT_FIYATLAR.get(filament, 500)
    f_mal     = (gram / 1000) * kg_fiyat
    watt      = YAZICI_KATALOGU.get(marka, {}).get(model, 150)
    e_tuk     = (watt / 1000) * saat
    e_mal     = e_tuk * get_electric_price()
    toplam    = f_mal + e_mal
    return round(toplam,2), round(f_mal,2), round(e_mal,2), watt, round(e_tuk,3)

# ── kullanıcı bazlı veri ──────────────────────────────────────
def u_load(file, user, default=[]):
    return [x for x in load_json(file, default) if x.get("owner") == user]

def u_save(file, user, items):
    all_data = load_json(file, [])
    others   = [x for x in all_data if x.get("owner") != user]
    save_json(file, others + items)

# ── aktivite logu ─────────────────────────────────────────────
def log_activity(user, action, detail=""):
    logs = load_json(LOG_FILE, [])
    logs.append({
        "owner": user, "action": action, "detail": detail,
        "tarih": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    })
    if len(logs) > 500:
        logs = logs[-500:]
    save_json(LOG_FILE, logs)

def load_logs(user):
    return [l for l in load_json(LOG_FILE, []) if l.get("owner") == user]

# ══════════════════════════════════════════════════════════════
#  UI YARDIMCILARI
# ══════════════════════════════════════════════════════════════

def make_card(parent, **kwargs):
    return ctk.CTkFrame(parent, corner_radius=16,
                        fg_color=BG_CARD, border_width=1,
                        border_color=BORDER, **kwargs)

def section_label(parent, text, size=18):
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(fill="x", padx=0, pady=(14, 6))
    ctk.CTkLabel(f, text=text,
                 font=ctk.CTkFont(family="Courier", size=size, weight="bold"),
                 text_color=ACCENT).pack(side="left")
    ctk.CTkFrame(f, height=2, fg_color=ACCENT).pack(
        side="left", fill="x", expand=True, padx=(10, 0), pady=10)
    return f

def accent_btn(parent, text, cmd, color=ACCENT2, hover="#5a1fd1", **kw):
    return ctk.CTkButton(
        parent, text=text, command=cmd,
        fg_color=color, hover_color=hover,
        corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"), **kw)

def danger_btn(parent, text, cmd, **kw):
    return accent_btn(parent, text, cmd, color=DANGER, hover="#c62828", **kw)

def success_btn(parent, text, cmd, **kw):
    return accent_btn(parent, text, cmd, color="#00695c", hover="#00897b", **kw)

def mini_entry(parent, ph, width=300, **kw):
    return ctk.CTkEntry(parent, placeholder_text=ph, width=width, height=38,
                        corner_radius=10, border_color=BORDER,
                        fg_color="#1C2333", **kw)

def mini_combo(parent, values, width=300, **kw):
    return ctk.CTkComboBox(parent, values=values, width=width, height=38,
                           corner_radius=10, border_color=BORDER,
                           fg_color="#1C2333", **kw)

# ══════════════════════════════════════════════════════════════
#  GELİŞMİŞ CANVAS GRAFİKLERİ
# ══════════════════════════════════════════════════════════════

class MiniBarChart(tk.Canvas):
    """Basit canvas çubuk grafiği."""
    def __init__(self, parent, data: dict, color=ACCENT, height=120, **kw):
        super().__init__(parent, height=height, bg=BG_CARD,
                         highlightthickness=0, **kw)
        self.pack(fill="x", padx=4, pady=4)
        self._draw(data, color, height)

    def _draw(self, data, color, h):
        self.update_idletasks()
        w   = self.winfo_reqwidth() or 400
        if not data: return
        vals = list(data.values())
        keys = list(data.keys())
        mx   = max(vals) if max(vals) > 0 else 1
        n    = len(vals)
        pad  = 10
        bar_w= (w - 2*pad) / n
        for i,(k,v) in enumerate(zip(keys,vals)):
            x0 = pad + i * bar_w + bar_w*0.1
            x1 = pad + i * bar_w + bar_w*0.9
            bh = int((v/mx) * (h-30))
            y0 = h - 20 - bh
            y1 = h - 20
            self.create_rectangle(x0, y0, x1, y1, fill=color, outline="",
                                  tags="bar")
            self.create_text((x0+x1)/2, h-10, text=k[:6],
                             fill="#aaa", font=("Courier",7))
            if bh > 14:
                self.create_text((x0+x1)/2, y0+4,
                                 text=f"{v:.0f}", fill="white",
                                 font=("Courier",7), anchor="n")


class DonutChart(tk.Canvas):
    """Basit donut (halka) grafiği."""
    COLORS = ["#00D4FF","#7B2FFF","#00E676","#FFD600","#FF1744",
              "#FF6D00","#40C4FF","#EA80FC","#B9F6CA","#FFD180"]

    def __init__(self, parent, data: dict, size=160, **kw):
        super().__init__(parent, width=size, height=size,
                         bg=BG_CARD, highlightthickness=0, **kw)
        self._draw(data, size)

    def _draw(self, data, size):
        if not data or sum(data.values()) == 0:
            return
        total  = sum(data.values())
        cx, cy = size/2, size/2
        r_out  = size/2 - 8
        r_in   = r_out * 0.55
        start  = -90
        for i, (k, v) in enumerate(data.items()):
            if v <= 0: continue
            extent = (v/total) * 360
            color  = self.COLORS[i % len(self.COLORS)]
            self.create_arc(cx-r_out, cy-r_out, cx+r_out, cy+r_out,
                            start=start, extent=extent,
                            fill=color, outline=BG_CARD, width=2)
            start += extent
        # ortayı kapat (donut deliği)
        self.create_oval(cx-r_in, cy-r_in, cx+r_in, cy+r_in,
                         fill=BG_CARD, outline=BG_CARD)
        self.create_text(cx, cy, text=f"{total:.0f}", fill="white",
                         font=("Courier",11,"bold"))


# ══════════════════════════════════════════════════════════════
#  ANA UYGULAMA
# ══════════════════════════════════════════════════════════════

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("3D Baskı Atölye PRO  ·  v3.0")
        self.geometry("1440x860")
        self.minsize(1280, 720)
        self.configure(fg_color=BG_DARK)

        for f in [USERS_FILE, PROJECTS_FILE, SETTINGS_FILE,
                  STOCK_FILE, SALES_FILE, EXPENSES_FILE,
                  CUSTOMERS_FILE, TASKS_FILE, NOTES_FILE, LOG_FILE]:
            default = [] if f not in [SETTINGS_FILE, STOCK_FILE] else (
                {"elektrik_fiyati":1.73, "low_stock_threshold":500}
                if f == SETTINGS_FILE else {k:0 for k in FILAMENT_FIYATLAR})
            ensure_file(f, default)

        self.current_user = None
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.after(100, self.show_auth_page)

    def clear_container(self):
        for w in self.container.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════
    #  AUTH SAYFASI
    # ══════════════════════════════════════════════════════════

    def show_auth_page(self):
        self.clear_container()
        root = ctk.CTkFrame(self.container, fg_color="transparent")
        root.pack(fill="both", expand=True, padx=40, pady=40)

        # Sol panel — tanıtım
        left = ctk.CTkFrame(root, corner_radius=24, fg_color=BG_CARD,
                            border_width=1, border_color=BORDER)
        left.pack(side="left", fill="both", expand=True, padx=(0,20))

        # dekoratif çizgi
        ctk.CTkFrame(left, height=4, fg_color=ACCENT,
                     corner_radius=2).pack(fill="x", padx=30, pady=(30,0))

        ctk.CTkLabel(left, text="3D BASKI\nATÖLYE PRO",
                     font=ctk.CTkFont(family="Courier", size=40, weight="bold"),
                     text_color=ACCENT).pack(anchor="w", padx=30, pady=(20,4))

        ctk.CTkLabel(left,
            text="Profesyonel üretim yönetimi, filament takibi,\n"
                 "satış & kar analizi tek platformda. By YAĞIZ BAYRAKTAR",
            font=ctk.CTkFont(size=15), text_color="#8B949E").pack(anchor="w", padx=30)

        badges = ctk.CTkFrame(left, fg_color="transparent")
        badges.pack(anchor="w", padx=30, pady=20)
        for txt, col in [("● Stok Takibi", ACCENT),("● Satış & Kar", SUCCESS),
                         ("● Müşteri CRM", ACCENT2),("● Raporlama", WARNING)]:
            ctk.CTkLabel(badges, text=txt,
                         font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
                         text_color=col).pack(side="left", padx=8)

        features = [
            "📦  Filament stok & değer analizi",
            "💰  Satış kaydı, müşteri & ödeme takibi",
            "📈  Gelir/gider ve net kar hesabı",
            "👥  Müşteri CRM ve alışveriş geçmişi",
            "✅  Görev listesi & atölye notları",
            "📊  Canlı grafikler ve istatistikler",
            "🔔  Düşük stok uyarısı sistemi",
            "📋  CSV dışa aktarma",
            "🔢  Akıllı fiyat hesaplama & kar marjı",
            "📅  Aktivite & işlem logu",
        ]
        for f in features:
            ctk.CTkLabel(left, text=f,
                         font=ctk.CTkFont(size=13), text_color="#C9D1D9",
                         anchor="w").pack(anchor="w", padx=30, pady=2)

        ctk.CTkLabel(left, text="v3.0 PRO  —  2025",
                     font=ctk.CTkFont(family="Courier", size=11),
                     text_color="#30363D").pack(side="bottom", pady=16)

        # Sağ panel — giriş / kayıt
        right = ctk.CTkFrame(root, corner_radius=24, fg_color=BG_CARD,
                             border_width=1, border_color=BORDER, width=420)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tabs = ctk.CTkTabview(right, fg_color="transparent",
                              segmented_button_fg_color="#1C2333",
                              segmented_button_selected_color=ACCENT2,
                              segmented_button_selected_hover_color="#5a1fd1")
        tabs.pack(padx=20, pady=20, fill="both", expand=True)

        lt = tabs.add("  Giriş Yap  ")
        rt = tabs.add("  Kayıt Ol  ")

        # — Giriş
        ctk.CTkLabel(lt, text="HOŞ GELDİN",
                     font=ctk.CTkFont(family="Courier", size=26, weight="bold"),
                     text_color=ACCENT).pack(pady=(30,4))
        ctk.CTkLabel(lt, text="Hesabına giriş yap",
                     text_color="#8B949E").pack(pady=(0,20))
        self.login_username = mini_entry(lt, "Kullanıcı adı")
        self.login_username.pack(pady=8)
        self.login_password = mini_entry(lt, "Şifre", show="*")
        self.login_password.pack(pady=8)
        self.login_password.bind("<Return>", lambda e: self.login())
        accent_btn(lt, "  GİRİŞ YAP  →", self.login, height=44).pack(pady=20)
        self.login_info = ctk.CTkLabel(lt, text="", text_color=DANGER,
                                       font=ctk.CTkFont(size=12))
        self.login_info.pack()

        # — Kayıt
        ctk.CTkLabel(rt, text="HESAP OLUŞTUR",
                     font=ctk.CTkFont(family="Courier", size=24, weight="bold"),
                     text_color=ACCENT).pack(pady=(30,4))
        ctk.CTkLabel(rt, text="Ücretsiz kayıt ol",
                     text_color="#8B949E").pack(pady=(0,20))
        self.reg_username  = mini_entry(rt, "Kullanıcı adı")
        self.reg_username.pack(pady=8)
        self.reg_password  = mini_entry(rt, "Şifre", show="*")
        self.reg_password.pack(pady=8)
        self.reg_password2 = mini_entry(rt, "Şifre tekrar", show="*")
        self.reg_password2.pack(pady=8)
        accent_btn(rt, "  KAYIT OL  →", self.register, height=44).pack(pady=20)
        self.reg_info = ctk.CTkLabel(rt, text="", font=ctk.CTkFont(size=12))
        self.reg_info.pack()

    def login(self):
        u, p = self.login_username.get().strip(), self.login_password.get().strip()
        for user in load_json(USERS_FILE, []):
            if user["username"] == u and user["password"] == p:
                self.current_user = u
                log_activity(u, "GİRİŞ", "Sisteme giriş yapıldı.")
                self.show_dashboard()
                return
        self.login_info.configure(text="✗  Kullanıcı adı veya şifre hatalı.")

    def register(self):
        u  = self.reg_username.get().strip()
        p  = self.reg_password.get().strip()
        p2 = self.reg_password2.get().strip()
        if len(u) < 3:
            self.reg_info.configure(text="✗  En az 3 karakter.", text_color=DANGER); return
        if len(p) < 4:
            self.reg_info.configure(text="✗  En az 4 karakter şifre.", text_color=DANGER); return
        if p != p2:
            self.reg_info.configure(text="✗  Şifreler eşleşmiyor.", text_color=DANGER); return
        users = load_json(USERS_FILE, [])
        if any(x["username"] == u for x in users):
            self.reg_info.configure(text="✗  Bu kullanıcı adı alınmış.", text_color=DANGER); return
        users.append({"username":u,"password":p,
                      "created_at":datetime.now().strftime("%d.%m.%Y %H:%M")})
        save_json(USERS_FILE, users)
        self.reg_info.configure(text="✓  Kayıt başarılı! Giriş yapabilirsin.",
                                text_color=SUCCESS)
        for e in [self.reg_username, self.reg_password, self.reg_password2]:
            e.delete(0,"end")

    # ══════════════════════════════════════════════════════════
    #  DASHBOARD KABUK
    # ══════════════════════════════════════════════════════════

    def get_all_projects(self):
        return u_load(PROJECTS_FILE, self.current_user)

    def save_user_projects(self, projects):
        u_save(PROJECTS_FILE, self.current_user, projects)

    def show_dashboard(self):
        self.clear_container()

        outer = ctk.CTkFrame(self.container, fg_color="transparent")
        outer.pack(fill="both", expand=True)

        # ── Sidebar ──────────────────────────────────────────
        sidebar = ctk.CTkFrame(outer, width=220, corner_radius=0,
                               fg_color=BG_SIDEBAR, border_width=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo
        logo_f = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_f.pack(fill="x", padx=16, pady=(24,8))
        ctk.CTkFrame(logo_f, height=3, fg_color=ACCENT,
                     corner_radius=2).pack(fill="x")
        ctk.CTkLabel(logo_f, text="3D ATÖLYE",
                     font=ctk.CTkFont(family="Courier", size=20, weight="bold"),
                     text_color=ACCENT).pack(pady=(8,0))
        ctk.CTkLabel(logo_f, text="PRO v3.0",
                     font=ctk.CTkFont(family="Courier", size=11),
                     text_color=ACCENT2).pack()

        # Kullanıcı şeridi
        user_f = ctk.CTkFrame(sidebar, fg_color="#1C2333", corner_radius=12)
        user_f.pack(fill="x", padx=12, pady=(8,16))
        ctk.CTkLabel(user_f, text="👤",
                     font=ctk.CTkFont(size=24)).pack(pady=(10,2))
        ctk.CTkLabel(user_f, text=self.current_user,
                     font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
                     text_color=ACCENT).pack()
        ctk.CTkLabel(user_f, text="Atölye Sahibi",
                     font=ctk.CTkFont(size=11), text_color="#8B949E").pack(pady=(0,10))

        # Nav butonları
        self._active_nav = None
        nav_items = [
            ("📊", "Dashboard",     self.show_main_tab),
            ("📦", "Stok Takibi",   self.show_stock_tab),
            ("💰", "Satış",         self.show_sales_tab),
            ("📈", "Finans",        self.show_finance_tab),
            ("👥", "Müşteriler",    self.show_customers_tab),
            ("✅", "Görevler",      self.show_tasks_tab),
            ("📝", "Notlar",        self.show_notes_tab),
            ("📉", "İstatistikler", self.show_stats_tab),
            ("📋", "Aktivite Logu", self.show_log_tab),
            ("⚙️", "Ayarlar",       self.show_settings_tab),
        ]
        self._nav_btns = {}
        for icon, label, cmd in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f" {icon}  {label}",
                anchor="w",
                height=40,
                corner_radius=10,
                fg_color="transparent",
                hover_color="#1C2333",
                text_color="#C9D1D9",
                font=ctk.CTkFont(size=13),
                command=lambda c=cmd, l=label: self._nav_click(c, l),
            )
            btn.pack(fill="x", padx=10, pady=2)
            self._nav_btns[label] = btn

        # Çıkış
        ctk.CTkFrame(sidebar, height=1, fg_color=BORDER).pack(
            fill="x", padx=12, pady=12)
        accent_btn(sidebar, " 🚪  Çıkış Yap", self.show_auth_page,
                   color=DANGER, hover="#c62828",
                   height=40).pack(fill="x", padx=10, pady=(0,16))

        # ── İçerik alanı ─────────────────────────────────────
        self.main_area = ctk.CTkFrame(outer, corner_radius=0,
                                      fg_color=BG_DARK)
        self.main_area.pack(side="right", fill="both", expand=True)

        self._nav_click(self.show_main_tab, "Dashboard")

    def _nav_click(self, cmd, label):
        # önceki aktif butonu sıfırla
        if self._active_nav and self._active_nav in self._nav_btns:
            self._nav_btns[self._active_nav].configure(
                fg_color="transparent", text_color="#C9D1D9")
        self._active_nav = label
        if label in self._nav_btns:
            self._nav_btns[label].configure(
                fg_color="#1C2333", text_color=ACCENT)
        cmd()

    def clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    def _page_header(self, icon, title, subtitle=""):
        hdr = ctk.CTkFrame(self.main_area, fg_color="transparent")
        hdr.pack(fill="x", padx=28, pady=(22,6))
        ctk.CTkLabel(hdr,
                     text=f"{icon}  {title}",
                     font=ctk.CTkFont(family="Courier", size=28, weight="bold"),
                     text_color="white").pack(side="left")
        if subtitle:
            ctk.CTkLabel(hdr, text=subtitle,
                         font=ctk.CTkFont(size=12), text_color="#8B949E").pack(
                side="left", padx=14, pady=6)
        ctk.CTkFrame(self.main_area, height=1,
                     fg_color=BORDER).pack(fill="x", padx=28, pady=(0,10))

    # ══════════════════════════════════════════════════════════
    #  SEKME 1: ANA DASHBOARD
    # ══════════════════════════════════════════════════════════

    def show_main_tab(self):
        self.clear_main()
        self._page_header("📊", "Dashboard", "Genel bakış & hızlı işlemler")

        scroll = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=0)

        # ── KPI kartları (satır 1) ────────────────────────────
        projects  = self.get_all_projects()
        sales     = u_load(SALES_FILE, self.current_user)
        expenses  = u_load(EXPENSES_FILE, self.current_user)
        customers = u_load(CUSTOMERS_FILE, self.current_user)
        stock     = load_stock()
        threshold = get_low_stock_threshold()

        t_mal    = sum(p.get("toplam_maliyet",0) for p in projects)
        t_satis  = sum(s.get("satis_fiyati",0) for s in sales)
        t_gider  = sum(e.get("tutar",0) for e in expenses)
        net_kar  = t_satis - t_mal - t_gider
        t_stok   = sum(stock.values())
        dusuk    = sum(1 for v in stock.values() if 0 < v < threshold)

        kpis_r1 = [
            ("📋", "Proje",        str(len(projects)),          "#C9D1D9"),
            ("⚖️", "Toplam Gram",  f"{t_mal:,.0f} g",           "#C9D1D9"),
            ("💸", "Proje Maliyet",f"{t_mal:,.2f} TL",          "#C9D1D9"),
            ("🛒", "Toplam Satış", f"{t_satis:,.2f} TL",        SUCCESS),
            ("✅", "Net Kar",      f"{net_kar:,.2f} TL",
             SUCCESS if net_kar >= 0 else DANGER),
        ]
        kpis_r2 = [
            ("📤", "Toplam Gider", f"{t_gider:,.2f} TL",        DANGER),
            ("📦", "Toplam Stok",  f"{t_stok:,.0f} g",          ACCENT),
            ("⚠️", "Düşük Stok",  f"{dusuk} ürün",
             WARNING if dusuk else SUCCESS),
            ("👥", "Müşteri",      str(len(customers)),          ACCENT2),
            ("🛍️", "Satış Adedi", str(len(sales)),              "#C9D1D9"),
        ]

        for row_data in [kpis_r1, kpis_r2]:
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=4)
            for icon, label, val, col in row_data:
                card = make_card(row, height=105)
                card.pack(side="left", expand=True, fill="x", padx=5)
                card.pack_propagate(False)
                ctk.CTkLabel(card, text=icon,
                             font=ctk.CTkFont(size=20)).pack(pady=(12,2))
                ctk.CTkLabel(card, text=label,
                             font=ctk.CTkFont(size=11),
                             text_color="#8B949E").pack()
                ctk.CTkLabel(card, text=val,
                             font=ctk.CTkFont(family="Courier",size=16,weight="bold"),
                             text_color=col).pack(pady=(2,8))

        # ── Orta: form + mini grafikler ───────────────────────
        mid = ctk.CTkFrame(scroll, fg_color="transparent")
        mid.pack(fill="both", expand=True, pady=8)

        # — Proje ekleme formu ——
        form_card = make_card(mid, width=360)
        form_card.pack(side="left", fill="y", padx=(0,10))
        form_card.pack_propagate(False)

        fc = ctk.CTkScrollableFrame(form_card, fg_color="transparent")
        fc.pack(fill="both", expand=True, padx=4, pady=4)

        ctk.CTkLabel(fc, text="➕  YENİ PROJE",
                     font=ctk.CTkFont(family="Courier", size=16, weight="bold"),
                     text_color=ACCENT).pack(pady=(12,10))

        self.entry_model    = mini_entry(fc, "Model adı *", width=310)
        self.entry_model.pack(pady=4, padx=10)
        self.entry_category = mini_entry(fc, "Kategori *", width=310)
        self.entry_category.pack(pady=4, padx=10)
        self.entry_color    = mini_entry(fc, "Renk *", width=310)
        self.entry_color.pack(pady=4, padx=10)
        self.entry_gram     = mini_entry(fc, "Kullanılan gram *", width=310)
        self.entry_gram.pack(pady=4, padx=10)
        self.entry_time     = mini_entry(fc, "Baskı süresi (saat)", width=310)
        self.entry_time.insert(0,"0")
        self.entry_time.pack(pady=4, padx=10)
        self.entry_note     = mini_entry(fc, "Kısa not", width=310)
        self.entry_note.pack(pady=4, padx=10)
        self.entry_elektrik = mini_entry(fc, "Elektrik TL/kWh", width=310)
        self.entry_elektrik.insert(0, str(get_electric_price()))
        self.entry_elektrik.pack(pady=4, padx=10)

        ctk.CTkLabel(fc, text="Filament Türü",
                     text_color="#8B949E", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.combo_filament = mini_combo(fc, list(FILAMENT_FIYATLAR.keys()), width=310)
        self.combo_filament.set("PLA")
        self.combo_filament.pack(pady=4, padx=10)

        ctk.CTkLabel(fc, text="Yazıcı Markası",
                     text_color="#8B949E", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.combo_brand = mini_combo(fc, list(YAZICI_KATALOGU.keys()), width=310,
                                      command=self._update_model_combo)
        self.combo_brand.set("Bambu Lab")
        self.combo_brand.pack(pady=4, padx=10)

        ctk.CTkLabel(fc, text="Yazıcı Modeli",
                     text_color="#8B949E", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.combo_model = mini_combo(fc, [], width=310)
        self.combo_model.pack(pady=4, padx=10)
        self._update_model_combo("Bambu Lab")

        ctk.CTkLabel(fc, text="Proje Durumu",
                     text_color="#8B949E", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.combo_status = mini_combo(fc, ["Hazırlanıyor","Basılıyor","Tamamlandı","İptal"], width=310)
        self.combo_status.set("Hazırlanıyor")
        self.combo_status.pack(pady=4, padx=10)

        # Kar marjı hesaplama
        ctk.CTkLabel(fc, text="Önerilen Satış Fiyatı",
                     text_color="#8B949E", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(8,0))
        marj_f = ctk.CTkFrame(fc, fg_color="transparent")
        marj_f.pack(fill="x", padx=10)
        self.combo_marj = mini_combo(marj_f, list(KAR_MARJI_ONERILERI.keys()), width=200)
        self.combo_marj.set("Normal (%40)")
        self.combo_marj.pack(side="left")
        accent_btn(marj_f, "Hesapla", self._hesapla_satis_fiyati,
                   height=38, width=100).pack(side="left", padx=6)

        self.lbl_oneri = ctk.CTkLabel(fc, text="",
                                      font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
                                      text_color=WARNING)
        self.lbl_oneri.pack(pady=4)

        btn_row = ctk.CTkFrame(fc, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(10,4))
        accent_btn(btn_row, "💾 Kaydet", self.add_project, height=40).pack(side="left", expand=True, fill="x", padx=(0,4))
        accent_btn(btn_row, "⚡ Elektrik Güncelle", self.update_electric_price,
                   color="#1C4370", hover="#1a3a6b", height=40).pack(side="left", expand=True, fill="x")

        self.add_info = ctk.CTkLabel(fc, text="", wraplength=310,
                                     font=ctk.CTkFont(size=12))
        self.add_info.pack(pady=(4,12))

        # — Sağ: proje listesi + mini grafik ——
        right_panel = ctk.CTkFrame(mid, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        # Küçük filament kullanım grafiği
        graph_card = make_card(right_panel)
        graph_card.pack(fill="x", pady=(0,10))
        ctk.CTkLabel(graph_card, text="🧵  Filament Kullanımı",
                     font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
                     text_color=ACCENT).pack(anchor="w", padx=14, pady=(10,4))

        fil_usage = {}
        for p in projects:
            f  = p.get("filament_turu","PLA")
            fil_usage[f] = fil_usage.get(f,0) + p.get("gram",0)
        if fil_usage:
            MiniBarChart(graph_card, fil_usage, color=ACCENT, height=90)
        else:
            ctk.CTkLabel(graph_card, text="Henüz veri yok.",
                         text_color="#555").pack(pady=20)

        # Proje listesi
        list_card = make_card(right_panel)
        list_card.pack(fill="both", expand=True)

        lhdr = ctk.CTkFrame(list_card, fg_color="transparent")
        lhdr.pack(fill="x", padx=14, pady=(12,6))
        ctk.CTkLabel(lhdr, text="📋  PROJELER",
                     font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
                     text_color=ACCENT).pack(side="left")

        # Arama
        self.search_entry = mini_entry(lhdr, "Ara...", width=200, height=34)
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", lambda e: self._live_search())

        btn_row2 = ctk.CTkFrame(list_card, fg_color="transparent")
        btn_row2.pack(fill="x", padx=14, pady=(0,6))
        accent_btn(btn_row2, "📋 Forma Yükle",   self.load_project_to_form,
                   color="#1C4370", hover="#1a3a6b", height=34, width=130).pack(side="left", padx=(0,4))
        success_btn(btn_row2, "✏️ Güncelle",     self.update_selected_project,
                    height=34, width=110).pack(side="left", padx=4)
        danger_btn(btn_row2, "🗑 Sil",           self.delete_selected_project,
                   height=34, width=80).pack(side="left", padx=4)

        self.project_list = ctk.CTkTextbox(list_card, corner_radius=10,
                                           fg_color="#0D1117",
                                           font=ctk.CTkFont(family="Courier", size=12))
        self.project_list.pack(fill="both", expand=True, padx=14, pady=(0,6))

        self.select_entry = mini_entry(list_card, "İşlem yapılacak proje numarası", height=34)
        self.select_entry.pack(fill="x", padx=14, pady=(0,12))

        self._fill_project_list(projects)

    def _update_model_combo(self, brand=None):
        brand = brand or self.combo_brand.get()
        models = list(YAZICI_KATALOGU.get(brand, {}).keys()) or ["Model Yok"]
        self.combo_model.configure(values=models)
        self.combo_model.set(models[0])

    # compat alias
    def update_model_combo(self, b=None): self._update_model_combo(b)

    def _hesapla_satis_fiyati(self):
        try:
            gram    = float(self.entry_gram.get().strip().replace(",",".") or "0")
            sure    = float(self.entry_time.get().strip().replace(",",".") or "0")
            filament= self.combo_filament.get().upper()
            marka   = self.combo_brand.get()
            model   = self.combo_model.get()
            toplam, *_ = toplam_maliyet_hesapla(gram, filament, sure, marka, model)
            marj_key= self.combo_marj.get()
            marj    = KAR_MARJI_ONERILERI.get(marj_key, 0.40)
            oneri   = round(toplam * (1 + marj), 2)
            self.lbl_oneri.configure(
                text=f"Maliyet: {toplam} TL  →  Satış: {oneri} TL")
        except Exception as e:
            self.lbl_oneri.configure(text=f"Hata: {e}", text_color=DANGER)

    def update_electric_price(self):
        try:
            v = float(self.entry_elektrik.get().strip().replace(",","."))
            if v <= 0: raise ValueError
            set_electric_price(v)
            self.add_info.configure(
                text=f"✓ Elektrik {v} TL/kWh olarak kaydedildi.", text_color=SUCCESS)
        except ValueError:
            messagebox.showerror("Hata","Geçerli pozitif sayı gir.")

    def add_project(self):
        try:
            model   = self.entry_model.get().strip()
            kat     = self.entry_category.get().strip()
            fil     = self.combo_filament.get().strip().upper()
            marka   = self.combo_brand.get().strip()
            ymdl    = self.combo_model.get().strip()
            renk    = self.entry_color.get().strip()
            gram    = float(self.entry_gram.get().strip().replace(",","."))
            sure    = float(self.entry_time.get().strip().replace(",",".") or "0")
            durum   = self.combo_status.get().strip()
            not_txt = self.entry_note.get().strip()

            if not model or not kat or not renk:
                self.add_info.configure(text="✗ Model, kategori, renk zorunlu.", text_color=DANGER)
                return

            stock = load_stock()
            if stock.get(fil,0) < gram:
                self.add_info.configure(
                    text=f"✗ Yeterli {fil} yok! Mevcut: {stock.get(fil,0):.0f} g",
                    text_color=DANGER)
                return
            stock[fil] -= gram
            save_stock(stock)

            toplam, f_mal, e_mal, watt, e_tuk = toplam_maliyet_hesapla(
                gram, fil, sure, marka, ymdl)

            prj = {
                "owner": self.current_user,
                "model_adi": model.title(), "kategori": kat.title(),
                "filament_turu": fil, "yazici_marka": marka, "yazici_model": ymdl,
                "watt": watt, "renk": renk.title(), "gram": gram, "sure": sure,
                "filament_maliyet": f_mal, "elektrik_maliyet": e_mal,
                "elektrik_tuketimi": e_tuk, "toplam_maliyet": toplam,
                "maliyet": toplam, "durum": durum, "not": not_txt,
                "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
            }
            projects = self.get_all_projects()
            projects.append(prj)
            self.save_user_projects(projects)
            log_activity(self.current_user, "PROJE EKLENDİ", model)

            self.add_info.configure(
                text=f"✓ {model.title()} eklendi | Toplam: {toplam} TL",
                text_color=SUCCESS)

            for attr in ["entry_model","entry_category","entry_color","entry_gram","entry_note"]:
                getattr(self, attr).delete(0,"end")
            self.entry_time.delete(0,"end"); self.entry_time.insert(0,"0")
            self.combo_filament.set("PLA"); self.combo_brand.set("Bambu Lab")
            self._update_model_combo("Bambu Lab"); self.combo_status.set("Hazırlanıyor")
            self._fill_project_list(self.get_all_projects())

        except ValueError:
            self.add_info.configure(text="✗ Gram ve süre sayı olmalı.", text_color=DANGER)
        except Exception as e:
            self.add_info.configure(text=f"✗ Hata: {e}", text_color=DANGER)

    def _fill_project_list(self, projects):
        self.project_list.configure(state="normal")
        self.project_list.delete("0.0","end")
        if not projects:
            self.project_list.insert("0.0","  Henüz kayıtlı proje yok.\n")
        else:
            durum_ikon = {"Tamamlandı":"✅","Basılıyor":"🔄","Hazırlanıyor":"⏳","İptal":"❌"}
            for i,p in enumerate(projects,1):
                d = p.get("durum","–")
                self.project_list.insert("end",
                    f"[{i:02d}] {p.get('model_adi','–')}  "
                    f"{durum_ikon.get(d,'·')} {d}\n"
                    f"     Kategori  : {p.get('kategori','–')}\n"
                    f"     Filament  : {p.get('filament_turu','–')}  |  "
                    f"Renk: {p.get('renk','–')}\n"
                    f"     Yazıcı    : {p.get('yazici_marka','–')} {p.get('yazici_model','–')}  "
                    f"({p.get('watt','–')} W)\n"
                    f"     Gram/Süre : {p.get('gram',0):.0f} g  /  {p.get('sure',0):.1f} h\n"
                    f"     Maliyet   : Filament {p.get('filament_maliyet',0):.2f} TL  "
                    f"+ Elektrik {p.get('elektrik_maliyet',0):.2f} TL  "
                    f"= {p.get('toplam_maliyet',0):.2f} TL\n"
                    f"     Not       : {p.get('not','–')}\n"
                    f"     Tarih     : {p.get('tarih','–')}\n"
                    f"{'─'*60}\n"
                )
        self.project_list.configure(state="disabled")

    def _live_search(self):
        kw = self.search_entry.get().strip().lower()
        all_p = self.get_all_projects()
        if not kw:
            self._fill_project_list(all_p); return
        filtered = [p for p in all_p if kw in (
            f"{p.get('model_adi','')} {p.get('kategori','')} {p.get('filament_turu','')} "
            f"{p.get('durum','')} {p.get('not','')}").lower()]
        self._fill_project_list(filtered)

    def search_projects(self): self._live_search()

    def load_project_to_form(self):
        try:
            idx = int(self.select_entry.get().strip()) - 1
            projects = self.get_all_projects()
            if idx < 0 or idx >= len(projects):
                messagebox.showerror("Hata","Geçersiz proje numarası."); return
            p = projects[idx]
            for attr,key in [("entry_model","model_adi"),("entry_category","kategori"),
                              ("entry_color","renk"),("entry_gram","gram"),
                              ("entry_time","sure"),("entry_note","not")]:
                e = getattr(self, attr)
                e.delete(0,"end")
                e.insert(0, str(p.get(key,"")))
            self.combo_filament.set(p.get("filament_turu","PLA"))
            marka = p.get("yazici_marka","Bambu Lab")
            self.combo_brand.set(marka); self._update_model_combo(marka)
            self.combo_model.set(p.get("yazici_model","A1"))
            self.combo_status.set(p.get("durum","Hazırlanıyor"))
            self.add_info.configure(text="✓ Proje forma yüklendi.", text_color=WARNING)
        except ValueError:
            messagebox.showerror("Hata","Sayı gir.")

    def update_selected_project(self):
        try:
            idx = int(self.select_entry.get().strip()) - 1
            projects = self.get_all_projects()
            if idx < 0 or idx >= len(projects):
                messagebox.showerror("Hata","Geçersiz numara."); return
            p = projects[idx]
            old_fil, old_g = p.get("filament_turu","PLA"), p.get("gram",0)

            for attr, key, title in [
                ("entry_model","model_adi",True),
                ("entry_category","kategori",True),
                ("entry_color","renk",True),
                ("entry_note","not",False),
            ]:
                v = getattr(self,attr).get().strip()
                if v: p[key] = v.title() if title else v

            for attr, key in [("entry_gram","gram"),("entry_time","sure")]:
                v = getattr(self,attr).get().strip()
                if v: p[key] = float(v.replace(",","."))

            p["filament_turu"] = self.combo_filament.get().upper()
            p["yazici_marka"]  = self.combo_brand.get()
            p["yazici_model"]  = self.combo_model.get()
            p["durum"]         = self.combo_status.get()

            if not adjust_stock(old_fil, old_g, p["filament_turu"], p["gram"]):
                messagebox.showerror("Hata","Yeterli stok yok."); return

            toplam, f_mal, e_mal, watt, e_tuk = toplam_maliyet_hesapla(
                p["gram"], p["filament_turu"], p["sure"],
                p["yazici_marka"], p["yazici_model"])
            p.update({"filament_maliyet":f_mal,"elektrik_maliyet":e_mal,
                      "elektrik_tuketimi":e_tuk,"toplam_maliyet":toplam,
                      "maliyet":toplam,"watt":watt,
                      "tarih":datetime.now().strftime("%d.%m.%Y %H:%M")})
            projects[idx] = p
            self.save_user_projects(projects)
            self.select_entry.delete(0,"end")
            log_activity(self.current_user,"PROJE GÜNCELLENDİ", p.get("model_adi",""))
            self._fill_project_list(self.get_all_projects())
            messagebox.showinfo("Başarılı",f"{p['model_adi']} güncellendi.")
        except ValueError:
            messagebox.showerror("Hata","Sayı gir.")
        except Exception as e:
            messagebox.showerror("Hata",str(e))

    def delete_selected_project(self):
        try:
            idx = int(self.select_entry.get().strip()) - 1
            projects = self.get_all_projects()
            if idx < 0 or idx >= len(projects):
                messagebox.showerror("Hata","Geçersiz numara."); return
            if not messagebox.askyesno("Onay","Projeyi silmek istediğine emin misin?"): return
            silinen = projects.pop(idx)
            stock = load_stock()
            fil = silinen.get("filament_turu","PLA")
            stock[fil] = stock.get(fil,0) + silinen.get("gram",0)
            save_stock(stock)
            self.save_user_projects(projects)
            self.select_entry.delete(0,"end")
            log_activity(self.current_user,"PROJE SİLİNDİ", silinen.get("model_adi",""))
            self._fill_project_list(self.get_all_projects())
            messagebox.showinfo("Başarılı",f"{silinen['model_adi']} silindi. Stok geri yüklendi.")
        except ValueError:
            messagebox.showerror("Hata","Sayı gir.")
        except Exception as e:
            messagebox.showerror("Hata",str(e))

    # ══════════════════════════════════════════════════════════
    #  SEKME 2: FİLAMENT STOK TAKİBİ
    # ══════════════════════════════════════════════════════════

    def show_stock_tab(self):
        self.clear_main()
        self._page_header("📦","Filament Stok Takibi","Stok yönetimi & değer analizi")

        main = ctk.CTkFrame(self.main_area, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=8)

        # Sol: form
        lc = make_card(main, width=340)
        lc.pack(side="left", fill="y", padx=(0,12))
        lc.pack_propagate(False)

        ctk.CTkLabel(lc, text="STOK İŞLEMİ",
                     font=ctk.CTkFont(family="Courier", size=15, weight="bold"),
                     text_color=ACCENT).pack(pady=(18,10))

        self.stk_fil = mini_combo(lc, list(FILAMENT_FIYATLAR.keys()), width=290)
        self.stk_fil.pack(pady=5, padx=18)
        self.stk_amount = mini_entry(lc, "Gram (negatif = çıkar)", width=290)
        self.stk_amount.pack(pady=5, padx=18)
        self.stk_note = mini_entry(lc, "Açıklama", width=290)
        self.stk_note.pack(pady=5, padx=18)

        accent_btn(lc,"➕ Stok Ekle / Çıkar", self._do_stock_update, height=40, width=290).pack(pady=6, padx=18)
        danger_btn(lc,"↩ Seçileni Sıfırla",  self._reset_stock,     height=40, width=290).pack(pady=4, padx=18)

        self.stk_info = ctk.CTkLabel(lc, text="", wraplength=280, font=ctk.CTkFont(size=12))
        self.stk_info.pack(pady=6)

        # Eşik ayarı
        ctk.CTkFrame(lc, height=1, fg_color=BORDER).pack(fill="x", padx=18, pady=10)
        ctk.CTkLabel(lc, text="Düşük Stok Eşiği (g)",
                     text_color="#8B949E", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=18)
        self.stk_threshold = mini_entry(lc, "Gram", width=290)
        self.stk_threshold.insert(0, str(int(get_low_stock_threshold())))
        self.stk_threshold.pack(pady=5, padx=18)
        accent_btn(lc,"💾 Eşiği Kaydet", self._save_threshold, height=38, width=290).pack(pady=4, padx=18)

        # CSV
        ctk.CTkFrame(lc, height=1, fg_color=BORDER).pack(fill="x", padx=18, pady=10)
        accent_btn(lc,"📥 CSV Dışa Aktar", self._export_stock_csv,
                   color="#1C4370", hover="#1a3a6b", height=38, width=290).pack(pady=4, padx=18)

        # Sağ: tablo + donut
        rc = make_card(main)
        rc.pack(side="right", fill="both", expand=True)

        rhdr = ctk.CTkFrame(rc, fg_color="transparent")
        rhdr.pack(fill="x", padx=16, pady=(14,6))
        ctk.CTkLabel(rhdr, text="MEVCUT STOKLAR",
                     font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
                     text_color=ACCENT).pack(side="left")
        accent_btn(rhdr,"🔃 Yenile", self._refresh_stock_view, height=30, width=80).pack(side="right")

        # Donut grafik + tablo yan yana
        inner = ctk.CTkFrame(rc, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=(0,16))

        stock_data = load_stock()
        nonempty   = {k:v for k,v in stock_data.items() if v > 0}
        if nonempty:
            dc = ctk.CTkFrame(inner, fg_color="transparent", width=170)
            dc.pack(side="left", fill="y", pady=4)
            dc.pack_propagate(False)
            ctk.CTkLabel(dc, text="Dağılım", text_color="#8B949E",
                         font=ctk.CTkFont(size=11)).pack()
            DonutChart(dc, nonempty, size=155)

        self.stock_box = ctk.CTkTextbox(inner, corner_radius=10,
                                        fg_color="#0D1117",
                                        font=ctk.CTkFont(family="Courier", size=12))
        self.stock_box.pack(side="right", fill="both", expand=True, padx=(12,0))
        self._refresh_stock_view()

    def _refresh_stock_view(self):
        try: thr = float(self.stk_threshold.get().strip() or "500")
        except: thr = 500
        stock = load_stock()
        self.stock_box.configure(state="normal")
        self.stock_box.delete("0.0","end")
        self.stock_box.insert("end",
            f"{'Filament':<22}{'Stok':>10}{'kg Fiyatı':>12}{'Değer':>14}{'Durum':>14}\n"
            + "═"*72 + "\n")
        total_val = 0
        for fil, gram in sorted(stock.items(), key=lambda x: x[1], reverse=True):
            fiyat = FILAMENT_FIYATLAR.get(fil,0)
            deger = (gram/1000)*fiyat
            total_val += deger
            if gram == 0:   durum = "❌ TÜKENDİ"
            elif gram < thr: durum = "⚠️  DÜŞÜK"
            else:            durum = "✅ YETERLİ"
            bar = "▓"*min(int(gram/200),10)
            self.stock_box.insert("end",
                f"{fil:<22}{gram:>8.0f} g{fiyat:>9} TL/kg{deger:>11.2f} TL  {durum}\n"
                f"  {bar}\n")
        self.stock_box.insert("end",
            "═"*72 + f"\n{'TOPLAM STOK DEĞERİ':<50}{total_val:>10.2f} TL\n")
        self.stock_box.configure(state="disabled")

    def _do_stock_update(self):
        try:
            fil    = self.stk_fil.get().upper()
            amount = float(self.stk_amount.get().strip().replace(",","."))
            stock  = load_stock()
            new    = stock.get(fil,0) + amount
            if new < 0:
                messagebox.showerror("Hata",f"Stok negatif olamaz! Mevcut: {stock.get(fil,0):.0f} g"); return
            stock[fil] = new
            save_stock(stock)
            op = "eklendi" if amount >= 0 else "çıkarıldı"
            self.stk_info.configure(text=f"✓ {abs(amount):.0f} g {op}. Yeni: {new:.0f} g",
                                    text_color=SUCCESS)
            log_activity(self.current_user,"STOK GÜNCELLENDİ",
                         f"{fil}: {amount:+.0f} g")
            self.stk_amount.delete(0,"end")
            self._refresh_stock_view()
        except ValueError:
            messagebox.showerror("Hata","Geçerli sayı gir.")

    def _reset_stock(self):
        fil = self.stk_fil.get().upper()
        if messagebox.askyesno("Onay",f"{fil} stokunu sıfırlamak istiyor musun?"):
            s = load_stock(); s[fil]=0; save_stock(s)
            self.stk_info.configure(text=f"{fil} sıfırlandı.", text_color=WARNING)
            self._refresh_stock_view()

    def _save_threshold(self):
        try:
            v = float(self.stk_threshold.get().strip())
            set_low_stock_threshold(v)
            self.stk_info.configure(text=f"✓ Eşik {v:.0f} g olarak kaydedildi.",
                                    text_color=SUCCESS)
            self._refresh_stock_view()
        except ValueError:
            messagebox.showerror("Hata","Sayı gir.")

    def _export_stock_csv(self):
        stock = load_stock()
        path  = f"stok_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(path,"w",encoding="utf-8",newline="") as f:
            w = csv.writer(f)
            w.writerow(["Filament","Stok (g)","Birim Fiyat TL/kg","Değer TL"])
            for fil,gram in stock.items():
                fiyat = FILAMENT_FIYATLAR.get(fil,0)
                w.writerow([fil,gram,fiyat,round((gram/1000)*fiyat,2)])
        messagebox.showinfo("CSV","Stok dışa aktarıldı:\n"+path)

    # ══════════════════════════════════════════════════════════
    #  SEKME 3: SATIŞ YÖNETİMİ
    # ══════════════════════════════════════════════════════════

    def show_sales_tab(self):
        self.clear_main()
        self._page_header("💰","Satış Yönetimi","Sipariş kayıtları & kar analizi")

        main = ctk.CTkFrame(self.main_area, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=8)

        # Sol form
        lc = ctk.CTkScrollableFrame(main, fg_color=BG_CARD,
                                    corner_radius=16, width=340,
                                    border_width=1, border_color=BORDER)
        lc.pack(side="left", fill="y", padx=(0,12))

        ctk.CTkLabel(lc, text="YENİ SATIŞ",
                     font=ctk.CTkFont(family="Courier", size=15, weight="bold"),
                     text_color=ACCENT).pack(pady=(14,10))

        projects  = self.get_all_projects()
        customers = u_load(CUSTOMERS_FILE, self.current_user)

        ctk.CTkLabel(lc, text="Proje (opsiyonel)",
                     text_color="#8B949E", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=14)
        self.sale_prj = mini_combo(lc,
            ["(Bağımsız)"] + [f"[{i+1}] {p.get('model_adi','')}" for i,p in enumerate(projects)],
            width=300)
        self.sale_prj.set("(Bağımsız)")
        self.sale_prj.pack(pady=4, padx=14)

        ctk.CTkLabel(lc, text="Müşteri",
                     text_color="#8B949E", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=14)
        self.sale_cust = mini_combo(lc,
            ["(Anonim)"] + [c.get("ad","") for c in customers], width=300)
        self.sale_cust.set("(Anonim)")
        self.sale_cust.pack(pady=4, padx=14)

        for attr,ph in [("sale_product","Ürün adı *"),
                        ("sale_price","Satış fiyatı (TL) *"),
                        ("sale_qty","Adet"),("sale_note","Not")]:
            e = mini_entry(lc, ph, width=300)
            e.pack(pady=4, padx=14)
            setattr(self, attr, e)
        self.sale_qty.insert(0,"1")

        ctk.CTkLabel(lc, text="Ödeme Yöntemi",
                     text_color="#8B949E", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=14)
        self.sale_pay = mini_combo(lc,
            ["Nakit","Kredi Kartı","EFT/Havale","Taksit","Diğer"], width=300)
        self.sale_pay.set("Nakit")
        self.sale_pay.pack(pady=4, padx=14)

        # İndirim
        ctk.CTkLabel(lc, text="İndirim (%)",
                     text_color="#8B949E", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=14)
        self.sale_discount = mini_entry(lc, "Örn: 10", width=300)
        self.sale_discount.insert(0,"0")
        self.sale_discount.pack(pady=4, padx=14)

        accent_btn(lc,"💾 Satışı Kaydet", self._add_sale, height=42, width=300).pack(pady=(14,4), padx=14)
        self.sale_info = ctk.CTkLabel(lc, text="", wraplength=290, font=ctk.CTkFont(size=12))
        self.sale_info.pack(pady=6)

        # Sağ: liste
        rc = make_card(main)
        rc.pack(side="right", fill="both", expand=True)

        rhdr = ctk.CTkFrame(rc, fg_color="transparent")
        rhdr.pack(fill="x", padx=16, pady=(14,6))
        ctk.CTkLabel(rhdr, text="SATIŞ GEÇMİŞİ",
                     font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
                     text_color=ACCENT).pack(side="left")
        danger_btn(rhdr,"🗑 Seçileni Sil", self._del_sale, height=34, width=120).pack(side="right")
        accent_btn(rhdr,"📥 CSV", self._export_sales_csv,
                   color="#1C4370", hover="#1a3a6b", height=34, width=80).pack(side="right", padx=6)

        self.sales_box = ctk.CTkTextbox(rc, corner_radius=10,
                                        fg_color="#0D1117",
                                        font=ctk.CTkFont(family="Courier", size=12))
        self.sales_box.pack(fill="both", expand=True, padx=16, pady=(0,6))

        self.sale_sel = mini_entry(rc, "Silmek için satış no", height=34)
        self.sale_sel.pack(fill="x", padx=16, pady=(0,12))

        self._refresh_sales()

    def _add_sale(self):
        try:
            product  = self.sale_product.get().strip()
            price    = float(self.sale_price.get().strip().replace(",","."))
            qty      = int(self.sale_qty.get().strip() or "1")
            note     = self.sale_note.get().strip()
            payment  = self.sale_pay.get()
            customer = self.sale_cust.get()
            discount = float(self.sale_discount.get().strip().replace(",",".") or "0")
            if not product:
                self.sale_info.configure(text="✗ Ürün adı boş.", text_color=DANGER); return

            prj_txt  = self.sale_prj.get()
            prj_cost = 0; prj_name = ""
            if prj_txt != "(Bağımsız)":
                try:
                    idx = int(prj_txt.split("]")[0].replace("[","")) - 1
                    prj = self.get_all_projects()[idx]
                    prj_cost = prj.get("toplam_maliyet",0)
                    prj_name = prj.get("model_adi","")
                except: pass

            total_before = price * qty
            indirim_tutar= total_before * (discount/100)
            total        = total_before - indirim_tutar
            kar          = total - prj_cost * qty

            s = {
                "owner": self.current_user,
                "urun": product.title(), "proje": prj_name,
                "musteri": customer,
                "satis_fiyati": round(total,2),
                "birim_fiyat": price, "adet": qty,
                "indirim_yuzde": discount,
                "indirim_tutar": round(indirim_tutar,2),
                "maliyet": round(prj_cost*qty,2),
                "kar": round(kar,2),
                "odeme": payment, "not": note,
                "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
            }
            sales = u_load(SALES_FILE, self.current_user)
            sales.append(s)
            u_save(SALES_FILE, self.current_user, sales)
            log_activity(self.current_user,"SATIŞ KAYDEDİLDİ",
                         f"{product} — {total:.2f} TL")
            self.sale_info.configure(
                text=f"✓ Kaydedildi | Toplam: {total:.2f} TL | Kar: {kar:.2f} TL",
                text_color=SUCCESS)
            for attr in ["sale_product","sale_price","sale_note"]:
                getattr(self,attr).delete(0,"end")
            self.sale_qty.delete(0,"end"); self.sale_qty.insert(0,"1")
            self.sale_discount.delete(0,"end"); self.sale_discount.insert(0,"0")
            self._refresh_sales()
        except ValueError:
            self.sale_info.configure(text="✗ Fiyat/adet sayı olmalı.", text_color=DANGER)
        except Exception as e:
            self.sale_info.configure(text=f"✗ {e}", text_color=DANGER)

    def _del_sale(self):
        try:
            idx   = int(self.sale_sel.get().strip()) - 1
            sales = u_load(SALES_FILE, self.current_user)
            if idx < 0 or idx >= len(sales):
                messagebox.showerror("Hata","Geçersiz no."); return
            if not messagebox.askyesno("Onay","Satışı silmek istiyor musun?"): return
            sales.pop(idx)
            u_save(SALES_FILE, self.current_user, sales)
            self.sale_sel.delete(0,"end")
            self._refresh_sales()
        except ValueError:
            messagebox.showerror("Hata","Sayı gir.")

    def _refresh_sales(self):
        sales = u_load(SALES_FILE, self.current_user)
        self.sales_box.configure(state="normal")
        self.sales_box.delete("0.0","end")
        if not sales:
            self.sales_box.insert("0.0","  Satış kaydı yok.\n")
        else:
            t_satis = sum(s.get("satis_fiyati",0) for s in sales)
            t_kar   = sum(s.get("kar",0) for s in sales)
            self.sales_box.insert("end",
                f"  TOPLAM: {t_satis:,.2f} TL  |  NET KAR: {t_kar:,.2f} TL\n"
                + "═"*65 + "\n\n")
            for i,s in enumerate(sales,1):
                kar_ikon = "▲" if s.get("kar",0)>=0 else "▼"
                self.sales_box.insert("end",
                    f"[{i:02d}] {s.get('urun','–')}  ×{s.get('adet',1)}  "
                    f"→ {s.get('satis_fiyati',0):.2f} TL\n"
                    f"     Müşteri  : {s.get('musteri','Anonim')}\n"
                    f"     Proje    : {s.get('proje','–')}\n"
                    f"     İndirim  : %{s.get('indirim_yuzde',0)}  "
                    f"({s.get('indirim_tutar',0):.2f} TL)\n"
                    f"     Maliyet  : {s.get('maliyet',0):.2f} TL  "
                    f"|  Kar {kar_ikon}: {s.get('kar',0):.2f} TL\n"
                    f"     Ödeme    : {s.get('odeme','–')}  "
                    f"|  {s.get('tarih','–')}\n"
                    f"     Not      : {s.get('not','–')}\n"
                    + "─"*55 + "\n")
        self.sales_box.configure(state="disabled")

    def _export_sales_csv(self):
        sales = u_load(SALES_FILE, self.current_user)
        path  = f"satislar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(path,"w",encoding="utf-8",newline="") as f:
            w = csv.writer(f)
            w.writerow(["No","Ürün","Müşteri","Adet","Fiyat","İndirim%","Maliyet","Kar","Ödeme","Tarih"])
            for i,s in enumerate(sales,1):
                w.writerow([i, s.get("urun",""), s.get("musteri",""),
                            s.get("adet",1), s.get("satis_fiyati",0),
                            s.get("indirim_yuzde",0), s.get("maliyet",0),
                            s.get("kar",0), s.get("odeme",""), s.get("tarih","")])
        messagebox.showinfo("CSV","Satışlar dışa aktarıldı:\n"+path)

    # ══════════════════════════════════════════════════════════
    #  SEKME 4: FİNANS (GELİR/GİDER)
    # ══════════════════════════════════════════════════════════

    def show_finance_tab(self):
        self.clear_main()
        self._page_header("📈","Finans","Gelir · Gider · Kar/Zarar")

        main = ctk.CTkFrame(self.main_area, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=8)

        # Sol: form + özet
        lc = make_card(main, width=360)
        lc.pack(side="left", fill="y", padx=(0,12))
        lc.pack_propagate(False)

        ctk.CTkLabel(lc, text="GİDER EKLE",
                     font=ctk.CTkFont(family="Courier", size=15, weight="bold"),
                     text_color=ACCENT).pack(pady=(18,10))

        for attr,ph in [("exp_title","Başlık *"),("exp_amount","Tutar (TL) *"),("exp_note","Açıklama")]:
            e = mini_entry(lc, ph, width=310)
            e.pack(pady=5, padx=18)
            setattr(self, attr, e)

        ctk.CTkLabel(lc, text="Kategori", text_color="#8B949E",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=18)
        self.exp_cat = mini_combo(lc,
            ["Filament Alımı","Elektrik","Bakım/Onarım","Ekipman Alımı",
             "Kargo","Pazarlama","Diğer"], width=310)
        self.exp_cat.set("Filament Alımı")
        self.exp_cat.pack(pady=5, padx=18)

        accent_btn(lc,"💾 Gider Kaydet", self._add_expense, height=40, width=310).pack(pady=(12,4), padx=18)
        self.exp_info = ctk.CTkLabel(lc, text="", wraplength=290, font=ctk.CTkFont(size=12))
        self.exp_info.pack(pady=6)

        # Finansal özet
        ctk.CTkFrame(lc, height=1, fg_color=BORDER).pack(fill="x", padx=18, pady=8)
        ctk.CTkLabel(lc, text="FİNANSAL ÖZET",
                     font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
                     text_color=ACCENT).pack(pady=(4,6))
        self.fin_summary = ctk.CTkTextbox(lc, height=220, corner_radius=10,
                                          fg_color="#0D1117",
                                          font=ctk.CTkFont(family="Courier", size=12))
        self.fin_summary.pack(fill="x", padx=18, pady=(0,14))

        # Sağ
        rc = make_card(main)
        rc.pack(side="right", fill="both", expand=True)

        rhdr = ctk.CTkFrame(rc, fg_color="transparent")
        rhdr.pack(fill="x", padx=16, pady=(14,6))
        ctk.CTkLabel(rhdr, text="GİDER GEÇMİŞİ",
                     font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
                     text_color=ACCENT).pack(side="left")
        danger_btn(rhdr,"🗑 Sil", self._del_expense, height=34, width=80).pack(side="right")
        accent_btn(rhdr,"📥 CSV", self._export_expenses_csv,
                   color="#1C4370", hover="#1a3a6b", height=34, width=80).pack(side="right", padx=6)

        self.exp_box = ctk.CTkTextbox(rc, corner_radius=10, fg_color="#0D1117",
                                      font=ctk.CTkFont(family="Courier", size=12))
        self.exp_box.pack(fill="both", expand=True, padx=16, pady=(0,6))

        self.exp_sel = mini_entry(rc, "Silmek için gider no", height=34)
        self.exp_sel.pack(fill="x", padx=16, pady=(0,12))

        self._refresh_finance()

    def _add_expense(self):
        try:
            title  = self.exp_title.get().strip()
            amount = float(self.exp_amount.get().strip().replace(",","."))
            note   = self.exp_note.get().strip()
            cat    = self.exp_cat.get()
            if not title:
                self.exp_info.configure(text="✗ Başlık boş.", text_color=DANGER); return
            exp = {"owner":self.current_user, "baslik":title.title(),
                   "tutar":amount, "kategori":cat, "not":note,
                   "tarih":datetime.now().strftime("%d.%m.%Y %H:%M")}
            exps = u_load(EXPENSES_FILE, self.current_user)
            exps.append(exp)
            u_save(EXPENSES_FILE, self.current_user, exps)
            log_activity(self.current_user,"GİDER KAYDEDİLDİ",
                         f"{title} — {amount:.2f} TL")
            self.exp_info.configure(text=f"✓ {amount:.2f} TL gider kaydedildi.",
                                    text_color=SUCCESS)
            for attr in ["exp_title","exp_amount","exp_note"]:
                getattr(self,attr).delete(0,"end")
            self._refresh_finance()
        except ValueError:
            self.exp_info.configure(text="✗ Tutar sayı olmalı.", text_color=DANGER)

    def _del_expense(self):
        try:
            idx  = int(self.exp_sel.get().strip()) - 1
            exps = u_load(EXPENSES_FILE, self.current_user)
            if idx < 0 or idx >= len(exps):
                messagebox.showerror("Hata","Geçersiz no."); return
            if not messagebox.askyesno("Onay","Gideri silmek istiyor musun?"): return
            exps.pop(idx)
            u_save(EXPENSES_FILE, self.current_user, exps)
            self.exp_sel.delete(0,"end")
            self._refresh_finance()
        except ValueError:
            messagebox.showerror("Hata","Sayı gir.")

    def _refresh_finance(self):
        exps     = u_load(EXPENSES_FILE, self.current_user)
        sales    = u_load(SALES_FILE,    self.current_user)
        projects = self.get_all_projects()

        t_satis = sum(s.get("satis_fiyati",0) for s in sales)
        t_mal   = sum(p.get("toplam_maliyet",0) for p in projects)
        t_gider = sum(e.get("tutar",0) for e in exps)
        net     = t_satis - t_mal - t_gider

        self.fin_summary.configure(state="normal")
        self.fin_summary.delete("0.0","end")
        self.fin_summary.insert("end",
            f" Toplam Satış   : {t_satis:>10,.2f} TL\n"
            f" Proje Maliyeti : {t_mal:>10,.2f} TL\n"
            f" Toplam Gider   : {t_gider:>10,.2f} TL\n"
            + "─"*34 + "\n"
            f" NET KAR/ZARAR  : {net:>10,.2f} TL\n\n"
        )
        cat_totals = {}
        for e in exps:
            cat_totals[e.get("kategori","Diğer")] = \
                cat_totals.get(e.get("kategori","Diğer"),0) + e.get("tutar",0)
        self.fin_summary.insert("end"," Kategori Bazlı Gider:\n")
        for cat,total in sorted(cat_totals.items(), key=lambda x:x[1], reverse=True):
            self.fin_summary.insert("end", f"  {cat:<18}: {total:,.2f} TL\n")
        self.fin_summary.configure(state="disabled")

        self.exp_box.configure(state="normal")
        self.exp_box.delete("0.0","end")
        if not exps:
            self.exp_box.insert("0.0","  Gider kaydı yok.\n")
        else:
            for i,e in enumerate(exps,1):
                self.exp_box.insert("end",
                    f"[{i:02d}] {e.get('baslik','–')}  →  {e.get('tutar',0):,.2f} TL\n"
                    f"     Kategori : {e.get('kategori','–')}\n"
                    f"     Not      : {e.get('not','–')}\n"
                    f"     Tarih    : {e.get('tarih','–')}\n"
                    + "─"*50 + "\n")
        self.exp_box.configure(state="disabled")

    def _export_expenses_csv(self):
        exps = u_load(EXPENSES_FILE, self.current_user)
        path = f"giderler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(path,"w",encoding="utf-8",newline="") as f:
            w = csv.writer(f)
            w.writerow(["No","Başlık","Tutar","Kategori","Not","Tarih"])
            for i,e in enumerate(exps,1):
                w.writerow([i, e.get("baslik",""), e.get("tutar",0),
                            e.get("kategori",""), e.get("not",""), e.get("tarih","")])
        messagebox.showinfo("CSV","Giderler dışa aktarıldı:\n"+path)

    # ══════════════════════════════════════════════════════════
    #  SEKME 5: MÜŞTERİ YÖNETİMİ
    # ══════════════════════════════════════════════════════════

    def show_customers_tab(self):
        self.clear_main()
        self._page_header("👥","Müşteri Yönetimi","CRM · Alışveriş geçmişi")

        main = ctk.CTkFrame(self.main_area, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=8)

        lc = make_card(main, width=360)
        lc.pack(side="left", fill="y", padx=(0,12))
        lc.pack_propagate(False)

        ctk.CTkLabel(lc, text="MÜŞTERİ EKLE",
                     font=ctk.CTkFont(family="Courier", size=15, weight="bold"),
                     text_color=ACCENT).pack(pady=(18,10))

        for attr,ph in [("cust_name","Ad Soyad *"),("cust_phone","Telefon"),
                        ("cust_email","E-posta"),("cust_address","Adres"),
                        ("cust_note","Not")]:
            e = mini_entry(lc, ph, width=310)
            e.pack(pady=5, padx=18)
            setattr(self, attr, e)

        accent_btn(lc,"💾 Müşteri Ekle", self._add_customer, height=40, width=310).pack(pady=(12,4), padx=18)
        self.cust_info = ctk.CTkLabel(lc, text="", wraplength=290, font=ctk.CTkFont(size=12))
        self.cust_info.pack(pady=6)

        rc = make_card(main)
        rc.pack(side="right", fill="both", expand=True)

        rhdr = ctk.CTkFrame(rc, fg_color="transparent")
        rhdr.pack(fill="x", padx=16, pady=(14,6))
        ctk.CTkLabel(rhdr, text="MÜŞTERİ LİSTESİ",
                     font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
                     text_color=ACCENT).pack(side="left")
        danger_btn(rhdr,"🗑 Sil", self._del_customer, height=34, width=80).pack(side="right")

        self.cust_box = ctk.CTkTextbox(rc, corner_radius=10, fg_color="#0D1117",
                                       font=ctk.CTkFont(family="Courier", size=12))
        self.cust_box.pack(fill="both", expand=True, padx=16, pady=(0,6))

        self.cust_sel = mini_entry(rc, "Silmek için müşteri no", height=34)
        self.cust_sel.pack(fill="x", padx=16, pady=(0,12))

        self._refresh_customers()

    def _add_customer(self):
        name = self.cust_name.get().strip()
        if not name:
            self.cust_info.configure(text="✗ Ad boş.", text_color=DANGER); return
        custs = u_load(CUSTOMERS_FILE, self.current_user)
        custs.append({
            "owner": self.current_user,
            "ad": name.title(),
            "telefon": self.cust_phone.get().strip(),
            "email":   self.cust_email.get().strip(),
            "adres":   self.cust_address.get().strip(),
            "not":     self.cust_note.get().strip(),
            "kayit":   datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        u_save(CUSTOMERS_FILE, self.current_user, custs)
        log_activity(self.current_user,"MÜŞTERİ EKLENDİ", name)
        self.cust_info.configure(text=f"✓ {name} eklendi.", text_color=SUCCESS)
        for attr in ["cust_name","cust_phone","cust_email","cust_address","cust_note"]:
            getattr(self,attr).delete(0,"end")
        self._refresh_customers()

    def _del_customer(self):
        try:
            idx   = int(self.cust_sel.get().strip()) - 1
            custs = u_load(CUSTOMERS_FILE, self.current_user)
            if idx < 0 or idx >= len(custs):
                messagebox.showerror("Hata","Geçersiz no."); return
            if not messagebox.askyesno("Onay","Müşteriyi silmek istiyor musun?"): return
            custs.pop(idx)
            u_save(CUSTOMERS_FILE, self.current_user, custs)
            self.cust_sel.delete(0,"end")
            self._refresh_customers()
        except ValueError:
            messagebox.showerror("Hata","Sayı gir.")

    def _refresh_customers(self):
        custs = u_load(CUSTOMERS_FILE, self.current_user)
        sales = u_load(SALES_FILE,     self.current_user)
        self.cust_box.configure(state="normal")
        self.cust_box.delete("0.0","end")
        if not custs:
            self.cust_box.insert("0.0","  Müşteri yok.\n")
        else:
            for i,c in enumerate(custs,1):
                name    = c.get("ad","")
                c_sales = [s for s in sales if s.get("musteri","") == name]
                c_total = sum(s.get("satis_fiyati",0) for s in c_sales)
                c_kar   = sum(s.get("kar",0) for s in c_sales)
                self.cust_box.insert("end",
                    f"[{i:02d}] {name}\n"
                    f"     Tel      : {c.get('telefon','–')}\n"
                    f"     E-posta  : {c.get('email','–')}\n"
                    f"     Adres    : {c.get('adres','–')}\n"
                    f"     Not      : {c.get('not','–')}\n"
                    f"     Alışveriş: {len(c_sales)} satış  "
                    f"→  {c_total:,.2f} TL  (Kar: {c_kar:,.2f} TL)\n"
                    f"     Kayıt    : {c.get('kayit','–')}\n"
                    + "─"*55 + "\n")
        self.cust_box.configure(state="disabled")

    # ══════════════════════════════════════════════════════════
    #  SEKME 6: GÖREVLER (TO-DO)
    # ══════════════════════════════════════════════════════════

    def show_tasks_tab(self):
        self.clear_main()
        self._page_header("✅","Görev Listesi","Atölye iş takibi")

        main = ctk.CTkFrame(self.main_area, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=8)

        lc = make_card(main, width=360)
        lc.pack(side="left", fill="y", padx=(0,12))
        lc.pack_propagate(False)

        ctk.CTkLabel(lc, text="YENİ GÖREV",
                     font=ctk.CTkFont(family="Courier", size=15, weight="bold"),
                     text_color=ACCENT).pack(pady=(18,10))

        self.task_title  = mini_entry(lc, "Görev başlığı *", width=310)
        self.task_title.pack(pady=5, padx=18)
        self.task_detail = mini_entry(lc, "Detay", width=310)
        self.task_detail.pack(pady=5, padx=18)
        self.task_due    = mini_entry(lc, "Son tarih (GG.AA.YYYY)", width=310)
        self.task_due.pack(pady=5, padx=18)

        ctk.CTkLabel(lc, text="Öncelik", text_color="#8B949E",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=18)
        self.task_prio = mini_combo(lc,["🔴 Yüksek","🟡 Orta","🟢 Düşük"], width=310)
        self.task_prio.set("🟡 Orta")
        self.task_prio.pack(pady=5, padx=18)

        accent_btn(lc,"➕ Görev Ekle", self._add_task, height=40, width=310).pack(pady=(12,4), padx=18)
        self.task_info = ctk.CTkLabel(lc, text="", wraplength=290, font=ctk.CTkFont(size=12))
        self.task_info.pack(pady=6)

        rc = make_card(main)
        rc.pack(side="right", fill="both", expand=True)

        rhdr = ctk.CTkFrame(rc, fg_color="transparent")
        rhdr.pack(fill="x", padx=16, pady=(14,6))
        ctk.CTkLabel(rhdr, text="GÖREVLER",
                     font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
                     text_color=ACCENT).pack(side="left")

        btn_f = ctk.CTkFrame(rhdr, fg_color="transparent")
        btn_f.pack(side="right")
        success_btn(btn_f,"✓ Tamamlandı", self._complete_task, height=34, width=120).pack(side="left", padx=4)
        danger_btn(btn_f,"🗑 Sil",        self._del_task,      height=34, width=80).pack(side="left")

        self.task_box = ctk.CTkTextbox(rc, corner_radius=10, fg_color="#0D1117",
                                       font=ctk.CTkFont(family="Courier", size=12))
        self.task_box.pack(fill="both", expand=True, padx=16, pady=(0,6))

        self.task_sel = mini_entry(rc, "İşlem yapılacak görev no", height=34)
        self.task_sel.pack(fill="x", padx=16, pady=(0,12))

        self._refresh_tasks()

    def _add_task(self):
        title = self.task_title.get().strip()
        if not title:
            self.task_info.configure(text="✗ Başlık boş.", text_color=DANGER); return
        tasks = u_load(TASKS_FILE, self.current_user)
        tasks.append({
            "owner": self.current_user,
            "baslik":  title,
            "detay":   self.task_detail.get().strip(),
            "son_tarih": self.task_due.get().strip(),
            "oncelik": self.task_prio.get(),
            "durum":   "Bekliyor",
            "tarih":   datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        u_save(TASKS_FILE, self.current_user, tasks)
        self.task_info.configure(text="✓ Görev eklendi.", text_color=SUCCESS)
        for attr in ["task_title","task_detail","task_due"]:
            getattr(self,attr).delete(0,"end")
        self._refresh_tasks()

    def _complete_task(self):
        try:
            idx   = int(self.task_sel.get().strip()) - 1
            tasks = u_load(TASKS_FILE, self.current_user)
            if idx < 0 or idx >= len(tasks):
                messagebox.showerror("Hata","Geçersiz no."); return
            tasks[idx]["durum"] = "✅ Tamamlandı"
            u_save(TASKS_FILE, self.current_user, tasks)
            self.task_sel.delete(0,"end")
            self._refresh_tasks()
        except ValueError:
            messagebox.showerror("Hata","Sayı gir.")

    def _del_task(self):
        try:
            idx   = int(self.task_sel.get().strip()) - 1
            tasks = u_load(TASKS_FILE, self.current_user)
            if idx < 0 or idx >= len(tasks):
                messagebox.showerror("Hata","Geçersiz no."); return
            tasks.pop(idx)
            u_save(TASKS_FILE, self.current_user, tasks)
            self.task_sel.delete(0,"end")
            self._refresh_tasks()
        except ValueError:
            messagebox.showerror("Hata","Sayı gir.")

    def _refresh_tasks(self):
        tasks = u_load(TASKS_FILE, self.current_user)
        self.task_box.configure(state="normal")
        self.task_box.delete("0.0","end")
        if not tasks:
            self.task_box.insert("0.0","  Görev yok.\n")
        else:
            bekleyen = [t for t in tasks if t.get("durum","") != "✅ Tamamlandı"]
            tamamlanan = [t for t in tasks if t.get("durum","") == "✅ Tamamlandı"]
            for grp, grp_tasks in [("BEKLEYEN", bekleyen),("TAMAMLANAN", tamamlanan)]:
                if grp_tasks:
                    self.task_box.insert("end", f"\n── {grp} ──────────────────\n")
                    for i_g, t in enumerate(grp_tasks,1):
                        idx_global = tasks.index(t) + 1
                        self.task_box.insert("end",
                            f"[{idx_global:02d}] {t.get('oncelik','–')}  {t.get('baslik','–')}\n"
                            f"     Detay      : {t.get('detay','–')}\n"
                            f"     Son Tarih  : {t.get('son_tarih','–')}\n"
                            f"     Durum      : {t.get('durum','Bekliyor')}\n"
                            + "─"*45 + "\n")
        self.task_box.configure(state="disabled")

    # ══════════════════════════════════════════════════════════
    #  SEKME 7: NOTLAR
    # ══════════════════════════════════════════════════════════

    def show_notes_tab(self):
        self.clear_main()
        self._page_header("📝","Atölye Notları","Hızlı not alma & referans")

        main = ctk.CTkFrame(self.main_area, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=8)

        lc = make_card(main, width=360)
        lc.pack(side="left", fill="y", padx=(0,12))
        lc.pack_propagate(False)

        ctk.CTkLabel(lc, text="YENİ NOT",
                     font=ctk.CTkFont(family="Courier", size=15, weight="bold"),
                     text_color=ACCENT).pack(pady=(18,10))

        self.note_title = mini_entry(lc, "Başlık", width=310)
        self.note_title.pack(pady=5, padx=18)

        ctk.CTkLabel(lc, text="Etiket", text_color="#8B949E",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=18)
        self.note_tag = mini_combo(lc,
            ["Genel","Teknik","Müşteri","Fikir","Hatırlatma"], width=310)
        self.note_tag.set("Genel")
        self.note_tag.pack(pady=5, padx=18)

        ctk.CTkLabel(lc, text="Not İçeriği", text_color="#8B949E",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=18, pady=(8,2))
        self.note_body = ctk.CTkTextbox(lc, height=200, corner_radius=10,
                                        fg_color="#0D1117",
                                        font=ctk.CTkFont(size=13))
        self.note_body.pack(fill="x", padx=18)

        accent_btn(lc,"💾 Notu Kaydet", self._add_note, height=40, width=310).pack(pady=(12,4), padx=18)
        self.note_info = ctk.CTkLabel(lc, text="", wraplength=290, font=ctk.CTkFont(size=12))
        self.note_info.pack(pady=6)

        rc = make_card(main)
        rc.pack(side="right", fill="both", expand=True)

        rhdr = ctk.CTkFrame(rc, fg_color="transparent")
        rhdr.pack(fill="x", padx=16, pady=(14,6))
        ctk.CTkLabel(rhdr, text="NOTLAR",
                     font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
                     text_color=ACCENT).pack(side="left")
        danger_btn(rhdr,"🗑 Sil", self._del_note, height=34, width=80).pack(side="right")

        self.notes_box = ctk.CTkTextbox(rc, corner_radius=10, fg_color="#0D1117",
                                        font=ctk.CTkFont(family="Courier", size=12))
        self.notes_box.pack(fill="both", expand=True, padx=16, pady=(0,6))

        self.note_sel = mini_entry(rc, "Silmek için not no", height=34)
        self.note_sel.pack(fill="x", padx=16, pady=(0,12))

        self._refresh_notes()

    def _add_note(self):
        title = self.note_title.get().strip()
        body  = self.note_body.get("0.0","end").strip()
        tag   = self.note_tag.get()
        if not body:
            self.note_info.configure(text="✗ İçerik boş.", text_color=DANGER); return
        notes = u_load(NOTES_FILE, self.current_user)
        notes.append({
            "owner":  self.current_user,
            "baslik": title or "—",
            "icerik": body,
            "etiket": tag,
            "tarih":  datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        u_save(NOTES_FILE, self.current_user, notes)
        self.note_info.configure(text="✓ Not kaydedildi.", text_color=SUCCESS)
        self.note_title.delete(0,"end")
        self.note_body.delete("0.0","end")
        self._refresh_notes()

    def _del_note(self):
        try:
            idx   = int(self.note_sel.get().strip()) - 1
            notes = u_load(NOTES_FILE, self.current_user)
            if idx < 0 or idx >= len(notes):
                messagebox.showerror("Hata","Geçersiz no."); return
            notes.pop(idx)
            u_save(NOTES_FILE, self.current_user, notes)
            self.note_sel.delete(0,"end")
            self._refresh_notes()
        except ValueError:
            messagebox.showerror("Hata","Sayı gir.")

    def _refresh_notes(self):
        notes = u_load(NOTES_FILE, self.current_user)
        self.notes_box.configure(state="normal")
        self.notes_box.delete("0.0","end")
        if not notes:
            self.notes_box.insert("0.0","  Not yok.\n")
        else:
            tag_icons = {"Genel":"📄","Teknik":"🔧","Müşteri":"👤",
                         "Fikir":"💡","Hatırlatma":"🔔"}
            for i,n in enumerate(notes,1):
                icon = tag_icons.get(n.get("etiket",""),"📄")
                self.notes_box.insert("end",
                    f"[{i:02d}] {icon} {n.get('etiket','–')}  ·  {n.get('baslik','–')}\n"
                    f"     {n.get('tarih','–')}\n\n"
                    f"{n.get('icerik','')}\n\n"
                    + "─"*55 + "\n\n")
        self.notes_box.configure(state="disabled")

    # ══════════════════════════════════════════════════════════
    #  SEKME 8: İSTATİSTİKLER
    # ══════════════════════════════════════════════════════════

    def show_stats_tab(self):
        self.clear_main()
        self._page_header("📉","İstatistikler","Detaylı analiz & raporlar")

        scroll = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=8)

        projects  = self.get_all_projects()
        sales     = u_load(SALES_FILE,    self.current_user)
        expenses  = u_load(EXPENSES_FILE, self.current_user)
        stock     = load_stock()

        # ── Filament kullanım grafiği ─────────────────────────
        section_label(scroll, "🧵 Filament Kullanımı (gram)")
        fil_use = {}
        for p in projects:
            f = p.get("filament_turu","PLA")
            fil_use[f] = fil_use.get(f,0) + p.get("gram",0)

        bar_card = make_card(scroll)
        bar_card.pack(fill="x", pady=(0,8))
        if fil_use:
            row_charts = ctk.CTkFrame(bar_card, fg_color="transparent")
            row_charts.pack(fill="x", padx=10, pady=10)
            # Bar grafik
            bc = ctk.CTkFrame(row_charts, fg_color="transparent")
            bc.pack(side="left", fill="both", expand=True)
            ctk.CTkLabel(bc, text="Bar Grafik", text_color="#8B949E",
                         font=ctk.CTkFont(size=11)).pack()
            MiniBarChart(bc, fil_use, color=ACCENT, height=100)
            # Donut grafik
            dc = ctk.CTkFrame(row_charts, fg_color="transparent", width=170)
            dc.pack(side="right", fill="y", padx=(10,0))
            dc.pack_propagate(False)
            ctk.CTkLabel(dc, text="Donut", text_color="#8B949E",
                         font=ctk.CTkFont(size=11)).pack()
            DonutChart(dc, fil_use, size=155)
            # Tablo
            tb = ctk.CTkTextbox(bar_card, height=120, corner_radius=8,
                                fg_color="#0D1117",
                                font=ctk.CTkFont(family="Courier", size=12))
            tb.pack(fill="x", padx=10, pady=(0,10))
            total_fil = sum(fil_use.values())
            tb.insert("end",f"{'Filament':<22}{'Gram':>10}{'Oran':>8}{'Maliyet':>14}\n" + "─"*56+"\n")
            for f,g in sorted(fil_use.items(),key=lambda x:x[1],reverse=True):
                fiyat = FILAMENT_FIYATLAR.get(f,0)
                mal   = (g/1000)*fiyat
                oran  = (g/total_fil*100) if total_fil else 0
                tb.insert("end",f"{f:<22}{g:>8.0f} g{oran:>7.1f}%{mal:>11.2f} TL\n")
            tb.configure(state="disabled")
        else:
            ctk.CTkLabel(bar_card, text="Veri yok.", text_color="#555").pack(pady=20)

        # ── Aylık özet ─────────────────────────────────────────
        section_label(scroll, "📅 Bu Ayki Özet")
        now = datetime.now()
        this_m = f"{now.month:02d}.{now.year}"
        def in_m(x): 
            try: return x.get("tarih","")[3:10] == this_m
            except: return False

        m_prj  = [p for p in projects  if in_m(p)]
        m_sal  = [s for s in sales     if in_m(s)]
        m_exp  = [e for e in expenses  if in_m(e)]

        month_card = make_card(scroll)
        month_card.pack(fill="x", pady=(0,8))
        mc_inner = ctk.CTkFrame(month_card, fg_color="transparent")
        mc_inner.pack(fill="x", padx=16, pady=14)

        for label, val, col in [
            ("Yeni Proje",    str(len(m_prj)),                                  ACCENT),
            ("Proje Maliyet", f"{sum(p.get('toplam_maliyet',0) for p in m_prj):,.2f} TL", "#C9D1D9"),
            ("Satış Geliri",  f"{sum(s.get('satis_fiyati',0) for s in m_sal):,.2f} TL",   SUCCESS),
            ("Giderler",      f"{sum(e.get('tutar',0) for e in m_exp):,.2f} TL",          DANGER),
            ("Net Kar",       f"{sum(s.get('satis_fiyati',0) for s in m_sal)-sum(p.get('toplam_maliyet',0) for p in m_prj)-sum(e.get('tutar',0) for e in m_exp):,.2f} TL",
             SUCCESS),
        ]:
            f = ctk.CTkFrame(mc_inner, fg_color="#0D1117", corner_radius=10)
            f.pack(side="left", expand=True, fill="x", padx=5)
            ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=11),
                         text_color="#8B949E").pack(pady=(8,2))
            ctk.CTkLabel(f, text=val,
                         font=ctk.CTkFont(family="Courier",size=15,weight="bold"),
                         text_color=col).pack(pady=(0,8))

        # ── Stok değer analizi ─────────────────────────────────
        section_label(scroll, "💎 Stok Değer Analizi")
        stk_card = make_card(scroll)
        stk_card.pack(fill="x", pady=(0,8))

        stk_inner = ctk.CTkFrame(stk_card, fg_color="transparent")
        stk_inner.pack(fill="x", padx=10, pady=10)

        stk_nonempty = {k:v for k,v in stock.items() if v > 0}
        if stk_nonempty:
            dc2 = ctk.CTkFrame(stk_inner, fg_color="transparent", width=160)
            dc2.pack(side="left", fill="y")
            dc2.pack_propagate(False)
            DonutChart(dc2, stk_nonempty, size=150)

        stk_tb = ctk.CTkTextbox(stk_inner, height=160, corner_radius=8,
                                fg_color="#0D1117",
                                font=ctk.CTkFont(family="Courier", size=12))
        stk_tb.pack(side="right", fill="both", expand=True, padx=(10,0))
        total_stk_val = 0
        stk_tb.insert("end",f"{'Filament':<22}{'Stok':>10}{'Birim':>12}{'Değer':>14}\n"+"─"*58+"\n")
        for f,g in sorted(stock.items(), key=lambda x:x[1], reverse=True):
            fp  = FILAMENT_FIYATLAR.get(f,0)
            val = (g/1000)*fp
            total_stk_val += val
            stk_tb.insert("end",f"{f:<22}{g:>8.0f} g{fp:>9} TL/kg{val:>11.2f} TL\n")
        stk_tb.insert("end","─"*58+f"\n{'TOPLAM STOK DEĞERİ':<44}{total_stk_val:>11.2f} TL\n")
        stk_tb.configure(state="disabled")

        # ── En çok satan ──────────────────────────────────────
        section_label(scroll, "🏆 En Çok Satan Ürünler (Top 5)")
        top_card = make_card(scroll)
        top_card.pack(fill="x", pady=(0,8))
        urun_totals = {}
        for s in sales:
            u = s.get("urun","–")
            urun_totals[u] = urun_totals.get(u,0) + s.get("satis_fiyati",0)
        if urun_totals:
            top5 = sorted(urun_totals.items(), key=lambda x:x[1], reverse=True)[:5]
            MiniBarChart(top_card, dict(top5), color=SUCCESS, height=90)
            for rank,(u,t) in enumerate(top5,1):
                row = ctk.CTkFrame(top_card, fg_color="transparent")
                row.pack(fill="x", padx=14, pady=2)
                ctk.CTkLabel(row,
                    text=f"{'🥇🥈🥉🏅🏅'[rank-1]}  {rank}. {u}",
                    font=ctk.CTkFont(size=13), anchor="w",
                    text_color="#C9D1D9").pack(side="left")
                ctk.CTkLabel(row, text=f"{t:,.2f} TL",
                             font=ctk.CTkFont(family="Courier",size=13,weight="bold"),
                             text_color=SUCCESS).pack(side="right")
            ctk.CTkLabel(top_card, text="").pack(pady=4)
        else:
            ctk.CTkLabel(top_card, text="Satış yok.", text_color="#555").pack(pady=16)

        # ── Yazıcı istatistikleri ─────────────────────────────
        section_label(scroll, "🖨️ Yazıcı Kullanım İstatistikleri")
        prn_card = make_card(scroll)
        prn_card.pack(fill="x", pady=(0,20))
        pstats = {}
        for p in projects:
            k = f"{p.get('yazici_marka','–')} {p.get('yazici_model','–')}"
            pstats.setdefault(k,{"proje":0,"gram":0,"sure":0,"maliyet":0})
            pstats[k]["proje"]  += 1
            pstats[k]["gram"]   += p.get("gram",0)
            pstats[k]["sure"]   += p.get("sure",0)
            pstats[k]["maliyet"]+= p.get("toplam_maliyet",0)
        if pstats:
            ptb = ctk.CTkTextbox(prn_card, height=180, corner_radius=8,
                                 fg_color="#0D1117",
                                 font=ctk.CTkFont(family="Courier", size=12))
            ptb.pack(fill="x", padx=14, pady=14)
            ptb.insert("end",
                f"{'Yazıcı':<32}{'Proje':>8}{'Gram':>12}{'Süre':>10}{'Maliyet':>14}\n"
                + "═"*78+"\n")
            for prn,st in sorted(pstats.items(), key=lambda x:x[1]["proje"], reverse=True):
                ptb.insert("end",
                    f"{prn:<32}{st['proje']:>6} prj{st['gram']:>10.0f} g"
                    f"{st['sure']:>8.1f} h{st['maliyet']:>11.2f} TL\n")
            ptb.configure(state="disabled")
        else:
            ctk.CTkLabel(prn_card, text="Proje yok.", text_color="#555").pack(pady=16)

    # ══════════════════════════════════════════════════════════
    #  SEKME 9: AKTİVİTE LOGU
    # ══════════════════════════════════════════════════════════

    def show_log_tab(self):
        self.clear_main()
        self._page_header("📋","Aktivite Logu","Tüm işlem kayıtları")

        top = ctk.CTkFrame(self.main_area, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(0,8))
        accent_btn(top,"🔃 Yenile", self._refresh_log, height=34, width=100).pack(side="right")
        danger_btn(top,"🗑 Tüm Logu Temizle", self._clear_log, height=34, width=160).pack(side="right", padx=8)

        log_card = make_card(self.main_area)
        log_card.pack(fill="both", expand=True, padx=20, pady=(0,20))

        self.log_box = ctk.CTkTextbox(log_card, corner_radius=10,
                                      fg_color="#0D1117",
                                      font=ctk.CTkFont(family="Courier", size=12))
        self.log_box.pack(fill="both", expand=True, padx=14, pady=14)
        self._refresh_log()

    def _refresh_log(self):
        logs = load_logs(self.current_user)
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0","end")
        if not logs:
            self.log_box.insert("0.0","  Log kaydı yok.\n")
        else:
            for l in reversed(logs):
                action = l.get("action","")
                col_map = {
                    "GİRİŞ":              "▶",
                    "PROJE EKLENDİ":      "➕",
                    "PROJE SİLİNDİ":      "🗑",
                    "PROJE GÜNCELLENDİ":  "✏️",
                    "STOK GÜNCELLENDİ":   "📦",
                    "SATIŞ KAYDEDİLDİ":   "💰",
                    "GİDER KAYDEDİLDİ":   "📤",
                    "MÜŞTERİ EKLENDİ":    "👥",
                }
                icon = col_map.get(action,"·")
                self.log_box.insert("end",
                    f"{l.get('tarih','–')}  {icon}  {action}\n"
                    f"  {l.get('detail','')}\n"
                    + "─"*55 + "\n")
        self.log_box.configure(state="disabled")

    def _clear_log(self):
        if messagebox.askyesno("Onay","Tüm logu silmek istiyor musun?"):
            all_logs = load_json(LOG_FILE,[])
            others   = [l for l in all_logs if l.get("owner") != self.current_user]
            save_json(LOG_FILE, others)
            self._refresh_log()

    # ══════════════════════════════════════════════════════════
    #  SEKME 10: AYARLAR
    # ══════════════════════════════════════════════════════════

    def show_settings_tab(self):
        self.clear_main()
        self._page_header("⚙️","Ayarlar","Sistem & tercihler")

        scroll = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=8)

        # ── Elektrik ──────────────────────────────────────────
        section_label(scroll, "⚡ Elektrik Fiyatı")
        ep = make_card(scroll)
        ep.pack(fill="x", pady=(0,10))
        er = ctk.CTkFrame(ep, fg_color="transparent")
        er.pack(padx=18, pady=16, fill="x")
        ctk.CTkLabel(er, text="TL/kWh :", text_color="#8B949E").pack(side="left")
        self.settings_electric = mini_entry(er, "Örn: 1.73", width=200)
        self.settings_electric.insert(0, str(get_electric_price()))
        self.settings_electric.pack(side="left", padx=10)
        accent_btn(er,"Kaydet", self._save_electric, height=36, width=100).pack(side="left")

        # ── Filament fiyatları ─────────────────────────────────
        section_label(scroll, "🧵 Filament Birim Fiyatları (TL/kg)")
        fp = make_card(scroll)
        fp.pack(fill="x", pady=(0,10))
        ctk.CTkLabel(fp, text="Değişiklikler yalnızca yeni projeler için geçerlidir.",
                     text_color=WARNING, font=ctk.CTkFont(size=12)).pack(anchor="w", padx=18, pady=(12,6))

        self.fil_entries = {}
        cols_f = ctk.CTkFrame(fp, fg_color="transparent")
        cols_f.pack(fill="x", padx=18, pady=(0,10))
        items = list(FILAMENT_FIYATLAR.items())
        half  = math.ceil(len(items)/2)
        for col_i, (c_items) in enumerate([items[:half], items[half:]]):
            col_frame = ctk.CTkFrame(cols_f, fg_color="transparent")
            col_frame.pack(side="left", fill="both", expand=True, padx=(0,10 if col_i==0 else 0))
            for fil, fiyat in c_items:
                row = ctk.CTkFrame(col_frame, fg_color="transparent")
                row.pack(fill="x", pady=3)
                ctk.CTkLabel(row, text=f"{fil}:", width=170, anchor="w",
                             text_color="#C9D1D9").pack(side="left")
                e = mini_entry(row, "", width=110)
                e.insert(0, str(fiyat))
                e.pack(side="left")
                ctk.CTkLabel(row, text="TL/kg", text_color="#8B949E").pack(side="left", padx=4)
                self.fil_entries[fil] = e
        accent_btn(fp,"💾 Filament Fiyatlarını Güncelle",
                   self._save_fil_prices, height=38).pack(pady=(0,14), padx=18)

        # ── Görünüm ────────────────────────────────────────────
        section_label(scroll, "🎨 Görünüm")
        th = make_card(scroll)
        th.pack(fill="x", pady=(0,10))
        th_row = ctk.CTkFrame(th, fg_color="transparent")
        th_row.pack(padx=18, pady=16, fill="x")
        ctk.CTkButton(th_row, text="🌙 Koyu Tema", height=38, width=160,
                      command=lambda: ctk.set_appearance_mode("dark")).pack(side="left", padx=(0,10))
        ctk.CTkButton(th_row, text="☀️ Açık Tema", height=38, width=160,
                      command=lambda: ctk.set_appearance_mode("light")).pack(side="left")

        # ── Veri yönetimi ─────────────────────────────────────
        section_label(scroll, "🗄️ Veri Yönetimi")
        dm = make_card(scroll)
        dm.pack(fill="x", pady=(0,20))
        dm_row = ctk.CTkFrame(dm, fg_color="transparent")
        dm_row.pack(padx=18, pady=16, fill="x")
        accent_btn(dm_row,"📊 Özet Rapor", self._summary_report,
                   height=38, width=160).pack(side="left", padx=(0,10))
        accent_btn(dm_row,"📥 Tüm Veriyi CSV", self._export_all_csv,
                   color="#1C4370", hover="#1a3a6b",
                   height=38, width=160).pack(side="left", padx=(0,10))
        danger_btn(dm_row,"🗑 Tüm Projeler", self._delete_all_projects,
                   height=38, width=160).pack(side="left")

        # ── Şifre değiştir ─────────────────────────────────────
        section_label(scroll, "🔐 Şifre Değiştir")
        pw = make_card(scroll)
        pw.pack(fill="x", pady=(0,20))
        pw_inner = ctk.CTkFrame(pw, fg_color="transparent")
        pw_inner.pack(padx=18, pady=16, fill="x")
        self.pw_old  = mini_entry(pw_inner, "Mevcut şifre", show="*", width=200)
        self.pw_new  = mini_entry(pw_inner, "Yeni şifre",   show="*", width=200)
        self.pw_new2 = mini_entry(pw_inner, "Tekrar",       show="*", width=200)
        for e in [self.pw_old, self.pw_new, self.pw_new2]:
            e.pack(side="left", padx=(0,8))
        accent_btn(pw_inner,"Değiştir", self._change_password,
                   height=38, width=120).pack(side="left")
        self.pw_info = ctk.CTkLabel(pw, text="", font=ctk.CTkFont(size=12))
        self.pw_info.pack(pady=(0,10))

    def _save_electric(self):
        try:
            v = float(self.settings_electric.get().strip().replace(",","."))
            if v <= 0: raise ValueError
            set_electric_price(v)
            messagebox.showinfo("Başarılı",f"Elektrik fiyatı {v} TL/kWh kaydedildi.")
        except ValueError:
            messagebox.showerror("Hata","Geçerli pozitif sayı gir.")

    def _save_fil_prices(self):
        try:
            for fil, e in self.fil_entries.items():
                v = float(e.get().strip().replace(",","."))
                if v > 0: FILAMENT_FIYATLAR[fil] = v
            messagebox.showinfo("Başarılı","Filament fiyatları güncellendi (bu oturum için).")
        except ValueError:
            messagebox.showerror("Hata","Tüm fiyatlar geçerli sayı olmalı.")

    def _save_electric_setting(self): self._save_electric()
    def _save_filament_prices(self): self._save_fil_prices()

    def _summary_report(self):
        projects  = self.get_all_projects()
        sales     = u_load(SALES_FILE,    self.current_user)
        expenses  = u_load(EXPENSES_FILE, self.current_user)
        customers = u_load(CUSTOMERS_FILE, self.current_user)
        stock     = load_stock()

        t_mal  = sum(p.get("toplam_maliyet",0) for p in projects)
        t_sat  = sum(s.get("satis_fiyati",0) for s in sales)
        t_gid  = sum(e.get("tutar",0) for e in expenses)
        net    = t_sat - t_mal - t_gid
        t_stk  = sum(stock.values())
        t_sval = sum((g/1000)*FILAMENT_FIYATLAR.get(f,0) for f,g in stock.items())

        report = (
            "╔" + "═"*43 + "╗\n"
            f"║   ATÖLYE ÖZET RAPORU  —  {self.current_user:<15}║\n"
            f"║   {datetime.now().strftime('%d.%m.%Y %H:%M'):<38}║\n"
            "╠" + "═"*43 + "╣\n"
            f"║  Toplam Proje     : {len(projects):<23}║\n"
            f"║  Proje Maliyeti   : {t_mal:>10,.2f} TL{'':>10}║\n"
            f"║  Toplam Satış     : {t_sat:>10,.2f} TL{'':>10}║\n"
            f"║  Toplam Gider     : {t_gid:>10,.2f} TL{'':>10}║\n"
            f"║  NET KAR / ZARAR  : {net:>10,.2f} TL{'':>10}║\n"
            "╠" + "═"*43 + "╣\n"
            f"║  Müşteri Sayısı   : {len(customers):<23}║\n"
            f"║  Satış Sayısı     : {len(sales):<23}║\n"
            f"║  Gider Sayısı     : {len(expenses):<23}║\n"
            "╠" + "═"*43 + "╣\n"
            f"║  Toplam Stok      : {t_stk:>10,.0f} g{'':>12}║\n"
            f"║  Stok Değeri      : {t_sval:>10,.2f} TL{'':>10}║\n"
            "╚" + "═"*43 + "╝\n"
        )

        win = ctk.CTkToplevel(self)
        win.title("Özet Rapor")
        win.geometry("520x460")
        win.configure(fg_color=BG_DARK)
        ctk.CTkLabel(win, text="📊 ÖZET RAPOR",
                     font=ctk.CTkFont(family="Courier", size=18, weight="bold"),
                     text_color=ACCENT).pack(pady=(16,8))
        tb = ctk.CTkTextbox(win, fg_color="#0D1117",
                            font=ctk.CTkFont(family="Courier", size=13))
        tb.pack(fill="both", expand=True, padx=16, pady=(0,16))
        tb.insert("end", report)
        tb.configure(state="disabled")

    def _export_all_csv(self):
        """Tüm verileri tek bir CSV dosyasına aktar."""
        projects = self.get_all_projects()
        path = f"tum_veri_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(path,"w",encoding="utf-8",newline="") as f:
            w = csv.writer(f)
            w.writerow(["=== PROJELER ==="])
            w.writerow(["Model","Kategori","Filament","Gram","Süre","Maliyet","Durum","Tarih"])
            for p in projects:
                w.writerow([p.get("model_adi",""), p.get("kategori",""),
                            p.get("filament_turu",""), p.get("gram",0),
                            p.get("sure",0), p.get("toplam_maliyet",0),
                            p.get("durum",""), p.get("tarih","")])
            w.writerow([])
            w.writerow(["=== SATIŞLAR ==="])
            sales = u_load(SALES_FILE, self.current_user)
            w.writerow(["Ürün","Müşteri","Fiyat","Adet","Kar","Tarih"])
            for s in sales:
                w.writerow([s.get("urun",""), s.get("musteri",""),
                            s.get("satis_fiyati",0), s.get("adet",1),
                            s.get("kar",0), s.get("tarih","")])
        messagebox.showinfo("CSV","Tüm veri dışa aktarıldı:\n"+path)

    def _delete_all_projects(self):
        if messagebox.askyesno("DİKKAT!",
            "Tüm projelerini silmek istiyor musun?\nBu işlem geri ALINAMAZ."):
            self.save_user_projects([])
            messagebox.showinfo("Başarılı","Tüm projeler silindi.")

    def _change_password(self):
        old  = self.pw_old.get().strip()
        new  = self.pw_new.get().strip()
        new2 = self.pw_new2.get().strip()
        if not old or not new:
            self.pw_info.configure(text="✗ Alanlar boş.", text_color=DANGER); return
        if len(new) < 4:
            self.pw_info.configure(text="✗ En az 4 karakter.", text_color=DANGER); return
        if new != new2:
            self.pw_info.configure(text="✗ Şifreler eşleşmiyor.", text_color=DANGER); return
        users = load_json(USERS_FILE,[])
        changed = False
        for u in users:
            if u["username"] == self.current_user and u["password"] == old:
                u["password"] = new
                changed = True
                break
        if not changed:
            self.pw_info.configure(text="✗ Mevcut şifre yanlış.", text_color=DANGER); return
        save_json(USERS_FILE, users)
        log_activity(self.current_user,"ŞİFRE DEĞİŞTİRİLDİ","")
        self.pw_info.configure(text="✓ Şifre güncellendi.", text_color=SUCCESS)
        for e in [self.pw_old, self.pw_new, self.pw_new2]:
            e.delete(0,"end")

    # ── Uyumluluk alias'ları (v2 ile geriye dönük) ─────────
    def show_main_tab(self):
        self.clear_main()
        self._page_header("📊","Dashboard","Genel bakış & hızlı işlemler")
        scroll = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=0)
        self._build_dashboard_content(scroll)

    def _build_dashboard_content(self, scroll):
        projects  = self.get_all_projects()
        sales     = u_load(SALES_FILE,    self.current_user)
        expenses  = u_load(EXPENSES_FILE, self.current_user)
        customers = u_load(CUSTOMERS_FILE, self.current_user)
        stock     = load_stock()
        threshold = get_low_stock_threshold()

        t_mal   = sum(p.get("toplam_maliyet",0) for p in projects)
        t_satis = sum(s.get("satis_fiyati",0) for s in sales)
        t_gider = sum(e.get("tutar",0) for e in expenses)
        net_kar = t_satis - t_mal - t_gider
        t_stok  = sum(stock.values())
        dusuk   = sum(1 for v in stock.values() if 0 < v < threshold)

        kpis_r1 = [
            ("📋","Proje",         str(len(projects)),         "#C9D1D9"),
            ("💸","Proje Maliyet", f"{t_mal:,.2f} TL",         "#C9D1D9"),
            ("🛒","Toplam Satış",  f"{t_satis:,.2f} TL",       SUCCESS),
            ("✅","Net Kar",       f"{net_kar:,.2f} TL",
             SUCCESS if net_kar >= 0 else DANGER),
            ("📤","Toplam Gider",  f"{t_gider:,.2f} TL",       DANGER),
        ]
        kpis_r2 = [
            ("📦","Toplam Stok",   f"{t_stok:,.0f} g",         ACCENT),
            ("⚠️","Düşük Stok",   f"{dusuk} ürün",
             WARNING if dusuk else SUCCESS),
            ("👥","Müşteri",       str(len(customers)),         ACCENT2),
            ("🛍️","Satış Adedi",  str(len(sales)),             "#C9D1D9"),
            ("📝","Not",           str(len(u_load(NOTES_FILE, self.current_user))), "#C9D1D9"),
        ]

        for row_data in [kpis_r1, kpis_r2]:
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=4)
            for icon,label,val,col in row_data:
                card = make_card(row, height=100)
                card.pack(side="left", expand=True, fill="x", padx=5)
                card.pack_propagate(False)
                ctk.CTkLabel(card, text=icon,
                             font=ctk.CTkFont(size=18)).pack(pady=(10,2))
                ctk.CTkLabel(card, text=label,
                             font=ctk.CTkFont(size=11), text_color="#8B949E").pack()
                ctk.CTkLabel(card, text=val,
                             font=ctk.CTkFont(family="Courier",size=15,weight="bold"),
                             text_color=col).pack(pady=(2,8))

        # Form + liste
        mid = ctk.CTkFrame(scroll, fg_color="transparent")
        mid.pack(fill="both", expand=True, pady=8)

        form_card = make_card(mid, width=370)
        form_card.pack(side="left", fill="y", padx=(0,10))
        form_card.pack_propagate(False)
        fc = ctk.CTkScrollableFrame(form_card, fg_color="transparent")
        fc.pack(fill="both", expand=True, padx=4, pady=4)

        ctk.CTkLabel(fc, text="➕  YENİ PROJE",
                     font=ctk.CTkFont(family="Courier", size=15, weight="bold"),
                     text_color=ACCENT).pack(pady=(12,8))

        self.entry_model    = mini_entry(fc, "Model adı *",           width=330)
        self.entry_model.pack(pady=4, padx=10)
        self.entry_category = mini_entry(fc, "Kategori *",            width=330)
        self.entry_category.pack(pady=4, padx=10)
        self.entry_color    = mini_entry(fc, "Renk *",                width=330)
        self.entry_color.pack(pady=4, padx=10)
        self.entry_gram     = mini_entry(fc, "Kullanılan gram *",      width=330)
        self.entry_gram.pack(pady=4, padx=10)
        self.entry_time     = mini_entry(fc, "Baskı süresi (saat)",   width=330)
        self.entry_time.insert(0,"0")
        self.entry_time.pack(pady=4, padx=10)
        self.entry_note     = mini_entry(fc, "Kısa not",               width=330)
        self.entry_note.pack(pady=4, padx=10)
        self.entry_elektrik = mini_entry(fc, "Elektrik TL/kWh",       width=330)
        self.entry_elektrik.insert(0, str(get_electric_price()))
        self.entry_elektrik.pack(pady=4, padx=10)

        ctk.CTkLabel(fc, text="Filament", text_color="#8B949E",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.combo_filament = mini_combo(fc, list(FILAMENT_FIYATLAR.keys()), width=330)
        self.combo_filament.set("PLA")
        self.combo_filament.pack(pady=4, padx=10)

        ctk.CTkLabel(fc, text="Yazıcı Markası", text_color="#8B949E",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.combo_brand = mini_combo(fc, list(YAZICI_KATALOGU.keys()), width=330,
                                      command=self._update_model_combo)
        self.combo_brand.set("Bambu Lab")
        self.combo_brand.pack(pady=4, padx=10)

        ctk.CTkLabel(fc, text="Yazıcı Modeli", text_color="#8B949E",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.combo_model = mini_combo(fc, [], width=330)
        self.combo_model.pack(pady=4, padx=10)
        self._update_model_combo("Bambu Lab")

        ctk.CTkLabel(fc, text="Durum", text_color="#8B949E",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        self.combo_status = mini_combo(fc,
            ["Hazırlanıyor","Basılıyor","Tamamlandı","İptal"], width=330)
        self.combo_status.set("Hazırlanıyor")
        self.combo_status.pack(pady=4, padx=10)

        # Kar marjı
        ctk.CTkLabel(fc, text="Kar Marjı Hesapla", text_color="#8B949E",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(8,0))
        mf = ctk.CTkFrame(fc, fg_color="transparent")
        mf.pack(fill="x", padx=10)
        self.combo_marj = mini_combo(mf, list(KAR_MARJI_ONERILERI.keys()), width=210)
        self.combo_marj.set("Normal (%40)")
        self.combo_marj.pack(side="left")
        accent_btn(mf,"Hesapla", self._hesapla_satis_fiyati,
                   height=36, width=108).pack(side="left", padx=6)
        self.lbl_oneri = ctk.CTkLabel(fc, text="",
                                      font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
                                      text_color=WARNING)
        self.lbl_oneri.pack(pady=4)

        br = ctk.CTkFrame(fc, fg_color="transparent")
        br.pack(fill="x", padx=10, pady=(10,4))
        accent_btn(br,"💾 Kaydet",   self.add_project,         height=38).pack(side="left", expand=True, fill="x", padx=(0,4))
        accent_btn(br,"⚡ Elektrik", self.update_electric_price,
                   color="#1C4370", hover="#1a3a6b", height=38).pack(side="left", expand=True, fill="x")
        self.add_info = ctk.CTkLabel(fc, text="", wraplength=320, font=ctk.CTkFont(size=12))
        self.add_info.pack(pady=(4,12))

        # Sağ: grafikler + liste
        rp = ctk.CTkFrame(mid, fg_color="transparent")
        rp.pack(side="right", fill="both", expand=True)

        # Stok özet grafiği
        gc = make_card(rp)
        gc.pack(fill="x", pady=(0,8))
        gr = ctk.CTkFrame(gc, fg_color="transparent")
        gr.pack(fill="x", padx=10, pady=10)

        fil_use = {}
        for p in projects:
            f = p.get("filament_turu","PLA")
            fil_use[f] = fil_use.get(f,0) + p.get("gram",0)

        bl = ctk.CTkFrame(gr, fg_color="transparent")
        bl.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(bl, text="🧵 Filament Kullanım",
                     font=ctk.CTkFont(family="Courier",size=12,weight="bold"),
                     text_color=ACCENT).pack(anchor="w")
        if fil_use:
            MiniBarChart(bl, fil_use, color=ACCENT, height=80)
        else:
            ctk.CTkLabel(bl, text="Veri yok.", text_color="#555").pack(pady=10)

        # Satış / stok mini donut
        dl = ctk.CTkFrame(gr, fg_color="transparent", width=140)
        dl.pack(side="right", fill="y", padx=(8,0))
        dl.pack_propagate(False)
        nonempty = {k:v for k,v in stock.items() if v > 0}
        ctk.CTkLabel(dl, text="📦 Stok Dağılımı",
                     font=ctk.CTkFont(size=11), text_color="#8B949E").pack()
        if nonempty:
            DonutChart(dl, nonempty, size=130)
        else:
            ctk.CTkLabel(dl, text="Stok yok.", text_color="#555").pack(pady=20)

        # Proje listesi
        lc2 = make_card(rp)
        lc2.pack(fill="both", expand=True)

        lh = ctk.CTkFrame(lc2, fg_color="transparent")
        lh.pack(fill="x", padx=14, pady=(12,4))
        ctk.CTkLabel(lh, text="📋 PROJELER",
                     font=ctk.CTkFont(family="Courier",size=14,weight="bold"),
                     text_color=ACCENT).pack(side="left")
        self.search_entry = mini_entry(lh, "Canlı ara...", width=190, height=32)
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", lambda e: self._live_search())

        br2 = ctk.CTkFrame(lc2, fg_color="transparent")
        br2.pack(fill="x", padx=14, pady=(0,4))
        accent_btn(br2,"📋 Forma Yükle", self.load_project_to_form,
                   color="#1C4370", hover="#1a3a6b", height=32, width=120).pack(side="left", padx=(0,4))
        success_btn(br2,"✏️ Güncelle",  self.update_selected_project,
                    height=32, width=100).pack(side="left", padx=4)
        danger_btn(br2,"🗑 Sil",        self.delete_selected_project,
                   height=32, width=72).pack(side="left", padx=4)

        self.project_list = ctk.CTkTextbox(lc2, corner_radius=10,
                                           fg_color="#0D1117",
                                           font=ctk.CTkFont(family="Courier", size=12))
        self.project_list.pack(fill="both", expand=True, padx=14, pady=(0,4))

        self.select_entry = mini_entry(lc2, "Proje numarası", height=32)
        self.select_entry.pack(fill="x", padx=14, pady=(0,10))

        self._fill_project_list(projects)


# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
