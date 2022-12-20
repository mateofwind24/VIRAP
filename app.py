import math
from flask import Flask, request, url_for, render_template, redirect, jsonify
app = Flask(__name__)

@app.route('/')
def main():
    return "Hello World!"


@app.route('/module4',  methods=['POST'])
def module4():
    totalnum = 10000
    data = [[0 for j in range(10)] for i in range(1)]
    '''
    list param(new use)
    henry's constant: DHvs, Rc, Tsk, Tr, HR, R, Ts
    DeffA: Dair, nSA, nwSA, Dwater
    DeffCZ: nCZ, nwCZ
    DeffT: hSA, Lb, hCZ
    Qb: Abf, Hb, ach
    Qsoil: Qsoil_Qb
    A_param: Ls, Lf, eta
    Risk: EX
    '''
    inputdata = request.get_json()
    
    for i in range(1):
        # VFwesp calculate
        DHvs = inputdata[i]['DHvs']
        Rc = inputdata[i]['Rc']
        Tsk = inputdata[i]['Tsk']
        Tr = inputdata[i]['Tr']
        HR = inputdata[i]['HR']
        R = inputdata[i]['R']
        Ts = inputdata[i]['Ts']
        Dair = inputdata[i]['Dair']
        nSA = inputdata[i]['nSA']
        nwSA = inputdata[i]['nwSA']
        Dwater = inputdata[i]['Dwater']
        nCZ = inputdata[i]['nCZ']
        nwCZ = inputdata[i]['nwCZ']
        hSA = inputdata[i]['hSA']
        Lb = inputdata[i]['Lb']
        hCZ = inputdata[i]['hCZ']
        Abf = inputdata[i]['Abf']
        Hb = inputdata[i]['Hb']
        ach = inputdata[i]['ach']
        Qsoil_Qb = inputdata[i]['Qsoil_Qb']
        Ls = inputdata[i]['Ls']
        Lf = inputdata[i]['Lf']
        eta = inputdata[i]['eta']
        HS = ((math.exp(-(DHvs/Rc)*((1/Tsk)-(1/Tr))))*HR)/(R*Ts)
        DeffA = Dair*(math.pow((nSA-nwSA),3.33)/math.pow(nSA,2))+(Dwater/HS)*(math.pow(nwSA,3.33)/math.pow(nSA,2))
        DeffCZ = Dair*(math.pow((nCZ-nwCZ),3.33)/math.pow(nCZ,2))+(Dwater/HS)*(math.pow(nwCZ,3.33)/math.pow(nCZ,2))
        DeffT = (hSA-Lb)/((hSA-Lb-hCZ)/DeffA+hCZ/DeffCZ)
        Qb = Abf*Hb*ach
        Qsoil = Qsoil_Qb*Qb
        if Qsoil == 0:
            A_param = (DeffT*(Abf+4*Lb*math.sqrt(Abf)*0.36))/(Qb*(Ls-Lb))
            VFwesp = A_param/(1+A_param+((DeffT*Lf)/((Ls-Lb)*DeffA*eta)))
        else:
            A_param = (DeffT*(Abf+4*Lb*math.sqrt(Abf)*0.36))/(Qb*(Ls-Lb))
            B_param = (Qsoil_Qb*Qb*Lf)/(DeffA*eta*(Abf+4*Lb*math.sqrt(Abf))*0.36)
            C_param = Qsoil_Qb
            VFwesp = (A_param*(math.exp(B_param)))/(math.exp(B_param)+A_param+(A_param/C_param)*(math.exp(B_param)-1))
        # Risk calculate
        ATc = 70
        MMOAF = 72
        EX = inputdata[i]['EX']
        if EX == 0:
            EF = 350
            ED = 26
            ET = 24
        else:
            EF = 250
            ED = 25
            ET = 8
        mIURTCE_R_GW = 1.0e-6;
        IURTCE_R_GW = 3.1e-6;
        mIURTCE_C_GW = 4.1e-6;
        IURTCE_C_GW = 4.1e-6;

        # HQ calculate







        data[i][0] = mIURTCE_C_GW
        data[i][1] = Qsoil
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)