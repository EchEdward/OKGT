# pylint: disable=E0611
# pylint: disable=E1101
from PyQt5.QtWidgets import QTableWidgetSelectionRange
from PyQt5.QtCore import Qt


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


def checker_init_data(Okgt_node_table,Okgt_sector_table,Okgt_single_table,Ps_table,vl_liks,rpa_liks,mainTabWidget):
    separator = " - "
    ln_okgt_tb = Okgt_node_table.rowCount()

    # 1. Нет ни одной записи в таблице узлов
    if ln_okgt_tb < 1:
        mainTabWidget.setCurrentIndex(0)
        raise Exception('Нет ни одной записи в таблице узлов ОКГТ')
    
    nodes = {}
    lst = []
    branches = set()
    for i in range(ln_okgt_tb):
        tn1 = Okgt_node_table.item(i,0).text()
        tk1 = Okgt_node_table.item(i,1).text()

        if tn1=='':
            mainTabWidget.setCurrentIndex(0)
            Okgt_node_table.setRangeSelected(QTableWidgetSelectionRange(i, 0, i, 0), True)
            raise Exception(f'В строке {i+1} таблицы узлов ОКГТ не задан "Узел начала"')

        if tk1=='':
            mainTabWidget.setCurrentIndex(0)
            Okgt_node_table.setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 1), True)
            raise Exception(f'В строке {i+1} таблицы узлов ОКГТ не задан "Узел конца"')
        
        nodes[tn1] = 0
        nodes[tk1] = 0
        branches.add((tn1,tk1))
        if (tn1,tk1) in branches:
            lst.append((tn1,tk1))

    t = [False]*len(lst)
    rcrs(lst,t,nodes,lst[0][0],lst[0][0],True)
    dd = {i:j for i,j in zip(lst,t)}

    for i in range(ln_okgt_tb):
        tn1 = Okgt_node_table.item(i,0).text()
        tk1 = Okgt_node_table.item(i,1).text()
            
        if not dd.get((tn1,tk1),False):
            mainTabWidget.setCurrentIndex(0)
            Okgt_node_table.setRangeSelected(QTableWidgetSelectionRange(i, 0, i, 1), True)
            raise Exception(f'В строке {i+1} таблицы узлов ОКГТ заданная ветвь не принадлежит разомкнатому графу')

    used_okgt_branches = {separator.join(i): [False,j] for j,i in enumerate(lst)}

    #Таблица участков ОКГТ
    ln_okgt_sect_tb = Okgt_sector_table.rowCount()

    if ln_okgt_sect_tb < 1:
        mainTabWidget.setCurrentIndex(0)
        raise Exception('Нет ни одной записи в таблице участков ОКГТ')

    single_okgt = {}
    vl_okgt = {}
    for i in range(ln_okgt_sect_tb):
        br = Okgt_sector_table.cellWidget(i,0).currentText()
        if br == "Нет": 
            mainTabWidget.setCurrentIndex(0)
            Okgt_sector_table.setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 3), True)
            raise Exception(f'В строке {i+1} таблицы участков ОКГТ не выбрана ветвь')

        used_okgt_branches[br][0] = True

        tp = Okgt_sector_table.cellWidget(i,1).currentText()
        sector_name = Okgt_sector_table.item(i,2).text()
        sector_len = Okgt_sector_table.item(i,3).text()

        if sector_name == "Нет": 
            mainTabWidget.setCurrentIndex(0)
            Okgt_sector_table.setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 2), True)
            raise Exception(f'В строке {i+1} таблицы участков ОКГТ в качестве названия участка нельзя использовать строку "Нет"')
        
        elif sector_name == "": 
            mainTabWidget.setCurrentIndex(0)
            Okgt_sector_table.setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 2), True)
            raise Exception(f'В строке {i+1} таблицы участков ОКГТ не задано "Имя участка"')

        if sector_len == "": 
            mainTabWidget.setCurrentIndex(0)
            Okgt_sector_table.setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
            raise Exception(f'В строке {i+1} таблицы участков ОКГТ не задана "Длина"')
        
        elif float(sector_len) == 0: 
            mainTabWidget.setCurrentIndex(0)
            Okgt_sector_table.setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
            raise Exception(f'В строке {i+1} таблицы участков ОКГТ "Длина" не может иметь нулевое значение')

        if tp=='ВЛ':
            vl_okgt[sector_name] = [False, float(sector_len)]
        elif tp == 'Проводящий':
            single_okgt[sector_name] = [False,i]

    
    for br, (j,i)in used_okgt_branches.items():
        if not j:
            mainTabWidget.setCurrentIndex(0)
            Okgt_node_table.setRangeSelected(QTableWidgetSelectionRange(i, 0, i, 1), True)
            raise Exception(f'На ветвь ОКГТ в строке {i+1} не ссылается ни одна запись')
            
    
    ln_okgt_sing_tb = Okgt_single_table.rowCount()

    if ln_okgt_sing_tb < 1:
        mainTabWidget.setCurrentIndex(0)
        raise Exception('Нет ни одной записи в таблице параметров ОКГТ')

    for i in range(ln_okgt_sing_tb):
        sector_name = Okgt_single_table.cellWidget(i,0).currentText()

        if sector_name == "Нет": 
            mainTabWidget.setCurrentIndex(0)
            Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 5), True)
            raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ не выбран участок')

        if single_okgt[sector_name][0]:
            mainTabWidget.setCurrentIndex(0)
            Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 5), True)
            raise Exception(f'Строка {i+1} таблицы пареметров ОКГТ ссылается на уже описанный ранее участок')
        
        single_okgt[sector_name][0] = True

        X = Okgt_single_table.item(i,2).text()
        Y = Okgt_single_table.item(i,3).text()
        C_zy = Okgt_single_table.item(i,4).text()

        if X == "": 
            mainTabWidget.setCurrentIndex(0)
            Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 2), True)
            raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ не задан "X"')

        if Y == "": 
            mainTabWidget.setCurrentIndex(0)
            Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
            raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ не задан "Y"')

        if C_zy == "": 
            mainTabWidget.setCurrentIndex(0)
            Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 4, i, 4), True)
            raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ не задано "Кол. ЗУ"')

        elif int(C_zy)!=0:
            R_zy = Okgt_single_table.item(i,5).text()

            if R_zy == "": 
                mainTabWidget.setCurrentIndex(0)
                Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 5, i, 5), True)
                raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ не задан "Rзу"')

            elif float(R_zy) == 0: 
                mainTabWidget.setCurrentIndex(0)
                Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 5, i, 5), True)
                raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ "Rзу" не может иметь нулевое значение')


            if "Нет" == Okgt_single_table.cellWidget(i,6).currentText():
                mainTabWidget.setCurrentIndex(0)
                Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 5), True)
                raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ не выбран способ заземления')

        if Okgt_single_table.item(i,7).checkState() == Qt.Checked:
            X_c = Okgt_single_table.item(i,8).text()
            Y_c = Okgt_single_table.item(i,9).text()
            D_c = Okgt_single_table.item(i,10).text()
            R0_c = Okgt_single_table.item(i,11).text()

            if X_c == "": 
                mainTabWidget.setCurrentIndex(0)
                Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 8, i, 8), True)
                raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ для противовеса не задан "X"')

            if Y_c == "": 
                mainTabWidget.setCurrentIndex(0)
                Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 9, i, 9), True)
                raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ для противовеса не задан "Y"')

            if D_c == "": 
                mainTabWidget.setCurrentIndex(0)
                Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 10, i, 10), True)
                raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ для противовеса не задан "D"')

            elif float(D_c) == 0: 
                mainTabWidget.setCurrentIndex(0)
                Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 10, i, 10), True)
                raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ "D" не может иметь нулевое значение')

            if R0_c == "": 
                mainTabWidget.setCurrentIndex(0)
                Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 11, i, 11), True)
                raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ для противовеса не задан "Po"')

            elif float(R0_c) == 0: 
                mainTabWidget.setCurrentIndex(0)
                Okgt_single_table.setRangeSelected(QTableWidgetSelectionRange(i, 11, i, 11), True)
                raise Exception(f'В строке {i+1} таблицы пареметров ОКГТ "Po" не может иметь нулевое значение')


    for sector_name, (j,i)in single_okgt.items():
        if not j:
            mainTabWidget.setCurrentIndex(0)
            Okgt_sector_table.setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 2), True)
            raise Exception(f'На участок ОКГТ в строке {i+1} не ссылается ни одна запись')



            

