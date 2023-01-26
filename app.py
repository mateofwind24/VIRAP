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
    Source      # GW=0, Soil=1
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
    column = int(inputdata['column'])
    row = int(inputdata['row'])
    totalnum = column*row
    chem = int(inputdata['chem'])
    S = float(inputdata['S'])
    Hc = float(inputdata['Hc'])
    Dair = float(inputdata['Dair'])
    Dwater = float(inputdata['Dwater'])
    DHvb = float(inputdata['DHvb'])
    Tc = float(inputdata['Tc'])
    Tb = float(inputdata['Tb'])
    MW = float(inputdata['MW'])
    IUR = float(inputdata['IUR'])
    Rfc = float(inputdata['Rfc'])
    Mut = int(inputdata['Mut'])
    Source = int(inputdata['Source'])
    Ts = float(inputdata['Ts'])
    Organic = int(inputdata['Organic'])
    Koc = float(inputdata['Koc'])
    kd = float(inputdata['kd'])
    pH = float(inputdata['pH'])
    nSA = float(inputdata['nSA'])
    nwSA = float(inputdata['nwSA'])
    nairSA = float(inputdata['nairSA'])
    rhoSA = float(inputdata['rhoSA'])
    hcz = float(inputdata['hcz'])
    ncz = float(inputdata['ncz'])
    nwcz = float(inputdata['nwcz'])
    naircz = float(inputdata['naircz'])
    buildingType = int(inputdata['buildingType'])
    # grid input start
    Cmedium_input = inputdata['Cmedium']
    WT_input = inputdata['WT']
    LE_input = inputdata['LE']
    foc_input = inputdata['foc']
    Lb_input = inputdata['Lb']
    Lf_input = inputdata['Lf']
    eta_input = inputdata['eta']
    Abf_input = inputdata['Abf']
    Hb_input = inputdata['Hb']
    ach_input = inputdata['ach']
    Qsoil_Qb_input = inputdata['Qsoil_Qb']
    Ex_input = inputdata['Ex']
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
            Ls[i][j] = LE[i][j]-WT[i][j]
            hSA[i][j] = Ls[i][j]
    # VFwesp calculate CM6a
    if Source == 0:
        DeffT_6a = [[0 for j in range(row)] for i in range(column)]
        A_param_6a = [[0 for j in range(row)] for i in range(column)]
        B_param_6a = [[0 for j in range(row)] for i in range(column)]
        C_param_6a = [[0 for j in range(row)] for i in range(column)]
        VFwesp_6a = [[0 for j in range(row)] for i in range(column)]
        DeffA_6a = Dair*(math.pow((nSA-nwSA),3.33)/math.pow(nSA,2))+(Dwater/Hs)*(math.pow(nwSA,3.33)/math.pow(nSA,2))
        DeffCZ_6a = Dair*(math.pow((ncz-nwcz),3.33)/math.pow(ncz,2))+(Dwater/Hs)*(math.pow(nwcz,3.33)/math.pow(ncz,2))
        for i in range(column):
            for j in range(row):
                DeffT_6a[i][j] = (hSA[i][j]-Lb[i][j])/((hSA[i][j]-Lb[i][j]-hcz)/DeffA_6a+hcz/DeffCZ_6a)
                if Qsoil[i][j] == 0:
                    A_param_6a[i][j] = (DeffT_6a[i][j]*(Abf[i][j]+4*Lb[i][j]*math.sqrt(Abf[i][j])*0.36))/(Qb[i][j]*(Ls[i][j]-Lb[i][j]))
                    VFwesp_6a[i][j] = A_param_6a[i][j]/(1+A_param_6a[i][j]+((DeffT_6a[i][j]*Lf[i][j])/((Ls[i][j]-Lb[i][j])*DeffA_6a*eta[i][j])))
                elif Qsoil[i][j] > 0:
                    A_param_6a[i][j] = (DeffT_6a[i][j]*(Abf[i][j]+4*Lb[i][j]*math.sqrt(Abf[i][j])*0.36))/(Qb[i][j]*(Ls[i][j]-Lb[i][j]))
                    B_param_6a[i][j] = (Qsoil_Qb[i][j]*Qb[i][j]*Lf[i][j])/(DeffA_6a*eta[i][j]*(Abf[i][j]+4*Lb[i][j]*math.sqrt(Abf[i][j]))*0.36)
                    C_param_6a[i][j] = Qsoil_Qb[i][j]
                    VFwesp_6a[i][j] = (A_param_6a[i][j]*math.exp(B_param_6a[i][j]))/(math.exp(B_param_6a[i][j])+A_param_6a[i][j]+(A_param_6a[i][j]/C_param_6a[i][j])*(math.exp(B_param_6a[i][j])-1))
    # VFsesp calculate CM4
    if Source == 1:
        ks = [[0 for j in range(row)] for i in range(column)]
        DeffT_4a = [[0 for j in range(row)] for i in range(column)]
        A_param_4a = [[0 for j in range(row)] for i in range(column)]
        B_param_4a = [[0 for j in range(row)] for i in range(column)]
        C_param_4a = [[0 for j in range(row)] for i in range(column)]
        VFsesp_4a = [[0 for j in range(row)] for i in range(column)]
        DeffA_4a = Dair*(math.pow((nSA-nwSA),3.33)/math.pow(nSA,2))+(Dwater/Hs)*(math.pow(nwSA,3.33)/math.pow(nSA,2))
        DeffCZ_4a = Dair*(math.pow((ncz-nwcz),3.33)/math.pow(ncz,2))+(Dwater/Hs)*(math.pow(nwcz,3.33)/math.pow(ncz,2))
        for i in range(column):
            for j in range(row):
                if Organic == 0:
                    ks[i][j] = kd
                else:
                    ks[i][j] = Koc*foc[i][j]
                DeffT_4a[i][j] = (hSA[i][j]-Lb[i][j])/((hSA[i][j]-Lb[i][j]-hcz)/DeffA_4a+hcz/DeffCZ_4a)
                A_param_4a[i][j] = (Hs*rhoSA)/(nwSA+ks[i][j]*rhoSA+Hs*nairSA)
                B_param_4a[i][j] = (Qsoil_Qb[i][j]*Qb[i][j]*Lf[i][j])/(DeffA_4a*eta[i][j]*(Abf[i][j]+4*Lb[i][j]*math.sqrt(Abf[i][j]))*0.36)
                C_param_4a[i][j] = (DeffA_4a*(Abf[i][j]+4*Lb[i][j]*math.sqrt(Abf[i][j]))*0.36)/(Qb[i][j]*Ls[i][j])
                if Qsoil[i][j] == 0:                                                                                    #check
                    VFsesp_4a[i][j] = (A_param_4a[i][j]*C_param_4a[i][j])/(1+A_param_4a[i][j]+((DeffT_4a[i][j]*Lf[i][j])/Ls[i][j]*DeffA_4a[i][j]*eta[i][j]))
                elif Qsoil[i][j] > 0:
                    VFsesp_4a[i][j] = (A_param_4a[i][j]*C_param_4a[i][j]*math.exp(B_param_4a[i][j]))/(math.exp(B_param_4a[i][j])+C_param_4a[i][j]+(A_param_4a[i][j]/C_param_4a[i][j])*(math.exp(B_param_4a[i][j])-1))
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
            if Source == 0:
                Cia[i][j] = VFwesp_6a[i][j]*Cs[i][j]
            elif Source == 1:
                Cia[i][j] = VFsesp_4a[i][j]*Cs[i][j]
            if chem == 165 and Ex[i][j] == 0:
                Risk[i][j] = (Cia[i][j]*mIURTCE_R_GW*MMOAF*EF[i][j]*ET[i][j])/(ATc*365*24) + (Cia[i][j]*IURTCE_R_GW*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24)
            elif chem == 165 and Ex[i][j] == 1:
                Risk[i][j] = (Cia[i][j]*mIURTCE_C_GW*MMOAF*EF[i][j]*ET[i][j])/(ATc*365*24) + (Cia[i][j]*IURTCE_C_GW*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24)
            elif Mut == 0:                          # check no Ex
                Risk[i][j] = (IUR*EF[i][j]*ED[i][j]*ET[i][j]*Cia[i][j])/(ATc*365*24)
            elif Mut == 1 and chem != 165:          # check no Ex
                Risk[i][j] = (IUR*EF[i][j]*MMOAF*ET[i][j]*Cia[i][j])/(ATc*365*24)
            elif Mut == 2 and Ex[i][j] == 0:
                Risk[i][j] = Cia[i][j]*(IUR+(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24))
            elif Mut == 2 and Ex[i][j] == 1:
                Risk[i][j] = Cia[i][j]*(IUR*ED[i][j]*EF[i][j]*ET[i][j])/(ATc*365*24)
    # HQ calculate
    HQ = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            if Rfc != 0:
                HQ[i][j] = (EF[i][j]*ED[i][j]*(ET[i][j]/24)*Cia[i][j])/(Rfc*1000*ATnc[i][j]*365)
            else:
                HQ[i][j] = -9999
    # Cca, Cnca calculate
    mIURTCE_R = 1
    IURTCE_R = 1
    TCR = 1.0e-6
    THQ = 1
    Cca = [[0 for j in range(row)] for i in range(column)]
    Cnca = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            if chem == 165:
                Cca[i][j] = 1/((EF[i][j]*MMOAF*ET[i][j]*mIURTCE_R/(TCR*ATc*365*24))+EF[i][j]*ED[i][j]*ET[i][j]*IURTCE_R/(TCR*ATc*365*24))
                Cnca[i][j] = Cca[i][j]
            else:
                if IUR != 0 and Rfc != 0:
                    Cca[i][j] = (TCR*ATc*365*24)/(EF[i][j]*ED[i][j]*ET[i][j]*IUR)
                    Cnca[i][j] = (THQ*Rfc*ATnc[i][j]*365*24*1000)/(EF[i][j]*ED[i][j]*ET[i][j])
                else:
                    Cca[i][j] = -9999
                    Cnca[i][j] = -9999
    if Source == 0:
        data = {
        "VFwesp": VFwesp_6a,
        "Qsoil": Qsoil,
        "Risk": Risk,
        "HQ": HQ,
        "Cca": Cca,
        "Cnca": Cnca
        }
    elif Source == 1:
        data = {
        "VFsesp": VFsesp_4a,
        "Qsoil": Qsoil,
        "Risk": Risk,
        "HQ": HQ,
        "Cca": Cca,
        "Cnca": Cnca
        }
    return jsonify(data)

@app.route('/multipleSource', methods=['POST'])
def multipleSource():
    inputdata = request.get_json()
    chemNum = int(inputdata['chemNum'])
    chem_input = inputdata['chem']
    S_input = inputdata['S']
    Hc_input = inputdata['Hc']
    Dair_input = inputdata['Dair']
    Dwater_input = inputdata['Dwater']
    DHvb_input = inputdata['DHvb']
    Tc_input = inputdata['Tc']
    Tb_input = inputdata['Tb']
    MW_input = inputdata['MW']
    IUR_input = inputdata['IUR']
    Rfc_input = inputdata['Rfc']
    Mut_input = inputdata['Mut']
    Source = int(inputdata['Source'])
    Ts = float(inputdata['Ts'])
    Organic_input = inputdata['Organic']
    Koc_input = inputdata['Koc']
    kd = float(inputdata['kd'])
    pH = float(inputdata['pH'])
    nSA = float(inputdata['nSA'])
    nwSA = float(inputdata['nwSA'])
    nairSA = float(inputdata['nairSA'])
    rhoSA = float(inputdata['rhoSA'])
    hcz = float(inputdata['hcz'])
    ncz = float(inputdata['ncz'])
    nwcz = float(inputdata['nwcz'])
    naircz = float(inputdata['naircz'])
    buildingType = int(inputdata['buildingType'])
    Cmedium_input = inputdata['Cmedium']
    WT = float(inputdata['WT'])
    LE = float(inputdata['LE'])
    foc_input = inputdata['foc']
    Lb = float(inputdata['Lb'])
    Lf = float(inputdata['Lf'])
    eta = float(inputdata['eta'])
    Abf = float(inputdata['Abf'])
    Hb = float(inputdata['Hb'])
    ach = float(inputdata['ach'])
    Qsoil_Qb = float(inputdata['Qsoil_Qb'])
    Ex = int(inputdata['Ex'])
    S = [0 for i in range(chemNum)]
    Hc = [0 for i in range(chemNum)]
    Dair = [0 for i in range(chemNum)]
    Dwater = [0 for i in range(chemNum)]
    DHvb = [0 for i in range(chemNum)]
    Tc = [0 for i in range(chemNum)]
    Tb = [0 for i in range(chemNum)]
    MW = [0 for i in range(chemNum)]
    IUR = [0 for i in range(chemNum)]
    Rfc = [0 for i in range(chemNum)]
    Mut = [0 for i in range(chemNum)]
    Organic = [0 for i in range(chemNum)]
    Koc = [0 for i in range(chemNum)]
    Cmedium = [0 for i in range(chemNum)]
    foc = [0 for i in range(chemNum)]
    for i in range(chemNum):
        S[i] = float(S_input[i])
        Hc[i] = float(Hc_input[i])
        Dair[i] = float(Dair_input[i])
        Dwater[i] = float(Dwater_input[i])
        DHvb[i] = float(DHvb_input[i])
        Tc[i] = float(Tc_input[i])
        Tb[i] = float(Tb_input[i])
        MW[i] = float(MW_input[i])
        IUR[i] = float(IUR_input[i])
        Rfc[i] = float(Rfc_input[i])
        Mut[i] = float(Mut_input[i])
        Organic[i] = float(Organic_input[i])
        Koc[i] = float(Koc_input[i])
        Cmedium[i] = float(Cmedium_input[i])
        foc[i] = float(foc_input[i])
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
    Qb = Abf*Hb*ach
    Qsoil = Qsoil_Qb*Qb
    Ls = LE-WT
    hSA = Ls
    Cs = [0 for i in range(chemNum)]
    for i in range(chemNum):
        Cs[i] = Hs*Cmedium[i]*1000
    # VFwesp calculate CM6a
    if Source == 0:
        DeffA_6a = [0 for i in range(chemNum)]
        DeffCZ_6a = [0 for i in range(chemNum)]
        DeffT_6a = [0 for i in range(chemNum)]
        A_param_6a = [0 for i in range(chemNum)]
        B_param_6a = [0 for i in range(chemNum)]
        C_param_6a = [0 for i in range(chemNum)]
        VFwesp_6a = [0 for i in range(chemNum)]
        for i in range(chemNum):
            DeffA_6a[i] = Dair[i]*(math.pow((nSA-nwSA),3.33)/math.pow(nSA,2))+(Dwater[i]/Hs)*(math.pow(nwSA,3.33)/math.pow(nSA,2))
            DeffCZ_6a[i] = Dair[i]*(math.pow((ncz-nwcz),3.33)/math.pow(ncz,2))+(Dwater[i]/Hs)*(math.pow(nwcz,3.33)/math.pow(ncz,2))
            DeffT_6a[i] = (hSA-Lb)/((hSA-Lb-hcz)/DeffA_6a[i]+hcz/DeffCZ_6a[i])
            if Qsoil == 0:
                A_param_6a[i] = (DeffT_6a[i]*(Abf+4*Lb*math.sqrt(Abf)*0.36))/(Qb*(Ls-Lb))
                VFwesp_6a[i] = A_param_6a[i]/(1+A_param_6a[i]+((DeffT_6a[i]*Lf/((Ls-Lb)*DeffA_6a[i]*eta))))
            elif Qsoil > 0:
                A_param_6a[i] = (DeffT_6a[i]*(Abf+4*Lb*math.sqrt(Abf)*0.36))/(Qb*(Ls-Lb))
                B_param_6a[i] = (Qsoil_Qb*Qb*Lf)/(DeffA_6a[i]*eta*(Abf+4*Lb*math.sqrt(Abf))*0.36)
                C_param_6a[i] = Qsoil_Qb[i][j]
                VFwesp_6a[i] = (A_param_6a[i]*math.exp(B_param_6a[i]))/(math.exp(B_param_6a[i])+A_param_6a[i]+(A_param_6a[i]/C_param_6a[i])*(math.exp(B_param_6a[i])-1))
    # VFsesp calculate CM4
    if Source == 1:
        ks = [0 for i in range(chemNum)]
        DeffA_4a = [0 for i in range(chemNum)]
        DeffCZ_4a = [0 for i in range(chemNum)]
        DeffT_4a = [0 for i in range(chemNum)]
        A_param_4a = [0 for i in range(chemNum)]
        B_param_4a = [0 for i in range(chemNum)]
        C_param_4a = [0 for i in range(chemNum)]
        VFsesp_4a = [0 for i in range(chemNum)]
        DeffA_4a[i] = Dair[i]*(math.pow((nSA-nwSA),3.33)/math.pow(nSA,2))+(Dwater[i]/Hs)*(math.pow(nwSA,3.33)/math.pow(nSA,2))
        DeffCZ_4a[i] = Dair[i]*(math.pow((ncz-nwcz),3.33)/math.pow(ncz,2))+(Dwater[i]/Hs)*(math.pow(nwcz,3.33)/math.pow(ncz,2))
        for i in range(chemNum):
            if Organic == 0:
                ks[i] = kd
            else:
                ks[i] = Koc[i]*foc[i]
                DeffA_4a[i] = Dair[i]*(math.pow((nSA-nwSA),3.33)/math.pow(nSA,2))+(Dwater[i]/Hs)*(math.pow(nwSA,3.33)/math.pow(nSA,2))
                DeffCZ_4a[i] = Dair[i]*(math.pow((ncz-nwcz),3.33)/math.pow(ncz,2))+(Dwater[i]/Hs)*(math.pow(nwcz,3.33)/math.pow(ncz,2))
                DeffT_4a[i] = (hSA-Lb)/((hSA-Lb-hcz)/DeffA_4a[i]+hcz/DeffCZ_4a[i])
                A_param_4a[i] = (Hs*rhoSA)/(nwSA+ks[i]*rhoSA+Hs*nairSA)
                B_param_4a[i] = (Qsoil_Qb*Qb*Lf)/(DeffA_4a[i]*eta*(Abf+4*Lb*math.sqrt(Abf))*0.36)
                C_param_4a[i] = (DeffA_4a[i]*(Abf+4*Lb*math.sqrt(Abf))*0.36)/(Qb*Ls)
                if Qsoil == 0:
                    VFsesp_4a[i] = (A_param_4a[i]*C_param_4a[i])/(1+A_param_4a[i]+((DeffT_4a[i]*Lf)/Ls*DeffA_4a[i]*eta))
                elif Qsoil > 0:
                    VFsesp_4a[i] = (A_param_4a[i]*C_param_4a[i]*math.exp(B_param_4a[i]))/(math.exp(B_param_4a[i])+C_param_4a[i]+(A_param_4a[i]/C_param_4a[i])*(math.exp(B_param_4a[i])-1))
 
    return 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)