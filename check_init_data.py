# pylint: disable=E0611
# pylint: disable=E1101
from PyQt5.QtWidgets import QTableWidgetSelectionRange
from PyQt5.QtCore import Qt

from calc_okgt import k_conductors


def rcrs(lst,t,nd,st,p,f_one):
    count = 0
    for i,(n,k) in enumerate(lst):
        if p == n and k != st and nd[k][0] == 0:
            if f_one and count==0 and n==st:
                count += 1
                t[i] = True
                nd[k][0]+=1
                nd[n][1]=False
                rcrs(lst,t,nd,st,k,f_one)
            elif f_one and n!=st:
                t[i] = True
                nd[k][0]+=1
                nd[n][1]=False
                rcrs(lst,t,nd,st,k,f_one)
            elif not f_one:
                t[i] = True
                nd[k][0]+=1
                nd[n][1]=False
                rcrs(lst,t,nd,st,k,f_one)

def make_sectors(st, direct):
    sp = sorted(list(st), reverse = not direct)    
    rez = []
    j = sp[0][0]
    i = 0
    for i in range(1,len(sp)):
        if abs(sp[i][0]-sp[i-1][1])>1:
            rez.append((j,sp[i-1][1]))
            j=sp[i][0]

    rez.append((j,sp[i][1]))

    return rez




def checker_init_data(Okgt_node_table,Okgt_sector_table,Okgt_single_table,Ps_table,vl_liks,rpa_liks,Vl_Tabs,Rpa_Tabs,mainTabWidget):
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
        
        nodes[tn1] = [0, True]
        nodes[tk1] = [0, True]
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

    # Проверка таблицы ПС
    ln_ps_tb = Ps_table.rowCount()

    if ln_ps_tb < 1:
        mainTabWidget.setCurrentIndex(1)
        raise Exception('Нет ни одной записи в таблице параметров ПС')

    ps_names = {}
    for i in range(ln_ps_tb):
        ps_row_name = Ps_table.item(i,0).text()
        ps_row_zy = Ps_table.item(i,1).text()

        if ps_row_name == '':
            mainTabWidget.setCurrentIndex(1)
            Ps_table.setRangeSelected(QTableWidgetSelectionRange(i, 0, i, 0), True)
            raise Exception(f'В строке {i+1} таблицы параметров ПС не задано "Название подстанции"')

        elif ps_row_name == 'Нет':
            mainTabWidget.setCurrentIndex(1)
            Ps_table.setRangeSelected(QTableWidgetSelectionRange(i, 0, i, 0), True)
            raise Exception(f'В строке {i+1} таблицы параметров ПС в качестве названия "Название подстанции" нельзя использовать строку "Нет"')

        if ps_row_zy == '':
            mainTabWidget.setCurrentIndex(1)
            Ps_table.setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 1), True)
            raise Exception(f'В строке {i+1} таблицы параметров ПС не задано "Rзу"')

        elif float(ps_row_zy) == 0:
            mainTabWidget.setCurrentIndex(1)
            Ps_table.setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 1), True)
            raise Exception(f'В строке {i+1} таблицы параметров ПС "Rзу" не может иметь нулевое значение')

        ps_names[ps_row_name] = False

    
    vl_names = {}
    for lv_w, vl_item in vl_liks.items():
        vl_name = vl_item["line"].text()

        if vl_name == '':
            mainTabWidget.setCurrentIndex(2)
            Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
            raise Exception('В параметрах ВЛ не задано название ВЛ')

        elif vl_name == 'Нет':
            mainTabWidget.setCurrentIndex(2)
            Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
            raise Exception(f'В параметрах ВЛ в качестве название ВЛ нельзя использовать строку "Нет"')

        vl_names[vl_name] = False

        ln_vl_brn_tb = vl_item["branches"].rowCount()

        if ln_vl_brn_tb < 1:
            mainTabWidget.setCurrentIndex(2)
            Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
            raise Exception('Нет ни одной записи в таблице ветвей ВЛ')

        nodes = {}
        lst = []
        branches = set()
        for i in range(ln_vl_brn_tb):
            tn1 = vl_item["branches"].item(i,0).text()
            tk1 = vl_item["branches"].item(i,1).text()

            if tn1=='':
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["branches"].setRangeSelected(QTableWidgetSelectionRange(i, 0, i, 0), True)
                raise Exception(f'В строке {i+1} таблицы узлов ВЛ не задан "Узел начала"')

            if tk1=='':
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["branches"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 1), True)
                raise Exception(f'В строке {i+1} таблицы узлов ВЛ не задан "Узел конца"')
            
            nodes[tn1] = [0, True]
            nodes[tk1] = [0, True]
            branches.add((tn1,tk1))
            if (tn1,tk1) in branches:
                lst.append((tn1,tk1))

        t = [False]*len(lst)
        rcrs(lst,t,nodes,lst[0][0],lst[0][0],True)
        dd = {i:j for i,j in zip(lst,t)}

        for i in range(ln_vl_brn_tb):
            tn1 = vl_item["branches"].item(i,0).text()
            tk1 = vl_item["branches"].item(i,1).text()
                
            if not dd.get((tn1,tk1),False):
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["branches"].setRangeSelected(QTableWidgetSelectionRange(i, 0, i, 1), True)
                raise Exception(f'В строке {i+1} таблицы узлов ВЛ заданная ветвь не принадлежит разомкнатому графу')

        used_vl_branches = {separator.join(i): [False,j] for j,i in enumerate(lst)}
        ps_branches = {separator.join(i): {'left':False,'right':True} if nodes.get(i[1],[0,False])[1] else {'left':False,'right':False} for i in lst}
        ps_branches[separator.join(lst[0])]['left'] = True
        print(ps_branches)

        ln_vl_sect_tb = vl_item["sector"].rowCount()

        if ln_vl_sect_tb < 1:
            mainTabWidget.setCurrentIndex(2)
            Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
            raise Exception('Нет ни одной записи в таблице участков ВЛ')

        branch_subsectors = {}
        sector_subsectors = {}
        sector_branch = {}
        sector_pos = {}
        

        for i in range(ln_vl_sect_tb):
            vl_row_branch = vl_item["sector"].cellWidget(i,0).currentText()
            vl_row_type = vl_item["sector"].cellWidget(i,1).currentText()
            len_N = vl_item["sector"].item(i,2).text()
            len_K = vl_item["sector"].item(i,3).text()
            support_N = vl_item["sector"].item(i,4).text()
            support_K = vl_item["sector"].item(i,5).text()

            if vl_row_branch == "Нет": 
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 5), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ не выбрана ветвь')

            used_vl_branches[vl_row_branch][0] = True

            if len_N=='':
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 2), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ не задано "Lн"')

            if len_K=='':
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ не задано "Lк"')

            if support_N=='':
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 4, i, 4), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ не задано "Оп. нач."')

            if support_K=='':
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 5, i, 5), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ не задано "Оп. конц."')

            if float(len_N)>float(len_K) or float(len_N)==float(len_K):
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 3), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ "Lн" должно быть меньше "Lк"')

            if int(support_N)==int(support_K):
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 4, i, 5), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ "Оп. нач." и "Оп. конц." не могут быть одинаковыми')

            len_N = float(len_N)
            len_K = float(len_K)
            support_N = int(support_N)
            support_K = int(support_K)
            
            if vl_row_branch not in branch_subsectors:
                branch_subsectors[vl_row_branch] = set()
                branch_subsectors[vl_row_branch].add((support_N,support_K,len_N,len_K,support_N<support_K))
            else:
                branch_subsectors[vl_row_branch].add((support_N,support_K,len_N,len_K,support_N<support_K))

            if vl_row_type not in sector_subsectors and vl_row_type!="Нет":
                sector_subsectors[vl_row_type] = set()
                sector_subsectors[vl_row_type].add((support_N,support_K,len_N,len_K,support_N<support_K))
            elif vl_row_type in sector_subsectors:
                sector_subsectors[vl_row_type].add((support_N,support_K,len_N,len_K,support_N<support_K))

            if (support_N,support_K,len_N,len_K,support_N<support_K) not in sector_pos:
                sector_pos[(support_N,support_K,len_N,len_K,support_N<support_K)] = i
            else:
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 5), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ записан повторяющийся участок')

            if vl_row_type != "Нет":
                sector_branch[vl_row_type] = vl_row_branch
                
        
        branch_sector_order = {}
        for br, val in branch_subsectors.items():
            direction = sum([j[4] for j in val])
            if direction >= len(val)/2 and not (direction == len(val) or direction == 0):
                for j in val:
                    if not j[4]:
                        break
                
                i = sector_pos[j]
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 4, i, 5), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ "Оп. нач." должна быть меньше "Оп. конц."')

            elif direction < len(val)/2 and not (direction == len(val) or direction == 0):
                for j in val:
                    if j[4]:
                        break
                        
                i = sector_pos[j]
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 4, i, 5), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ "Оп. нач." должна быть больше "Оп. конц."')
            
            sector_order = []
            while True:
                if len(val) != 0:
                    for j in val:
                        if len(sector_order)==0:
                            sector_order.append(j)
                            val.remove(j)
                            break
                        elif j[1] == sector_order[0][0]:
                            sector_order.insert(0, j)
                            val.remove(j)
                            break
                        elif j[0] == sector_order[-1][1]:
                            sector_order.append(j)
                            val.remove(j)
                            break
                    else:
                        i = sector_pos[val.pop()]
                        mainTabWidget.setCurrentIndex(2)
                        Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                        vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 4, i, 5), True)
                        raise Exception(f'В строке {i+1} таблицы участков ВЛ заданный участок не связан с другими участками')
                else:
                    break
            
            branch_sector_order[br] = sector_order
            #print(vl_name,br,sector_order)
        okgt_sector_order ={}
        for tp, val in sector_subsectors.items():
            sector_order = []
            while True:
                if len(val) != 0:
                    for j in val:
                        if len(sector_order)==0:
                            sector_order.append(j)
                            val.remove(j)
                            break
                        elif abs(j[3] - sector_order[0][2])<0.0001:
                            sector_order.insert(0, j)
                            val.remove(j)
                            break
                        elif abs(j[2] - sector_order[-1][3])<0.0001:
                            sector_order.append(j)
                            val.remove(j)
                            break
                    else:
                        i = sector_pos[val.pop()]
                        mainTabWidget.setCurrentIndex(2)
                        Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                        vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 3), True)
                        raise Exception(f'В строке {i+1} таблицы участков ВЛ заданная длинна не связана с другой')
                else:
                    break

               

            if sector_order[0][2]>0:
                i = sector_pos[sector_order[0]]
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 2), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ участок с ОКГТ не начинается с 0')

            if sector_order[-1][3]<vl_okgt[tp][1]:
                i = sector_pos[sector_order[-1]]
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ участок ВЛ с ОКГТ полностью не заполняет участок ОКГТ')

            if sector_order[-1][3]>vl_okgt[tp][1]:
                i = sector_pos[sector_order[-1]]
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
                raise Exception(f'В строке {i+1} таблицы участков ВЛ участок ВЛ с ОКГТ превышает длину участок ОКГТ')

            
            br_sct = branch_sector_order[sector_branch[tp]]

            f = len(sector_order)
            for j in range(len(br_sct)):
                if br_sct[j:j+f] == sector_order:
                    break
            else:
                i = sector_pos[sector_order[0]]
                st = [sector_pos[j] for j in sector_order]
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["sector"].setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 5), True)
                raise Exception(f'В строках {st} таблицы участков ВЛ для участков с ОКГТ последовательность длин конфликтует с последовательностью опор')

            okgt_sector_order[tp] = sector_order

        for br, (j,i)in used_vl_branches.items():
            if not j:
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["branches"].setRangeSelected(QTableWidgetSelectionRange(i, 0, i, 1), True)
                raise Exception(f'На ветвь ВЛ в строке {i+1} не ссылается ни одна запись')

        branch_sector_set = {}
        for br_n, diap in branch_sector_order.items():
            i,j = diap[0][0], diap[-1][1]
            direct = i<j
            rn = zip(range(i,j),range(i+1,j+1)) if direct else zip(range(i,j,-1),range(i-1,j-1,-1))
            branch_sector_set[br_n] = (set([(i,j) for i,j in rn]),direct)

        okgt_sector_set = {}
        for tp, diap in okgt_sector_order.items():
            i,j = diap[0][0], diap[-1][1]
            rn = zip(range(i,j),range(i+1,j+1)) if i<j else zip(range(i,j,-1),range(i-1,j-1,-1))
            if sector_branch[tp] not in okgt_sector_set:
                okgt_sector_set[sector_branch[tp]] = set()
            okgt_sector_set[sector_branch[tp]].update(set([(i,j) for i,j in rn]))


        check_list = [
            ("conductors",0,"проводов",'не выбран "Провод"'),\
            ("phases",1,"фазировки",'не выбрана "Фазировка"'),
            ("supports",2,"опор",'не выбран "Тип опоры"'),\
        ]

        for tb_type, tb_page, er_t_1, er_t_2 in check_list:

            branch_sector_set_for = {}

            ln_vl_tb = vl_item["params"][tb_type].rowCount()

            if ln_vl_tb < 1:
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(tb_page)
                raise Exception(f'Нет ни одной записи в таблице {er_t_1} ВЛ')

            for i in range(ln_vl_tb):
                vl_row_branch = vl_item["params"][tb_type].cellWidget(i,0).currentText()
                support_N = vl_item["params"][tb_type].item(i,1).text()
                support_K = vl_item["params"][tb_type].item(i,2).text()
                vl_row_paran = vl_item["params"][tb_type].cellWidget(i,3).currentText()

                if vl_row_branch == "Нет":
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(tb_page)
                    vl_item["params"][tb_type].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы {er_t_1} ВЛ не выбрана ветвь')

                if vl_row_paran == "Нет":
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(tb_page)
                    vl_item["params"][tb_type].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы {er_t_1} ВЛ {er_t_2}')

                if support_N=='':
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(tb_page)
                    vl_item["params"][tb_type].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 1), True)
                    raise Exception(f'В строке {i+1} таблицы {er_t_1} ВЛ не задано "Оп. нач."')

                if support_K=='':
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(tb_page)
                    vl_item["params"][tb_type].setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы {er_t_1} ВЛ не задано "Оп. конц."')

                if int(support_N)==int(support_K):
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(tb_page)
                    vl_item["params"][tb_type].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы {er_t_1} ВЛ "Оп. нач." и "Оп. конц." не могут быть одинаковыми')

                if (int(support_N)<int(support_K)) != branch_sector_set[vl_row_branch][1]:
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(tb_page)
                    vl_item["params"][tb_type].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы {er_t_1} ВЛ "Оп. нач." и "Оп. конц." имеют противоположное направление с таблицой участков ВЛ')

                s_n,s_k = int(support_N), int(support_K)
                rn = zip(range(s_n,s_k),range(s_n+1,s_k+1)) if s_n<s_k else zip(range(s_n,s_k,-1),range(s_n-1,s_k-1,-1))
                curent_set = set([(i,j) for i,j in rn])
                
                
                if not (curent_set <=  branch_sector_set[vl_row_branch][0]):
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(tb_page)
                    vl_item["params"][tb_type].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы {er_t_1} ВЛ "Оп. нач." и "Оп. конц." не принадлежит ветви ВЛ')
                else:
                    if vl_row_branch not in branch_sector_set_for:
                        branch_sector_set_for[vl_row_branch] = set()

                    
                    if branch_sector_set_for[vl_row_branch] >= curent_set:
                        mainTabWidget.setCurrentIndex(2)
                        Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                        vl_item["params_tab"].setCurrentIndex(tb_page)
                        vl_item["params"][tb_type].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                        raise Exception(f'В строке {i+1} таблицы {er_t_1} ВЛ участок с такими же граничными опорами уже задан')

                    else:
                        branch_sector_set_for[vl_row_branch].update(curent_set)

            for br_n in branch_sector_set:
                st = branch_sector_set[br_n][0].difference(branch_sector_set_for[br_n])
                if len(st)!=0:
                    rez = make_sectors(st, branch_sector_set[br_n][1])
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(tb_page)
                    raise Exception(f'В таблице {er_t_1} ВЛ не заданы следующие участки: {rez}')


        branch_sector_set_for = {}
        okgt_sector_set_for = {}

        ln_vl_gw_tb = vl_item["params"]["groundwires"].rowCount()

        if ln_vl_gw_tb < 1:
            mainTabWidget.setCurrentIndex(2)
            Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
            vl_item["params_tab"].setCurrentIndex(3)
            raise Exception(f'Нет ни одной записи в таблице грозотросов ВЛ')

        for i in range(ln_vl_gw_tb):
            vl_row_branch = vl_item["params"]["groundwires"].cellWidget(i,0).currentText()
            support_N = vl_item["params"]["groundwires"].item(i,1).text()
            support_K = vl_item["params"]["groundwires"].item(i,2).text()
            vl_gw1_w = vl_item["params"]["groundwires"].cellWidget(i,3)
            vl_gw2_w = vl_item["params"]["groundwires"].cellWidget(i,4)

            gw1,chb1,_ = vl_item["params"]["groundwires"].wd_d[vl_gw1_w]
            gw2,chb2,_ = vl_item["params"]["groundwires"].wd_d[vl_gw2_w]

            if vl_row_branch == "Нет":
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(3)
                vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ не выбрана ветвь')

            if support_N=='':
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(3)
                vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 1), True)
                raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ не задано "Оп. нач."')

            if support_K=='':
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(3)
                vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 2, i, 2), True)
                raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ не задано "Оп. конц."')

            if int(support_N)==int(support_K):
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(3)
                vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ "Оп. нач." и "Оп. конц." не могут быть одинаковыми')

            if (int(support_N)<int(support_K)) != branch_sector_set[vl_row_branch][1]:
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(3)
                vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ "Оп. нач." и "Оп. конц." имеют противоположное направление с таблицой участков ВЛ')

            s_n,s_k = int(support_N), int(support_K)
            rn = zip(range(s_n,s_k),range(s_n+1,s_k+1)) if s_n<s_k else zip(range(s_n,s_k,-1),range(s_n-1,s_k-1,-1))
            curent_set = set([(i,j) for i,j in rn])

            if chb1.checkState() == Qt.Checked:
                
                if gw1.currentText() == "Нет":
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(3)
                    vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ не выбран ОКГТ')
                elif k_conductors[gw1.currentText()]["Bsc"] is None:
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(3)
                    vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ выбраный ОКГТ не имеет предельной термической стойкости')
                else: 
                    if vl_row_branch not in okgt_sector_set_for:
                        okgt_sector_set_for[vl_row_branch] = set()

                    if okgt_sector_set_for[vl_row_branch] >= curent_set:
                        mainTabWidget.setCurrentIndex(2)
                        Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                        vl_item["params_tab"].setCurrentIndex(3)
                        vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                        raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ участок с такими же граничными опорами уже задан')
                    else:
                        okgt_sector_set_for[vl_row_branch].update(curent_set)

            elif chb2.checkState() == Qt.Checked:
                if gw2.currentText() == "Нет":
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(3)
                    vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ не выбран ОКГТ')
                elif k_conductors[gw2.currentText()]["Bsc"] is None:
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(3)
                    vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ выбраный ОКГТ не имеет предельной термической стойкости')
                else:
                    if vl_row_branch not in okgt_sector_set_for:
                        okgt_sector_set_for[vl_row_branch] = set()

                    if okgt_sector_set_for[vl_row_branch] >= curent_set:
                        mainTabWidget.setCurrentIndex(2)
                        Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                        vl_item["params_tab"].setCurrentIndex(3)
                        vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                        raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ участок с такими же граничными опорами уже задан')
                    else:
                        okgt_sector_set_for[vl_row_branch].update(curent_set)


            if not (curent_set <=  branch_sector_set[vl_row_branch][0]):
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(3)
                vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ "Оп. нач." и "Оп. конц." не принадлежит ветви ВЛ')
            else:
                if vl_row_branch not in branch_sector_set_for:
                    branch_sector_set_for[vl_row_branch] = set()

                
                if branch_sector_set_for[vl_row_branch] >= curent_set:
                    mainTabWidget.setCurrentIndex(2)
                    Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                    vl_item["params_tab"].setCurrentIndex(3)
                    vl_item["params"]["groundwires"].setRangeSelected(QTableWidgetSelectionRange(i, 1, i, 2), True)
                    raise Exception(f'В строке {i+1} таблицы грозотросов ВЛ участок с такими же граничными опорами уже задан')

                else:
                    branch_sector_set_for[vl_row_branch].update(curent_set)

        for br_n in okgt_sector_set:
            st = okgt_sector_set[br_n].difference(okgt_sector_set_for[br_n])
            if len(st)!=0:
                rez = make_sectors(st, branch_sector_set[br_n][1])
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(3)
                raise Exception(f'В таблице грозотросов ВЛ не заданы следующие участки: {rez}')


        ln_vl_ps_tb = vl_item["params"]["PSs"].rowCount()

        if ln_vl_ps_tb < 1:
            mainTabWidget.setCurrentIndex(2)
            Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
            vl_item["params_tab"].setCurrentIndex(4)
            raise Exception(f'Нет ни одной записи в таблице ПС ВЛ')

        vl_ps_names = set()

        side_d = {"Слева":"left","Справа":"right",}

        for i in range(ln_vl_ps_tb):
            vl_row_branch = vl_item["params"]["PSs"].cellWidget(i,0).currentText()
            vl_row_ps = vl_item["params"]["PSs"].cellWidget(i,1).currentText()
            vl_row_side = vl_item["params"]["PSs"].cellWidget(i,2).currentText()
            vl_row_leng = vl_item["params"]["PSs"].item(i,3).text()
            
            #ps_branches
            #ps_names

            if vl_row_branch == "Нет":
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(4)
                vl_item["params"]["PSs"].setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
                raise Exception(f'В строке {i+1} таблицы ПС ВЛ не выбрана ветвь')

            if vl_row_ps == "Нет":
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(4)
                vl_item["params"]["PSs"].setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
                raise Exception(f'В строке {i+1} таблицы ПС ВЛ не выбрана ПС')
            
            elif vl_row_ps in vl_ps_names:
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(4)
                vl_item["params"]["PSs"].setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
                raise Exception(f'В строке {i+1} таблицы ПС ВЛ линия не может присоединяться к одной ПС дважды')
            else:
                vl_ps_names.add(vl_row_ps)
                ps_names[vl_row_ps] = True

            if vl_row_leng == "":
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(4)
                vl_item["params"]["PSs"].setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
                raise Exception(f'В строке {i+1} таблицы ПС ВЛ не задано "L"')

            elif float(vl_row_leng) == 0:
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(4)
                vl_item["params"]["PSs"].setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
                raise Exception(f'В строке {i+1} таблицы ПС ВЛ "L" не может быть нулевым')

            if not ps_branches[vl_row_branch][side_d[vl_row_side]]:
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(4)
                vl_item["params"]["PSs"].setRangeSelected(QTableWidgetSelectionRange(i, 3, i, 3), True)
                raise Exception(f'В строке {i+1} таблицы ПС ВЛ ветвь не может быть присоедена к ПС')
            else:
                ps_branches[vl_row_branch][side_d[vl_row_side]] = False

        for i, j in ps_branches.items():
            if j["left"] or j["right"]:
                mainTabWidget.setCurrentIndex(2)
                Vl_Tabs.setCurrentIndex(Vl_Tabs.indexOf(lv_w))
                vl_item["params_tab"].setCurrentIndex(4)
                raise Exception(f'В таблице ПС ВЛ не задано присоединение к подстанции для ветви {i}')

            
            
            

            

            

            
            


        



            



            

