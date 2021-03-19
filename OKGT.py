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

from table_classes import traceback_erors, OkgtSectorTable, OkgtSingleTable, PSTable, NodeTable, LineEditManager,\
    VlParamsTable, VlSectorTable, VlPsParamsTable, VlCommonChainsTable

from calc_okgt import k_supports, k_conductors, main_calc

from initial_data import okgt_info, vl_info, ps_info, rpa_info

   
    

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
        self.mainTabWidget = QTabWidget()
        topVBoxLayout.addWidget(self.mainTabWidget) 
        central_widget = QWidget()
        central_widget.setLayout(topVBoxLayout)
        self.setCentralWidget(central_widget) 

        
        self.Okgt_Widget = QWidget()
        self.Vl_Tabs = QTabWidget()
        self.Ps_Widget = QWidget()
        Rpa_Tabs = QTabWidget()
        Rez_Tabs = QTabWidget()

        self.mainTabWidget.addTab(self.Okgt_Widget,"ОКГТ")
        self.mainTabWidget.addTab(self.Ps_Widget,"ПС")
        self.mainTabWidget.addTab(self.Vl_Tabs,"ВЛ")
        self.mainTabWidget.addTab(Rpa_Tabs,"РЗА")
        self.mainTabWidget.addTab(Rez_Tabs,"Результаты")


        self.cntr_pr = {"trig":False,"timer":QTimer()}
        self.cntr_pr["timer"].timeout.connect(self.on_timeout)
        self.cntr_pr["timer"].setSingleShot(True)


        self.okgt_tab_maker()
        self.ps_tab_maker()
        self.MenuBarMaker()

        self.le_manager = LineEditManager(self.Vl_Tabs)
        self.vl_liks = {}
        self.vl_settings_dict = {
            "conductors":"Провода","phases":"Фазировка","supports":"Опоры","groundwires":"Грозотросы",\
            "PSs":"ПС","grounded":"Заземление проводов","countercables":"Противовес","commonchains":"Смежные цепи",
        }
        self.vl_settings_dict_rev = {v:k for k,v in self.vl_settings_dict.items()}

        


    def on_timeout(self):
        self.cntr_pr["trig"] = False

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.cntr_pr["trig"] = True
            self.cntr_pr["timer"].start(500)
            
    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_Control:
            self.cntr_pr["trig"] = False

    

    def MenuBarMaker(self):
        self.statusBar()
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&Файл')

        open_file = QAction( '&Открыть', self) #QIcon('exit.png'),
        open_file.setShortcut('Ctrl+K')
        open_file.setStatusTip('Открыть файл')
        open_file.triggered.connect(self.OpenFile)
        fileMenu.addAction(open_file)

        read_table = QAction( '&Прочитать таблицы', self) #QIcon('exit.png'),
        read_table.setShortcut('Ctrl+L')
        read_table.setStatusTip('Прочитать таблицы')
        read_table.triggered.connect(self.ReadTables)
        fileMenu.addAction(read_table)

        exitAction = QAction( '&Выход', self) #QIcon('exit.png'),
        exitAction.setShortcut('Esc')
        exitAction.setStatusTip('Выход и программы')
        exitAction.triggered.connect(lambda:self.closeEvent(QCloseEvent()))
        fileMenu.addAction(exitAction)
      
    

        editMenu = menubar.addMenu('&Правка')


        add_row = QAction( '&Добавить ветвь', self) #QIcon('exit.png'),
        add_row.setShortcut('Ctrl+Q')
        add_row.setStatusTip('Добавить ветвь в таблицу')
        add_row.triggered.connect(self.AddBranch)
        editMenu.addAction(add_row)

        remove_row = QAction( '&Удалить ветвь', self) #QIcon('exit.png'),
        remove_row.setShortcut('Ctrl+A')
        remove_row.setStatusTip('Удалить ветвь из таблицы')
        remove_row.triggered.connect(self.RemoveBranch) 
        editMenu.addAction(remove_row)

        add_sector = QAction( '&Добавить участок', self) #QIcon('exit.png'),
        add_sector.setShortcut('Ctrl+W')
        add_sector.setStatusTip('Добавить участок в таблицу')
        add_sector.triggered.connect(self.AddSector)
        editMenu.addAction(add_sector)

        remove_sector = QAction( '&Удалить участок', self) #QIcon('exit.png'),
        remove_sector.setShortcut('Ctrl+S')
        remove_sector.setStatusTip('Удалить участок из таблицы')
        remove_sector.triggered.connect(self.RemoveSector)
        editMenu.addAction(remove_sector)

        add_params = QAction( '&Добавить параметры', self) #QIcon('exit.png'),
        add_params.setShortcut('Ctrl+E')
        add_params.setStatusTip('Добавить параметры в таблицу')
        add_params.triggered.connect(self.AddParams)
        editMenu.addAction(add_params)

        remove_params = QAction( '&Удалить параметры', self) #QIcon('exit.png'),
        remove_params.setShortcut('Ctrl+D')
        remove_params.setStatusTip('Удалить параметры из таблицы')
        remove_params.triggered.connect(self.RemoveParams)
        editMenu.addAction(remove_params)

        add_tab = QAction( '&Добавить вкладку', self) #QIcon('exit.png'),
        add_tab.setShortcut("Ctrl+F")
        add_tab.setStatusTip('Добаваить новую вкладку')
        add_tab.triggered.connect(self.AddTab)
        editMenu.addAction(add_tab)

        remove_tab = QAction( '&Удалить вкладку', self) #QIcon('exit.png'),
        remove_tab.setShortcut("Ctrl+G")
        remove_tab.setStatusTip('Удалить текущую вкладку')
        remove_tab.triggered.connect(self.RemoveTab)
        editMenu.addAction(remove_tab)

        clear_tab = QAction( '&Очистить вкладку', self) #QIcon('exit.png'),
        clear_tab.setShortcut("Ctrl+Shift+D")
        clear_tab.setStatusTip('Очистить текущую вкладку')
        clear_tab.triggered.connect(self.ClearTab)
        editMenu.addAction(clear_tab)



    def AddBranch(self):
        ind = self.mainTabWidget.currentIndex()
        if ind == 0:
            self.Okgt_node_table.add_row()
        elif ind == 1:
            self.Ps_table.add_row()
        elif ind == 2:
            ind = self.Vl_Tabs.currentIndex()
            if ind>-1:
                wd = self.Vl_Tabs.widget(ind)
                data = self.vl_liks[wd]
                data["branches"].add_row()
        

    def AddSector(self):
        ind = self.mainTabWidget.currentIndex()
        if ind == 0:
            self.Okgt_sector_table.add_row()
        elif ind == 2:
            ind = self.Vl_Tabs.currentIndex()
            if ind>-1:
                wd = self.Vl_Tabs.widget(ind)
                data = self.vl_liks[wd]
                data["sector"].add_row()
        

    def AddParams(self):
        ind = self.mainTabWidget.currentIndex()
        if ind == 0:
            self.Okgt_single_table.add_row()
        elif ind == 2:
            ind = self.Vl_Tabs.currentIndex()
            if ind>-1:
                wd = self.Vl_Tabs.widget(ind)
                data = self.vl_liks[wd]
                p_ind = data["params_tab"].currentIndex()
                header_t = data["params_tab"].tabText(p_ind)
                data["params"][self.vl_settings_dict_rev[header_t]].add_row()
        

    def RemoveBranch(self):
        ind = self.mainTabWidget.currentIndex()
        if ind == 0:
            self.Okgt_node_table.remove_row()
        elif ind == 1:
            self.Ps_table.remove_row()
        elif ind == 2:
            ind = self.Vl_Tabs.currentIndex()
            if ind>-1:
                wd = self.Vl_Tabs.widget(ind)
                data = self.vl_liks[wd]
                data["branches"].remove_row()
        

    def RemoveSector(self):
        ind = self.mainTabWidget.currentIndex()
        if ind == 0:
            self.Okgt_sector_table.remove_row()
        elif ind == 2:
            ind = self.Vl_Tabs.currentIndex()
            if ind>-1:
                wd = self.Vl_Tabs.widget(ind)
                data = self.vl_liks[wd]
                data["sector"].remove_row()
        

    def RemoveParams(self):
        ind = self.mainTabWidget.currentIndex()
        if ind == 0:
            self.Okgt_single_table.remove_row()
        elif ind == 2:
            ind = self.Vl_Tabs.currentIndex()
            if ind>-1:
                wd = self.Vl_Tabs.widget(ind)
                data = self.vl_liks[wd]
                p_ind = data["params_tab"].currentIndex()
                header_t = data["params_tab"].tabText(p_ind)
                data["params"][self.vl_settings_dict_rev[header_t]].remove_row()
        

    def ClearTab(self):
        ind = self.mainTabWidget.currentIndex()
        if ind == 0:
            self.Okgt_node_table.clear_table()
            self.Okgt_sector_table.clear_table()
            self.Okgt_single_table.clear_table()
            
        elif ind == 1:
            self.Ps_table.clear_table()
        elif ind == 2:
            ind = self.Vl_Tabs.currentIndex()
            if ind>-1:
                wd = self.Vl_Tabs.widget(ind)
                data = self.vl_liks[wd]
                data["branches"].clear_table()
                data["sector"].clear_table()
                for table in data["params"].values():
                    table.clear_table()


    def AddTab(self):
        ind = self.mainTabWidget.currentIndex()
        if ind == 2:
            print("Add VL")
            self.add_vl_tab()
        elif ind == 3:
            
            print("Add RPA")

    def RemoveTab(self):
        ind = self.mainTabWidget.currentIndex()
        if ind == 2:
            print("Remove VL")
            self.remove_vl_tab()
        elif ind == 3:
            print("Remove RPA")
        


    def okgt_tab_maker(self):
        self.Okgt_node_table = NodeTable()
        self.Okgt_sector_table = OkgtSectorTable(self.Okgt_node_table,self.cntr_pr)
        self.Okgt_single_table = OkgtSingleTable(self.Okgt_sector_table,self.cntr_pr)

        self.Okgt_sector_table.setMinimumHeight(200)

        
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

    def ps_tab_maker(self):
        self.Ps_table = PSTable()
        ps_vbl = QVBoxLayout()
        ps_vbl.addWidget(self.Ps_table)
        self.Ps_Widget.setLayout(ps_vbl)


    def add_vl_tab(self):
        line = QLineEdit()
        
        vl_branches = NodeTable()
        
        vl_sectors = VlSectorTable(vl_branches,self.Okgt_sector_table,self.cntr_pr)
        vl_sectors.setMinimumHeight(180)
        
        d = {}
        param_tabs = QTabWidget()
        for k,v in self.vl_settings_dict.items():
            if k == "PSs":
                table = VlPsParamsTable(vl_branches,self.Ps_table,self.cntr_pr)
            elif k == "commonchains":
                table = VlCommonChainsTable(vl_branches,self.vl_liks,self.le_manager,line,self.cntr_pr) 
            else:
                table = VlParamsTable(vl_branches,k,self.cntr_pr)
                
            param_tabs.addTab(table,v)
            d[k] = table
        
        vl_spltV = QSplitter(Qt.Vertical)
        vl_spltV.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        v_top = QVBoxLayout()
        h_top = QHBoxLayout()
        h_top.addWidget(QLabel("Название ВЛ:"))
        h_top.addWidget(line)
        v_top.addLayout(h_top)
        v_top.addWidget(vl_branches)
        v_top.setContentsMargins(0, 0, 0, 0)
        top = QWidget()
        top.setLayout(v_top)

        vl_spltV.addWidget(top)
        vl_spltV.addWidget(vl_sectors)
        vl_spltV.addWidget(param_tabs)
        vl_spltV.setStretchFactor(1, 3) 
        vl_spltV.setStretchFactor(3, 2) 
        vl_spltV.setContentsMargins(11, 5, 11, 0)

        ind = self.Vl_Tabs.addTab(vl_spltV,"")

        self.le_manager.add_lineEdit(line,vl_spltV)
        name = self.le_manager.get_unique_name("ВЛ № ")
        line.setText(name)
        #setTabText
        self.Vl_Tabs.setCurrentIndex(ind)

        self.vl_liks[vl_spltV] = {
            "line":line,
            "branches":vl_branches,
            "sector":vl_sectors,
            "params_tab":param_tabs,
            "params":d,
        }


    def remove_vl_tab(self, s_int=None):
        ind = self.Vl_Tabs.currentIndex() if s_int is None else s_int
        if ind>-1:
            wd = self.Vl_Tabs.widget(ind)
            data = self.vl_liks[wd]
            self.le_manager.remove_lineEdit(data["line"])
            self.Vl_Tabs.removeTab(ind)
            del self.vl_liks[wd]
        
    #@traceback_erors 
    def OpenFile(self):
        self.Okgt_node_table.write_table(okgt_info)
        self.Okgt_sector_table.write_table(okgt_info)
        self.Okgt_single_table.write_table(okgt_info)
        self.Ps_table.write_table(ps_info)

        for ind in range(self.Vl_Tabs.count()-1,-1,-1):
            self.remove_vl_tab(ind)

        for ind, (name,info) in enumerate(vl_info.items()):
            self.add_vl_tab()
            data = self.vl_liks[self.Vl_Tabs.widget(ind)]
            data['line'].setText(name)
            data["branches"].write_table(info,vl=True)
            data["sector"].write_table(info)
            
            for t_n, table in data["params"].items():
                if t_n!="commonchains":
                    table.write_table(info)

        for ind, info in enumerate(vl_info.values()):
            data = self.vl_liks[self.Vl_Tabs.widget(ind)]
            data["params"]["commonchains"].write_table(info)
         
        
    #@traceback_erors
    def ReadTables(self):
        
        global okgt_info, ps_info, vl_info
        lst = self.Okgt_node_table.read_table()
        dct = self.Okgt_sector_table.read_table(lst)
        okgt_info = self.Okgt_single_table.read_table(dct)
        ps_info = self.Ps_table.read_table()
        #print(okgt_info_new)

        d_lst = {}
        d_com_tables = {}
        vl_info_new = {}
        for data in self.vl_liks.values():
            name = data['line'].text()
            br_lst = data["branches"].read_table()
            d_lst[name] = br_lst
            d_com_tables[name] = data["params"]["commonchains"]
            vl_info_new[name] = {}

            vl_info_new[name].update([(key,val) for key,val in data["sector"].read_table(br_lst).items()])
            for t_n, table in data["params"].items():
                if t_n!="commonchains":
                    vl_info_new[name].update([(key,val) for key,val in table.read_table(br_lst).items()])

        
        for name, table in d_com_tables.items():
            vl_info_new[name].update([(key,val) for key,val in table.read_table(name,d_lst).items()])

        vl_info = vl_info_new


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

    