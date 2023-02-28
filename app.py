import math
from flask import Flask, request, url_for, render_template, redirect, jsonify, Response
from flask_cors import CORS
#from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
CORS(app)
'''
app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "1234"
    )
jwt = JWTManager(app)

@app.after_request
def set_response_headers(r):
    r.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '0'
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r
'''

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@app.route('/singleSource', methods=HTTP_METHODS)
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
    Ts = 288.15
    try:
        Ts = float(inputdata['Ts']) + 273.15
    except:
        pass
    Koc_input = inputdata['value_Koc']
    if Koc_input=="NULL":
        Koc = 0
    else:
        Koc = Koc_input
    foc = float(inputdata['value_foc'])
    if Type == "sat":
        Cmedium_input = Stringbreak(inputdata['sat_soilconc'], column, row)
    elif Type == "unsat":
        Cmedium_input = Stringbreak(inputdata['unsat_soilconc'], column, row)
    else:
        Cmedium_input = Stringbreak(inputdata['sat_soilconc'], column, row)
        Cmedium2_input = Stringbreak(inputdata['unsat_soilconc'], column, row)
    WT_input = Stringbreak(inputdata['waterlevel'], column, row)
    LE_input = Stringbreak(inputdata['elevation'], column, row)
    Geo_Type = int(inputdata['Geo_Type'])
    layerType = inputdata['layerType']
    if layerType=="multiple":
        DeffTtmp = float(inputdata['DeffT'])
    buildingType_input = Stringbreak(inputdata['Found_Type'], column, row)
    # Building Type start
    try:
        Lb11 = float(inputdata['LB_11'])
        Lb12 = float(inputdata['LB_12'])
        Lb13 = float(inputdata['LB_13'])
        Lb14 = float(inputdata['LB_14'])
        Lb15 = float(inputdata['LB_15'])
    except:
        pass
    try:
        Lf11 = float(inputdata['Lf_11'])
        Lf12 = float(inputdata['Lf_12'])
        Lf13 = float(inputdata['Lf_13'])
        Lf14 = float(inputdata['Lf_14'])
        Lf15 = float(inputdata['Lf_15'])
    except:
        pass
    try:
        eta11 = float(inputdata['eta_11'])
        eta12 = float(inputdata['eta_12'])
        eta13 = float(inputdata['eta_13'])
        eta14 = float(inputdata['eta_14'])
        eta15 = float(inputdata['eta_15'])
    except:
        pass
    try:
        Abf11 = float(inputdata['Abf_11'])
        Abf12 = float(inputdata['Abf_12'])
        Abf13 = float(inputdata['Abf_13'])
        Abf14 = float(inputdata['Abf_14'])
        Abf15 = float(inputdata['Abf_15'])
    except:
        pass
    try:
        Hb11 = float(inputdata['Hb_11'])
        Hb12 = float(inputdata['Hb_12'])
        Hb13 = float(inputdata['Hb_13'])
        Hb14 = float(inputdata['Hb_14'])
        Hb15 = float(inputdata['Hb_15'])
    except:
        pass
    try:
        ach11 = float(inputdata['ach_11'])
        ach12 = float(inputdata['ach_12'])
        ach13 = float(inputdata['ach_13'])
        ach14 = float(inputdata['ach_14'])
        ach15 = float(inputdata['ach_15'])
    except:
        pass
    try:
        Qsoil_Qb11 = float(inputdata['Qsoil_Qb_11'])
        Qsoil_Qb12 = float(inputdata['Qsoil_Qb_12'])
        Qsoil_Qb13 = float(inputdata['Qsoil_Qb_13'])
        Qsoil_Qb14 = float(inputdata['Qsoil_Qb_14'])
        Qsoil_Qb15 = float(inputdata['Qsoil_Qb_15'])
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
    try:
        ATc3 = float(inputdata['ATC_3'])
        ATc4 = float(inputdata['ATc_4'])
        ATc5 = float(inputdata['ATc_5'])
    except:
        pass
    try:
        ATnc3 = float(inputdata['ATnc_3'])
        ATnc4 = float(inputdata['ATnc_4'])
        ATnc5 = float(inputdata['ATnc_5'])
    except:
        pass
    # Ex end
    if Geo_Type == 1:
        nSA = 0.459
        nwSA = 0.215
        nairSA = nSA - nwSA
        rhoSA = 1.43
        hcz = 0.815217391
        ncz = 0.459
        nwcz = 0.41185514
    elif Geo_Type == 2:
        nSA = 0.442
        nwSA = 0.168
        nairSA = nSA - nwSA
        rhoSA = 1.48
        hcz = 0.46875
        ncz = 0.442
        nwcz = 0.375117458
    elif Geo_Type == 3:
        nSA = 0.399
        nwSA = 0.148
        nairSA = nSA - nwSA
        rhoSA = 1.59
        hcz = 0.375
        ncz = 0.399
        nwcz = 0.331630276
    elif Geo_Type == 4:
        nSA = 0.39
        nwSA = 0.076
        nairSA = nSA - nwSA
        rhoSA = 1.62
        hcz = 0.1875
        ncz = 0.39
        nwcz = 0.302585409
    elif Geo_Type == 5:
        nSA = 0.375
        nwSA = 0.054
        nairSA = nSA - nwSA
        rhoSA = 1.66
        hcz = 0.170454545
        ncz = 0.375
        nwcz = 0.253258113
    elif Geo_Type == 6:
        nSA = 0.385
        nwSA = 0.197
        nairSA = nSA - nwSA
        rhoSA = 1.63
        hcz = 0.3
        ncz = 0.385
        nwcz = 0.354846864
    elif Geo_Type == 7:
        nSA = 0.384
        nwSA = 0.146
        nairSA = nSA - nwSA
        rhoSA = 1.63
        hcz = 0.25862069
        ncz = 0.384
        nwcz = 0.333283473
    elif Geo_Type == 8:
        nSA = 0.387
        nwSA = 0.103
        nairSA = nSA - nwSA
        rhoSA = 1.62
        hcz = 0.25
        ncz = 0.387
        nwcz = 0.31973079
    elif Geo_Type == 9:
        nSA = 0.489
        nwSA = 0.167
        nairSA = nSA - nwSA
        rhoSA = 1.35
        hcz = 1.630434783
        ncz = 0.489
        nwcz = 0.381686648
    elif Geo_Type == 10:
        nSA = 0.439
        nwSA = 0.18
        nairSA = nSA - nwSA
        rhoSA = 1.49
        hcz = 0.681818182
        ncz = 0.439
        nwcz = 0.348694517
    elif Geo_Type == 11:
        nSA = 0.481
        nwSA = 0.216
        nairSA = nSA - nwSA
        rhoSA = 1.38
        hcz = 1.923076923
        ncz = 0.481
        nwcz = 0.423644962
    elif Geo_Type == 12:
        nSA = 0.482
        nwSA = 0.198
        nairSA = nSA - nwSA
        rhoSA = 1.37
        hcz = 1.339285714
        ncz = 0.482
        nwcz = 0.399159996
    elif Geo_Type == 13:
        nSA = float(inputdata['nSA_13'])
        nwSA = float(inputdata['nwSA_13'])
        nairSA = nSA - nwSA
        rhoSA = float(inputdata['rhoSA_13'])
        hcz = float(inputdata['hcz_13'])
        ncz = float(inputdata['ncz_13'])
        nwcz = float(inputdata['nwcz_13'])
    Cmedium = [[0 for j in range(row)] for i in range(column)]
    Cmedium2 = [[0 for j in range(row)] for i in range(column)]
    WT = [[0 for j in range(row)] for i in range(column)]
    LE = [[0 for j in range(row)] for i in range(column)]
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
    ATc = [[0 for j in range(row)] for i in range(column)]
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
            Ex[i][j] = int(Ex_input[i][j])
            if Ex[i][j] == 1:
                ATc[i][j] = 70
                ATnc[i][j] = 26
                EF[i][j] = 350
                ED[i][j] = 26
                ET[i][j] = 24
            elif Ex[i][j] == 2:
                ATc[i][j] = 70
                ATnc[i][j] = 25
                EF[i][j] = 250
                ED[i][j] = 25
                ET[i][j] = 8
            elif Ex[i][j] == 3:
                ATc[i][j] = ATc3
                ATnc[i][j] = ATnc3
                EF[i][j] = EF3
                ED[i][j] = ED3
                ET[i][j] = ET3
            elif Ex[i][j] == 4:
                ATc[i][j] = ATc4
                ATnc[i][j] = ATnc4
                EF[i][j] = EF4
                ED[i][j] = ED4
                ET[i][j] = ET4
            elif Ex[i][j] == 5:
                ATc[i][j] = ATc5
                ATnc[i][j] = ATnc5
                EF[i][j] = EF5
                ED[i][j] = ED5
                ET[i][j] = ET5
    # constant, no grid param
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
        DeffT = [[0 for j in range(row)] for i in range(column)]
        A_param_6a = [[0 for j in range(row)] for i in range(column)]
        B_param = [[0 for j in range(row)] for i in range(column)]
        C_param_6a = [[0 for j in range(row)] for i in range(column)]
        VFwesp_6a = [[0 for j in range(row)] for i in range(column)]
        DeffA = DeffA_cal(Dair,nSA,nwSA,Dwater,Hs)
        DeffCZ = DeffCZ_cal(Dair,ncz,nwcz,Dwater,Hs)
        for i in range(column):
            for j in range(row):
                if layerType=="multiple":
                    DeffT[i][j] = DeffTtmp
                else:
                    DeffT[i][j] = DeffT_cal(hSA[i][j],Lb[i][j],hcz,DeffA,DeffCZ)
                A_param_6a[i][j] = A_param_6a_cal(DeffT[i][j],Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                if Qsoil[i][j] == 0:
                    VFwesp_6a[i][j] = VFwesp_6a_Qszero_cal(A_param_6a[i][j],DeffT[i][j],Lf[i][j],Ls[i][j],Lb[i][j],DeffA,eta[i][j])
                elif Qsoil[i][j] > 0:
                    B_param[i][j] = B_param_cal(Qsoil_Qb[i][j],Qb[i][j],Lf[i][j],DeffA,eta[i][j],Abf[i][j],Lb[i][j])
                    C_param_6a[i][j] = C_param_6a_cal(Qsoil_Qb[i][j])
                    VFwesp_6a[i][j] = VFwesp_6a_Qsnozero_cal(A_param_6a[i][j],B_param[i][j],C_param_6a[i][j])
    # VFsesp calculate CM4
    elif Type == "unsat":
        DeffT = [[0 for j in range(row)] for i in range(column)]
        B_param = [[0 for j in range(row)] for i in range(column)]
        C_param_4a = [[0 for j in range(row)] for i in range(column)]
        VFsesp_4a = [[0 for j in range(row)] for i in range(column)]
        ks = Koc*foc
        DeffA = DeffA_cal(Dair,nSA,nwSA,Dwater,Hs)
        DeffCZ = DeffCZ_cal(Dair,ncz,nwcz,Dwater,Hs)
        A_param_4a = A_param_4a_cal(Hs,rhoSA,nwSA,ks,nairSA)
        for i in range(column):
            for j in range(row):
                if layerType=="multiple":
                    DeffT[i][j] = DeffTtmp
                else:
                    DeffT[i][j] = DeffT_cal(hSA[i][j],Lb[i][j],hcz,DeffA,DeffCZ)
                B_param[i][j] = B_param_cal(Qsoil_Qb[i][j],Qb[i][j],Lf[i][j],DeffA,eta[i][j],Abf[i][j],Lb[i][j])
                C_param_4a[i][j] = C_param_4a_cal(DeffA,Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                if Qsoil[i][j] == 0:
                    VFsesp_4a[i][j] = VFsesp_4a_Qszero_cal(A_param_4a,C_param_4a[i][j],DeffT[i][j],Lf[i][j],Ls[i][j],DeffA,eta[i][j])
                elif Qsoil[i][j] > 0:
                    VFsesp_4a[i][j] = VFsesp_4a_Qsnozero_cal(A_param_4a,C_param_4a[i][j],B_param[i][j])
    # CM4 and CM6 both
    else:
        DeffT = [[0 for j in range(row)] for i in range(column)]
        A_param_6a = [[0 for j in range(row)] for i in range(column)]
        B_param = [[0 for j in range(row)] for i in range(column)]
        C_param_6a = [[0 for j in range(row)] for i in range(column)]
        C_param_4a = [[0 for j in range(row)] for i in range(column)]
        VFwesp_6a = [[0 for j in range(row)] for i in range(column)]
        VFsesp_4a = [[0 for j in range(row)] for i in range(column)]
        ks = Koc*foc
        DeffA = DeffA_cal(Dair,nSA,nwSA,Dwater,Hs)
        DeffCZ = DeffCZ_cal(Dair,ncz,nwcz,Dwater,Hs)
        A_param_4a = A_param_4a_cal(Hs,rhoSA,nwSA,ks,nairSA)
        for i in range(column):
            for j in range(row):
                if layerType=="multiple":
                    DeffT[i][j] = DeffTtmp
                else:
                    DeffT[i][j] = DeffT_cal(hSA[i][j],Lb[i][j],hcz,DeffA,DeffCZ)
                A_param_6a[i][j] = A_param_6a_cal(DeffT[i][j],Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                B_param[i][j] = B_param_cal(Qsoil_Qb[i][j],Qb[i][j],Lf[i][j],DeffA,eta[i][j],Abf[i][j],Lb[i][j])
                C_param_4a[i][j] = C_param_4a_cal(DeffA,Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                if Qsoil[i][j] == 0:
                    VFwesp_6a[i][j] = VFwesp_6a_Qszero_cal(A_param_6a[i][j],DeffT[i][j],Lf[i][j],Ls[i][j],Lb[i][j],DeffA,eta[i][j])
                    VFsesp_4a[i][j] = VFsesp_4a_Qszero_cal(A_param_4a,C_param_4a[i][j],DeffT[i][j],Lf[i][j],Ls[i][j],DeffA,eta[i][j])
                elif Qsoil[i][j] > 0:
                    C_param_6a[i][j] = C_param_6a_cal(Qsoil_Qb[i][j])
                    VFwesp_6a[i][j] = VFwesp_6a_Qsnozero_cal(A_param_6a[i][j],B_param[i][j],C_param_6a[i][j])
                    VFsesp_4a[i][j] = VFsesp_4a_Qsnozero_cal(A_param_4a,C_param_4a[i][j],B_param[i][j])
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
                    Risk[i][j] = Risk_TCE_cal(Cia[i][j],mIURTCE_R_GW,MMOAF,EF[i][j],ET[i][j],ATc[i][j],IURTCE_R_GW,ED[i][j])
                elif chem == "Trichloroethylene" and Ex[i][j] == 2:
                    Risk[i][j] = Risk_TCE_cal(Cia[i][j],mIURTCE_C_GW,MMOAF,EF[i][j],ET[i][j],ATc[i][j],IURTCE_C_GW,ED[i][j])
                elif Mut == "No":
                    Risk[i][j] = Risk_noMut_cal(IUR,EF[i][j],ED[i][j],ET[i][j],Cia[i][j],ATc[i][j])
                elif Mut == "Yes":
                    Risk[i][j] = Risk_yesMut_cal(IUR,EF[i][j],MMOAF,ET[i][j],Cia[i][j],ATc[i][j])
                elif Mut == "VC" and Ex[i][j] == 1:
                    Risk[i][j] = Cia[i][j]*(IUR+(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc[i][j]*365*24))
                elif Mut == "VC" and Ex[i][j] == 2:
                    Risk[i][j] = Cia[i][j]*(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc[i][j]*365*24)
            else:
                Cia[i][j] = VFwesp_6a[i][j]*Cs[i][j]
                Cia2[i][j] = VFsesp_4a[i][j]*Cs2[i][j]
                if chem == "Trichloroethylene" and Ex[i][j] == 1:
                    Risk[i][j] = Risk_TCE_cal(Cia[i][j],mIURTCE_R_GW,MMOAF,EF[i][j],ET[i][j],ATc[i][j],IURTCE_R_GW,ED[i][j]) + Risk_TCE_cal(Cia2[i][j],mIURTCE_R_GW,MMOAF,EF[i][j],ET[i][j],ATc[i][j],IURTCE_R_GW,ED[i][j])
                elif chem == "Trichloroethylene" and Ex[i][j] == 2:
                    Risk[i][j] = Risk_TCE_cal(Cia[i][j],mIURTCE_C_GW,MMOAF,EF[i][j],ET[i][j],ATc[i][j],IURTCE_C_GW,ED[i][j]) + Risk_TCE_cal(Cia2[i][j],mIURTCE_C_GW,MMOAF,EF[i][j],ET[i][j],ATc[i][j],IURTCE_C_GW,ED[i][j])
                elif Mut == "No":
                    Risk[i][j] = Risk_noMut_cal(IUR,EF[i][j],ED[i][j],ET[i][j],Cia[i][j],ATc[i][j]) + Risk_noMut_cal(IUR,EF[i][j],ED[i][j],ET[i][j],Cia2[i][j],ATc[i][j])
                elif Mut == "Yes":
                    Risk[i][j] = Risk_yesMut_cal(IUR,EF[i][j],MMOAF,ET[i][j],Cia[i][j],ATc[i][j]) + Risk_yesMut_cal(IUR,EF[i][j],MMOAF,ET[i][j],Cia2[i][j],ATc[i][j])
                elif Mut == "VC" and Ex[i][j] == 1:
                    Risk[i][j] = Cia[i][j]*(IUR+(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc[i][j]*365*24)) + Cia2[i][j]*(IUR+(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc[i][j]*365*24))
                elif Mut == "VC" and Ex[i][j] == 2:
                    Risk[i][j] = Cia[i][j]*(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc[i][j]*365*24) + Cia2[i][j]*(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc[i][j]*365*24)
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
    data = {
    "Risk": Risk,
    "HQ": HQ,
    "Cia":Cia
    }
    return jsonify(data)

@app.route('/multipleSource', methods=HTTP_METHODS)
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
    IUR = [0 for i in range(5)]
    IURt = [0 for i in range(5)]
    Rfc = [0 for i in range(5)]
    Rfct = [0 for i in range(5)]
    Mut = [0 for i in range(5)]
    Koc = [0 for i in range(5)]
    Koct = [0 for i in range(5)]
    Cmedium = [0 for i in range(5)]
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
        Kow[0] = float(inputdata['value_Kow_1'])
        Kow[1] = float(inputdata['value_Kow_2'])
        Kow[2] = float(inputdata['value_Kow_3'])
        Kow[3] = float(inputdata['value_Kow_4'])
        Kow[4] = float(inputdata['value_Kow_5'])
    except:
        pass
    try:
        Ts[0] = float(inputdata['Ts_1']) + 273.15
        Ts[1] = float(inputdata['Ts_2']) + 273.15
        Ts[2] = float(inputdata['Ts_3']) + 273.15
        Ts[3] = float(inputdata['Ts_4']) + 273.15
        Ts[4] = float(inputdata['Ts_5']) + 273.15
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
        Cmedium[0] = float(inputdata['soilconc_1'])
        Cmedium[1] = float(inputdata['soilconc_2'])
        Cmedium[2] = float(inputdata['soilconc_3'])
        Cmedium[3] = float(inputdata['soilconc_4'])
        Cmedium[4] = float(inputdata['soilconc_5'])
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
    nSA = float(inputdata['nSA'])
    nwSA = float(inputdata['nwSA'])
    nairSA = nSA - nwSA
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
    Ex = inputdata['expType']
    EF = int(inputdata['EF'])
    ED = int(inputdata['ED'])
    ET = int(inputdata['ET'])
    ATc = int(inputdata['ATc'])
    ATnc = int(inputdata['ATnc'])
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
        Hs[i] = (math.exp(-(DHvs[i]/Rc)*((1/Ts[i])-(1/Tr)))*Hc[i])/(R*Ts[i])
        Ls[i] = LE[i]-WT[i]
        hSA[i] = Ls[i]
        Cs[i] = Hs[i]*Cmedium[i]*1000
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
                VFwesp_6a[i] = VFwesp_6a_Qszero_cal(A_param_6a[i],DeffT[i],Lf,Ls[i],Lb,DeffA[i],eta)
            elif Qsoil > 0:
                B_param[i] = B_param_cal(Qsoil_Qb,Qb,Lf,DeffA[i],eta,Abf,Lb)
                C_param_6a[i] = C_param_6a_cal(Qsoil_Qb)
                VFwesp_6a[i] = VFwesp_6a_Qsnozero_cal(A_param_6a[i],B_param[i],C_param_6a[i])
        # VFsesp calculate CM4
        elif Type[i] == "unsat":
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
    # Risk calculate loop
    mIURTCE_R_GW = 1.0e-6;
    IURTCE_R_GW = 3.1e-6;
    mIURTCE_C_GW = 4.1e-6;
    IURTCE_C_GW = 4.1e-6;
    Cia = [0 for i in range(chemNum)]
    Risk = [0 for i in range(chemNum)]
    for i in range(chemNum):
        if Type[i] == "sat":
            Cia[i] = VFwesp_6a[i]*Cs[i]
        else:
            Cia[i] = VFsesp_4a[i]*Cs[i]
        if chem[i] == "Trichloroethylene" and Ex == "residential":
            Risk[i] = Risk_TCE_cal(Cia[i],mIURTCE_R_GW,MMOAF,EF,ET,ATc,IURTCE_R_GW,ED)
        elif chem[i] == "Trichloroethylene" and Ex == "commercial":
            Risk[i] = Risk_TCE_cal(Cia[i],mIURTCE_C_GW,MMOAF,EF,ET,ATc,IURTCE_C_GW,ED)
        elif Mut[i] == "No":
            Risk[i] = Risk_noMut_cal(IUR[i],EF,ED,ET,Cia[i],ATc)
        elif Mut[i] == "Yes":
            Risk[i] = Risk_yesMut_cal(IUR[i],EF,MMOAF,ET,Cia[i],ATc)
        elif Mut[i] == "VC" and Ex == "residential":
            Risk[i] = Cia[i]*(IUR[i]+(IUR[i]*ED*EF*ET)/(ATc*365*24))
        elif Mut[i] == "VC" and Ex == "commercial":
            Risk[i] = Cia[i]*(IUR[i]*ED*EF*ET)/(ATc*365*24)
    # HQ calculate
    HQ = [0 for i in range(chemNum)]
    for i in range(chemNum):
        if Rfc[i] != 0:
            HQ[i] = HQ_cal(EF,ED,ET,Cia[i],Rfc[i],ATnc)
        else:
            HQ[i] = "NULL"
    data = {
    "Risk": Risk,
    "HQ": HQ,
    "Cia": Cia
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)