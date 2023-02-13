import math
from flask import Flask, request, url_for, render_template, redirect, jsonify
app = Flask(__name__)

@app.route('/singleSource', methods=['POST'])
def singleSource():
    inputdata = request.get_json()
    column = int(Column_cal(inputdata['waterlevel']))
    row = int(Row_cal(inputdata['waterlevel'], column))
    chem = inputdata['chem']
    S = float(inputdata['value_S'])
    Hc = float(inputdata['value_Hc'])
    Dair = float(inputdata['value_Dair'])
    Dwater = float(inputdata['value_Dwater'])
    DHvb = float(inputdata['value_DHvb'])
    Tc = float(inputdata['value_Tc'])
    Tb = float(inputdata['value_Tb'])
    IUR_input = inputdata['value_IUR']
    if IUR_input=="NULL":
        IUR = 0
    else:
        IUR = float(IUR_input)
    Rfc_input = inputdata['value_Rfc']
    if Rfc_input=="NULL":
        Rfc = 0
    else:
        Rfc = float(Rfc_input)
    Mut = inputdata['value_Mut']
    Type = inputdata['conc_type']
    Ts = float(inputdata['Ts']) + 273.15
    Organic = 0#int(inputdata['value_Organic'])
    Koc_input = inputdata['value_Koc']
    if Koc_input=="NULL":
        Koc = 0
    else:
        Koc = Koc_input
    foc = float(inputdata['value_foc'])
    kd = 1#float(inputdata['value_kd'])
    # grid input start
    if Type == "sat":
        Cmedium_input = Stringbreak(inputdata['sat_soilconc'], column, row)
    elif Type == "unsat":
        Cmedium_input = Stringbreak(inputdata['unsat_soilconc'], column, row)
    else:
        Cmedium_input = Stringbreak(inputdata['sat_soilconc'], column, row)
        Cmedium2_input = Stringbreak(inputdata['unsat_soilconc'], column, row)
    WT_input = Stringbreak(inputdata['waterlevel'], column, row)
    LE_input = Stringbreak(inputdata['elevation'], column, row)
    Geo_Type_input = Stringbreak(inputdata['Geo_Type'], column, row)
    # Geo Type start
    try:
        hSA13 = float(inputdata['hSA_13'])
        hSA14 = float(inputdata['hSA_14'])
        hSA15 = float(inputdata['hSA_15'])
        hSA16 = float(inputdata['hSA_16'])
        hSA17 = float(inputdata['hSA_17'])
        hSA18 = float(inputdata['hSA_18'])
        hSA19 = float(inputdata['hSA_19'])
        hSA20 = float(inputdata['hSA_20'])
    except:
        pass
    try:
        nSA13 = float(inputdata['nSA_13'])
        nSA14 = float(inputdata['nSA_14'])
        nSA15 = float(inputdata['nSA_15'])
        nSA16 = float(inputdata['nSA_16'])
        nSA17 = float(inputdata['nSA_17'])
        nSA18 = float(inputdata['nSA_18'])
        nSA19 = float(inputdata['nSA_19'])
        nSA20 = float(inputdata['nSA_20'])
    except:
        pass
    try:
        nwSA13 = float(inputdata['nwSA_13'])
        nwSA14 = float(inputdata['nwSA_14'])
        nwSA15 = float(inputdata['nwSA_15'])
        nwSA16 = float(inputdata['nwSA_16'])
        nwSA17 = float(inputdata['nwSA_17'])
        nwSA18 = float(inputdata['nwSA_18'])
        nwSA19 = float(inputdata['nwSA_19'])
        nwSA20 = float(inputdata['nwSA_20'])
    except:
        pass
    try:
        rhoSA13 = float(inputdata['rhoSA_13'])
        rhoSA14 = float(inputdata['rhoSA_14'])
        rhoSA15 = float(inputdata['rhoSA_15'])
        rhoSA16 = float(inputdata['rhoSA_16'])
        rhoSA17 = float(inputdata['rhoSA_17'])
        rhoSA18 = float(inputdata['rhoSA_18'])
        rhoSA19 = float(inputdata['rhoSA_19'])
        rhoSA20 = float(inputdata['rhoSA_20'])
    except:
        pass
    try:
        hcz13 = float(inputdata['hcz_13'])
        hcz14 = float(inputdata['hcz_14'])
        hcz15 = float(inputdata['hcz_15'])
        hcz16 = float(inputdata['hcz_16'])
        hcz17 = float(inputdata['hcz_17'])
        hcz18 = float(inputdata['hcz_18'])
        hcz19 = float(inputdata['hcz_19'])
        hcz20 = float(inputdata['hcz_20'])
    except:
        pass
    try:
        ncz13 = float(inputdata['ncz_13'])
        ncz14 = float(inputdata['ncz_14'])
        ncz15 = float(inputdata['ncz_15'])
        ncz16 = float(inputdata['ncz_16'])
        ncz17 = float(inputdata['ncz_17'])
        ncz18 = float(inputdata['ncz_18'])
        ncz19 = float(inputdata['ncz_19'])
        ncz20 = float(inputdata['ncz_20'])
    except:
        pass
    try:
        nwcz13 = float(inputdata['nwcz_13'])
        nwcz14 = float(inputdata['nwcz_14'])
        nwcz15 = float(inputdata['nwcz_15'])
        nwcz16 = float(inputdata['nwcz_16'])
        nwcz17 = float(inputdata['nwcz_17'])
        nwcz18 = float(inputdata['nwcz_18'])
        nwcz19 = float(inputdata['nwcz_19'])
        nwcz20 = float(inputdata['nwcz_20'])
    except:
        pass
    # Geo Type end
    buildingType_input = Stringbreak(inputdata['Found_Type'], column, row)
    # Building Type start
    try:
        Lb11 = float(inputdata['LB_11'])
        Lb12 = float(inputdata['LB_12'])
        Lb13 = float(inputdata['LB_13'])
        Lb14 = float(inputdata['LB_14'])
        Lb15 = float(inputdata['LB_15'])
        Lb16 = float(inputdata['LB_16'])
        Lb17 = float(inputdata['LB_17'])
        Lb18 = float(inputdata['LB_18'])
        Lb19 = float(inputdata['LB_19'])
        Lb20 = float(inputdata['LB_20'])
    except:
        pass
    try:
        Lf11 = float(inputdata['Lf_11'])
        Lf12 = float(inputdata['Lf_12'])
        Lf13 = float(inputdata['Lf_13'])
        Lf14 = float(inputdata['Lf_14'])
        Lf15 = float(inputdata['Lf_15'])
        Lf16 = float(inputdata['Lf_16'])
        Lf17 = float(inputdata['Lf_17'])
        Lf18 = float(inputdata['Lf_18'])
        Lf19 = float(inputdata['Lf_19'])
        Lf20 = float(inputdata['Lf_20'])
    except:
        pass
    try:
        eta11 = float(inputdata['eta_11'])
        eta12 = float(inputdata['eta_12'])
        eta13 = float(inputdata['eta_13'])
        eta14 = float(inputdata['eta_14'])
        eta15 = float(inputdata['eta_15'])
        eta16 = float(inputdata['eta_16'])
        eta17 = float(inputdata['eta_17'])
        eta18 = float(inputdata['eta_18'])
        eta19 = float(inputdata['eta_19'])
        eta20 = float(inputdata['eta_20'])
    except:
        pass
    try:
        Abf11 = float(inputdata['Abf_11'])
        Abf12 = float(inputdata['Abf_12'])
        Abf13 = float(inputdata['Abf_13'])
        Abf14 = float(inputdata['Abf_14'])
        Abf15 = float(inputdata['Abf_15'])
        Abf16 = float(inputdata['Abf_16'])
        Abf17 = float(inputdata['Abf_17'])
        Abf18 = float(inputdata['Abf_18'])
        Abf19 = float(inputdata['Abf_19'])
        Abf20 = float(inputdata['Abf_20'])
    except:
        pass
    try:
        Hb11 = float(inputdata['Hb_11'])
        Hb12 = float(inputdata['Hb_12'])
        Hb13 = float(inputdata['Hb_13'])
        Hb14 = float(inputdata['Hb_14'])
        Hb15 = float(inputdata['Hb_15'])
        Hb16 = float(inputdata['Hb_16'])
        Hb17 = float(inputdata['Hb_17'])
        Hb18 = float(inputdata['Hb_18'])
        Hb19 = float(inputdata['Hb_19'])
        Hb20 = float(inputdata['Hb_20'])
    except:
        pass
    try:
        ach11 = float(inputdata['ach_11'])
        ach12 = float(inputdata['ach_12'])
        ach13 = float(inputdata['ach_13'])
        ach14 = float(inputdata['ach_14'])
        ach15 = float(inputdata['ach_15'])
        ach16 = float(inputdata['ach_16'])
        ach17 = float(inputdata['ach_17'])
        ach18 = float(inputdata['ach_18'])
        ach19 = float(inputdata['ach_19'])
        ach20 = float(inputdata['ach_20'])
    except:
        pass
    try:
        Qsoil_Qb11 = float(inputdata['Qsoil_Qb_11'])
        Qsoil_Qb12 = float(inputdata['Qsoil_Qb_12'])
        Qsoil_Qb13 = float(inputdata['Qsoil_Qb_13'])
        Qsoil_Qb14 = float(inputdata['Qsoil_Qb_14'])
        Qsoil_Qb15 = float(inputdata['Qsoil_Qb_15'])
        Qsoil_Qb16 = float(inputdata['Qsoil_Qb_16'])
        Qsoil_Qb17 = float(inputdata['Qsoil_Qb_17'])
        Qsoil_Qb18 = float(inputdata['Qsoil_Qb_18'])
        Qsoil_Qb19 = float(inputdata['Qsoil_Qb_19'])
        Qsoil_Qb20 = float(inputdata['Qsoil_Qb_20'])
    except:
        pass
    # Building Type end
    Ex_input = Stringbreak(inputdata['Expo_Type'], column, row)
    # Ex start
    try:
        EF3 = float(inputdata['EF_3'])
        EF4 = float(inputdata['EF_4'])
        EF5 = float(inputdata['EF_5'])
    except:
        pass
    try:
        ED3 = float(inputdata['ED_3'])
        ED4 = float(inputdata['ED_4'])
        ED5 = float(inputdata['ED_5'])
    except:
        pass
    try:
        ET3 = float(inputdata['ET_3'])
        ET4 = float(inputdata['ET_4'])
        ET5 = float(inputdata['ET_5'])
    except:
        pass
    # Ex end
    Cmedium = [[0 for j in range(row)] for i in range(column)]
    Cmedium2 = [[0 for j in range(row)] for i in range(column)]
    WT = [[0 for j in range(row)] for i in range(column)]
    LE = [[0 for j in range(row)] for i in range(column)]
    Geo_Type = [[0 for j in range(row)] for i in range(column)]
    nSA = [[0 for j in range(row)] for i in range(column)]
    nwSA = [[0 for j in range(row)] for i in range(column)]
    nairSA = [[0 for j in range(row)] for i in range(column)]
    rhoSA = [[0 for j in range(row)] for i in range(column)]
    hcz = [[0 for j in range(row)] for i in range(column)]
    ncz = [[0 for j in range(row)] for i in range(column)]
    nwcz = [[0 for j in range(row)] for i in range(column)]
    buildingType = [[0 for j in range(row)] for i in range(column)]
    Lb = [[0 for j in range(row)] for i in range(column)]
    Lf = [[0 for j in range(row)] for i in range(column)]
    eta = [[0 for j in range(row)] for i in range(column)]
    Abf = [[0 for j in range(row)] for i in range(column)]
    Hb = [[0 for j in range(row)] for i in range(column)]
    ach = [[0 for j in range(row)] for i in range(column)]
    Qsoil_Qb = [[0 for j in range(row)] for i in range(column)]
    Ex = [[0 for j in range(row)] for i in range(column)]
    ATnc = [[0 for j in range(row)] for i in range(column)]
    EF = [[0 for j in range(row)] for i in range(column)]
    ED = [[0 for j in range(row)] for i in range(column)]
    ET = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            if Type != "both":
                Cmedium[i][j] = float(Cmedium_input[i][j])
            else:
                Cmedium[i][j] = float(Cmedium_input[i][j])
                Cmedium2[i][j] = float(Cmedium2_input[i][j])
            LE[i][j] = float(LE_input[i][j])
            WT[i][j] = float(WT_input[i][j])
            Geo_Type[i][j] = int(Geo_Type_input[i][j])
            if Geo_Type[i][j] == 1:
                nSA[i][j] = 0.459
                nwSA[i][j] = 0.215
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.43
                hcz[i][j] = 0.815217391
                ncz[i][j] = 0.459
                nwcz[i][j] = 0.41185514
            elif Geo_Type[i][j] == 2:
                nSA[i][j] = 0.442
                nwSA[i][j] = 0.168
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.48
                hcz[i][j] = 0.46875
                ncz[i][j] = 0.442
                nwcz[i][j] = 0.375117458
            elif Geo_Type[i][j] == 3:
                nSA[i][j] = 0.399
                nwSA[i][j] = 0.148
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.59
                hcz[i][j] = 0.375
                ncz[i][j] = 0.399
                nwcz[i][j] = 0.331630276
            elif Geo_Type[i][j] == 4:
                nSA[i][j] = 0.39
                nwSA[i][j] = 0.076
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.62
                hcz[i][j] = 0.1875
                ncz[i][j] = 0.39
                nwcz[i][j] = 0.302585409
            elif Geo_Type[i][j] == 5:
                nSA[i][j] = 0.375
                nwSA[i][j] = 0.054
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.66
                hcz[i][j] = 0.170454545
                ncz[i][j] = 0.375
                nwcz[i][j] = 0.253258113
            elif Geo_Type[i][j] == 6:
                nSA[i][j] = 0.385
                nwSA[i][j] = 0.197
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.63
                hcz[i][j] = 0.3
                ncz[i][j] = 0.385
                nwcz[i][j] = 0.354846864
            elif Geo_Type[i][j] == 7:
                nSA[i][j] = 0.384
                nwSA[i][j] = 0.146
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.63
                hcz[i][j] = 0.25862069
                ncz[i][j] = 0.384
                nwcz[i][j] = 0.333283473
            elif Geo_Type[i][j] == 8:
                nSA[i][j] = 0.387
                nwSA[i][j] = 0.103
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.62
                hcz[i][j] = 0.25
                ncz[i][j] = 0.387
                nwcz[i][j] = 0.31973079
            elif Geo_Type[i][j] == 9:
                nSA[i][j] = 0.489
                nwSA[i][j] = 0.167
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.35
                hcz[i][j] = 1.630434783
                ncz[i][j] = 0.489
                nwcz[i][j] = 0.381686648
            elif Geo_Type[i][j] == 10:
                nSA[i][j] = 0.439
                nwSA[i][j] = 0.18
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.49
                hcz[i][j] = 0.681818182
                ncz[i][j] = 0.439
                nwcz[i][j] = 0.348694517
            elif Geo_Type[i][j] == 11:
                nSA[i][j] = 0.481
                nwSA[i][j] = 0.216
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.38
                hcz[i][j] = 1.923076923
                ncz[i][j] = 0.481
                nwcz[i][j] = 0.423644962
            elif Geo_Type[i][j] == 12:
                nSA[i][j] = 0.482
                nwSA[i][j] = 0.198
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = 1.37
                hcz[i][j] = 1.339285714
                ncz[i][j] = 0.482
                nwcz[i][j] = 0.399159996
            elif Geo_Type[i][j] == 13:
                nSA[i][j] = nSA13
                nwSA[i][j] = nwSA13
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = rhoSA13
                hcz[i][j] = hcz13
                ncz[i][j] = ncz13
                nwcz[i][j] = nwcz13
            elif Geo_Type[i][j] == 14:
                nSA[i][j] = nSA14
                nwSA[i][j] = nwSA14
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = rhoSA14
                hcz[i][j] = hcz14
                ncz[i][j] = ncz14
                nwcz[i][j] = nwcz14
            elif Geo_Type[i][j] == 15:
                nSA[i][j] = nSA15
                nwSA[i][j] = nwSA15
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = rhoSA15
                hcz[i][j] = hcz15
                ncz[i][j] = ncz15
                nwcz[i][j] = nwcz15
            elif Geo_Type[i][j] == 16:
                nSA[i][j] = nSA16
                nwSA[i][j] = nwSA16
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = rhoSA16
                hcz[i][j] = hcz16
                ncz[i][j] = ncz16
                nwcz[i][j] = nwcz16
            elif Geo_Type[i][j] == 17:
                nSA[i][j] = nSA17
                nwSA[i][j] = nwSA17
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = rhoSA17
                hcz[i][j] = hcz17
                ncz[i][j] = ncz17
                nwcz[i][j] = nwcz17
            elif Geo_Type[i][j] == 18:
                nSA[i][j] = nSA18
                nwSA[i][j] = nwSA18
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = rhoSA18
                hcz[i][j] = hcz18
                ncz[i][j] = ncz18
                nwcz[i][j] = nwcz18
            elif Geo_Type[i][j] == 19:
                nSA[i][j] = nSA19
                nwSA[i][j] = nwSA19
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = rhoSA19
                hcz[i][j] = hcz19
                ncz[i][j] = ncz19
                nwcz[i][j] = nwcz19
            elif Geo_Type[i][j] == 20:
                nSA[i][j] = nSA20
                nwSA[i][j] = nwSA20
                nairSA[i][j] = nSA[i][j] - nwSA[i][j]
                rhoSA[i][j] = rhoSA20
                hcz[i][j] = hcz20
                ncz[i][j] = ncz20
                nwcz[i][j] = nwcz20
            buildingType[i][j] = int(buildingType_input[i][j])
            if buildingType[i][j] == 1:
                Lb[i][j] = 1
                Lf[i][j] = 0.1
                eta[i][j] = 0.001
                Abf[i][j] = 150
                Hb[i][j] = 1.3
                ach[i][j] = 0.45
                Qsoil_Qb[i][j] =0.003 
            elif buildingType[i][j] == 2:
                Lb[i][j] = 1
                Lf[i][j] = 0
                eta[i][j] = 1
                Abf[i][j] = 150
                Hb[i][j] = 1.3
                ach[i][j] = 0.45
                Qsoil_Qb[i][j] = 0.003
            elif buildingType[i][j] == 3:
                Lb[i][j] = 2
                Lf[i][j] = 0.1
                eta[i][j] = 0.001
                Abf[i][j] = 150
                Hb[i][j] = 3.66
                ach[i][j] = 0.45
                Qsoil_Qb[i][j] = 0.003
            elif buildingType[i][j] == 4:
                Lb[i][j] = 2
                Lf[i][j] = 0
                eta[i][j] = 1
                Abf[i][j] = 150
                Hb[i][j] = 3.66
                ach[i][j] = 0.45
                Qsoil_Qb[i][j] = 0.003
            elif buildingType[i][j] == 5:
                Lb[i][j] = 0.1
                Lf[i][j] = 0.1
                eta[i][j] = 0.001
                Abf[i][j] = 150
                Hb[i][j] = 2.44
                ach[i][j] = 0.45
                Qsoil_Qb[i][j] = 0.003
            elif buildingType[i][j] == 6:
                Lb[i][j] = 1
                Lf[i][j] = 0.2
                eta[i][j] = 0.001
                Abf[i][j] = 1500
                Hb[i][j] = 3
                ach[i][j] = 1.5
                Qsoil_Qb[i][j] = 0.003
            elif buildingType[i][j] == 7:
                Lb[i][j] = 1
                Lf[i][j] = 0
                eta[i][j] = 1
                Abf[i][j] = 1500
                Hb[i][j] = 3
                ach[i][j] = 1.5
                Qsoil_Qb[i][j] = 0.003
            elif buildingType[i][j] == 8:
                Lb[i][j] = 2
                Lf[i][j] = 0.2
                eta[i][j] = 0.001
                Abf[i][j] = 1500
                Hb[i][j] = 3
                ach[i][j] = 1.5
                Qsoil_Qb[i][j] = 0.003
            elif buildingType[i][j] == 9:
                Lb[i][j] = 2
                Lf[i][j] = 0
                eta[i][j] = 1
                Abf[i][j] = 1500
                Hb[i][j] = 3
                ach[i][j] = 1.5
                Qsoil_Qb[i][j] = 0.003
            elif buildingType[i][j] == 10:
                Lb[i][j] = 0.2
                Lf[i][j] = 0.2
                eta[i][j] = 0.001
                Abf[i][j] = 1500
                Hb[i][j] = 3
                ach[i][j] = 1.5
                Qsoil_Qb[i][j] = 0.003
            elif buildingType[i][j] == 11:
                Lb[i][j] = Lb11
                Lf[i][j] = Lf11
                eta[i][j] = eta11
                Abf[i][j] = Abf11
                Hb[i][j] = Hb11
                ach[i][j] = ach11
                Qsoil_Qb[i][j] = Qsoil_Qb11
            elif buildingType[i][j] == 12:
                Lb[i][j] = Lb12
                Lf[i][j] = Lf12
                eta[i][j] = eta12
                Abf[i][j] = Abf12
                Hb[i][j] = Hb12
                ach[i][j] = ach12
                Qsoil_Qb[i][j] = Qsoil_Qb12
            elif buildingType[i][j] == 13:
                Lb[i][j] = Lb13
                Lf[i][j] = Lf13
                eta[i][j] = eta13
                Abf[i][j] = Abf13
                Hb[i][j] = Hb13
                ach[i][j] = ach13
                Qsoil_Qb[i][j] = Qsoil_Qb13
            elif buildingType[i][j] == 14:
                Lb[i][j] = Lb14
                Lf[i][j] = Lf14
                eta[i][j] = eta14
                Abf[i][j] = Abf14
                Hb[i][j] = Hb14
                ach[i][j] = ach14
                Qsoil_Qb[i][j] = Qsoil_Qb14
            elif buildingType[i][j] == 15:
                Lb[i][j] = Lb15
                Lf[i][j] = Lf15
                eta[i][j] = eta15
                Abf[i][j] = Abf15
                Hb[i][j] = Hb15
                ach[i][j] = ach15
                Qsoil_Qb[i][j] = Qsoil_Qb15
            elif buildingType[i][j] == 16:
                Lb[i][j] = Lb16
                Lf[i][j] = Lf16
                eta[i][j] = eta16
                Abf[i][j] = Abf16
                Hb[i][j] = Hb16
                ach[i][j] = ach16
                Qsoil_Qb[i][j] = Qsoil_Qb16
            elif buildingType[i][j] == 17:
                Lb[i][j] = Lb17
                Lf[i][j] = Lf17
                eta[i][j] = eta17
                Abf[i][j] = Abf17
                Hb[i][j] = Hb17
                ach[i][j] = ach17
                Qsoil_Qb[i][j] = Qsoil_Qb17
            elif buildingType[i][j] == 18:
                Lb[i][j] = Lb18
                Lf[i][j] = Lf18
                eta[i][j] = eta18
                Abf[i][j] = Abf18
                Hb[i][j] = Hb18
                ach[i][j] = ach18
                Qsoil_Qb[i][j] = Qsoil_Qb18
            elif buildingType[i][j] == 19:
                Lb[i][j] = Lb19
                Lf[i][j] = Lf19
                eta[i][j] = eta19
                Abf[i][j] = Abf19
                Hb[i][j] = Hb19
                ach[i][j] = ach19
                Qsoil_Qb[i][j] = Qsoil_Qb19
            elif buildingType[i][j] == 20:
                Lb[i][j] = Lb20
                Lf[i][j] = Lf20
                eta[i][j] = eta20
                Abf[i][j] = Abf20
                Hb[i][j] = Hb20
                ach[i][j] = ach20
                Qsoil_Qb[i][j] = Qsoil_Qb20
            Ex[i][j] = int(Ex_input[i][j])
            if Ex[i][j] == 1:
                ATnc[i][j] = 26
                EF[i][j] = 350
                ED[i][j] = 26
                ET[i][j] = 24
            elif Ex[i][j] == 2:
                ATnc[i][j] = 25
                EF[i][j] = 250
                ED[i][j] = 25
                ET[i][j] = 8
            elif Ex[i][j] == 3:
                ATnc[i][j] = 25
                EF[i][j] = EF3
                ED[i][j] = ED3
                ET[i][j] = ET3
            elif Ex[i][j] == 4:
                ATnc[i][j] = 25
                EF[i][j] = EF4
                ED[i][j] = ED4
                ET[i][j] = ET4
            elif Ex[i][j] == 5:
                ATnc[i][j] = 25
                EF[i][j] = EF5
                ED[i][j] = ED5
                ET[i][j] = ET5
    # constant, no grid param
    ATc = 70
    MMOAF = 72
    Rc = 1.987
    Tr = 298.1
    R = 0.00008205
    Tb_Tc = Tb/Tc
    if Tb_Tc<=0.57:
        n = 0.3
    elif Tb_Tc>0.57 and Tb_Tc<=0.71:
        n = 0.74*Tb_Tc-0.116
    else:
        n = 0.41
    DHvs = DHvb*(math.pow((1-Ts/Tc)/(1-Tb/Tc),n))
    Hs = (math.exp(-(DHvs/Rc)*(1/Ts-1/Tr))*Hc)/(R*Ts)
    # grid param cal
    Qb = [[0 for j in range(row)] for i in range(column)]
    Qsoil = [[0 for j in range(row)] for i in range(column)]
    Cs = [[0 for j in range(row)] for i in range(column)]
    Cs2 = [[0 for j in range(row)] for i in range(column)]
    Ls = [[0 for j in range(row)] for i in range(column)]
    hSA = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            Qb[i][j] = Abf[i][j]*Hb[i][j]*ach[i][j]
            Qsoil[i][j] = Qsoil_Qb[i][j]*Qb[i][j]
            if Type != "both":
                Cs[i][j] = Hs*Cmedium[i][j]*1000
            else:
                Cs[i][j] = Hs*Cmedium[i][j]*1000
                Cs2[i][j] = Hs*Cmedium2[i][j]*1000
            Ls[i][j] = LE[i][j]-WT[i][j]
            hSA[i][j] = Ls[i][j]
    # VFwesp calculate CM6a
    if Type == "sat":
        DeffA = [[0 for j in range(row)] for i in range(column)]
        DeffCZ = [[0 for j in range(row)] for i in range(column)]
        DeffT = [[0 for j in range(row)] for i in range(column)]
        A_param_6a = [[0 for j in range(row)] for i in range(column)]
        B_param = [[0 for j in range(row)] for i in range(column)]
        C_param_6a = [[0 for j in range(row)] for i in range(column)]
        VFwesp_6a = [[0 for j in range(row)] for i in range(column)]
        for i in range(column):
            for j in range(row):
                DeffA[i][j] = DeffA_cal(Dair,nSA[i][j],nwSA[i][j],Dwater,Hs)
                DeffCZ[i][j] = DeffCZ_cal(Dair,ncz[i][j],nwcz[i][j],Dwater,Hs)
                DeffT[i][j] = DeffT_cal(hSA[i][j],Lb[i][j],hcz[i][j],DeffA[i][j],DeffCZ[i][j])
                A_param_6a[i][j] = A_param_6a_cal(DeffT[i][j],Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                if Qsoil[i][j] == 0:
                    VFwesp_6a[i][j] = VFwesp_6a_Qszero_cal(A_param_6a[i][j],DeffT[i][j],Lf[i][j],Ls[i][j],Lb[i][j],DeffA[i][j],eta[i][j])
                elif Qsoil[i][j] > 0:
                    B_param[i][j] = B_param_cal(Qsoil_Qb[i][j],Qb[i][j],Lf[i][j],DeffA[i][j],eta[i][j],Abf[i][j],Lb[i][j])
                    C_param_6a[i][j] = C_param_6a_cal(Qsoil_Qb[i][j])
                    VFwesp_6a[i][j] = VFwesp_6a_Qsnozero_cal(A_param_6a[i][j],B_param[i][j],C_param_6a[i][j])
    # VFsesp calculate CM4
    if Type == "unsat":
        ks = [[0 for j in range(row)] for i in range(column)]
        DeffA = [[0 for j in range(row)] for i in range(column)]
        DeffCZ = [[0 for j in range(row)] for i in range(column)]
        DeffT = [[0 for j in range(row)] for i in range(column)]
        A_param_4a = [[0 for j in range(row)] for i in range(column)]
        B_param = [[0 for j in range(row)] for i in range(column)]
        C_param_4a = [[0 for j in range(row)] for i in range(column)]
        VFsesp_4a = [[0 for j in range(row)] for i in range(column)]
        for i in range(column):
            for j in range(row):
                if Organic == 0:
                    ks[i][j] = kd
                else:
                    ks[i][j] = Koc*foc
                DeffA[i][j] = DeffA_cal(Dair,nSA[i][j],nwSA[i][j],Dwater,Hs)
                DeffCZ[i][j] = DeffCZ_cal(Dair,ncz[i][j],nwcz[i][j],Dwater,Hs)
                DeffT[i][j] = DeffT_cal(hSA[i][j],Lb[i][j],hcz[i][j],DeffA[i][j],DeffCZ[i][j])
                A_param_4a[i][j] = A_param_4a_cal(Hs,rhoSA[i][j],nwSA[i][j],ks[i][j],nairSA[i][j])
                B_param[i][j] = B_param_cal(Qsoil_Qb[i][j],Qb[i][j],Lf[i][j],DeffA[i][j],eta[i][j],Abf[i][j],Lb[i][j])
                C_param_4a[i][j] = C_param_4a_cal(DeffA[i][j],Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                if Qsoil[i][j] == 0:
                    VFsesp_4a[i][j] = VFsesp_4a_Qszero_cal(A_param_4a[i][j],C_param_4a[i][j],DeffT[i][j],Lf[i][j],Ls[i][j],DeffA[i][j],eta[i][j])
                elif Qsoil[i][j] > 0:
                    VFsesp_4a[i][j] = VFsesp_4a_Qsnozero_cal(A_param_4a[i][j],C_param_4a[i][j],B_param[i][j])
    # CM4 and CM6 both
    if Type == "both":
        ks = [[0 for j in range(row)] for i in range(column)]
        DeffA = [[0 for j in range(row)] for i in range(column)]
        DeffCZ = [[0 for j in range(row)] for i in range(column)]
        DeffT = [[0 for j in range(row)] for i in range(column)]
        A_param_6a = [[0 for j in range(row)] for i in range(column)]
        A_param_4a = [[0 for j in range(row)] for i in range(column)]
        B_param = [[0 for j in range(row)] for i in range(column)]
        C_param_6a = [[0 for j in range(row)] for i in range(column)]
        C_param_4a = [[0 for j in range(row)] for i in range(column)]
        VFwesp_6a = [[0 for j in range(row)] for i in range(column)]
        VFsesp_4a = [[0 for j in range(row)] for i in range(column)]
        for i in range(column):
            for j in range(row):
                if Organic == 0:
                    ks[i][j] = kd
                else:
                    ks[i][j] = Koc*foc
                DeffA[i][j] = DeffA_cal(Dair,nSA[i][j],nwSA[i][j],Dwater,Hs)
                DeffCZ[i][j] = DeffCZ_cal(Dair,ncz[i][j],nwcz[i][j],Dwater,Hs)
                DeffT[i][j] = DeffT_cal(hSA[i][j],Lb[i][j],hcz[i][j],DeffA[i][j],DeffCZ[i][j])
                A_param_6a[i][j] = A_param_6a_cal(DeffT[i][j],Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                A_param_4a[i][j] = A_param_4a_cal(Hs,rhoSA[i][j],nwSA[i][j],ks[i][j],nairSA[i][j])
                B_param[i][j] = B_param_cal(Qsoil_Qb[i][j],Qb[i][j],Lf[i][j],DeffA[i][j],eta[i][j],Abf[i][j],Lb[i][j])
                C_param_4a[i][j] = C_param_4a_cal(DeffA[i][j],Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                if Qsoil[i][j] == 0:
                    VFwesp_6a[i][j] = VFwesp_6a_Qszero_cal(A_param_6a[i][j],DeffT[i][j],Lf[i][j],Ls[i][j],Lb[i][j],DeffA,eta[i][j])
                    VFsesp_4a[i][j] = VFsesp_4a_Qszero_cal(A_param_4a[i][j],C_param_4a[i][j],DeffT[i][j],Lf[i][j],Ls[i][j],DeffA[i][j],eta[i][j])
                elif Qsoil[i][j] > 0:
                    C_param_6a[i][j] = C_param_6a_cal(Qsoil_Qb[i][j])
                    VFwesp_6a[i][j] = VFwesp_6a_Qsnozero_cal(A_param_6a[i][j],B_param[i][j],C_param_6a[i][j])
                    VFsesp_4a[i][j] = VFsesp_4a_Qsnozero_cal(A_param_4a[i][j],C_param_4a[i][j],B_param[i][j])
    # Risk calculate loop
    mIURTCE_R_GW = 1.0e-6;
    IURTCE_R_GW = 3.1e-6;
    mIURTCE_C_GW = 4.1e-6;
    IURTCE_C_GW = 4.1e-6;
    Cia = [[0 for j in range(row)] for i in range(column)]
    Cia2 = [[0 for j in range(row)] for i in range(column)]
    Risk = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            if Type!="both":
                if Type == "sat":
                    Cia[i][j] = VFwesp_6a[i][j]*Cs[i][j]
                elif Type == "unsat":
                    Cia[i][j] = VFsesp_4a[i][j]*Cs[i][j]
                if chem == "Trichloroethylene" and Ex[i][j] == 1:
                    Risk[i][j] = Risk_TCE_cal(Cia[i][j],mIURTCE_R_GW,MMOAF,EF[i][j],ET[i][j],ATc,IURTCE_R_GW,ED[i][j])
                elif chem == "Trichloroethylene" and Ex[i][j] == 2:
                    Risk[i][j] = Risk_TCE_cal(Cia[i][j],mIURTCE_C_GW,MMOAF,EF[i][j],ET[i][j],ATc,IURTCE_C_GW,ED[i][j])
                elif Mut == "No":
                    Risk[i][j] = Risk_noMut_cal(IUR,EF[i][j],ED[i][j],ET[i][j],Cia[i][j],ATc)
                elif Mut == "Yes":
                    Risk[i][j] = Risk_yesMut_cal(IUR,EF[i][j],MMOAF,ET[i][j],Cia[i][j],ATc)
                elif Mut == "VC" and Ex[i][j] == 1:
                    Risk[i][j] = Cia[i][j]*(IUR+(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24))
                elif Mut == "VC" and Ex[i][j] == 2:
                    Risk[i][j] = Cia[i][j]*(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24)
            else:
                Cia[i][j] = VFwesp_6a[i][j]*Cs[i][j]
                Cia2[i][j] = VFsesp_4a[i][j]*Cs2[i][j]
                if chem == "Trichloroethylene" and Ex[i][j] == 1:
                    Risk[i][j] = Risk_TCE_cal(Cia[i][j],mIURTCE_R_GW,MMOAF,EF[i][j],ET[i][j],ATc,IURTCE_R_GW,ED[i][j]) + Risk_TCE_cal(Cia2[i][j],mIURTCE_R_GW,MMOAF,EF[i][j],ET[i][j],ATc,IURTCE_R_GW,ED[i][j])
                elif chem == "Trichloroethylene" and Ex[i][j] == 2:
                    Risk[i][j] = Risk_TCE_cal(Cia[i][j],mIURTCE_C_GW,MMOAF,EF[i][j],ET[i][j],ATc,IURTCE_C_GW,ED[i][j]) + Risk_TCE_cal(Cia2[i][j],mIURTCE_C_GW,MMOAF,EF[i][j],ET[i][j],ATc,IURTCE_C_GW,ED[i][j])
                elif Mut == "No":
                    Risk[i][j] = Risk_noMut_cal(IUR,EF[i][j],ED[i][j],ET[i][j],Cia[i][j],ATc) + Risk_noMut_cal(IUR,EF[i][j],ED[i][j],ET[i][j],Cia2[i][j],ATc)
                elif Mut == "Yes":
                    Risk[i][j] = Risk_yesMut_cal(IUR,EF[i][j],MMOAF,ET[i][j],Cia[i][j],ATc) + Risk_yesMut_cal(IUR,EF[i][j],MMOAF,ET[i][j],Cia2[i][j],ATc)
                elif Mut == "VC" and Ex[i][j] == 1:
                    Risk[i][j] = Cia[i][j]*(IUR+(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24)) + Cia2[i][j]*(IUR+(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24))
                elif Mut == "VC" and Ex[i][j] == 2:
                    Risk[i][j] = Cia[i][j]*(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24) + Cia2[i][j]*(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24)
    # HQ calculate
    HQ = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            if Type!="both":
                if Rfc != 0:
                    HQ[i][j] = HQ_cal(EF[i][j],ED[i][j],ET[i][j],Cia[i][j],Rfc,ATnc[i][j])
                else:
                    HQ[i][j] = "NULL"
            else:
                if Rfc != 0:
                    HQ[i][j] = HQ_cal(EF[i][j],ED[i][j],ET[i][j],Cia[i][j],Rfc,ATnc[i][j]) + HQ_cal(EF[i][j],ED[i][j],ET[i][j],Cia2[i][j],Rfc,ATnc[i][j])
                else:
                    HQ[i][j] = "NULL"
    # Cca, Cnca calculate
    mIURTCE_R = 1
    IURTCE_R = 1
    TCR = 1.0e-6
    THQ = 1
    Cca = [[0 for j in range(row)] for i in range(column)]
    Cnca = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            if chem == "Trichloroethylene":
                Cca[i][j] = Cca_TCE_cal(EF[i][j],MMOAF,ET[i][j],mIURTCE_R,TCR,ATc,ED[i][j],IURTCE_R)
                Cnca[i][j] = Cca[i][j]
            else:
                if IUR != 0 and Rfc != 0:
                    Cca[i][j] = Cca_cal(TCR,ATc,EF[i][j],ED[i][j],ET[i][j],IUR)
                    Cnca[i][j] = Cnca_cal(THQ,Rfc,ATnc[i][j],EF[i][j],ED[i][j],ET[i][j])
                else:
                    Cca[i][j] = "NULL"
                    Cnca[i][j] = "NULL"
    if Type == "sat":
        data = {
        "Risk": Risk,
        "HQ": HQ,
        "Cca": Cca,
        "Cnca": Cnca,
        "DeffA": DeffA,
        "DeffCZ":DeffCZ,
        "DeffT":DeffT,
        "Aparam":A_param_6a,
        "Bparam":B_param,
        "Cparam":C_param_6a,
        "VFwesp":VFwesp_6a,
        "Cia":Cia
        }
    elif Type == "unsat":
        data = {
        "Risk": Risk,
        "HQ": HQ,
        "Cca": Cca,
        "Cnca": Cnca,
        "DeffA": DeffA,
        "DeffCZ":DeffCZ,
        "DeffT":DeffT,
        "Aparam":A_param_4a,
        "Bparam":B_param,
        "Cparam":C_param_4a,
        "VFsesp":VFsesp_4a,
        "Cia":Cia
        }
    elif Type == "both":
        data = {
        "Risk": Risk,
        "HQ": HQ,
        "Cca": Cca,
        "Cnca": Cnca,
        "DeffA": DeffA,
        "DeffCZ":DeffCZ,
        "DeffT":DeffT,
        "Aparam":A_param_6a,
        "Aparam":A_param_4a,
        "Bparam":B_param,
        "Cparam":C_param_6a,
        "Cparam":C_param_4a,
        "VFwesp":VFwesp_6a,
        "VFsesp":VFsesp_4a,
        "Cia":Cia
        }
    return jsonify(data)

@app.route('/multipleSource', methods=['POST'])
def multipleSource():
    inputdata = request.get_json(silent=True)
    chem = [0 for i in range(5)]
    S = [0 for i in range(5)]
    Hc = [0 for i in range(5)]
    Dair = [0 for i in range(5)]
    Dwater = [0 for i in range(5)]
    DHvb = [0 for i in range(5)]
    Tc = [0 for i in range(5)]
    Tb = [0 for i in range(5)]
    MW = [0 for i in range(5)]
    IUR = [0 for i in range(5)]
    IURt = [0 for i in range(5)]
    Rfc = [0 for i in range(5)]
    Rfct = [0 for i in range(5)]
    Mut = [0 for i in range(5)]
    Organic = [0 for i in range(5)]
    Koc = [0 for i in range(5)]
    Koct = [0 for i in range(5)]
    Cmedium = [0 for i in range(5)]
    Cmedium2 = [0 for i in range(5)]
    foc = [0 for i in range(5)]
    Ts = [0 for i in range(5)]
    Type = [0 for i in range(5)]
    WT = [0 for i in range(5)]
    LE = [0 for i in range(5)]
    try:
        chem[0] = inputdata['chem_1']
        chem[1] = inputdata['chem_2']
        chem[2] = inputdata['chem_3']
        chem[3] = inputdata['chem_4']
        chem[4] = inputdata['chem_5']
    except:
        pass
    if chem[1]==0:
        chemNum = 1
    elif chem[2]==0:
        chemNum = 2
    elif chem[3]==0:
        chemNum = 3
    elif chem[4]==0:
        chemNum = 4
    elif chem[4]!=0:
        chemNum = 5
    try:
        S[0] = float(inputdata['value_S_1'])
        S[1] = float(inputdata['value_S_2'])
        S[2] = float(inputdata['value_S_3'])
        S[3] = float(inputdata['value_S_4'])
        S[4] = float(inputdata['value_S_5'])
    except:
        pass
    try:
        Hc[0] = float(inputdata['value_Hc_1'])
        Hc[1] = float(inputdata['value_Hc_2'])
        Hc[2] = float(inputdata['value_Hc_3'])
        Hc[3] = float(inputdata['value_Hc_4'])
        Hc[4] = float(inputdata['value_Hc_5'])
    except:
        pass
    try:
        Dair[0] = float(inputdata['value_Dair_1'])
        Dair[1] = float(inputdata['value_Dair_2'])
        Dair[2] = float(inputdata['value_Dair_3'])
        Dair[3] = float(inputdata['value_Dair_4'])
        Dair[4] = float(inputdata['value_Dair_5'])
    except:
        pass
    try:
        Dwater[0] = float(inputdata['value_Dwater_1'])
        Dwater[1] = float(inputdata['value_Dwater_2'])
        Dwater[2] = float(inputdata['value_Dwater_3'])
        Dwater[3] = float(inputdata['value_Dwater_4'])
        Dwater[4] = float(inputdata['value_Dwater_5'])
    except:
        pass
    try:
        DHvb[0] = float(inputdata['value_DHvb_1'])
        DHvb[1] = float(inputdata['value_DHvb_2'])
        DHvb[2] = float(inputdata['value_DHvb_3'])
        DHvb[3] = float(inputdata['value_DHvb_4'])
        DHvb[4] = float(inputdata['value_DHvb_5'])
    except:
        pass
    try:
        Tc[0] = float(inputdata['value_Tc_1'])
        Tc[1] = float(inputdata['value_Tc_2'])
        Tc[2] = float(inputdata['value_Tc_3'])
        Tc[3] = float(inputdata['value_Tc_4'])
        Tc[4] = float(inputdata['value_Tc_5'])
    except:
        pass
    try:
        Tb[0] = float(inputdata['value_Tb_1'])
        Tb[1] = float(inputdata['value_Tb_2'])
        Tb[2] = float(inputdata['value_Tb_3'])
        Tb[3] = float(inputdata['value_Tb_4'])
        Tb[4] = float(inputdata['value_Tb_5'])
    except:
        pass
    try:
        IURt[0] = inputdata['value_IUR_1']
        if IURt[0]=="NULL":
            IUR[0] = 0
        else:
            IUR[0] = float(IURt[0])
        IURt[1] = inputdata['value_IUR_2']
        if IURt[1]=="NULL":
            IUR[1] = 0
        else:
            IUR[1] = float(IURt[1])
        IURt[2] = inputdata['value_IUR_3']
        if IURt[2]=="NULL":
            IUR[2] = 0
        else:
            IUR[2] = float(IURt[2])
        IURt[3] = inputdata['value_IUR_4']
        if IURt[3]=="NULL":
            IUR[3] = 0
        else:
            IUR[3] = float(IURt[3])
        IURt[4] = inputdata['value_IUR_5']
        if IURt[4]=="NULL":
            IUR[4] = 0
        else:
            IUR[4] = float(IURt[4])
    except:
        pass
    try:
        Rfct[0] = inputdata['value_Rfc_1']
        if Rfct[0]=="NULL":
            Rfc[0] = 0
        else:
            Rfc[0] = float(Rfct[0])
        Rfc[1] = inputdata['value_Rfc_2']
        if Rfct[1]=="NULL":
            Rfc[1] = 0
        else:
            Rfc[1] = float(Rfct[1])
        Rfc[2] = inputdata['value_Rfc_3']
        if Rfct[2]=="NULL":
            Rfc[2] = 0
        else:
            Rfc[2] = float(Rfct[2])
        Rfc[3] = inputdata['value_Rfc_4']
        if Rfct[3]=="NULL":
            Rfc[3] = 0
        else:
            Rfc[3] = float(Rfct[3])
        Rfc[4] = inputdata['value_Rfc_5']
        if Rfct[4]=="NULL":
            Rfc[4] = 0
        else:
            Rfc[4] = float(Rfct[4])
    except:
        pass
    try:
        Mut[0] = inputdata['value_Mut_1']
        Mut[1] = inputdata['value_Mut_2']
        Mut[2] = inputdata['value_Mut_3']
        Mut[3] = inputdata['value_Mut_4']
        Mut[4] = inputdata['value_Mut_5']
    except:
        pass
    try:
        Organic[0] = float(inputdata['value_Organic_1'])
        Organic[1] = float(inputdata['value_Organic_2'])
        Organic[2] = float(inputdata['value_Organic_3'])
        Organic[3] = float(inputdata['value_Organic_4'])
        Organic[4] = float(inputdata['value_Organic_5'])
    except:
        pass
    try:
        Koct[0] = float(inputdata['value_Koc_1'])
        if Koct[0]=="NULL":
            Koc[0] = 0
        else:
            Koc[0] = float(Koct[0])
        Koct[1] = float(inputdata['value_Koc_2'])
        if Koct[1]=="NULL":
            Koc[1] = 0
        else:
            Koc[1] = float(Koct[1])
        Koct[2] = float(inputdata['value_Koc_3'])
        if Koct[2]=="NULL":
            Koc[2] = 0
        else:
            Koc[2] = float(Koct[2])
        Koct[3] = float(inputdata['value_Koc_4'])
        if Koct[3]=="NULL":
            Koc[3] = 0
        else:
            Koc[3] = float(Koct[3])
        Koct[4] = float(inputdata['value_Koc_5'])
        if Koct[4]=="NULL":
            Koc[4] = 0
        else:
            Koc[4] = float(Koct[4])
    except:
        pass
    try:
        foc[0] = float(inputdata['value_foc_1'])
        foc[1] = float(inputdata['value_foc_2'])
        foc[2] = float(inputdata['value_foc_3'])
        foc[3] = float(inputdata['value_foc_4'])
        foc[4] = float(inputdata['value_foc_5'])
    except:
        pass
    try:
        Ts[0] = float(inputdata['value_Ts_1']) + 273.15
        Ts[1] = float(inputdata['value_Ts_2']) + 273.15
        Ts[2] = float(inputdata['value_Ts_3']) + 273.15
        Ts[3] = float(inputdata['value_Ts_4']) + 273.15
        Ts[4] = float(inputdata['value_Ts_5']) + 273.15
    except:
        pass
    try:
        Type[0] = inputdata['type_1']
        Type[1] = inputdata['type_2']
        Type[2] = inputdata['type_3']
        Type[3] = inputdata['type_4']
        Type[4] = inputdata['type_5']
    except:
        pass
    try:
        if Type[0] == "sat":
            Cmedium[0] = float(inputdata['sat_soilconc_1'])
        elif Type[0] == "unsat":
            Cmedium[0] = float(inputdata['unsat_soilconc_1'])
        else:
            Cmedium[0] = float(inputdata['sat_soilconc_1'])
            Cmedium2[0] = float(inputdata['unsat_soilconc_1'])
        if Type[1] == "sat":
            Cmedium[1] = float(inputdata['sat_soilconc_2'])
        elif Type[1] == "unsat":
            Cmedium[1] = float(inputdata['unsat_soilconc_2'])
        else:
            Cmedium[1] = float(inputdata['sat_soilconc_2'])
            Cmedium2[1] = float(inputdata['unsat_soilconc_2'])
        if Type[2] == "sat":
            Cmedium[2] = float(inputdata['sat_soilconc_3'])
        elif Type[2] == "unsat":
            Cmedium[2] = float(inputdata['unsat_soilconc_3'])
        else:
            Cmedium[2] = float(inputdata['sat_soilconc_3'])
            Cmedium2[2] = float(inputdata['unsat_soilconc_3'])
        if Type[3] == "sat":
            Cmedium[3] = float(inputdata['sat_soilconc_4'])
        elif Type[3] == "unsat":
            Cmedium[3] = float(inputdata['unsat_soilconc_4'])
        else:
            Cmedium[3] = float(inputdata['sat_soilconc_4'])
            Cmedium2[3] = float(inputdata['unsat_soilconc_4'])
        if Type[4] == "sat":
            Cmedium[4] = float(inputdata['sat_soilconc_5'])
        elif Type[4] == "unsat":
            Cmedium[4] = float(inputdata['unsat_soilconc_5'])
        else:
            Cmedium[4] = float(inputdata['sat_soilconc_5'])
            Cmedium2[4] = float(inputdata['unsat_soilconc_5'])
    except:
        pass
    try:
        WT[0] = float(inputdata['waterlevel_1'])
        WT[1] = float(inputdata['waterlevel_2'])
        WT[2] = float(inputdata['waterlevel_3'])
        WT[3] = float(inputdata['waterlevel_4'])
        WT[4] = float(inputdata['waterlevel_5'])
    except:
        pass
    try:
        LE[0] = float(inputdata['elevation_1'])
        LE[1] = float(inputdata['elevation_2'])
        LE[2] = float(inputdata['elevation_3'])
        LE[3] = float(inputdata['elevation_4'])
        LE[4] = float(inputdata['elevation_5'])
    except:
        pass
    kd = float(inputdata['kd'])
    nSA = float(inputdata['nSA'])
    nwSA = float(inputdata['nwSA'])
    nairSA = float(inputdata['nairSA'])
    rhoSA = float(inputdata['rhoSA'])
    hcz = float(inputdata['hcz'])
    ncz = float(inputdata['ncz'])
    nwcz = float(inputdata['nwcz'])
    Lb = float(inputdata['LB'])
    Lf = float(inputdata['Lf'])
    eta = float(inputdata['eta'])
    Abf = float(inputdata['Abf'])
    Hb = float(inputdata['Hb'])
    ach = float(inputdata['ach'])
    Qsoil_Qb = float(inputdata['Qsoil_Qb'])
    Ex = int(inputdata['expType'])
    EF = int(inputdata['EF'])
    ED = int(inputdata['ED'])
    ET = int(inputdata['ET'])
    ATc = 70
    MMOAF = 72
    Rc = 1.987
    Tr = 298.1
    R = 0.00008205
    Qb = Abf*Hb*ach
    Qsoil = Qsoil_Qb*Qb
    Tb_Tc = [0 for i in range(5)]
    n = [0 for i in range(5)]
    Hr = [0 for i in range(5)]
    DHvs = [0 for i in range(5)]
    Hs = [0 for i in range(5)]
    Ls = [0 for i in range(5)]
    hSA = [0 for i in range(5)]
    Cs = [0 for i in range(chemNum)]
    Cs2 = [0 for i in range(chemNum)]
    for i in range(chemNum):
        Tb_Tc[i] = Tb[i]/Tc[i]
        if Tb_Tc[i]<=0.57:
            n[i] = 0.3
        elif Tb_Tc[i]>0.57 and Tb_Tc[i]<=0.71:
            n[i] = 0.74*Tb_Tc[i]-0.116
        else:
            n[i] = 0.41
        Hr[i] = Hc[i]/(0.000082057*298)
        DHvs[i] = DHvb[i]*(math.pow((1-Ts[i]/Tc[i])/(1-Tb[i]/Tc[i]),n[i]))
        Hs[i] = (math.exp(-(DHvs[i]/Rc)*(1/Ts[i]-1/Tr))*Hc[i])/(R*Ts[i])
        Ls[i] = LE[i]-WT[i]
        hSA[i] = Ls[i]
        if Type != "both":
            Cs[i] = Hs[i]*Cmedium[i]*1000
        else:
            Cs[i] = Hs[i]*Cmedium[i]*1000
            Cs2[i] = Hs[i]*Cmedium2[i]*1000
    # VFwesp calculate CM6a
    DeffA = [0 for i in range(chemNum)]
    DeffCZ = [0 for i in range(chemNum)]
    DeffT = [0 for i in range(chemNum)]
    A_param_6a = [0 for i in range(chemNum)]
    B_param = [0 for i in range(chemNum)]
    C_param_6a = [0 for i in range(chemNum)]
    VFwesp_6a = [0 for i in range(chemNum)]
    ks = [0 for i in range(chemNum)]
    A_param_4a = [0 for i in range(chemNum)]
    C_param_4a = [0 for i in range(chemNum)]
    VFsesp_4a = [0 for i in range(chemNum)]
    for i in range(chemNum):
        # VFwesp calculate CM6
        if Type[i] == "sat":
            DeffA[i] = DeffA_cal(Dair[i],nSA,nwSA,Dwater[i],Hs[i])
            DeffCZ[i] = DeffCZ_cal(Dair[i],ncz,nwcz,Dwater[i],Hs[i])
            DeffT[i] = DeffT_cal(hSA[i],Lb,hcz,DeffA[i],DeffCZ[i])
            A_param_6a[i] = A_param_6a_cal(DeffT[i],Abf,Lb,Qb,Ls[i])
            if Qsoil == 0:
                VFwesp_6a[i] = VFwesp_6a_Qszero_cal(A_param_6a[i],DeffT[i],Lf,Ls,Lb,DeffA[i],eta)
            elif Qsoil > 0:
                B_param[i] = B_param_cal(Qsoil_Qb,Qb,Lf,DeffA[i],eta,Abf,Lb)
                C_param_6a[i] = C_param_6a_cal(Qsoil_Qb)
                VFwesp_6a[i] = VFwesp_6a_Qsnozero_cal(A_param_6a[i],B_param[i],C_param_6a[i])
        # VFsesp calculate CM4
        elif Type[i] == "unsat":
            if Organic == 0:
                ks[i] = kd
            else:
                ks[i] = Koc[i]*foc[i]
            DeffA[i] = DeffA_cal(Dair[i],nSA,nwSA,Dwater[i],Hs[i])
            DeffCZ[i] = DeffCZ_cal(Dair[i],ncz,nwcz,Dwater[i],Hs[i])
            DeffT[i] = DeffT_cal(hSA[i],Lb,hcz,DeffA[i],DeffCZ[i])
            A_param_4a[i] = A_param_4a_cal(Hs[i],rhoSA,nwSA,ks[i],nairSA)
            B_param[i] = B_param_cal(Qsoil_Qb,Qb,Lf,DeffA[i],eta,Abf,Lb)
            C_param_4a[i] = C_param_4a_cal(DeffA[i],Abf,Lb,Qb,Ls[i])
            if Qsoil == 0:
                VFsesp_4a[i] = VFsesp_4a_Qszero_cal(A_param_4a[i],C_param_4a[i],DeffT[i],Lf,Ls[i],DeffA[i],eta)
            elif Qsoil > 0:
                VFsesp_4a[i] = VFsesp_4a_Qsnozero_cal(A_param_4a[i],C_param_4a[i],B_param[i])
        # both delete
        else:
            if Organic == 0:
                ks[i] = kd
            else:
                ks[i] = Koc[i]*foc[i]
            DeffA[i] = DeffA_cal(Dair[i],nSA,nwSA,Dwater[i],Hs[i])
            DeffCZ[i] = DeffCZ_cal(Dair[i],ncz,nwcz,Dwater[i],Hs[i])
            DeffT[i] = DeffT_cal(hSA[i],Lb,hcz,DeffA[i],DeffCZ[i])
            A_param_6a[i] = A_param_6a_cal(DeffT[i],Abf,Lb,Qb,Ls[i])
            B_param[i] = B_param_cal(Qsoil_Qb,Qb,Lf,DeffA[i],eta,Abf,Lb)
            C_param_4a[i] = C_param_4a_cal(DeffA[i],Abf,Lb,Qb,Ls[i])
            if Qsoil == 0:
                VFwesp_6a[i] = VFwesp_6a_Qszero_cal(A_param_6a[i],DeffT[i],Lf,Ls,Lb,DeffA[i],eta)
                VFsesp_4a[i] = VFsesp_4a_Qszero_cal(A_param_4a[i],C_param_4a[i],DeffT[i],Lf,Ls[i],DeffA[i],eta)
            elif Qsoil > 0:
                C_param_6a[i] = C_param_6a_cal(Qsoil_Qb)
                VFwesp_6a[i] = VFwesp_6a_Qsnozero_cal(A_param_6a[i],B_param[i],C_param_6a[i])
                VFsesp_4a[i] = VFsesp_4a_Qsnozero_cal(A_param_4a[i],C_param_4a[i],B_param[i])
    # Risk calculate loop
    mIURTCE_R_GW = 1.0e-6;
    IURTCE_R_GW = 3.1e-6;
    mIURTCE_C_GW = 4.1e-6;
    IURTCE_C_GW = 4.1e-6;
    Cia = [0 for i in range(chemNum)]
    Cia2 = [0 for i in range(chemNum)]
    Risk = [0 for i in range(chemNum)]
    for i in range(chemNum):
        if Ex == 1:
            ATnc = 26
        else:
            ATnc = 25
        if Type == "sat":
            Cia[i] = VFwesp_6a[i]*Cs[i]
        elif Type == "unsat":
            Cia[i] = VFsesp_4a[i]*Cs[i]
        else:
            Cia[i] = VFwesp_6a[i]*Cs[i]
            Cia2[i] = VFsesp_4a[i]*Cs2[i]
        if Type != "both":
            if chem[i] == "Trichloroethylene" and Ex[i] == 1:
                Risk[i] = Risk_TCE_cal(Cia[i],mIURTCE_R_GW,MMOAF,EF,ET,ATc,IURTCE_R_GW,ED)
            elif chem[i] == "Trichloroethylene" and Ex[i] == 2:
                Risk[i] = Risk_TCE_cal(Cia[i],mIURTCE_C_GW,MMOAF,EF,ET,ATc,IURTCE_C_GW,ED)
            elif Mut[i] == "No":
                Risk[i] = Risk_noMut_cal(IUR[i],EF,ED,ET,Cia[i],ATc)
            elif Mut[i] == "Yes":
                Risk[i] = Risk_yesMut_cal(IUR[i],EF,MMOAF,ET,Cia[i],ATc)
            elif Mut[i] == "VC" and Ex == 1:
                Risk[i] = Cia[i]*(IUR[i]+(IUR[i]*ED*EF*ET)/(ATc*365*24))
            elif Mut[i] == "VC" and Ex == 2:
                Risk[i] = Cia[i]*(IUR[i]*ED*EF*ET)/(ATc*365*24)
        else:
            if chem[i] == "Trichloroethylene" and Ex[i] == 1:
                Risk[i] = Risk_TCE_cal(Cia[i],mIURTCE_R_GW,MMOAF,EF,ET,ATc,IURTCE_R_GW,ED) + Risk_TCE_cal(Cia2[i],mIURTCE_R_GW,MMOAF,EF,ET,ATc,IURTCE_R_GW,ED)
            elif chem[i] == "Trichloroethylene" and Ex[i] == 2:
                Risk[i] = Risk_TCE_cal(Cia[i],mIURTCE_C_GW,MMOAF,EF,ET,ATc,IURTCE_C_GW,ED) + Risk_TCE_cal(Cia2[i],mIURTCE_C_GW,MMOAF,EF,ET,ATc,IURTCE_C_GW,ED)
            elif Mut[i] == "No":
                Risk[i] = Risk_noMut_cal(IUR[i],EF,ED,ET,Cia[i],ATc) + Risk_noMut_cal(IUR[i],EF,ED,ET,Cia2[i],ATc)
            elif Mut[i] == "Yes":
                Risk[i] = Risk_yesMut_cal(IUR[i],EF,MMOAF,ET,Cia[i],ATc) + Risk_yesMut_cal(IUR[i],EF,MMOAF,ET,Cia2[i],ATc)
            elif Mut[i] == "VC" and Ex == 1:
                Risk[i] = Cia[i]*(IUR[i]+(IUR[i]*ED*EF*ET)/(ATc*365*24)) + Cia2[i]*(IUR[i]+(IUR[i]*ED*EF*ET)/(ATc*365*24))
            elif Mut[i] == "VC" and Ex == 2:
                Risk[i] = Cia[i]*(IUR[i]*ED*EF*ET)/(ATc*365*24) + Cia2[i]*(IUR[i]*ED*EF*ET)/(ATc*365*24)
    # HQ calculate
    HQ = [0 for i in range(chemNum)]
    for i in range(chemNum):
        if Type != "both":
            if Rfc[i] != 0:
                HQ[i] = HQ_cal(EF,ED,ET,Cia[i],Rfc[i],ATnc)
            else:
                HQ[i] = "NULL"
        else:
            if Rfc[i] != 0:
                HQ[i] = HQ_cal(EF,ED,ET,Cia[i],Rfc[i],ATnc) + HQ_cal(EF,ED,ET,Cia2[i],Rfc[i],ATnc)
            else:
                HQ[i] = "NULL"
    # Cca, Cnca calculate
    mIURTCE_R = 1
    IURTCE_R = 1
    TCR = 1.0e-6
    THQ = 1
    Cca = [0 for i in range(chemNum)]
    Cnca = [0 for i in range(chemNum)]
    for i in range(chemNum):
        if chem[i] == "Trichloroethylene":
            Cca[i] = Cca_TCE_cal(EF,MMOAF,ET,mIURTCE_R,TCR,ATc,ED,IURTCE_R)
            Cnca[i] = Cca[i]
        else:
            if IUR[i] != 0 and Rfc[i] != 0:
                Cca[i] = Cca_cal(TCR,ATc,EF,ED,ET,IUR[i])
                Cnca[i] = Cnca_cal(THQ,Rfc[i],ATnc,EF,ED,ET)
            else:
                Cca[i] = "NULL"
                Cnca[i] = "NULL"
    data = {
    "VFwesp": VFwesp_6a,
    "VFsesp": VFsesp_4a,
    "Qsoil": Qsoil,
    "Risk": Risk,
    "HQ": HQ,
    "Cca": Cca,
    "Cnca": Cnca
    }
    return jsonify(data)

def Column_cal(str):
    column = str.count("]") - 1
    return column

def Row_cal(str, column):
    row = (str.count(",")+1)/column
    return row

def Stringbreak(str, column, row):
    tmp = str.replace('[', '')
    tmp1 = tmp.replace("]", '')
    datat = tmp1.split(",")
    k = 0
    data  = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            data[i][j] = datat[k]
            k = k + 1
    return data

def DeffA_cal(Dair,nSA,nwSA,Dwater,Hs):
    DeffA = Dair*(math.pow((nSA-nwSA),3.33)/math.pow(nSA,2))+(Dwater/Hs)*(math.pow(nwSA,3.33)/math.pow(nSA,2))
    return DeffA

def DeffCZ_cal(Dair,ncz,nwcz,Dwater,Hs):
    DeffCZ = (Dair*math.pow((ncz-nwcz),3.33)+(Dwater/Hs)*math.pow(nwcz,3.33))/math.pow(ncz,2)
    return DeffCZ

def DeffT_cal(hSA,Lb,hcz,DeffA,DeffCZ):
    DeffT = (hSA-Lb)/((hSA-Lb-hcz)/DeffA+hcz/DeffCZ)
    return DeffT

def A_param_6a_cal(DeffT,Abf,Lb,Qb,Ls):
    A_param_6a = (DeffT*((Abf+4*Lb*math.sqrt(Abf))*0.36))/(Qb*(Ls-Lb))
    return A_param_6a

def B_param_cal(Qsoil_Qb,Qb,Lf,DeffA,eta,Abf,Lb):
    B_param = (Qsoil_Qb*Qb*Lf)/(DeffA*eta*(Abf+4*Lb*math.sqrt(Abf))*0.36)
    return B_param

def C_param_6a_cal(Qsoil_Qb):
    C_param_6a = Qsoil_Qb
    return C_param_6a

def VFwesp_6a_Qszero_cal(A_param_6a,DeffT,Lf,Ls,Lb,DeffA,eta):
    VFwesp_6a_Qszero = A_param_6a/(1+A_param_6a+((DeffT*Lf)/((Ls-Lb)*DeffA*eta)))
    return VFwesp_6a_Qszero

def VFwesp_6a_Qsnozero_cal(A_param_6a,B_param,C_param_6a):
    VFwesp_6a_Qsnozero = (A_param_6a*math.exp(B_param))/(math.exp(B_param)+A_param_6a+(A_param_6a/C_param_6a)*(math.exp(B_param)-1))
    return VFwesp_6a_Qsnozero

def A_param_4a_cal(Hs,rhoSA,nwSA,ks,nairSA):
    A_param_4a = (Hs*rhoSA)/(nwSA+ks*rhoSA+Hs*nairSA)
    return A_param_4a

def C_param_4a_cal(DeffA,Abf,Lb,Qb,Ls):
    C_param_4a = (DeffA*(Abf+4*Lb*math.sqrt(Abf))*0.36)/(Qb*Ls)
    return C_param_4a

def VFsesp_4a_Qszero_cal(A_param_4a,C_param_4a,DeffT,Lf,Ls,DeffA,eta):
    VFsesp_Qszero_4a = (A_param_4a*C_param_4a)/(1+A_param_4a+((DeffT*Lf)/Ls*DeffA*eta))
    return VFsesp_Qszero_4a

def VFsesp_4a_Qsnozero_cal(A_param_4a,C_param_4a,B_param):
    VFsesp_4a_Qsnozero = (A_param_4a*C_param_4a*math.exp(B_param))/(math.exp(B_param)+C_param_4a+(A_param_4a/C_param_4a)*(math.exp(B_param)-1))
    return VFsesp_4a_Qsnozero

def Risk_TCE_cal(Cia,mIURTCE_X_GW,MMOAF,EF,ET,ATc,IURTCE_X_GW,ED):
    Risk_TCE = (Cia*mIURTCE_X_GW*MMOAF*EF*ET)/(ATc*365*24) + (Cia*IURTCE_X_GW*ED*EF*ET)/(ATc*365*24)
    return Risk_TCE

def Risk_noMut_cal(IUR,EF,ED,ET,Cia,ATc):
    Risk_noMut = (IUR*EF*ED*ET*Cia)/(ATc*365*24)
    return Risk_noMut

def Risk_yesMut_cal(IUR,EF,MMOAF,ET,Cia,ATc):
    Risk_yesMut = (IUR*EF*MMOAF*ET*Cia)/(ATc*365*24)
    return Risk_yesMut

def HQ_cal(EF,ED,ET,Cia,Rfc,ATnc):
    HQ = (EF*ED*(ET/24)*Cia)/(Rfc*1000*ATnc*365)
    return HQ

def Cca_TCE_cal(EF,MMOAF,ET,mIURTCE_R,TCR,ATc,ED,IURTCE_R):
    Cca_TCE = 1/((EF*MMOAF*ET*mIURTCE_R/(TCR*ATc*365*24))+EF*ED*ET*IURTCE_R/(TCR*ATc*365*24))
    return Cca_TCE

def Cca_cal(TCR,ATc,EF,ED,ET,IUR):
    Cca = (TCR*ATc*365*24)/(EF*ED*ET*IUR)
    return Cca

def Cnca_cal(THQ,Rfc,ATnc,EF,ED,ET):
    Cnca = (THQ*Rfc*ATnc*365*24*1000)/(EF*ED*ET)
    return Cnca

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)