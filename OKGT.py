# pylint: disable=E0611
# pylint: disable=E1101
#pyi-makespec --onefile --icon=icon.ico --noconsole VEZRead.py
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,\
    QScrollArea,QSizePolicy, QTableWidgetItem,QSplitter, QFrame, QSizePolicy, QListView, QTableWidget, qApp, QAction,\
     QMessageBox,QFileDialog, QErrorMessage, QDoubleSpinBox, QSpacerItem, QLineEdit, QItemDelegate, QProgressBar,\
     QTabWidget, QComboBox
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QImage, QIcon, QTransform, QStandardItemModel,QStandardItem,\
     QDoubleValidator, QValidator, QCloseEvent, QColor
from PyQt5.QtCore import QPersistentModelIndex, Qt,  QSize, QModelIndex, QThread, pyqtSignal, QTimer

import sys
import os
import traceback

from calc_okgt import k_supports, k_conductors, main_calc


class MyValidator(QValidator):
    """ Позволяет вводить только числа """
    def __init__(self, var, parent,to=False,minus=False):
        QValidator.__init__(self, parent)
        self.minus = minus
        self.var = var
        self.to = to
        self.s = set(['0','1','2','3','4','5','6','7','8','9','.',',',''])

    def validate(self, s, pos): 
        """ проверяет привильная ли строка """   
        i=-1
        t1 = 0
        t2 = False
        t3 = 0
        for i in range(len(s)):
            if self.minus and i==0 and s[i] =="-":
                t3 += 1
                
            elif self.minus and i!=0 and s[i] =="-":
                i=-1
                break

            if self.to and i==2:
                if s[i] !="." and s[i] !="," and self.var == "duble":
                    i=-1
                    break
                elif self.var == "int":
                    i=-1
                    break
            if s[i] == ".":
                if self.var =="int":
                    i=-1
                    break
                elif self.var =="duble":
                    t1 += 1
            if s[i] == ",":
                if self.var =="int":
                    i=-1
                    break
                elif self.var =="duble":
                    t1 += 1
                    t2 = True
            if t1>1:
                i=-1
                break
            if s[i] not in self.s and not (self.minus and s[i]=="-"):
                i-=1
                break

        if s=='-':
            t2=True
        
        if i == len(s)-1:
            if t2:
                return (QValidator.Intermediate, s, pos) 
            else:
                return (QValidator.Acceptable, s, pos)
        else:
            return (QValidator.Invalid, s, pos)

    def fixup(self, s):
        """ форматирует неправильную строку """
        s1=''
        if s=="-":return ""
        t = False
        for i in s:
            if i in self.s or (self.minus and i=="-"):
                if  (i=="." or i==","):
                    if not t:
                        s1+="."
                        t = True
                else:
                    s1+=i
        s=s1
        return s

class DownloadDelegate(QItemDelegate):
    """ Переопределение поведения ячейки таблицы """
    def __init__(self, tp, parent=None):
        super(DownloadDelegate, self).__init__(parent)
        self.tp = tp
        
    def createEditor(self, parent, option, index):
        lineedit=QLineEdit(parent)
        if self.tp=="okgt_length":
            if index.column() == 3:
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        if self.tp=="okgt_single":
            if index.column() in (3,5,9,10,11):
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            if index.column() in (2,8):
                lineedit.setValidator(MyValidator("duble",lineedit,minus=True))
                return lineedit
            elif index.column() == 4:
                lineedit.setValidator(MyValidator("int",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)


        else:
            return QItemDelegate.createEditor(self, parent, option, index)

            #
        


class TableTempalte(QTableWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.closeEditorSignal = None
        self.BranchesTrig = False
        self.previousItem = ""
        self.rows = 0

        self.childrenList = {}
        self.spColums = {}
        self.spCombo = {}
        #self.nodes = set()
        self.branches = set()

        

        #self.itemEntered.connect(lambda x: print(x.text()))
        #self.cellDoubleClicked[int,int].connect(self.setPreviousItem)
        

    def setCheckBranches(self,c1,c2):
        self.BranchesTrig = True
        self.branchesCels = (c1,c2)

    def checkBranches(self,row,column,pr,nw):
        #self.rowCount()
        (c1,c2) = self.branchesCels
        n1p = pr if c1 == column else self.item(row,c1).text()
        n2p = pr if c2 == column else self.item(row,c2).text()

        n1n = nw if c1 == column else self.item(row,c1).text()
        n2n = nw if c2 == column else self.item(row,c2).text()

        if n1n!="" and n2n!="":
            self.branches.discard((n1p,n2p))
            if (n1n,n2n) in self.branches:
                n1n = n1n+"*" if c1 == column else n1n
                n2n = n2n+"*" if c2 == column else n2n
                self.item(row,column).setText(nw+"*")
            elif (n2n,n1n) in self.branches:
                n1n = n1n+"*" if c1 == column else n1n
                n2n = n2n+"*" if c2 == column else n2n
                self.item(row,column).setText(nw+"*")
            self.branches.add((n1n,n2n))

        self.recolorBrances()

    def add_branch(self):
        try:
            self.recolorBrances()
        except Exception as ex:
            print(ex)

    def remove_branch(self,row):
        (c1,c2) = self.branchesCels
        self.branches.discard((self.item(row,c1).text(),self.item(row,c2).text()))
        self.recolorBrances()
        

    def recolorBrances(self):
        (c1,c2) = self.branchesCels
        if self.rowCount() > 1:
            for i in range(self.rowCount()):
                tn1 = self.item(i,c1).text()
                tk1 = self.item(i,c2).text()
                trig = True
                for j in range(self.rowCount()):
                    tn2 = self.item(j,c1).text()
                    tk2 = self.item(j,c2).text()

                    if (tk1==tn2 or tn1==tk2) and not (tk1==tn2 and tk2==tn1) and (tn1,tk1) in self.branches and (tn2,tk2) in self.branches:
                        trig = False
                        self.item(i,c1).setBackground(QColor(255,255,255))
                        self.item(i,c2).setBackground(QColor(255,255,255))
                        break

                if trig:
                    self.item(i,c1).setBackground(QColor(255,0,0,100))
                    self.item(i,c2).setBackground(QColor(255,0,0,100))

        elif self.rowCount()==1:
            tn1 = self.item(0,c1).text()
            tk1 = self.item(0,c2).text()

            if tn1=="" or tk1=="":
                self.item(0,c1).setBackground(QColor(255,0,0,100))
                self.item(0,c2).setBackground(QColor(255,0,0,100))
            else:
                self.item(0,c1).setBackground(QColor(255,255,255))
                self.item(0,c2).setBackground(QColor(255,255,255))


        
    def setcloseEditorSignal(self,metod):
        self.closeEditorSignal = metod

    def setComboDependence(self,ind):
        for key, val in self.spCombo.items():
            if len(key)==2:
                for (colum,_) in key[1]:
                    comb = self.cellWidget(ind,colum)
                    comb.currentTextChanged.connect(lambda t, k=key, o=comb,col=colum: self.ComboChangeEvent(t,k,o,col))
                    val.add(comb)
                    self.ComboChangeEvent(comb.currentText(),key,comb,colum)
                    

    def removeComboDependence(self,ind):
        for key, val in self.spCombo.items():
            if len(key)==2:
                for (colum,_) in key[1]:
                    comb = self.cellWidget(ind,colum)
                    comb.currentTextChanged.disconnect()
                    val.discard(comb)
                    
       

    def ComboChangeEvent(self,text,key,obj,colum):
        if len(key)==2:
            for ind in range(self.rowCount()):
                if self.cellWidget(ind,colum)==obj:
                    break
            
            if len(key[0])==1:
                txt = self.item(ind,key[0][0]).text()
            elif len(key[0])>1:
                txt = key[0][:-1].join([self.item(ind,k).text() for k in key[0][:-1]])

            conformity = [1 if self.cellWidget(ind,c).currentText()==m else 0 for c,m in key[1]]

            if sum(conformity)==len(conformity):
                self.spColums[key].add(txt)
            else:
                self.spColums[key].discard(txt)

            for child in self.childrenList[key]:
                cr_t = child.currentText()
                cr_t = "Нет" if cr_t not in self.spColums[key] else cr_t
                child.clear()
                child.addItems(["Нет"]+list(self.spColums[key]))
                child.setCurrentText(cr_t)
                    
    def edit(self, index, trigger, event):
        if index.row()!=-1 and index.column()!=-1:
            self.previousItem = self.item(index.row(),index.column()).text()
        return super().edit(index, trigger, event)              

    def closeEditor(self, editor, hint):
        if self.closeEditorSignal is not None:
            self.closeEditorSignal()

        try:
            i = self.currentRow()
            j = self.currentColumn()
            now = self.currentItem().text()
            #print("afffff",self.previousItem)

            self.edit_sp(i,j,self.previousItem,now)
            self.checkBranches(i,j,self.previousItem,now)
        
        except Exception as ex:
            print(ex)
            print(traceback.format_exc())
        
        QTableWidget.closeEditor(self, editor, hint)
        


    def add_row(self):
        self.rows+=1
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1
        self.insertRow(ind)
        self.setItem(ind,0, QTableWidgetItem("Test"+str(self.rows)))
        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)
        
        
    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            self.rows-=1
            
            self.remove_sp(ind)
            
            self.removeRow(ind)
            self.selectionModel().clearSelection()
            self.setCurrentCell(-1,-1)

    def setLinkParentToChildren(self,linkList):
        self.childrenList = {i:set() for i in linkList}
        self.spColums = {i:set() for i in linkList}
        self.spCombo = {i:set() if len(i)==2 else None for i in linkList}

    

    def remove_sp(self, ind):
        for key, st in self.spColums.items():
            if len(key)==1 and len(key[0]) == 1:
                st.discard(self.item(ind,key).text())

                for child in self.childrenList[key]:
                    cr_t = "Нет" if child.currentText() not in st else child.currentText()
                    child.clear()
                    child.addItems(["Нет"]+list(self.spColums[key]))
                    child.setCurrentText(cr_t)


            elif len(key)==1 and len(key[0])>1:
                s = key[0][-1].join([self.item(ind,i).text() for i in key[:-1]])
                
                st.discard(s)

                for child in self.childrenList[key]:
                    cr_t = "Нет" if child.currentText() not in st else child.currentText()
                    child.clear()
                    child.addItems(["Нет"]+list(self.spColums[key]))
                    child.setCurrentText(cr_t)

            elif len(key)==2:
                if len(key[0])==1:
                    s = self.item(ind,key[0][0]).text()
                elif len(key[0])>1:
                    s = key[0][:-1].join([self.item(ind,k).text() for k in key[0][:-1]])

                conformity = [1 if self.cellWidget(ind,c).currentText()==m else 0 for c,m in key[1]]
                st.discard(s)

                if sum(conformity)==len(conformity):
                    st.discard(s)
                
                    for child in self.childrenList[key]:
                        cr_t = "Нет" if child.currentText() not in st else child.currentText()
                        child.clear()
                        child.addItems(["Нет"]+list(self.spColums[key]))
                        child.setCurrentText(cr_t)


    def edit_sp(self,i,j,prev,now):
        for key, st in self.spColums.items():
            if len(key)==1 and len(key[0]) == 1:
                if j == key[0][0]:
                    p = prev
                    n = now
                    if p=="" and n!="":
                        st.add(n)
                    elif p!="" and n=="":
                        st.discard(p)
                    elif p!="" and n!="":
                        st.discard(p)
                        st.add(n)

                    for child in self.childrenList[key]:
                        cr_t = n if child.currentText() == p else child.currentText()
                        cr_t = "Нет" if cr_t not in st else cr_t
                        child.clear()
                        child.addItems(["Нет"]+list(self.spColums[key]))
                        child.setCurrentText(cr_t)

            elif len(key)==1 and len(key[0])>1:
                if j in key[0][:-1]:
                    sp = [self.item(i,k).text() if k!=j else prev for k in key[0][:-1]]
                    sn = [self.item(i,k).text() if k!=j else now for k in key[0][:-1]]

                    if "" in sp and "" not in sn:
                        st.add(key[0][-1].join(sn))
                    elif "" not in sp and "" in sn:
                        st.discard(key[0][-1].join(sp))
                    elif "" not in sp and "" not in sn:
                        st.discard(key[0][-1].join(sp))
                        st.add(key[0][-1].join(sn))

                    for child in self.childrenList[key]:
                        cr_t = key[0][-1].join(sn) if child.currentText() == key[0][-1].join(sp) else child.currentText()
                        cr_t = "Нет" if cr_t not in st else cr_t
                        child.clear()
                        child.addItems(["Нет"]+list(self.spColums[key]))
                        child.setCurrentText(cr_t)

            elif len(key)==2 and len(key[0])==1:
                if j == key[0][0]:
                    p = prev
                    n = now
                    conformity = [1 if self.cellWidget(i,c).currentText()==m else 0 for c,m in key[1]]

                    if sum(conformity)==len(conformity):
                        if p=="" and n!="":
                            st.add(n)
                        elif p!="" and n=="":
                            st.discard(p)
                        elif p!="" and n!="":
                            st.discard(p)
                            st.add(n)

                        for child in self.childrenList[key]:
                            cr_t = n if child.currentText() == p else child.currentText()
                            cr_t = "Нет" if cr_t not in st else cr_t
                            child.clear()
                            child.addItems(["Нет"]+list(self.spColums[key]))
                            child.setCurrentText(cr_t)
            
            elif len(key)==2 and len(key[0])>1:
                if j in key[0][:-1]:
                    sp = [self.item(i,k).text() if k!=j else prev for k in key[0][:-1]]
                    sn = [self.item(i,k).text() if k!=j else now for k in key[0][:-1]]

                    conformity = [1 if self.cellWidget(i,c).currentText()==m else 0 for c,m in key[1]]

                    if sum(conformity)==len(conformity):
                        if "" in sp and "" not in sn:
                            st.add(key[0][-1].join(sn))
                        elif "" not in sp and "" in sn:
                            st.discard(key[0][-1].join(sp))
                        elif "" not in sp and "" not in sn:
                            st.discard(key[0][-1].join(sp))
                            st.add(key[0][-1].join(sn))

                        for child in self.childrenList[key]:
                            cr_t = key[0][-1].join(sn) if child.currentText() == key[0][-1].join(sp) else child.currentText()
                            cr_t = "Нет" if cr_t not in st else cr_t
                            child.clear()
                            child.addItems(["Нет"]+list(self.spColums[key]))
                            child.setCurrentText(cr_t)
            

    def add_child(self,key,child):
        if key in self.childrenList:
            self.childrenList[key].add(child)
            child.addItems(["Нет"]+list(self.spColums[key]))
            child.setCurrentText("Нет")

    def remove_child(self,key,child):
        if key in self.childrenList:
            self.childrenList[key].discard(child)

class UserComboBox(QComboBox):
    def __init__(self,trig, parent=None):
        super(UserComboBox, self).__init__(parent)
        self.Trig = trig

    def wheelEvent(self, *args, **kwargs):
        if self.Trig["trig"]:
            self.Trig["timer"].stop()
            self.Trig["timer"].start(500)
            return QComboBox.wheelEvent(self, *args, **kwargs)  


class OkgtNodeTable(TableTempalte):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Узел начала","Узел конца"])
        self.setColumnWidth(0,100)
        self.setColumnWidth(0,100)

        self.setCheckBranches(0,1)

        #self.setcloseEditorSignal(lambda:self.WriteTable(who_edited = "table"))
        #self.itemChanged(lambda:print("change2"))
        #self.cellClicked[int,int].connect(lambda x, y: print(x,y))
        #self.setItemDelegate(DownloadDelegate(self))

    def add_row(self):
        super().add_row()
        
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1
        self.setItem(ind,0, QTableWidgetItem(""))
        self.setItem(ind,1, QTableWidgetItem(""))
        self.add_branch()

    def remove_row(self):
        ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
        self.remove_branch(ind)
        super().remove_row()
        

class OkgtSectorTable(TableTempalte):
    def __init__(self,dataSetObj,timer,parent=None):
        super().__init__(parent)

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Ветвь","Тип","Имя участка","Длина"])
        self.setColumnWidth(0,200)
        self.setColumnWidth(1,100)
        self.setColumnWidth(2,140)
        self.setColumnWidth(3,70)
        self.dataSetObj  = dataSetObj
        self.dataSetObj.setLinkParentToChildren([((0,1," - "),)])
        self.add_cmb = dataSetObj.add_child
        self.remove_cmb = dataSetObj.remove_child
        self.timer = timer

        self.setItemDelegate(DownloadDelegate("okgt_length"))

    def add_row(self):
        super().add_row()
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1

        cmb = UserComboBox(self.timer)
        tp = UserComboBox(self.timer)
        tp.addItems(["ВЛ","Проводящий","Непроводящий"])
        self.setCellWidget(ind,0, cmb)
        self.setCellWidget(ind,1, tp)
        self.setItem(ind,2, QTableWidgetItem(""))
        self.setItem(ind,3, QTableWidgetItem(""))

        self.add_cmb(((0,1," - "),),cmb)
        try:
            self.setComboDependence(ind)

        except Exception as ex:
            print(ex)
            print(traceback.format_exc())

    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            self.removeComboDependence(ind)
            cmb = self.cellWidget(ind,0)
            self.remove_cmb(((0,1," - "),),cmb)
        super().remove_row()
        


class OkgtSingleTable(TableTempalte):
    def __init__(self,dataSetObj,timer,parent=None):
        super().__init__(parent)

        self.setColumnCount(12)
        self.setHorizontalHeaderLabels(["Имя участка","ОКГТ","X, м","Y, м","Кол. ЗУ","Rзу, Ом","Тип ЗУ","Противовес","X, м","Y, м","D, мм","Ро, Ом*м"])
        self.setColumnWidth(0,140)
        self.setColumnWidth(1,70)
        self.setColumnWidth(2,50)
        self.setColumnWidth(3,70)
        self.setColumnWidth(4,70)
        self.setColumnWidth(5,70)
        self.setColumnWidth(6,100)
        self.setColumnWidth(7,100)
        self.setColumnWidth(8,50)
        self.setColumnWidth(9,50)
        self.setColumnWidth(10,50)
        self.setColumnWidth(11,70)
        

        dataSetObj.setLinkParentToChildren([((2,),((1,"Проводящий"),))])
        self.add_cmb = dataSetObj.add_child
        self.remove_cmb = dataSetObj.remove_child
        self.timer = timer

        
        self.setItemDelegate(DownloadDelegate("okgt_single"))

    def add_row(self):
        super().add_row()
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1

        
        sector = UserComboBox(self.timer)
        self.setCellWidget(ind,0, sector)

        groundwire = UserComboBox(self.timer)
        groundwire.addItems([key for key,val in k_conductors.items() if val["Bsc"] is not None])
        self.add_cmb(((2,),((1,"Проводящий"),)),sector)
        self.setCellWidget(ind,1, groundwire)


        self.setItem(ind,2, QTableWidgetItem(""))
        self.setItem(ind,3, QTableWidgetItem(""))
        self.setItem(ind,4, QTableWidgetItem(""))
        self.setItem(ind,5, QTableWidgetItem(""))

        zytype = UserComboBox(self.timer)
        zytype.addItems(["Нет","Внутри","начиная слева","Начиная справа","Везде"])
        self.setCellWidget(ind,6, zytype)

        contorcable = QTableWidgetItem()
        contorcable.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        contorcable.setCheckState(Qt.Unchecked) 
        self.setItem(ind,7, contorcable)

        self.setItem(ind,8, QTableWidgetItem(""))
        self.setItem(ind,9, QTableWidgetItem(""))
        self.setItem(ind,10, QTableWidgetItem(""))
        self.setItem(ind,11, QTableWidgetItem(""))

        

    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            sector = self.cellWidget(ind,0)
            self.remove_cmb(((2,),((1,"Проводящий"),)),sector)
        super().remove_row()
    


class MyWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MyWindow,self).__init__(parent)

        try:
            self.path_home = os.path.expanduser("~\\Desktop\\")
        except Exception:
            self.path_home = ""

        desktop = QApplication.desktop()
        wd = desktop.width()
        hg = desktop.height()
        ww = 1000
        wh = 500
        if ww>wd: ww = int(0.7*wd)
        if wh>hg: wh = int(0.7*hg)
        x = (wd-ww)//2
        y = (hg-wh)//2
        self.setGeometry(x, y, ww, wh)

        topVBoxLayout = QVBoxLayout(self)
        mainTabWidget = QTabWidget()
        topVBoxLayout.addWidget(mainTabWidget) 
        central_widget = QWidget()
        central_widget.setLayout(topVBoxLayout)
        self.setCentralWidget(central_widget) 

        self.statusBar()
        menubar = self.menuBar()

        self.Okgt_Widget = QWidget()
        Vl_Tabs = QTabWidget()
        Ps_Widget = QWidget()
        Rpa_Tabs = QTabWidget()
        Rez_Tabs = QTabWidget()

        mainTabWidget.addTab(self.Okgt_Widget,"ОКГТ")
        mainTabWidget.addTab(Vl_Tabs,"ВЛ")
        mainTabWidget.addTab(Ps_Widget,"ПС")
        mainTabWidget.addTab(Rpa_Tabs,"РЗА")
        mainTabWidget.addTab(Rez_Tabs,"Результаты")


        self.cntr_pr = {"trig":False,"timer":QTimer()}
        self.cntr_pr["timer"].timeout.connect(self.on_timeout)
        self.cntr_pr["timer"].setSingleShot(True)


        self.okgt_tab_maker()

        exitAction = QAction( '&Выход', self) #QIcon('exit.png'),
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Выход и программы')
        exitAction.triggered.connect(lambda:self.closeEvent(QCloseEvent()))

        add_row = QAction( '&Добавить', self) #QIcon('exit.png'),
        add_row.setShortcut('Ctrl+W')
        add_row.setStatusTip('Добавить строку в таблицу')
        add_row.triggered.connect(self.Okgt_node_table.add_row)

        remove_row = QAction( '&Удалить', self) #QIcon('exit.png'),
        remove_row.setShortcut('Ctrl+E')
        remove_row.setStatusTip('Удалить строку из таблицу')
        remove_row.triggered.connect(self.Okgt_node_table.remove_row)

        add_sector = QAction( '&Добавить сектор', self) #QIcon('exit.png'),
        add_sector.setShortcut('Ctrl+S')
        add_sector.setStatusTip('Добавить строку в таблицу')
        add_sector.triggered.connect(self.Okgt_sector_table.add_row)

        remove_sector = QAction( '&Удалить сектор', self) #QIcon('exit.png'),
        remove_sector.setShortcut('Ctrl+D')
        remove_sector.setStatusTip('Удалить строку из таблицу')
        remove_sector.triggered.connect(self.Okgt_sector_table.remove_row)

        add_single = QAction( '&Добавить параметры одиночного', self) #QIcon('exit.png'),
        add_single.setShortcut('Ctrl+R')
        add_single.setStatusTip('Добавить строку в таблицу')
        add_single.triggered.connect(self.Okgt_single_table.add_row)

        remove_single = QAction( '&Удалить параметры одиночного', self) #QIcon('exit.png'),
        remove_single.setShortcut('Ctrl+T')
        remove_single.setStatusTip('Удалить строку из таблицу')
        remove_single.triggered.connect(self.Okgt_single_table.remove_row)


        #self.Okgt_sector_table


        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(add_row)
        fileMenu.addAction(remove_row)
        fileMenu.addAction(add_sector)
        fileMenu.addAction(remove_sector)
        fileMenu.addAction(add_single)
        fileMenu.addAction(remove_single)


    def on_timeout(self):
        self.cntr_pr["trig"] = False

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.cntr_pr["trig"] = True
            self.cntr_pr["timer"].start(500)
            
    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_Control:
            self.cntr_pr["trig"] = False



    def okgt_tab_maker(self):
        self.Okgt_node_table = OkgtNodeTable()
        self.Okgt_sector_table = OkgtSectorTable(self.Okgt_node_table,self.cntr_pr)
        self.Okgt_single_table = OkgtSingleTable(self.Okgt_sector_table,self.cntr_pr)

        
        
        
        
        okgt_spltV = QSplitter(Qt.Vertical)
        okgt_spltV.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        okgt_spltV.addWidget(self.Okgt_node_table)
        okgt_spltV.addWidget(self.Okgt_sector_table)
        okgt_spltV.addWidget(self.Okgt_single_table)
        okgt_spltV.setStretchFactor(1, 3) 
        okgt_spltV.setStretchFactor(3, 1) 

        
        okgt_vbl = QVBoxLayout()
        okgt_vbl.addWidget(okgt_spltV)
        self.Okgt_Widget.setLayout(okgt_vbl)

        
       
        


        #self.TWGr.addTab(self.Tabs[self.vkl],self.nm_ivl[i]) # Добавляем закладку в QTabWidget
    def closeEvent(self, event):
        Message = QMessageBox(QMessageBox.Question,  'Выход из программы',
            "Вы дейстивлеьно хотите выйти?", parent=self)
        Message.addButton('Да', QMessageBox.YesRole)
        Message.addButton('Нет', QMessageBox.NoRole)
        #Message.addButton('Сохранить', QMessageBox.ActionRole)
        reply = Message.exec()
        if reply == 0:  
            qApp.quit()
        elif reply == 1:
            event.ignore()


if __name__=='__main__':
    app=QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())