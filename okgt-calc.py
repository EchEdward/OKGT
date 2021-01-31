import numpy as np

from scipy.integrate import simps
from scipy.constants import epsilon_0

import scipy.sparse as sparse
import scipy.sparse.linalg as linalg

from initial_data import okgt_info, vl_info


""" 
# graf of power station
Aps = sparse.lil_matrix((10,5),dtype=np.float64)
for i in range(5):
   Aps[i,i] = 1
   Aps[i+5,i+5] = -1

# graf of okgt with transmision line
Aokgt1n = sparse.lil_matrix((6,6),dtype=np.float64)
for i in range(6):
   Aokgt1n[i,i] = 1
Aokgt1k = - Aokgt1n

# graf of single conductive okgt 
Aokgt2n = sparse.lil_matrix((2,2),dtype=np.float64)
for i in range(6):
   Aokgt2n[i,i] = 1
Aokgt2k = - Aokgt2n

# graf of single dielectric okgt 
Aokgt3n = sparse.lil_matrix((1,1),dtype=np.float64)
for i in range(6):
   Aokgt3n[i,i] = 1
Aokgt3k = - Aokgt3n

# graf of transmision line without okgt 
Atrlnn = sparse.lil_matrix((5,5),dtype=np.float64)
for i in range(5):
   Atrlnn[i,i] = 1
Atrlnk = - Atrlnn 
"""

def get_vl_sector(key):
    lst = []
    for name, value in vl_info.items():
        branches = {}
        for k, branch in value["branches"].items():
            branches[k] = (branch["supportN"],branch["supportK"])
        
        for sector in value["sectors"]:
            if sector["type"] == "with_okgt":
                if sector["link_okgt"] == key:
                    d_sector = {k:v for k,v in sector.items()}
                    d_sector["branch_supports"] = branches[d_sector["link_branch"]]
                    d_sector["name_vl"] = name
                    lst.append(d_sector)
    return lst   


def find_entry(lst, length):
    dl = 0.0001
    ln, lk = 0,  length
    order = []
    len_lst  = len(lst)
    for _ in range(len_lst):
        for i, val in enumerate(lst):
            if i in order: 
                continue
            if ln-dl<=val['lengthN']<=ln+dl and val['lengthK']<=lk+dl:
                order.append(i)
                ln = val['lengthK']

        if len_lst == len(order):
            #print("exit")
            break

    else:
        raise Exception("Entries were not found")
        #return "lol"

    return order

def sector_entry(lst,branch):
    new_lst = [i for i,val in enumerate(lst) if val["link_branch"]==branch]
    if len(new_lst) == 0:
        raise Exception("Entries were not found 3")
    count = 0
    for i in new_lst:
        if lst[i]["supportN"]<lst[i]["supportK"]:
            count+=1
    #print(count, len(new_lst))
    if count != len(new_lst) and count != 0:
        raise Exception("Entries were not found 1")

    derection = count == len(new_lst)
    order = sorted(new_lst, key=lambda x: lst[x]["supportN"], reverse=not derection)
    for i in range(1,len(new_lst)):
        if lst[order[i]]["supportN"] != lst[order[i-1]]["supportK"]:
            raise Exception("Entries were not found 2")

    return order

#print(sector_entry(vl_info["VL #4"]["sectors"],("3","4")))

#print(get_vl_sector("one"))
# Construct graph of okgt's links
nodes_position = {}
i, j = 0, 0
lst_conections = []
lst_cc_conections = []

for (n, k), sectors in okgt_info.items():
    if n not in nodes_position:
        nodes_position[n] = (i,j)

    
    for ind, sector in enumerate(sectors):
        if sector["type"] == "VL":
            vl_sectors = get_vl_sector(sector["name"])
            vl_sectors = [vl_sectors[i] for i in find_entry(vl_sectors,sector["length"])]

            for m, vl_sector in enumerate(vl_sectors):
                N, K = vl_sector['supportN'], vl_sector['supportK']
                drct = int((K-N)/abs(K-N))
                gen = zip(range(abs(K-N)),range(N,K,drct),range(N+drct,K+drct,drct))
                dl = abs(vl_sector['lengthK']-vl_sector['lengthN'])/abs(K-N)
                
                for t, nc, kc in gen:
                    if ind == 0 and m==0 and t==0 and n in nodes_position:
                        i_old = nodes_position[n][0]
                        start = (i_old,j,-1)
                    else:
                        start = (i,j,-1)
                    i += 1
                    end = (i,j,1)
                    j += 1

                    d_row = {
                        "start": start,
                        "end": end,
                        "type":"VL",
                        'supportN': nc,
                        'supportK': kc,
                        "length":dl,
                        "link_branch":vl_sector["link_branch"],
                        "name_vl":vl_sector["name_vl"],
                        "link_okgt": sector["name"]
                        }
                    lst_conections.append(d_row)

  
        elif sector["type"] == "single_dielectric":
            if ind == 0 and n in nodes_position:
                i_old = nodes_position[n][0]
                start = (i_old,j,-1)
            else:
                start = (i,j,-1)
            i += 1
            end = (i,j,1)
            j += 1
            d_row = {"start": start, "end": end, "length":sector["length"], "type":sector["type"]}
            lst_conections.append(d_row )
                
        elif sector["type"] == "single_conductive":
            if sector["way_grounded"] == "not":
                v = sector["point_grounded"]+1
            elif sector["way_grounded"] in ["left", "right"]:
                v = sector["point_grounded"]
            elif sector["way_grounded"] == "both":
                v = sector["point_grounded"]-1
            dl = sector["length"]/v
            for m in range(v):
                if ind == 0 and m==0 and n in nodes_position:
                    i_old = nodes_position[n][0]
                    start = (i_old,j,-1)
                else:
                    start = (i,j,-1)
                i += 1
                end = (i,j,1)
                j += 1
                d_row = {
                    "start": start,
                    "end": end,
                    "type": sector["type"],
                    'supportN': m,
                    'supportK': m+1,
                    "link_okgt": sector["name"],
                    "length":dl,
                    "groundwire": sector["groundwire"], 
                    "H_cable":sector["H_cable"],
                    "countercable": sector["countercable"]
                    }
                lst_conections.append(d_row)
                if sector["countercable"]:
                    lst_cc_conections.append({"is_vl":False, "s":start,"e":end,"length":dl,"sector":sector,})

            

    if k not in nodes_position:
        nodes_position[k] = (i,j)


#print(nodes_position)
""" for row in lst_conections:
    print(row) """

def get_vl_sector_info(vl,branch,supports,dtype):
    #"phases", "conductors", "groundwires", "supports", "PSs"
    f = lambda ni,ki,ns,ks: (ni<ki and ns>=ni and ks<=ki) or (ni>ki and ns<=ni and ks>=ki)
    if dtype["name"] == "conductors":
        for item in vl_info[vl]["conductors"]:
            if item["link_branch"]==branch and f(item["supportN"],item["supportK"],supports[0],supports[1]):
                return {"c1":item["conductor"],"c2":item["conductor"],"c3":item["conductor"]}

    elif dtype["name"] == "phases":
        for item in vl_info[vl]["phases"]:
            if item["link_branch"]==branch and f(item["supportN"],item["supportK"],supports[0],supports[1]):
                return {"p1":item["phase"][0],"p2":item["phase"][1],"p3":item["phase"][2]}

    elif dtype["name"] =="supports":
        for item in vl_info[vl]["supports"]:
            if item["link_branch"]==branch and f(item["supportN"],item["supportK"],supports[0],supports[1]):
                return {"s1":item["support"],"s2":item["support"],"s3":item["support"],"s4":item["support"],"s5":item["support"]}

    elif dtype["name"] =="groundwires":
        for item in vl_info[vl]["groundwires"]:
            if item["link_branch"]==branch and f(item["supportN"],item["supportK"],supports[0],supports[1]):
                if item["type"] == "one":
                    if item["is_okgt"] is None:
                        return {"gw1":item["groundwire1"],"gw2":None,"is_okgt":None}
                    elif item["is_okgt"] is not None and item["is_okgt"]=="groundwire1":
                        return {"gw1":item["groundwire1"],"gw2":None, "is_okgt":"gw1"}
                elif item["type"] == "two":
                    if item["is_okgt"] is None:
                        return {"gw1":item["groundwire1"],"gw2":item["groundwire2"],"is_okgt":None}
                    elif item["is_okgt"] is not None and item["is_okgt"]=="groundwire1":
                        return {"gw1":item["groundwire1"],"gw2":item["groundwire2"],"is_okgt":"gw1"}
                    elif item["is_okgt"] is not None and item["is_okgt"]=="groundwire2":
                        return {"gw1":item["groundwire1"],"gw2":item["groundwire2"],"is_okgt":"gw2"}
        else:
            return {"gw1":None,"gw2":None,"is_okgt":None}

    elif dtype["name"] =="PSs":
        for item in vl_info[vl]["PSs"]:
            if vl_info[vl]["branches"][branch][dtype["side"]] == item["PS_name"]:
                return {"length":item["length"]}

    #"countercables"
    elif dtype["name"] =="countercables":
        for item in vl_info[vl]["countercables"]:
            if item["link_branch"]==branch and f(item["supportN"],item["supportK"],supports[0],supports[1]):
                return item
        else:
            return None

    raise Exception("Supports %s don't exist in %s %s %s" % (str(supports),vl,str(branch),dtype["name"]))


# Construct graph of transmission lines' links
lst_vl_conections = []
i += 1

s_i_vl, s_j_vl = i,j

for vl_name, vl in vl_info.items():
    nodes_position = {}
    for key, branch in vl["branches"].items():
        if key[0] not in nodes_position:
            nodes_position[key[0]] = (i,j)

        add_Ps = False
        if branch["PS"] in ["both", "left"]:
            add_Ps = True
            nodes_position[key[0]] = (i,j)
        trig_first = False
        order = sector_entry(vl["sectors"],key)
        #print(key, order)
        for sector in [vl["sectors"][i] for i in order]:
            #print(key, sector["link_branch"])
            if key == sector["link_branch"]:
                #print("aaaaaaaaaa")
                N, K = sector["supportN"], sector["supportK"]
                drct = int((K-N)/abs(K-N))
                gen = zip(range(abs(K-N)),range(N,K,drct),range(N+drct,K+drct,drct))
                

                if sector["type"]=="with_okgt":
                    dl = abs(sector['lengthK']-sector['lengthN'])/abs(K-N)
                elif sector["type"]=="without_okgt":
                    dl = abs(sector['length'])/abs(K-N)

                for t, nc, kc in gen:
                    data1,data2,data3,data4,data5 = {},{},{},{},{}

                    keyword = ["name_vl","supportN","supportK","link_branch"]
                    dt = [vl_name, nc, kc, key]
                    for kw,rz in zip(keyword,dt):
                        data1[kw],data2[kw],data3[kw],data4[kw],data5[kw] = rz,rz,rz,rz,rz

                    #"phases", "conductors", "groundwires", "supports"
                    phases = get_vl_sector_info(vl_name,key,(nc, kc,),{"name":"phases"})
                    conductors = get_vl_sector_info(vl_name,key,(nc, kc,),{"name":"conductors"})
                    supports = get_vl_sector_info(vl_name,key,(nc, kc,),{"name":"supports"})
                    groundwires = get_vl_sector_info(vl_name,key,(nc, kc,),{"name":"groundwires"})
                    countercables = get_vl_sector_info(vl_name,key,(nc, kc,),{"name":"countercables"})


                    keyword = ["type","is_Ps_sector","length","Tsupport","phase","conductor"] #"start","end",
                    d1 = [sector["type"],False,dl,supports["s1"],phases["p1"],conductors["c1"]] #s1,e1,
                    d2 = [sector["type"],False,dl,supports["s2"],phases["p2"],conductors["c2"]] #s2,e2,
                    d3 = [sector["type"],False,dl,supports["s3"],phases["p3"],conductors["c3"]] #s3,e3,
                    d4 = [sector["type"],False,dl,supports["s4"],"T1",{"gw1":groundwires["gw1"],"is_okgt":groundwires["is_okgt"]}] #s4,e4,
                    d5 = [sector["type"],False,dl,supports["s5"],"T2",{"gw1":groundwires["gw1"],"is_okgt":groundwires["is_okgt"]}] #s5,e5,

                    for kw,rz1,rz2,rz3,rz4,rz5 in zip(keyword,d1,d2,d3,d4,d5):
                        data1[kw],data2[kw],data3[kw],data4[kw],data5[kw] = rz1,rz2,rz3,rz4,rz5

                    if not trig_first and t==0 and key[0] in nodes_position:
                        if not add_Ps:
                            trig_first = True
                            i_old = nodes_position[key[0]][0]
                            s1,s2,s3,s4,s5 = (i_old,j,-1),(i_old+1,j+1,-1),(i_old+2,j+2,-1),(i_old+3,j+3,-1),(i_old+4,j+4,-1)
                            i+=5
                            e1,e2,e3,e4,e5= (i,j,1),(i+1,j+1,1),(i+2,j+2,1),(i+3,j+3,1),(i+4,j+4,1)
                        else:
                            trig_first = True
                            add_Ps = False
                            i_old = nodes_position[key[0]][0]
                            s1,s2,s3,s4,s5 = (i_old,j,-1),(i_old+1,j+1,-1),(i_old+2,j+2,-1),(i_old+3,j+3,-1),(i_old+4,j+4,-1)
                            i+=5
                            e1,e2,e3,e4,e5= (i,j,1),(i+1,j+1,1),(i+2,j+2,1),(i+3,j+3,1),(i+4,j+4,1)
                            j += 5
                            ps = get_vl_sector_info(vl_name,key,(nc, kc,),{"name":"PSs","side":"PS_name_1"})
                            lst_vl_conections.append({"start":s1,"end":e1,**data1,"length":ps["length"],"is_Ps_sector":True})
                            lst_vl_conections.append({"start":s2,"end":e2,**data2,"length":ps["length"],"is_Ps_sector":True})
                            lst_vl_conections.append({"start":s3,"end":e3,**data3,"length":ps["length"],"is_Ps_sector":True})
                            lst_vl_conections.append({"start":s4,"end":e4,**data4,"length":ps["length"],"is_Ps_sector":True})
                            lst_vl_conections.append({"start":s5,"end":e5,**data5,"length":ps["length"],"is_Ps_sector":True})
                            
                            s1,s2,s3,s4,s5 = (i,j,-1),(i+1,j+1,-1),(i+2,j+2,-1),(i+3,j+3,-1),(i+4,j+4,-1)
                            i += 5
                            e1,e2,e3,e4,e5= (i,j,1),(i+1,j+1,1),(i+2,j+2,1),(i+3,j+3,1),(i+4,j+4,1)
                            

                    else:
                        s1,s2,s3,s4,s5 = (i,j,-1),(i+1,j+1,-1),(i+2,j+2,-1),(i+3,j+3,-1),(i+4,j+4,-1)
                        i += 5
                        e1,e2,e3,e4,e5= (i,j,1),(i+1,j+1,1),(i+2,j+2,1),(i+3,j+3,1),(i+4,j+4,1)

                    
                    #e1,e2,e3,e4,e5= (i,j,1),(i+1,j+1,1),(i+2,j+2,1),(i+3,j+3,1),(i+4,j+4,1)
                    j += 5

                
                    lst_vl_conections.append({"start":s1,"end":e1,**data1})
                    lst_vl_conections.append({"start":s2,"end":e2,**data2})
                    lst_vl_conections.append({"start":s3,"end":e3,**data3})
                    lst_vl_conections.append({"start":s4,"end":e4,**data4})
                    lst_vl_conections.append({"start":s5,"end":e5,**data5})

                    if countercables is not None:
                        lst_cc_conections.append({"is_vl":True, "s":s4,"e":e4,"length":dl,"sector":countercables})


        if branch["PS"] in ["both", "right"]:
            s1,s2,s3,s4,s5 = (i,j,-1),(i+1,j+1,-1),(i+2,j+2,-1),(i+3,j+3,-1),(i+4,j+4,-1)
            i += 5
            e1,e2,e3,e4,e5= (i,j,1),(i+1,j+1,1),(i+2,j+2,1),(i+3,j+3,1),(i+4,j+4,1)
            ps = get_vl_sector_info(vl_name,key,(nc, kc,),{"name":"PSs","side":"PS_name_2"})
            lst_vl_conections.append({"start":s1,"end":e1,**data1,"length":ps["length"],"is_Ps_sector":True})
            lst_vl_conections.append({"start":s2,"end":e2,**data2,"length":ps["length"],"is_Ps_sector":True})
            lst_vl_conections.append({"start":s3,"end":e3,**data3,"length":ps["length"],"is_Ps_sector":True})
            lst_vl_conections.append({"start":s4,"end":e4,**data4,"length":ps["length"],"is_Ps_sector":True})
            lst_vl_conections.append({"start":s5,"end":e5,**data5,"length":ps["length"],"is_Ps_sector":True})
            
            i+=5
            j+=5
            

        if key[1] not in nodes_position:
            nodes_position[key[1]] = (i,j)


s_i_сс, s_j_сс = i,j
cc_lst_conections = []
for item in lst_cc_conections:
    d = {"is_vl":item["is_vl"],
        "start":(item["s"][0],j,-1),
        "end":(item["e"][0],j,1),
        "link_s":item["s"],
        "link_e":item["e"],
        "length":item["length"],
        "H_countercable":item["sector"]["H_countercable"],
        "X_countercable": item["sector"]["X_countercable"],
        "D_countercable": item["sector"]["D_countercable"],
        "ground_resistance": item["sector"]["ground_resistance"],
        }
    cc_lst_conections.append(d)
    
    j+=1

    #i+=1
    #j+=1
    #print(nodes_position)
""" for row in lst_vl_conections:
    print(row) """


""" for row in cc_lst_conections:
    print(row) """

