import codecs
import sys
import subprocess
import time
import datetime
import math
import binascii
import os
import shutil
import random
import zipfile
import traceback
import locale
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    global version
    def __init__(self):
        version = "2.0"
        QtGui.QMainWindow.__init__(self)
        self.setWindowFlags(QtCore.Qt.Dialog);
        self.setWindowTitle('Gameplayzer')
        widget = QtGui.QWidget(self)
        grid = QtGui.QGridLayout(widget)
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(15)
        ##CSS Style
        css = """
        QWidget
        {
        Background:rgba(0,0,0,100%);
        background-image: url(configgm16/backgr.jpg);
        background-size: 100% 100%;
        color:white;
        font:12px bold;
        font-weight:bold;
        border-radius: 1px;
        height: 11px;
        }
        QPushButton{
        Background:rgba(255,255,255,35%);
        color:black;
        font-size:11px;
        border:1px solid black;
        width:100px;
        height:30px;
        }
        QPushButton:hover{
        Background:rgba(255,255,255,80%);
        color:black;
        font-size:11px;
        border:1px solid black;
        width:100px;
        height:30px;
        }
        QPushButton[disabled=disabled], QPushButton:disabled {
        Background:rgba(255,255,255,15%);
        color:grey;
        }
        QTextEdit{
        background: rgba(255,255,255,70%);
        color:black;
        font-size:8px;
        border: 1px solid black;
        }
        QLabel{
        background: rgba(0,0,0,0%);
        }
        QProgressBar{
        color:grey;
        border:1px solid white;
        text-align:center;
        padding:5px;
        }
"""
        self.setStyleSheet(css);
        ##WIDGET CREATION
        self.lblGameplayzer = QtGui.QLabel('Gameplayzer for FIFA 16 FULL by Fifaccitiu v:'+version,widget)
        self.btnOpen = QtGui.QPushButton("Open database", widget)
        self.btnOpen.setEnabled(False)
        self.btnOpen.setToolTip("Open a FIFA 16 Database to gameplayze it!")
        self.btnSave = QtGui.QPushButton("Save Database", widget)
        self.btnSave.setEnabled(False)
        self.btnSave.setToolTip("Save the gameplayzed database")
        self.btnOpenMatrix = QtGui.QPushButton("Open matrix file", widget)
        self.btnOpenMatrix.setToolTip("Open a matrix CSV file that contain the attributes matrix for every playing style")
        self.lblLogWindow = QtGui.QLabel('Log Window:',widget)
        self.matrixfilename = "";
        self.inputdbfilename = "";
        self.outputdbfilename ="";
        self.useoldph = False;
        self.connect(self.btnOpen, QtCore.SIGNAL('clicked()'), self.openDB)
        self.connect(self.btnSave, QtCore.SIGNAL('clicked()'), self.saveDB)
        self.connect(self.btnOpenMatrix, QtCore.SIGNAL('clicked()'), self.openmatrix)
        self.textEdit = QtGui.QTextEdit(widget)
        self.textEdit.setReadOnly(True)
        self.lblLogError = QtGui.QLabel('Log Error:',widget)
        self.textEdit2 = QtGui.QTextEdit(widget)
        self.textEdit2.setReadOnly(True)
        self.progressBar = QtGui.QProgressBar(widget)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)
        ##AGGIUNTA WIDGET##
        grid.addWidget(self.lblGameplayzer,0,0,1,6)
        grid.addWidget(self.btnOpenMatrix,1,0)
        grid.addWidget(self.btnOpen, 1, 1)
        grid.addWidget(self.btnSave, 1, 2)
        grid.addWidget(self.lblLogWindow,2,0)
        grid.addWidget(self.textEdit, 3, 0,7,4)
        grid.addWidget(self.lblLogError,2,4)
        grid.addWidget(self.textEdit2, 3, 4,7,4)
        grid.addWidget(self.progressBar,1,4)
        self.setLayout(grid)
        self.setCentralWidget(widget)
        self.setGeometry(300,300,700,450);
        self.show();

    def openmatrix(self):
        fName = QtGui.QFileDialog.getOpenFileName(self, "Open matrix", "", self.tr("FIFA DB Files (*csv)"))            
        if fName.isEmpty() == False:
              self.btnOpen.setEnabled(True)
              self.matrixfilename = fName
              self.textEdit.append("Matrix Filename: "+self.matrixfilename)
    def openDB(self):
        fName = QtGui.QFileDialog.getOpenFileName(self, "Open database", "", self.tr("FIFA DB Files (*db)"))            
        if fName.isEmpty() == False:
              self.btnSave.setEnabled(True)
              self.inputdbfilename = fName
              self.textEdit.append("DB Filename: "+self.inputdbfilename)
    def saveDB(self):
        fName = QtGui.QFileDialog.getSaveFileName(self, "GAMEPLAYZE!", "", self.tr("FIFA DB Files (*db)"))            
        if fName.isEmpty() == False:
              self.btnSave.setEnabled(True)
              self.outputdbfilename = fName #QtCore.QFileInfo(fName).fileName()
              print(str(self.outputdbfilename))
              self.textEdit.append("DB Gameplayzed: "+self.outputdbfilename)
              self.textEdit.append("Applying GAMEPLAY, please wait 2-3 minutes...")
        self.mains(self.matrixfilename,self.inputdbfilename,self.outputdbfilename)


    def mains(self,matrixfilename,inputdbfilename,outputdbfilename):
        try:
            locale.setlocale(locale.LC_NUMERIC,''); #EVITO I PROBLEMI CON LE VIRGOLE COME SEPARATORI
            shutil.copyfile(str(inputdbfilename),str(outputdbfilename)); #COPIO L INPUT COME BASE PER L OUTPUT
            p=subprocess.Popen(('configgm16\\DBEI.exe','-e','configgm16\\tempdb',str(inputdbfilename),'configgm16\\fifa_ng_db-meta.xml')); #CONVERTO IL DB CON TXT
            QtGui.QApplication.processEvents();
            p.wait();
            QtGui.QApplication.processEvents();
            self.progressBar.setValue(30);
            QtGui.QApplication.processEvents();
            #CHECK IF GAMEPLAYZED
            self.textEdit.append(str(self.useoldph));
            self.textEdit.append("EXPORT FROM FIFA DB... done!");
            #SISTEMO I GIOVANI E I NEWGENS
            #shutil.copyfile('configgm\\regenv2.uni','configgm\\tempdb\\career_regenplayerattributes.txt');
            #shutil.copyfile('configgm\\youthv2.uni','configgm\\tempdb\\career_youthplayerattributes.txt');
            #self.textEdit.append('YOUTH AND REGENS RECALIBRATION.... done!');
            #SISTEMO LE SLIDER
            #shutil.copyfile('configgm\\sliderv2.uni','configgm\\tempdb\\fifaGameSettings.txt');
            #self.textEdit.append('SLIDER SETTING....done!');
            #METTO I NUOVI LIMITI DI POS PER RUOLO
            shutil.copyfile('configgm16\\fieldv214.uni','configgm16\\tempdb\\playerpositionzones.txt');
            shutil.copyfile('configgm16\\fieldv214.uni','configgm16\\tempdb\\fieldpositionboundingboxes.txt');
            self.textEdit.append('NEW POSITION SETTINGS...done!');
            #SISTEMO PER EVITARE IL DISCORSO VIRGOLE
            frmt = self.Aprifile('configgm16\\tempdb\\playerpositionzones.txt');
            primarigafrmt = self.Columnname(frmt);
            matrixfrmt = self.Rimuovitabs(frmt);
            self.applylocalization(matrixfrmt,"field");
            self.Salva('configgm16\\tempdb\\playerpositionzones.txt',primarigafrmt,matrixfrmt);
            self.Salva('configgm16\\tempdb\\fieldpositionboundingboxes.txt',primarigafrmt,matrixfrmt);
            #APRO LA MATRICE
            psmatrix = self.Aprifile(str(matrixfilename));
            StMxB = self.Rimuovitabs(psmatrix);
            self.textEdit.append('LOADED PERSONALIZED MATRIX');
            QtGui.QApplication.processEvents();
            self.progressBar.setValue(40);
            giocatori = self.Aprifile('configgm16\\tempdb\\players.txt');
            primariga = self.Columnname(giocatori);
            matrixgiocatori = self.Rimuovitabs(giocatori);
            #PRENDO GLI STILI PERSONALIZZATI (da ritoccare il modo tale da evitare il casino)
            playst = self.Aprifile('configgm16\\playstv2-v.csv');
            primarigaps = self.Columnname(playst);
            matrixplays = self.Rimuovitabsps(playst);
            colps=self.GetPS(StMxB,matrixgiocatori);
            self.progressBar.setValue(43);
            listaid = self.IdExtraction(matrixgiocatori,83);
            colpsnew = self.NewPs(matrixplays,colps,matrixgiocatori);
            self.Gameplayization(StMxB,matrixgiocatori,colpsnew);
            QtGui.QApplication.processEvents();
            self.progressBar.setValue(45);
            self.Salva('configgm16\\tempdb\\players.txt',primariga,matrixgiocatori);
            self.textEdit.append("SAVED PLAYERS TABLE");
            QtGui.QApplication.processEvents();
            self.progressBar.setValue(50);
            squadre = self.Aprifile('configgm16\\tempdb\\teams.txt');
            primarigateams = self.Columnname(squadre);
            matrixsquadre = self.Rimuovitabs(squadre);
            self.SqGameplayization(matrixsquadre);
            self.Salva('configgm16\\tempdb\\teams.txt',primarigateams,matrixsquadre);
            self.textEdit.append("TEAM STYLES ADDED!");
            self.textEdit.append("SAVED TEAMS TABLES");
            QtGui.QApplication.processEvents();
            self.progressBar.setValue(60);
            #arbitri = self.Aprifile('configgm\\tempdb\\referee.txt');
            #shutil.copyfile('configgm\\tempdb\\referee.txt','configgm\\tempdb\\refereesorig.txt');
            #primarigaarbitri = self.Columnname(arbitri);
            #matrixarbitri = self.Rimuovitabs(arbitri);
            #self.RfGameplayization(matrixarbitri);
            #self.Salva('configgm\\tempdb\\referee.txt',primarigaarbitri,matrixarbitri);
            #self.textEdit.append("SAVED REFEREE TABLES");
            ###TEAM SHEETS###
            teamsheets = self.Aprifile('configgm16\\tempdb\\default_teamsheets.txt');
            primarigateamsheets = self.Columnname(teamsheets);
            matrixteamsheets = self.Rimuovitabs(teamsheets);
            self.StGameplayization(matrixteamsheets,colps,listaid,StMxB,matrixsquadre);
            self.Salva('configgm16\\tempdb\\default_teamsheets.txt',primarigateamsheets,matrixteamsheets);
            QtGui.QApplication.processEvents();
            self.progressBar.setValue(63);
            ###DEFAULT TEAMDATA###
            teamdata = self.Aprifile('configgm16\\tempdb\\defaultteamdata.txt');
            primarigateamdata = self.Columnname(teamdata);
            matrixteamdata = self.Rimuovitabs(teamdata);
            self.SdGameplayization(matrixteamdata,matrixteamsheets,colps,listaid,StMxB,matrixsquadre);
            self.Salva('configgm16\\tempdb\\defaultteamdata.txt',primarigateamdata,matrixteamdata);
            QtGui.QApplication.processEvents();
            self.progressBar.setValue(65);
            ###FORMATIONS###
            formations = self.Aprifile('configgm16\\tempdb\\formations.txt');
            primarigaformations = self.Columnname(formations);
            matrixformations = self.Rimuovitabs(formations);
            self.FmGameplayization(matrixformations,matrixteamsheets,colps,listaid,StMxB);
            #self.applylocalization(matrixformations,"formation");#new!
            self.Salva('configgm16\\tempdb\\formations.txt',primarigaformations,matrixformations);
            ###REIMPORTING###
            self.progressBar.setValue(70);
            QtGui.QApplication.processEvents();
            p2=subprocess.Popen(('configgm16\\DBEI.exe','-i','configgm16\\tempdb',str(outputdbfilename),'configgm16\\fifa_ng_db-meta.xml'));
            p2.wait();
            self.textEdit.append("REIMPORT...done!");
            shutil.rmtree('configgm16\\tempdb');
            self.progressBar.setValue(100);
            self.msgbox = QtGui.QMessageBox.about(self, "Completed", "Enjoy the new DB gameplayzed!");
            self.textEdit.append("-- ENJOY MY GAMEPLAY "+version+" --");
        except IndexError:
            formatted_lines = traceback.format_exc().splitlines()
            for i in range(0,len(formatted_lines)):
                self.textEdit2.append(str(formatted_lines[i]));
    contarighe = 0;
    contacolonne = 0;
    playerstotal=0;
    gktotal=0;
    gameplayversion="6.0 Final";
    destversion=" for your patch";
    version=gameplayversion+destversion;

    #Open file
    def Aprifile(self,filei):
        f = codecs.open(filei,'r',encoding='utf-16');
        giocatori = [];
        for line in f:
            line = line.split('\r\n');
            giocatori.append(line[0]);
        return giocatori;

    def Columnname(self,lista):
        primariga = lista.pop(0);
        return primariga;

    def Rimuovitabs(self,lista):
        global contarighe, contacolonne;
        '''tolgo = lista.pop(0);'''
        righe = 1;
        nuovalista=[];
        nlista=[];
        shoetypecode=[];
        for d in lista:
            c = d.split('\t');
            colonne=len(c);
            nlista.append(c);
            righe = righe+1;
        '''stampami la lista righe x colonna'''
        contarighe = righe;
        contacolonne = colonne;
        return nlista;

    def Rimuovitabsps(self,lista):
        global contarigheps, contacolonneps;
        '''tolgo = lista.pop(0);'''
        righe = 1;
        nuovalista=[];
        nlista=[];
        shoetypecode=[];
        for d in lista:
            c = d.split('\t');
            colonne=len(c);
            nlista.append(c);
            righe = righe+1;
        contarigheps = righe;
        contacolonneps = colonne;
        return nlista;

    def Rimuovitabsts(self,lista):
        global contarighets, contacolonnets;
        righe = 1;
        nuovalista=[];
        nlista=[];
        shoetypecode=[];
        for d in lista:
            c = d.split('\t');
            colonne=len(c);
            nlista.append(c);
            righe = righe+1;
        contarighets = righe;
        contacolonnets = colonne;
        return nlista;

    def GetPS(self,StMx,lista): #gli passo le stmx e il players
        WeMx=[[1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
        [1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
        [1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
        [1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9],
        [1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
        [1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
        [1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6],
        [9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [9,9,9,9,9,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]];
        for i in range(1,len(StMx)):
            for j in range(0,len(StMx[0])):
                if(i==31):
                    StMx[i][j] = float(int(StMx[i][j])/100.0);
                else:
                    StMx[i][j] = int(StMx[i][j]);
        #listasta=[44,24,32,31,64,20,83,56,15,45,12,33,100,62,10,22,28,29,7,51,63,38,78,81,42,21,67,52,85,26,89];
        totpl = len(lista);
        totdimenouno = 0;
        listaps = contarighe*[99];
        totalix = 88*[0.0];
        M = 88*[0]; #Count
        S = 88*[0.0]; #Values
        gkvalues=[];
        cbvalues=[];
        sbvalues=[];
        wbvalues=[];
        dmvalues=[];
        cmvalues=[];
        amvalues=[];
        smvalues=[];
        swvalues=[];
        cfvalues=[];
        stvalues=[];
        #Analyze every player comparing their attributes to Playstyle standard attributes, then balance it to have players with different playstyle
        tot=11*[0];
        for rig in range(0,len(lista)):
            #from cf to st
            macroposition = self.GetMacroPosition(int(lista[rig][42]));
            pfoot = int(lista[rig][78]); #foot 1 D 2 S
            ### GK=0,CB=1,SB=2,WB=3,DM=4,CM=5,AM=6,SM=7,WM=8,CF=9,ST=10 ###
            if(int(lista[rig][12])==-1 and int(lista[rig][101])==-1):
                totdimenouno=totdimenouno+1;
            ovr = int(lista[rig][90]);
            intnationalrep = int(lista[rig][54]);
            idplayer = int(lista[rig][83]);
            #posizione nella tabella players degli attributi ordinati in base alla matrice (vedi excel CalcoloOverall)
            #14stat=[44,24,32,31,64,20,83,56,15,45,12,33,100,62,10,22,28,29,7,51,63,38,78,81,42,21,67,52,85,26];
            #15stat=[43,22,30,29,63,18,83,55,13,44,10,31,100,61, 8,20,26,27,5,50,62,36,78,81,40,19,66,50,85,24];
            ##########0  1  2  3  4  5  6  7  8  9 10 11  12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 
            stat   =[43,22,30,29,64,18,84,56,13,44,10,31,102,62, 8,20,26,27, 5,50,63,36,79,82,40,19,67,50,86,24];
            #normalizzare overall 75/70= bco - 10 S[j]=S[j]+int(((int(lista[rig][stat[i-1]])-(StMx[i][j]*10))/ovr));
            norm = ovr/70.0;
            if(macroposition==0):
                k = 0;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis0=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                gkvalues.append(lis0);
                tot[0]=tot[0]+1;
            elif(macroposition==1):
                k = 8;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis1=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                cbvalues.append(lis1);
                tot[1]=tot[1]+1;
            elif(macroposition==2):
                k = 16;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis2=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                sbvalues.append(lis2);
                tot[2]=tot[2]+1;
            elif(macroposition==3):
                k = 24;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis3=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                wbvalues.append(lis3);
                tot[3]=tot[3]+1;
            elif(macroposition==4):
                k = 32;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis4=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                dmvalues.append(lis4);
                tot[4]=tot[4]+1;
            elif(macroposition==5):
                k = 40;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis5=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                cmvalues.append(lis5);
                tot[5]=tot[5]+1;
            elif(macroposition==6):
                k = 48;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis6=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                amvalues.append(lis6);
                tot[6]=tot[6]+1;
            elif(macroposition==7):
                k = 56;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis7=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                smvalues.append(lis7);
                tot[7]=tot[7]+1;
            elif(macroposition==8):
                k = 64;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis8=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                swvalues.append(lis8);
                tot[8]=tot[8]+1;
            elif(macroposition==9):
                k = 72;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis9=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                cfvalues.append(lis9);
                tot[9]=tot[9]+1;
            elif(macroposition==10):
                k = 80;
                for j in range(k,k+8):
                    for i in range(1,31):
                        S[j]=S[j]+int(int(int(lista[rig][stat[i-1]])/norm)-((StMx[i][j]-1)*12));
                lis10=[rig,S[k+0],S[k+1],S[k+2],S[k+3],S[k+4],S[k+5],S[k+6],S[k+7]];
                S[k+0]=S[k+1]=S[k+2]=S[k+3]=S[k+4]=S[k+5]=S[k+6]=S[k+7]=0;
                stvalues.append(lis10);
                tot[10]=tot[10]+1;           
            #Smista gkvalues
        print("i -1 "+str(totdimenouno));
        print("rig "+str(len(lista)));
        if(totdimenouno>=(len(lista)-15)):
            print("Ohi, errore!");
            shutil.rmtree('configgm\\tempdb');
            self.msgbox = QtGui.QMessageBox.about(self, "Error", "This is a Gameplayzed DB, i can't gameplayze it!");
            sys.exit();
        listaps=self.scrematura(gkvalues,listaps,0,StMx[36][0],StMx[36][1],StMx[36][2],StMx[36][3],StMx[36][4],StMx[36][5],StMx[36][6],StMx[36][7]);
        listaps=self.scrematura(cbvalues,listaps,8,StMx[36][8],StMx[36][9],StMx[36][10],StMx[36][11],StMx[36][12],StMx[36][13],StMx[36][14],StMx[36][15]);
        listaps=self.scrematura(sbvalues,listaps,16,StMx[36][16],StMx[36][17],StMx[36][18],StMx[36][19],StMx[36][20],StMx[36][21],StMx[36][22],StMx[36][23]);
        listaps=self.scrematura(wbvalues,listaps,24,StMx[36][24],StMx[36][25],StMx[36][26],StMx[36][27],StMx[36][28],StMx[36][29],StMx[36][30],StMx[36][31]);
        listaps=self.scrematura(dmvalues,listaps,32,StMx[36][32],StMx[36][33],StMx[36][34],StMx[36][35],StMx[36][36],StMx[36][37],StMx[36][38],StMx[36][39]);
        listaps=self.scrematura(cmvalues,listaps,40,StMx[36][40],StMx[36][41],StMx[36][42],StMx[36][43],StMx[36][44],StMx[36][45],StMx[36][46],StMx[36][47]);
        listaps=self.scrematura(amvalues,listaps,48,StMx[36][48],StMx[36][49],StMx[36][50],StMx[36][51],StMx[36][52],StMx[36][53],StMx[36][54],StMx[36][55]);
        listaps=self.scrematura(smvalues,listaps,56,StMx[36][56],StMx[36][57],StMx[36][58],StMx[36][59],StMx[36][60],StMx[36][61],StMx[36][62],StMx[36][63]);
        listaps=self.scrematura(swvalues,listaps,64,StMx[36][64],StMx[36][65],StMx[36][66],StMx[36][67],StMx[36][68],StMx[36][69],StMx[36][70],StMx[36][71]);
        listaps=self.scrematura(cfvalues,listaps,72,StMx[36][72],StMx[36][73],StMx[36][74],StMx[36][75],StMx[36][76],StMx[36][77],StMx[36][78],StMx[36][79]);
        listaps=self.scrematura(stvalues,listaps,80,StMx[36][80],StMx[36][81],StMx[36][82],StMx[36][83],StMx[36][84],StMx[36][85],StMx[36][86],StMx[36][87]);
        for i in range(0,len(listaps)):
            for j in range(0,88):
                if(listaps[i]==j):
                    M[j]=M[j]+1;
            #listaps.append(pls);            
    #STAMPO ANALISI STATISTICA PLAYSTYLE
        global playerstotal,gktotal;
        playerstotal = tot[0]+tot[1]+tot[2]+tot[3]+tot[4]+tot[5]+tot[6]+tot[7]+tot[8]+tot[9]+tot[10];
        gktotal = tot[0];
        self.textEdit.append("                ");
        self.textEdit.append("FIFACCITIU STYLE GAMEPLAY: v: "+version+"");
        self.textEdit.append("TOTAL PLAYERS IN THIS DB: "+str(playerstotal));
        for s in range(0,88):
            t = ((s)/8);
            #self.textEdit.append(StMx[0][s]+" "+str(M[s])+" players,with "+str(M[s]*100/tot[t])+"%");
        print("--------------------------");
        print("listaps "+str(len(listaps)));
        return listaps;
    #Removing International reputation from Overall.
    
    def Remove_ir_from_ovr(self,ovr,ir):
        if(ir == 3):
            if(ovr>49):
                ovr = ovr-1;
            else:
                ovr = ovr-0;
        if(ir == 4):
            if(ovr>65):
                ovr = ovr-2;
            if(ovr>32):
                ovr = ovr-1;
            else:
                ovr = ovr-0;
        if(ir == 5):
            if(ovr>74):
                ovr = ovr-3;
            if(ovr>49):
                ovr = ovr-2;
            if(ovr>24):
                ovr = ovr-1;
            else:
                ovr = ovr-0;
        return ovr;
    #Eliminazione valori minori di 10. Solo attributi tecnici e mentali

    def scrematura(self,c,allv,soprasomma,P1,P2,P3,P4,P5,P6,P7,P8):
        vmin = 1000000;
        vmax = 0;
        pssdef=(contarighe)*[99];
        assa = [0,0];
        pssdefe = len(c)*[assa];
        ps=0;
        for i in range(0,len(c)):
            nvmin = int(min(c[i][1:]));
            nvmax = int(max(c[i][1:]));
            if nvmin<vmin:
                vmin=nvmin;
            if nvmax>vmax:
                vmax=nvmax;
        #print("minimo "+str(vmin)+" massimo "+str(vmax)+ "gruppo " + str(soprasomma) );
        #print(c);
        eev = vmax;
        epsilon = 2;#1
        aa=0;bb=0;cc=0;dd=0;ee=0;ff=0;gg=0;hh=0;
        aamx=int(len(c)*P1/100);
        bbmx=int(len(c)*P2/100);
        ccmx=int(len(c)*P3/100);
        ddmx=int(len(c)*P4/100);
        eemx=int(len(c)*P5/100);
        ffmx=int(len(c)*P6/100);
        ggmx=int(len(c)*P7/100);
        hhmx=int(len(c)*P8/100);
        while(eev>=vmin):
            for i in range(0,len(c)):
                for j in range(1,len(c[0])): 
                    if(c[i][j]>=eev):
                        riga=i;
                        posmx=int(c[i][0]);
                        ####DA sistemare
                        if(j==1):
                            if(aa<=aamx):
                                aa=aa+1;
                                plays=0;
                            elif(bb<=bbmx):
                                bb=bb+1;
                                plays=1;
                            elif(cc<=ccmx):
                                cc=cc+1;
                                plays=2;
                            elif(dd<=ddmx):
                                dd=dd+1;
                                plays=3;
                            elif(ee<=eemx):
                                ee=ee+1;
                                plays=4;
                            elif(ff<=ffmx):
                                ff=ff+1;
                                plays=5;
                            elif(gg<=ggmx):
                                gg=gg+1;
                                plays=6;
                            elif(hh<=hhmx):
                                hh=hh+1;
                                plays=7;
                        if(j==2):
                            if(bb<=bbmx):
                                bb=bb+1;
                                plays=1;
                            elif(cc<=ccmx):
                                cc=cc+1;
                                plays=2;
                            elif(dd<=ddmx):
                                dd=dd+1;
                                plays=3;
                            elif(ee<=eemx):
                                ee=ee+1;
                                plays=4;
                            elif(ff<=ffmx):
                                ff=ff+1;
                                plays=5;
                            elif(gg<=ggmx):
                                gg=gg+1;
                                plays=6;
                            elif(hh<=hhmx):
                                hh=hh+1;
                                plays=7;
                            elif(aa<=aamx):
                                aa=aa+1;
                                plays=0;
                        if(j==3):
                            if(cc<=ccmx):
                                cc=cc+1;
                                plays=2;
                            elif(dd<=ddmx):
                                dd=dd+1;
                                plays=3;
                            elif(ee<=eemx):
                                ee=ee+1;
                                plays=4;
                            elif(ff<=ffmx):
                                ff=ff+1;
                                plays=5;
                            elif(gg<=ggmx):
                                gg=gg+1;
                                plays=6;
                            elif(hh<=hhmx):
                                hh=hh+1;
                                plays=7;
                            elif(aa<=aamx):
                                aa=aa+1;
                                plays=0;
                            elif(bb<=bbmx):
                                bb=bb+1;
                                plays=1;
                        if(j==4):
                            if(dd<=ddmx):
                                dd=dd+1;
                                plays=3;
                            elif(ee<=eemx):
                                ee=ee+1;
                                plays=4;
                            elif(ff<=ffmx):
                                ff=ff+1;
                                plays=5;
                            elif(gg<=ggmx):
                                gg=gg+1;
                                plays=6;
                            elif(hh<=hhmx):
                                hh=hh+1;
                                plays=7;
                            elif(aa<=aamx):
                                aa=aa+1;
                                plays=0;
                            elif(bb<=bbmx):
                                bb=bb+1;
                                plays=1;
                            elif(cc<=ccmx):
                                cc=cc+1;
                                plays=2;
                        if(j==5):
                            if(ee<=eemx):
                                ee=ee+1;
                                plays=4;
                            elif(ff<=ffmx):
                                ff=ff+1;
                                plays=5;
                            elif(gg<=ggmx):
                                gg=gg+1;
                                plays=6;
                            elif(hh<=hhmx):
                                hh=hh+1;
                                plays=7;
                            elif(aa<=aamx):
                                aa=aa+1;
                                plays=0;
                            elif(bb<=bbmx):
                                bb=bb+1;
                                plays=1;
                            elif(cc<=ccmx):
                                cc=cc+1;
                                plays=2;
                            elif(dd<=ddmx):
                                dd=dd+1;
                                plays=3;
                        if(j==6):
                            if(ff<=ffmx):
                                ff=ff+1;
                                plays=5;
                            elif(gg<=ggmx):
                                gg=gg+1;
                                plays=6;
                            elif(hh<=hhmx):
                                hh=hh+1;
                                plays=7;
                            elif(aa<=aamx):
                                aa=aa+1;
                                plays=0;
                            elif(bb<=bbmx):
                                bb=bb+1;
                                plays=1;
                            elif(cc<=ccmx):
                                cc=cc+1;
                                plays=2;
                            elif(dd<=ddmx):
                                dd=dd+1;
                                plays=3;
                            elif(ee<=eemx):
                                ee=ee+1;
                                plays=4;
                        if(j==7):
                            if(gg<=ggmx):
                                gg=gg+1;
                                plays=6;
                            elif(hh<=hhmx):
                                hh=hh+1;
                                plays=7;
                            elif(aa<=aamx):
                                aa=aa+1;
                                plays=0;
                            elif(bb<=bbmx):
                                bb=bb+1;
                                plays=1;
                            elif(cc<=ccmx):
                                cc=cc+1;
                                plays=2;
                            elif(dd<=ddmx):
                                dd=dd+1;
                                plays=3;
                            elif(ee<=eemx):
                                ee=ee+1;
                                plays=4;
                            elif(ff<=ffmx):
                                ff=ff+1;
                                plays=5;
                        if(j==8):
                            if(hh<=hhmx):
                                hh=hh+1;
                                plays=7;
                            elif(aa<=aamx):
                                aa=aa+1;
                                plays=0;
                            elif(bb<=bbmx):
                                bb=bb+1;
                                plays=1;
                            elif(cc<=ccmx):
                                cc=cc+1;
                                plays=2;
                            elif(dd<=ddmx):
                                dd=dd+1;
                                plays=3;
                            elif(ee<=eemx):
                                ee=ee+1;
                                plays=4;
                            elif(ff<=ffmx):
                                ff=ff+1;
                                plays=5;
                            elif(gg<=ggmx):
                                gg=gg+1;
                                plays=6;
                        defplays = plays+soprasomma;
                        allv[posmx]=defplays;
                            #print(eev,c[i][j],i,plays);
                        c[i][1]=0;
                        c[i][2]=0;
                        c[i][3]=0;
                        c[i][4]=0;
                        c[i][5]=0;
                        c[i][6]=0;
                        c[i][7]=0;
                        c[i][8]=0;
            eev=eev-epsilon;
        print(aamx,bbmx,ccmx,ddmx,eemx,ffmx,ggmx,hhmx,aa+bb+cc+dd+ee+ff+gg+hh,aa,bb,cc,dd,ee,ff,gg,hh);
        return allv;
    
    def IdExtraction(self,lista,pos):
        listaid= [];
        for rig in range(0,len(lista)):
            listaid.append(int(lista[rig][pos]));
        return listaid;

    def NewPs(self,listapsmia,listacalc,listagioc):
        for rigps in range(0,len(listapsmia)):
            playid = int(listapsmia[rigps][0]);
            nome = unicode(listapsmia[rigps][1]);
            psty = int(listapsmia[rigps][2]);
            pots = int(listapsmia[rigps][3]);
            roll = int(listapsmia[rigps][4]);
            onoff = int(listapsmia[rigps][5]);
            bco = int(listapsmia[rigps][6]);
            cro = int(listapsmia[rigps][7]);
            dri = int(listapsmia[rigps][8]);
            fin = int(listapsmia[rigps][9]);
            hea = int(listapsmia[rigps][10]);
            lon = int(listapsmia[rigps][11]);
            mar = int(listapsmia[rigps][12]);
            pas = int(listapsmia[rigps][13]);
            lpa = int(listapsmia[rigps][14]);
            sht = int(listapsmia[rigps][15]);
            stk = int(listapsmia[rigps][16]);
            slk = int(listapsmia[rigps][17]);
            vol = int(listapsmia[rigps][18]);
            agg = int(listapsmia[rigps][19]);
            atk = int(listapsmia[rigps][20]);
            inte = int(listapsmia[rigps][21]);
            rea = int(listapsmia[rigps][22]);
            vis = int(listapsmia[rigps][23]);
            agi = int(listapsmia[rigps][24]);
            bal = int(listapsmia[rigps][25]);
            acc = int(listapsmia[rigps][26]);
            spr = int(listapsmia[rigps][27]);
            jum = int(listapsmia[rigps][28]);
            sta = int(listapsmia[rigps][29]);
            stre = int(listapsmia[rigps][30]);
            div = int(listapsmia[rigps][31]);
            han = int(listapsmia[rigps][32]);
            kic = int(listapsmia[rigps][33]);
            pos = int(listapsmia[rigps][34]);
            ref = int(listapsmia[rigps][35]);
            for rig in range(0,len(listagioc)):
                if(playid ==  int(listagioc[rig][83]) and (onoff == 1)):
                    listagioc[rig][59]=1;
                    if(psty != -1):
                        listacalc[rig] = psty;
                    if(pots != -1):
                        listagioc[rig][23]=pots;
                    if(roll != -1):
                        listagioc[rig][42]=roll;
                    if(bco != -1):
                        listagioc[rig][43] = bco;
                    if(cro != -1):
                        listagioc[rig][22] = cro;
                    if(dri != -1):
                        listagioc[rig][30] = dri;
                    if(fin != -1):
                        listagioc[rig][29] = fin;
                    if(hea != -1):
                        listagioc[rig][64] = hea;
                    if(lon != -1):
                        listagioc[rig][18] = lon;
                    if(mar != -1):
                        listagioc[rig][84] = mar;
                    if(pas != -1):
                        listagioc[rig][56] = pas;
                    if(lpa != -1):
                        listagioc[rig][13] = lpa;
                    if(sht != -1):
                        listagioc[rig][44] = sht;
                    if(stk != -1):
                        listagioc[rig][10] = stk;
                    if(slk != -1):
                        listagioc[rig][31] = slk;
                    if(vol != -1):
                        listagioc[rig][102] = vol;
                    if(agg != -1):
                        listagioc[rig][62] = agg;
                    if(atk != -1):
                        listagioc[rig][8] = atk;
                    if(inte != -1):
                        listagioc[rig][20] = inte;
                    if(rea != -1):
                        listagioc[rig][26] = rea;
                    if(vis != -1):
                        listagioc[rig][27] = vis;
                    if(agi != -1):
                        listagioc[rig][5] = agi;
                    if(bal != -1):
                        listagioc[rig][50] = bal;
                    if(acc != -1):
                        listagioc[rig][63] = acc;
                    if(spr != -1):
                        listagioc[rig][36] = spr;
                    if(jum != -1):
                        listagioc[rig][79] = jum;
                    if(sta != -1):
                        listagioc[rig][82] = sta;
                    if(stre != -1):
                        listagioc[rig][40] = stre;
                    if(div != -1):
                        listagioc[rig][19] = div;
                    if(han != -1):
                        listagioc[rig][67] = han;
                    if(kic != -1):
                        listagioc[rig][50] = kic;
                    if(pos != -1):
                        listagioc[rig][86] = pos;
                    if(ref != -1):
                        listagioc[rig][24] = ref;
        return listacalc;

    #Dalla posizione del giocatore ricavo il ruolo in generale.
    def GetMacroPosition(self,posid):
        macroid = -1;
        if(posid==0):
            macroid = 0;#GK
        elif(posid==4 or posid==5 or posid==6 or posid==1):
            macroid = 1;#CD-SD
        elif(posid==3 or posid==7):
            macroid = 2;
        elif(posid==2 or posid==8):
            macroid = 3;
        elif(posid==9 or posid==10 or posid==11):
            macroid = 4;
        elif(posid==13 or posid==14 or posid==15):
            macroid = 5;
        elif(posid==17 or posid==18 or posid==19):
            macroid = 6; 
        elif(posid==12 or posid==16):
            macroid=7;
        elif(posid==23 or posid==27):
            macroid=8;
        elif(posid==20 or posid==21 or posid==22):
            macroid=9;#ST
        elif(posid==24 or posid==25 or posid==26):
            macroid=10;
        elif(posid==-1):
            macroid=11
        return macroid;
        
    def Gameplayization(self,StMx,lista,ps):
        for i in range(1,len(StMx)):
            for j in range(0,len(StMx[0])):
                if(i==31):
                    StMx[i][j] = float(StMx[i][j]);
                else:
                    StMx[i][j] = int(StMx[i][j]);
        m=0;
        found=specialplayers=0;
        totlongshot=totlongpasser=totdivetackle=0;
        totplaymaker=totflair=totavoidweak=totearlycrosser=tottiroesterno=0;
        totdiver=totbeatline=totspeeddribbler=totgksavetype=totpowerfk=0;
        tothardhead=totswerve=tot2ndwind=totfinshot=totpunchergk=totoneone=totselfish=0;
        totweak0=totweak1=totweak2=totweak3=totweak4=0;
        totskillm0=totskillm1=totskillm2=totskillm3=totskillm4=0;
        dribbler=poacher=aerialt=speedsteer=engine=distanceshooter=clinicalfinisher=strength=tackling=speedster=playmaker=crosser=acrobat=tactician=0;
        tot10=tot20=tot30=tot40=tot50=tot60=tot70=tot80=tot90=tot99=0;
        top10=top20=top30=top40=top50=top60=top70=top80=top90=top99=0;
        htref=180;wtref=75;perfectwt=0;wtdiff=0;
        perc=1.0;dage=0.0;lonstaker=0;
        agilm90=accem90=sprim90=balam90=jumpm90=stamm90=strem90=0;
        agilm80=accem80=sprim80=balam80=jumpm80=stamm80=strem80=0;
        agilm70=accem70=sprim70=balam70=jumpm70=stamm70=strem70=0;
        agilm55=accem55=sprim55=balam55=jumpm55=stamm55=strem55=0;
        agilm35=accem35=sprim35=balam35=jumpm35=stamm35=strem35=0;
        agilm10=accem10=sprim10=balam10=jumpm10=stamm10=strem10=0;
        for rig in range(len(lista)):
            ht =int(lista[rig][37]); #altezza
            wt =int(lista[rig][47]); #peso
            bdtp =int(lista[rig][98]);#bodytype
            potenz = int(lista[rig][23]); #potenziale
            ir = int(lista[rig][54]);#international reputation
            age = self.etac(int(lista[rig][41]));
            ovr = int(lista[rig][90]);
            ovr = self.Remove_ir_from_ovr(ovr,ir);
            #VALUTAZIONE POTENZIALE
            potlimit=max(0,int((27-age)*2));
            if(potenz-ovr>potlimit):
                potenz=ovr+potlimit;
            if(potenz<ovr):
                potenz=ovr;
            nation = int(lista[rig][75]);
            idplayer = int(lista[rig][83]);
            attw=int(lista[rig][60]);
            defw=int(lista[rig][74]);
            curve = int(lista[rig][3]);
            skillm = int(lista[rig][58]);
            freekacc = int(lista[rig][57]);
            penalt = int(lista[rig][14]);
            contratto = int(lista[rig][28]);
            posid=int(lista[rig][42]);
            posid2=int(lista[rig][39]);
            posid3=int(lista[rig][12]);
            macropos = self.GetMacroPosition(posid);
            macropos2 = self.GetMacroPosition(posid2);
            macropos3 = self.GetMacroPosition(posid3);
            #Coefficienti tecnici e fisici standard.
            coeadd=ovr-70.0;
            oldfk = int(lista[rig][57]);
            oldbco = bco = int(lista[rig][43]);
            oldcro = cro = int(lista[rig][22]);
            olddri = dri = int(lista[rig][30]);
            oldfin = fin = int(lista[rig][29]);
            oldhea = hea = int(lista[rig][64]);
            oldlons = lons = int(lista[rig][18]);
            oldmar = mar = int(lista[rig][84]);
            oldspas = spas = int(lista[rig][56]);
            oldlpas = lpas = int(lista[rig][13]);
            oldpsht = psht = int(lista[rig][44]);
            oldsttk = sttk = int(lista[rig][10]);
            oldsltk = sltk = int(lista[rig][31]);
            oldvol = vol = int(lista[rig][102]);
            oldagg = agg = int(lista[rig][62]);
            oldatk = atk = int(lista[rig][8]);
            oldinte = inte = int(lista[rig][20]);
            oldrea = rea = int(lista[rig][26]);
            oldvis = vis = int(lista[rig][28]);
            oldagil = agil = int(lista[rig][5]);
            oldbala = bala = int(lista[rig][50]);
            oldacce = acce = int(lista[rig][63]);
            oldspri = spri = int(lista[rig][36]);
            oldjump = jump = int(lista[rig][79]);
            oldstam = stam = int(lista[rig][82]);
            oldstre = stre =int(lista[rig][40]);
            olddiv = div = int(lista[rig][19]);
            oldhand = hand = int(lista[rig][67]);
            oldkic = kic = int(lista[rig][52]);
            oldpost = post = int(lista[rig][86]);
            oldref = ref = int(lista[rig][24]);
            oldcurve = curve = int(lista[rig][3]);
            if(posid==0):
                ovrf2 = 0;
                ovrm2 = (oldrea*11)/100.0;
                ovrs2 = (olddiv*21+oldhand*21+oldpost*21+oldref*21+oldkic*5)/100.0;
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            elif(posid==4 or posid==5 or posid==6 or posid==1):
                ovrf2 = (oldstre*10+oldjump*3+oldspri*2)/100.0;#15
                ovrm2 = (oldagg*7+oldinte*13+oldrea*5)/100.0;#25
                ovrs2 = (oldmar*14+oldsttk*17+oldsltk*10+oldhea*10+oldspas*5+oldbco*4)/100.0;#60
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            elif(posid==3 or posid==7):
                ovrf2 = (oldacce*5+oldstam*8+oldspri*7)/100.0;#20
                ovrm2 = (oldinte*12+oldrea*8)/100.0;#20
                ovrs2 = (oldsltk*14+oldsttk*11+oldmar*8+oldcro*9+oldhea*4+oldbco*7+oldspas*7)/100.0;#60
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            elif(posid==2 or posid==8):
                ovrf2 = (oldstam*10+oldspri*6+oldacce*4)/100.0;#20
                ovrm2 = (oldinte*12+oldrea*8)/100.0;#20
                ovrs2 = (oldsttk*8+oldsltk*11+oldcro*12+oldspas*10+oldbco*8+oldmar*7+olddri*4)/100.0;#60
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            elif(posid==9 or posid==10 or posid==11):
                ovrf2 = (oldstam*6+oldstre*4)/100.0;#10
                ovrm2 = (oldinte*14+oldrea*7+oldvis*4+oldagg*5)/100.0;#30
                ovrs2 = (oldspas*14+oldlpas*10+oldmar*9+oldsttk*12+oldbco*10+oldsltk*5)/100.0;#60
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            elif(posid==13 or posid==14 or posid==15):
                ovrf2 = (oldstam*6)/100.0;#6
                ovrm2 = (oldvis*13+oldrea*8+oldinte*5+oldatk*6)/100.0;#32
                ovrs2 = (oldspas*17+oldlpas*13+oldbco*14+olddri*7+oldfin*2+oldsttk*5+oldlons*4)/100.0;#62
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            elif(posid == 18 or posid==17 or posid==19):
                ovrf2 = (oldacce*4+oldagil*3+oldspri*3)/100.0;#10
                ovrm2 = (oldvis*14+oldatk*9+oldrea*7)/100.0;#30
                ovrs2 = (oldspas*16+oldbco*15+olddri*13+oldlons*5+oldfin*7+oldlpas*4)/100.0;#60
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            elif(posid==12 or posid==16 ):
                ovrf2 = (oldstam*5+oldacce*7+oldspri*6)/100.0;#18
                ovrm2 = (oldvis*7+oldrea*7+oldatk*8)/100.0;#22
                ovrs2 = (oldcro*10+olddri*15+oldspas*11+oldbco*13+oldlpas*5+oldfin*6)/100.0;#60
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            elif(posid==23 or posid==27):
                ovrf2 = (oldacce*7+oldspri*6+oldagil*3)/100.0;#16
                ovrm2 = (oldatk*9+oldrea*7+oldvis*6)/100.0;#22
                ovrs2 = (oldcro*9+olddri*16+oldbco*14+oldspas*9+oldfin*10+oldlons*4)/100.0;#62
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            elif(posid==20 or posid==21 or posid==22):
                ovrf2 = (oldacce*5+oldspri*5)/100.0;#10
                ovrm2 = (oldatk*13+oldrea*9+oldvis*8)/100.0;#30
                ovrs2 = (oldfin*11+olddri*14+oldbco*15+oldpsht*5+oldlons*4+oldspas*9+oldhea*2)/100.0;#60
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            elif(posid==24 or posid==25 or posid==26):
                ovrf2 = (oldacce*4+oldspri*5+oldstre*5)/100.0;#14
                ovrm2 = (oldatk*13+oldrea*8)/100.0;#21
                ovrs2 = (oldfin*18+oldhea*10+oldpsht*10+olddri*7+oldbco*10+oldvol*2+oldlons*3+oldspas*5)/100.0;#65
                ovrtt2 = ovrf2+ovrm2+ovrs2;
            ###NEW OVERALL WIDE RANGE###
            perfectwt=int((0.8*ht)-68.4);
            perfectht=int((wt+68.4)/0.8);
            hw= ht-100-wt;
            if(ps[rig]>87):
                ps[rig]=87;
            #self.textEdit.append(str(ps[rig])+"**"+str(rig)+"**"+str(idplayer));
            if(int(lista[rig][59])!=1):
                agefactormental=0;#int((age-25)*0.75);#5*0.5=2.5
                agefactorphisical=0;#int((age-25)*-0.75);#5*-0.5=-2.5
                agefactortech=0;
                if(age-27>=0):
                    agefactortech=int((age-27)*0.5);
                    agefactormental=int(0);
                    agefactorphisical=int(abs(age-27)**1.5);
                else:
                    agefactortech=int((age-27)*0.50);
                    agefactormental=int((27-age)**1.25)*-1;
                    agefactorphisical=int(0);               
                overallfactormental = 0;#int((ovr-80)/2);#65-80=-15/2=-7.5;90-80=10/2=5
                overallfactorphisical= 0;#int((ovr-80)/2);#
                lmm=99;
                bco =min(lmm,int(self.zone(StMx[1][ps[rig]],ovr,0))+agefactortech);
                cro =min(lmm,int(self.zone(StMx[2][ps[rig]],ovr,0))+agefactortech);
                dri =min(lmm,int(self.zone(StMx[3][ps[rig]],ovr,0))+agefactortech);
                fin =min(lmm,int(self.zone(StMx[4][ps[rig]],ovr,0))+agefactortech);
                hea =min(lmm,int(self.zone(StMx[5][ps[rig]],ovr,0))+agefactortech);
                lons=min(lmm,int(self.zone(StMx[6][ps[rig]],ovr,0))+agefactortech);
                mar =min(lmm,int(self.zone(StMx[7][ps[rig]],ovr,0))+agefactortech);
                spas=min(lmm,int(self.zone(StMx[8][ps[rig]],ovr,0))+agefactortech);
                lpas=min(lmm,int(self.zone(StMx[9][ps[rig]],ovr,0))+agefactortech);
                psht=min(lmm,int(self.zone(StMx[10][ps[rig]],ovr,0))+agefactortech);
                sttk=min(lmm,int(self.zone(StMx[11][ps[rig]],ovr,0))+agefactortech);
                sltk=min(lmm,int(self.zone(StMx[12][ps[rig]],ovr,0))+agefactortech);
                vol =min(lmm,int(self.zone(StMx[13][ps[rig]],ovr,0))+agefactortech);
                agg =min(lmm,int(self.zone(StMx[14][ps[rig]],ovr,2))+agefactormental+overallfactormental);
                atk =min(lmm,int(self.zone(StMx[15][ps[rig]],ovr,2))+agefactormental+overallfactormental);
                inte=min(lmm,int(self.zone(StMx[16][ps[rig]],ovr,2))+agefactormental+overallfactormental);
                rea =min(lmm,int(self.zone(StMx[16][ps[rig]],ovr,2))+agefactormental+overallfactormental);#min(lmm,int(self.zone(StMx[17][ps[rig]],ovr,2))+agefactormental+overallfactormental);
                vis =min(lmm,int(self.zone(StMx[18][ps[rig]],ovr,2))+agefactormental+overallfactormental);
                if(posid==0):
                    div = int(self.zone(StMx[26][ps[rig]],ovr,0));
                    hand = int(self.zone(StMx[27][ps[rig]],ovr,0));
                    kic = int(self.zone(StMx[28][ps[rig]],ovr,0));
                    post = int(self.zone(StMx[29][ps[rig]],ovr,0));
                    ref = int(self.zone(StMx[30][ps[rig]],ovr,0));
                else:
                    div = 5;
                    hand = 5;
                    kic = 5;
                    post = 5;
                    ref = 5;
                agilzone = StMx[19][ps[rig]];
                balazone = StMx[20][ps[rig]];
                accezone = StMx[21][ps[rig]];
                sprizone = StMx[22][ps[rig]];
                jumpzone = StMx[23][ps[rig]];
                stamzone = StMx[24][ps[rig]];
                strezone = StMx[25][ps[rig]];
                #1=+20;2=+10;3=+5;4=-10;5=-20
                azone=-0.7143;
                bzone=-6.7143;
                czone=27
                agil=64+random.randrange(-2,3)+int(azone*agilzone*agilzone+bzone*agilzone+czone)+agefactorphisical;#min(lmm,int(self.zone(agilzone,ovr,1))+agefactorphisical+overallfactorphisical);
                bala=64+random.randrange(-2,3)+int(azone*balazone*balazone+bzone*balazone+czone)+agefactorphisical;#min(lmm,int(self.zone(balazone,ovr,1))+agefactorphisical+overallfactorphisical);
                acce=64+random.randrange(-2,3)+int(azone*accezone*accezone+bzone*accezone+czone)+agefactorphisical;#min(lmm,int(self.zone(accezone,ovr,1))+agefactorphisical+overallfactorphisical);
                spri=64+random.randrange(-2,3)+int(azone*sprizone*sprizone+bzone*sprizone+czone)+agefactorphisical;#min(lmm,int(self.zone(sprizone,ovr,1))+agefactorphisical+overallfactorphisical);
                jump=64+random.randrange(-2,3)+int(azone*jumpzone*jumpzone+bzone*jumpzone+czone)+agefactorphisical;#min(lmm,int(self.zone(jumpzone,ovr,1))+agefactorphisical+overallfactorphisical);
                stam=64+random.randrange(-2,3)+int(azone*stamzone*stamzone+bzone*stamzone+czone)+agefactorphisical;#min(lmm,int(self.zone(stamzone,ovr,1))+agefactorphisical+overallfactorphisical);
                stre=64+random.randrange(-2,3)+int(azone*strezone*strezone+bzone*strezone+czone)+agefactorphisical;#min(lmm,int(self.zone(strezone,ovr,1))+agefactorphisical+overallfactorphisical);
                wwt = wt-perfectwt;
                hht = ht-180;
                if(ht>=200):
                    stre=stre+20;
                    agil=agil-30;
                    jump=jump+10;
                    acce=acce+5;
                elif(ht>=195):
                    stre=stre+15;
                    agil=agil-20;
                    jump=jump+10;
                    acce=acce+5;
                elif(ht>=190):
                    stre=stre+10;
                    agil=agil-10;
                    jump=jump+5;
                    acce=acce+5;
                elif(ht>=185):
                    stre=stre+5;
                    agil=agil-5;
                    jump=jump+2;
                    acce=acce+5;
                elif(ht>=180):
                    stre=stre+0;
                    agil=agil-0;
                    spri=spri+5;
                    acce=acce+0;
                elif(ht>=175):
                    stre=stre-5;
                    agil=agil+5;
                    jump=jump-5;
                    stam=stam+5;
                    spri=spri+5;
                elif(ht>=170):
                    stre=stre-10;
                    agil=agil+10;
                    jump=jump-10;
                    stam=stam+5;
                    spri=spri+5;
                elif(ht>=165):
                    stre=stre-20;
                    agil=agil+15;
                    jump=jump-20;
                    stam=stam+5;
                    spri=spri+5;
                elif(ht>=160):
                    stre=stre-30;
                    agil=agil+20;
                    jump=jump-30;
                    stam=stam+5;
                    spri=spri+5;
                elif(ht<161):
                    stre=stre-40;
                    agil=agil+20;
                    jump=jump-40;
                    stam=stam+5;
                    spri=spri+5;
                if(wwt>=9):
                    acce=acce+10;
                    spri=spri-30;
                    stam=stam-20;
                    bala=bala+30;
                    stre=stre+10;
                    agil=agil-20;
                elif(wwt>=6):
                    acce=acce+10;
                    spri=spri-20;
                    stam=stam-10;
                    bala=bala+20;
                    stre=stre+5;
                    agil=agil-10;
                elif(wwt>=3):
                    acce=acce+10;
                    spri=spri-10;
                    stam=stam-5;
                    bala=bala+10;
                    stre==stre+5;
                    agil=agil-5;
                elif(wwt>=0):
                    acce=acce+5;
                    spri=spri-5;
                    stam=stam-0;
                    bala=bala+5;
                elif(wwt>=-3):
                    acce=acce+0;
                    spri=spri-0;
                    stam=stam+5;
                    bala=bala+0;
                    agil=agil+2;
                elif(wwt>=-6):
                    acce=acce-5;
                    spri=spri+5;
                    stam=stam+5;
                    bala=bala-5;
                    stre=stre-2;
                    agil=agil+5;
                elif(wwt>=-9):
                    acce=acce-10;
                    spri=spri+10;
                    stam=stam+10;
                    bala=bala-10;
                    stre=stre-5;
                    agil=agil+10;
                elif(wwt>=-12):
                    acce=acce-20;
                    spri=spri+15;
                    stam=stam+10;
                    bala=bala-10;
                    stre=stre-10;
                    agil=agil+15;
                elif(wwt<=-13):
                    acce=acce-30;
                    spri=spri+20;
                    stam=stam-5;
                    bala=bala-10;
                    stre=stre-20;
                    agil=agil+15;
            ###CALCOLO DEI NUOVI OVERALL###
            if(posid==0):
                ovrf1 = 0;
                ovrm1 = (rea*11)/100.0;
                ovrs1 = (div*21+hand*21+post*21+ref*21+kic*5)/100.0;
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            elif(posid==4 or posid==5 or posid==6 or posid==1):
                ovrf1 = (stre*10+jump*3+spri*2)/100.0;#15
                ovrm1 = (agg*7+inte*13+rea*5)/100.0;#25
                ovrs1 = (mar*14+sttk*17+sltk*10+hea*10+spas*5+bco*4)/100.0;#60
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            elif(posid==3 or posid==7):
                ovrf1 = (acce*5+stam*8+spri*7)/100.0;#20
                ovrm1 = (inte*12+rea*8)/100.0;#20
                ovrs1 = (sltk*14+sttk*11+mar*8+cro*9+hea*4+bco*7+spas*7)/100.0;#60
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            elif(posid==2 or posid==8):
                ovrf1 = (stam*10+spri*6+acce*4)/100.0;#20
                ovrm1 = (inte*12+rea*8)/100.0;#20
                ovrs1 = (sttk*8+sltk*11+cro*12+spas*10+bco*8+mar*7+dri*4)/100.0;#60
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            elif(posid==9 or posid==10 or posid==11):
                ovrf1 = (stam*6+stre*4)/100.0;#10
                ovrm1 = (inte*14+rea*7+vis*4+agg*5)/100.0;#30
                ovrs1 = (spas*14+lpas*10+mar*9+sttk*12+bco*10+sltk*5)/100.0;#60
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            elif(posid==13 or posid==14 or posid==15):
                ovrf1 = (stam*6)/100.0;#6
                ovrm1 = (vis*13+rea*8+inte*5+atk*6)/100.0;#32
                ovrs1 = (spas*17+lpas*13+bco*14+dri*7+fin*2+sttk*5+lons*4)/100.0;#62
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            elif(posid == 18 or posid==17 or posid==19):
                ovrf1 = (acce*4+agil*3+spri*3)/100.0;#10
                ovrm1 = (vis*14+atk*9+rea*7)/100.0;#30
                ovrs1 = (spas*16+bco*15+dri*13+lons*5+fin*7+lpas*4)/100.0;#60
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            elif(posid==12 or posid==16 ):
                ovrf1 = (stam*5+acce*7+spri*6)/100.0;#18
                ovrm1 = (vis*7+rea*7+atk*8)/100.0;#22
                ovrs1 = (cro*10+dri*15+spas*11+bco*13+lpas*5+fin*6)/100.0;#60
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            elif(posid==23 or posid==27):
                ovrf1 = (acce*7+spri*6+agil*3)/100.0;#16
                ovrm1 = (atk*9+rea*7+vis*6)/100.0;#22
                ovrs1 = (cro*9+bco*16+dri*14+spas*9+fin*10+lons*4)/100.0;#62
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            elif(posid==20 or posid==21 or posid==22):
                ovrf1 = (acce*5+spri*5)/100.0;#10
                ovrm1 = (atk*13+rea*9+vis*8)/100.0;#30
                ovrs1 = (fin*11+dri*14+bco*15+psht*5+lons*4+spas*9+hea*2)/100.0;#60
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            elif(posid==24 or posid==25 or posid==26):
                ovrf1 = (acce*4+spri*5+stre*5)/100.0;#14
                ovrm1 = (atk*13+rea*8)/100.0;#21
                ovrs1 = (fin*18+hea*10+psht*10+dri*7+bco*10+vol*2+lons*3+spas*5)/100.0;#65
                ovrtt1 = ovrf1+ovrm1+ovrs1;
            ###NEW OVERALL WIDE RANGE###
            diffovrs=ovrtt1-ovr;
            if(int(lista[rig][59])!=1):
                bco=int(max(5,min(99,bco-diffovrs)));
                cro=int(max(5,min(99,cro-diffovrs)));
                dri=int(max(5,min(99,dri-diffovrs)));
                fin=int(max(5,min(99,fin-diffovrs)));
                hea=int(max(5,min(99,hea-diffovrs)));
                lons=int(max(5,min(99,lons-diffovrs)));
                mar=int(max(5,min(99,mar-diffovrs)));
                spas=int(max(5,min(99,spas-diffovrs)));
                lpas=int(max(5,min(99,lpas-diffovrs)));
                psht=int(max(5,min(99,psht-diffovrs)));
                sttk=int(max(5,min(99,sttk-diffovrs)));
                sltk=int(max(5,min(99,sltk-diffovrs)));
                vol=int(max(5,min(99,vol-diffovrs)));
                agg=int(max(10,min(99,agg-diffovrs)));
                atk=int(max(10,min(99,atk-diffovrs)));
                inte=int(max(10,min(99,inte-diffovrs)));
                rea=int(max(10,min(99,rea-diffovrs)));
                vis=int(max(10,min(99,vis-diffovrs)));
                acce=int(max(10,min(99,acce-diffovrs)));
                agil=int(max(10,min(99,agil-diffovrs)));
                bala=int(max(10,min(99,bala-diffovrs)));
                spri=int(max(10,min(99,spri-diffovrs)));
                jump=int(max(10,min(99,jump-diffovrs)));
                stam=int(max(10,min(99,stam-diffovrs)));
                stre=int(max(10,min(99,stre-diffovrs)));
                skillm = int(StMx[35][ps[rig]]);
                skillm = skillm+1;
                skillm = min(max(skillm,0),4);
                freekacc = max(5,min(100,max(freekacc,skillm*25+random.randrange(-20,-5))));
                curve = max(curve,int(skillm*25+random.randrange(-20,-5))); 
                div = int(max(10,min(random.randrange(96,100),div-diffovrs)));
                hand = int(max(10,min(random.randrange(96,100),hand-diffovrs)));
                kic = int(max(10,min(random.randrange(96,100),kic-diffovrs)));
                post = int(max(10,min(random.randrange(96,100),post-diffovrs)));
                ref = int(max(10,min(random.randrange(96,100),ref-diffovrs)));
            #NATION COEFF:
    #Valori tecnici. Moltiplico i vaori della matrice per il coefficiente tecnico.    
            weakf=int(lista[rig][78]); #-1a3, 11234 , da 1 a 5
            if((weakf)==4):
                weakf=3;
            elif((weakf)==2):
                weakf=1;
    ####SKILL MOVES
            if(posid == 0):
                #curve = int(curve/3);
                freekacc = int(freekacc/3);
            #ASSEGNAZIONE TRAIT. Per chi ce l'ha gia non faccio modifiche, altrimenti li aggiungo.
            # 0 1         Inflexibility
            # 1 2         Long Throw In 
            # 2 4         Powerful Free Kick
            # 3 8         Diver
            # 4 16        Injury Prone 
            # 5 32        Injury Free 
            # 6 64        Avoid to use the Weak foot 
            # 7 128       Dives Into Tackles 
            # 8 256       Tries To Beat Defensive Line 
            # 9 512       Selfish 
            #10 1024      Leadership 
            #11 2048      Argues With Referee 
            #12 4096      Early Crosser
            #13 8192      Try Often Finesse Shot
            #14 16384     Flair
            #15 32768     Long Passer
            #16 65536     Long shot taker
            #17 131072    Speed Dribbler
            #18 262144    Play Maker
            #19 524288    Pushes Up for Corners
            #20 1048576   Puncher GK
            #21 2097152   Long Thrower GK
            #22 4194304   Power Header
            #23 8388608   NE (uno contro uno)
            #24 16777216  Giant Throwin
            #25 33554432  OutSide Foot Shot
            #26 67108864  NE (favorito tifosi)
            #27 134217728 Through Ball
            #28 268435456 NE  (second wind)
            #29 536870912 NE acrobatic clearance
            trait1 = self.trait(int(lista[rig][45]));
            ppos1 = int(lista[rig][42]);
            if(int(lista[rig][9])==1):
                totgksavetype = totgksavetype+1;
            if(ppos1==0)and((ps[rig]==0)or(ps[rig]==1)or(ps[rig]==2)or(ps[rig]==3)):
                gksavetype=1;
                totgksavetype = totgksavetype+1;
            else:
                gksavetype=0;
            if(trait1[16]==0):
                if(ppos1!=0)and(ps[rig]>=32):
                    trait1[16]=1;
                    totlongshot=totlongshot+1;
            else:
                totlongshot=totlongshot+1; 
            if(trait1[2]==0):
                if((psht>=85)and(freekacc>=70)):
                    trait1[2]=1;
                    totpowerfk=totpowerfk+1;
            else:
                totpowerfk=totpowerfk+1;
            if(trait1[3]==0):
                if(((ps[rig]>=0)and(ps[rig]<=14))):
                    trait1[3]=0;
                else:
                    trait1[3]=1;
                    totdiver = totdiver+1;
            else:
                totdiver=totdiver+1;
            if(trait1[6]==0):
                if((weakf<=3)):
                    trait1[6]=1;
                    totavoidweak = totavoidweak +1;
            else:
                totavoidweak = totavoidweak + 1;
            if(trait1[15]==0):
                if(ppos1!=0)and((ps[rig]==8)or(ps[rig]==10)or(ps[rig]==14)or(ps[rig]==16)or(ps[rig]==17)or(ps[rig]==18)or
                                (ps[rig]==33)or(ps[rig]==37)or(ps[rig]==42)or(ps[rig]==44)or(ps[rig]==47)or(ps[rig]==48)or
                                (ps[rig]==56)or(ps[rig]==9)or(ps[rig]==11)):
                    trait1[15]=0;
                else:
                    trait1[15]=1;
                    totlongpasser=totlongpasser+1;
            else:
                totlongpasser=totlongpasser+1;
            if(trait1[14]==0):
                if(((ps[rig]>=40)) and skillm>=3):
                    trait1[14]=1;
                    totflair=totflair+1;
            else:
                totflair=totflair+1;
            if(trait1[18]==0):
                if((ps[rig]==37)or(ps[rig]==44)or(ps[rig]==50))and(ppos1!=0):
                    trait1[18]=1;
                    totplaymaker = totplaymaker+1;
            else:
                totplaymaker = totplaymaker+1;
            if(trait1[9]==0):
                if((ps[rig]>=64)):
                    if(ppos1!=0):
                        trait1[9]=1;
                        totselfish = totselfish+1;
            else:
                totselfish = totselfish+1;
            if(trait1[25]==0):
                if(skillm>=4):
                    if(ppos1!=0):
                        trait1[25]=1;
                        tottiroesterno = tottiroesterno+1;
            else:
                tottiroesterno = tottiroesterno+1;
            if(trait1[12]==0):
                if((ps[rig]==16)or(ps[rig]==18)or(ps[rig]==64)or(ps[rig]==56)or(ps[rig]==59)):
                    totearlycrosser = totearlycrosser +1;
                    trait1[12]=1;
            else:
                totearlycrosser = totearlycrosser + 1;
            if(trait1[7]==0):
                if((ps[rig]==14)or(ps[rig]==17)or(ps[rig]==18)or(ps[rig]==19)or(ps[rig]==34)or(ps[rig]==41)or(ps[rig]==15))and(ppos1!=0):
                    trait1[7]=1;
                    totdivetackle=totdivetackle+1;
            else:
                totdivetackle=totdivetackle+1;
            if(trait1[8]==0):
                if((ppos1!=0)and((ps[rig]==58)or(ps[rig]==66)or(ps[rig]==74)or(ps[rig]==80))):
                    trait1[8]=1;
                    totbeatline = totbeatline+1;
            else:
                totbeatline = totbeatline+1;
            if(trait1[17]==0):
                if((ps[rig]==16)or(ps[rig]==17)or(ps[rig]==19)or(ps[rig]==45)or(ps[rig]==56)or(ps[rig]==76)or(ps[rig]==84))and(ppos1!=0):
                    trait1[17]=1;
                    totspeeddribbler = totspeeddribbler +1;
            else:
                totspeeddribbler = totspeeddribbler +1;
            if(trait1[23]==0):
                if((ps[rig]==2))and(ppos1==0):
                    trait1[23]=1;
                    totoneone = totoneone+1;
            else:
                totoneone = totoneone+1;
            if(trait1[22]==0):
                if(hea>=90)and(ppos1!=0):
                    trait1[22]=1;
                    tothardhead = tothardhead+1;
            else:
                tothardhead = tothardhead+1;
            if(trait1[27]==0):
                if(skillm>=4)and(ppos1!=0):
                    trait1[27]=1;
                    totswerve = totswerve+1;
            else:
                totswerve = totswerve+1;
            if(trait1[28]==0):
                if(((ps[rig]==32)or(ps[rig]==40)or(ps[rig]==34)or(ps[rig]==35)) and(ppos1!=0)):
                    trait1[28]=1;
                    tot2ndwind = tot2ndwind+1;
            else:
                tot2ndwind = tot2ndwind+1;
            if(trait1[13]==0):
                if((ps[rig]==50)or(ps[rig]==73)or(ps[rig]==86))and(ppos1!=0):
                    trait1[13]=1;
                    totfinshot = totfinshot+1;
            else:
                totfinshot = totfinshot+1;
            if(trait1[20]==0):
                if((ps[rig]==0)and(ppos1==0)):
                    trait1[20]=1;
                    totpunchergk = totpunchergk+1;
            else:
                totpunchergk = totpunchergk+1;
            lstrait1 = self.sommatrait(trait1);               
            #print(trait1);
            attw = (StMx[33][ps[rig]]);
            defw = (StMx[34][ps[rig]]);
            #SPECIALTIES
            #dribbler=poacher=aerialt=speedsteer=engine=distanceshooter=clinicalfinisher=strength=playmaker=crosser=acrobat=tactician=0;
            if((dri>=86 and skillm==4)or(dri>=86 and bala>=75)):
                dribbler=dribbler+1;
            if((fin>=85 and hea>=75) and (attw==0 or attw==1) and (defw==0 or defw==1)):
                poacher=poacher+1;
            if((ht<=188 and hea>=90 and (stre>=85 or jump>=85))):
                aerialt=aerialt+1;
            if((acce+spri)>=180):
                speedsteer=speedsteer+1;
            if(defw==2 and attw==2):
                engine=engine+1;
            if((psht+lons)>=174):
                distanceshooter=distanceshooter+1;
            if(lons>=80 and fin>=86):
                clinicalfinisher=clinicalfinisher+1;
            if((wt>=82 and stre>=90) or (wt>=83 and stre>=86)):
                strength=strength+1;
            if(spas>=86 and vis>=86 and lpas>=73):
                playmaker=playmaker+1;
            if(cro>=86 and curve>=80):
                crosser=crosser+1;
            if(agil>=90 or (agil>=86 and rea>=80)):
                acrobat=acrobat+1;
            if(sttk>=86 and sltk>=85):
                tackling=tackling+1;
            if(inte>=86 and rea>=80):
                tactician=tactician+1;
            if(contratto<2014):
                    contratto = 2014;
            elif(contratto>2020):
                    contratto = 2020;
            #######
            ttt=ovr;
            ppp=potenz;
            if(ttt>19) and (ttt<30):
                tot20 = tot20+1;
            elif(ttt>29) and (ttt<40):
                tot30 = tot30+1;
            elif(ttt>39) and (ttt<50):
                tot40 = tot40+1;
            elif(ttt>49) and (ttt<60):
                tot50 = tot50+1;
            elif(ttt>59) and (ttt<70):
                tot60 = tot60+1;
            elif(ttt>69) and (ttt<80):
                tot70 = tot70+1;
            elif(ttt>79) and (ttt<90):
                tot80 = tot80+1;
            elif(ttt>89) and (ttt<100):
                tot90 = tot90+1;
            if(ppp>19) and (ppp<30):
                top20 = top20+1;
            elif(ppp>29) and (ppp<40):
                top30 = top30+1;
            elif(ppp>39) and (ppp<50):
                top40 = top40+1;
            elif(ppp>49) and (ppp<60):
                top50 = top50+1;
            elif(ppp>59) and (ppp<70):
                top60 = top60+1;
            elif(ppp>69) and (ppp<80):
                top70 = top70+1;
            elif(ppp>79) and (ppp<90):
                top80 = top80+1;
            elif(ppp>89) and (ppp<100):
                top90 = top90+1;
            #lista[rig][0] = str(birthdate);
            if(agil<35):
                agilm10=agilm10+1;
            elif(agil>=35 and agil<55):
                agilm35=agilm35+1;
            elif(agil>=55 and agil<70):
                agilm55=agilm55+1;
            elif(agil>=70 and agil<80):
                agilm70=agilm70+1;
            elif(agil>=80 and agil<90):
                agilm80=agilm80+1;
            elif(agil>=90):
                agilm90=agilm90+1;
            if(bala<35):
                balam10=balam10+1;
            elif(bala>=35 and bala<55):
                balam35=balam35+1;
            elif(bala>=55 and bala<70):
                balam55=balam55+1;
            elif(bala>=70 and bala<80):
                balam70=balam70+1;
            elif(bala>=80 and bala<90):
                balam80=balam80+1;
            elif(bala>=90):
                balam90=balam90+1;
            if(acce<35):
                accem10=accem10+1;
            elif(acce>=35 and acce<55):
                accem35=accem35+1;
            elif(acce>=55 and acce<70):
                accem55=accem55+1;
            elif(acce>=70 and acce<80):
                accem70=accem70+1;
            elif(acce>=80 and acce<90):
                accem80=accem80+1;
            elif(acce>=90):
                accem90=accem90+1;
            if(spri<35):
                sprim10=sprim10+1;
            elif(spri>=35 and spri<55):
                sprim35=sprim35+1;
            elif(spri>=55 and spri<70):
                sprim55=sprim55+1;
            elif(spri>=70 and spri<80):
                sprim70=sprim70+1;
            elif(spri>=80 and spri<90):
                sprim80=sprim80+1;
            elif(spri>=90):
                sprim90=sprim90+1;
            if(jump<35):
                jumpm10=jumpm10+1;
            elif(jump>=35 and jump<55):
                jumpm35=jumpm35+1;
            elif(jump>=55 and jump<70):
                jumpm55=jumpm55+1;
            elif(jump>=70 and jump<80):
                jumpm70=jumpm70+1;
            elif(jump>=80 and jump<90):
                jumpm80=jumpm80+1;
            elif(jump>=90):
                jumpm90=jumpm90+1;
            if(stam<35):
                sprim10=stamm10+1;
            elif(stam>=35 and stam<55):
                stamm35=stamm35+1;
            elif(stam>=55 and stam<70):
                stamm55=stamm55+1;
            elif(stam>=70 and stam<80):
                stamm70=stamm70+1;
            elif(stam>=80 and stam<90):
                stamm80=stamm80+1;
            elif(stam>=90):
                stamm90=stamm90+1;
            if(stre<35):
                strem10=strem10+1;
            elif(stre>=35 and stre<55):
                strem35=strem35+1;
            elif(stre>=55 and stre<70):
                strem55=strem55+1;
            elif(stre>=70 and stre<80):
                strem70=strem70+1;
            elif(stre>=80 and stre<90):
                strem80=strem80+1;
            elif(stre>=90):
                strem90=strem90+1;
            lista[rig][28] = str(contratto);
            lista[rig][23] = str(max(5,min(95,potenz)));
            lista[rig][7] = str(0);#str(gksavetype);
            lista[rig][43] = str(bco);
            lista[rig][22] = str(cro);
            lista[rig][30] = str(dri);
            lista[rig][29] = str(fin);
            lista[rig][64] = str(hea);
            lista[rig][18] = str(lons);
            lista[rig][84] = str(mar);
            lista[rig][56] = str(spas);
            lista[rig][13] = str(lpas);
            lista[rig][44] = str(psht);
            lista[rig][10] = str(sttk);
            lista[rig][31] = str(sltk);
            lista[rig][102] = str(vol);
            lista[rig][62] = str(agg);
            lista[rig][8] = str(atk);
            lista[rig][20] = str(inte);
            lista[rig][26] = str(rea);
            lista[rig][27] = str(vis);
            lista[rig][5] = str(agil);
            lista[rig][50] = str(bala);
            lista[rig][63] = str(acce);
            lista[rig][36] = str(spri);
            lista[rig][79] = str(jump);
            lista[rig][82] = str(stam);
            lista[rig][40] = str(stre);
            lista[rig][90] = str(ovr) 
            lista[rig][19] = str(div);
            lista[rig][67] = str(hand);
            lista[rig][50] = str(kic);
            lista[rig][86] = str(post);
            lista[rig][24] = str(ref);
            lista[rig][12] = str(-1);
            lista[rig][101] = str(-1);
            lista[rig][78] = str(weakf);
            lista[rig][60] = str(attw);
            lista[rig][74] = str(defw);
            lista[rig][3] = str(max(20,min(95,curve)));
            lista[rig][57] = str(max(20,min(95,freekacc)));
            lista[rig][14] = str(max(20,min(95,penalt)));
            lista[rig][45] = str(lstrait1);
            lista[rig][42] = str(posid);
            lista[rig][39] = str(posid2);
            if(lista[rig][59]==1):
                specialplayers=specialplayers+1;
            lista[rig][59] = str(0);
        self.textEdit.append("SPECIAL ID players:");
        self.textEdit.append("No:"+str(specialplayers));
        self.textEdit.append("TRAITS statistics:");
        self.textEdit.append("players with LONGSHOTTAKER trait: "+str(totlongshot)+" ("+str(totlongshot*100/playerstotal)+"%) ");
        self.textEdit.append("players with LONGPASSER trait: "+str(totlongpasser)+" ("+str(totlongpasser*100/playerstotal)+"%) ");
        self.textEdit.append("players with DIVE INTO TACKLE trait: "+str(totdivetackle)+" ("+str(totdivetackle*100/playerstotal)+"%) ");
        self.textEdit.append("players with PLAY MAKER trait: "+str(totplaymaker)+" ("+str(totplaymaker*100/playerstotal)+"%) ");
        self.textEdit.append("players with FLAIR trait: "+str(totflair)+" ("+str(totflair*100/playerstotal)+"%) ");
        self.textEdit.append("players with AVOID WEAK FOOT trait: "+str(totavoidweak)+" ("+str(totavoidweak*100/playerstotal)+"%) ");
        self.textEdit.append("players with EARLY CROSSER trait: "+str(totearlycrosser)+" ("+str(totearlycrosser*100/playerstotal)+"%) ");
        self.textEdit.append("players with SPEED DRIBBLER trait: "+str(totspeeddribbler)+" ("+str(totspeeddribbler*100/playerstotal)+"%) ");
        self.textEdit.append("players with PLAY AT OFFSIDE LIMIT trait: "+str(totbeatline)+" ("+str(totbeatline*100/playerstotal)+"%) ");
        self.textEdit.append("players with DIVER trait: "+str(totdiver)+" ("+str(totdiver*100/playerstotal)+"%) ");
        self.textEdit.append("players with POWERFUL HEADER trait: "+str(tothardhead)+" ("+str(tothardhead*100/playerstotal)+"%) ");
        self.textEdit.append("players with POWERFUL FREEKICK trait: "+str(totpowerfk)+" ("+str(totpowerfk*100/playerstotal)+"%) ");
        self.textEdit.append("players with OUTSIDE FOOT SHOT trait: "+str(tottiroesterno)+" ("+str(tottiroesterno*100/playerstotal)+"%) ");
        self.textEdit.append("players with SWING PASSES trait: "+str(totswerve)+" ("+str(totswerve*100/playerstotal)+"%) ");
        self.textEdit.append("players with HIGH STAMINA trait: "+str(tot2ndwind)+" ("+str(tot2ndwind*100/playerstotal)+"%) ");
        self.textEdit.append("players with FINESSE SHOT trait: "+str(totfinshot)+" ("+str(totfinshot*100/playerstotal)+"%) ");
        self.textEdit.append("players with SELFISH trait: "+str(totselfish)+" ("+str(totselfish*100/playerstotal)+"%) ");
        self.textEdit.append("keepers with GK PUNCHER trait: "+str(totpunchergk)+" ("+str(totpunchergk*100/gktotal)+"%) ");
        self.textEdit.append("keepers with ONE VS ONE trait: "+str(totoneone)+" ("+str(totoneone*100/gktotal)+"%) ");
        self.textEdit.append("keepers with ACROBATIC SAVE trait: "+str(totgksavetype)+" ("+str(totgksavetype*100/gktotal)+"%) ");
        #dribbler=poacher=aerialt=speedsteer=engine=distanceshooter=clinicalfinisher=strength=playmaker=crosser=acrobat=tactician=0;
        self.textEdit.append("SPECIAL statistics:");
        self.textEdit.append("players with DRIBBLER spec: "+str(dribbler)+" "+str(dribbler*100/playerstotal));
        self.textEdit.append("players with POACHER spec: "+str(poacher)+" "+str(poacher*100/playerstotal));
        self.textEdit.append("players with AERIAL THREAT spec: "+str(aerialt)+" "+str(aerialt*100/playerstotal));
        self.textEdit.append("players with SPEEDSTER spec: "+str(speedsteer)+" "+str(speedsteer*100/playerstotal));
        self.textEdit.append("players with ENGINE spec: "+str(engine)+" "+str(engine*100/playerstotal));
        self.textEdit.append("players with DISTANCE SHOOT spec: "+str(distanceshooter)+" "+str(distanceshooter*100/playerstotal));
        self.textEdit.append("players with CLINICAL FINISHER spec: "+str(clinicalfinisher)+" "+str(clinicalfinisher*100/playerstotal));
        self.textEdit.append("players with STRENGTH spec: "+str(strength)+" "+str(strength*100/playerstotal));
        self.textEdit.append("players with PLAYMAKER spec: "+str(playmaker)+" "+str(playmaker*100/playerstotal));
        self.textEdit.append("players with CROSSER spec: "+str(crosser)+" "+str(crosser*100/playerstotal));
        self.textEdit.append("players with ACROBAT spec: "+str(acrobat)+" "+str(acrobat*100/playerstotal));
        self.textEdit.append("players with TACKLING spec: "+str(tackling)+" "+str(tackling*100/playerstotal));
        self.textEdit.append("players with TACTICIAN spec: "+str(tactician)+" "+str(tactician*100/playerstotal));
        self.textEdit.append("SPECIAL statistics:");
        self.textEdit.append("players with AGILITY VERY BAD: "+str(agilm10)+" "+str(agilm10*100/playerstotal));
        self.textEdit.append("players with BALANCE VERY BAD : "+str(balam10)+" "+str(balam10*100/playerstotal));
        self.textEdit.append("players with ACCELERATION VERY BAD: "+str(accem10)+" "+str(accem10*100/playerstotal));
        self.textEdit.append("players with SPRINT SPEED VERY BAD: "+str(sprim10)+" "+str(sprim10*100/playerstotal));
        self.textEdit.append("players with JUMPION VERY BAD: "+str(jumpm10)+" "+str(jumpm10*100/playerstotal));
        self.textEdit.append("players with STAMINA VERY BAD: "+str(stamm10)+" "+str(stamm10*100/playerstotal));
        self.textEdit.append("players with STRENGTH VERY BAD: "+str(strem10)+" "+str(strem10*100/playerstotal));
        self.textEdit.append("----------------");
        self.textEdit.append("players with AGILITY  BAD: "+str(agilm35)+" "+str(agilm35*100/playerstotal));
        self.textEdit.append("players with BALANCE  BAD: "+str(balam35)+" "+str(balam35*100/playerstotal));
        self.textEdit.append("players with ACCELERATION BAD: "+str(accem35)+" "+str(accem35*100/playerstotal));
        self.textEdit.append("players with SPRINT SPEED BAD: "+str(sprim35)+" "+str(sprim35*100/playerstotal));
        self.textEdit.append("players with JUMPION BAD: "+str(jumpm35)+" "+str(jumpm35*100/playerstotal));
        self.textEdit.append("players with STAMINA BAD: "+str(stamm35)+" "+str(stamm35*100/playerstotal));
        self.textEdit.append("players with STRENGTH BAD: "+str(strem35)+" "+str(strem35*100/playerstotal));
        self.textEdit.append("----------------");
        self.textEdit.append("players with AGILITY AVG: "+str(agilm55)+" "+str(agilm55*100/playerstotal));
        self.textEdit.append("players with BALANCE  AVG: "+str(balam55)+" "+str(balam55*100/playerstotal));
        self.textEdit.append("players with ACCELERATION  AVG: "+str(accem55)+" "+str(accem55*100/playerstotal));
        self.textEdit.append("players with SPRINT SPEED  AVG: "+str(sprim55)+" "+str(sprim55*100/playerstotal));
        self.textEdit.append("players with JUMPION AVG: "+str(jumpm55)+" "+str(jumpm55*100/playerstotal));
        self.textEdit.append("players with STAMINA  AVG: "+str(stamm55)+" "+str(stamm55*100/playerstotal));
        self.textEdit.append("players with STRENGTH  AVG: "+str(strem55)+" "+str(strem55*100/playerstotal));
        self.textEdit.append("----------------");
        self.textEdit.append("players with AGILITY GOOD: "+str(agilm70)+" "+str(agilm70*100/playerstotal));
        self.textEdit.append("players with BALANCE GOOD: "+str(balam70)+" "+str(balam70*100/playerstotal));
        self.textEdit.append("players with ACCELERATION GOOD: "+str(accem70)+" "+str(accem70*100/playerstotal));
        self.textEdit.append("players with SPRINT SPEED GOOD: "+str(sprim70)+" "+str(sprim70*100/playerstotal));
        self.textEdit.append("players with JUMPION GOOD: "+str(jumpm70)+" "+str(jumpm70*100/playerstotal));
        self.textEdit.append("players with STAMINA GOOD: "+str(stamm70)+" "+str(stamm70*100/playerstotal));
        self.textEdit.append("players with STRENGTH GOOD: "+str(strem70)+" "+str(strem70*100/playerstotal));
        self.textEdit.append("----------------");
        self.textEdit.append("players with AGILITY VERY GOOD: "+str(agilm80)+" "+str(agilm80*100/playerstotal));
        self.textEdit.append("players with BALANCE VERY GOOD: "+str(balam80)+" "+str(balam80*100/playerstotal));
        self.textEdit.append("players with ACCELERATION VERY GOOD: "+str(accem80)+" "+str(accem80*100/playerstotal));
        self.textEdit.append("players with SPRINT SPEED VERY GOOD: "+str(sprim80)+" "+str(sprim80*100/playerstotal));
        self.textEdit.append("players with JUMPION VERY GOOD: "+str(jumpm80)+" "+str(jumpm80*100/playerstotal));
        self.textEdit.append("players with STAMINA VERY GOOD: "+str(stamm80)+" "+str(stamm80*100/playerstotal));
        self.textEdit.append("players with STRENGTH VERY GOOD: "+str(strem80)+" "+str(strem80*100/playerstotal));
        self.textEdit.append("----------------");
        self.textEdit.append("players with AGILITY EXCELLENT: "+str(agilm90)+" "+str(agilm90*100/playerstotal));
        self.textEdit.append("players with BALANCE EXCELLENT: "+str(balam90)+" "+str(balam90*100/playerstotal));
        self.textEdit.append("players with ACCELERATION EXCELLENT: "+str(accem90)+" "+str(accem90*100/playerstotal));
        self.textEdit.append("players with SPRINT SPEED EXCELLENT: "+str(sprim90)+" "+str(sprim90*100/playerstotal));
        self.textEdit.append("players with JUMPION EXCELLENT: "+str(jumpm90)+" "+str(jumpm90*100/playerstotal));
        self.textEdit.append("players with STAMINA EXCELLENT: "+str(stamm90)+" "+str(stamm90*100/playerstotal));
        self.textEdit.append("players with STRENGTH EXCELLENT: "+str(strem90)+" "+str(strem90*100/playerstotal));
        self.textEdit.append("OVERALL DISTRIBUTION:");
        self.textEdit.append("players in 90-99 range: "+str(tot90)+" "+str(tot90*100/playerstotal)+"%");
        self.textEdit.append("players in 80-89 range: "+str(tot80)+" "+str(tot80*100/playerstotal)+"%");
        self.textEdit.append("players in 70-79 range: "+str(tot70)+" "+str(tot70*100/playerstotal)+"%");
        self.textEdit.append("players in 60-69 range: "+str(tot60)+" "+str(tot60*100/playerstotal)+"%");
        self.textEdit.append("players in 50-59 range: "+str(tot50)+" "+str(tot50*100/playerstotal)+"%");
        self.textEdit.append("players in 40-49 range: "+str(tot40)+" "+str(tot40*100/playerstotal)+"%");
        self.textEdit.append("players in 30-39 range: "+str(tot30)+" "+str(tot30*100/playerstotal)+"%");
        self.textEdit.append("players in 20-29 range: "+str(tot20)+" "+str(tot20*100/playerstotal)+"%");
        self.textEdit.append("players in 10-19 range: "+str(tot10)+" "+str(tot10*100/playerstotal)+"%");
        self.textEdit.append("POTENTIAL DISTRIBUTION:");
        self.textEdit.append("players in 90-99 range: "+str(top90)+" "+str(top90*100/playerstotal)+"%");
        self.textEdit.append("players in 80-89 range: "+str(top80)+" "+str(top80*100/playerstotal)+"%");
        self.textEdit.append("players in 70-79 range: "+str(top70)+" "+str(top70*100/playerstotal)+"%");
        self.textEdit.append("players in 60-69 range: "+str(top60)+" "+str(top60*100/playerstotal)+"%");
        self.textEdit.append("players in 50-59 range: "+str(top50)+" "+str(top50*100/playerstotal)+"%");
        self.textEdit.append("players in 40-49 range: "+str(top40)+" "+str(top40*100/playerstotal)+"%");
        self.textEdit.append("players in 30-39 range: "+str(top30)+" "+str(top30*100/playerstotal)+"%");
        self.textEdit.append("players in 20-29 range: "+str(top20)+" "+str(top20*100/playerstotal)+"%");
        self.textEdit.append("players in 10-19 range: "+str(top10)+" "+str(top10*100/playerstotal)+"%");
        self.textEdit.append("END OF STATISTICS:");
        #print("player with id "+str(found)+" have style no. "+str(stilegiocatore)+"");
        return lista;

    def etac(self,num):
        r=int((157564-num)/365.25)
        if(r>45):
            r=26;
        return r;
        

    def trait(self,num):
        traitlist=[];
        for i in range(0,29):
            a = int(math.pow(2,i));
            s = int(num/a);
            z = s % 2;
            traitlist.append(z);
        return traitlist;

    def sommatrait(self,lis):
        tt=0;
        for i in range(0,29):
            a = int(math.pow(2,i));
            tt=tt + a*lis[i];
        return tt;
    
    def zone(self,position,ovr,tipo):
        tmp=5;
        if(tipo==0):
            if(position==1):
                tmp=random.randrange(ovr+0,ovr+9);#14
            elif(position==2):
                tmp=random.randrange(ovr-5,ovr+4);#14
            elif(position==3):
                tmp=random.randrange(ovr-10,ovr-1);#14#5
            elif(position==4):
                tmp=random.randrange(ovr-40,ovr-11);#4
            elif(position==5):
                tmp=random.randrange(ovr-55,ovr-41);#8
            elif(position==6):
                tmp=random.randrange(10,max(11,ovr-51));
        elif(tipo==1):
            if(position==1):
                tmp=random.randrange(85,90);#14
            elif(position==2):
                tmp=random.randrange(80,89);#14
            elif(position==3):
                tmp=random.randrange(70,79);#14
            elif(position==4):
                tmp=random.randrange(33,69);#14
            elif(position==5):
                tmp=random.randrange(33,55);#14
            elif(position==6):
                tmp=random.randrange(33,34);#14
        elif(tipo==2):
            if(position==1):
                tmp=random.randrange(85,90);#14
            elif(position==2):
                tmp=random.randrange(80,89);#14
            elif(position==3):
                tmp=random.randrange(70,79);#14
            elif(position==4):
                tmp=random.randrange(33,69);#14
            elif(position==5):
                tmp=random.randrange(33,55);#14
            elif(position==6):
                tmp=random.randrange(33,34);#14
        tmp=max(1,min(int(tmp),random.randrange(96,100)));
        return tmp;
    
    def SqGameplayization(self,lista):
        for rig in range(0,len(lista)):
            balltype=int(lista[rig][1]);
            ipre=int(lista[rig][61]);#1-20
            teamid=int(lista[rig][41]);
            transferbudget = int(lista[rig][53]);
            defagg = int(lista[rig][38]);
            defmen = int(lista[rig][14]);
            buspas = int(lista[rig][28]);
            busspe = int(lista[rig][52]);
            ccshot = int(lista[rig][54]);
            ccpass = int(lista[rig][56]);
            defwid = int(lista[rig][31]);
            cccros = int(lista[rig][64]);
            busdri = int(lista[rig][35]);
            buspos = int(lista[rig][49]);
            ccposi = int(lista[rig][51]);
            deflin = int(lista[rig][60]);
            #ifat = int(ipre*1);#10-75;1-20
            #ifat=int(ipre-14)*4;#juve.20 = 30, serie a= 0, cesena -16
            if(ipre-15>0):
                ifat=(ipre-15)*6;
            else:
                ifat=(ipre-15)*8;
            defagg = 40+ipre*2;#int(55+ifat+random.randrange(-5,5));#contain-closein-doublecharge
            defmen = 80;#40+ipre*2;#int(55+ifat+random.randrange(-5,5));#stayback-presslittle-pressmuch
            ccshot = 80;#40+ipre*2;#int(75+random.randrange(-5,5));#less-mixed-more shoots
            ccpass = 60;#40+ipre*2;#int(75+random.randrange(-5,5));#secure-normal-risky
            cccros = 50;#int(50+ifat+random.randrange(-5,5));#little-normal-lots
            busspe = 60;#0+ipre*2;#int(75+random.randrange(-5,5));#slow-medium-fast buildup
            buspas = 80;#80-ipre*2;#int(60-ifat+random.randrange(-5,5));#short-mixed-long passing
            busdri = 80;#50;#int(75+random.randrange(-5,5));#less-mixed-much
            defwid = 50;#int(50-ifat+random.randrange(-5,5));
            ccposi=0;
            deflin=1;
            buspos=0;
            pressingalto = [0];
            possessopalla = [0];
            contropiede = [0];
            pallalunga = [0];
            for x in pressingalto:
                if(teamid==x):#PRESSING ALTO
                    defagg = int(75);#contain-closein-doublecharge
                    defmen = int(85);#stayback-presslittle-pressmuch
                    ccshot = int(75);#less-mixed-more shoots
                    ccpass = int(75);#secure-normal-risky
                    cccros = int(50);#little-normal-lots
                    busspe = int(50);#slow-medium-fast buildup
                    buspas = int(50);#short-mixed-long passing
                    busdri = int(50);#less-mixed-much
                    defwid = int(25);
                    ccposi=0;
                    deflin=1;
                    buspos=0;
            for x in possessopalla:
                if(teamid==x):#POSSESSO PALLA
                    defagg = int(25);#contain-closein-doublecharge
                    defmen = int(50);#stayback-presslittle-pressmuch
                    ccshot = int(25);#less-mixed-more shoots
                    ccpass = int(25);#secure-normal-risky
                    cccros = int(25);#little-normal-lots
                    busspe = int(20);#slow-medium-fast buildup
                    buspas = int(20);#short-mixed-long passing
                    busdri = int(20);#less-mixed-much
                    defwid = int(50);
                    ccposi=1;
                    deflin=0;
                    buspos=1;
            for x in contropiede:
                if(teamid==x):#CONTROPIEDE
                    defagg = int(50);#contain-closein-doublecharge
                    defmen = int(10);#stayback-presslittle-pressmuch
                    ccshot = int(50);#less-mixed-more shoots
                    ccpass = int(50);#secure-normal-risky
                    cccros = int(50);#little-normal-lots
                    busspe = int(95);#slow-medium-fast buildup
                    buspas = int(50);#short-mixed-long passing
                    busdri = int(50);#less-mixed-much
                    defwid = int(60);
                    ccposi=0;
                    deflin=0;
                    buspos=0;
            for x in pallalunga:
                if(teamid==x):#pallalunga
                    defagg = int(75);#contain-closein-doublecharge
                    defmen = int(50);#stayback-presslittle-pressmuch
                    ccshot = int(75);#less-mixed-more shoots
                    ccpass = int(75);#secure-normal-risky
                    cccros = int(75);#little-normal-lots
                    busspe = int(90);#slow-medium-fast buildup
                    buspas = int(90);#short-mixed-long passing
                    busdri = int(90);#less-mixed-much
                    defwid = int(50);
                    ccposi=0;
                    deflin=1;
                    buspos=0;
            if(transferbudget>100):
                tras = int((transferbudget)/1000.0);
                tras2 = tras*1000;
            lista[rig][53] = str(tras2);
            lista[rig][38] = str(max(15,min(85,defagg)));#defaggress
            lista[rig][14] = str(max(15,min(85,defmen)));#defmentality
            lista[rig][28] = str(max(15,min(85,buspas)));#buspass
            lista[rig][52] = str(max(15,min(85,busspe)));#busspeed
            lista[rig][54] = str(max(15,min(85,ccshot)));#ccshoot
            lista[rig][56] = str(max(15,min(85,ccpass)));#ccpass
            lista[rig][31] = str(max(15,min(85,defwid)));#defwidth
            lista[rig][64] = str(max(15,min(85,cccros)));#cccross
            lista[rig][35] = str(max(15,min(85,busdri)));#busdrib
            lista[rig][49] = str(buspos);#busposition
            lista[rig][51] = str(ccposi);#ccposit
            lista[rig][60] = str(deflin);#defline
        return lista;

    def RfGameplayization(self,lista):
        for rig in range(0,len(lista)):
            #13 foulstrictness,10 style code
            stylecode = int(lista[rig][10]);
            foulstrictness = int(lista[rig][13]);
            leagueid = int(lista[rig][16]);
            stylecode = random.randrange(0,3);
            if((leagueid==13)or(leagueid==14)or(leagueid==16)or(leagueid==19)or(leagueid==31)or(leagueid==53)or(leagueid==67)or(leagueid==308)):
                foulstrictness = 2;
                stylecode = 2;
            else:
                foulstrictness = 2;
                stylecode = 2;
            lista[rig][10] = str(stylecode);
            lista[rig][13] = str(foulstrictness);
            lista[rig][16] = str(leagueid);
        return lista;

    def applylocalization(self,lista,tipo):
        for i in range(0,len(lista)):
            for j in range(0,len(lista[0])-1):
                virg = 0;
                #print(str(i) + "  " + str(j)+ " fv  "+str(lista[i][j]));
                if(tipo=="field"):
                    s = locale.str(locale.atof(lista[i][j]));
                if(tipo=="formation"):
                    if(j==47):
                        s = unicode(lista[i][j]);
                    else:
                        s = locale.atof(lista[i][j])#locale.str(locale.atof(lista[i][j]));
                b = unicode(s);
                lista[i][j] = b;
        return lista;

    def posizionatore(self,pos,ofr,dd,mm,cc,tt,aa):
        pxy=["",""];
        pos = int(pos);
        ofr = ((ofr*1))/100.0;#0a4
        #campo calcio 105x68
        #px=[0.50,0.50,0.90,0.90,0.65,0.50,0.35,0.10,0.10,0.65,0.50,0.35,0.90,0.65,0.50,0.35,0.10,0.65,0.50,0.35,0.65,0.50,0.35,0.90,0.65,0.50,0.35,0.10];
        #py=[0.08,0.10,0.30,0.20,0.15,0.13,0.15,0.20,0.30,0.40,0.38,0.40,0.55,0.50,0.48,0.50,0.55,0.60,0.58,0.60,0.80,0.78,0.80,0.80,0.85,0.83,0.85,0.80];
        #####0#####1####2####3####4###5####6####7#####8###9####10###11####12###13###14###15###16###17##18###19
        px=[0.50,0.50,0.95,0.95,0.75,0.50,0.25,0.05,0.05,0.75,0.50,0.25,0.95,0.75,0.50,0.25,0.05,0.75,0.50,0.25,0.75,0.50,0.25,0.95,0.75,0.50,0.25,0.05];
        py=[0.05,0.10,0.35,0.20,0.15,0.15,0.15,0.20,0.35,0.35,0.35,0.35,0.50,0.50,0.50,0.50,0.50,0.65,0.65,0.65,0.70,0.70,0.70,0.75,0.80,0.80,0.80,0.75];
        px[0]=0.50;
        px[20]=0.80;
        px[21]=0.60;
        px[22]=0.40;
        if(dd==1 or dd==3 or dd==5):
            px[2]=0.95;
            px[3]=0.90;
            px[4]=0.75;
            px[5]=0.50;
            px[6]=0.25;
            px[7]=0.10;
            px[8]=0.05;
        elif(dd==2 or dd==4 or dd==6):
            px[2]=0.95;
            px[3]=0.90;
            px[4]=0.65;
            px[5]=0.50;
            px[6]=0.35;
            px[7]=0.10;
            px[8]=0.05;
        if(mm==1 or mm==3):
            px[9]=0.75;
            px[10]=0.50;
            px[11]=0.25;
        elif(mm==2 or mm==4):
            px[9]=0.65;
            px[10]=0.50;
            px[11]=0.35;            
        if(cc==1 or cc==3 or cc==5):
            px[12]=0.95;
            px[13]=0.75;
            px[14]=0.50;
            px[15]=0.25;
            px[16]=0.05;
        elif(cc==2):
            px[12]=0.90;
            px[13]=0.70;
            px[14]=0.50;
            px[15]=0.30;
            px[16]=0.10;
        elif(cc==4 or cc==6):
            px[12]=0.90;
            px[13]=0.65;
            px[14]=0.50;
            px[15]=0.35;
            px[16]=0.10;
        if(tt==1 or tt==3):
            px[17]=0.75;
            px[18]=0.50;
            px[19]=0.25;
        elif(tt==2 or tt==4):
            px[17]=0.65;
            px[18]=0.50;
            px[19]=0.35;
        if(aa==1 or aa==3 or aa==5):
            px[23]=0.80;
            px[24]=0.75;
            px[25]=0.50;
            px[26]=0.25;
            px[27]=0.20;
        elif(aa==2 or aa==4 or aa==6):
            px[23]=0.85;
            px[24]=0.65;
            px[25]=0.50;
            px[26]=0.35;
            px[27]=0.15;
        #print(str(dd)+"-"+str(mm)+"-"+str(cc)+"-"+str(tt)+"-"+str(aa));
        pxy[0] = locale.str(px[pos]);
        pxy[1] = locale.str(py[pos]+ofr);
        return pxy;
        
    def assignPlayerInstruction(self,pos):
        pos = int(pos);
        istr = -2147483648+16;
        if(pos==0):
            istr = -2147483648+1073741824;
        elif(pos==2 or pos==8):
            istr = -2147483648+8;
        elif(pos==3 or pos==7):
            istr = -2147483648+8;
        elif(pos==4 or pos==5 or pos==6):
            istr = -2147483648+16;
        elif(pos==9 or pos==10 or pos==11):
            istr = -2147483648+320;
        elif(pos==13 or pos==14 or pos==15):
            istr = -2147483648+134220032;
        elif(pos==18 or pos==19 or pos==20):
            istr = -2147483648+134252544;
        elif(pos==12 or pos==16):
            istr = -2147483648+2394112;
        elif(pos==23 or pos==27):
            istr = -2147483648+2394112;
        elif(pos==20 or pos==21 or pos==22):
            istr = -2147483648+294920;
        elif(pos==24 or pos==25 or pos==26):
            istr = -2147483648+294920;
        return str(istr);
    
    def assignPlayerInstruction2(self,pos):
        pos = int(pos);
        istr = -2147483648+2;
        if(pos==0):
            istr = -2147483648+0;
        elif(pos==2 or pos==8):
            istr = -2147483648+4;
        elif(pos==3 or pos==7):
            istr = -2147483648+4;
        elif(pos==4 or pos==5 or pos==6):
            istr = -2147483648+4;
        elif(pos==9 or pos==10 or pos==11):
            istr = -2147483648+4;
        elif(pos==13 or pos==14 or pos==15):
            istr = -2147483648+4;
        elif(pos==18 or pos==19 or pos==20):
            istr = -2147483648+2;
        elif(pos==12 or pos==16):
            istr = -2147483648+2;
        elif(pos==23 or pos==27):
            istr = -2147483648+1;
        elif(pos==20 or pos==21 or pos==22):
            istr = -2147483648+1;
        elif(pos==24 or pos==25 or pos==26):
            istr = -2147483648+1;
        return str(istr);
    
    def StGameplayization(self,lista,listaps,listaid,StMx,squadre):       
        for rig in range(0,len(lista)):
            teamidts = int(lista[rig][87]);
            pos0 = int(lista[rig][122]);
            pos1 = int(lista[rig][128]);
            pos2 = int(lista[rig][88]);
            pos3 = int(lista[rig][109]);
            pos4 = int(lista[rig][99]);
            pos5 = int(lista[rig][66]);
            pos6 = int(lista[rig][38]);
            pos7 = int(lista[rig][126]);
            pos8 = int(lista[rig][46]);
            pos9 = int(lista[rig][123]);
            pos10 = int(lista[rig][30]);
            gg=0;dd=0;mm=0;cc=0;tt=0;aa=0;
            formationposition = [pos0,pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8,pos9,pos10];
            for x in formationposition:
                if(x==0):
                    gg=gg+1;
                elif(x>=2 and x<=8):
                    dd=dd+1;
                elif(x>=9 and x<=11):
                    mm=mm+1;
                elif(x>=12 and x<=16):
                    cc=cc+1
                elif(x>=17 and x<=19):
                    tt=tt+1
                elif(x>=20 and x<=27):
                    aa=aa+1                
            try:
                psposition0 = listaps[listaid.index(int(lista[rig][26]))];
            except ValueError:
                psposition0 = 7;
            try:
                psposition1 = listaps[listaid.index(int(lista[rig][37]))];
            except ValueError:
                psposition1 = 15;
            try:
                psposition2 = listaps[listaid.index(int(lista[rig][64]))];
            except ValueError:
                psposition2 = 23;
            try:
                psposition3 = listaps[listaid.index(int(lista[rig][94]))];
            except ValueError:
                psposition3 = 31;
            try:
                psposition4 = listaps[listaid.index(int(lista[rig][84]))];
            except ValueError:
                psposition4 = 39;
            try:
                psposition5 = listaps[listaid.index(int(lista[rig][54]))];
            except ValueError:
                psposition5 = 47;
            try:
                psposition6 = listaps[listaid.index(int(lista[rig][50]))];
            except ValueError:
                psposition6 = 55;
            try:
                psposition7 = listaps[listaid.index(int(lista[rig][43]))];
            except ValueError:
                psposition7 = 63;
            try:
                psposition8 = listaps[listaid.index(int(lista[rig][57]))];
            except ValueError:
                psposition8 = 71;
            try:
                psposition9 = listaps[listaid.index(int(lista[rig][28]))];
            except ValueError:
                psposition9 = 79;
            try:
                psposition10 = listaps[listaid.index(int(lista[rig][121]))];
            except ValueError:
                psposition10 = 87;
            offr = 0;
            lista[rig][13]=self.posizionatore(pos0,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][17]=self.posizionatore(pos0,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][18]=self.posizionatore(pos1,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][21]=self.posizionatore(pos1,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][3]=self.posizionatore(pos2,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][4]=self.posizionatore(pos2,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][7]=self.posizionatore(pos3,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][10]=self.posizionatore(pos3,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][11]=self.posizionatore(pos4,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][19]=self.posizionatore(pos4,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][16]=self.posizionatore(pos5,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][1]=self.posizionatore(pos5,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][0]=self.posizionatore(pos6,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][5]=self.posizionatore(pos6,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][6]=self.posizionatore(pos7,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][12]=self.posizionatore(pos7,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][8]=self.posizionatore(pos8,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][14]=self.posizionatore(pos8,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][15]=self.posizionatore(pos9,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][20]=self.posizionatore(pos9,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][2]=self.posizionatore(pos10,offr,dd,mm,cc,tt,aa)[0];
            lista[rig][9]=self.posizionatore(pos10,offr,dd,mm,cc,tt,aa)[1];
            lista[rig][96]=str(-0+int(StMx[32][psposition0]));
            lista[rig][27]=str(-0+int(StMx[32][psposition1]));
            lista[rig][129]=str(-0+int(StMx[32][psposition2]));
            lista[rig][25]=str(-0+int(StMx[32][psposition3]));
            lista[rig][89]=str(-0+int(StMx[32][psposition4]));
            lista[rig][65]=str(-0+int(StMx[32][psposition5]));
            lista[rig][73]=str(-0+int(StMx[32][psposition6]));
            lista[rig][51]=str(-0+int(StMx[32][psposition7]));
            lista[rig][61]=str(-0+int(StMx[32][psposition8]));
            lista[rig][35]=str(-0+int(StMx[32][psposition9]));
            lista[rig][24]=str(-0+int(StMx[32][psposition10]));
            ###
            #lista[rig][56]=self.assignPlayerInstruction2(pos0);
            #lista[rig][39]=self.assignPlayerInstruction2(pos1);
            #lista[rig][101]=self.assignPlayerInstruction2(pos2);
            #lista[rig][82]=self.assignPlayerInstruction2(pos3);
            #lista[rig][36]=self.assignPlayerInstruction2(pos4);
            #lista[rig][40]=self.assignPlayerInstruction2(pos5);
            #lista[rig][78]=self.assignPlayerInstruction2(pos6);
            #lista[rig][115]=self.assignPlayerInstruction2(pos7);
            #lista[rig][93]=self.assignPlayerInstruction2(pos8);
            #lista[rig][32]=self.assignPlayerInstruction2(pos9);
            lista[rig][56]=str(-2147483648+int(StMx[37][psposition0]));
            lista[rig][39]=str(-2147483648+int(StMx[37][psposition1]));
            lista[rig][101]=str(-2147483648+int(StMx[37][psposition2]));
            lista[rig][82]=str(-2147483648+int(StMx[37][psposition3]));
            lista[rig][36]=str(-2147483648+int(StMx[37][psposition4]));
            lista[rig][40]=str(-2147483648+int(StMx[37][psposition5]));
            lista[rig][78]=str(-2147483648+int(StMx[37][psposition6]));
            lista[rig][115]=str(-2147483648+int(StMx[37][psposition7]));
            lista[rig][93]=str(-2147483648+int(StMx[37][psposition8]));
            lista[rig][32]=str(-2147483648+int(StMx[37][psposition9]));
            lista[rig][80]=str(-2147483648+int(StMx[37][psposition10]));
            defagg=defmen=buspas=busspe=ccshot=ccpass=defwid=cccros=busdri=buspos=ccposi=deflin="";
            for ris in range(0,len(squadre)):
                teamid = int(squadre[ris][41]);
                if(teamid==teamidts):
                    defagg = (squadre[ris][38]);
                    defmen = (squadre[ris][14]);
                    buspas = (squadre[ris][28]);
                    busspe = (squadre[ris][52]);
                    ccshot = (squadre[ris][54]);
                    ccpass = (squadre[ris][56]);
                    defwid = (squadre[ris][31]);
                    cccros = (squadre[ris][64]);
                    busdri = (squadre[ris][35]);
                    buspos = (squadre[ris][49]);
                    ccposi = (squadre[ris][51]);
                    deflin = (squadre[ris][60]);
            lista[rig][23]=(defmen);#defmentality
            lista[rig][53]=(buspas);#buspassing
            lista[rig][60]=defwid;#defteamwidth
            lista[rig][67]=busdri;#busdribbling
            lista[rig][74]=defagg;#defaggression
            lista[rig][79]=str(-7);#tactic
            lista[rig][103]=buspos;#buspositioning
            lista[rig][106]=ccposi;#ccpositioning
            lista[rig][107]=busspe;#busbuildupdpeed
            lista[rig][108]=ccshot;#ccshooting
            lista[rig][111]=ccpass;#ccpassing
            lista[rig][118]=deflin;#defdefenderline
            lista[rig][127]=cccros;#cccrossing
            #lista[rig][28]=str(0);#position10
        return lista;
    
    def SdGameplayization(self,listadef,lista,listaps,listaid,StMx,squadre):       
        for rig in range(0,len(lista)):
            teamidts = int(listadef[rig][48]);
            pos0 = int(listadef[rig][63]);
            pos1 = int(listadef[rig][67]);
            pos2 = int(listadef[rig][49]);
            pos3 = int(listadef[rig][59]);
            pos4 = int(listadef[rig][53]);
            pos5 = int(listadef[rig][40]);
            pos6 = int(listadef[rig][30]);
            pos7 = int(listadef[rig][65]);
            pos8 = int(listadef[rig][33]);
            pos9 = int(listadef[rig][64]);
            pos10 = int(listadef[rig][26]);
            gg=0;dd=0;mm=0;cc=0;tt=0;aa=0;
            formationposition = [pos0,pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8,pos9,pos10];
            for x in formationposition:
                if(x==0):
                    gg=gg+1;
                elif(x>=2 and x<=8):
                    dd=dd+1;
                elif(x>=9 and x<=11):
                    mm=mm+1;
                elif(x>=12 and x<=16):
                    cc=cc+1
                elif(x>=17 and x<=19):
                    tt=tt+1
                elif(x>=20 and x<=27):
                    aa=aa+1 
            try:
                psposition0 = listaps[listaid.index(int(lista[rig][26]))];
            except ValueError:
                psposition0 = 7;
            try:
                psposition1 = listaps[listaid.index(int(lista[rig][37]))];
            except ValueError:
                psposition1 = 15;
            try:
                psposition2 = listaps[listaid.index(int(lista[rig][64]))];
            except ValueError:
                psposition2 = 23;
            try:
                psposition3 = listaps[listaid.index(int(lista[rig][94]))];
            except ValueError:
                psposition3 = 31;
            try:
                psposition4 = listaps[listaid.index(int(lista[rig][84]))];
            except ValueError:
                psposition4 = 39;
            try:
                psposition5 = listaps[listaid.index(int(lista[rig][54]))];
            except ValueError:
                psposition5 = 47;
            try:
                psposition6 = listaps[listaid.index(int(lista[rig][50]))];
            except ValueError:
                psposition6 = 55;
            try:
                psposition7 = listaps[listaid.index(int(lista[rig][43]))];
            except ValueError:
                psposition7 = 63;
            try:
                psposition8 = listaps[listaid.index(int(lista[rig][57]))];
            except ValueError:
                psposition8 = 71;
            try:
                psposition9 = listaps[listaid.index(int(lista[rig][28]))];
            except ValueError:
                psposition9 = 79;
            try:
                psposition10 = listaps[listaid.index(int(lista[rig][121]))];
            except ValueError:
                psposition10 = 87;
            offr = 0;
            listadef[rig][13]=self.posizionatore(pos0,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][17]=self.posizionatore(pos0,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][18]=self.posizionatore(pos1,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][21]=self.posizionatore(pos1,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][3]=self.posizionatore(pos2,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][4]=self.posizionatore(pos2,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][7]=self.posizionatore(pos3,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][10]=self.posizionatore(pos3,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][11]=self.posizionatore(pos4,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][19]=self.posizionatore(pos4,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][16]=self.posizionatore(pos5,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][1]=self.posizionatore(pos5,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][0]=self.posizionatore(pos6,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][5]=self.posizionatore(pos6,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][6]=self.posizionatore(pos7,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][12]=self.posizionatore(pos7,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][8]=self.posizionatore(pos8,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][14]=self.posizionatore(pos8,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][15]=self.posizionatore(pos9,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][20]=self.posizionatore(pos9,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][2]=self.posizionatore(pos10,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][9]=self.posizionatore(pos10,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][52]=str(-0+int(StMx[32][psposition0]));
            listadef[rig][25]=str(-0+int(StMx[32][psposition1]));
            listadef[rig][68]=str(-0+int(StMx[32][psposition2]));
            listadef[rig][24]=str(-0+int(StMx[32][psposition3]));
            listadef[rig][50]=str(-0+int(StMx[32][psposition4]));
            listadef[rig][39]=str(-0+int(StMx[32][psposition5]));
            listadef[rig][42]=str(-0+int(StMx[32][psposition6]));
            listadef[rig][34]=str(-0+int(StMx[32][psposition7]));
            listadef[rig][38]=str(-0+int(StMx[32][psposition8]));
            listadef[rig][28]=str(-0+int(StMx[32][psposition9]));
            listadef[rig][23]=str(-0+int(StMx[32][psposition10]));
            defagg=defmen=buspas=busspe=ccshot=ccpass=defwid=cccros=busdri=buspos=ccposi=deflin="";
            for ris in range(0,len(squadre)):
                teamid = int(squadre[ris][41]);
                if(teamid==teamidts):
                    defagg = (squadre[ris][38]);
                    defmen = (squadre[ris][14]);
                    buspas = (squadre[ris][28]);
                    busspe = (squadre[ris][52]);
                    ccshot = (squadre[ris][54]);
                    ccpass = (squadre[ris][56]);
                    defwid = (squadre[ris][31]);
                    cccros = (squadre[ris][64]);
                    busdri = (squadre[ris][35]);
                    buspos = (squadre[ris][49]);
                    ccposi = (squadre[ris][51]);
                    deflin = (squadre[ris][60]);
            listadef[rig][22]=str(defmen);#defmentality
            listadef[rig][35]=str(buspas);#buspassing
            listadef[rig][37]=defwid;#defteamwidth
            listadef[rig][41]=busdri;#busdribbling
            listadef[rig][43]=defagg;#defaggression
            listadef[rig][45]=str(0);#tacticid
            listadef[rig][55]=buspos;#buspos
            listadef[rig][56]=ccposi;#ccpos
            listadef[rig][57]=busspe;#busbuildup
            listadef[rig][58]=ccshot;#ccshoot
            listadef[rig][60]=ccpass;#ccpasss
            listadef[rig][62]=str(1);
            listadef[rig][66]=cccros;#cccross
            #lista[rig][28]=str(0);#position10
        return listadef;

    def FmGameplayization(self,listadef,lista,listaps,listaid,StMx):       
        for rig in range(0,len(lista)):
            teamid = int(listadef[rig][54]);
            #dd = (listadef[rig][8]);
            #cc = (listadef[rig][34]);
            #aa = (listadef[rig][30]);
            pos0 = int(listadef[rig][60]);
            pos1 = int(listadef[rig][63]);
            pos2 = int(listadef[rig][55]);
            pos3 = int(listadef[rig][58]);
            pos4 = int(listadef[rig][57]);
            pos5 = int(listadef[rig][52]);
            pos6 = int(listadef[rig][49]);
            pos7 = int(listadef[rig][62]);
            pos8 = int(listadef[rig][51]);
            pos9 = int(listadef[rig][61]);
            pos10 = int(listadef[rig][48]);
            gg=0;dd=0;mm=0;cc=0;tt=0;aa=0;
            formationposition = [pos0,pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8,pos9,pos10];
            for x in formationposition:
                if(x==0):
                    gg=gg+1;
                elif(x>=2 and x<=8):
                    dd=dd+1;
                elif(x>=9 and x<=11):
                    mm=mm+1;
                elif(x>=12 and x<=16):
                    cc=cc+1
                elif(x>=17 and x<=19):
                    tt=tt+1
                elif(x>=20 and x<=27):
                    aa=aa+1 
            try:
                psposition0 = listaps[listaid.index(int(lista[rig][26]))];
            except ValueError:
                psposition0 = 7;
            try:
                psposition1 = listaps[listaid.index(int(lista[rig][37]))];
            except ValueError:
                psposition1 = 15;
            try:
                psposition2 = listaps[listaid.index(int(lista[rig][64]))];
            except ValueError:
                psposition2 = 23;
            try:
                psposition3 = listaps[listaid.index(int(lista[rig][94]))];
            except ValueError:
                psposition3 = 31;
            try:
                psposition4 = listaps[listaid.index(int(lista[rig][84]))];
            except ValueError:
                psposition4 = 39;
            try:
                psposition5 = listaps[listaid.index(int(lista[rig][54]))];
            except ValueError:
                psposition5 = 47;
            try:
                psposition6 = listaps[listaid.index(int(lista[rig][50]))];
            except ValueError:
                psposition6 = 55;
            try:
                psposition7 = listaps[listaid.index(int(lista[rig][43]))];
            except ValueError:
                psposition7 = 63;
            try:
                psposition8 = listaps[listaid.index(int(lista[rig][57]))];
            except ValueError:
                psposition8 = 71;
            try:
                psposition9 = listaps[listaid.index(int(lista[rig][28]))];
            except ValueError:
                psposition9 = 79;
            try:
                psposition10 = listaps[listaid.index(int(lista[rig][121]))];
            except ValueError:
                psposition10 = 87;
            offr = 0;
            listadef[rig][26]=self.posizionatore(pos0,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][38]=self.posizionatore(pos0,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][40]=self.posizionatore(pos1,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][45]=self.posizionatore(pos1,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][7]=self.posizionatore(pos2,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][10]=self.posizionatore(pos2,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][17]=self.posizionatore(pos3,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][21]=self.posizionatore(pos3,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][23]=self.posizionatore(pos4,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][41]=self.posizionatore(pos4,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][37]=self.posizionatore(pos5,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][3]=self.posizionatore(pos5,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][0]=self.posizionatore(pos6,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][14]=self.posizionatore(pos6,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][15]=self.posizionatore(pos7,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][25]=self.posizionatore(pos7,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][18]=self.posizionatore(pos8,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][28]=self.posizionatore(pos8,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][33]=self.posizionatore(pos9,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][43]=self.posizionatore(pos9,offr,dd,mm,cc,tt,aa)[1];
            listadef[rig][6]=self.posizionatore(pos10,offr,dd,mm,cc,tt,aa)[0];
            listadef[rig][19]=self.posizionatore(pos10,offr,dd,mm,cc,tt,aa)[1];
            #listadef[rig][39]=str(-2147483648+int(StMx[32][psposition0]));
            listadef[rig][39]=str(-0+int(StMx[32][psposition0]));
            listadef[rig][4]=str(-0+int(StMx[32][psposition1]));
            listadef[rig][46]=str(-0+int(StMx[32][psposition2]));
            listadef[rig][2]=str(-0+int(StMx[32][psposition3]));
            listadef[rig][35]=str(-0+int(StMx[32][psposition4]));
            listadef[rig][24]=str(-0+int(StMx[32][psposition5]));
            listadef[rig][27]=str(-0+int(StMx[32][psposition6]));
            listadef[rig][16]=str(-0+int(StMx[32][psposition7]));
            listadef[rig][22]=str(-0+int(StMx[32][psposition8]));
            listadef[rig][9]=str(-0+int(StMx[32][psposition9]));
            listadef[rig][1]=str(-0+int(StMx[32][psposition10]));
            #lista[rig][28]=str(0);#position10
        return listadef;

    #Salva sul file di testo, con parametri nome del file, la prima colonna e il resto delle stats
    def Salva(self,fileo,columnname,lista):
        testo='';
        print("saved: "+str(contarighe)+" rows.");
        o = codecs.open(fileo,'w',encoding='utf-16');
        columnname = columnname+'\r\n';
        o.write(columnname);
        for rig in range(0,contarighe-1):
            testo='';
            for col in range(0,contacolonne):
                #testo = testo+str(lista[rig][col])+'\t';
                testo = testo+lista[rig][col]+'\t';
            testo = testo + '\r\n';
            '''print(testo);'''
            o.write(testo);
        o.close();
        return;
            
app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
