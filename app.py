import math
from tkinter import Tcl, TclError
from flask import Flask, request, url_for, render_template, redirect, jsonify
app = Flask(__name__)

@app.route('/')
def main():
    return "Hello VIRAP!"

@app.route('/module4', methods=['POST'])
def module4():
    inputdata = request.get_json()     # json no list just dic
    '''
    row
    column
    totalnum
    chem        # 1~283 number
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
    Lb          # gridinput
    Lf          # gridinput
    eta         # gridinput
    Abf         # gridinput
    Hb          # gridinput
    ach         # gridinput
    Qsoil_Qb    # gridinput
    Qb          # cal
    Qsoil       # cal
    Ex          # gridinput
    ATc         # cal
    ATnc        # cal
    MMOAF       # cal
    EF          # cal
    ED          # cal
    ET          # cal
    Cia         # cal
    '''
    column = inputdata['column']
    row = inputdata['row']
    totalnum = column*row
    chem = inputdata['chem']
    S = inputdata['S']
    Hc = inputdata['Hc']
    Dair = inputdata['Dair']
    Dwater = inputdata['Dwater']
    DHvb = inputdata['DHvb']
    Tc = inputdata['Tc']
    Tb = inputdata['Tb']
    MW = inputdata['MW']
    IUR = inputdata['IUR']
    Rfc = inputdata['Rfc']
    Mut = inputdata['Mut']
    Ts = inputdata['Ts']
    Organic = inputdata['Organic']
    Koc = inputdata['Koc']
    kd = inputdata['kd']
    pH = inputdata['pH']
    nSA = inputdata['nSA']
    nwSA = inputdata['nwSA']
    nairSA = inputdata['nairSA']
    rhoSA = inputdata['rhoSA']
    hcz = inputdata['hcz']     #cm
    ncz = inputdata['ncz']
    nwcz = inputdata['nwcz']
    naircz = inputdata['naircz']
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
            Lb[i][j] = float(Lb_input[i][j])
            Lf[i][j] = float(Lf_input[i][j])
            eta[i][j] = float(eta_input[i][j])
            Abf[i][j] = float(Abf_input[i][j])
            Hb[i][j] = float(Hb_input[i][j])
            ach[i][j] = float(ach_input[i][j])
            Qsoil_Qb[i][j] = float(Qsoil_Qb_input[i][j])
            Ex[i][j] = int(Ex_input[i][j])
    # constant, no grid param
    ATc = 70
    MMOAF = 72
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
            Cs[i][j] = Hs*Cmedium[i][j]*1000
            Ls[i][j] = LE[i][j]-WT[i][j]
            hSA[i][j] = Ls[i][j]
    # VFwesp calculate CM6a(Qs>0)
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
        if Qsoil == 0:
            A_param_6a[i][j] = (DeffT_6a[i][j]*(Abf[i][j]+4*Lb[i][j]*math.sqrt(Abf[i][j])*0.36))/(Qb[i][j]*(Ls[i][j]-Lb[i][j]))
            VFwesp_6a[i][j] = A_param_6a[i][j]/(1+A_param_6a[i][j]+((DeffT_6a[i][j]*Lf[i][j])/((Ls[i][j]-Lb[i][j])*DeffA_6a*eta[i][j])))
        else:
            A_param_6a[i][j] = (DeffT_6a[i][j]*(Abf[i][j]+4*Lb[i][j]*math.sqrt(Abf[i][j])*0.36))/(Qb[i][j]*(Ls[i][j]-Lb[i][j]))
            B_param_6a[i][j] = (Qsoil_Qb[i][j]*Qb[i][j]*Lf[i][j])/(DeffA_6a*eta[i][j]*(Abf[i][j]+4*Lb[i][j]*math.sqrt(Abf[i][j]))*0.36)
            C_param_6a[i][j] = Qsoil_Qb[i][j]
            VFwesp_6a[i][j] = (A_param_6a[i][j]*(math.exp(B_param_6a[i][j])))/(math.exp(B_param_6a[i][j])+A_param_6a[i][j]+(A_param_6a[i][j]/C_param_6a[i][j])*(math.exp(B_param_6a[i][j])-1))
    # VFsesp calculate CM4
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
            if Qsoil == 0:
                VFsesp_4a[i][j] = (A_param_4a[i][j]*C_param_4a[i][j])/(1+A_param_4a[i][j]+((DeffT_4a[i][j]*Lf[i][j])/Ls[i][j]*DeffA_4a[i][j]*eta[i][j]))
            else:
                VFsesp_4a[i][j] = (A_param_4a[i][j]*C_param_4a[i][j]*math.exp(B_param_4a[i][j]))/(math.exp(B_param_4a[i][j])+C_param_4a[i][j]+(A_param_4a[i][j]/C_param_4a[i][j])*(math.exp(B_param_4a[i][j])-1))
    # Risk calculate loop
    mIURTCE_R_GW = 1.0e-6;
    IURTCE_R_GW = 3.1e-6;
    mIURTCE_C_GW = 4.1e-6;
    IURTCE_C_GW = 4.1e-6;
    Cia = [[0 for j in range(row)] for i in range(column)]
    Risk = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            Cia[i][j] = VFwesp_6a[i][j]*Cs[i][j]
            if chem == 258 and Ex == 0:
                Risk[i][j] = (Cia[i][j]*mIURTCE_R_GW*MMOAF*EF*ET)/(ATc*365*24) + (Cia[i][j]*IURTCE_R_GW*ED*EF*ET)/(ATc*365*24)
            elif chem == 258 and Ex == 1:
                Risk[i][j] = (Cia[i][j]*mIURTCE_C_GW*MMOAF*EF*ET)/(ATc*365*24) + (Cia[i][j]*IURTCE_C_GW*ED*EF*ET)/(ATc*365*24)
            elif Mut == 0:                          # check no Ex
                Risk[i][j] = (IUR*EF*ED*ET*Cia[i][j])/(ATc*365*24)
            elif Mut == 1 and chem != 258:          # check no Ex
                Risk[i][j] = (IUR*EF*MMOAF*ET*Cia[i][j])/(ATc*365*24)
            elif Mut == 2 and Ex == 0:
                Risk[i][j] = Cia[i][j]*(IUR+(IUR*ED*EF*ET)/(ATc*365*24))
            elif Mut == 2 and Ex == 1:
                Risk[i][j] = Cia[i][j]*(IUR*ED*EF*ET)/(ATc*365*24)
    # HQ calculate
    HQ = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            if Rfc != 0:
                HQ[i][j] = (EF*ED*(ET/24)*Cia[i][j])/(Rfc*1000*ATnc*365)
            else:
                HQ[i][j] = -9999
    # Cca, Cnca calculate
    mIURTCE_R = 1
    IURTCE_R = 1
    TCR = 1.0e-6
    THQ = 1
    if chem == 258:
        Cca = 1/((EF*MMOAF*ET*mIURTCE_R/(TCR*ATc*365*24))+EF*ED*ET*IURTCE_R/(TCR*ATc*365*24))
        Cnca = 1/((EF*MMOAF*ET*mIURTCE_R/(TCR*ATc*365*24))+EF*ED*ET*IURTCE_R/(TCR*ATc*365*24))
    else:
        if IUR != 0 and Rfc != 0:
            Cca = (TCR*ATc*365*24)/(EF*ED*ET*IUR)
            Cnca = (THQ*Rfc*ATnc*365*24*1000)/(EF*ED*ET)
        else:
            Cca = -9999
            Cnca = -9999
    data = {
        "chem": chem,
        "VFwesp": VFwesp_6a,
        "VFsesp": VFsesp_4a,
        "Risk": Risk,
        "HQ": HQ,
        "Cca": Cca,
        "Cnca": Cnca
        }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)