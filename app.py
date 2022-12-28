import math
from tkinter import Tcl, TclError
from flask import Flask, request, url_for, render_template, redirect, jsonify
app = Flask(__name__)

@app.route('/')
def main():
    return "Hello VIRAP!"

@app.route('/module4_unchange_param_input', methods=['POST'])
def module4_unchange_param_input():
    input1 = request.get_json()     # postman no list just dic
    global row
    global column
    global totalnum
    global chem     #plus 1~283 number
    global S
    global Hc
    global Hr       #plus
    global Hs       #plus
    global Dair
    global Dwater
    global DHvb
    global Tc
    global Tb
    global MW
    global IUR
    global Rfc
    global Mut      # No=0, Yes=1, VC=2
    global n        #cal
    global Ls
    global Ts
    global Cs       # grid cal plus
    global Cmedium  # grid
    global WT       # grid
    global LE       # grid
    global foc      # grid
    global Organic  # No=0 Yes=1
    global Koc
    global kd
    global pH
    global hSA      #cal
    global nSA
    global nwSA
    global nairSA
    global rhoSA
    global hcz
    global ncz
    global nwcz
    global naircz
    global Lb
    global Lf
    global eta
    global Abf
    global Hb
    global ach
    global Qsoil_Qb
    global Qb
    global Qsoil
    global Ex
    global ATc      #cal
    global ATnc     #cal
    global MMOAF    #cal
    global EF       #cal
    global ED       #cal
    global ET       #cal
    global Cia      #plus
    column = input1['column']
    row = input1['row']
    totalnum = column*row
    chem = input1['chem']
    S = input1['S']
    Hc = input1['Hc']
    Dair = input1['Dair']
    Dwater = input1['Dwater']
    DHvb = input1['DHvb']
    Tc = input1['Tc']
    Tb = input1['Tb']
    MW = input1['MW']
    IUR = input1['IUR']
    Rfc = input1['Rfc']
    Mut = input1['Mut']
    Ts = input1['Ts']
    Organic = input1['Organic']
    Koc = input1['Koc']
    kd = input1['kd']
    pH = input1['pH']
    nSA = input1['nSA']
    nwSA = input1['nwSA']
    nairSA = input1['nairSA']
    rhoSA = input1['rhoSA']
    hcz = input1['hcz']     #cm
    ncz = input1['ncz']
    nwcz = input1['nwcz']
    naircz = input1['naircz']
    Lb = input1['Lb']
    Lf = input1['Lf']
    eta = input1['eta']
    Abf = input1['Abf']
    Hb = input1['Hb']
    ach = input1['ach']
    Qsoil_Qb = input1['Qsoil_Qb']
    Ex = input1['Ex']
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
    Qb = Abf*Hb*ach
    Qsoil = Qsoil_Qb*Qb
    DHvs = DHvb*(math.pow((1-Ts/Tc)/(1-Tb/Tc),n))
    Hs = (math.exp(-(DHvs/Rc)*(1/Ts-1/Tr))*Hc)/(R*Ts)
    Cs = [[0 for j in range(row)] for i in range(column)]
    Ls = [[0 for j in range(row)] for i in range(column)]
    hSA = [[0 for j in range(row)] for i in range(column)]
    for i in range(column):
        for j in range(row):
            Cs[i][j] = Hs*Cmedium[i][j]*1000
            Ls[i][j] = LE[i][j]-WT[i][j]
            hSA[i][j] = Ls[i][j]

@app.route('/module4_Cmedium_input', methods=['POST'])
def module4_Cmedium_input():
    global Cmedium
    global column
    global row
    Cmedium = [[0 for j in range(row)] for i in range(column)]
    input_Cmedium = request.get_json()
    for i in range(column):
        for j in range(row):
            Cmedium[i][j] = float(input_Cmedium[i][j])
    return Cmedium

@app.route('/module4_WT_input', methods=['POST'])
def module4_WT_input():
    global WT
    global column
    global row
    WT = [[0 for j in range(row)] for i in range(column)]
    input_WT = request.get_json()
    for i in range(column):
        for j in range(row):
            WT[i][j] = float(input_WT[i][j])
    return WT

@app.route('/module4_LE_input', methods=['POST'])
def module4_LE_input():
    global LE
    global column
    global row
    LE = [[0 for j in range(row)] for i in range(column)]
    input_LE = request.get_json()
    for i in range(column):
        for j in range(row):
            LE[i][j] = float(input_LE[i][j])
    return LE

@app.route('/module4_foc_input', methods=['POST'])
def module4_foc_input():
    global foc
    global column
    global row
    foc = [[0 for j in range(row)] for i in range(column)]
    input_foc = request.get_json()
    for i in range(column):
        for j in range(row):
            foc[i][j] = float(input_foc[i][j])
    return foc

@app.route('/module4_totalcalculate')
def module4_totalcalculate():
    global row
    global column
    global totalnum
    global chem     #plus 1~283 number
    global S
    global Hc
    global Hr       #plus
    global Hs       #plus
    global Dair
    global Dwater
    global DHvb
    global Tc
    global Tb
    global MW
    global IUR
    global Rfc
    global Mut      # No=0, Yes=1, VC=2
    global n        #cal
    global Ls
    global Ts
    global Cs       # grid cal plus
    global Cmedium  # grid
    global WT       # grid
    global LE       # grid
    global foc      # grid
    global Organic  # No=0 Yes=1
    global Koc
    global kd
    global pH
    global hSA      #cal
    global nSA
    global nwSA
    global nairSA
    global rhoSA
    global hcz
    global ncz
    global nwcz
    global naircz
    global Lb
    global Lf
    global eta
    global Abf
    global Hb
    global ach
    global Qsoil_Qb
    global Qb
    global Qsoil
    global Ex
    global ATc      #cal
    global ATnc
    global MMOAF    #cal
    global EF       #cal
    global ED       #cal
    global ET       #cal
    global Cia      #plus
    data = [[0 for j in range(10)] for i in range(1)]
    for i in range(1):
        # VFwesp calculate CM6a(Qs>0) loop
        DeffA_6a = Dair*(math.pow((nSA-nwSA),3.33)/math.pow(nSA,2))+(Dwater/Hs)*(math.pow(nwSA,3.33)/math.pow(nSA,2))
        DeffCZ_6a = Dair*(math.pow((ncz-nwcz),3.33)/math.pow(ncz,2))+(Dwater/Hs)*(math.pow(nwcz,3.33)/math.pow(ncz,2))
        DeffT_6a = (hSA-Lb)/((hSA-Lb-hcz)/DeffA_6a+hcz/DeffCZ_6a)
        if Qsoil == 0:
            A_param_6a = (DeffT_6a*(Abf+4*Lb*math.sqrt(Abf)*0.36))/(Qb*(Ls-Lb))
            VFwesp_6a = A_param_6a/(1+A_param_6a+((DeffT_6a*Lf)/((Ls-Lb)*DeffA_6a*eta)))
        else:
            A_param_6a = (DeffT_6a*(Abf+4*Lb*math.sqrt(Abf)*0.36))/(Qb*(Ls-Lb))
            B_param_6a = (Qsoil_Qb*Qb*Lf)/(DeffA_6a*eta*(Abf+4*Lb*math.sqrt(Abf))*0.36)
            C_param_6a = Qsoil_Qb
            VFwesp_6a = (A_param_6a*(math.exp(B_param_6a)))/(math.exp(B_param_6a)+A_param_6a+(A_param_6a/C_param_6a)*(math.exp(B_param_6a)-1))
        # VFsesp calculate CM4 loop
        if Organic == 0:
            ks = kd
        else:
            ks = Koc*foc    #loop
        DeffA_4a = Dair*(math.pow((nSA-nwSA),3.33)/math.pow(nSA,2))+(Dwater/Hs)*(math.pow(nwSA,3.33)/math.pow(nSA,2))
        DeffCZ_4a = Dair*(math.pow((ncz-nwcz),3.33)/math.pow(ncz,2))+(Dwater/Hs)*(math.pow(nwcz,3.33)/math.pow(ncz,2))  # my think
        DeffT_4a = (hSA-Lb)/((hSA-Lb-hcz)/DeffA_4a+hcz/DeffCZ_4a)   #my think
        A_param_4a = (Hs*rhoSA)/(nwSA+ks*rhoSA+Hs*nairSA)
        B_param_4a = (Qsoil_Qb*Qb*Lf)/(DeffA_4a*eta*(Abf+4*Lb*math.sqrt(Abf))*0.36)
        C_param_4a = (DeffA_4a*(Abf+4*Lb*math.sqrt(Abf))*0.36)/(Qb*Ls)
        if Qsoil == 0:
            VFsesp_4a = (A_param_4a*C_param_4a)/(1+A_param_4a+((DeffT_4a*Lf)/Ls*DeffA_4a*eta))
        else:
            VFsesp_4a = (A_param_4a*C_param_4a*math.exp(B_param_4a))/(math.exp(B_param_4a)+C_param_4a+(A_param_4a/C_param_4a)*(math.exp(B_param_4a)-1))
        # Risk calculate loop
        mIURTCE_R_GW = 1.0e-6;
        IURTCE_R_GW = 3.1e-6;
        mIURTCE_C_GW = 4.1e-6;
        IURTCE_C_GW = 4.1e-6;
        Cia = VFwesp_6a*Cs  #loop
        if chem == 258 and Ex == 0:
            Risk = (Cia*mIURTCE_R_GW*MMOAF*EF*ET)/(ATc*365*24) + (Cia*IURTCE_R_GW*ED*EF*ET)/(ATc*365*24)
        elif chem == 258 and Ex == 1:
            Risk = (Cia*mIURTCE_C_GW*MMOAF*EF*ET)/(ATc*365*24) + (Cia*IURTCE_C_GW*ED*EF*ET)/(ATc*365*24)
        elif Mut == 0 and Ex == 0:
            Risk = (IUR*EF*ED*ET*Cia)/(ATc*365*24)
        elif Mut == 0 and Ex == 1:
            Risk = (IUR*EF*ED*ET*Cia)/(ATc*365*24)
        elif Mut == 1 and chem != 258:                  # check no Ex
            Risk = (IUR*EF*MMOAF*ET*Cia)/(ATc*365*24)
        elif Mut == 2 and Ex == 0:
            Risk = Cia*(IUR+(IUR*ED*EF*ET)/(ATc*365*24))
        elif Mut == 2 and Ex == 1:
            Risk = Cia*(IUR*ED*EF*ET)/(ATc*365*24)
        # HQ calculate loop
            HQ = (EF*ED*(ET/24)*Cia)/(Rfc*1000*ATnc*365)
        # Cca, Cnca calculate
        mIURTCE_R = 1
        IURTCE_R = 1
        TCR = 1.0e-6
        THQ = 1
        if chem == 258:
            Cca = 1/((EF*MMOAF*ET*mIURTCE_R/(TCR*ATc*365*24))+EF*ED*ET*IURTCE_R/(TCR*ATc*365*24))
            Cnca = 1/((EF*MMOAF*ET*mIURTCE_R/(TCR*ATc*365*24))+EF*ED*ET*IURTCE_R/(TCR*ATc*365*24))
        else:
            Cca = (TCR*ATc*365*24)/(EF*ED*ET*IUR)
            Cnca = (THQ*Rfc*ATnc*365*24*1000)/(EF*ED*ET)
        data[i][0] = VFwesp_6a
        data[i][1] = VFsesp_4a
        data[i][2] = Risk
        data[i][3] = HQ
        data[i][4] = Cca
        data[i][5] = Cnca
        data[i][6] = Cia
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)