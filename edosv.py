#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 23:57:47 2021

@author: marcio
"""
cor = ['#000000','#FF0000', '#00FF00','#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#006400', "#000080", '#FF8C00', '#FF4500',	'#9400D3']
import sys
#PyQt5
import time
from PyQt5.QtWidgets import (QFileDialog, QMainWindow, QMessageBox, QPushButton,
                             QLabel, QApplication, QRadioButton, QFrame, QWidget,
                             QLineEdit,QTextEdit, QComboBox, QVBoxLayout, QProgressBar)
from PyQt5.QtCore import  QRect# pyqtSlot
from PyQt5.QtGui import QIcon, QColor
# matplotlib
import matplotlib as mpl
from cycler import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color=cor)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
import os # interage com o sistema operacional
import modulo3 ## módulo das funções DOS E pDOS
##------------------ cores da interface --------------------------------------
background = "background:#555555" # Interface
cor_area_texto = 'background:#606060' # Área de texto
cor_texto = 'white' # Cor do texto na caixa de textos
line_edit = 'background:#707070' # Linha de inserção de dados
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
        super(MplCanvas, self).__init__(self.fig)
class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('DOSView')
        self.setFixedSize(1200, 680)
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
        self.main_widget.setGeometry(475,30,720,650)
        self.frame1 = QFrame(self)
        self.frame1.setGeometry(475,0, 720, 680)
        self.frame1.setStyleSheet(background)
#----------------------- grupo 1 ----------------------------------------
        self.GrupDOS = QFrame(self)
        self.GrupDOS.setGeometry(10,55,460,130)
        self.GrupDOS.setStyleSheet("background:#606060")
#-----------------------------------------------------------------------------
        self.Titulo3 = QLabel(self.GrupDOS,text='DOS')
        self.Titulo3.setGeometry(10, 0, 100, 30)
        self.Titulo3.setStyleSheet("color:blue;font-size:18px")
        self.line_dosV = QLineEdit(self.GrupDOS)
        self.line_dosV.setGeometry(5, 40, 405, 30)
        self.line_dosV.setStyleSheet(line_edit)
        self.search13 = QPushButton(self.GrupDOS)
        self.search13.setIcon(QIcon(path+"/temps/lupa.png"))
        self.search13.setGeometry(QRect(415, 40, 40, 30))
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
        self.combo12.setGeometry(110, 80, 240, 30)
        self.combo12.setStyleSheet("font-size:14px")
        self.combo12.addItems(["DOS","intDOS"])
        self.Calculete13 = QPushButton(self.GrupDOS, text='Calcule')
        self.Calculete13.setGeometry(QRect(355, 80, 100, 30))
        self.Calculete13.setToolTip("to calculete")
        self.Calculete13.clicked.connect(self.DOS)
#---------------------------- grupo 2 ----------------------------------------
        self.GrupPDOS = QFrame(self)
        self.GrupPDOS.setGeometry(10,200,460,160)
        self.GrupPDOS.setStyleSheet("background:#606060")
#-----------------------------------------------------------------------------
        self.Titulo4 = QLabel(self.GrupPDOS,text='pDOS')
        self.Titulo4.setGeometry(10, 0, 100, 30)
        self.Titulo4.setStyleSheet("color:blue;font-size:18px")
        self.line_pdosV = QLineEdit(self.GrupPDOS)
        self.line_pdosV.setGeometry(5, 35, 405, 30)
        self.line_pdosV.setStyleSheet(line_edit)
        self.search23 = QPushButton(self.GrupPDOS)
        self.search23.setIcon(QIcon(path+"/temps/lupa.png"))
        self.search23.setGeometry(QRect(415, 35, 40, 30))
        self.search23.clicked.connect(self.ReadPDOS)       ## click connect
        self.search23.setToolTip("Search")
        self.series1 = QLabel(self.GrupPDOS,text='Série')
        self.series1.setGeometry(10, 75, 50, 30)
        self.series1.setStyleSheet("font-size:14px")
        self.combo21 = QComboBox(self.GrupPDOS)
        self.combo21.setGeometry(50, 75, 55, 30)
        self.combo21.setStyleSheet("font-size:14px")
        self.combo21.addItems(["+","-"])
        self.combo22 = QComboBox(self.GrupPDOS)
        self.combo22.setGeometry(110, 75, 240, 30)
        self.combo22.addItems(["lDOS", "pDOS"])
        self.combo22.setStyleSheet("font-size:14px")
#-----------------------------------------------------------------------------
        self.label = QLabel(self.GrupPDOS,text='Orbitals')
        self.label.setGeometry(10, 110, 100, 30)
        self.label.setStyleSheet("font-size:14px")
        self.orbital = QComboBox(self.GrupPDOS)
        self.orbital.setGeometry(110, 110, 240, 30)
        self.orbital.setStyleSheet("font-size:14px")
        self.Calculete23 = QPushButton(self.GrupPDOS, text='Calcule')
        self.Calculete23.setGeometry(QRect(355, 110, 100, 30))
        self.Calculete23.setToolTip("to calculete")
        self.Calculete23.clicked.connect(self.pDOS)

        self.mono = QRadioButton(self, text='Magnetic \t (Select if calculated with polarized spin)')
        self.mono.setStyleSheet("background:#606060;font-size:14px")
        self.mono.setGeometry(10, 375, 460, 30)
        self.mono.toggled.connect(self.Magnetic)
        self.mono.toggled.connect(self.Combo)
#----------------------- grupo 3 ----------------------------------------
        self.frame3 = QFrame(self)
        self.frame3.setGeometry(10,420,460,100)
        self.frame3.setStyleSheet("background:#606060")
        self.Fig_edit = QLabel(self.frame3,text='Label for data')
        self.Fig_edit.setStyleSheet("font-size:14px")
        self.Fig_edit.setGeometry(10, 10, 90, 30)
        self.line_label = QLineEdit(self.frame3)
        self.line_label.setGeometry(110, 10, 235, 30)
        self.line_label.setStyleSheet(line_edit)
        self.line_label.setText('Label')
        self.btn_remove = QPushButton(self.frame3,text='Remove data')#
        self.btn_remove.setGeometry(QRect(245, 50, 100, 30))
        self.btn_remove.clicked.connect(self.Remove) ##
        self.btn_remove.setStyleSheet("font-size:14px")
        self.btn_remove.setToolTip("Remove the current data")
        self.separator = QFrame(self.frame3)
        self.separator.setGeometry(350,10,110,80)
        self.separator.setStyleSheet("background:#608060")
        self.btn_clean = QPushButton(self.frame3,text='Erase Figure')#
        self.btn_clean.setGeometry(QRect(355, 15, 100, 30))
        self.btn_clean.clicked.connect(self.Erase) ##
        self.btn_clean.setStyleSheet("font-size:14px")
        self.btn_clean.setToolTip("Clear the graphics area")
        self.btn_4 = QPushButton(self.frame3,text='Save Figure')#
        self.btn_4.setGeometry(QRect(355, 50, 100, 30))
        self.btn_4.clicked.connect(self.SaveFig) ##
        self.btn_4.setStyleSheet("font-size:14px")
        self.btn_4.setToolTip("Save the graphic as .png")
        self.s_data = QComboBox(self.frame3)
        self.s_data.setGeometry(10,50,230,30)
        self.s_data.setStyleSheet("font-size:14px")
        self.s_data.setToolTip("list with data series")
#-------------------------botões 2 ---------------------------------------------
        self.GrupButton2 = QFrame(self)
        self.GrupButton2.setGeometry(10,530,460,80)
        self.GrupButton2.setStyleSheet("background:#606060")
        self.btn_5 = QPushButton(self.GrupButton2,text='Clean')# botão salvar
        self.btn_5.setGeometry(QRect(15, 40, 100, 30))
        self.btn_5.clicked.connect(self.Clean) ## conecta a função salvar
        self.btn_5.setStyleSheet("font-size:14px")
        self.btn_6 = QPushButton(self.GrupButton2,text='Save')# botão salvar
        self.btn_6.setGeometry(QRect(120, 40, 100, 30))
        self.btn_6.clicked.connect(self.Salvar) ## conecta a função salvar
        self.btn_6.setStyleSheet("font-size:14px")
        self.btn_7 = QPushButton(self.GrupButton2,text='Edit')#
        self.btn_7.setGeometry(QRect(225, 40, 100, 30))
        self.btn_7.clicked.connect(self.Editar)
        self.btn_7.setStyleSheet("font-size:14px")
        self.btn_8 = QPushButton(self.GrupButton2,text='Copy')#
        self.btn_8.setGeometry(QRect(330, 40, 100, 30))
        self.btn_8.clicked.connect(self.Copiar) ##
        self.btn_8.setStyleSheet("font-size:14px")
#------------------- área de texto  -------------------------------------------
        self.texto = QTextEdit(self.frame1)
        self.texto.setGeometry(7,480,708,200)
        self.texto.setTextColor(QColor(cor_texto))
        self.texto.setStyleSheet(cor_area_texto)
        self.texto.setReadOnly(True)
#------------------- área gráfica PDOS ---------------------------------------
        self.grafico = MplCanvas(self, width=16, height=9, dpi=100)
        self.toolbar1 = NavigationToolbar(self.grafico, self.frame1)
        self.layout1 = QVBoxLayout(self.frame1)
        self.layout1.addWidget(self.toolbar1)
        self.layout1.addWidget(self.grafico)
        self.grafico1 = QWidget(self.frame1)
        self.grafico1.setLayout(self.layout1)
        self.grafico1.setGeometry(0,0, 720, 480)
#------------------- Controle de dados ---------------------------------------
        self.data = {}
        self.data_text = {}
        self.cont = 1
        self.chaves = []
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
                self.combo22.clear()
                self.combo22.addItems(["lDOS"])
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
            self.main_widget.progress.setGeometry(10, 460, 700, 10)
            self.main_widget.progress.setMaximum(100)
            self.main_widget.progress.setValue(59)
            dados = modulo3.Resp(self.line_dosV.text(),X1,X2,None)
            self.texto.setText(str(dados[0]))
            key = self.line_label.text()+'_'+X2+'_'+str(self.cont) # nome da série.
            self.chaves.insert(0, key)
            self.s_data.clear()
            self.s_data.addItems(self.chaves) # adiciona nome no combobox
            self.Grafico(dados[1],dados[2]) # plota o gráfico
            self.data[key] = [dados[1],dados[2]] # add in dict np.array
            self.data_text[key] = dados[0] # add in dict text
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
            if self.combo21.currentText() == 'pDOS':
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
                self.main_widget.progress.setGeometry(10, 460, 700, 10)
                self.main_widget.progress.setMaximum(100)
                self.main_widget.progress.setValue(53)
                dados = modulo3.Resp(self.line_pdosV.text(),Y1,Y2,Y3)
                self.texto.setText(dados[0]) # insere dados na área de texto
                key = self.line_label.text()+'_'+Y2+'_'+str(self.cont) # nome da série.
                self.chaves.insert(0, key)
                self.s_data.clear()
                self.s_data.addItems(self.chaves) # adiciona nome no combobox
                self.Grafico(dados[1],dados[2]) # plota o gráfico
                self.data[key] = [dados[1],dados[2]] # add in dict data array
                self.data_text[key] = dados[0] # add in dict text
                self.cont += 1 #atualiza o contador
            else:
                self.messageBox.about(self,"Error", 'Insert the projwfc.x outfile!')
        except:
            self.messageBox.about(self, "Error!", "data incompatible with pdos")
            self.main_widget.progress.close()
    def ReadPDOS(self):
#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
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
        self.texto.clear()
        self.line_pdosV.clear()
        self.line_dosV.clear()
        self.orbitais = None
        self.orbital.clear()
    def Salvar(self):
        self.fileName2, _ = QFileDialog.getSaveFileName(None, path, ".dat","Dat files (*.dat);; txt files (*.txt)",)
        try:
            with open (self.fileName2, 'w') as saida:
                saida.write(self.texto.toPlainText())
        except: pass
    def Editar(self):
        self.texto.setReadOnly(False)
    def Copiar(self):
        if self.texto.toPlainText() != '':
            cb = QApplication.clipboard()
            cb.setText(self.texto2.toPlainText())
            self.messageBox.about(self,'Info', 'Text copied to clipboard')
        else:
            self.messageBox.about(self,'Erro', 'There is no text to copy')
###############################################################################
    def Grafico(self, a, b):
        #print('fui chamado')
        self.Progress()########################
        self.grafico.axes.plot(a, b, linewidth=1.0)
        self.grafico.fig.canvas.draw() ## """Atualiza o gráfico"""
    def Erase(self):
        self.grafico.axes.clear()
        self.grafico.axes.xaxis.set_minor_locator(AutoMinorLocator(5))
        self.grafico.axes.yaxis.set_minor_locator(AutoMinorLocator(5))
        self.grafico.fig.canvas.draw()
    def SaveFig(self):
        path = QFileDialog.getSaveFileName(self, 'Save as', '.png', '*.png')
        if path != ('', ''):
            self.grafico.fig.savefig(path[0],dpi=300, grid=False)
    def Remove(self):
        if self.s_data.currentText() in self.data:
            self.data.pop(self.s_data.currentText()) # remove data of dict
            self.data_text.pop(self.s_data.currentText()) # remove data of dict
            self.s_data.removeItem(self.s_data.currentIndex())
            self.grafico.axes.clear()
            self.line_pdosV.clear()
            self.line_dosV.clear()
            for i in self.data:
                x, y = self.data[i][0], self.data[i][1]
                current = i
                self.grafico.axes.plot(x, y, linewidth=1.0)
                self.grafico.axes.xaxis.set_minor_locator(AutoMinorLocator(5))
                self.grafico.axes.yaxis.set_minor_locator(AutoMinorLocator(5))
                self.grafico.fig.canvas.draw()
            try:
                self.texto.setText(self.data_text[current])
            except:
                self.texto.clear()
                self.data_text.clear()
                self.chaves.clear()
                self.cont = 1
        else:
            self.messageBox.about(self, 'Info', 'No data to remove')
        if len(self.data) == 0:
            self.Erase()
            self.texto.clear()
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
