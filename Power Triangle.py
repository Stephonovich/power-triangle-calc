# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Power Triangle.py
#
# Created on: 2017-04-13
# Stephan Garland
# stephan.marc.garland@gmail.com
#
# Given two inputs (kW, kVA, kVAR, PF, or theta), calculates the others
# and graphs the resulting triangle as a PNG (requires matplotlib)



import math as m
try:
    import tkinter as tk  # Python 3.x
    from tkinter import messagebox as tkMsg
except ImportError:  # Python 2.x
    import Tkinter as tk
    import tkMessageBox as tkMsg
import matplotlib.pyplot as plt


fields = 'kW', 'kVA', 'kVAR', 'PF', 'Theta'
labels = {'kW':'kW (Real)', 'kVA':'kVA (Apparent)', 'kVAR':'kVAR (Reactive)',\
          'PF':'PF (0.00-1.00)', 'Theta':'Theta (Degrees)'}

def fetch(entries):
    inputs = {}
    for entry in entries:
        field = entry[0]
        text = entry[1].get() # User input for each textbox
        if text: # True if field isn't blank
            inputs[field] = float(text)
    if inputs.get('Theta') is not None: # If Theta isn't given, don't convert
        if inputs.get('Theta') > 0 and inputs.get('Theta') <= 90:
            inputs['Theta'] = m.radians(inputs['Theta']) # Use radians internally
        else:
            tkMsg.showerror("Error","Theta must be 0 < x < 90")
            quitProg()
    if inputs.get('kVA',0) <= max(inputs.get('kW',0),inputs.get('kVAR',0))\
        and inputs.get('kVA') is not None:
            tkMsg.showerror("Error","kVA must be > any other side")
            quitProg()
    if inputs.get('PF') is not None:
        if inputs.get('PF') < 0 or inputs.get('PF') > 1:
            pfError = tkMsg.askyesno("PF out of range", "You entered {0} for PF\
            \nDid you mean {1}?".format(inputs['PF'],inputs['PF']/100))
            if pfError == 1:
                inputs['PF'] = inputs['PF']/100
            if pfError == 0:
                tkMsg.showerror("Error","PF must be 0 < x < 1")
                quitProg() 
    global calcInputs
    calcInputs = inputs
    root.quit()
        


def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=25, text=labels[field], anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries

    
    
def resultsWindow(fields):
    root.withdraw()
    top = tk.Toplevel()
    b3 = tk.Button(top, text = 'Quit', command=quitProg)
    b3.pack(side=tk.RIGHT, padx=5, pady=5)
    for field in fields:
        row = tk.Frame(top)
        lab = tk.Label(row, width=25, text=field, anchor='w')
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
    

    
def returnResults(kW, kVAR, kVA, PF, Theta):
    d = locals()
    roundedOut = {}
    for k,v in d.items():
        if k == 'Theta':
            # Cast theta to a string to allow concatenating with degree symbol
            # Also convert theta to degrees; all internal calcs are in radians
            roundedOut['Theta'] = str(round(m.degrees(v),3)) + "\xb0"
        else:
            roundedOut[k] = round(v,3)
    root.quit()
    resultsWindow(roundedOut.items())
    drawViz(kW, kVAR, kVA, m.degrees(Theta))
    
    
    
def from_KW_KVA(kW, kVA):
    Theta = m.acos(kW / kVA)
    kVAR = m.sin(Theta) * kVA
    PF = m.cos(Theta)
    returnResults(kW, kVAR, kVA, PF, Theta)


    
def from_KW_KVAR(kW, kVAR):
    Theta = m.atan(kVAR / kW)
    PF = m.cos(Theta)
    kVA = kW / PF
    returnResults(kW, kVAR, kVA, PF, Theta)
    
    
    
def from_KW_PF(kW, PF):
    Theta = m.acos(PF)
    kVAR = m.tan(Theta) * kW
    kVA = kW / PF
    returnResults(kW, kVAR, kVA, PF, Theta)
        
        
        
def from_KW_THETA(kW, Theta):
    kVAR = m.tan(Theta) * kW
    PF = m.cos(Theta)
    kVA = kW / PF
    returnResults(kW, kVAR, kVA, PF, Theta)
    
    
def from_KVA_KVAR(kVA, kVAR):
    Theta = (m.asin(kVAR/kVA))
    PF = m.cos(Theta)
    kW = kVA * PF
    returnResults(kW, kVAR, kVA, PF, Theta)
    
    
    
def from_KVA_PF(kVA, PF):
    Theta = m.acos(PF)
    kW = kVA * PF
    kVAR = m.tan(Theta)*kW
    returnResults(kW, kVAR, kVA, PF, Theta)



def from_KVA_THETA(kVA, Theta):
    PF = m.cos(Theta)
    kW = kVA * PF
    kVAR = m.tan(Theta)*kW
    returnResults(kW, kVAR, kVA, PF, Theta)



def from_KVAR_PF(kVAR, PF):
    Theta = m.acos(PF)
    kVA = kVAR / m.sin(Theta)
    kW = kVA * PF
    returnResults(kW, kVAR, kVA, PF, Theta)



def from_KVAR_THETA(kVAR, Theta):
    PF = m.cos(Theta)
    kVA = kVAR / m.sin(Theta)
    kW = kVA * PF
    returnResults(kW, kVAR, kVA, PF, Theta)
    
    

def catchInput(PF, Theta):
    tkMsg.showwarning("Inadequate Data", "Power Factor is cos(theta).\nPlease use other values.")
    quitProg()
    
    
    
def getInput():
    root.deiconify()
    root.title("Power Triangle Calculator")
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))
    b1 = tk.Button(root, text = 'Calculate', command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text = 'Quit', command=quitProg)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()

    
    
def drawViz(kW, kVAR, kVA, Theta):
    p = [0, 0] # x = 0, y = 0 (real power base)
    q = [kW, 0] # x = kW, y = 0 (real power scalar / reactive power base)
    s = [kW, kVAR] # x = kW, y = kVAR (apparent power top)
    slope = kVAR/kW
    points = [p, q, s]
    plt.axes()
    polygon = plt.Polygon(points)
    plt.gca().add_patch(polygon)
    plt.axis('scaled')
    # All xy values were established with trial and error, change as desired
    plt.annotate('{0} kW'.format(round(kW,2)), xy=(0.5,-0.1), xycoords='axes fraction')
    plt.annotate('{0} kVAR'.format(round(kVAR,2)), xy=(1.05,0.5), xycoords='axes fraction')
    plt.annotate('{0} kVA'.format(round(kVA,2)), xy=((0.25*kW),\
        (0.5*(slope*kW)+(0.05*kW))), xycoords='data')
    #$\\x$ is LaTeX encoding for matplotlib
    plt.annotate(u'$\\theta$ {0} \xb0'.format(round(Theta,3)),\
        xy=((0.05*kW),(0.02*kVAR)), xycoords='data')
    plt.show()
 

 
def restartProg():
    #root.quit()
    main()
    
    

def quitProg():
    raise SystemExit
    
    

def main():
    root.withdraw()

    getInput()

    given_keys = []

    for key in sorted(fields):
        if key in calcInputs:
            given_keys.append(key)

    calc_key = '_'.join(given_keys)

    dispatch = {

            'kW_kVA' : from_KW_KVA,
            'kVA_kW' : from_KW_KVA,
            'kW_kVAR' : from_KW_KVAR,
            'kVAR_kW' : from_KW_KVAR,
            'kW_PF' : from_KW_PF,
            'PF_kW' : from_KW_PF,
            'kW_Theta' : from_KW_THETA,
            'Theta_kW' : from_KW_THETA,
            'kVA_kVAR' : from_KVA_KVAR,
            'kVAR_kVA' : from_KVA_KVAR,
            'kVA_PF' : from_KVA_PF,
            'PF_kVA' : from_KVA_PF,
            'kVA_Theta' : from_KVA_THETA,
            'Theta_kVA' : from_KVA_THETA,
            'kVAR_PF' : from_KVAR_PF,
            'PF_kVAR' : from_KVAR_PF,
            'kVAR_Theta' : from_KVAR_THETA,
            'Theta_kVAR' : from_KVAR_THETA,
            'PF_Theta' : catchInput,
            'Theta_PF' : catchInput
            
                } # PF_Theta doesn't work as PF is cos(theta)
                  # Couldn't find a better way to sort, so foo_bar | bar_foo works
                
    calc_function = dispatch[calc_key] # e.g. calc_function becomes from_KW_KVA
    calc_function(**calcInputs) # e.g. from_KW_KVA is called with calcInputs as kwargs

    
root = tk.Tk()
root.withdraw()    
tkMsg.showinfo("Usage", "Please enter only two values.\nTheta and Power Factor cannot be used together.")
main()