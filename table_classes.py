# pylint: disable=E0611
# pylint: disable=E1101
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QItemDelegate, QComboBox, QLineEdit,\
    QCheckBox, QWidget, QHBoxLayout, QButtonGroup, QSizePolicy, QDialog, QVBoxLayout,QDialogButtonBox,\
    QLabel, QGridLayout, QLayout
from PyQt5.QtGui import  QValidator,  QColor, QBrush
from PyQt5.QtCore import Qt

from calc_okgt import k_supports, k_conductors

import traceback


#tableWidget.setSpan(3, 0, 3, 1)  

def traceback_erors(func):
    def wrapper(*args, **kwargs):
        try:
            return_value = func(*args, **kwargs)
        except Exception:
            print(args, kwargs)
            print(traceback.format_exc())

        return return_value

    return wrapper


class CustomTableWidgetItem(QTableWidgetItem):
    def text(self):
        return QTableWidgetItem.text(self).strip()

class CustomButtonGroup(QButtonGroup):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.buttonPressed.connect(self.startEmpty)
        self.buttonReleased.connect(self.endEmpty)
        self.ex = False
    def startEmpty(self, obj):
        st = obj.checkState()
        if st == Qt.Checked:
            self.setExclusive(False)
            self.ex = True 
    def endEmpty(self, obj):
        if self.ex:
            self.setExclusive(True)
            self.ex = False
    


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

        elif self.tp=="okgt_single":
            if index.column() in (3,5,9,10,11):
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            elif index.column() in (2,8):
                lineedit.setValidator(MyValidator("duble",lineedit,minus=True))
                return lineedit
            elif index.column() == 4:
                lineedit.setValidator(MyValidator("int",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        elif self.tp=="PS":
            if index.column() == 1:
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        elif self.tp=="vl_sector": 
            if index.column() in (2,3):
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            elif index.column() in (4,5):
                lineedit.setValidator(MyValidator("int",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        elif self.tp in ("vl_conductors","vl_phases","vl_supports","vl_groundwires"): 
            if index.column() in (1,2):
                lineedit.setValidator(MyValidator("int",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        elif self.tp == "vl_ps": 
            if index.column() == 3:
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        elif self.tp=="vl_grounded": 
            if index.column() in (1,2):
                lineedit.setValidator(MyValidator("int",lineedit,minus=False))
                return lineedit
            elif index.column() in (4,):
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        elif self.tp=="vl_countercables": 
            if index.column() in (1,2):
                lineedit.setValidator(MyValidator("int",lineedit,minus=False))
                return lineedit
            elif index.column() in (3,):
                lineedit.setValidator(MyValidator("duble",lineedit,minus=True))
                return lineedit
            elif index.column() in (4,5,6):
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        elif self.tp=="vl_commonchains": 
            if index.column() in (1,2,5,6):
                lineedit.setValidator(MyValidator("int",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        elif self.tp=="SCLine":
            if index.column() == 0:
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            elif index.column() == 1:
                lineedit.setValidator(MyValidator("duble",lineedit,minus=True))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        elif self.tp["tp"]=="RPASettings":
            if index.column() in (0,1):
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            elif index.column() > 1 and self.tp["relative"]:
                lineedit.setValidator(MyValidator("duble",lineedit,minus=True))
                return lineedit
            elif index.column() > 1 and not self.tp["relative"]:
                lineedit.setValidator(MyValidator("duble",lineedit,minus=False))
                return lineedit
            else: 
                return QItemDelegate.createEditor(self, parent, option, index)

        else:
            return QItemDelegate.createEditor(self, parent, option, index)


        #{"tp":"RPASettings","relative":True}



class TableTempalte(QTableWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.closeEditorSignal = None
        self.BranchesTrig = False
        self.UniqueTrig = False
        self.previousItem = ""
        self.rows = 0

        self.childrenList = {}
        self.spColums = {}
        self.spCombo = {}
        #self.nodes = set()
        self.branches = set()
        self.UniqueDct = {}

        self.ComboConnections = set()

        

        #self.itemEntered.connect(lambda x: print(x.text()))
        #self.cellDoubleClicked[int,int].connect(self.setPreviousItem)
        
    #@traceback_erors
    def setCheckBranches(self,c1,c2):
        self.BranchesTrig = True
        self.branchesCels = (c1,c2)

    def setUniqueNamesColumn(self,lst):
        self.UniqueTrig = True
        self.UniqueDct = {i:set() for i in lst}

    def checkUnique(self,row,column,pr,nw):
        #print("unique")
        if column in self.UniqueDct:
            self.UniqueDct[column].discard(pr)
            if nw == "" or nw in self.UniqueDct[column]:
                self.item(row,column).setText(pr)
            else:
                self.UniqueDct[column].add(nw)


    def add_Unique(self,row):
        for col, st in self.UniqueDct.items():
            s = self.item(row,col).text()
            if s in st:
                self.item(row,col).setText("")
            else:
                st.add(s)
        

    def remove_Unique(self,row):
        for col, st in self.UniqueDct.items():
            s = self.item(row,col).text()
            st.discard(s)
        
    #@traceback_erors
    def checkBranches(self,row,column,pr,nw):
        if self.BranchesTrig:
            (c1,c2) = self.branchesCels
            n1p = pr if c1 == column else self.item(row,c1).text()
            n2p = pr if c2 == column else self.item(row,c2).text()

            n1n = nw if c1 == column else self.item(row,c1).text()
            n2n = nw if c2 == column else self.item(row,c2).text()

            self.branches.discard((n1p,n2p))
            if n1n!="" and n2n!="":
                if (n1n,n2n) not in self.branches and (n2n,n1n) not in self.branches:
                    self.branches.add((n1n,n2n))
                else:
                    self.item(row,column).setText("")

            self.recolorBrances()

    #@traceback_erors   
    def add_branch(self,row):
        if self.BranchesTrig:
            (c1,c2) = self.branchesCels
            n = self.item(row,c1).text()
            k = self.item(row,c2).text()

            if n!="" and k!="":
                if (n,k) not in self.branches and (k,n) not in self.branches:
                    self.branches.add((n,k))
                else:
                    self.item(row,c2).setText("")

            self.recolorBrances()
      
    #@traceback_erors
    def remove_branch(self,row):
        if self.BranchesTrig and row>-1:
            (c1,c2) = self.branchesCels
            self.branches.discard((self.item(row,c1).text(),self.item(row,c2).text()))
            self.recolorBrances()   

    #@traceback_erors
    def recolorBrances(self):
        if self.BranchesTrig:
            (c1,c2) = self.branchesCels
            nodes = {}
            for (n,k) in self.branches:
                nodes[n] = 0
                nodes[k] = 0
            
            lst = []
            for i in range(self.rowCount()):
                tn1 = self.item(i,c1).text()
                tk1 = self.item(i,c2).text()
                if (tn1,tk1) in self.branches:
                    lst.append((tn1,tk1))

            t = [False]*len(lst)

            def rcrs(lst,t,nd,st,p,f_one):
                count = 0
                for i,(n,k) in enumerate(lst):
                    if p == n and k != st and nd[k] == 0:
                        if f_one and count==0 and n==st:
                            count += 1
                            t[i] = True
                            nd[k]+=1
                            rcrs(lst,t,nd,st,k,f_one)
                        elif f_one and n!=st:
                            t[i] = True
                            nd[k]+=1
                            rcrs(lst,t,nd,st,k,f_one)
                        elif not f_one:
                            t[i] = True
                            nd[k]+=1
                            rcrs(lst,t,nd,st,k,f_one)
            
            if len(lst)>0:
                rcrs(lst,t,nodes,lst[0][0],lst[0][0],True)

            dd = {i:j for i,j in zip(lst,t)}
                    
            for i in range(self.rowCount()):
                tn1 = self.item(i,c1).text()
                tk1 = self.item(i,c2).text()

                if dd.get((tn1,tk1),False):
                    self.item(i,c1).setBackground(QColor(255,255,255))
                    self.item(i,c2).setBackground(QColor(255,255,255))
                    
                elif not dd.get((tn1,tk1),False):
                    self.item(i,c1).setBackground(QColor(255,0,0,100))
                    self.item(i,c2).setBackground(QColor(255,0,0,100))
        
    #@traceback_erors               
    def setcloseEditorSignal(self,metod):
        self.closeEditorSignal = metod
        
    #@traceback_erors
    def setComboDependence(self,ind):
        exist_connects = set()
        for key, val in self.spCombo.items():
            if len(key)==2:
                for (colum,_) in key[1]:
                    comb = self.cellWidget(ind,colum)
                    if colum not in exist_connects and comb not in self.ComboConnections:
                        comb.currentTextChanged.connect(lambda t, k=key, o=comb,col=colum: self.ComboChangeEvent(t,o,col))
                        exist_connects.add(colum)
                        self.ComboConnections.add(comb)
                    val.add(comb)
                    self.ComboChangeEvent(comb.currentText(),comb,colum)
                               
    #@traceback_erors
    def removeComboDependence(self,ind):
        for key, val in self.spCombo.items():
            if len(key)==2:
                for (colum,_) in key[1]:
                    comb = self.cellWidget(ind,colum)
                    if comb in self.ComboConnections:
                        comb.currentTextChanged.disconnect()
                        self.ComboConnections.discard(comb)
                    val.discard(comb)
         
       
    #@traceback_erors
    def ComboChangeEvent(self,text,obj,colum):
        for key in self.spCombo:
            if len(key)==2:
                for ind in range(self.rowCount()):
                    if self.cellWidget(ind,colum)==obj:
                        break
                
                if len(key[0])==1:
                    txt = self.item(ind,key[0][0]).text()
                    tr = txt == ""
                elif len(key[0])>1:
                    txt = key[0][:-1].join([self.item(ind,k).text() for k in key[0][:-1]])
                    tr = sum([self.item(ind,k).text()=="" for k in key[0][:-1]])>0

                if not tr:

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
               
    #@traceback_erors               
    def edit(self, index, trigger, event):
        
        if index.row()!=-1 and index.column()!=-1:
            if self.item(index.row(),index.column()) is not None:
                self.previousItem = self.item(index.row(),index.column()).text()
            else:
                self.previousItem = ""
        return super().edit(index, trigger, event) 

               
    #@traceback_erors
    def closeEditor(self, editor, hint):
        if self.closeEditorSignal is not None:
            self.closeEditorSignal()
        
        i = self.currentRow()
        j = self.currentColumn()
        now = self.currentItem().text()       
        self.checkUnique(i,j,self.previousItem,now)
        #self.previousItem = now
        now = self.currentItem().text()
        
        self.edit_sp(i,j,self.previousItem,now)
        self.checkBranches(i,j,self.previousItem,now)
        
        
        
        QTableWidget.closeEditor(self, editor, hint)
        

    #@traceback_erors
    def add_row(self):
        self.rows+=1
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1
        self.insertRow(ind)
        
                
        
    #@traceback_erors  
    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            self.rows-=1

            self.remove_Unique(ind)
            self.remove_sp(ind)
            self.removeRow(ind)
            self.selectionModel().clearSelection()
            self.setCurrentCell(-1,-1)

        
    #@traceback_erors
    def setLinkParentToChildren(self,linkList):
        for i in linkList:
            if i not in self.childrenList:
                self.childrenList[i] = set()
            if i not in self.spColums:
                self.spColums[i] = set()
            if i not in self.spCombo and len(i)==2:
                self.spCombo[i] = set()

        #self.childrenList = {i:set() for i in linkList}
        #self.spColums = {i:set() for i in linkList}
        #self.spCombo = {i:set() if len(i)==2 else None for i in linkList}

    #@traceback_erors
    def add_sp(self, ind):
        for key, st in self.spColums.items():
            if len(key)==1 and len(key[0]) == 1:
                if self.item(ind,key[0][0]).text() != "":
                    st.add(self.item(ind,key[0][0]).text())

                    for child in self.childrenList[key]:
                        cr_t = "Нет" if child.currentText() not in st else child.currentText()
                        child.clear()
                        child.addItems(["Нет"]+list(self.spColums[key]))
                        child.setCurrentText(cr_t)

            elif len(key)==1 and len(key[0])>1:
                s = key[0][-1].join([self.item(ind,i).text() for i in key[0][:-1]])
                
                if sum([self.item(ind,i).text()!="" for i in key[:-1]])==len(key[:-1]):
                    st.add(s)

                    for child in self.childrenList[key]:
                        cr_t = "Нет" if child.currentText() not in st else child.currentText()
                        child.clear()
                        child.addItems(["Нет"]+list(self.spColums[key]))
                        child.setCurrentText(cr_t)


            elif len(key)==2:
                if len(key[0])==1:
                    s = self.item(ind,key[0][0]).text()
                    tr = s!=""
                elif len(key[0])>1:
                    s = key[0][:-1].join([self.item(ind,k).text() for k in key[0][:-1]])
                    tr =  sum([self.item(ind,i).text()!="" for i in key[:-1]])==len(key[:-1])

                if tr:
                    #print(self.cellWidget(ind,1).currentText())
                    conformity = [1 if self.cellWidget(ind,c).currentText()==m else 0 for c,m in key[1]]
                    

                    if sum(conformity)==len(conformity):
                        st.add(s)
                    
                        for child in self.childrenList[key]:
                            cr_t = "Нет" if child.currentText() not in st else child.currentText()
                            child.clear()
                            child.addItems(["Нет"]+list(self.spColums[key]))
                            child.setCurrentText(cr_t)

    #@traceback_erors
    def remove_sp(self, ind):
        for key, st in self.spColums.items():
            if len(key)==1 and len(key[0]) == 1:
                st.discard(self.item(ind,key[0][0]).text())

                for child in self.childrenList[key]:
                    cr_t = "Нет" if child.currentText() not in st else child.currentText()
                    child.clear()
                    child.addItems(["Нет"]+list(self.spColums[key]))
                    child.setCurrentText(cr_t)


            elif len(key)==1 and len(key[0])>1:
                s = key[0][-1].join([self.item(ind,i).text() for i in key[0][:-1]])
                
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
                

                if sum(conformity)==len(conformity):
                    st.discard(s)
                
                    for child in self.childrenList[key]:
                        cr_t = "Нет" if child.currentText() not in st else child.currentText()
                        child.clear()
                        child.addItems(["Нет"]+list(self.spColums[key]))
                        child.setCurrentText(cr_t)

    #@traceback_erors
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
        
           
    #@traceback_erors
    def add_child(self,key,child):
        if key in self.childrenList:
            self.childrenList[key].add(child)
            child.clear()
            child.addItems(["Нет"]+list(self.spColums[key]))
            child.setCurrentText("Нет")
        
    #@traceback_erors
    def remove_child(self,key,child):
        if key in self.childrenList:
            self.childrenList[key].discard(child)
            child.clear()
            child.addItems(["Нет"])



    

class UserComboBox(QComboBox):
    def __init__(self,trig, parent=None):
        super(UserComboBox, self).__init__(parent)
        self.Trig = trig

    
    def wheelEvent(self, *args, **kwargs):
        if self.Trig["trig"]:
            self.Trig["timer"].stop()
            self.Trig["timer"].start(500)
            return QComboBox.wheelEvent(self, *args, **kwargs)
   


class NodeTable(TableTempalte):
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
        self.setItem(ind,0, CustomTableWidgetItem(""))
        self.setItem(ind,1, CustomTableWidgetItem(""))
        self.add_branch(ind)

        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)

    def remove_row(self):
        ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
        self.remove_branch(ind)
        super().remove_row()

    def write_table(self,info,vl=False):
        self.clear_table()
        for i, (n,k) in enumerate((info["branches"] if vl else info).keys()):
            self.add_row()
            self.item(i,0).setText(n)
            self.item(i,1).setText(k)
            self.add_branch(i)

    def clear_table(self):
        for _ in range(self.rowCount()):
            self.remove_row()

    def read_table(self):
        lst = []
        for i in range(self.rowCount()):
            n = self.item(i,0).text()
            k = self.item(i,1).text()
            if n!="" and k!="":
                lst.append((n,k))

        return lst
        

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
        self.separator = " - "
        self.dataSetObj.setLinkParentToChildren([((0,1,self.separator),)])
        self.add_cmb = dataSetObj.add_child
        self.remove_cmb = dataSetObj.remove_child
        self.timer = timer

        self.setItemDelegate(DownloadDelegate("okgt_length"))

        self.setUniqueNamesColumn([2])

        
        self.type_dct = {"VL":"ВЛ","single_conductive":"Проводящий","single_dielectric":"Непроводящий"}

    #@traceback_erors
    def add_row(self):
        super().add_row()
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1

        cmb = UserComboBox(self.timer)
        tp = UserComboBox(self.timer)
        tp.addItems([i for i in self.type_dct.values()])
        self.setCellWidget(ind,0, cmb)
        self.setCellWidget(ind,1, tp)
        self.setItem(ind,2, CustomTableWidgetItem(""))
        self.setItem(ind,3, CustomTableWidgetItem(""))
        
        self.add_Unique(ind)

        self.add_cmb(((0,1,self.separator),),cmb)
        
        self.setComboDependence(ind)

        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)

        

    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            
            self.removeComboDependence(ind)
            cmb = self.cellWidget(ind,0)
            self.remove_cmb(((0,1,self.separator),),cmb)
        super().remove_row()


    def write_table(self,okgt_info):
        self.clear_table()
        for i in range(self.dataSetObj.rowCount()):
            self.dataSetObj.add_sp(i)
        i=0
        for (n,k), val in okgt_info.items():
            for item in val:
                self.add_row()
                
                self.cellWidget(i,0).setCurrentText(self.separator.join((n,k)))
                self.cellWidget(i,1).setCurrentText(self.type_dct.get(item["type"],"ВЛ"))
                self.item(i,2).setText(item["name"])
                self.item(i,3).setText(str("" if item["length"] is None else item["length"]))

                self.add_Unique(i)

                i+=1
        
        

    def clear_table(self):
        for _ in range(self.rowCount()):
            self.remove_row()

    def read_table(self,lst):
        type_dct = {j:i for i,j in self.type_dct.items()}
        dct = {}
        for key in lst:
            s = self.separator.join(key)
            dct[key] = []
            for i in range(self.rowCount()):
                if s == self.cellWidget(i,0).currentText():
                    dct[key].append({
                        "type":type_dct[self.cellWidget(i,1).currentText()],
                        "name":self.item(i,2).text(),
                        "length": None if self.item(i,3).text()=="" else float(self.item(i,3).text())
                    })

            if dct[key] == []:
                del dct[key]
        return dct



class VlSectorTable(TableTempalte):
    def __init__(self,NodeObj,SectorObj,timer,parent=None):
        super().__init__(parent)

        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["Ветвь","Участок ОКГТ","Lн, км","Lк, км","Оп. нач.","Оп. конц."])    

        self.NodeObj = NodeObj
        self.SectorObj = SectorObj
        self.timer = timer

        self.separator = " - "
        self.NodeObj.setLinkParentToChildren([((0,1,self.separator),)])
        self.SectorObj.setLinkParentToChildren([((2,),((1,"ВЛ"),))])   

        self.setItemDelegate(DownloadDelegate("vl_sector"))   

    def add_row(self):
        super().add_row()
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1

        branch = UserComboBox(self.timer)
        okgt_sector = UserComboBox(self.timer)
        
        self.setCellWidget(ind,0, branch)
        self.setCellWidget(ind,1, okgt_sector)
        self.setItem(ind,2, CustomTableWidgetItem(""))
        self.setItem(ind,3, CustomTableWidgetItem(""))
        self.setItem(ind,4, CustomTableWidgetItem(""))
        self.setItem(ind,5, CustomTableWidgetItem(""))
        
        self.NodeObj.add_child(((0,1,self.separator),),branch)
        self.SectorObj.add_child(((2,),((1,"ВЛ"),)),okgt_sector)

        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)
        
    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            branch = self.cellWidget(ind,0)
            okgt_sector = self.cellWidget(ind,1)
            self.NodeObj.remove_child(((0,1,self.separator),),branch)
            self.SectorObj.remove_child(((2,),((1,"ВЛ"),)),okgt_sector)
        super().remove_row()

    def clear_table(self):
        for _ in range(self.rowCount()):
            self.remove_row()
            
    def read_table(self,lst):
        rez = []
        sep_keys = {self.separator.join(key):key for key in lst}
        for i in range(self.rowCount()):
            if self.cellWidget(i,0).currentText() in sep_keys:
                d = {
                    "type": "without_okgt" if self.cellWidget(i,1).currentText()=="Нет" else "with_okgt",
                    "link_okgt": self.cellWidget(i,1).currentText(),
                    "link_branch": sep_keys[self.cellWidget(i,0).currentText()],
                    "supportN" : None if self.item(i,4).text()=="" else int(self.item(i,4).text()),
                    "supportK" : None if self.item(i,5).text()=="" else int(self.item(i,5).text()),
                    "lengthN": None if self.item(i,2).text()=="" else float(self.item(i,2).text()),
                    "lengthK": None if self.item(i,3).text()=="" else float(self.item(i,3).text()),
                }
                if d["type"] == "without_okgt":
                    ln, lk = self.item(i,2).text(), self.item(i,3).text()
                    d["length"] = abs(float(lk)-float(ln)) if ln!="" and lk!="" else None
                
                rez.append(d)
        return {"sectors":rez}
    #@traceback_erors
    def write_table(self, vl_info):
        self.clear_table()
        for i in range(self.NodeObj.rowCount()):
            self.NodeObj.add_sp(i)
        for i in range(self.SectorObj.rowCount()):
            self.SectorObj.add_sp(i)
        
        for i, sector in enumerate(vl_info["sectors"]):
            self.add_row()
            
            self.cellWidget(i,0).setCurrentText(self.separator.join(sector["link_branch"]))
            self.cellWidget(i,1).setCurrentText(sector.get("link_okgt","Нет"))
            
            self.item(i,4).setText(str("" if sector["supportN"] is None else sector["supportN"]))
            self.item(i,5).setText(str("" if sector["supportK"] is None else sector["supportK"]))

            if "lengthN" in sector and "lengthK" in sector:
                self.item(i,2).setText(str("" if sector["lengthN"] is None else sector["lengthN"]))
                self.item(i,3).setText(str("" if sector["lengthK"] is None else sector["lengthK"]))
            else:
                self.item(i,2).setText("0")
                self.item(i,3).setText(str("" if sector["length"] is None else sector["length"]))


class VlPsParamsTable(TableTempalte):
    #@traceback_erors
    def __init__(self,NodeObj,PSObj,timer,parent=None):
        super().__init__(parent)     

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Ветвь","ПС","Сторона","L, км"])   

        self.NodeObj = NodeObj
        self.PSObj = PSObj
        
        self.timer = timer

        self.separator = " - "
        self.NodeObj.setLinkParentToChildren([((0,1,self.separator),)])
        self.PSObj.setLinkParentToChildren([((0,),)])
          
        self.setItemDelegate(DownloadDelegate("vl_ps"))

    def add_row(self):
        super().add_row()
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1

        branch = UserComboBox(self.timer)
        self.NodeObj.add_child(((0,1,self.separator),),branch)
        self.setCellWidget(ind,0, branch)

        ps = UserComboBox(self.timer)
        self.PSObj.add_child(((0,),),ps)
        self.setCellWidget(ind,1, ps)

        side = UserComboBox(self.timer)
        side.addItems(["Слева","Справа"])
        self.setCellWidget(ind,2, side)

        self.setItem(ind,3, CustomTableWidgetItem(""))

        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)

    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            branch = self.cellWidget(ind,0)
            ps = self.cellWidget(ind,1)
            self.NodeObj.remove_child(((0,1,self.separator),),branch)
            self.PSObj.remove_child(((0,),),ps)
        super().remove_row()

    def clear_table(self):
        for _ in range(self.rowCount()):
            self.remove_row()
    
    #@traceback_erors
    def read_table(self,lst):
        rez = []
        sep_keys = {self.separator.join(key):key for key in lst}
        for i in range(self.rowCount()):
            if self.cellWidget(i,0).currentText() in sep_keys and self.cellWidget(i,1).currentText()!="Нет":
                d = { 
                    "link_branch": sep_keys[self.cellWidget(i,0).currentText()],
                    "PS":self.cellWidget(i,1).currentText(),
                    "side": "left" if self.cellWidget(i,2).currentText() == "Слева" else "right",
                    "length": None if self.item(i,3).text()=="" else float(self.item(i,3).text()),
                } 
                rez.append(d)
        branches = {key:{} for key in lst}
        PSs = [{"PS_name":i["PS"],"length":i["length"]} for i in rez]

        for branch, info in branches.items():
            current_ps = list(filter(lambda x: x["link_branch"] == branch, rez))
            if len(current_ps)==2:
                ps1,ps2 = current_ps[0:2]
                if (ps1["side"]=="left" and ps2["side"]=="right") or (ps1["side"]=="right" and ps2["side"]=="left"):
                    info["PS"] = "both"
                    info["PS_name_1" if ps1["side"]=="left" else "PS_name_2"] = ps1["PS"]
                    info["PS_name_1" if ps2["side"]=="left" else "PS_name_2"] = ps2["PS"]
                else:
                    info["PS"] = "not"
            elif len(current_ps)==1:
                ps = current_ps[0]
                info["PS"] = ps["side"]
                info["PS_name_1" if ps["side"]=="left" else "PS_name_2"] = ps["PS"]
            elif len(current_ps)==0:
                info["PS"] = "not"
            elif len(current_ps)>2:
                info["PS"] = "not"


        return {"branches":branches,"PSs":PSs}
    
    #@traceback_erors
    def write_table(self, vl_info):
        self.clear_table()
        for i in range(self.NodeObj.rowCount()):
            self.NodeObj.add_sp(i)
        for i in range(self.PSObj.rowCount()):
            self.PSObj.add_sp(i)

        psLength = {i["PS_name"]:i["length"] for i in vl_info["PSs"]}

        i=0
        for (n,k), data in vl_info["branches"].items():
            if data["PS"] in ("both","left"):
                self.add_row()
                self.cellWidget(i,0).setCurrentText(self.separator.join((n,k)))
                self.cellWidget(i,1).setCurrentText(data["PS_name_1"])
                self.cellWidget(i,2).setCurrentText("Слева")
                self.item(i,3).setText(str("" if psLength[data["PS_name_1"]] is None else psLength[data["PS_name_1"]]))
                i+=1

            if data["PS"] in ("both","right"):
                self.add_row()
                self.cellWidget(i,0).setCurrentText(self.separator.join((n,k)))
                self.cellWidget(i,1).setCurrentText(data["PS_name_2"])
                self.cellWidget(i,2).setCurrentText("Справа")
                self.item(i,3).setText(str("" if psLength[data["PS_name_2"]] is None else psLength[data["PS_name_2"]]))
                i+=1


class VlCommonChainsTable(TableTempalte):
    #@traceback_erors
    def __init__(self,NodeObj,VlObj,le_manager,line,timer,parent=None):
        super().__init__(parent)   

        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(["Ветвь","Оп. нач.","Оп. конц.","Название ВЛ","Ветвь ВЛ","Оп. нач. ВЛ","Оп. конц. ВЛ"]) 

        self.NodeObj = NodeObj
        self.VlObj = VlObj
        self.le_manager = le_manager
        self.line = line
        
        self.timer = timer

        self.separator = " - "
        self.NodeObj.setLinkParentToChildren([((0,1,self.separator),)])
        for branches in self.VlObj.values():
            branches["branches"].setLinkParentToChildren([((0,1,self.separator),)])

        self.setItemDelegate(DownloadDelegate("vl_commonchains"))

        self.prevComboText = {}
        self.ThisToThat = {}
        self.vlComboEventResolution = True
        self.editTableResolution = True
        self.branchComboEventResolution = True
        self.cell_links = {1:5,2:6,5:1,6:2}
        
    def TableFinding(self,text):
        for page in self.VlObj.values():
            if page['line'].text().strip() == text:
                break
        else:
            return None
        return page
        
    
    #@traceback_erors
    def add_row(self):
        super().add_row()
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1

        branch = UserComboBox(self.timer)
        self.NodeObj.add_child(((0,1,self.separator),),branch)
        self.setCellWidget(ind,0, branch)
        branch.currentTextChanged.connect(lambda t, o=branch: self.BranchChanged(t,o))

        self.setItem(ind,1, CustomTableWidgetItem(""))
        self.setItem(ind,2, CustomTableWidgetItem(""))
        
        vl_name = UserComboBox(self.timer)
        #vl_name.addItems(["Нет"])
        self.prevComboText[vl_name] = "Нет"
        self.le_manager.add_child(vl_name,self.line)
        self.setCellWidget(ind,3, vl_name)
        vl_name.currentTextChanged.connect(lambda t, o=vl_name: self.setVlBranchCombo(t,o))

        vl_branch = UserComboBox(self.timer)
        vl_branch.addItems(["Нет"])
        self.setCellWidget(ind,4, vl_branch)
        vl_branch.currentTextChanged.connect(lambda t, o=vl_branch: self.BranchChanged(t,o,own=False))

        self.setItem(ind,5, CustomTableWidgetItem(""))
        self.setItem(ind,6, CustomTableWidgetItem(""))

        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)
    
    #@traceback_erors
    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            branch = self.cellWidget(ind,0)
            self.NodeObj.remove_child(((0,1,self.separator),),branch)
            
            vl_name = self.cellWidget(ind,3)
            
            self.le_manager.remove_child(vl_name)
            vl_name.currentTextChanged.disconnect()

            for key1 in self.VlObj:
                if self.VlObj[key1]["line"].text() == vl_name.currentText():
                    break
            else:
                key1 = None

            if key1 is not None:
                self.VlObj[key1]["branches"].remove_child(((0,1,self.separator),),self.cellWidget(ind,4))

            self.remove_other_row(ind)

        super().remove_row()

    def add_other_row(self,ind,page):
        if self.vlComboEventResolution:
            table = page["params"]["commonchains"]
            table.vlComboEventResolution = False
            table.editTableResolution = False
            table.branchComboEventResolution = False

            table.add_row()
            row = table.rowCount()-1
            obj = self.cellWidget(ind,3)
            other_obj = table.cellWidget(row,3)
            other_obj.setCurrentText(self.line.text().strip())
            self.ThisToThat[obj] = (other_obj,table)
            table.ThisToThat[other_obj] = (obj,self)

            table.item(row,1).setText(self.item(ind,5).text())
            table.item(row,2).setText(self.item(ind,6).text())
            table.item(row,5).setText(self.item(ind,1).text())
            table.item(row,6).setText(self.item(ind,2).text())

            table.cellWidget(row,0).setCurrentText(self.cellWidget(ind,4).currentText())
            table.cellWidget(row,4).setCurrentText(self.cellWidget(ind,0).currentText())

            table.vlComboEventResolution = True
            table.editTableResolution = True
            table.branchComboEventResolution = True

    def remove_other_row(self,ind):
        if self.vlComboEventResolution:
            obj = self.cellWidget(ind,3)
            if obj in self.ThisToThat:
                other_obj, table = self.ThisToThat[obj]
                table.vlComboEventResolution = False
                for row in range(table.rowCount()):
                    if table.cellWidget(row,3) == other_obj:
                        break
                table.setCurrentCell(row, 1)
                table.remove_row()

                del self.ThisToThat[obj]
                del table.ThisToThat[other_obj]

                table.vlComboEventResolution = True
            


    #@traceback_erors
    def setVlBranchCombo(self,t,obj):
        for ind in range(self.rowCount()):
            if self.cellWidget(ind,3)==obj:
                break
        else:
            ind = -1
        
        prev_text = self.prevComboText[obj]
        page1 = self.TableFinding(prev_text)
        page2 = self.TableFinding(obj.currentText())

        
        if ind>-1 and page1 is None and page2 is not None:
            page2["branches"].add_child(((0,1,self.separator),),self.cellWidget(ind,4))

            self.add_other_row(ind,page2)

        elif ind>-1 and page1 is not None and page2 is not None:
            page1["branches"].remove_child(((0,1,self.separator),),self.cellWidget(ind,4))
            page2["branches"].add_child(((0,1,self.separator),),self.cellWidget(ind,4))

            self.remove_other_row(ind)
            self.add_other_row(ind,page2)

        elif ind>-1 and page1 is not None and page2 is None:
            page1["branches"].remove_child(((0,1,self.separator),),self.cellWidget(ind,4))

            self.remove_other_row(ind)

        self.prevComboText[obj] = t


    #@traceback_erors
    def BranchChanged(self,t,obj,own=True):
        if self.branchComboEventResolution:
            f,s = (0,4) if own else (4,0)
            for ind in range(self.rowCount()):
                if self.cellWidget(ind,f) == obj:
                    break

            if self.cellWidget(ind,3) in self.ThisToThat:
                other_obj, table = self.ThisToThat[self.cellWidget(ind,3)]
                table.branchComboEventResolution = False
                for row in range(table.rowCount()):
                    if table.cellWidget(row,3) == other_obj:
                        break

                other_branch = table.cellWidget(row,s)
                other_branch.setCurrentText(t)
                table.branchComboEventResolution = True


    def closeEditor(self, editor, hint):
        super().closeEditor(editor, hint)
        if self.editTableResolution:
            i1 = self.currentRow()
            if self.cellWidget(i1,3) in self.ThisToThat:
                other_obj, table = self.ThisToThat[self.cellWidget(i1,3)]
                table.editTableResolution = False
                for i2 in range(table.rowCount()):
                    if table.cellWidget(i2,3) == other_obj:
                        break

                j1 = self.currentColumn()
                j2 = self.cell_links[j1]
                
                table.item(i2,j2).setText(self.item(i1,j1).text())

                table.editTableResolution = True

    def clear_table(self):
        for _ in range(self.rowCount()):
            self.remove_row()

    #@traceback_erors
    def read_table(self, vl_name, d_lst):
        rez = []
        sep_keys = {name:{self.separator.join(key):key for key in lst} for name, lst in d_lst.items()}

        for i in range(self.rowCount()):
            if self.cellWidget(i,0).currentText() in sep_keys[vl_name]:
                d = {
                    "link_branch": sep_keys[vl_name][self.cellWidget(i,0).currentText()],
                    "supportN" : None if self.item(i,1).text()=="" else int(self.item(i,1).text()),
                    "supportK" : None if self.item(i,2).text()=="" else int(self.item(i,2).text()),
                    "other_vl_name": self.cellWidget(i,3).currentText(),
                    "other_link_branch": sep_keys[self.cellWidget(i,3).currentText()][self.cellWidget(i,4).currentText()],
                    "other_supportN" : None if self.item(i,5).text()=="" else int(self.item(i,5).text()),
                    "other_supportK" : None if self.item(i,6).text()=="" else int(self.item(i,6).text()),
                }
                
                rez.append(d)
        return {"commonchains":rez}

    #@traceback_erors
    def write_table(self, vl_info):
        self.clear_table()
        for i in range(self.NodeObj.rowCount()):
            self.NodeObj.add_sp(i)


        #self.vlComboEventResolution = False
        #self.editTableResolution = False
        #self.branchComboEventResolution = False
        
        
        for i, sector in enumerate(vl_info["commonchains"]):
            self.add_row()
            
            self.cellWidget(i,0).setCurrentText(self.separator.join(sector["link_branch"]))

            self.item(i,1).setText(str("" if sector["supportN"] is None else sector["supportN"]))
            self.item(i,2).setText(str("" if sector["supportK"] is None else sector["supportK"]))

            self.item(i,5).setText(str("" if sector["other_supportN"] is None else sector["other_supportN"]))
            self.item(i,6).setText(str("" if sector["other_supportK"] is None else sector["other_supportK"]))

            self.cellWidget(i,3).setCurrentText(sector["other_vl_name"])
            
            self.cellWidget(i,4).setCurrentText(self.separator.join(sector["other_link_branch"]))

            
   

        #self.vlComboEventResolution = True
        #self.editTableResolution = True
        #self.branchComboEventResolution = True
            
            
        


class VlParamsTable(TableTempalte):
    
    def __init__(self,NodeObj,tp_params,timer,parent=None):
        super().__init__(parent)

        self._tp_params = tp_params
        Header = ["Ветвь","Оп. нач.","Оп. конц."]

        if self._tp_params == "conductors":
            Header+=["Провод"]
        elif self._tp_params == "phases":
            Header+=["Фазировка"]
        elif self._tp_params == "supports":
            Header+=["Тип опоры"]
        elif self._tp_params == "groundwires":
            Header+=["Грозотрос №1","Грозотрос №2"]
        elif self._tp_params == "grounded":
            Header+=["Заземлён","Rзу, Ом"]
        elif self._tp_params == "countercables":
            Header+=["X, м","Y, м","D, мм","Ро, Ом*м","Подкл. к ПС"]
        else:
            raise Exception(f"atribut tp_params can't have valuse: {tp_params}")

        self.setColumnCount(len(Header))
        self.setHorizontalHeaderLabels(Header)    

        self.NodeObj = NodeObj
        
        self.timer = timer

        self.separator = " - "
        self.NodeObj.setLinkParentToChildren([((0,1,self.separator),)])
          
        self.setItemDelegate(DownloadDelegate(f"vl_{self._tp_params}"))

        self.ph = ["ABC","ACB","BCA","BAC","CAB","CBA","-ABC","-ACB","-BCA","-BAC","-CAB","-CBA"]
        self.gr_zy = {"№1":"first","№2":"second","№1 и №2":"both"}
        
        self.wd_d = {}

    @property
    def tp_params(self):
        return self._tp_params
    #@traceback_erors
    def add_row(self):
        super().add_row()
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1

        branch = UserComboBox(self.timer)
        self.NodeObj.add_child(((0,1,self.separator),),branch)
        self.setCellWidget(ind,0, branch)
        self.setItem(ind,1, CustomTableWidgetItem(""))
        self.setItem(ind,2, CustomTableWidgetItem(""))

        if self._tp_params == "conductors":
            conductor = UserComboBox(self.timer)
            conductor.addItems(["Нет"]+[key for key in k_conductors.keys()])
            self.setCellWidget(ind,3, conductor)


            #conductor.setItemData(0, QBrush(Qt.red), Qt.ForegroundRole)
            #clr = conductor.currentData(Qt.ForegroundRole).color().name()
            #conductor.setStyleSheet("QComboBox:editable{{ color: {} }}".format(clr))
            #conductor.setStyleSheet("QComboBox:editable{{ color: inherit }}")
            #conductor.setItemData(0, Qt.red, Qt.TextColorRole)
            #conductor.setItemData(0, QBrush(Qt.red), Qt.BackgroundRole)


        elif self._tp_params == "phases":
            phase = UserComboBox(self.timer)
            phase.addItems(self.ph)
            self.setCellWidget(ind,3, phase)
        elif self._tp_params == "supports":
            support = UserComboBox(self.timer)
            support.addItems(["Нет"]+[key for key in k_supports.keys()]) 
            self.setCellWidget(ind,3, support)
        elif self._tp_params == "groundwires":
            gw1 = UserComboBox(self.timer)
            gw1.addItems(["Нет"]+[key for key in k_conductors.keys()])
            gw2 = UserComboBox(self.timer)
            gw2.addItems(["Нет"]+[key for key in k_conductors.keys()])
            chb1 = QCheckBox('')
            chb2 = QCheckBox('')

            button_group = CustomButtonGroup()
            button_group.addButton(chb1)
            button_group.addButton(chb2)

            w1 = QWidget()
            layout1 = QHBoxLayout()
            layout1.addWidget(chb1)
            layout1.addWidget(gw1)
            gw1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout1.setContentsMargins(0, 0, 0, 0)
            w1.setLayout(layout1)
            
            w2 = QWidget()
            layout2 = QHBoxLayout()
            layout2.addWidget(chb2)
            layout2.addWidget(gw2)
            gw2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout2.setContentsMargins(0, 0, 0, 0)
            w2.setLayout(layout2)

            self.wd_d[w1] = (gw1,chb1,button_group)
            self.wd_d[w2] = (gw2,chb2,button_group)
            self.setCellWidget(ind,3, w1)
            self.setCellWidget(ind,4, w2)

            #self.cellWidget(ind,3).setSpacing(0)

        elif self._tp_params == "grounded":
            tp_zy = UserComboBox(self.timer)
            tp_zy.addItems([i for i in self.gr_zy])
            self.setCellWidget(ind,3, tp_zy)
            self.setItem(ind,4, CustomTableWidgetItem("30.0"))
        elif self._tp_params == "countercables":
            self.setItem(ind,3, CustomTableWidgetItem(""))
            self.setItem(ind,4, CustomTableWidgetItem(""))
            self.setItem(ind,5, CustomTableWidgetItem(""))
            self.setItem(ind,6, CustomTableWidgetItem(""))
            
            to_ps = CustomTableWidgetItem()
            to_ps.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            to_ps.setCheckState(Qt.Unchecked) 
            self.setItem(ind,7, to_ps)

        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)

    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            branch = self.cellWidget(ind,0)
            self.NodeObj.remove_child(((0,1,self.separator),),branch)

            if self._tp_params == "groundwires":
                del self.wd_d[self.cellWidget(ind,3)]
                del self.wd_d[self.cellWidget(ind,4)]
            
        super().remove_row()

    def clear_table(self):
        for _ in range(self.rowCount()):
            self.remove_row()


    def read_table(self,lst):
        rez = []
        gw_p = {(2,0):"groundwire1",(0,2):"groundwire2",(0,0):None}

        sep_keys = {self.separator.join(key):key for key in lst}
        for i in range(self.rowCount()):
            if self.cellWidget(i,0).currentText() in sep_keys:
                d_main = {
                    "link_branch": sep_keys[self.cellWidget(i,0).currentText()],
                    "supportN" : None if self.item(i,1).text()=="" else int(self.item(i,1).text()),
                    "supportK" : None if self.item(i,2).text()=="" else int(self.item(i,2).text()),
                }
                
                if self._tp_params == "conductors":
                    d_add = {"conductor":self.cellWidget(i,3).currentText()}
                elif self._tp_params == "phases":
                    d_add = {"phase":self.cellWidget(i,3).currentText()}
                elif self._tp_params == "supports":
                    d_add = {"support":self.cellWidget(i,3).currentText()}
                elif self._tp_params == "groundwires":
                    (gw1,chb1,_) = self.wd_d[self.cellWidget(i,3)]
                    (gw2,chb2,_) = self.wd_d[self.cellWidget(i,4)]
                    d_add = {
                        "is_okgt":gw_p[(chb1.checkState(),chb2.checkState())],
                        "type": "two",
                        "groundwire1": gw1.currentText() if gw1.currentText()!="Нет" else None,
                        "groundwire2": gw2.currentText() if gw2.currentText()!="Нет" else None,
                    }
                elif self._tp_params == "grounded":
                    d_add = {
                        "type":self.gr_zy[self.cellWidget(i,3).currentText()],
                        "resistance": None if self.item(i,4).text()=="" else float(self.item(i,4).text()),
                    }
                elif self._tp_params == "countercables":
                    d_add = {
                        "X_countercable": None if self.item(i,3).text()=="" else float(self.item(i,3).text()),
                        "H_countercable": None if self.item(i,4).text()=="" else float(self.item(i,4).text()),
                        "D_countercable": None if self.item(i,5).text()=="" else float(self.item(i,5).text()),
                        "ground_resistance": None if self.item(i,6).text()=="" else float(self.item(i,6).text()),
                        "connect_to_ps": True if self.item(i,7).checkState() == Qt.Checked else False,
                    }

                d_main.update([(k,v) for k,v in d_add.items()])
                
                rez.append(d_main)
        return {self._tp_params:rez}

    #@traceback_erors
    def write_table(self, vl_info):
        self.clear_table()
        for i in range(self.NodeObj.rowCount()):
            self.NodeObj.add_sp(i)
        #for i in range(self.SectorObj.rowCount()):
            #self.SectorObj.add_sp(i)
        
        gr_zy = {v:k for k,v in self.gr_zy.items()}

        for i, sector in enumerate(vl_info[self._tp_params]):
            self.add_row()
            
            self.cellWidget(i,0).setCurrentText(self.separator.join(sector["link_branch"]))
            self.item(i,1).setText(str("" if sector["supportN"] is None else sector["supportN"]))
            self.item(i,2).setText(str("" if sector["supportK"] is None else sector["supportK"]))

            if self._tp_params == "conductors": # (,"phases","supports"):
                self.cellWidget(i,3).setCurrentText(sector["conductor"])
            elif self._tp_params == "phases":
                self.cellWidget(i,3).setCurrentText(sector["phase"])
            elif self._tp_params == "supports":
                self.cellWidget(i,3).setCurrentText(sector["support"])
            elif self._tp_params == "groundwires":
                (gw1,chb1,_) = self.wd_d[self.cellWidget(i,3)]
                (gw2,chb2,_) = self.wd_d[self.cellWidget(i,4)]

                gw1.setCurrentText(sector.get("groundwire1") if sector.get("groundwire1") is not None else "Нет")
                gw2.setCurrentText(sector.get("groundwire2") if sector.get("groundwire2") is not None else "Нет")

                if sector["is_okgt"] == "groundwire1":
                    chb1.setChecked(True)
                elif sector["is_okgt"] == "groundwire2":
                    chb2.setChecked(True)
     
            elif self._tp_params == "grounded":
                self.cellWidget(i,3).setCurrentText(gr_zy[sector["type"]])
                self.item(i,4).setText(str("" if sector["resistance"] is None else sector["resistance"]))
            elif self._tp_params == "countercables":
                self.item(i,3).setText(str("" if sector["X_countercable"] is None else sector["X_countercable"]))
                self.item(i,4).setText(str("" if sector["H_countercable"] is None else sector["H_countercable"]))
                self.item(i,5).setText(str("" if sector["D_countercable"] is None else sector["D_countercable"]))
                self.item(i,6).setText(str("" if sector["ground_resistance"] is None else sector["ground_resistance"]))
                self.item(i,7).setCheckState(Qt.Checked if sector["connect_to_ps"] else Qt.Unchecked)
                
       
        

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
        self.dataSetObj = dataSetObj

        self.dataSetObj.setLinkParentToChildren([((2,),((1,"Проводящий"),)),((2,),((1,"ВЛ"),))])
        self.add_cmb = self.dataSetObj.add_child
        self.remove_cmb = self.dataSetObj.remove_child
        self.timer = timer

        self.tp_zy = {"not":"Нет","inside":"Внутри","left":"Начиная слева","right":"Начиная справа","both":"Везде"}

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


        self.setItem(ind,2, CustomTableWidgetItem(""))
        self.setItem(ind,3, CustomTableWidgetItem(""))
        self.setItem(ind,4, CustomTableWidgetItem(""))
        self.setItem(ind,5, CustomTableWidgetItem(""))

        zytype = UserComboBox(self.timer)
        zytype.addItems(list(self.tp_zy.values()))
        self.setCellWidget(ind,6, zytype)

        contorcable = CustomTableWidgetItem()
        contorcable.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        contorcable.setCheckState(Qt.Unchecked) 
        self.setItem(ind,7, contorcable)

        self.setItem(ind,8, CustomTableWidgetItem(""))
        self.setItem(ind,9, CustomTableWidgetItem(""))
        self.setItem(ind,10, CustomTableWidgetItem(""))
        self.setItem(ind,11, CustomTableWidgetItem(""))

        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)

        

    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            sector = self.cellWidget(ind,0)
            self.remove_cmb(((2,),((1,"Проводящий"),)),sector)
        super().remove_row()


    def write_table(self,okgt_info):
        self.clear_table()
        for i in range(self.dataSetObj.rowCount()):
            self.dataSetObj.add_sp(i)
        i=0
        for val in okgt_info.values():
            for item in val:
                if item["type"] == "single_conductive":
                    self.add_row()
                    self.cellWidget(i,0).setCurrentText(item["name"])
                    self.cellWidget(i,1).setCurrentText(item["groundwire"])
                    self.item(i,2).setText(str("" if item["X_cable"] is None else item["X_cable"]))
                    self.item(i,3).setText(str("" if item["H_cable"] is None else item["H_cable"]))
                    self.item(i,4).setText(str("" if item["point_grounded"] is None else item["point_grounded"]))
                    self.item(i,5).setText(str("" if item.get("point_resistance","") is None else item.get("point_resistance","")))
                    self.cellWidget(i,6).setCurrentText(self.tp_zy[item["way_grounded"]])
                    self.item(i,7).setCheckState(Qt.Checked if item["countercable"] else Qt.Unchecked)
                    self.item(i,8).setText(str("" if item.get("X_countercable","") is None else item.get("X_countercable","")))
                    self.item(i,9).setText(str("" if item.get("H_countercable","") is None else item.get("H_countercable","")))
                    self.item(i,10).setText(str("" if item.get("D_countercable","") is None else item.get("D_countercable","")))
                    self.item(i,11).setText(str("" if item.get("ground_resistance","") is None else item.get("ground_resistance","")))
                    
                    i+=1
        
        

    def clear_table(self):
        for _ in range(self.rowCount()):
            self.remove_row()

    def read_table(self, dct):
        tp_zy = {j:i for i,j in self.tp_zy.items()}
        for i in range(self.rowCount()):
            for branches in dct.values():
                for sector in branches:
                    if sector["name"]==self.cellWidget(i,0).currentText():
                        sector["groundwire"] = self.cellWidget(i,1).currentText()
                        sector["X_cable"] = None if self.item(i,2).text()=="" else float(self.item(i,2).text())
                        sector["H_cable"] = None if self.item(i,3).text()=="" else float(self.item(i,3).text())
                        sector["point_grounded"] = None if self.item(i,4).text()=="" else int(self.item(i,4).text())
                        sector["point_resistance"] = None if self.item(i,5).text()=="" else float(self.item(i,5).text())
                        sector["way_grounded"] = tp_zy[self.cellWidget(i,6).currentText()]
                        sector["countercable"] = True if self.item(i,7).checkState() == Qt.Checked else False
                        sector["X_countercable"] = None if self.item(i,8).text()=="" else float(self.item(i,8).text())
                        sector["H_countercable"] = None if self.item(i,9).text()=="" else float(self.item(i,9).text())
                        sector["D_countercable"] = None if self.item(i,10).text()=="" else float(self.item(i,10).text())
                        sector["ground_resistance"] = None if self.item(i,11).text()=="" else float(self.item(i,11).text())

        return dct
                        
                        
class PSTable(TableTempalte):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Название подстанции","Rзу, Ом"])
        self.setColumnWidth(0,140)
        self.setColumnWidth(1,70)

        self.setUniqueNamesColumn([0])

        self.setLinkParentToChildren([((0,),)])
        
        
        
        self.setItemDelegate(DownloadDelegate("PS"))

    def add_row(self):
        super().add_row()
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1
        self.setItem(ind,0, CustomTableWidgetItem(""))
        self.setItem(ind,1, CustomTableWidgetItem(""))
        self.add_Unique(ind)

        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)

    
     
    def write_table(self,ps_info):
        self.clear_table()
        for i, (ps_name,item) in enumerate(ps_info.items()):
            self.add_row()
            self.item(i,0).setText(ps_name)
            self.item(i,1).setText(str("" if item["resistance"] is None else item["resistance"]))
            self.add_Unique(i)

        
    def read_table(self):
        ps_info = {}
        for i in range(self.rowCount()):
            if self.item(i,0).text()!="":
                ps_info[self.item(i,0).text()] = {"resistance":None if self.item(i,1).text()=="" else float(self.item(i,1).text())}
                    
        return ps_info

    def clear_table(self):
        for _ in range(self.rowCount()):
            self.remove_row()




class RPASettingsTable(QTableWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setColumnCount(2)
        self.setRowCount(1)
        self.setSpan(0, 0, 1, 2)
        self.setItem(0,0, CustomTableWidgetItem("Длительность паузы АПВ, с"))
        self.item(0,0).setFlags(Qt.ItemIsEditable)
        self.setHorizontalHeaderLabels(["Iуст, кА","tуст, с"])
        self.setColumnWidth(0,90)
        self.setColumnWidth(1,90)

        self.typeDelegate = {"tp":"RPASettings","relative":True}

        self.setItemDelegate(DownloadDelegate(self.typeDelegate))


    #@traceback_erors
    def add_row(self):
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rowCount()
        self.insertRow(ind)
        
        for j in range(self.columnCount()):
            self.setItem(ind,j, CustomTableWidgetItem(""))
        
        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)

    #@traceback_erors  
    def remove_row(self):
        if self.rowCount()>1:
            ind = self.currentRow() if self.currentRow() != -1 else self.rowCount()-1

            self.removeRow(ind)
            self.selectionModel().clearSelection()
            self.setCurrentCell(-1,-1)

    #@traceback_erors 
    def setColumn(self,ln):
        c_l = self.columnCount()
        if ln != c_l-2: 
            if c_l-2<ln:
                self.setColumnCount(ln+2)
                self.setHorizontalHeaderLabels(["Iуст, кА","tуст, с"]+[f"АПВ№{i+1}" for i in range(ln)])
                for j in range(c_l,ln+2):
                    self.setColumnWidth(j,60)
                    self.setItem(0,j, CustomTableWidgetItem(""))
                    for i in range(self.rowCount()):
                        self.setItem(i,j, CustomTableWidgetItem(""))

            elif c_l-2>ln:
                self.setColumnCount(ln+2)
                
                

    #@traceback_erors
    def setRelativeState(self, trig):
        
        if trig != self.typeDelegate["relative"]:
            
            if trig:
                for i in range(1,self.rowCount()):
                    t = float(self.item(i,1).text()) if self.item(i,1).text()!='' else None
                    if t is not None:
                        for j in range(2,self.columnCount()):
                            if self.item(i,j).text()!='':
                                self.item(i,j).setText(str(round(t-float(self.item(i,j).text()),3)))
                
            else:
                
                for i in range(1,self.rowCount()):
                    t = float(self.item(i,1).text()) if self.item(i,1).text()!='' else None
                    for j in range(2,self.columnCount()):
                        if t is not None and self.item(i,j).text()!='':
                            num = round(t-float(self.item(i,j).text()),3)
                            self.item(i,j).setText(str(0 if num<0 else num))
                        elif t is None and self.item(i,j).text()!='':
                            num = float(self.item(i,j).text())
                            self.item(i,j).setText(str(0 if num<0 else num))

            self.typeDelegate["relative"] = not self.typeDelegate["relative"]


    def clear_table(self):
        for _ in range(self.rowCount()):
            self.remove_row()

    #@traceback_erors
    def write_table(self,key,rpa_info):
        self.clear_table()
        save_trig = self.typeDelegate["relative"]
        self.setRelativeState(True)

        I_yst, t_yst = rpa_info[key]["rpa_I_setting"], rpa_info[key]["rpa_time_setting"]
        for i, (I,t) in enumerate(zip(I_yst, t_yst)):
            self.add_row()
            self.item(i+1,0).setText(str("" if I is None else I))
            self.item(i+1,1).setText(str("" if t is None else t))

        self.setColumn(rpa_info[key]["arc_times"])

        arc = zip(range(2,rpa_info[key]["arc_times"]+2),rpa_info[key]["arc_setting"],rpa_info[key]["arc_pause"])

        for j, current_arc, pause in arc:
            self.item(0,j).setText(str("" if pause is None else pause))
            for i, t_arc in enumerate(current_arc):
                self.item(i+1,j).setText(str("" if t_arc is None else t_arc))

        self.setRelativeState(save_trig)
           
    #@traceback_erors    
    def read_table(self):
        save_trig = self.typeDelegate["relative"]
        self.setRelativeState(True)
        I_yst, t_yst, T_arc, T_pause = [], [], [],[]
        for i in range(1,self.rowCount()):
            I_yst.append(float(self.item(i,0).text()) if self.item(i,0).text()!='' else None)
            t_yst.append(float(self.item(i,1).text()) if self.item(i,1).text()!='' else None)

        for j in range(2,self.columnCount()):
            T_arc.append([])
            T_pause.append(float(self.item(0,j).text()) if self.item(0,j).text()!='' else None)
            for i in range(1,self.rowCount()):
                T_arc[j-2].append(float(self.item(i,j).text()) if self.item(i,j).text()!='' else None)

        
        self.setRelativeState(save_trig)
          
        return {"rpa_I_setting":I_yst,"rpa_time_setting":t_yst,"arc_setting":T_arc,"arc_pause":T_pause} #,"arc_times":len(T_arc)
        
        


class ShortCircuitLineTable(QTableWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Iкз, кА","L, км"])
        #self.setColumnWidth(0,140)
        self.PlotDataFunc = None

        self.setItemDelegate(DownloadDelegate("SCLine"))

    def setPlotDataFunc(self,func):
        self.PlotDataFunc = func

    #@traceback_erors
    def closeEditor(self, editor, hint):
        data = self.read_table(own=True)
        self.setColorMistakes(data['I_sc'], data['L_sc'])
        if self.PlotDataFunc is not None:
            self.PlotDataFunc(data)
        QTableWidget.closeEditor(self, editor, hint)
        

    #@traceback_erors
    def add_row(self):
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rowCount()
        self.insertRow(ind)

        self.setItem(ind,0, CustomTableWidgetItem(""))
        self.setItem(ind,1, CustomTableWidgetItem(""))
        
        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)
        
        
    #@traceback_erors  
    def remove_row(self):
        if self.rowCount()>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rowCount()-1

            self.removeRow(ind)
            self.selectionModel().clearSelection()
            self.setCurrentCell(-1,-1)

    def clear_table(self):
        for _ in range(self.rowCount()):
            self.remove_row()

    #@traceback_erors
    def write_table(self,key,rpa_info):
        self.clear_table()
        I_sc, L_sc = rpa_info[key]["I_sc"], rpa_info[key]["L_sc"]
        for i, (I,L) in enumerate(zip(I_sc, L_sc)):
            self.add_row()
            self.item(i,0).setText(str("" if I is None else I))
            self.item(i,1).setText(str("" if L is None else L))
            

    #@traceback_erors   
    def read_table(self, own=False):
        I_sc, L_sc = [], []
        for i in range(self.rowCount()):
            if self.item(i,0).text()!="" and self.item(i,1).text():
                I_sc.append(float(self.item(i,0).text()))
                L_sc.append(float(self.item(i,1).text()))
            elif own:
                I_sc.append(None)
                L_sc.append(None)
          
        return {"I_sc":I_sc,"L_sc":L_sc}

    #@traceback_erors
    def setColorMistakes(self, I_sc, L_sc):
        rows = self.rowCount()
        #print(I_sc, L_sc)
        if rows <= 2:
            for i in range(len(I_sc)):
                if I_sc[i] is None:
                    self.item(i,0).setBackground(QColor(255,0,0,100))
                else:
                    self.item(i,0).setBackground(QColor(255,255,255))

                if L_sc[i] is None:
                    self.item(i,1).setBackground(QColor(255,0,0,100))
                else:
                    self.item(i,1).setBackground(QColor(255,255,255))
        elif rows >= 3:
            a = [j for j in I_sc if j is not None][:2]
            b = [j for j in L_sc if j is not None][:2]

            d1 = a[1]>a[0] if len(a)==2 else None
            d2 = b[1]>b[0] if len(b)==2 else None

            c1 = (-float('inf') if d1 else float('inf')) if d1 is not None else None
            c2 = (-float('inf') if d2 else float('inf')) if d2 is not None else None

            
            for i in range(rows):
                if I_sc[i] is None:
                    self.item(i,0).setBackground(QColor(255,0,0,100))
                elif d1 is not None:
                    if (d1 and I_sc[i]>c1) or (not d1 and I_sc[i]<c1):
                        c1 = I_sc[i]
                        self.item(i,0).setBackground(QColor(255,255,255))
                    else:
                        self.item(i,0).setBackground(QColor(255,0,0,100))
                else:
                    self.item(i,0).setBackground(QColor(255,255,255))

                if L_sc[i] is None:
                    self.item(i,1).setBackground(QColor(255,0,0,100))
                elif d2 is not None:
                    if (d2 and L_sc[i]>c2) or (not d2 and L_sc[i]<c2):
                        c2 = L_sc[i]
                        self.item(i,1).setBackground(QColor(255,255,255))
                    else:
                        self.item(i,1).setBackground(QColor(255,0,0,100))
                else:
                    self.item(i,1).setBackground(QColor(255,255,255))

        



class LineEditManager():
    def __init__(self,tab):
        self.children_set = set()
        self.unique_set = set()
        self.line_edit_objs = {}
        self.tab = tab
        self.tab_pages_objs = {}
        self.children_except = {}

        
    def get_unique_name(self,text):
        lst = [i[len(text):] for i in self.unique_set if text==i[:len(text)]]
        i = 1
        while True:
            if str(i) not in lst:
                return text+str(i)
            else:
                i+=1

    def add_lineEdit(self, obj, page):
        if obj not in self.line_edit_objs:
            self.line_edit_objs[obj] = obj.text().strip()
            self.tab_pages_objs[obj] = page
            obj.textChanged.connect(lambda t,o=obj:self.editingFinished(t,o))
            if self.line_edit_objs[obj] not in self.unique_set and self.line_edit_objs[obj]!='':
                self.unique_set.add(self.line_edit_objs[obj])

            self.editChildren()
        
    #@traceback_erors
    def remove_lineEdit(self, obj):
        if obj in self.line_edit_objs:
            self.unique_set.discard(obj.text().strip())
            obj.textChanged.disconnect()
            del self.line_edit_objs[obj]
            del self.tab_pages_objs[obj]

            self.editChildren()

    #@traceback_erors
    def add_child(self,child,line=None):
        self.children_set.add(child)
        self.children_except[child] = line
        if line is not None:
            lst = list(self.unique_set-set([line.text().strip()]))
        else:
            lst = list(self.unique_set)
        child.addItems(["Нет"]+lst)
        child.setCurrentText("Нет")
        
    #@traceback_erors
    def remove_child(self,child):
        if child in self.children_except:
            self.children_set.discard(child)
            del self.children_except[child]


    def editChildren(self, pn=None):
        for child in self.children_set:
            cr_t = child.currentText()
            if pn is not None:
                cr_t = pn[1] if cr_t==pn[0] else cr_t
            cr_t = "Нет" if cr_t not in self.unique_set else cr_t
            child.clear()
            if self.children_except[child] is not None:
                lst = list(self.unique_set-set([self.children_except[child].text().strip()]))
            else:
                lst = list(self.unique_set)
            child.addItems(["Нет"]+lst)
            child.setCurrentText(cr_t)

    #@traceback_erors
    def editingFinished(self,new_text,obj):
        new_text = new_text.strip()
        old_text = self.line_edit_objs[obj]
        pn = (old_text,new_text)

        if new_text!=old_text:
            if new_text!='' and new_text not in self.unique_set:
                self.unique_set.discard(old_text)
                self.unique_set.add(new_text)
                self.line_edit_objs[obj] = new_text

                ind = self.tab.indexOf(self.tab_pages_objs[obj])
                self.tab.setTabText(ind,new_text)

                self.editChildren(pn)

            elif new_text=='' and old_text!='':
                obj.setText(old_text)

        #obj.clearFocus()
        #print("test")


class CustomDialog(QDialog):
    def __init__(self, lst, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Способ чтения")

        self.setFixedSize(180,95)
        
        vl = QVBoxLayout()

        self.cb = QComboBox()
        self.cb.addItems(lst)

        btn_box = QDialogButtonBox()
        btn_box.addButton("Столбцы 1, 2", QDialogButtonBox.ActionRole)
        btn_box.addButton("Столбцы 1, 3", QDialogButtonBox.ActionRole)

        vl.addWidget(QLabel("Лист:"))
        vl.addWidget(self.cb)
        vl.addWidget(btn_box)
        self.setLayout(vl)

        btn_box.clicked.connect(self.clickEvent)


    def clickEvent(self,btn):
        if btn.text() == "Столбцы 1, 2":
            self.done(2)
        elif btn.text() == "Столбцы 1, 3":
            self.done(3)


class SingleSupportDialog(QDialog):
    def __init__(self, le_manager, vl_liks, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setWindowTitle("КЗ в точке")

        self.le_manager = le_manager
        self.vl_liks  = vl_liks
        self.separator = " - "
        self.state_color = False
        self.rez = None

        self.setFixedSize(self.width(),self.height())
        
        vl = QVBoxLayout()

        settingsGrid = QGridLayout()
        settingsGrid.addWidget(QLabel('ВЛ:'), 0,0)
        settingsGrid.addWidget(QLabel('Ветвь:'), 1,0)
        settingsGrid.addWidget(QLabel('Фаза:'), 2,0)
        settingsGrid.addWidget(QLabel('Опора:'), 3,0)
        

        self.vl_name = QComboBox()
        self.le_manager.add_child(self.vl_name)
        self.prevVlName = "Нет"
        self.vl_name.currentTextChanged.connect(self.setVlBranchCombo)

        self.branch = QComboBox()
        self.branch.currentTextChanged.connect(self.checkSupport)

        self.phase = QComboBox()
        self.phase.addItems(["A","B","C"])
        self.dct = {"A":0,"B":1,"C":2}

        self.support = QLineEdit()
        self.support.textChanged.connect(self.checkSupport)
        self.support.setValidator(MyValidator("int",self.support,minus=False))

        #page2["branches"].add_child(((0,1,self.separator),),self.cellWidget(ind,4))
        

        settingsGrid.addWidget(self.vl_name, 0,1)
        settingsGrid.addWidget(self.branch, 1,1)
        settingsGrid.addWidget(self.phase, 2,1)
        settingsGrid.addWidget(self.support, 3,1)

        btn_box = QDialogButtonBox()
        btn_box.addButton(QDialogButtonBox.Ok)
        btn_box.addButton(QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.OkBtn)
        btn_box.rejected.connect(self.CancelBtn)

        
        vl.addLayout(settingsGrid)
        vl.addWidget(btn_box)
        self.setLayout(vl)

        #self.setFixedSize(self.size())
        
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def OkBtn(self):
        vl_name = self.vl_name.currentText()
        page = self.TableFinding(vl_name)
        n,k = None, None
        if page is not None:
            for i in range(page["branches"].rowCount()):
                n = page["branches"].item(i,0).text()
                k = page["branches"].item(i,1).text()

                if self.separator.join([n,k]) == self.branch.currentText():
                    break
            
            
            #print(vl_name,(n,k),self.state_color)
            if vl_name!='' and None not in (n,k) and self.state_color:
                self.rez = (vl_name,(n,k),int(self.support.text()),self.dct[self.phase.currentText()])
                page["branches"].remove_child(((0,1,self.separator),),self.branch)
                self.le_manager.remove_child(self.vl_name)
                self.accept()
            else:
                self.CancelBtn()
        else:
            self.CancelBtn()
            
        


    def CancelBtn(self):
        page = self.TableFinding(self.vl_name.currentText())
        if page is not None:
            page["branches"].remove_child(((0,1,self.separator),),self.branch)
        self.le_manager.remove_child(self.vl_name)
        self.reject()

    def setVlBranchCombo(self,t):
        page1 = self.TableFinding(self.prevVlName)
        page2 = self.TableFinding(self.vl_name.currentText())
        
        if page1 is None and page2 is not None:
            page2["branches"].add_child(((0,1,self.separator),),self.branch)


        elif page1 is not None and page2 is not None:
            page1["branches"].remove_child(((0,1,self.separator),),self.branch)
            page2["branches"].add_child(((0,1,self.separator),),self.branch)


        elif page1 is not None and page2 is None:
            page1["branches"].remove_child(((0,1,self.separator),),self.branch)

        self.prevVlName  = t

    def TableFinding(self,text):
        for page in self.vl_liks.values():
            if page['line'].text().strip() == text:
                break
        else:
            return None
        return page


    def checkSupport(self):
        
        page = self.TableFinding(self.vl_name.currentText())
        if page is not None:
            for i in range(page["sector"].rowCount()):
                if page["sector"].cellWidget(i,0).currentText() == self.branch.currentText() and page["sector"].cellWidget(i,1).currentText() != "Нет":
                    s = int(self.support.text()) if self.support.text()!='' else None
                    n = int(page["sector"].item(i,4).text()) if page["sector"].item(i,4).text()!='' else None
                    k = int(page["sector"].item(i,5).text()) if page["sector"].item(i,5).text()!='' else None
                    
                    if None not in (s,n,k):
                        if (n<=s<=k or n>=s>=k):
                            self.support.setStyleSheet("QLineEdit {background-color: white;}")
                            self.state_color = True
                            break
            else:
                self.support.setStyleSheet("QLineEdit {background-color: #FC9E9E;}")
                self.state_color = False
                
            

        

if __name__=='__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    """ app=QApplication(sys.argv)
    window = SingleSupportDialog()    
    window.show()    
    sys.exit(app.exec_()) """

       
        