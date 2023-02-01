import math
from flask import Flask, request, url_for, render_template, redirect, jsonify
app = Flask(__name__)

@app.route('/')
def main():
    return "Hello VIRAP!"

@app.route('/singleSource', methods=['POST'])
def singleSource():
    inputdata = request.get_json()
    '''
    row
    column
    totalnum
    chem        # 1~179 number
    S
    Hc
    Hr          # cal
    Hs          # cal
    Dair
    Dwater
    DHvb
    Tc
    Tb
    MW
    IUR
    Rfc
    Mut         # No=0, Yes=1, VC=2
    n           # cal
    Ls
    type        # Groundwater, Soil, Groundwater&soil
    Ts
    Cs          # grid cal
    Cmedium     # gridinput
    WT          # gridinput
    LE          # gridinput
    foc         # gridinput
    Organic     # No=0 Yes=1
    Koc
    kd
    pH
    hSA         #cal
    nSA
    nwSA
    nairSA
    rhoSA
    hcz
    ncz
    nwcz
    naircz
    Lb          # gridinput or cons
    Lf          # gridinput or cons
    eta         # gridinput or cons
    Abf         # gridinput or cons
    Hb          # gridinput or cons
    ach         # gridinput or cons
    Qsoil_Qb    # gridinput or cons
    Qb          # cal
    Qsoil       # cal
    Ex          # gridinput
    ATc         # cal
    ATnc        # grid cal
    MMOAF       # cal
    EF          # grid cal
    ED          # grid cal
    ET          # grid cal
    Cia         # grid cal
    buildingType# 1~10 number 11 is select
    '''
    chem = inputdata['chem']
    S = float(inputdata['value_S'])
    Hc = float(inputdata['value_Hc'])
    Dair = float(inputdata['value_Dair'])
    Dwater = float(inputdata['value_Dwater'])
    DHvb = float(inputdata['value_DHvb'])
    Tc = float(inputdata['value_Tc'])
    Tb = float(inputdata['value_Tb'])
    MW = float(inputdata['value_MW'])
    IUR_input = inputdata['value_IUR']
    if IUR_input=="NULL":
        IUR = 0
    else:
        IUR = float(IUR_input)
    Rfc_input = inputdata['value_Rfc']
    if Rfc_input=="NULL":
        Rfc = 0
    else:
        Rfc = Rfc_input
    Mut = inputdata['value_Mut']
    Type = inputdata['type']
    Ts = float(inputdata['value_Ts'])
    Organic = int(inputdata['value_Organic'])
    Koc_input = inputdata['value_Koc']
    if Koc_input=="NULL":
        Koc = 0
    else:
        Koc = Koc_input
    kd = float(inputdata['value_kd'])
    nSA = float(inputdata['value_nSA'])
    nwSA = float(inputdata['value_nwSA'])
    nairSA = float(inputdata['value_nairSA'])
    rhoSA = float(inputdata['value_rhoSA'])
    hcz = float(inputdata['value_hcz'])
    ncz = float(inputdata['value_ncz'])
    nwcz = float(inputdata['value_nwcz'])
    naircz = float(inputdata['value_naircz'])
    buildingType = int(inputdata['buildingType'])
    # grid input start
    Cmedium_input = inputdata['soilconc']
    WT_input = inputdata['waterlevel']
    LE_input = inputdata['elevation']
    foc_input = inputdata['value_foc']
    Lb_input = inputdata['Lb']
    Lf_input = inputdata['Lf']
    eta_input = inputdata['eta']
    Abf_input = inputdata['Abf']
    Hb_input = inputdata['Hb']
    ach_input = inputdata['ach']
    Qsoil_Qb_input = inputdata['Qsoil_Qb']
    Ex_input = inputdata['Ex']
    column = len(WT_input)
    row = len(WT_input[0])
    Cmedium = [[0 for j in range(row)] for i in range(column)]
    WT = [[0 for j in range(row)] for i in range(column)]
    LE = [[0 for j in range(row)] for i in range(column)]
    foc = [[0 for j in range(row)] for i in range(column)]
    Lb = [[0 for j in range(row)] for i in range(column)]
    Lf = [[0 for j in range(row)] for i in range(column)]
    eta = [[0 for j in range(row)] for i in range(column)]
    Abf = [[0 for j in range(row)] for i in range(column)]
    Hb = [[0 for j in range(row)] for i in range(column)]
    ach = [[0 for j in range(row)] for i in range(column)]
    Qsoil_Qb = [[0 for j in range(row)] for i in range(column)]
    Ex = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            Cmedium[i][j] = float(Cmedium_input[i][j])
            LE[i][j] = float(LE_input[i][j])
            WT[i][j] = float(WT_input[i][j])
            foc[i][j] = float(foc_input[i][j])
            Ex[i][j] = int(Ex_input[i][j])
            if buildingType == 11:
                Lb[i][j] = float(Lb_input[i][j])
                Lf[i][j] = float(Lf_input[i][j])
                eta[i][j] = float(eta_input[i][j])
                Abf[i][j] = float(Abf_input[i][j])
                Hb[i][j] = float(Hb_input[i][j])
                ach[i][j] = float(ach_input[i][j])
                Qsoil_Qb[i][j] = float(Qsoil_Qb_input[i][j])
            else:
                Lb[i][j] = float(Lb_input)
                Lf[i][j] = float(Lf_input)
                eta[i][j] = float(eta_input)
                Abf[i][j] = float(Abf_input)
                Hb[i][j] = float(Hb_input)
                ach[i][j] = float(ach_input)
                Qsoil_Qb[i][j] = float(Qsoil_Qb_input)
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
    Hr = Hc/(0.000082057*298)
    DHvs = DHvb*(math.pow((1-Ts/Tc)/(1-Tb/Tc),n))
    Hs = (math.exp(-(DHvs/Rc)*(1/Ts-1/Tr))*Hc)/(R*Ts)
    # grid param cal
    Qb = [[0 for j in range(row)] for i in range(column)]
    Qsoil = [[0 for j in range(row)] for i in range(column)]
    Cs = [[0 for j in range(row)] for i in range(column)]
    Ls = [[0 for j in range(row)] for i in range(column)]
    hSA = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            Qb[i][j] = Abf[i][j]*Hb[i][j]*ach[i][j]
            Qsoil[i][j] = Qsoil_Qb[i][j]*Qb[i][j]
            if Qsoil[i][j] < 0:
                return "Error: Qsoil < 0"
            Cs[i][j] = Hs*Cmedium[i][j]*1000
            Ls[i][j] = WT[i][j]-LE[i][j]
            hSA[i][j] = Ls[i][j]
    # VFwesp calculate CM6a
    if Type == "Groundwater":
        DeffT = [[0 for j in range(row)] for i in range(column)]
        A_param_6a = [[0 for j in range(row)] for i in range(column)]
        B_param = [[0 for j in range(row)] for i in range(column)]
        C_param_6a = [[0 for j in range(row)] for i in range(column)]
        VFwesp_6a = [[0 for j in range(row)] for i in range(column)]
        DeffA = DeffA_cal(Dair,nSA,nwSA,Dwater,Hs)
        DeffCZ = DeffCZ_cal(Dair,ncz,nwcz,Dwater,Hs)
        for i in range(column):
            for j in range(row):
                DeffT[i][j] = DeffT_cal(hSA[i][j],Lb[i][j],hcz,DeffA,DeffCZ)
                A_param_6a[i][j] = A_param_6a_cal(DeffT[i][j],Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                if Qsoil[i][j] == 0:
                    VFwesp_6a[i][j] = VFwesp_6a_Qszero_cal(A_param_6a[i][j],DeffT[i][j],Lf[i][j],Ls[i][j],Lb[i][j],DeffA,eta[i][j])
                elif Qsoil[i][j] > 0:
                    B_param[i][j] = B_param_cal(Qsoil_Qb[i][j],Qb[i][j],Lf[i][j],DeffA,eta[i][j],Abf[i][j],Lb[i][j])
                    C_param_6a[i][j] = C_param_6a_cal(Qsoil_Qb[i][j])
                    VFwesp_6a[i][j] = VFwesp_6a_Qsnozero_cal(A_param_6a[i][j],B_param[i][j],C_param_6a[i][j])
    # VFsesp calculate CM4
    if Type == "Soil":
        ks = [[0 for j in range(row)] for i in range(column)]
        DeffT = [[0 for j in range(row)] for i in range(column)]
        A_param_4a = [[0 for j in range(row)] for i in range(column)]
        B_param = [[0 for j in range(row)] for i in range(column)]
        C_param_4a = [[0 for j in range(row)] for i in range(column)]
        VFsesp_4a = [[0 for j in range(row)] for i in range(column)]
        DeffA = DeffA_cal(Dair,nSA,nwSA,Dwater,Hs)
        DeffCZ = DeffCZ_cal(Dair,ncz,nwcz,Dwater,Hs)
        for i in range(column):
            for j in range(row):
                if Organic == 0:
                    ks[i][j] = kd
                else:
                    ks[i][j] = Koc*foc[i][j]
                DeffT[i][j] = DeffT_cal(hSA[i][j],Lb[i][j],hcz,DeffA,DeffCZ)
                A_param_4a[i][j] = A_param_4a_cal(Hs,rhoSA,nwSA,ks[i][j],nairSA)
                B_param[i][j] = B_param_cal(Qsoil_Qb[i][j],Qb[i][j],Lf[i][j],DeffA,eta[i][j],Abf[i][j],Lb[i][j])
                C_param_4a[i][j] = C_param_4a_cal(DeffA,Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                if Qsoil[i][j] == 0:                                                                                    #check
                    VFsesp_4a[i][j] = VFsesp_4a_Qszero_cal(A_param_4a[i][j],C_param_4a[i][j],DeffT[i][j],Lf[i][j],Ls[i][j],DeffA[i][j],eta[i][j])
                elif Qsoil[i][j] > 0:
                    VFsesp_4a[i][j] = VFsesp_4a_Qsnozero_cal(A_param_4a[i][j],C_param_4a[i][j],B_param[i][j])
    if Type == "Groundwater&Soil":
        ks = [[0 for j in range(row)] for i in range(column)]
        DeffT = [[0 for j in range(row)] for i in range(column)]
        A_param_6a = [[0 for j in range(row)] for i in range(column)]
        A_param_4a = [[0 for j in range(row)] for i in range(column)]
        B_param = [[0 for j in range(row)] for i in range(column)]
        C_param_6a = [[0 for j in range(row)] for i in range(column)]
        C_param_4a = [[0 for j in range(row)] for i in range(column)]
        VFwesp_6a = [[0 for j in range(row)] for i in range(column)]
        VFsesp_4a = [[0 for j in range(row)] for i in range(column)]
        DeffA = DeffA_cal(Dair,nSA,nwSA,Dwater,Hs)
        DeffCZ = DeffCZ_cal(Dair,ncz,nwcz,Dwater,Hs)
        for i in range(column):
            for j in range(row):
                if Organic == 0:
                    ks[i][j] = kd
                else:
                    ks[i][j] = Koc*foc[i][j]
                DeffT[i][j] = DeffT_cal(hSA[i][j],Lb[i][j],hcz,DeffA,DeffCZ)
                A_param_6a[i][j] = A_param_6a_cal(DeffT[i][j],Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
                A_param_4a[i][j] = A_param_4a_cal(Hs,rhoSA,nwSA,ks[i][j],nairSA)
                B_param[i][j] = B_param_cal(Qsoil_Qb[i][j],Qb[i][j],Lf[i][j],DeffA,eta[i][j],Abf[i][j],Lb[i][j])
                C_param_4a[i][j] = C_param_4a_cal(DeffA,Abf[i][j],Lb[i][j],Qb[i][j],Ls[i][j])
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
    Risk = [[0 for j in range(row)] for i in range(column)]
    ATnc = [[0 for j in range(row)] for i in range(column)]
    EF = [[0 for j in range(row)] for i in range(column)]
    ED = [[0 for j in range(row)] for i in range(column)]
    ET = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            if Ex[i][j] == 0:
                ATnc[i][j] = 26
                EF[i][j] = 350
                ED[i][j] = 26
                ET[i][j] = 24
            else:
                ATnc[i][j] = 25
                EF[i][j] = 250
                ED[i][j] = 25
                ET[i][j] = 8
            if Type!="Groundwater&Soil":
                if Type == "Groundwater":
                    Cia[i][j] = VFwesp_6a[i][j]*Cs[i][j]
                elif Type == "Soil":
                    Cia[i][j] = VFsesp_4a[i][j]*Cs[i][j]
                if chem == "Trichloroethylene":
                    Risk[i][j] = Risk_TCE_cal(Cia[i][j],mIURTCE_R_GW,MMOAF,EF[i][j],ET[i][j],ATc,IURTCE_R_GW,ED[i][j])
                elif Mut == "No":          # check no Ex
                    Risk[i][j] = Risk_noMut_cal(IUR,EF[i][j],ED[i][j],ET[i][j],Cia[i][j],ATc)
                elif Mut == "Yes":          # check no Ex
                    Risk[i][j] = Risk_yesMut_cal(IUR,EF[i][j],MMOAF,ET[i][j],Cia[i][j],ATc)
                elif Mut == "VC" and Ex[i][j] == 0:
                    Risk[i][j] = Cia[i][j]*(IUR+(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24))
                elif Mut == "VC" and Ex[i][j] == 1:
                    Risk[i][j] = Cia[i][j]*(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24)
            else:
                Cia2 = [[0 for j in range(row)] for i in range(column)]
                if Type == "Groundwater":
                    Cia[i][j] = VFwesp_6a[i][j]*Cs[i][j]
                elif Type == "Soil":
                    Cia2[i][j] = VFsesp_4a[i][j]*Cs[i][j]
                if chem == "Trichloroethylene":
                    Risk[i][j] = Risk_TCE_cal(Cia[i][j],mIURTCE_R_GW,MMOAF,EF[i][j],ET[i][j],ATc,IURTCE_R_GW,ED[i][j]) + Risk_TCE_cal(Cia2[i][j],mIURTCE_R_GW,MMOAF,EF[i][j],ET[i][j],ATc,IURTCE_R_GW,ED[i][j])
                elif Mut == "No":          # check no Ex
                    Risk[i][j] = Risk_noMut_cal(IUR,EF[i][j],ED[i][j],ET[i][j],Cia[i][j],ATc) + Risk_noMut_cal(IUR,EF[i][j],ED[i][j],ET[i][j],Cia2[i][j],ATc)
                elif Mut == "Yes":          # check no Ex
                    Risk[i][j] = Risk_yesMut_cal(IUR,EF[i][j],MMOAF,ET[i][j],Cia[i][j],ATc) + Risk_yesMut_cal(IUR,EF[i][j],MMOAF,ET[i][j],Cia2[i][j],ATc)
                elif Mut == "VC" and Ex[i][j] == 0:
                    Risk[i][j] = Cia[i][j]*(IUR+(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24)) + Cia2[i][j]*(IUR+(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24))
                elif Mut == "VC" and Ex[i][j] == 1:
                    Risk[i][j] = Cia[i][j]*(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24) + Cia2[i][j]*(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24)
    # HQ calculate
    HQ = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            if Type!="Groundwater&Soil":
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
    if Type == "Groundwater":
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
        "VFwesp":VFwesp_6a,
        "Cia":Cia
        }
    elif Type == "Soil":
        data = {
        "Risk": Risk,
        "HQ": HQ,
        "Cca": Cca,
        "Cnca": Cnca
        }
    elif Type == "Grounwater&Soil":
        data = {
        "Risk": Risk,
        "HQ": HQ,
        "Cca": Cca,
        "Cnca": Cnca
        }
    return jsonify(data)

@app.route('/multipleSource', methods=['POST'])
def multipleSource():
    inputdata = request.get_json()
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
        MW[0] = float(inputdata['value_MW_1'])
        MW[1] = float(inputdata['value_MW_2'])
        MW[2] = float(inputdata['value_MW_3'])
        MW[3] = float(inputdata['value_MW_4'])
        MW[4] = float(inputdata['value_MW_5'])
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
        Rfc[0] = inputdata['value_Rfc_1']
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
        Cmedium[0] = float(inputdata['soilconc_1'])
        Cmedium[1] = float(inputdata['soilconc_2'])
        Cmedium[2] = float(inputdata['soilconc_3'])
        Cmedium[3] = float(inputdata['soilconc_4'])
        Cmedium[4] = float(inputdata['soilconc_5'])
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
        Ts[0] = float(inputdata['value_Ts_1'])
        Ts[1] = float(inputdata['value_Ts_2'])
        Ts[2] = float(inputdata['value_Ts_3'])
        Ts[3] = float(inputdata['value_Ts_4'])
        Ts[4] = float(inputdata['value_Ts_5'])
    except:
        pass
    try:
        Type[0] = float(inputdata['type_1'])
        Type[1] = float(inputdata['type_2'])
        Type[2] = float(inputdata['type_3'])
        Type[3] = float(inputdata['type_4'])
        Type[4] = float(inputdata['type_5'])
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
    naircz = float(inputdata['naircz'])
    buildingType = int(inputdata['buildingType'])
    Lb = float(inputdata['Lb'])
    Lf = float(inputdata['Lf'])
    eta = float(inputdata['eta'])
    Abf = float(inputdata['Abf'])
    Hb = float(inputdata['Hb'])
    ach = float(inputdata['ach'])
    Qsoil_Qb = float(inputdata['Qsoil_Qb'])
    Ex = int(inputdata['Ex'])
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
        if Type[i] == "Groundwater":
            DeffA[i] = DeffA_cal(Dair[i],nSA,nwSA,Dwater[i],Hs[i])
            DeffCZ[i] = DeffCZ_cal(Dair[i],ncz,nwcz,Dwater[i],Hs[i])
            DeffT[i] = DeffT_cal(hSA[i],Lb,hcz,DeffA[i],DeffCZ[i])
            A_param_6a[i] = A_param_6a_cal(DeffT[i],Abf,Lb,Qb,Ls[i])
            if Qsoil == 0:
                VFwesp_6a[i] = VFwesp_6a_Qszero_cal(A_param_6a[i],DeffT[i],Lf,Ls,Lb,DeffA[i],eta)
            elif Qsoil > 0:
                B_param[i] = B_param_cal(Qsoil_Qb,Qb,Lf,DeffA[i],eta,Abf,Lb)
                C_param_6a[i] = C_param_6a_cal(Qsoil_Qb[i])
                VFwesp_6a[i] = VFwesp_6a_Qsnozero_cal(A_param_6a[i],B_param[i],C_param_6a[i])
    # VFsesp calculate CM4
        if Type[i] == "Soil":
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
    # Risk calculate loop
    mIURTCE_R_GW = 1.0e-6;
    IURTCE_R_GW = 3.1e-6;
    mIURTCE_C_GW = 4.1e-6;
    IURTCE_C_GW = 4.1e-6;
    Cia = [0 for i in range(chemNum)]
    Risk = [0 for i in range(chemNum)]
    for i in range(chemNum):
        if Ex == 0:
            ATnc = 26
            EF = 350
            ED = 26
            ET = 24
        else:
            ATnc = 25
            EF = 250
            ED = 25
            ET = 8
        if Type == "Groundwater":
            Cia[i] = VFwesp_6a[i]*Cs[i]
        elif Type == "Soil":
            Cia[i] = VFsesp_4a[i]*Cs[i]
        if chem[i] == "Trichloroethylene":
            Risk[i] = Risk_TCE_cal(Cia[i],mIURTCE_R_GW,MMOAF,EF,ET,ATc,IURTCE_R_GW,ED)
        elif Mut[i] == "No":        # check no Ex
            Risk[i] = Risk_noMut_cal(IUR[i],EF,ED,ET,Cia[i],ATc)
        elif Mut[i] == "Yes":       # check no Ex
            Risk[i] = Risk_yesMut_cal(IUR[i],EF,MMOAF,ET,Cia[i],ATc)
        elif Mut[i] == "VC" and Ex == 0:
            Risk[i] = Cia[i]*(IUR[i]+(IUR[i]*ED*EF*ET)/(ATc*365*24))
        elif Mut[i] == "VC" and Ex == 1:
            Risk[i] = Cia[i]*(IUR[i]*ED*EF*ET)/(ATc*365*24)
    # HQ calculate
    HQ = [0 for i in range(chemNum)]
    for i in range(chemNum):
        if Rfc[i] != 0:
            HQ[i] = HQ_cal(EF,ED,ET,Cia[i],Rfc[i],ATnc)
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

def DeffA_cal(Dair,nSA,nwSA,Dwater,Hs):
    DeffA = Dair*(math.pow((nSA-nwSA),3.33)/math.pow(nSA,2))+(Dwater/Hs)*(math.pow(nwSA,3.33)/math.pow(nSA,2))
    return DeffA

def DeffCZ_cal(Dair,ncz,nwcz,Dwater,Hs):
    DeffCZ = Dair*(math.pow((ncz-nwcz),3.33)/math.pow(ncz,2))+(Dwater/Hs)*(math.pow(nwcz,3.33)/math.pow(ncz,2))
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

def Risk_TCE_cal(Cia,mIURTCE_R_GW,MMOAF,EF,ET,ATc,IURTCE_R_GW,ED):
    Risk_TCE = (Cia*mIURTCE_R_GW*MMOAF*EF*ET)/(ATc*365*24) + (Cia*IURTCE_R_GW*ED*EF*ET)/(ATc*365*24)
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
    app.run(host='0.0.0.0', port=5000, debug=True)