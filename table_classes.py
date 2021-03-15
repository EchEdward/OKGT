# pylint: disable=E0611
# pylint: disable=E1101
from PyQt5.QtWidgets import  QTableWidgetItem, QTableWidget, QItemDelegate, QComboBox, QLineEdit
from PyQt5.QtGui import  QValidator,  QColor
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
            if index.column() in (2,8):
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


        else:
            return QItemDelegate.createEditor(self, parent, option, index)

            #
        


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

        

        #self.itemEntered.connect(lambda x: print(x.text()))
        #self.cellDoubleClicked[int,int].connect(self.setPreviousItem)
        
    @traceback_erors
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
        
    @traceback_erors
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

    @traceback_erors   
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
      
    @traceback_erors
    def remove_branch(self,row):
        if self.BranchesTrig and row>-1:
            (c1,c2) = self.branchesCels
            self.branches.discard((self.item(row,c1).text(),self.item(row,c2).text()))
            self.recolorBrances()   

    @traceback_erors
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
        
    @traceback_erors               
    def setcloseEditorSignal(self,metod):
        self.closeEditorSignal = metod
        
    @traceback_erors
    def setComboDependence(self,ind):
        for key, val in self.spCombo.items():
            if len(key)==2:
                for (colum,_) in key[1]:
                    comb = self.cellWidget(ind,colum)
                    comb.currentTextChanged.connect(lambda t, k=key, o=comb,col=colum: self.ComboChangeEvent(t,k,o,col))
                    val.add(comb)
                    self.ComboChangeEvent(comb.currentText(),key,comb,colum)
                               
    @traceback_erors
    def removeComboDependence(self,ind):
        for key, val in self.spCombo.items():
            if len(key)==2:
                for (colum,_) in key[1]:
                    comb = self.cellWidget(ind,colum)
                    comb.currentTextChanged.disconnect()
                    val.discard(comb)
         
       
    @traceback_erors
    def ComboChangeEvent(self,text,key,obj,colum):
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

               
    @traceback_erors
    def closeEditor(self, editor, hint):
        if self.closeEditorSignal is not None:
            self.closeEditorSignal()
        
        i = self.currentRow()
        j = self.currentColumn()
        now = self.currentItem().text()
        
        self.checkUnique(i,j,self.previousItem,now)
        self.previousItem = now
        now = self.currentItem().text()
        
        self.edit_sp(i,j,self.previousItem,now)
        self.checkBranches(i,j,self.previousItem,now)
        
        
        
        QTableWidget.closeEditor(self, editor, hint)
        

    @traceback_erors
    def add_row(self):
        self.rows+=1
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1
        self.insertRow(ind)
        
        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)
        
        
    @traceback_erors  
    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            self.rows-=1

            self.remove_Unique(ind)
            self.remove_sp(ind)
            self.removeRow(ind)
            self.selectionModel().clearSelection()
            self.setCurrentCell(-1,-1)

        
    @traceback_erors
    def setLinkParentToChildren(self,linkList):
        self.childrenList = {i:set() for i in linkList}
        self.spColums = {i:set() for i in linkList}
        self.spCombo = {i:set() if len(i)==2 else None for i in linkList}

    @traceback_erors
    def add_sp(self, ind):
        for key, st in self.spColums.items():
            if len(key)==1 and len(key[0]) == 1:
                if self.item(ind,key).text() != "":
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

    @traceback_erors
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

    @traceback_erors
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
        
           
    @traceback_erors
    def add_child(self,key,child):
        if key in self.childrenList:
            self.childrenList[key].add(child)
            child.addItems(["Нет"]+list(self.spColums[key]))
            child.setCurrentText("Нет")
        
    @traceback_erors
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
        self.setItem(ind,0, QTableWidgetItem(""))
        self.setItem(ind,1, QTableWidgetItem(""))
        self.add_branch(ind)

    def remove_row(self):
        ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
        self.remove_branch(ind)
        super().remove_row()

    def write_table(self,okgt_info):
        self.clear_table()
        for i, (n,k) in enumerate(okgt_info.keys()):
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

    @traceback_erors
    def add_row(self):
        super().add_row()
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1

        cmb = UserComboBox(self.timer)
        tp = UserComboBox(self.timer)
        tp.addItems([i for i in self.type_dct.values()])
        self.setCellWidget(ind,0, cmb)
        self.setCellWidget(ind,1, tp)
        self.setItem(ind,2, QTableWidgetItem(""))
        self.setItem(ind,3, QTableWidgetItem(""))
        
        self.add_Unique(ind)

        self.add_cmb(((0,1,self.separator),),cmb)
        
        self.setComboDependence(ind)

        

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

        self.dataSetObj.setLinkParentToChildren([((2,),((1,"Проводящий"),))])
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


        self.setItem(ind,2, QTableWidgetItem(""))
        self.setItem(ind,3, QTableWidgetItem(""))
        self.setItem(ind,4, QTableWidgetItem(""))
        self.setItem(ind,5, QTableWidgetItem(""))

        zytype = UserComboBox(self.timer)
        zytype.addItems(list(self.tp_zy.values()))
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
        
        
        
        self.setItemDelegate(DownloadDelegate("PS"))

    def add_row(self):
        super().add_row()
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1
        self.setItem(ind,0, QTableWidgetItem(""))
        self.setItem(ind,1, QTableWidgetItem(""))
        self.add_Unique(ind)

    
     
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