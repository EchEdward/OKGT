from docxtpl import DocxTemplate, R, Listing

# pylint: disable=E0611
# pylint: disable=E1101
from docx import Document
from docx.shared import Pt, Mm, Cm
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE
from docx.oxml.shared import OxmlElement, qn

from calc_okgt import k_conductors


def decToRoman(num):
    rome_nums = ''
    S1 = {1: 'IVX', 10: 'XLC', 100: 'CDM', 1000: 'M  '}
    for i in (1000, 100, 10, 1):
        if num // i != 0:
            a, b, c = S1[i]
            S = (a, a * 2, a * 3, a + b, b, b + a, b + 2 * a, b + 3 * a, a + c)
            rome_nums += S[num // i - 1]
            num = num - (num // i) * i
    return rome_nums

# Функция выравнивания содержимого таблицы по вертикали
def set_cell_vertical_alignment(cell, align="center"): 
    try:   
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcValign = OxmlElement('w:vAlign')  
        tcValign.set(qn('w:val'), align)  
        tcPr.append(tcValign)
        return True 
    except:
        #traceback.print_exc()             
        return False

def cell_settings(cell, text, align="center", width=None, font_size=12, font_name="Times"):
    cell.text = text
    align_tp = {"center":WD_ALIGN_PARAGRAPH.CENTER,"right":WD_ALIGN_PARAGRAPH.RIGHT,"left":WD_ALIGN_PARAGRAPH.LEFT }
    cell.paragraphs[0].alignment = align_tp[align]
    set_cell_vertical_alignment(cell, align="center")
    cell.paragraphs[0].paragraph_format.space_before = Pt(0)
    cell.paragraphs[0].paragraph_format.space_after = Pt(0)
    cell.paragraphs[0].runs[0].font.size = Pt(font_size)
    cell.paragraphs[0].runs[0].font.name = font_name

    if width is not None:
        cell.width = Inches(width)

def rpa_settings_table(doc, tbl_ind, vl_name, ps_name, current_rpa_info, report_setings, font_size=12, font_name="Times"):
    p1=doc.add_paragraph()
    p1.add_run(f'Таблица {tbl_ind} - {vl_name} > {ps_name}')
    p1.runs[0].font.size = Pt(font_size)
    p1.runs[0].font.name = font_name
    pt_f = p1.paragraph_format
    pt_f.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pt_f.space_after = Pt(0)
    pt_f.space_before = Pt(10)
    

    rows = len(current_rpa_info["rpa_time_setting"])+3 if report_setings["show_arc_pause"] else len(current_rpa_info["rpa_time_setting"])+2
    cols = 3+current_rpa_info["arc_times"] if report_setings["show_Irpa"] else 2+current_rpa_info["arc_times"] 
    # Создаём шапку таблицы
    
    tbl=doc.add_table(rows=rows, cols=cols, style='Table Grid') # Таблица с размерами и стилем  , style='Table Grid'

    tbl.cell(0, 0).merge(tbl.cell(1, 0)) 

    if report_setings["show_Irpa"]:
        tbl.cell(0, 1).merge(tbl.cell(1, 1))
        tbl.cell(0, 2).merge(tbl.cell(0, cols-1))

    else:
        tbl.cell(0, 1).merge(tbl.cell(0, cols-1))

    if report_setings["show_arc_pause"]:
        tbl.cell(rows-1, 0).merge(tbl.cell(rows-1, cols-1-current_rpa_info["arc_times"]))

    cell_settings(tbl.cell(0, 0), 'Ступень защиты ВЛ', align="center", font_size=font_size, font_name=font_name)
    tbl.cell(0, 0).width = Inches(0.2)
    

    shift = 0
    if report_setings["show_Irpa"]:
        cell_settings(tbl.cell(0, 1), 'Уставка по току Iкз, кА', align="center", font_size=font_size, font_name=font_name)
        tbl.cell(0, 1).width = Inches(0.2) 
        shift = 1

    cell_settings(tbl.cell(0, 1+shift), 'Время отключения однофазного замыкания на землю Тср.з., с', align="center", font_size=font_size, font_name=font_name)
    tbl.cell(0, 1+shift).width = Inches(0.2) 

    cell_settings(tbl.cell(1, 1+shift), 'Первичное', align="center", font_size=font_size, font_name=font_name)
     
    
    for i in range(current_rpa_info["arc_times"]):
        cell_settings(tbl.cell(1, 2+shift+i), f'АПВ№{i+1}', align="center", font_size=font_size, font_name=font_name)

    if report_setings["show_arc_pause"]:
        cell_settings(tbl.cell(rows-1, 0), 'Длительность паузы между отключением КЗ и срабатыванием АПВ, с', align="center", font_size=font_size, font_name=font_name)
        

        for i, val in enumerate(current_rpa_info["arc_pause"]):
            ind = cols-current_rpa_info["arc_times"]+i
            cell_settings(tbl.cell(rows-1, ind), str(round(val,3)), align="center", font_size=font_size, font_name=font_name)

    
    time_setting = current_rpa_info["rpa_time_setting"]

    sort_ind = sorted([i for i in range(len(time_setting))], key=lambda x:time_setting[x])

    rpa_time_setting = [time_setting[i] for i in sort_ind]
    rpa_I_setting = [current_rpa_info["rpa_I_setting"][i] for i in sort_ind]
    arc_setting = [[current_rpa_info["arc_setting"][j][i] for i in sort_ind] for j in range(len(current_rpa_info["arc_setting"]))]

    if report_setings["show_Irpa"]:
        for i, val in enumerate(rpa_I_setting):
            ind = i+2
            cell_settings(tbl.cell(ind, 1), str(round(val,3)), align="center", font_size=font_size, font_name=font_name)
            

    for i, val in enumerate(rpa_time_setting):
        ind = i+2
        cell_settings(tbl.cell(ind, 1+shift), str(round(val,3)), align="center", font_size=font_size, font_name=font_name)
        cell_settings(tbl.cell(ind, 0), decToRoman(i+1), align="center", font_size=font_size, font_name=font_name)

    for j, lst in enumerate(arc_setting):
        c = j+2+shift
        for i, (val1,val2) in enumerate(zip(rpa_time_setting,lst)):
            ind = i+2
            current_time_arc = round(val1-val2,3) if val1-val2>0 else 0
            cell_settings(tbl.cell(ind, c), str(current_time_arc), align="center", font_size=font_size, font_name=font_name)

def colis(n1,k1,n2,k2):
    b = n1<=n2<k2<=k1 or n1>=n2>k2>=k1 or n2<=n1<k1<=k2 or n2>=n1>k1>=k2 or\
        n1<n2<k1 or n1>n2>k1 or n1<k2<k1 or n1>k2>k1 or\
        n2<n1<k2 or n2>n1>k2 or n2<k1<k2 or n2>k1>k2
    return b

def set_col_widths(table, widths):
    for row in table.rows:
        for idx, width in enumerate(widths):
            row.cells[idx].width = width

def description_settings(doc, okgt_info, vl_info, calc_results, font_size=12, font_name="Times"):
    tbl=doc.add_table(rows=0, cols=5, style='Table Grid')
    for (n,k), val in calc_results.items():
        row_cells = tbl.add_row().cells
        row_cells[0].merge(row_cells[1])
        row_cells[2].merge(row_cells[4])

        cell_settings(row_cells[0], 'Наименование ветви ОКГТ', align="left", font_size=font_size, font_name=font_name)
        cell_settings(row_cells[2], f"{n} - {k}", align="left", font_size=font_size, font_name=font_name)

        for sector in val["sectors"]:
            if sector[1] == "VL":
                st, ed = sector[2:]
                start = val['links'][st][0]
                end = val['links'][ed-1][0]
                
                Vlname = start[0]
                ps_name = vl_info[Vlname]["PSs"][0]["PS_name"]

                groundwires = []
                for i in vl_info[start[0]]["groundwires"]:
                    if i["link_branch"]==start[1] and colis(start[2],end[3],i["supportN"],i["supportK"]):
                        groundwires.append(i)
                
                grounded = []
                for i in vl_info[start[0]]["grounded"]:
                    if i["resistance"]<30.0 and i["link_branch"]==start[1] and colis(start[2],end[3],i["supportN"],i["supportK"]):
                        grounded.append(i)
                
                countercables = []
                for i,(vl_name, branch,_,_) in enumerate(val['links'][st]):
                    if i==0:
                        countercables += [i for i in vl_info[vl_name]["countercables"] if i["link_branch"]==branch and colis(start[2],end[3],i["supportN"],i["supportK"])]
                    else:
                        for item in vl_info[vl_name]["countercables"]:
                            if item["link_branch"]==branch:
                                N = item["supportN"]
                                K = item["supportK"]
                                N_new, K_new = -1,-1
                                for j in range(st,ed):
                                    for link in val['links'][j]:
                                        if (vl_name,branch,N) == link[:3]:
                                            N_new = val['links'][0][2]
                                        if (vl_name,branch,K) == (link[0],link[1],link[3]):
                                            K_new = val['links'][0][3]
                                if N_new!=-1 and K_new!=-1:
                                    d = {"supportN":N_new, "supportK": K_new, "link_branch":start[1]}
                                    if colis(start[2],end[3],d["supportN"],d["supportK"]):
                                        countercables.append({kw:(d[kw] if kw in d else v) for kw, v in item.items()})
                
                support_set = set()
                #print((start[2],end[3]))
                support_set.add(start[2])
                support_set.add(end[3])
                for lst in [grounded,groundwires,countercables]:
                    for item in lst:
                        if start[2]<=item["supportN"]<=end[3] or start[2]>=item["supportN"]>=end[3]:
                            support_set.add(item["supportN"])
                        if start[2]<=item["supportK"]<=end[3] or start[2]>=item["supportK"]>=end[3]:
                            support_set.add(item["supportK"])

                support = sorted(list(support_set),reverse=start[2]>end[3])
                subsectors = [[support[i-1],support[i]] for i in range(1,len(support))]

                #to_ps = set()
                subsectors_info = []
                for N, K in subsectors:
                    wires, ground, conter = None, None, None
                    for item in groundwires:
                        if colis(N,K,item["supportN"],item["supportK"]):
                            okgt = item[item["is_okgt"]]
                            W = k_conductors[okgt]["R0"]
                            gw = item.get(("groundwire2" if item["is_okgt"]=="groundwire1" else "groundwire1"),None)
                            wires = (okgt,W,gw)

                    for item in grounded:
                        if colis(N,K,item["supportN"],item["supportK"]):
                            ground = item["resistance"]

                    for item in countercables:
                        if colis(N,K,item["supportN"],item["supportK"]):
                            connect_to_ps = []
                            if item["connect_to_ps"]:
                                for ps_n, ps_l in val['length_to_ps_lst'][start[0]].items():
                                    if ps_l.get((start[1],N),float('inf')) == 0:
                                        connect_to_ps.append(ps_n)
                                        print("Start", N)
                                    if ps_l.get((start[1],K),float('inf')) == 0:
                                        connect_to_ps.append(ps_n)
                                        print("End", K)
                                    
                            conter = (item["D_countercable"],connect_to_ps)  

                    print(N,K,wires, ground, conter)  
                    subsectors_info.append((N,K,wires, ground, conter))

                if subsectors_info:
                    row_cells = tbl.add_row().cells
                    row_cells[0].merge(row_cells[1])
                    row_cells[2].merge(row_cells[4])

                    cell_settings(row_cells[0], 'Наименование участка ОКГТ', align="left", font_size=font_size, font_name=font_name)
                    cell_settings(row_cells[2], sector[0], align="left", font_size=font_size, font_name=font_name)

                    row_cells = tbl.add_row().cells
                    row_cells[0].merge(row_cells[1])

                    cell_settings(row_cells[0], 'Наименование субучастков ОКГТ', align="center", width=0.05, font_size=font_size, font_name=font_name)
                    row_cells[1].width = Inches(0.05)
                    cell_settings(row_cells[2], 'Сопротивление постоянному току не более, Ом/км', align="center", width=0.1, font_size=font_size, font_name=font_name) 
                    cell_settings(row_cells[3], 'Допустимый тепловой импульс, кА^2', align="center", width=0.1, font_size=font_size, font_name=font_name) 
                    cell_settings(row_cells[4], 'Дополнительные мероприятия', align="center", width=2, font_size=font_size, font_name=font_name)

                    for item in subsectors_info:
                        row_cells1 = tbl.add_row().cells
                        row_cells2 = tbl.add_row().cells
                        row_cells3 = tbl.add_row().cells
                        row_cells4 = tbl.add_row().cells

                        row_cells1[2].merge(row_cells4[2])
                        row_cells1[3].merge(row_cells4[3])
                        row_cells1[4].merge(row_cells4[4])

                        cell_settings(row_cells1[0], 'ВЛ:', align="left", font_size=font_size, font_name=font_name)
                        cell_settings(row_cells2[0], 'Ветвь:', align="left", font_size=font_size, font_name=font_name)
                        cell_settings(row_cells3[0], 'От:', align="left", font_size=font_size, font_name=font_name)
                        cell_settings(row_cells4[0], 'До:', align="left", font_size=font_size, font_name=font_name)

                        cell_settings(row_cells1[1], Vlname, align="left", font_size=font_size, font_name=font_name)
                        cell_settings(row_cells2[1], f'{start[1][0]} - {start[1][1]}', align="left", font_size=font_size, font_name=font_name)

                        fr = round(val['length_to_ps_lst'][Vlname][ps_name][(start[1],item[0])],3)
                        t = round(val['length_to_ps_lst'][Vlname][ps_name][(start[1],item[1])],3)

                        cell_settings(row_cells3[1], f'{fr} км от {ps_name}' , align="left", font_size=font_size, font_name=font_name)
                        cell_settings(row_cells4[1], f'{t} км от {ps_name}', align="left", font_size=font_size, font_name=font_name)

                        #print(item[2])
                        cell_settings(row_cells1[2], str(item[2][1]) , align="center", font_size=font_size, font_name=font_name)
                        cell_settings(row_cells1[3], item[2][0], align="center", font_size=font_size, font_name=font_name)

                        s = []
                        count = 0
                        if item[3] is not None:
                            count += 1
                            s.append(f'{count}. Обеспечить на данном участке сопротивление ЗУ опор не более {round(item[3],2)} Ом')
                            

                        if item[2][2] is not None:
                            count += 1
                            s.append(f'{count}. Подвесить на данном участке второй грозотрос марки {item[2][2]}')
                            
                        
                        if item[4] is not None:
                            count += 1
                            a = f'{count}. ЗУ опор соединить между собой горизонтальным заземлителем из стали круглой диаметром {round(item[4][0],1)} мм'
                            if item[4][1]:
                                a += ' и присоединить к ЗУ %s' % ','.join(item[4][1])
                            s.append(a)

                        advices = ';\n'.join(s)

                        if len(advices)!=0:
                            cell_settings(row_cells1[4], advices+'.', align="left", font_size=font_size, font_name=font_name)
                        else:
                            cell_settings(row_cells1[4], '-', align="center", font_size=font_size, font_name=font_name)
                        


                #print(subsectors)ps_name

    set_col_widths(tbl, (Cm(2),Cm(2.5),Cm(5),Cm(4),Cm(7)))
                
def grounded_wires(doc, calc_results, font_size=12, font_name="Times"):
    tbl=doc.add_table(rows=1, cols=2, style='Table Grid')
    recomends = list(set().union(*[i['okgt_types'] for i in calc_results.values()]).difference(set([None])))
    recomends = sorted(recomends, key=lambda x: k_conductors[x]["Bsc"])
    cell_settings(tbl.cell(0, 0), 'Допустимый тепловой импульс ОКГТ, кА^2\u2E31с', align="center", font_size=font_size, font_name=font_name)
    cell_settings(tbl.cell(0, 1), 'Марка заземляющего проводника', align="center", font_size=font_size, font_name=font_name)
    for item in recomends:
        if k_conductors[item]["Grounded_conductor"] is not None:
            row_cells = tbl.add_row().cells
            cell_settings(row_cells[0], str(int(k_conductors[item]["Bsc"])), align="center", font_size=font_size, font_name=font_name)
            cell_settings(row_cells[1], k_conductors[item]["Grounded_conductor"], align="center", font_size=font_size, font_name=font_name)
            

    


def memorandum(okgt_info, vl_info, rpa_info, calc_results, report_setings):
    doc = DocxTemplate("docx_templates/memorandum.docx")
    context = { 
        'recipients' : R('\n'.join([i.strip() for i in report_setings['recipients'].split(';')])),
        "project_name" : report_setings['project_name']
    }
    doc.render(context)
    doc.save("docx_templates/midle_memorandum.docx")

    document = Document("docx_templates/midle_memorandum.docx")
    #document = Document()

    # Наследуем стиль и изменяем его
    style = document.styles['Normal'] # Берём стиль Нормальный
    f0 = style.font # Переменная для изменения параметров стиля
    f0.name = 'Times' # Шрифт
    f0.size = Pt(14) # Размер шрифта

    for i, ((vl_name,ps_name), rpa) in enumerate(rpa_info.items()):
        rpa_settings_table(document, i+1, vl_name, ps_name, rpa, report_setings)

    
    p1=document.add_paragraph()
    p1.add_run('Тестовый текст')
    p1.runs[0].font.size = Pt(9) #Меняем размер шрифта параграфа
    pt_f = p1.paragraph_format
    pt_f.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pt_f.space_after = Pt(0)
    pt_f.space_before = Pt(10)

    description_settings(document,okgt_info, vl_info, calc_results)

    p1=document.add_paragraph()
    p1.add_run('Тестовый текст')
    p1.runs[0].font.size = Pt(9) #Меняем размер шрифта параграфа
    pt_f = p1.paragraph_format
    pt_f.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pt_f.space_after = Pt(0)
    pt_f.space_before = Pt(10)


    grounded_wires(document, calc_results)


    


    document.save("docx_templates/test_memorandum.docx")
    print('memorandum was made')

    