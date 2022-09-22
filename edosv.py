#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 23:57:47 2021

@author: marcio
"""
cor = ['#FF0000', '#00FF00','#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#006400', "#000080", '#FF8C00', '#FF4500',	'#9400D3']
import sys
#PyQt5
import time
from PyQt5.QtWidgets import (QFileDialog, QMainWindow, QMessageBox, QPushButton,
                             QLabel, QApplication, QRadioButton, QFrame, QWidget,
                             QLineEdit, QComboBox, QVBoxLayout, QProgressBar)
from PyQt5.QtCore import  QRect
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
# matplotlib
import matplotlib as mpl
from cycler import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color=cor)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
import os # interage com o sistema operacional
import modulo3 ## módulo das funções DOS E pDOS
import numpy as np
##------------------ cores da interface --------------------------------------
background = "background:#555555" # Interface
cor_area_texto = 'background:#606060' # Área de texto
cor_texto = 'white' # Cor do texto na caixa de textos
line_edit = 'background:#707070;font-size:14px' # Linha de inserção de dados
path = os.path.dirname(os.path.realpath(__file__))
##############################################################################
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=9, height=6, dpi=400):
        self.fig = Figure(figsize=(width, height), dpi=dpi,facecolor='#656565')
        self.fig.set_tight_layout(True)
        self.axes = self.fig.add_subplot(111)# linha; coluna; posição;
        self.axes.set_facecolor("white")
        self.axes.xaxis.set_minor_locator(AutoMinorLocator(5))
        self.axes.yaxis.set_minor_locator(AutoMinorLocator(5))
        self.axes.axhline(y=0, linestyle='--', color='k')
        self.axes.axvline(x=0, linestyle='--', color='k')
        super(MplCanvas, self).__init__(self.fig)
class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('DOSView')
        self.setFixedSize(1000, 500)
        self.setStyleSheet(background)
        self.setWindowIcon(QIcon(path+"/temps/icon1.png"))
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        ## Barra de menu ####
        self.menubar = self.menuBar()
        self.menubar.setStyleSheet("font-size:15px")
        self.arquivo = self.menubar.addMenu('File')
        self.arquivo.setStyleSheet("font-size:14px")
        self.ajuda = self.arquivo.addAction('Help')
        self.ajuda.triggered.connect(self.AjudaDef)
        self.ajuda.setShortcut("F2")
        self.sobre = self.arquivo.addAction('About')
        self.sobre.triggered.connect(self.SobreDef)
        self.sobre.setShortcut("F3")
        self.fechar = self.arquivo.addAction('Quit')
        self.fechar.triggered.connect(self.FecharDef)
        self.fechar.setShortcut("F4")
        self.messageBox = QMessageBox()
        self.main_widget = QWidget(self)
        self.main_widget.setGeometry(475,30,520,560)
        self.frame1 = QFrame(self)
        self.frame1.setGeometry(375,0, 630, 600)
        self.frame1.setStyleSheet(background)
#----------------------- grupo 1 ----------------------------------------
        self.GrupDOS = QFrame(self)
        self.GrupDOS.setGeometry(10,25,360,130)
        self.GrupDOS.setStyleSheet("background:#606060")
#-----------------------------------------------------------------------------
        self.Titulo3 = QLabel(self.GrupDOS,text='DOS')
        self.Titulo3.setGeometry(10, 0, 100, 30)
        self.Titulo3.setStyleSheet("color:blue;font-size:18px")
        self.line_dosV = QLineEdit(self.GrupDOS)
        self.line_dosV.setGeometry(5, 40, 305, 30)
        self.line_dosV.setStyleSheet(line_edit)
        self.search13 = QPushButton(self.GrupDOS)
        self.search13.setIcon(QIcon(path+"/temps/lupa.png"))
        self.search13.setGeometry(QRect(315, 40, 40, 30))
        self.search13.clicked.connect(self.ReadDOS)       ## click connect
        self.search13.setToolTip("Search")
        self.series = QLabel(self.GrupDOS,text='Série')
        self.series.setGeometry(10, 80, 50, 30)
        self.series.setStyleSheet("font-size:14px")
        self.combo11 = QComboBox(self.GrupDOS)
        self.combo11.setGeometry(50, 80, 55, 30)
        self.combo11.setStyleSheet("font-size:14px")
        self.combo11.addItems(["+","-"])
        self.combo12 = QComboBox(self.GrupDOS)
        self.combo12.setGeometry(110, 80, 140, 30)
        self.combo12.setStyleSheet("font-size:14px")
        self.combo12.addItems(["DOS","intDOS"])
        self.Calculete13 = QPushButton(self.GrupDOS, text='Calcule')
        self.Calculete13.setGeometry(QRect(255, 80, 100, 30))
        self.Calculete13.setToolTip("to calculete")
        self.Calculete13.clicked.connect(self.DOS)
#---------------------------- grupo 2 ----------------------------------------
        self.GrupPDOS = QFrame(self)
        self.GrupPDOS.setGeometry(10,160,360,160)
        self.GrupPDOS.setStyleSheet("background:#606060")
#-----------------------------------------------------------------------------
        self.Titulo4 = QLabel(self.GrupPDOS,text='pDOS')
        self.Titulo4.setGeometry(10, 0, 100, 30)
        self.Titulo4.setStyleSheet("color:blue;font-size:18px")
        self.line_pdosV = QLineEdit(self.GrupPDOS)
        self.line_pdosV.setGeometry(5, 35, 305, 30)
        self.line_pdosV.setStyleSheet(line_edit)
        self.search23 = QPushButton(self.GrupPDOS)
        self.search23.setIcon(QIcon(path+"/temps/lupa.png"))
        self.search23.setGeometry(QRect(315, 35, 40, 30))
        self.search23.clicked.connect(self.ReadPDOS)       ## click connect
        self.search23.setToolTip("Search")
        self.series1 = QLabel(self.GrupPDOS,text='Série')
        self.series1.setGeometry(10, 110, 50, 30)
        self.series1.setStyleSheet("font-size:14px")
        self.combo21 = QComboBox(self.GrupPDOS)
        self.combo21.setGeometry(50, 110, 55, 30)
        self.combo21.setStyleSheet("font-size:14px")
        self.combo21.addItems(["+","-"])
        self.combo22 = QComboBox(self.GrupPDOS)
        self.combo22.setGeometry(110, 110, 140, 30)
        self.combo22.addItems(["lDOS", "pDOS"])
        self.combo22.setStyleSheet("font-size:14px")
#-----------------------------------------------------------------------------
        self.label = QLabel(self.GrupPDOS,text='Orbitals')
        self.label.setGeometry(10, 75, 100, 30)
        self.label.setStyleSheet("font-size:14px")
        self.orbital = QComboBox(self.GrupPDOS)
        self.orbital.setGeometry(110, 75, 245, 30)
        self.orbital.setStyleSheet("font-size:14px")
        self.Calculete23 = QPushButton(self.GrupPDOS, text='Calcule')
        self.Calculete23.setGeometry(QRect(255, 110, 100, 30))
        self.Calculete23.setToolTip("to calculete")
        self.Calculete23.clicked.connect(self.pDOS)

        self.mono = QRadioButton(self, text='Magnetic')
        self.mono.setStyleSheet("background:#707070;font-size:14px")
        self.mono.setGeometry(10, 330, 100, 30)
        self.mono.toggled.connect(self.Magnetic)
        self.mono.toggled.connect(self.Combo)
        self.mono.setToolTip("Select if calculated with polarized spin")

        self.E_Fermi = QLabel(self,text='Fermi Energy (eV)')
        self.E_Fermi.setStyleSheet("font-size:14px")
        self.E_Fermi.setGeometry(140, 330, 120, 30)
        self.EFermi = QLineEdit(self)
        self.EFermi.setGeometry(270, 330, 100, 30)
        self.EFermi.setStyleSheet(line_edit)
        self.EFermi.setText('0.000')
        self.EFermi.setAlignment(QtCore.Qt.AlignRight)
#----------------------- grupo 3 ----------------------------------------
        self.frame3 = QFrame(self)
        self.frame3.setGeometry(10,370,360,50)
        self.frame3.setStyleSheet("background:#606060")

        self.line_label = QLineEdit(self.frame3)
        self.line_label.setGeometry(5, 10, 100, 30)
        self.line_label.setStyleSheet(line_edit)
        self.line_label.setText('Label')

        self.s_data = QComboBox(self.frame3)
        self.s_data.setGeometry(110,10,140,30)
        self.s_data.setStyleSheet("font-size:14px")
        self.s_data.setToolTip("list with data series")

        self.btn_remove = QPushButton(self.frame3,text='Remove data')#
        self.btn_remove.setGeometry(QRect(255, 10, 100, 30))
        self.btn_remove.clicked.connect(self.Remove) ##
        self.btn_remove.setStyleSheet("font-size:14px")
        self.btn_remove.setToolTip("Remove the current data")



#-------------------------botões 2 ---------------------------------------------
        self.GrupButton2 = QFrame(self)
        self.GrupButton2.setGeometry(10,430,360,40)
        self.GrupButton2.setStyleSheet("background:#606060")
        self.btn_5 = QPushButton(self.GrupButton2,text='Clean')# botão salvar
        self.btn_5.setGeometry(QRect(5, 5, 80, 30))
        self.btn_5.clicked.connect(self.Clean) ## conecta a função salvar
        self.btn_5.setStyleSheet("font-size:14px")
        self.btn_6 = QPushButton(self.GrupButton2,text='Save')# botão salvar
        self.btn_6.setGeometry(QRect(95, 5, 80, 30))
        self.btn_6.clicked.connect(self.Salvar) ## conecta a função salvar
        self.btn_6.setStyleSheet("font-size:14px")

        self.btn_clean = QPushButton(self.GrupButton2,text='')#
        self.btn_clean.setGeometry(QRect(185, 5, 80, 30))
        #self.btn_clean.clicked.connect() ##
        #self.btn_clean.setStyleSheet("font-size:14px")
        self.btn_clean.blockSignals(True)
        self.btn_4 = QPushButton(self.GrupButton2,text='Save Figure')#
        self.btn_4.setGeometry(QRect(275, 5, 80, 30))
        self.btn_4.clicked.connect(self.SaveFig) ##
        self.btn_4.setStyleSheet("font-size:14px")
        self.btn_4.setToolTip("Save the graphic as .png")

#------------------- área gráfica PDOS ---------------------------------------
        self.grafico = MplCanvas(self, width=16, height=9, dpi=100)
        self.toolbar1 = NavigationToolbar(self.grafico, self.frame1)
        self.layout1 = QVBoxLayout(self.frame1)
        self.layout1.addWidget(self.toolbar1)
        self.layout1.addWidget(self.grafico)
        self.grafico1 = QWidget(self.frame1)
        self.grafico1.setLayout(self.layout1)
        self.grafico1.setGeometry(0,0, 620, 480)
#------------------- Controle de dados ---------------------------------------
        self.data = {} # Dicionário com os arrays
        self.data_text = {} # Dicionário com os textos ## obsolete
        self.cont = 1 # Variável de controle
        self.chaves = [] # lista com as chaves
        self.orbitais = None
#-----------------------------------------------------------------------------
    def Magnetic(self):
        self.Combo(self.orbitais)
        if self.mono.isChecked() == True:# ativa os orbitais
            self.combo22.clear()
            self.combo22.addItems(["lDOSUP","lDOSDW", "pDOS"])
            self.combo12.clear()
            self.combo12.addItems(["DOSUP","DOSDW"])
        elif self.mono.isChecked() == False:# ativa os orbitais
            self.combo22.clear()
            self.combo22.addItems(["lDOS", "pDOS"])
            self.combo12.clear()
            self.combo12.addItems(["DOS","intDOS"])
##############################################################################
    def Combo(self, parameters):
        if parameters == None:
            if self.line_pdosV.text() == '':
                pass
            else:
                self.orbital.clear()
                self.orbital.addItem("Inative pDOS function!")
        elif parameters == 's':
            if self.mono.isChecked() == False:
                self.orbital.clear()
                self.orbital.addItem("s [column 3]")
            elif self.mono.isChecked() == True:
                self.orbital.clear()
                self.orbital.addItems(["s(up) [column 4]","s(down) [column 5]"])
        elif parameters == 'p':
            if self.mono.isChecked() == False:
                self.orbital.clear()
                self.orbital.addItems(["px [column 3]", "py [column 4]", "pz [column 5]"])
            elif self.mono.isChecked() == True:
                self.orbital.clear()
                self.orbital.addItems(["px(up) [column 4]", "px(down) [column 5]",
                                     "py(up) [column 6]", "py(down) [column 7]",
                                     "pz(up) [column 8]", "pz(down) [column 9]"])
        elif parameters == 'd':
            if self.mono.isChecked() == False:
                self.orbital.clear()
                self.orbital.addItems(["dz2 [column 4]", "dxz [column 5]", "dyz [column 6]",
                                  "dxy [column 7]", "dx2-y2 [column 8]"])
            elif self.mono.isChecked() == True:
                self.orbital.clear()
                self.orbital.addItems(["dz2(up) [column 4]", "dz2(down) [column 5]",
                                  "dxz(up) [column 6]", "dxz(down) [column 7]",
                                 "dyz(up) [column 8]", "dyz(down) [column 9]",
                                 "dxy(up) [column 10]", "dxy(down) [column 11]",
                                 "dx2-y2(up) [column 12]","dx2-y2(down) [column 13]"])
        elif parameters == 'f':
            if self.mono.isChecked() == False:
                self.orbital.clear()
                self.orbital.addItems(["fz3 [column 3]", "fxz2 [column 4]",
                                      "fyz2 [column 5]", "fxyz [column 6]",
                                      "fz [column 7]","fx [column 8]","fy [column 9]"])
            elif self.mono.isChecked() == True:
                self.orbital.clear()
                self.orbital.addItems(["fz3(up) [column 3]", "fz3(down) [column 4]",
                                  "fxz2(up) [column 5]", "fxz2(down) [column 6]",
                                  "fyz2(up) [column 7]", "fyz2(down) [column 8]",
                                  "fxyz(up) [column 9]", "fxyz(down) [column 10]",
                                  "fz(up) [column 11]", "fz(down) [column 12]",
                                  "fx(up) [column 13]", "fx(down) [column 14]",
                                  "fy(up) [column 15]", "fy(down) [column 16]"])
##############################################################################
#------------------------ Funções do D O S -----------------------------------
    def DOS(self):
        X1 = self.combo11.currentText() # serie
        X2 = self.combo12.currentText() # tipo de dados
        if self.line_dosV.text() != '': #
            self.main_widget.progress = QProgressBar(self.frame1)
            self.main_widget.progress.show()
            self.main_widget.progress.setStyleSheet("font-size:10px")
            self.main_widget.progress.setGeometry(10, 460, 500, 10)
            self.main_widget.progress.setMaximum(100)
            self.main_widget.progress.setValue(59)
            dados = modulo3.Resp(self.line_dosV.text(),X1,X2,None)
            eV, pdos = dados[0] + float(self.EFermi.text()), dados[1]
            key = self.line_label.text()+'_'+X2+'_'+str(self.cont) # nome da série.
            self.chaves.insert(0, key)
            self.s_data.clear()
            self.s_data.addItems(self.chaves) # adiciona nome no combobox
            self.Grafico(eV, pdos) # plota o gráfico
            self.data[key] = [eV, pdos] # add in dict data array
            self.cont += 1 #atualiza o contador
        else:
            self.messageBox.about(self,"Error", 'Insert the dos.x outfile!')
    def ReadDOS(self):
        file_dosV, _ = QFileDialog.getOpenFileNames(None, path, "", "*.*")
        if file_dosV:
            f = []
            for filename in file_dosV:
                f.append(filename+';')
            texto = ''.join(map(str,f))
            if len(f) > 1:
                self.line_dosV.setText(texto)
            else:
                self.line_dosV.setText(f[0])
#---------------------- Funções do p D O S -----------------------------------
    def pDOS(self):
        try:
            if self.combo22.currentText() == 'pDOS':
                Y1 = self.combo21.currentText()
                Y2 = 'pDOS'
                Y3 = self.orbital.currentText()
            else:
                Y1 = self.combo21.currentText() # série
                Y2 = self.combo22.currentText() # tipo de dado
                Y3 = None
            if self.line_pdosV.text() != '':
                self.main_widget.progress = QProgressBar(self.frame1)
                self.main_widget.progress.show()
                self.main_widget.progress.setStyleSheet("font-size:10px")
                self.main_widget.progress.setGeometry(10, 460, 500, 10)
                self.main_widget.progress.setMaximum(100)
                self.main_widget.progress.setValue(53)
                #---------- leitura dos dados --------------------------------
                dados = modulo3.Resp(self.line_pdosV.text(),Y1,Y2,Y3)
                eV, pdos = dados[0] + float(self.EFermi.text()), dados[1]
                #self.texto.setText(str(np.transpose([eV,pdos]))) # insere dados na área de texto
                key = self.line_label.text()+'_'+Y2+'_'+str(self.cont) # nome da série.
                self.chaves.insert(0, key)
                self.s_data.clear()
                self.s_data.addItems(self.chaves) # adiciona nome no combobox
                self.Grafico(eV, pdos) # plota o gráfico
                self.data[key] = [eV, pdos] # add in dict data array
                #self.data_text[key] = dados[0] # add in dict text
                self.cont += 1 #atualiza o contador
            else:
                self.messageBox.about(self,"Error", 'Insert the projwfc.x outfile!')
        except:
            self.messageBox.about(self, "Error!", "data incompatible with pdos")
            self.main_widget.progress.close()
#------------------------------------------------------------------------------
    def ReadPDOS(self):
        #---------------------------------------------------------------------
        def Orbital(file):
            var = file.split(';')
            var.pop()
            orbitais = []
            materiais = []
            for i in var:
                materiais.append(i.split('/').pop())
            for j in materiais:
                orbitais.append(j.split('(').pop()[0])
            materiais.clear()
            for k in orbitais:
                if k not in materiais:
                    materiais.append(k)
            if len(materiais)>1:
                return None
            elif len(materiais) == 1:
                return materiais[0]
        #---------------------------------------------------------------------
        file_pdosV, _ = QFileDialog.getOpenFileNames(None, path, "", "*.*")
        if file_pdosV:
            f = []
            for filename in file_pdosV:
                f.append(filename+';')
            texto = ''.join(map(str,f))
            self.line_pdosV.setText(texto)#f[0])
            self.orbitais = Orbital(self.line_pdosV.text())
            self.Combo(self.orbitais) ##############
#--------------------------- B U T T O N S  2 ---------------------------------
    def Clean(self):
        self.line_pdosV.clear()
        self.line_dosV.clear()
        self.orbitais = None
        self.orbital.clear()
    def Salvar(self):
        self.fileName2, _ = QFileDialog.getSaveFileName(None, path, ".csv","CSV files (*.csv);;",)
        try:
            x = self.data[self.s_data.currentText()][0]
            y = self.data[self.s_data.currentText()][1]
            np.savetxt(self.fileName2, np.transpose([x,y]), delimiter=',', fmt='%3.5E')
        except: pass

###############################################################################
    def Grafico(self, a, b):
        self.Progress()########################
        self.grafico.axes.plot(a, b, '-', linewidth=1.0)
        self.grafico.fig.canvas.draw() ## """Atualiza o gráfico"""
    def SaveFig(self):
        path = QFileDialog.getSaveFileName(self, 'Save as', '.png', '*.png')
        if path != ('', ''):
            self.grafico.fig.savefig(path[0],dpi=400, grid=False)
    def Remove(self):
        if self.s_data.currentText() in self.data:
            self.data.pop(self.s_data.currentText()) # remove data of dict
            #self.data_text.pop(self.s_data.currentText()) # remove data of dict
            self.s_data.removeItem(self.s_data.currentIndex())
            self.grafico.axes.clear()
            self.line_pdosV.clear()
            self.line_dosV.clear()
            self.grafico.axes.axhline(y=0, linestyle='--', color='k')
            self.grafico.axes.axvline(x=0, linestyle='--', color='k')
            for i in self.data:
                x, y = self.data[i][0], self.data[i][1]
                self.grafico.axes.plot(x, y, linewidth=1.0)
                self.grafico.axes.xaxis.set_minor_locator(AutoMinorLocator(5))
                self.grafico.axes.yaxis.set_minor_locator(AutoMinorLocator(5))
                self.grafico.fig.canvas.draw()
            try:
                pass
            except:
                self.data_text.clear()
                self.chaves.clear()
                self.cont = 1
        else:
            self.messageBox.about(self, 'Info', 'No data to remove')
        if len(self.data) == 0:
            self.Erase()
    def Progress(self):
        TIME_LIMIT = 100
        count = 62
        while count < TIME_LIMIT:
            count += 1
            time.sleep(0.001)
            self.main_widget.progress.setValue(count)
        self.main_widget.progress.close()
#######################  funções barra de menu   ##############################
    def FecharDef(self):
        self.close()
    def SobreDef(self):
        self.messageBox.about(self, 'About', '''
        Program written to analyze electronic density of states
        obtained from the dos.x and projwfc.x programs\n\n
        author: Márcio F. Santos
        email: marciofs600@gmail.com''')
    def AjudaDef(self):
        self.messageBox.about(self, 'Help', """
# USAGE NOTES:
This algorithm handles output data from the dos.x and projwfc.x
programs available in the Quantum-ESPRESSO v. 6x. The total
electronic state density (DOS(E)) must be handled in the DOS field.
While the projected electronic state density (pDOS(E))
must be evaluated in the field (PDOS).
Caution: inverting the data can lead to spurious results.

If you want to study the pDOS of each orbital independently,
activate the "Enable for independent orbital analysis" selector
and choose which orbital (s, p, d or f) and its variants.
ATTENTION: The insertion of this data must be done with great
care so as not to generate wrong results.

If the calculations were performed with spin polarization
(nspin = 2), select the "Select if calculated with polarized spin" button
.""")
##############################################################################
if __name__ == '__main__':
    App = QApplication(sys.argv)
    gui = Window()
    gui.show()
    App.exec_()
