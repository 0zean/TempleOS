import ctypes
import random
import threading
import time
from math import *

import keyboard
import mouse
import pymem
import pymem.process
import requests
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

import img_rc

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()
dwClientState_MaxPlayer = int(response["signatures"]["dwClientState_MaxPlayer"])
m_iCompetitiveWins = int(response["netvars"]["m_iCompetitiveWins"])
dwEntityList = int(response["signatures"]["dwEntityList"])
dwGlowObjectManager = int(response["signatures"]["dwGlowObjectManager"])
m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])
m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
dwForceJump = int(response["signatures"]["dwForceJump"])
dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
m_fFlags = int(response["netvars"]["m_fFlags"])
dwForceAttack = int(response["signatures"]["dwForceAttack"])
m_iCrosshairId = int(response["netvars"]["m_iCrosshairId"])
m_flFlashMaxAlpha = int(response["netvars"]["m_flFlashMaxAlpha"])
m_iDefaultFOV = (0x332C)
dwClientState = int(response["signatures"]["dwClientState"])
m_iHealth = int(response["netvars"]["m_iHealth"])
dwViewMatrix = int(response["signatures"]["dwViewMatrix"])
m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])
dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])
m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
m_vecViewOffset = int(response["netvars"]["m_vecViewOffset"])
dwbSendPackets = int(response["signatures"]["dwbSendPackets"])
dwInput = int(response["signatures"]["dwInput"])
clientstate_net_channel = int(response["signatures"]["clientstate_net_channel"])
clientstate_last_outgoing_command = int(response["signatures"]["clientstate_last_outgoing_command"])
m_bSpotted = int(response["netvars"]["m_bSpotted"])
m_iShotsFired = int(response["netvars"]["m_iShotsFired"])
m_aimPunchAngle = int(response["netvars"]["m_aimPunchAngle"])
m_bGunGameImmunity = int(response["netvars"]["m_bGunGameImmunity"])
m_bIsDefusing = int(response["netvars"]["m_bIsDefusing"])
m_bDormant = int(response["signatures"]["m_bDormant"])
dwClientState_PlayerInfo = int(response["signatures"]["dwClientState_PlayerInfo"])
dwPlayerResource = int(response["signatures"]["dwPlayerResource"] )
m_iCompetitiveRanking = int(response["netvars"]["m_iCompetitiveRanking"])
eteam = False
antivacv2 = random.randint(1,100)
antivac = "foqnmwordqZQ$/Z§W784zw068ow78ashdijm333q33q5q4q3"
print(antivac)
print(antivacv2)
user32 = ctypes.windll.user32


def is_press(key):
    if key != "x2" and key != "x" and key != "right" and key != "wheel" and key != "left":
        return keyboard.is_pressed(key)
    else:
        return mouse.is_pressed(key)


def GetWindowText(handle, length=100):
    window_text = ctypes.create_string_buffer(length)
    user32.GetWindowTextA(
        handle,
        ctypes.byref(window_text),
        length
    )
    return window_text.value


def GetForegroundWindow():
    return user32.GetForegroundWindow()


def calc_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0.0:
        distancex = -distancex
    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0.0:
        distancey = -distancey
    return distancex, distancey


def normalizeAngles(viewAngleX, viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX < -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY < -180:
        viewAngleY += 360
    return viewAngleX, viewAngleY


def checkangles(x, y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True


def nanchecker(first, second):
    if isnan(first) or isnan(second):
        return False
    else:
        return True


def Distance(src_x, src_y, src_z, dst_x, dst_y, dst_z):
    try:
        diff_x = src_x - dst_x
        diff_y = src_y - dst_y
        diff_z = src_z - dst_z
        return sqrt(diff_x * diff_x + diff_y * diff_y + diff_z * diff_z)
    except:
        pass


def calcangle(localpos1, localpos2, localpos3, enemypos1, enemypos2, enemypos3):
    try:
        delta_x = localpos1 - enemypos1
        delta_y = localpos2 - enemypos2
        delta_z = localpos3 - enemypos3
        hyp = sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)
        x = asin(delta_z / hyp) * 180 / pi
        y = atan(delta_y / delta_x) * 180 / pi
        if delta_x >= 0.0:
            y += 180.0
    except:
        return 0,0
    return x, y


class Ui_TempleOS(object):
    def __init__(self):
        self.trigc = False
        self.wallc = False
        self.bhopc = False
        self.noflash = False
        self.trigkey = ""
        self.aimc = False
        self.silentc = False
        self.baim = False
        self.pm = pymem.Pymem("csgo.exe")
        self.client = pymem.process.module_from_name(self.pm.process_handle, "client.dll").lpBaseOfDll
        self.engine = pymem.process.module_from_name(self.pm.process_handle, "engine.dll").lpBaseOfDll
        self.rcsc = False
        self.aimrcs = True
        self.aimfov = False
        self.aimkey = str()
    def update(self):
        update = True
        while update:
            self.wallc = self.espBox.isChecked()
            self.noflash = self.flashBox.isChecked()
            self.trigc = self.trigBox.isChecked()
            self.aimc = self.aimBox.isChecked()
            if self.baim and not self.aimc:
                print("Turn on aimbot to use baim")
            if self.aimc:
                try:
                    self.aimfov = float(self.fovEdit.text())
                    self.aimkey = str(self.aimkeyEdit.text())
                except:
                    print("Use Different FOV / aim key")
                    self.aimc = False
                    self.aimBox.setChecked(False)
            try:
                self.trigkey = str(self.triggerkeyEdit.text())
            except:
                print("Use difference trigger key")
            self.bhopc = self.bhopBox.isChecked()
            self.rcsc = self.rcsBox.isChecked()
            self.silentc = self.silentaimButton.isChecked()
            if self.silentc and not self.aimc:
                print("Turn on aimbot first")
                self.silentc = False
                self.silentaimButton.setChecked(False)
            update = False
        time.sleep(1)
    def setupUi(self, TempleOS):
        if not TempleOS.objectName():
            TempleOS.setObjectName(u"Calibri")
        TempleOS.resize(460, 500)
        font = QFont()
        font.setFamilies([u"TempleOS"])
        font.setPointSize(7)
        TempleOS.setFont(font)
        #TempleOS.setDocumentMode(False)
        self.centralwidget = QWidget(TempleOS)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rcsSlider = QSlider(self.centralwidget)
        self.rcsSlider.setObjectName(u"rcsSlider")
        self.rcsSlider.setGeometry(QRect(40, 330, 131, 22))
        self.rcsSlider.setOrientation(Qt.Horizontal)
        self.aimBox = QCheckBox(self.centralwidget)
        self.aimBox.setObjectName(u"aimBox")
        self.aimBox.setGeometry(QRect(40, 40, 121, 21))
        palette = QPalette()
        brush = QBrush(QColor(67, 67, 67, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(71, 71, 71, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush1)
        brush2 = QBrush(QColor(50, 50, 50, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush2)
        brush3 = QBrush(QColor(0, 120, 215, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        brush4 = QBrush(QColor(0, 0, 0, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush4)
        brush5 = QBrush(QColor(240, 240, 240, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        brush6 = QBrush(QColor(120, 120, 120, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        self.aimBox.setPalette(palette)
        font1 = QFont()
        font1.setFamilies([u"TempleOS"])
        font1.setPointSize(12)
        font1.setBold(False)
        self.aimBox.setFont(font1)
        self.bhopBox = QCheckBox(self.centralwidget)
        self.bhopBox.setObjectName(u"bhopBox")
        self.bhopBox.setGeometry(QRect(40, 90, 171, 21))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette1.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        self.bhopBox.setPalette(palette1)
        font2 = QFont()
        font2.setFamilies([u"TempleOS"])
        font2.setPointSize(12)
        self.bhopBox.setFont(font2)
        self.flashBox = QCheckBox(self.centralwidget)
        self.flashBox.setObjectName(u"flashBox")
        self.flashBox.setGeometry(QRect(40, 140, 151, 21))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette2.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette2.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        self.flashBox.setPalette(palette2)
        self.flashBox.setFont(font2)
        self.espBox = QCheckBox(self.centralwidget)
        self.espBox.setObjectName(u"espBox")
        self.espBox.setGeometry(QRect(40, 190, 111, 21))
        palette3 = QPalette()
        palette3.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette3.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette3.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette3.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette3.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        self.espBox.setPalette(palette3)
        self.espBox.setFont(font2)
        self.rcsBox = QCheckBox(self.centralwidget)
        self.rcsBox.setObjectName(u"rcsBox")
        self.rcsBox.setGeometry(QRect(40, 290, 81, 21))
        palette4 = QPalette()
        palette4.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette4.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette4.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette4.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        self.rcsBox.setPalette(palette4)
        self.rcsBox.setFont(font2)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(40, 390, 131, 61))
        palette5 = QPalette()
        brush7 = QBrush(QColor(107, 114, 163, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette5.setBrush(QPalette.Active, QPalette.WindowText, brush7)
        brush8 = QBrush(QColor(97, 97, 138, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette5.setBrush(QPalette.Active, QPalette.ButtonText, brush8)
        palette5.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette5.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette5.setBrush(QPalette.Inactive, QPalette.ButtonText, brush4)
        palette5.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette5.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette5.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette5.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        self.pushButton.setPalette(palette5)
        self.pushButton.setFont(font2)
        self.pushButton.clicked.connect(self.update)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 350, 101, 21))
        palette6 = QPalette()
        palette6.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette6.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette6.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette6.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette6.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette6.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        self.label.setPalette(palette6)
        font3 = QFont()
        font3.setFamilies([u"TempleOS"])
        font3.setPointSize(7)
        self.label.setFont(font3)
        self.trigBox = QCheckBox(self.centralwidget)
        self.trigBox.setObjectName(u"trigBox")
        self.trigBox.setGeometry(QRect(40, 240, 201, 20))
        palette7 = QPalette()
        palette7.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette7.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette7.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette7.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette7.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette7.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        self.trigBox.setPalette(palette7)
        self.trigBox.setFont(font2)
        self.triggerkeyEdit = QLineEdit(self.centralwidget)
        self.triggerkeyEdit.setObjectName(u"triggerkeyEdit")
        self.triggerkeyEdit.setGeometry(QRect(320, 280, 101, 21))
        self.triggerkeyEdit.setFont(font)
        self.silentaimButton = QRadioButton(self.centralwidget)
        self.silentaimButton.setObjectName(u"silentaimButton")
        self.silentaimButton.setGeometry(QRect(170, 40, 81, 21))
        palette8 = QPalette()
        palette8.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette8.setBrush(QPalette.Active, QPalette.Button, brush5)
        brush9 = QBrush(QColor(255, 255, 255, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette8.setBrush(QPalette.Active, QPalette.Light, brush9)
        brush10 = QBrush(QColor(227, 227, 227, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette8.setBrush(QPalette.Active, QPalette.Midlight, brush10)
        brush11 = QBrush(QColor(160, 160, 160, 255))
        brush11.setStyle(Qt.SolidPattern)
        palette8.setBrush(QPalette.Active, QPalette.Dark, brush11)
        palette8.setBrush(QPalette.Active, QPalette.Mid, brush11)
        palette8.setBrush(QPalette.Active, QPalette.Text, brush4)
        palette8.setBrush(QPalette.Active, QPalette.BrightText, brush9)
        palette8.setBrush(QPalette.Active, QPalette.ButtonText, brush4)
        palette8.setBrush(QPalette.Active, QPalette.Base, brush9)
        palette8.setBrush(QPalette.Active, QPalette.Window, brush5)
        brush12 = QBrush(QColor(105, 105, 105, 255))
        brush12.setStyle(Qt.SolidPattern)
        palette8.setBrush(QPalette.Active, QPalette.Shadow, brush12)
        palette8.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette8.setBrush(QPalette.Active, QPalette.HighlightedText, brush9)
        brush13 = QBrush(QColor(0, 0, 255, 255))
        brush13.setStyle(Qt.SolidPattern)
        palette8.setBrush(QPalette.Active, QPalette.Link, brush13)
        brush14 = QBrush(QColor(255, 0, 255, 255))
        brush14.setStyle(Qt.SolidPattern)
        palette8.setBrush(QPalette.Active, QPalette.LinkVisited, brush14)
        brush15 = QBrush(QColor(245, 245, 245, 255))
        brush15.setStyle(Qt.SolidPattern)
        palette8.setBrush(QPalette.Active, QPalette.AlternateBase, brush15)
        palette8.setBrush(QPalette.Active, QPalette.NoRole, brush4)
        brush16 = QBrush(QColor(255, 255, 220, 255))
        brush16.setStyle(Qt.SolidPattern)
        palette8.setBrush(QPalette.Active, QPalette.ToolTipBase, brush16)
        palette8.setBrush(QPalette.Active, QPalette.ToolTipText, brush4)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Active, QPalette.PlaceholderText, brush4)
#endif
        palette8.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette8.setBrush(QPalette.Inactive, QPalette.Button, brush5)
        palette8.setBrush(QPalette.Inactive, QPalette.Light, brush9)
        palette8.setBrush(QPalette.Inactive, QPalette.Midlight, brush10)
        palette8.setBrush(QPalette.Inactive, QPalette.Dark, brush11)
        palette8.setBrush(QPalette.Inactive, QPalette.Mid, brush11)
        palette8.setBrush(QPalette.Inactive, QPalette.Text, brush4)
        palette8.setBrush(QPalette.Inactive, QPalette.BrightText, brush9)
        palette8.setBrush(QPalette.Inactive, QPalette.ButtonText, brush4)
        palette8.setBrush(QPalette.Inactive, QPalette.Base, brush9)
        palette8.setBrush(QPalette.Inactive, QPalette.Window, brush5)
        palette8.setBrush(QPalette.Inactive, QPalette.Shadow, brush12)
        palette8.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette8.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush4)
        palette8.setBrush(QPalette.Inactive, QPalette.Link, brush13)
        palette8.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush14)
        palette8.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush15)
        brush17 = QBrush(QColor(0, 0, 0, 255))
        brush17.setStyle(Qt.NoBrush)
        palette8.setBrush(QPalette.Inactive, QPalette.NoRole, brush17)
        palette8.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush16)
        palette8.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush4)
        brush18 = QBrush(QColor(0, 0, 0, 255))
        brush18.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush18)
#endif
        palette8.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette8.setBrush(QPalette.Disabled, QPalette.Button, brush5)
        palette8.setBrush(QPalette.Disabled, QPalette.Light, brush9)
        brush19 = QBrush(QColor(247, 247, 247, 255))
        brush19.setStyle(Qt.SolidPattern)
        palette8.setBrush(QPalette.Disabled, QPalette.Midlight, brush19)
        palette8.setBrush(QPalette.Disabled, QPalette.Dark, brush11)
        palette8.setBrush(QPalette.Disabled, QPalette.Mid, brush11)
        palette8.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette8.setBrush(QPalette.Disabled, QPalette.BrightText, brush9)
        palette8.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette8.setBrush(QPalette.Disabled, QPalette.Base, brush5)
        palette8.setBrush(QPalette.Disabled, QPalette.Window, brush5)
        palette8.setBrush(QPalette.Disabled, QPalette.Shadow, brush4)
        palette8.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        palette8.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush9)
        palette8.setBrush(QPalette.Disabled, QPalette.Link, brush13)
        palette8.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush14)
        palette8.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush15)
        brush20 = QBrush(QColor(0, 0, 0, 255))
        brush20.setStyle(Qt.NoBrush)
        palette8.setBrush(QPalette.Disabled, QPalette.NoRole, brush20)
        palette8.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush16)
        palette8.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush4)
        brush21 = QBrush(QColor(0, 0, 0, 255))
        brush21.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush21)
#endif
        self.silentaimButton.setPalette(palette8)
        self.silentaimButton.setFont(font)
        self.aimkeyEdit = QLineEdit(self.centralwidget)
        self.aimkeyEdit.setObjectName(u"aimkeyEdit")
        self.aimkeyEdit.setGeometry(QRect(320, 330, 101, 21))
        self.aimkeyEdit.setFont(font)
        self.fovEdit = QLineEdit(self.centralwidget)
        self.fovEdit.setObjectName(u"fovEdit")
        self.fovEdit.setGeometry(QRect(320, 380, 101, 21))
        self.fovEdit.setFont(font)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(320, 260, 101, 20))
        palette9 = QPalette()
        palette9.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette9.setBrush(QPalette.Active, QPalette.Button, brush5)
        palette9.setBrush(QPalette.Active, QPalette.Light, brush9)
        palette9.setBrush(QPalette.Active, QPalette.Midlight, brush10)
        palette9.setBrush(QPalette.Active, QPalette.Dark, brush11)
        palette9.setBrush(QPalette.Active, QPalette.Mid, brush11)
        palette9.setBrush(QPalette.Active, QPalette.Text, brush4)
        palette9.setBrush(QPalette.Active, QPalette.BrightText, brush9)
        palette9.setBrush(QPalette.Active, QPalette.ButtonText, brush4)
        palette9.setBrush(QPalette.Active, QPalette.Base, brush9)
        palette9.setBrush(QPalette.Active, QPalette.Window, brush5)
        palette9.setBrush(QPalette.Active, QPalette.Shadow, brush12)
        palette9.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette9.setBrush(QPalette.Active, QPalette.HighlightedText, brush9)
        palette9.setBrush(QPalette.Active, QPalette.Link, brush13)
        palette9.setBrush(QPalette.Active, QPalette.LinkVisited, brush14)
        palette9.setBrush(QPalette.Active, QPalette.AlternateBase, brush15)
        palette9.setBrush(QPalette.Active, QPalette.NoRole, brush4)
        palette9.setBrush(QPalette.Active, QPalette.ToolTipBase, brush16)
        palette9.setBrush(QPalette.Active, QPalette.ToolTipText, brush4)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Active, QPalette.PlaceholderText, brush4)
#endif
        palette9.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette9.setBrush(QPalette.Inactive, QPalette.Button, brush5)
        palette9.setBrush(QPalette.Inactive, QPalette.Light, brush9)
        palette9.setBrush(QPalette.Inactive, QPalette.Midlight, brush10)
        palette9.setBrush(QPalette.Inactive, QPalette.Dark, brush11)
        palette9.setBrush(QPalette.Inactive, QPalette.Mid, brush11)
        palette9.setBrush(QPalette.Inactive, QPalette.Text, brush4)
        palette9.setBrush(QPalette.Inactive, QPalette.BrightText, brush9)
        palette9.setBrush(QPalette.Inactive, QPalette.ButtonText, brush4)
        palette9.setBrush(QPalette.Inactive, QPalette.Base, brush9)
        palette9.setBrush(QPalette.Inactive, QPalette.Window, brush5)
        palette9.setBrush(QPalette.Inactive, QPalette.Shadow, brush12)
        palette9.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette9.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush4)
        palette9.setBrush(QPalette.Inactive, QPalette.Link, brush13)
        palette9.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush14)
        palette9.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush15)
        brush22 = QBrush(QColor(0, 0, 0, 255))
        brush22.setStyle(Qt.NoBrush)
        palette9.setBrush(QPalette.Inactive, QPalette.NoRole, brush22)
        palette9.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush16)
        palette9.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush4)
        brush23 = QBrush(QColor(0, 0, 0, 255))
        brush23.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush23)
#endif
        palette9.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette9.setBrush(QPalette.Disabled, QPalette.Button, brush5)
        palette9.setBrush(QPalette.Disabled, QPalette.Light, brush9)
        palette9.setBrush(QPalette.Disabled, QPalette.Midlight, brush19)
        palette9.setBrush(QPalette.Disabled, QPalette.Dark, brush11)
        palette9.setBrush(QPalette.Disabled, QPalette.Mid, brush11)
        palette9.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette9.setBrush(QPalette.Disabled, QPalette.BrightText, brush9)
        palette9.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette9.setBrush(QPalette.Disabled, QPalette.Base, brush5)
        palette9.setBrush(QPalette.Disabled, QPalette.Window, brush5)
        palette9.setBrush(QPalette.Disabled, QPalette.Shadow, brush4)
        palette9.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        palette9.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush9)
        palette9.setBrush(QPalette.Disabled, QPalette.Link, brush13)
        palette9.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush14)
        palette9.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush15)
        brush24 = QBrush(QColor(0, 0, 0, 255))
        brush24.setStyle(Qt.NoBrush)
        palette9.setBrush(QPalette.Disabled, QPalette.NoRole, brush24)
        palette9.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush16)
        palette9.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush4)
        brush25 = QBrush(QColor(0, 0, 0, 255))
        brush25.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush25)
#endif
        self.label_2.setPalette(palette9)
        self.label_2.setFont(font)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(340, 310, 71, 16))
        palette10 = QPalette()
        palette10.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette10.setBrush(QPalette.Active, QPalette.Button, brush5)
        palette10.setBrush(QPalette.Active, QPalette.Light, brush9)
        palette10.setBrush(QPalette.Active, QPalette.Midlight, brush10)
        palette10.setBrush(QPalette.Active, QPalette.Dark, brush11)
        palette10.setBrush(QPalette.Active, QPalette.Mid, brush11)
        palette10.setBrush(QPalette.Active, QPalette.Text, brush4)
        palette10.setBrush(QPalette.Active, QPalette.BrightText, brush9)
        palette10.setBrush(QPalette.Active, QPalette.ButtonText, brush4)
        palette10.setBrush(QPalette.Active, QPalette.Base, brush9)
        palette10.setBrush(QPalette.Active, QPalette.Window, brush5)
        palette10.setBrush(QPalette.Active, QPalette.Shadow, brush12)
        palette10.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette10.setBrush(QPalette.Active, QPalette.HighlightedText, brush9)
        palette10.setBrush(QPalette.Active, QPalette.Link, brush13)
        palette10.setBrush(QPalette.Active, QPalette.LinkVisited, brush14)
        palette10.setBrush(QPalette.Active, QPalette.AlternateBase, brush15)
        palette10.setBrush(QPalette.Active, QPalette.NoRole, brush4)
        palette10.setBrush(QPalette.Active, QPalette.ToolTipBase, brush16)
        palette10.setBrush(QPalette.Active, QPalette.ToolTipText, brush4)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette10.setBrush(QPalette.Active, QPalette.PlaceholderText, brush4)
#endif
        palette10.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette10.setBrush(QPalette.Inactive, QPalette.Button, brush5)
        palette10.setBrush(QPalette.Inactive, QPalette.Light, brush9)
        palette10.setBrush(QPalette.Inactive, QPalette.Midlight, brush10)
        palette10.setBrush(QPalette.Inactive, QPalette.Dark, brush11)
        palette10.setBrush(QPalette.Inactive, QPalette.Mid, brush11)
        palette10.setBrush(QPalette.Inactive, QPalette.Text, brush4)
        palette10.setBrush(QPalette.Inactive, QPalette.BrightText, brush9)
        palette10.setBrush(QPalette.Inactive, QPalette.ButtonText, brush4)
        palette10.setBrush(QPalette.Inactive, QPalette.Base, brush9)
        palette10.setBrush(QPalette.Inactive, QPalette.Window, brush5)
        palette10.setBrush(QPalette.Inactive, QPalette.Shadow, brush12)
        palette10.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette10.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush4)
        palette10.setBrush(QPalette.Inactive, QPalette.Link, brush13)
        palette10.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush14)
        palette10.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush15)
        brush26 = QBrush(QColor(0, 0, 0, 255))
        brush26.setStyle(Qt.NoBrush)
        palette10.setBrush(QPalette.Inactive, QPalette.NoRole, brush26)
        palette10.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush16)
        palette10.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush4)
        brush27 = QBrush(QColor(0, 0, 0, 255))
        brush27.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette10.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush27)
#endif
        palette10.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette10.setBrush(QPalette.Disabled, QPalette.Button, brush5)
        palette10.setBrush(QPalette.Disabled, QPalette.Light, brush9)
        palette10.setBrush(QPalette.Disabled, QPalette.Midlight, brush19)
        palette10.setBrush(QPalette.Disabled, QPalette.Dark, brush11)
        palette10.setBrush(QPalette.Disabled, QPalette.Mid, brush11)
        palette10.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette10.setBrush(QPalette.Disabled, QPalette.BrightText, brush9)
        palette10.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette10.setBrush(QPalette.Disabled, QPalette.Base, brush5)
        palette10.setBrush(QPalette.Disabled, QPalette.Window, brush5)
        palette10.setBrush(QPalette.Disabled, QPalette.Shadow, brush4)
        palette10.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        palette10.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush9)
        palette10.setBrush(QPalette.Disabled, QPalette.Link, brush13)
        palette10.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush14)
        palette10.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush15)
        brush28 = QBrush(QColor(0, 0, 0, 255))
        brush28.setStyle(Qt.NoBrush)
        palette10.setBrush(QPalette.Disabled, QPalette.NoRole, brush28)
        palette10.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush16)
        palette10.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush4)
        brush29 = QBrush(QColor(0, 0, 0, 255))
        brush29.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette10.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush29)
#endif
        self.label_4.setPalette(palette10)
        self.label_4.setFont(font)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(340, 360, 71, 20))
        palette11 = QPalette()
        palette11.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette11.setBrush(QPalette.Active, QPalette.Button, brush5)
        palette11.setBrush(QPalette.Active, QPalette.Light, brush9)
        palette11.setBrush(QPalette.Active, QPalette.Midlight, brush10)
        palette11.setBrush(QPalette.Active, QPalette.Dark, brush11)
        palette11.setBrush(QPalette.Active, QPalette.Mid, brush11)
        palette11.setBrush(QPalette.Active, QPalette.Text, brush4)
        palette11.setBrush(QPalette.Active, QPalette.BrightText, brush9)
        palette11.setBrush(QPalette.Active, QPalette.ButtonText, brush4)
        palette11.setBrush(QPalette.Active, QPalette.Base, brush9)
        palette11.setBrush(QPalette.Active, QPalette.Window, brush5)
        palette11.setBrush(QPalette.Active, QPalette.Shadow, brush12)
        palette11.setBrush(QPalette.Active, QPalette.Highlight, brush3)
        palette11.setBrush(QPalette.Active, QPalette.HighlightedText, brush9)
        palette11.setBrush(QPalette.Active, QPalette.Link, brush13)
        palette11.setBrush(QPalette.Active, QPalette.LinkVisited, brush14)
        palette11.setBrush(QPalette.Active, QPalette.AlternateBase, brush15)
        palette11.setBrush(QPalette.Active, QPalette.NoRole, brush4)
        palette11.setBrush(QPalette.Active, QPalette.ToolTipBase, brush16)
        palette11.setBrush(QPalette.Active, QPalette.ToolTipText, brush4)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette11.setBrush(QPalette.Active, QPalette.PlaceholderText, brush4)
#endif
        palette11.setBrush(QPalette.Inactive, QPalette.WindowText, brush4)
        palette11.setBrush(QPalette.Inactive, QPalette.Button, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Light, brush9)
        palette11.setBrush(QPalette.Inactive, QPalette.Midlight, brush10)
        palette11.setBrush(QPalette.Inactive, QPalette.Dark, brush11)
        palette11.setBrush(QPalette.Inactive, QPalette.Mid, brush11)
        palette11.setBrush(QPalette.Inactive, QPalette.Text, brush4)
        palette11.setBrush(QPalette.Inactive, QPalette.BrightText, brush9)
        palette11.setBrush(QPalette.Inactive, QPalette.ButtonText, brush4)
        palette11.setBrush(QPalette.Inactive, QPalette.Base, brush9)
        palette11.setBrush(QPalette.Inactive, QPalette.Window, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Shadow, brush12)
        palette11.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush4)
        palette11.setBrush(QPalette.Inactive, QPalette.Link, brush13)
        palette11.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush14)
        palette11.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush15)
        brush30 = QBrush(QColor(0, 0, 0, 255))
        brush30.setStyle(Qt.NoBrush)
        palette11.setBrush(QPalette.Inactive, QPalette.NoRole, brush30)
        palette11.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush16)
        palette11.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush4)
        brush31 = QBrush(QColor(0, 0, 0, 255))
        brush31.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette11.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush31)
#endif
        palette11.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette11.setBrush(QPalette.Disabled, QPalette.Button, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Light, brush9)
        palette11.setBrush(QPalette.Disabled, QPalette.Midlight, brush19)
        palette11.setBrush(QPalette.Disabled, QPalette.Dark, brush11)
        palette11.setBrush(QPalette.Disabled, QPalette.Mid, brush11)
        palette11.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette11.setBrush(QPalette.Disabled, QPalette.BrightText, brush9)
        palette11.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette11.setBrush(QPalette.Disabled, QPalette.Base, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Window, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Shadow, brush4)
        palette11.setBrush(QPalette.Disabled, QPalette.Highlight, brush3)
        palette11.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush9)
        palette11.setBrush(QPalette.Disabled, QPalette.Link, brush13)
        palette11.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush14)
        palette11.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush15)
        brush32 = QBrush(QColor(0, 0, 0, 255))
        brush32.setStyle(Qt.NoBrush)
        palette11.setBrush(QPalette.Disabled, QPalette.NoRole, brush32)
        palette11.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush16)
        palette11.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush4)
        brush33 = QBrush(QColor(0, 0, 0, 255))
        brush33.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette11.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush33)
#endif
        self.label_5.setPalette(palette11)
        self.label_5.setFont(font)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 0, 461, 471))
        self.label_3.setStyleSheet(u"background-image: url(:/newPrefix/grey.png);")
        TempleOS.setCentralWidget(self.centralwidget)
        self.label_3.raise_()
        self.rcsSlider.raise_()
        self.aimBox.raise_()
        self.bhopBox.raise_()
        self.flashBox.raise_()
        self.espBox.raise_()
        self.rcsBox.raise_()
        self.pushButton.raise_()
        self.label.raise_()
        self.trigBox.raise_()
        self.triggerkeyEdit.raise_()
        self.silentaimButton.raise_()
        self.aimkeyEdit.raise_()
        self.fovEdit.raise_()
        self.label_2.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.menubar = QMenuBar(TempleOS)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 460, 18))
        TempleOS.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(TempleOS)
        self.statusbar.setObjectName(u"statusbar")
        TempleOS.setStatusBar(self.statusbar)
        self.retranslateUi(TempleOS)
        QMetaObject.connectSlotsByName(TempleOS)
    # setupUi
    def retranslateUi(self, TempleOS):
        TempleOS.setWindowTitle(QCoreApplication.translate("TempleOS", u"TempleOS", None))
        self.aimBox.setText(QCoreApplication.translate("TempleOS", u"Aimbot", None))
        self.bhopBox.setText(QCoreApplication.translate("TempleOS", u"Bunny Hop", None))
        self.flashBox.setText(QCoreApplication.translate("TempleOS", u"No Flash", None))
        self.espBox.setText(QCoreApplication.translate("TempleOS", u"Walls", None))
        self.rcsBox.setText(QCoreApplication.translate("TempleOS", u"RCS", None))
        self.pushButton.setText(QCoreApplication.translate("TempleOS", u"Update", None))
        self.label.setText(QCoreApplication.translate("TempleOS", u"rcs slider", None))
        self.trigBox.setText(QCoreApplication.translate("TempleOS", u"Trigger Bot", None))
        self.silentaimButton.setText(QCoreApplication.translate("TempleOS", u"Silent", None))
        self.label_2.setText(QCoreApplication.translate("TempleOS", u"Trigger Key", None))
        self.label_4.setText(QCoreApplication.translate("TempleOS", u"Aim Key", None))
        self.label_5.setText(QCoreApplication.translate("TempleOS", u"Aim FOV", None))
        self.label_3.setText("")
    # retranslateUi
    def main(self):
        pm = self.pm
        client = self.client
        engine = self.engine
        player = pm.read_uint(client + dwLocalPlayer)
        engine_pointer = pm.read_uint(engine + dwClientState)
        while True:
            #if not GetWindowText(GetForegroundWindow()).decode('cp1252') == "Counter-Strike: Global Offensive":
            #    time.sleep(1)
            #    continue
            pm.write_uchar(engine + dwbSendPackets, 1)
            target = None
            olddistx = 111111111111
            olddisty = 111111111111
            if client and engine and pm:
                try:
                    #player = pm.read_uint(client + dwLocalPlayer)
                    #engine_pointer = pm.read_uint(engine + dwClientState)
                    glow_manager = pm.read_uint(client + dwGlowObjectManager)
                    crosshairID = pm.read_uint(player + m_iCrosshairId)
                    getcrosshairTarget = pm.read_uint(client + dwEntityList + (crosshairID - 1) * 0x10)
                     #immunitygunganme = pm.read_uint(getcrosshairTarget + m_bGunGameImmunity )
                    localTeam = pm.read_uint(player + m_iTeamNum)
                    crosshairTeam = pm.read_uint(getcrosshairTarget + m_iTeamNum)
                except:
                    print("Round not started yet")
                    time.sleep(5)
                    continue
            for i in range(1, 32):
                entity = pm.read_uint(client + dwEntityList + i * 0x10)
                if entity:
                    try:
                        entity_glow = pm.read_uint(entity + m_iGlowIndex)
                        entity_team_id = pm.read_uint(entity + m_iTeamNum)
                        #entity_isdefusing = pm.read_uint(entity + m_bIsDefusing)
                        entity_hp = pm.read_uint(entity + m_iHealth)
                        entity_dormant = pm.read_uint(entity + m_bDormant)
                    except:
                        print("Could not load Players Infos")
                        time.sleep(2)
                        continue
                    if entity_hp > 50 and not entity_hp == 100:
                        r, g, b = 255, 165, 0
                    elif entity_hp < 50:
                        r, g, b = 255, 0, 0
                    elif entity_hp == 100 and entity_team_id == 2:
                        r, g, b = 0, 255, 0
                    else:
                        r, g, b = 0, 255, 0
                    if self.aimc and localTeam != entity_team_id and entity_hp > 0:
                        entity_bones = pm.read_uint(entity + m_dwBoneMatrix)
                        localpos_x_angles = pm.read_float(engine_pointer + dwClientState_ViewAngles)
                        localpos_y_angles = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                        localpos1 = pm.read_float(player + m_vecOrigin)
                        localpos2 = pm.read_float(player + m_vecOrigin + 4)
                        localpos_z_angles = pm.read_float(player + m_vecViewOffset + 0x8)
                        localpos3 = pm.read_float(player + m_vecOrigin + 8) + localpos_z_angles
                        if self.baim:
                            try:
                                entitypos_x = pm.read_float(entity_bones + 0x30 * 5 + 0xC)
                                entitypos_y = pm.read_float(entity_bones + 0x30 * 5 + 0x1C)
                                entitypos_z = pm.read_float(entity_bones + 0x30 * 5 + 0x2C)
                            except:
                                continue
                        else:
                            try:
                                entitypos_x = pm.read_float(entity_bones + 0x30 * 8 + 0xC)
                                entitypos_y = pm.read_float(entity_bones + 0x30 * 8 + 0x1C)
                                entitypos_z = pm.read_float(entity_bones + 0x30 * 8 + 0x2C)
                            except:
                                continue
                        X, Y = calcangle(localpos1, localpos2, localpos3, entitypos_x, entitypos_y, entitypos_z)
                        newdist_x, newdist_y = calc_distance(localpos_x_angles, localpos_y_angles, X, Y)
                        if newdist_x < olddistx and newdist_y < olddisty and newdist_x <= self.aimfov and newdist_y <= self.aimfov:
                            olddistx, olddisty = newdist_x, newdist_y
                            target, target_hp, target_dormant = entity, entity_hp, entity_dormant
                            target_x, target_y, target_z = entitypos_x, entitypos_y, entitypos_z
                    if self.aimc and is_press(self.aimkey) and player:
                        if target and target_hp > 0 and not target_dormant:
                            pitch, yaw = calcangle(localpos1, localpos2, localpos3, target_x, target_y, target_z)
                            normalize_x, normalize_y = normalizeAngles(pitch, yaw)
                            punchx = pm.read_float(player + m_aimPunchAngle)
                            punchy = pm.read_float(player + m_aimPunchAngle + 0x4)
                            if self.silentc:
                                pm.write_uchar(engine + dwbSendPackets, 0)
                                Commands = pm.read_uint(client + dwInput + 0xF4)
                                VerifedCommands = pm.read_uint(client + dwInput + 0xF8 )
                                Desired = pm.read_uint(engine_pointer + clientstate_last_outgoing_command ) + 2
                                OldUser = Commands + ((Desired - 1) % 150) * 100
                                VerifedOldUser = VerifedCommands + ((Desired - 1) % 150) * 0x68
                                m_buttons = pm.read_uint(OldUser + 0x30)
                                Net_Channel = pm.read_uint(engine_pointer + clientstate_net_channel)
                                if pm.read_uint(Net_Channel + 0x18) < Desired:
                                    pass
                                elif self.aimrcs:
                                    pm.write_float(OldUser + 0x0C, normalize_x)
                                    pm.write_float(OldUser + 0x10, normalize_y)
                                    pm.write_int(OldUser + 0x30, m_buttons | (1 << 0))
                                    pm.write_float(VerifedOldUser + 0x0C, normalize_x - (punchx * 2))
                                    pm.write_float(VerifedOldUser + 0x10, normalize_y - (punchy * 2))
                                    pm.write_int(VerifedOldUser + 0x30, m_buttons | (1 << 0))
                                    pm.write_uchar(engine + dwbSendPackets, 1)
                                else:
                                    pm.write_float(OldUser + 0x0C, normalize_x)
                                    pm.write_float(OldUser + 0x10, normalize_y)
                                    pm.write_int(OldUser + 0x30, m_buttons | (1 << 0))
                                    pm.write_float(VerifedOldUser + 0x0C, normalize_x)
                                    pm.write_float(VerifedOldUser + 0x10, normalize_y)
                                    pm.write_int(VerifedOldUser + 0x30, m_buttons | (1 << 0))
                                    pm.write_uchar(engine + dwbSendPackets, 1)
                            elif self.aimrcs and pm.read_uint(player + m_iShotsFired) > 1:
                                pm.write_float(engine_pointer + dwClientState_ViewAngles, normalize_x - (punchx * 2))
                                pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, normalize_y - (punchy * 2))
                            else:
                                pm.write_float(engine_pointer + dwClientState_ViewAngles, normalize_x)
                                pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, normalize_y)
                    if self.wallc and entity_team_id != localTeam and not entity_dormant: # Terrorist Glow
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(r))    # R
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(g))    # G
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(b))   # B
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(255)) # A
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # Enable
                    else:
                        pass
            if self.trigc and is_press(
                    self.trigkey) and 0 < crosshairID <= 64 and localTeam != crosshairTeam:
                self.pm.write_int(client + dwForceAttack, 6)
            if self.noflash and player:
                flash_value = player + m_flFlashMaxAlpha
                if flash_value:
                    self.pm.write_float(flash_value, float(0))
            if self.rcsc:
                #oldpunchx = 0.0
                #oldpunchy = 0.0
                if pm.read_uint(player + m_iShotsFired) > 1:
                    rcs_x = pm.read_float(engine_pointer + dwClientState_ViewAngles)
                    rcs_y = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                    punchx = pm.read_float(player + m_aimPunchAngle)
                    punchy = pm.read_float(player + m_aimPunchAngle + 0x4)
                    newrcsx = rcs_x - (punchx - oldpunchx) * float(2)
                    newrcsy = rcs_y - (punchy - oldpunchy) * float(2)
                    newrcs, newrcy = normalizeAngles(newrcsx, newrcsy)
                    oldpunchx = punchx
                    oldpunchy = punchy
                    if nanchecker(newrcsx, newrcsy) and checkangles(newrcsx, newrcsy):
                        pm.write_float(engine_pointer + dwClientState_ViewAngles, newrcsx)
                        pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, newrcsy)
                else:
                    oldpunchx = oldpunchy = 0.0
            if self.bhopc:
                if is_press("space"):
                    force_jump = client + dwForceJump
                    on_ground = pm.read_uint(player + m_fFlags)
                    if player and on_ground and on_ground == 257:
                        pm.write_int(force_jump, 5)
                        time.sleep(0.06)
                        pm.write_int(force_jump, 4)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = QMainWindow()
    ui = Ui_TempleOS()
    ui.setupUi(Dialog)
    Dialog.show()
    threading.Thread(target=ui.main).start()
    sys.exit(app.exec_())
