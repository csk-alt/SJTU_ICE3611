from flask import Flask, redirect, render_template, request, url_for
from daltonlens import convert, simulate, generate
import matplotlib.pyplot as plt
import numpy as np
from simulate_m import LMSsim

app = Flask(__name__, static_folder="templates/static", template_folder="templates")
vienot1999 = simulate.Simulator_Vienot1999(convert.LMSModel_sRGB_SmithPokorny75())
brettel1997 = simulate.Simulator_Brettel1997(convert.LMSModel_sRGB_SmithPokorny75())
brettel1997_vischeck = simulate.Simulator_Vischeck()
machado2009 = simulate.Simulator_Machado2009()
coblisv1 = simulate.Simulator_CoblisV1()
coblisv2 = simulate.Simulator_CoblisV2()

methods = {"1997":brettel1997, "vischeck":brettel1997_vischeck, "1999":vienot1999, "V1":coblisv1, "V2":coblisv2, "2009":machado2009, "LMS":LMSsim}

def simula(file, method, severity):
    img_ori = plt.imread("./templates"+file)[..., :3]
    if img_ori.dtype != np.uint8:
        img_ori = np.uint8((img_ori*255))
    method = methods[method]
    simulat_img = method.simulate_cvd(img_ori, simulate.Deficiency.PROTAN, severity[0])
    plt.imsave("./templates/static/picture/PROTAN_tem.png", simulat_img)

    simulat_img = method.simulate_cvd(img_ori, simulate.Deficiency.DEUTAN, severity[1])
    plt.imsave("./templates/static/picture/DEUTAN_tem.png", simulat_img)

    simulat_img = method.simulate_cvd(img_ori, simulate.Deficiency.TRITAN, severity[2])
    plt.imsave("./templates/static/picture/TRITAN_tem.png", simulat_img)
    return 

def corr(file, method):
    img_ori = plt.imread("./templates"+file)[..., :3]
    if img_ori.dtype != np.uint8:
        img_ori = np.uint8((img_ori*255))
    method = methods[method]
    simulat_img, corr_img = method.simulate_cvd(img_ori, simulate.Deficiency.PROTAN, corr=True)
    plt.imsave("./templates/static/picture/PROTAN_tem.png", simulat_img)
    plt.imsave("./templates/static/picture/PROTAN_corr_tem.png", corr_img)
    plt.imsave("./templates/static/picture/PROTAN_corrsim_tem.png", method.simulate_cvd(corr_img, simulate.Deficiency.PROTAN))

    simulat_img, corr_img = method.simulate_cvd(img_ori, simulate.Deficiency.DEUTAN, corr=True)
    plt.imsave("./templates/static/picture/DEUTAN_tem.png", simulat_img)
    plt.imsave("./templates/static/picture/DEUTAN_corr_tem.png", corr_img)
    plt.imsave("./templates/static/picture/DEUTAN_corrsim_tem.png", method.simulate_cvd(corr_img, simulate.Deficiency.DEUTAN))

    simulat_img, corr_img = method.simulate_cvd(img_ori, simulate.Deficiency.TRITAN, corr=True)
    plt.imsave("./templates/static/picture/TRITAN_tem.png", simulat_img)
    plt.imsave("./templates/static/picture/TRITAN_corr_tem.png", corr_img)
    plt.imsave("./templates/static/picture/TRITAN_corrsim_tem.png", method.simulate_cvd(corr_img, simulate.Deficiency.TRITAN))
    return 
    

formal_filename = None

@app.route('/')
def skip():
    return redirect(url_for('simulat'))

@app.route('/simulator', methods=['POST', 'GET'])
def simulat():
    global formal_filename
    if request.method == "POST":
        result = False
        fil = request.files['file']
        se = []
        sev = request.form.get("severity")
        sev_d = request.form.get("severity_d")
        sev_t = request.form.get("severity_t")
        if sev:
            se.append(int(sev)/10)
            se.append(int(sev_d)/10)
            se.append(int(sev_t)/10)
        method = request.form.get("method")
        n = fil.filename
        t = n.split('.')[-1]
        file_name = "/static/picture/temashdfiopqw"+'.' +t
        fil.save("./templates"+file_name)
        
        if not t:
            file_name = formal_filename
        else:
            formal_filename = file_name
        if sev:
            simula(file_name, method, se)
            result = True
        return render_template("b.html", sim="SIMULATOR", origin_image=file_name, severity=sev, result=result, formal_sev = sev, formal_sev_d = sev_d, formal_sev_t = sev_t, methd = method)#redirect(url_for('simulate', origin_image=file_name))
    
    formal_filename = None

    return render_template("b.html", sim="SIMULATOR")#, origin_image="/static/picture/temashdfiopqw"+'.png')


@app.route('/corrector', methods=['GET', 'POST'])
def generate():
    global formal_filename
    if request.method == "POST":
        result = False
        fil = request.files['file']
        # se = []
        # sev = request.form.get("severity")
        # sev_d = request.form.get("severity_d")
        # sev_t = request.form.get("severity_t")
        # if sev:
        #     se.append(int(sev)/10)
        #     se.append(int(sev_d)/10)
        #     se.append(int(sev_t)/10)
        # method = request.form.get("method")
        n = fil.filename
        t = n.split('.')[-1]
        file_name = "/static/picture/temashdfiopqw"+'.' +t
        fil.save("./templates"+file_name)
        
        if not t:
            file_name = formal_filename
        else:
            formal_filename = file_name
        # if sev:
        corr(file_name, "LMS")
        result = True
        return render_template("corr.html", sim="CORRECTOR", origin_image=file_name, result=result)
    
    formal_filename = None

    return render_template("corr.html", sim="CORRECTOR")






if __name__ == '__main__':
    app.run(debug=False, port=8081)
