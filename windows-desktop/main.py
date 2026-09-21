# -*- coding: utf-8 -*-
import os
import re
import sys
import sqlite3
import shutil
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal
from PyQt5.QtGui import QColor, QPalette, QFont, QIcon, QPainter, QPen, QPixmap, QLinearGradient
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QLineEdit,
    QComboBox, QPushButton, QStackedWidget, QScrollArea, QGraphicsDropShadowEffect,
    QMessageBox
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))

# اطلاعات کاربر باید بیرون از پوشه نصب ذخیره شود؛ پوشه Program Files معمولاً
# اجازه نوشتن ندارد و در نسخه تک‌فایلی PyInstaller نیز موقتی است.
DATA_DIR = os.path.join(os.environ.get('APPDATA', APP_DIR), 'Qimat')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'qimat_v12.db')

# انتقال خودکار پایگاه داده نسخه قابل‌حمل قدیمی در اولین اجرا.
LEGACY_DB_PATH = os.path.join(APP_DIR, 'qimat_v12.db')
if not os.path.exists(DB_PATH) and os.path.isfile(LEGACY_DB_PATH) and LEGACY_DB_PATH != DB_PATH:
    try:
        shutil.copy2(LEGACY_DB_PATH, DB_PATH)
    except OSError:
        pass

# ----- Theme -----
BG = '#f6efe6'
WINDOW = '#fcf8f4'
CARD = '#fffdfb'
TEXT = '#20120b'
MUTED = '#9c7e65'
BORDER = '#e9ddcf'
SOFT = '#f3ebe1'
GOLD = '#c6a06a'
GOLD_LIGHT = '#ead0a2'
DARK = '#2d1a11'
DARK2 = '#47291a'
DARK3 = '#5b3823'


def add_shadow(widget, blur=24, offset_y=6, color='#d8c6b2'):
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(blur)
    eff.setOffset(0, offset_y)
    eff.setColor(QColor(color))
    widget.setGraphicsEffect(eff)


def money_fmt(v):
    try:
        return f"{int(round(float(v))):,}"
    except Exception:
        return '0'


def parse_money(text):
    d = re.sub(r'[^\d]', '', text or '')
    return int(d) if d else 0


def parse_num(text):
    t = (text or '').replace('٫', '.').replace(',', '')
    t = re.sub(r'[^0-9.]', '', t)
    if not t:
        return 0.0
    try:
        return float(t)
    except Exception:
        return 0.0


def make_icon(kind, size=28, color='#f0d6a4'):
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    pen = QPen(QColor(color))
    pen.setWidthF(1.8)
    p.setPen(pen)
    w = size
    h = size
    if kind == 'diamond':
        pts = [(w//2, 3), (w-5, 10), (w//2, h-4), (5, 10), (w//2, 3)]
        for a, b in zip(pts, pts[1:]):
            p.drawLine(a[0], a[1], b[0], b[1])
        p.drawLine(5, 10, w-5, 10)
        p.drawLine(w//2, 3, w//2, h-4)
    elif kind == 'calc':
        p.drawRoundedRect(5, 4, w-10, h-8, 4, 4)
        p.drawLine(8, 10, w-8, 10)
        for yy in (15, 20):
            for xx in (10, 16, 22):
                p.drawEllipse(xx-1, yy-1, 2, 2)
    elif kind == 'book':
        p.drawArc(4, 5, w//2, h-9, 90*16, 180*16)
        p.drawArc(w//2-1, 5, w//2-3, h-9, -90*16, 180*16)
        p.drawLine(w//2, 6, w//2, h-5)
    elif kind == 'necklace':
        p.drawArc(4, 2, w-8, h-8, 200*16, 140*16)
        p.drawLine(w//2, 16, w//2, 21)
        p.drawEllipse(w//2-3, 20, 6, 6)
    elif kind == 'ring':
        p.drawEllipse(6, 9, w-12, h-14)
        p.drawLine(12, 9, w//2, 3)
        p.drawLine(w-12, 9, w//2, 3)
        p.drawLine(w//2-4, 4, w//2+4, 4)
    elif kind == 'gear':
        p.drawEllipse(8, 8, w-16, h-16)
        p.drawEllipse(w//2-2, h//2-2, 4, 4)
        for x1, y1, x2, y2 in [
            (w//2, 2, w//2, 7), (w//2, h-7, w//2, h-2),
            (2, h//2, 7, h//2), (w-7, h//2, w-2, h//2),
            (6, 6, 10, 10), (w-10, 6, w-6, 10),
            (6, h-6, 10, h-10), (w-10, h-6, w-6, h-10)
        ]:
            p.drawLine(x1, y1, x2, y2)
    elif kind == 'gold':
        p.drawLine(6, 19, 11, 10)
        p.drawLine(11, 10, 16, 19)
        p.drawLine(6, 19, 16, 19)
        p.drawLine(13, 19, 18, 8)
        p.drawLine(18, 8, 23, 19)
        p.drawLine(13, 19, 23, 19)
        p.drawLine(9, 19, 18, 19)
    elif kind == 'scale':
        p.drawRoundedRect(6, 8, w-12, h-12, 3, 3)
        p.drawLine(10, 8, w-10, 8)
        p.drawLine(w//2, 4, w//2, 8)
        p.drawEllipse(w//2-2, 13, 4, 4)
    elif kind == 'percent':
        p.drawEllipse(6, 5, 5, 5)
        p.drawEllipse(w-11, h-10, 5, 5)
        p.drawLine(8, h-5, w-8, 5)
    elif kind == 'crown':
        p.drawLine(5, 19, w-5, 19)
        p.drawLine(7, 17, 5, 8)
        p.drawLine(5, 8, 11, 13)
        p.drawLine(11, 13, w//2, 6)
        p.drawLine(w//2, 6, w-11, 13)
        p.drawLine(w-11, 13, w-5, 8)
        p.drawLine(w-5, 8, w-7, 17)
    elif kind == 'info':
        p.drawEllipse(4, 4, w-8, h-8)
        p.drawLine(w//2, 11, w//2, h-7)
        p.drawEllipse(w//2-1, 7, 2, 2)
    elif kind == 'trash':
        p.drawLine(9, 9, w-9, 9)
        p.drawRect(9, 9, w-18, h-14)
        p.drawLine(12, 6, w-12, 6)
        p.drawLine(w//2-3, 4, w//2+3, 4)
    elif kind == 'plus':
        p.drawLine(w//2, 5, w//2, h-5)
        p.drawLine(5, h//2, w-5, h//2)
    p.end()
    return QIcon(pm)


# ----- DB / State -----
class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute('CREATE TABLE IF NOT EXISTS settings (k TEXT PRIMARY KEY, v TEXT)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS item_types (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, min_labor INTEGER)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS accessories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price INTEGER)')
        self.conn.commit()
        self.seed()

    def seed(self):
        for k, v in {
            'profit': '7', 'tax': '10', 'gold': '9850000', 'weight': '5.25',
            'labor_percent': '7', 'selected_type_id': '0', 'selected_acc_id': '0'
        }.items():
            self.conn.execute('INSERT OR IGNORE INTO settings(k,v) VALUES (?,?)', (k, v))
        if self.conn.execute('SELECT COUNT(*) FROM item_types').fetchone()[0] == 0:
            for n, m in [('گردنبند', 2000000), ('دستبند', 1500000), ('انگشتر', 1000000), ('گوشواره', 1200000)]:
                self.conn.execute('INSERT INTO item_types(name,min_labor) VALUES (?,?)', (n, m))
        if self.conn.execute('SELECT COUNT(*) FROM accessories').fetchone()[0] == 0:
            for n, p in [('بدون اکسسوری', 0), ('بند ابریشمی', 500000), ('میوکی ۵', 800000), ('میوکی ۳', 600000), ('چرم', 1200000)]:
                self.conn.execute('INSERT INTO accessories(name,price) VALUES (?,?)', (n, p))
        self.conn.commit()

    def get_setting(self, k, default='0'):
        row = self.conn.execute('SELECT v FROM settings WHERE k=?', (k,)).fetchone()
        return row[0] if row else default

    def set_setting(self, k, value):
        self.conn.execute('INSERT OR REPLACE INTO settings(k,v) VALUES (?,?)', (k, str(value)))
        self.conn.commit()

    def get_types(self):
        return self.conn.execute('SELECT id,name,min_labor FROM item_types ORDER BY id').fetchall()

    def get_accessories(self):
        return self.conn.execute('SELECT id,name,price FROM accessories ORDER BY id').fetchall()

    def add_type(self, name, min_labor):
        self.conn.execute('INSERT INTO item_types(name,min_labor) VALUES (?,?)', (name, int(min_labor)))
        self.conn.commit()

    def update_type(self, item_id, name, min_labor):
        self.conn.execute('UPDATE item_types SET name=?, min_labor=? WHERE id=?', (name, int(min_labor), item_id))
        self.conn.commit()

    def delete_type(self, item_id):
        self.conn.execute('DELETE FROM item_types WHERE id=?', (item_id,))
        self.conn.commit()

    def add_accessory(self, name, price):
        self.conn.execute('INSERT INTO accessories(name,price) VALUES (?,?)', (name, int(price)))
        self.conn.commit()

    def update_accessory(self, item_id, name, price):
        self.conn.execute('UPDATE accessories SET name=?, price=? WHERE id=?', (name, int(price), item_id))
        self.conn.commit()

    def delete_accessory(self, item_id):
        self.conn.execute('DELETE FROM accessories WHERE id=?', (item_id,))
        self.conn.commit()


class State(QObject):
    changed = pyqtSignal()
    structure_changed = pyqtSignal()

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.gold = int(float(self.db.get_setting('gold', '9850000')))
        self.weight = float(self.db.get_setting('weight', '5.25'))
        self.labor_percent = float(self.db.get_setting('labor_percent', '7'))
        self.selected_type_id = int(float(self.db.get_setting('selected_type_id', '0'))) or None
        self.selected_acc_id = int(float(self.db.get_setting('selected_acc_id', '0'))) or None
        self.reload()

    def reload(self):
        self.profit = float(self.db.get_setting('profit', '7'))
        self.tax = float(self.db.get_setting('tax', '10'))
        self.types = self.db.get_types()
        self.accessories = self.db.get_accessories()
        if self.types and self.selected_type_id not in [t[0] for t in self.types]:
            self.selected_type_id = self.types[0][0]
        if self.accessories and self.selected_acc_id not in [a[0] for a in self.accessories]:
            self.selected_acc_id = self.accessories[0][0]

    def set_inputs(self, gold=None, weight=None, labor_percent=None, type_id=None, acc_id=None):
        if gold is not None:
            self.gold = gold
        if weight is not None:
            self.weight = weight
        if labor_percent is not None:
            self.labor_percent = labor_percent
        if type_id is not None:
            self.selected_type_id = type_id
        if acc_id is not None:
            self.selected_acc_id = acc_id
        # هر تغییر کاربر همان لحظه ثبت می‌شود تا حتی در خاموشی ناگهانی باقی بماند.
        values = {
            'gold': self.gold,
            'weight': self.weight,
            'labor_percent': self.labor_percent,
            'selected_type_id': self.selected_type_id or 0,
            'selected_acc_id': self.selected_acc_id or 0,
        }
        self.db.conn.executemany(
            'INSERT OR REPLACE INTO settings(k,v) VALUES (?,?)',
            [(k, str(v)) for k, v in values.items()]
        )
        self.db.conn.commit()
        self.changed.emit()

    def get_current_type(self):
        for row in self.types:
            if row[0] == self.selected_type_id:
                return row
        return self.types[0] if self.types else None

    def get_current_acc(self):
        for row in self.accessories:
            if row[0] == self.selected_acc_id:
                return row
        return self.accessories[0] if self.accessories else None

    def compute(self):
        raw = self.gold * self.weight
        t = self.get_current_type()
        min_labor = t[2] if t else 0
        labor_calc = raw * self.labor_percent / 100.0
        labor_final = max(labor_calc, min_labor)
        minimum_applied = labor_calc < min_labor
        profit = (raw + labor_final) * self.profit / 100.0
        tax = (labor_final + profit) * self.tax / 100.0
        a = self.get_current_acc()
        acc_name = a[1] if a else 'بدون اکسسوری'
        acc_price = a[2] if a else 0
        final = raw + labor_final + profit + tax + acc_price
        return {
            'raw': int(round(raw)),
            'labor_final': int(round(labor_final)),
            'minimum_applied': minimum_applied,
            'profit': int(round(profit)),
            'tax': int(round(tax)),
            'acc_name': acc_name,
            'acc_price': int(round(acc_price)),
            'final': int(round(final)),
        }

    def set_profit(self, value):
        self.profit = max(0.0, float(value))
        self.db.set_setting('profit', self.profit)
        self.changed.emit()

    def set_tax(self, value):
        self.tax = max(0.0, float(value))
        self.db.set_setting('tax', self.tax)
        self.changed.emit()

    def add_type(self, name, min_labor):
        self.db.add_type(name, min_labor)
        self.reload(); self.structure_changed.emit(); self.changed.emit()

    def update_type(self, item_id, name, min_labor):
        self.db.update_type(item_id, name, min_labor)
        self.reload(); self.structure_changed.emit(); self.changed.emit()

    def delete_type(self, item_id):
        self.db.delete_type(item_id)
        self.reload(); self.structure_changed.emit(); self.changed.emit()

    def add_acc(self, name, price):
        self.db.add_accessory(name, price)
        self.reload(); self.structure_changed.emit(); self.changed.emit()

    def update_acc(self, item_id, name, price):
        self.db.update_accessory(item_id, name, price)
        self.reload(); self.structure_changed.emit(); self.changed.emit()

    def delete_acc(self, item_id):
        self.db.delete_accessory(item_id)
        self.reload(); self.structure_changed.emit(); self.changed.emit()


# ----- Widgets -----
class MoneyEdit(QLineEdit):
    def __init__(self, text=''):
        super().__init__(text)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.textEdited.connect(self._live)
        self.editingFinished.connect(self._finish)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.selectAll()

    def _live(self, _):
        d = re.sub(r'[^\d]', '', self.text())
        self.blockSignals(True)
        self.setText('' if not d else f"{int(d):,}")
        self.blockSignals(False)

    def _finish(self):
        d = re.sub(r'[^\d]', '', self.text())
        self.setText('' if not d else f"{int(d):,}")

    def value(self):
        return parse_money(self.text())


class NumEdit(QLineEdit):
    def __init__(self, text=''):
        super().__init__(text)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.textEdited.connect(self._live)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.selectAll()

    def _live(self, _):
        t = self.text().replace('٫', '.').replace(',', '')
        t = re.sub(r'[^0-9.]', '', t)
        parts = t.split('.')
        if len(parts) > 2:
            t = parts[0] + '.' + ''.join(parts[1:])
        self.blockSignals(True)
        self.setText(t)
        self.blockSignals(False)

    def value(self):
        return parse_num(self.text())


class BaseScrollPage(QScrollArea):
    def __init__(self, widget):
        super().__init__()
        self.setWidgetResizable(True)
        self.setWidget(widget)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet('QScrollArea{background:transparent;border:none;}')


class BackgroundPanel(QFrame):
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        grad = QLinearGradient(0, 0, self.width(), self.height())
        grad.setColorAt(0, QColor('#fcfaf7'))
        grad.setColorAt(1, QColor('#f6efe6'))
        p.fillRect(self.rect(), grad)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(255, 255, 255, 68))
        p.drawEllipse(-60, 140, 280, 360)
        p.drawEllipse(-20, self.height() - 310, 250, 220)
        p.end()
        super().paintEvent(e)


class LeftBrandPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        v = QVBoxLayout(self)
        v.setContentsMargins(14, 52, 20, 14)
        v.setSpacing(10)
        l = QLabel('╱')
        l.setStyleSheet(f'font-size:34px;color:{GOLD};')
        v.addWidget(l, 0, Qt.AlignLeft)
        v.addSpacing(44)
        big = QLabel('اعتماد\nزیبایی\nارزش ماندگار')
        big.setAlignment(Qt.AlignCenter)
        big.setStyleSheet('font-size:22px;color:#a57a4b;line-height:1.88;font-weight:500;')
        v.addWidget(big)
        dash = QLabel('—')
        dash.setAlignment(Qt.AlignCenter)
        dash.setStyleSheet(f'font-size:23px;color:{GOLD};')
        v.addWidget(dash)
        eng = QLabel('A BRIGHTER\nTOMORROW')
        eng.setAlignment(Qt.AlignCenter)
        eng.setStyleSheet('font-size:14px;color:#a18b77;letter-spacing:2px;line-height:1.9;')
        v.addWidget(eng)
        v.addStretch(1)
        cube = QFrame()
        cube.setFixedSize(118, 142)
        cube.setStyleSheet('''QFrame{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #e2c69f,stop:1 #c79861);border:1px solid #ebd3a7;border-radius:16px;}''')
        cl = QVBoxLayout(cube)
        cl.setContentsMargins(10, 10, 10, 10)
        top = QLabel()
        top.setPixmap(make_icon('ring', 42, '#7f5f3f').pixmap(42, 42))
        top.setAlignment(Qt.AlignLeft)
        txt = QLabel('QIMAT\nJEWELRY\nVALUES\nPEOPLE')
        txt.setStyleSheet('font-size:10px;color:#7a6249;line-height:1.65;')
        cl.addWidget(top)
        cl.addWidget(txt)
        v.addWidget(cube, 0, Qt.AlignLeft)


class LuxField(QFrame):
    def __init__(self, title, editor, icon_kind, unit='', compact=False):
        super().__init__()
        self.setStyleSheet(f'QFrame{{background:{CARD};border:1px solid {BORDER};border-radius:20px;}}')
        h = QHBoxLayout(self)
        h.setContentsMargins(16, 7 if compact else 14, 16, 7 if compact else 14)
        h.setSpacing(12 if compact else 16)

        value_wrap = QFrame(); value_wrap.setStyleSheet('QFrame{border:none;background:transparent;}')
        vh = QHBoxLayout(value_wrap); vh.setContentsMargins(0, 0, 0, 0); vh.setSpacing(8)
        if isinstance(editor, QComboBox):
            editor.setLayoutDirection(Qt.RightToLeft)
            editor.setStyleSheet(f'''
                QComboBox{{border:1px solid #ece3d7;background:#fffdfb;border-radius:14px;padding:10px 14px;font-size:19px;font-weight:700;color:{TEXT};min-height:34px;}}
                QComboBox::drop-down{{border:none;width:24px;}} QComboBox::down-arrow{{image:none;}}
            ''')
            arrow = QLabel('⌄')
            arrow.setStyleSheet('font-size:22px;color:#2e1c14;font-weight:700;')
            vh.addWidget(editor, 1)
            vh.addWidget(arrow)
        else:
            editor.setStyleSheet(f'QLineEdit{{border:none;background:transparent;color:{TEXT};font-size:{18 if compact else 20}px;font-weight:700;min-height:{26 if compact else 30}px;}}')
            vh.addWidget(editor, 1)
            if unit:
                lbl_unit = QLabel(unit)
                lbl_unit.setStyleSheet(f'font-size:17px;color:{MUTED};font-weight:600;')
                vh.addWidget(lbl_unit)

        right = QHBoxLayout(); right.setSpacing(12)
        lbl = QLabel(title)
        lbl.setStyleSheet(f'font-size:{17 if compact else 19}px;font-weight:700;color:{TEXT};')
        icon_size = 46 if compact else 56
        art_size = 25 if compact else 30
        icon = QLabel(); icon.setFixedSize(icon_size, icon_size); icon.setAlignment(Qt.AlignCenter)
        icon.setPixmap(make_icon(icon_kind, art_size, TEXT).pixmap(art_size, art_size))
        icon.setStyleSheet(f'background:{SOFT};border:1px solid #e9dece;border-radius:{21 if compact else 24}px;')
        right.addWidget(lbl)
        right.addWidget(icon)

        h.addWidget(value_wrap, 1)
        h.addLayout(right)


class ResultCard(QFrame):
    def __init__(self, compact=False):
        super().__init__()
        self.setStyleSheet(f'''QFrame{{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #4a2b1b, stop:0.45 #2a180f, stop:1 #5a3722);border:2px solid {GOLD};border-radius:24px;}}''')
        add_shadow(self, blur=30, offset_y=8)
        v = QVBoxLayout(self)
        v.setContentsMargins(22, 10 if compact else 18, 22, 12 if compact else 20)
        v.setSpacing(3 if compact else 6)
        hh = QHBoxLayout(); hh.setAlignment(Qt.AlignCenter)
        t = QLabel('قیمت اعلامی به مشتری')
        t.setStyleSheet(f'font-size:{17 if compact else 20}px;color:#efd6a4;font-weight:700;')
        ic = QLabel(); ic.setPixmap(make_icon('crown', 30, '#f1d7a1').pixmap(30, 30))
        hh.addWidget(t); hh.addWidget(ic)
        v.addLayout(hh)
        divider = QLabel('────────── ✦ ──────────')
        divider.setAlignment(Qt.AlignCenter)
        divider.setStyleSheet(f'font-size:14px;color:{GOLD};')
        v.addWidget(divider)
        rr = QHBoxLayout(); rr.setAlignment(Qt.AlignCenter)
        self.unit = QLabel('تومان')
        self.unit.setStyleSheet('font-size:19px;color:#f7e7c1;font-weight:700;')
        self.amount = QLabel('0')
        self.amount.setStyleSheet(f'font-size:{42 if compact else 58}px;color:#fff4d5;font-weight:800;')
        rr.addWidget(self.unit); rr.addWidget(self.amount)
        v.addLayout(rr)

    def set_value(self, value_text):
        self.amount.setText(value_text)


class SidebarButton(QPushButton):
    def __init__(self, text, icon_kind, active=False):
        super().__init__(text)
        self.setCheckable(True)
        self.setChecked(active)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setCursor(Qt.PointingHandCursor)
        self.setIcon(make_icon(icon_kind, 28, GOLD_LIGHT))
        self.setIconSize(QSize(28, 28))
        self.setMinimumHeight(64)
        self.setStyleSheet(f'''
            QPushButton{{text-align:right;padding:14px 18px;border:1px solid transparent;border-radius:18px;color:{GOLD_LIGHT};background:transparent;font-size:16px;font-weight:700;}}
            QPushButton:hover{{border:1px solid #745232;background:rgba(255,255,255,0.03);}}
            QPushButton:checked{{text-align:right;padding:14px 18px;border:1px solid {GOLD};border-radius:18px;color:#fff4df;background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #6b462c,stop:1 #89623b);}}
        ''')


class Sidebar(QFrame):
    def __init__(self, page_defs, switch_callback):
        super().__init__()
        self.setFixedWidth(295)
        self.setStyleSheet('''QFrame{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #3c2417,stop:1 #23150e);border:1px solid #86603a;border-radius:26px;}''')
        add_shadow(self, blur=18, offset_y=4, color='#b79a77')
        self.buttons = []

        v = QVBoxLayout(self)
        v.setContentsMargins(16, 18, 16, 18)
        v.setSpacing(12)
        hd = QHBoxLayout()
        top_text = QLabel('نسخه 1.2.2   |   قیمت')
        top_text.setStyleSheet('font-size:18px;font-weight:700;color:#f1d7a3;')
        top_icon = QLabel(); top_icon.setPixmap(make_icon('diamond', 24, '#f1d7a3').pixmap(24, 24))
        hd.addWidget(top_text, 1); hd.addWidget(top_icon)
        v.addLayout(hd)

        for i, (text, icon_kind) in enumerate(page_defs):
            btn = SidebarButton(text, icon_kind, active=(i == 0))
            btn.clicked.connect(lambda checked, idx=i: switch_callback(idx))
            self.buttons.append(btn)
            v.addWidget(btn)
        v.addStretch(1)
        curvy = QLabel('╱'); curvy.setAlignment(Qt.AlignRight); curvy.setStyleSheet(f'font-size:30px;color:{GOLD};')
        v.addWidget(curvy)
        bottom_text = QLabel('GOLD\nMORE THAN A METAL\nA TRUST')
        bottom_text.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        bottom_text.setStyleSheet('font-size:14px;color:#e2c48e;line-height:1.9;')
        v.addWidget(bottom_text)

    def set_active(self, index):
        for i, b in enumerate(self.buttons):
            b.setChecked(i == index)


class PageTitle(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 6, 0, 0)
        v.setSpacing(4)
        title = QLabel('قیمت')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f'font-size:58px;font-weight:800;color:{TEXT};')
        divider = QLabel('──────── ✦ ────────')
        divider.setAlignment(Qt.AlignCenter)
        divider.setStyleSheet(f'font-size:13px;color:{GOLD};')
        subtitle = QLabel('دقت در قیمت، اعتماد در معامله')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f'font-size:15px;color:{MUTED};')
        v.addWidget(title)
        v.addWidget(divider)
        v.addWidget(subtitle)


class QuickPage(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state

        content = QWidget()
        root = QHBoxLayout(content)
        root.setContentsMargins(30, 4, 30, 8)
        root.setSpacing(0)

        root.addStretch(1)
        center_wrap = QWidget()
        center_wrap.setMaximumWidth(860)
        center = QVBoxLayout(center_wrap)
        center.setContentsMargins(0, 0, 0, 0)
        center.setSpacing(8)

        self.gold_edit = MoneyEdit(money_fmt(self.state.gold))
        self.type_combo = QComboBox()
        self.weight_edit = NumEdit(str(self.state.weight))
        self.labor_edit = NumEdit(str(self.state.labor_percent))
        self.acc_combo = QComboBox()

        center.addWidget(LuxField('قیمت طلا', self.gold_edit, 'gold', 'تومان', compact=True))
        center.addWidget(LuxField('نوع جنس', self.type_combo, 'necklace', compact=True))
        center.addWidget(LuxField('وزن', self.weight_edit, 'scale', 'گرم', compact=True))
        center.addWidget(LuxField('اجرت', self.labor_edit, 'percent', '٪', compact=True))
        center.addWidget(LuxField('اکسسوری', self.acc_combo, 'ring', compact=True))

        self.result = ResultCard(compact=True)
        center.addWidget(self.result)

        info = QFrame()
        info.setStyleSheet(f'QFrame{{background:{CARD};border:1px solid {BORDER};border-radius:18px;}}')
        ih = QHBoxLayout(info); ih.setContentsMargins(14, 10, 14, 10)
        ii = QLabel(); ii.setPixmap(make_icon('info', 20, MUTED).pixmap(20, 20))
        it = QLabel('اجرت، سود، مالیات و اکسسوری‌ها از تنظیمات محاسبه می‌شوند.')
        it.setAlignment(Qt.AlignCenter); it.setStyleSheet(f'font-size:11px;color:{MUTED};')
        ih.addWidget(ii); ih.addWidget(it, 1)
        center.addWidget(info)
        center.addStretch(1)
        root.addWidget(center_wrap, 0, Qt.AlignHCenter)
        root.addStretch(1)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(BaseScrollPage(content))

        self.refresh_lists()
        self.gold_edit.textChanged.connect(self.push_state)
        self.weight_edit.textChanged.connect(self.push_state)
        self.labor_edit.textChanged.connect(self.push_state)
        self.type_combo.currentIndexChanged.connect(self.push_state)
        self.acc_combo.currentIndexChanged.connect(self.push_state)
        self.state.structure_changed.connect(self.on_structure)
        self.state.changed.connect(self.refresh_result)
        self.push_state()

    def refresh_lists(self):
        self.type_combo.blockSignals(True)
        self.type_combo.clear()
        for item_id, name, min_labor in self.state.types:
            self.type_combo.addItem(name, item_id)
        idx = self.type_combo.findData(self.state.selected_type_id)
        self.type_combo.setCurrentIndex(0 if idx < 0 else idx)
        self.type_combo.blockSignals(False)

        self.acc_combo.blockSignals(True)
        self.acc_combo.clear()
        for item_id, name, price in self.state.accessories:
            self.acc_combo.addItem(name, item_id)
        idx = self.acc_combo.findData(self.state.selected_acc_id)
        self.acc_combo.setCurrentIndex(0 if idx < 0 else idx)
        self.acc_combo.blockSignals(False)

    def push_state(self):
        self.state.set_inputs(
            gold=self.gold_edit.value(),
            weight=self.weight_edit.value(),
            labor_percent=self.labor_edit.value(),
            type_id=self.type_combo.currentData(),
            acc_id=self.acc_combo.currentData()
        )

    def refresh_result(self):
        self.result.set_value(money_fmt(self.state.compute()['final']))

    def on_structure(self):
        self.state.reload()
        self.refresh_lists()
        self.refresh_result()


class HeaderCard(QFrame):
    def __init__(self, title, icon_kind):
        super().__init__()
        self.setStyleSheet(f'QFrame{{background:{CARD};border:1px solid {BORDER};border-radius:20px;}}')
        h = QHBoxLayout(self)
        h.setContentsMargins(16, 12, 16, 12)
        lbl = QLabel(title)
        lbl.setStyleSheet(f'font-size:28px;font-weight:800;color:{TEXT};')
        icon = QLabel(); icon.setFixedSize(54, 54); icon.setAlignment(Qt.AlignCenter)
        icon.setPixmap(make_icon(icon_kind, 28, TEXT).pixmap(28, 28))
        icon.setStyleSheet(f'background:{SOFT};border:1px solid {BORDER};border-radius:27px;')
        h.addWidget(lbl, 1)
        h.addWidget(icon)


class SummaryBox(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setStyleSheet(f'QFrame{{background:{CARD};border:1px solid {BORDER};border-radius:18px;}}')
        v = QVBoxLayout(self)
        v.setContentsMargins(14, 14, 14, 14)
        self.t = QLabel(title)
        self.t.setAlignment(Qt.AlignRight)
        self.t.setStyleSheet(f'font-size:15px;color:{MUTED};font-weight:600;')
        self.v = QLabel('-')
        self.v.setAlignment(Qt.AlignCenter)
        self.v.setStyleSheet(f'font-size:26px;color:{TEXT};font-weight:800;')
        v.addWidget(self.t)
        v.addWidget(self.v)


class DetailsPage(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        content = QWidget()
        root = QVBoxLayout(content)
        root.setContentsMargins(28, 24, 28, 28)
        root.setSpacing(14)
        root.addWidget(HeaderCard('خلاصه محاسبه قیمت', 'book'))
        note = QLabel('در این صفحه جمع هر بخش نمایش داده می‌شود.')
        note.setStyleSheet(f'font-size:13px;color:{MUTED};')
        note.setAlignment(Qt.AlignRight)
        root.addWidget(note)

        r1 = QHBoxLayout(); r1.setSpacing(14)
        self.b1 = SummaryBox('ارزش طلای خام'); self.b2 = SummaryBox('اجرت نهایی'); self.b3 = SummaryBox('سود')
        r1.addWidget(self.b1); r1.addWidget(self.b2); r1.addWidget(self.b3)
        root.addLayout(r1)
        r2 = QHBoxLayout(); r2.setSpacing(14)
        self.b4 = SummaryBox('مالیات'); self.b5 = SummaryBox('اکسسوری'); self.b6 = SummaryBox('حداقل اجرت اعمال شد؟')
        r2.addWidget(self.b4); r2.addWidget(self.b5); r2.addWidget(self.b6)
        root.addLayout(r2)

        final_card = ResultCard()
        final_card.set_value('0')
        self.final_amount = final_card.amount
        root.addWidget(final_card)
        root.addStretch(1)
        lay = QVBoxLayout(self); lay.setContentsMargins(0,0,0,0); lay.addWidget(BaseScrollPage(content))
        self.state.changed.connect(self.refresh)
        self.refresh()

    def refresh(self):
        d = self.state.compute()
        self.b1.v.setText(money_fmt(d['raw']))
        self.b2.v.setText(money_fmt(d['labor_final']))
        self.b3.v.setText(money_fmt(d['profit']))
        self.b4.v.setText(money_fmt(d['tax']))
        self.b5.v.setText(f"{d['acc_name']}\n{money_fmt(d['acc_price'])}")
        self.b6.v.setText('بله' if d['minimum_applied'] else 'خیر')
        self.final_amount.setText(money_fmt(d['final']))


class RowEditor(QFrame):
    deleted = pyqtSignal(int)
    saved = pyqtSignal(int, str, int)

    def __init__(self, item_id, name, value, value_title):
        super().__init__()
        self.item_id = item_id
        self.setStyleSheet(f'QFrame{{background:{CARD};border:1px solid {BORDER};border-radius:18px;}}')
        h = QHBoxLayout(self); h.setContentsMargins(14, 14, 14, 14); h.setSpacing(10)
        self.name_edit = QLineEdit(name)
        self.name_edit.setStyleSheet(f'QLineEdit{{background:{SOFT};border:1px solid {BORDER};border-radius:14px;padding:10px 12px;font-size:15px;}}')
        self.value_edit = MoneyEdit(money_fmt(value))
        self.value_edit.setStyleSheet(f'QLineEdit{{background:{SOFT};border:1px solid {BORDER};border-radius:14px;padding:10px 12px;font-size:15px;}}')
        del_btn = QPushButton('حذف')
        del_btn.setIcon(make_icon('trash', 18, '#7b5b3a'))
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.setStyleSheet(f'QPushButton{{background:{SOFT};border:1px solid {BORDER};border-radius:14px;padding:10px 14px;font-size:14px;font-weight:700;color:#5f4330;}}')
        left = QFrame(); l1 = QHBoxLayout(left); l1.setContentsMargins(0,0,0,0); l1.addWidget(QLabel('نام')); l1.addWidget(self.name_edit)
        right = QFrame(); l2 = QHBoxLayout(right); l2.setContentsMargins(0,0,0,0); l2.addWidget(QLabel(value_title)); l2.addWidget(self.value_edit); l2.addWidget(QLabel('تومان'))
        h.addWidget(left, 3); h.addWidget(right, 3); h.addWidget(del_btn)
        self.name_edit.editingFinished.connect(self.save_emit)
        self.value_edit.editingFinished.connect(self.save_emit)
        del_btn.clicked.connect(lambda: self.deleted.emit(self.item_id))

    def save_emit(self):
        self.saved.emit(self.item_id, self.name_edit.text().strip(), self.value_edit.value())


class EditListPage(QWidget):
    def __init__(self, title, icon_kind):
        super().__init__()
        self.content = QWidget()
        self.root = QVBoxLayout(self.content)
        self.root.setContentsMargins(28, 24, 28, 28)
        self.root.setSpacing(14)
        self.root.addWidget(HeaderCard(title, icon_kind))
        lay = QVBoxLayout(self); lay.setContentsMargins(0,0,0,0); lay.addWidget(BaseScrollPage(self.content))


class TypesPage(EditListPage):
    def __init__(self, state):
        super().__init__('مدیریت نوع جنس', 'necklace')
        self.state = state
        self.name_new = QLineEdit(); self.name_new.setPlaceholderText('نام جنس جدید')
        self.name_new.setStyleSheet(f'QLineEdit{{background:{SOFT};border:1px solid {BORDER};border-radius:14px;padding:10px 12px;font-size:15px;}}')
        self.val_new = MoneyEdit(); self.val_new.setStyleSheet(f'QLineEdit{{background:{SOFT};border:1px solid {BORDER};border-radius:14px;padding:10px 12px;font-size:15px;}}')
        add_btn = QPushButton('افزودن نوع جنس'); add_btn.setIcon(make_icon('plus', 18, '#fff4dd')); add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet(f'QPushButton{{background:{DARK2};color:#fff4dd;border:1px solid {GOLD};border-radius:14px;padding:10px 16px;font-size:14px;font-weight:700;}}')
        card = QFrame(); card.setStyleSheet(f'QFrame{{background:{CARD};border:1px solid {BORDER};border-radius:18px;}}')
        ch = QHBoxLayout(card); ch.setContentsMargins(14, 14, 14, 14)
        val_wrap = QFrame(); vh = QHBoxLayout(val_wrap); vh.setContentsMargins(0,0,0,0); vh.addWidget(self.val_new); vh.addWidget(QLabel('تومان'))
        ch.addWidget(self.name_new, 3); ch.addWidget(val_wrap, 2); ch.addWidget(add_btn)
        self.root.addWidget(card)
        self.list_lay = QVBoxLayout(); self.list_lay.setSpacing(12); self.root.addLayout(self.list_lay); self.root.addStretch(1)
        add_btn.clicked.connect(self.add_item)
        self.state.structure_changed.connect(self.refresh)
        self.refresh()

    def add_item(self):
        name = self.name_new.text().strip()
        if not name:
            QMessageBox.warning(self, 'هشدار', 'نام جنس را وارد کنید.')
            return
        self.state.add_type(name, self.val_new.value())
        self.name_new.clear(); self.val_new.clear()

    def refresh(self):
        while self.list_lay.count():
            item = self.list_lay.takeAt(0)
            w = item.widget()
            if w: w.deleteLater()
        for item_id, name, min_labor in self.state.types:
            row = RowEditor(item_id, name, min_labor, 'حداقل اجرت')
            row.saved.connect(self.save_item); row.deleted.connect(self.delete_item)
            self.list_lay.addWidget(row)

    def save_item(self, item_id, name, value):
        if name:
            self.state.update_type(item_id, name, value)

    def delete_item(self, item_id):
        if len(self.state.types) <= 1:
            QMessageBox.warning(self, 'هشدار', 'حداقل یک نوع جنس باید باقی بماند.')
            return
        if QMessageBox.question(self, 'تأیید', 'این نوع جنس حذف شود؟') == QMessageBox.Yes:
            self.state.delete_type(item_id)


class AccessoriesPage(EditListPage):
    def __init__(self, state):
        super().__init__('اکسسوری‌ها', 'ring')
        self.state = state
        self.name_new = QLineEdit(); self.name_new.setPlaceholderText('نام اکسسوری جدید')
        self.name_new.setStyleSheet(f'QLineEdit{{background:{SOFT};border:1px solid {BORDER};border-radius:14px;padding:10px 12px;font-size:15px;}}')
        self.val_new = MoneyEdit(); self.val_new.setStyleSheet(f'QLineEdit{{background:{SOFT};border:1px solid {BORDER};border-radius:14px;padding:10px 12px;font-size:15px;}}')
        add_btn = QPushButton('افزودن اکسسوری'); add_btn.setIcon(make_icon('plus', 18, '#fff4dd')); add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet(f'QPushButton{{background:{DARK2};color:#fff4dd;border:1px solid {GOLD};border-radius:14px;padding:10px 16px;font-size:14px;font-weight:700;}}')
        card = QFrame(); card.setStyleSheet(f'QFrame{{background:{CARD};border:1px solid {BORDER};border-radius:18px;}}')
        ch = QHBoxLayout(card); ch.setContentsMargins(14, 14, 14, 14)
        val_wrap = QFrame(); vh = QHBoxLayout(val_wrap); vh.setContentsMargins(0,0,0,0); vh.addWidget(self.val_new); vh.addWidget(QLabel('تومان'))
        ch.addWidget(self.name_new, 3); ch.addWidget(val_wrap, 2); ch.addWidget(add_btn)
        self.root.addWidget(card)
        self.list_lay = QVBoxLayout(); self.list_lay.setSpacing(12); self.root.addLayout(self.list_lay); self.root.addStretch(1)
        add_btn.clicked.connect(self.add_item)
        self.state.structure_changed.connect(self.refresh)
        self.refresh()

    def add_item(self):
        name = self.name_new.text().strip()
        if not name:
            QMessageBox.warning(self, 'هشدار', 'نام اکسسوری را وارد کنید.')
            return
        self.state.add_acc(name, self.val_new.value())
        self.name_new.clear(); self.val_new.clear()

    def refresh(self):
        while self.list_lay.count():
            item = self.list_lay.takeAt(0)
            w = item.widget()
            if w: w.deleteLater()
        for item_id, name, price in self.state.accessories:
            row = RowEditor(item_id, name, price, 'قیمت')
            row.saved.connect(self.save_item); row.deleted.connect(self.delete_item)
            self.list_lay.addWidget(row)

    def save_item(self, item_id, name, value):
        if name:
            self.state.update_acc(item_id, name, value)

    def delete_item(self, item_id):
        if QMessageBox.question(self, 'تأیید', 'این اکسسوری حذف شود؟') == QMessageBox.Yes:
            self.state.delete_acc(item_id)


class SettingsPage(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        content = QWidget(); root = QVBoxLayout(content); root.setContentsMargins(28,24,28,28); root.setSpacing(14)
        root.addWidget(HeaderCard('تنظیمات عمومی', 'gear'))
        note = QLabel('درصد سود و مالیات از این بخش تعیین می‌شوند و بلافاصله روی قیمت نهایی اثر می‌گذارند.')
        note.setStyleSheet(f'font-size:13px;color:{MUTED};'); note.setAlignment(Qt.AlignRight)
        root.addWidget(note)
        self.profit_edit = NumEdit(str(self.state.profit)); self.tax_edit = NumEdit(str(self.state.tax))
        root.addWidget(LuxField('درصد سود', self.profit_edit, 'percent', '٪'))
        root.addWidget(LuxField('درصد مالیات', self.tax_edit, 'percent', '٪'))
        root.addStretch(1)
        lay = QVBoxLayout(self); lay.setContentsMargins(0,0,0,0); lay.addWidget(BaseScrollPage(content))
        self.profit_edit.textChanged.connect(lambda: self.state.set_profit(self.profit_edit.value()))
        self.tax_edit.textChanged.connect(lambda: self.state.set_tax(self.tax_edit.value()))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DB()
        self.state = State(self.db)
        self.setWindowTitle('قیمت')
        self.resize(1280, 700)
        self.setMinimumSize(1100, 650)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(f'QWidget{{background:{BG};font-family:Tahoma;color:{TEXT};}}')

        root = QVBoxLayout(self); root.setContentsMargins(16, 16, 16, 16)

        shell = BackgroundPanel()
        shell.setStyleSheet('QFrame{border:1px solid #dfd1c3;border-radius:30px;}')
        add_shadow(shell, blur=36, offset_y=10)
        outer = QVBoxLayout(shell)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        titlebar = QFrame(); titlebar.setFixedHeight(48)
        titlebar.setStyleSheet('QFrame{background:#fdfbf8;border:none;border-top-left-radius:30px;border-top-right-radius:30px;border-bottom:1px solid #eee3d7;}')
        th = QHBoxLayout(titlebar); th.setContentsMargins(16, 10, 16, 10)
        t = QLabel('قیمت'); t.setStyleSheet(f'font-size:18px;font-weight:700;color:{TEXT};')
        icon = QLabel(); icon.setPixmap(make_icon('diamond', 22, '#b68648').pixmap(22, 22))
        controls = QLabel('—    □    ✕'); controls.setStyleSheet(f'font-size:18px;color:{TEXT};')
        th.addWidget(t); th.addWidget(icon); th.addStretch(1); th.addWidget(controls)
        outer.addWidget(titlebar)

        body = QHBoxLayout(); body.setContentsMargins(16, 12, 20, 14); body.setSpacing(16)

        page_defs = [
            ('محاسبه سریع قیمت', 'calc'),
            ('نحوه محاسبه قیمت', 'book'),
            ('مدیریت نوع جنس', 'necklace'),
            ('اکسسوری‌ها', 'ring'),
            ('تنظیمات عمومی', 'gear'),
        ]
        self.stack = QStackedWidget(); self.stack.setStyleSheet('QStackedWidget{background:transparent;border:none;}')
        self.stack.addWidget(QuickPage(self.state))
        self.stack.addWidget(DetailsPage(self.state))
        self.stack.addWidget(TypesPage(self.state))
        self.stack.addWidget(AccessoriesPage(self.state))
        self.stack.addWidget(SettingsPage(self.state))

        self.sidebar = Sidebar(page_defs, self.switch_page)
        body.addWidget(self.sidebar)
        body.addWidget(self.stack, 1)
        outer.addLayout(body)

        root.addWidget(shell)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        self.sidebar.set_active(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setLayoutDirection(Qt.RightToLeft)
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor(BG))
    pal.setColor(QPalette.Base, QColor(CARD))
    pal.setColor(QPalette.Text, QColor(TEXT))
    app.setPalette(pal)
    app.setFont(QFont('Tahoma', 10))
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
