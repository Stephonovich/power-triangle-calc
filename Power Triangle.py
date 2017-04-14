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
# Does not currently do sanity checking outside of math domain errors
# Commented out imports and drawLegend function are TODOs

import math as m
try:
    import tkinter as tk  # Python 3.x
except ImportError:  # Python 2.x
    import Tkinter as tk
import matplotlib.pyplot as plt
#import numpy as np
import pymsgbox.native as gui
#from scipy import ndimage

fields = 'kW', 'kVA', 'kVAR', 'PF', 'Theta'
#labels = 'kW', 'kVA (Hypotenuse)', \
#'kVAR', 'PF (0.00 - 1.00)', 'Theta (Degrees)'

def fetch(entries):
    inputs = {}
    for entry in entries:
        field = entry[0]
        text = entry[1].get() # User input for each textbox
        if text: # True if field isn't blank
            inputs[field] = float(text)
    if inputs.get('Theta') is not None: # If Theta isn't given, don't convert
        inputs['Theta'] = m.radians(inputs['Theta']) # Use radians internally
    global calcInputs
    calcInputs = inputs
    root.quit()
        


def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=25, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries


    
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
    print("\n")
    for k,v in roundedOut.items():
        print(k,v)
    drawViz(kW, kVAR, kVA)
    
    
    
def from_KW_KVA(kW, kVA):
    Theta = m.acos(kW / kVA)
    kVAR = m.sin(Theta) * kVA
    PF = m.cos(Theta)
    returnResults(kW, kVAR, kVA, PF, Theta)


    
def from_KW_KVAR(kW, kVAR):
    Theta = m.tan(kVAR / kW)
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
    Theta = m.degrees(m.acos(PF))
    kVA = kVAR / m.sin(Theta)
    kW = kVA * PF
    returnResults(kW, kVAR, kVA, PF, Theta)



def from_KVAR_THETA(kVAR, Theta):
    PF = m.cos(Theta)
    kVA = kVAR / m.sin(Theta)
    kW = kVA * PF
    returnResults(kW, kVAR, kVA, PF, Theta)
    
    

def catchInput(PF, Theta):
    gui.alert("Power Factor is cos(theta).\nPlease use other values.")
    root.destroy()
    
    
    
def getInput():
    root.title("Power Triangle Calculator")
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))
    b1 = tk.Button(root, text = 'Calculate', command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    #b2 = tk.Button(root, text='Calculate', command=root.quit)
    #b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text = 'Quit', command=root.destroy)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()

    
    
def drawViz(kW, kVAR, kVA):
    p = [0, 0] # x = 0, y = 0 (real power base)
    q = [kW, 0] # x = kW, y = 0 (real power scalar / reactive power base)
    s = [kW, kVAR] # x = kW, y = kVAR (apparent power top)
    points = [p, q, s]
    #plt.axes()
    polygon = plt.Polygon(points)
    plt.gca().add_patch(polygon)
    plt.axis('scaled')
    plt.annotate('kW', xy=(0.5,-0.1), xycoords='axes fraction')
    plt.annotate('kVAR', xy=(1.05,0.5), xycoords='axes fraction')
    plt.annotate('kVA', xy=(-0.2,0.5), xycoords='axes fraction')
    #drawLegend()
    plt.show()
    
    
'''
# Thanks to Jan Kuiken on Stack Overflow
def drawLegend(axis = None):
    if axis == None:
        axis = plt.gca()

    N = 32
    Nlines = len(axis.lines)

    xmin, xmax = axis.get_xlim()
    ymin, ymax = axis.get_ylim()

    # the 'point of presence' matrix
    pop = np.zeros((Nlines, N, N), dtype=np.float)    

    for l in range(Nlines):
        # get xy data and scale it to the NxN squares
        xy = axis.lines[l].get_xydata()
        xy = (xy - [xmin,ymin]) / ([xmax-xmin, ymax-ymin]) * N
        xy = xy.astype(np.int32)
        # mask stuff outside plot        
        mask = (xy[:,0] >= 0) & (xy[:,0] < N) & (xy[:,1] >= 0) & (xy[:,1] < N)
        xy = xy[mask]
        # add to pop
        for p in xy:
            pop[l][tuple(p)] = 1.0

    # find whitespace, nice place for labels
    ws = 1.0 - (np.sum(pop, axis=0) > 0) * 1.0 
    # don't use the borders
    ws[:,0]   = 0
    ws[:,N-1] = 0
    ws[0,:]   = 0  
    ws[N-1,:] = 0  

    # blur the pop's
    for l in range(Nlines):
        pop[l] = ndimage.gaussian_filter(pop[l], sigma=N/5)

    for l in range(Nlines):
        # positive weights for current line, negative weight for others....
        w = -0.3 * np.ones(Nlines, dtype=np.float)
        w[l] = 0.5

        # calculate a field         
        p = ws + np.sum(w[:, np.newaxis, np.newaxis] * pop, axis=0)
        plt.figure()
        plt.imshow(p, interpolation='nearest')
        plt.title(axis.lines[l].get_label())

        pos = np.argmax(p)  # note, argmax flattens the array first 
        best_x, best_y =  (pos / N, pos % N) 
        x = xmin + (xmax-xmin) * best_x / N       
        y = ymin + (ymax-ymin) * best_y / N       


        axis.text(x, y, axis.lines[l].get_label(), 
                  horizontalalignment='center',
                  verticalalignment='center')
'''    
root = tk.Tk()
gui.alert("Please enter only two values.\nTheta and Power Factor cannot be used together.")
getInput()
#root.mainloop()

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