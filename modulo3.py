#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 11:37:05 2022

@author: marcio
"""
import numpy as np
spd = {"s [column 3]":2, "s(up) [column 4]":3, "s(down) [column 5]":4,
"px [column 3]":2, "py [column 4]":3, "pz [column 5]":4,"px(up) [column 4]":3,
"px(down) [column 5]":4, "py(up) [column 6]":5,"py(down) [column 7]":6,
"pz(up) [column 8]":7, "pz(down) [column 9]":8,"dz2 [column 4]":3,
"dxz [column 5]":4, "dyz [column 6]":5,"dxy [column 7]":6, "dx2-y2 [column 8]":7,
"dz2(up) [column 4]":3, "dz2(down) [column 5]":4, "dxz(up) [column 6]":5,
"dxz(down) [column 7]":6, "dyz(up) [column 8]":7,"dyz(down) [column 9]":8,
"dxy(up) [column 10]":9,"dxy(down) [column 11]":10, "dx2-y2(up) [column 12]":11,
"dx2-y2(down) [column 13]":12, "fz3(up) [column 3]":2,"fz3(down) [column 4]":3,
"fxz2(up) [column 5]":4, "fxz2(down) [column 6]":5,"fyz2(up) [column 7]":6,
"fyz2(down) [column 8]":7, "fxyz(up) [column 9]":8,"fxyz(down) [column 10]":9,
"fz(up) [column 11]":10, "fz(down) [column 12]":11,"fx(up) [column 13]":12,
"fx(down) [column 14]":13, "fy(up) [column 15]":14,"fy(down) [column 16]":15,
"fz3 [column 3]":2, "fxz2 [column 4]":3,"fyz2 [column 5]":4, "fxyz [column 6]":5,
"fz [column 7]":6, "fx [column 8]":7, "fy [column 9]":8}

#------------------- função que retorna o dos ---------------------------------
def DOS(file, serie):
    files = file.split(';')
    dos = []
    for i in files:
        if i != '':
            data = np.loadtxt(i,unpack=True)
            eV = data[0]
            dos.append(data[1])
    soma = (sum(dos))
    if serie == '+':
        return eV, soma
    elif serie == '-':
        return eV, soma*-1
#--------------------- função que retorna o intdos ----------------------------
def intDOS(file, serie):
    files = file.split(';')
    intdos = []
    for i in files:
        if i != '':
            data = np.loadtxt(i,unpack=True)
            eV = data[0]
            intdos.append(data[2])
    soma = (sum(intdos))
    if serie == '+':
        return eV, soma
    elif serie == '-':
        return eV, soma*-1
#--------------------- função que retorna o pdos ----------------------------
def PDOS(file, serie, orbital):
    files = file.split(';')
    pdos = []
    try:
        for i in files:
            if i != '':
                data = np.loadtxt(i,unpack=True)
                eV = data[0]
                pdos.append(data[spd[orbital]])
        soma = np.sum(pdos,axis=0)
        if serie == '+':
            return eV, soma
        elif serie == '-':
            return eV, soma*-1
    except:
        return None
#--------------------- função que retorna o pdos ----------------------------
def LDOS(file, serie):
    files = file.split(';')
    ldos = []
    for i in files:
        if i != '':
            data = np.loadtxt(i,unpack=True)
            eV = data[0]
            ldos.append(data[1])
    soma = np.sum(ldos,axis=0)
    if serie == '+':
        return eV, soma
    elif serie == '-':
        return eV, soma*-1
#--------------------- função que retorna o ldosup ----------------------------
def LDOSUP(file, serie):
    files = file.split(';')
    ldosup = []
    for i in files:
        if i != '':
            data = np.loadtxt(i,unpack=True)
            eV = data[0]
            ldosup.append(data[1])
    soma = np.sum(ldosup,axis=0)
    if serie == '+':
        return eV, soma
    elif serie == '-':
        return eV, soma*-1
#--------------------- função que retorna o ldosdw ----------------------------
def LDOSDW(file, serie):
    files = file.split(';')
    ldosdw = []
    for i in files:
        if i != '':
            data = np.loadtxt(i,unpack=True)
            eV = data[0]
            ldosdw.append(data[2])
    soma = np.sum(ldosdw,axis=0)
    if serie == '+':
        return eV, soma
    elif serie == '-':
        return eV, soma*-1
def Resp(a,b,c,d): # a = files; b = séries; c = tipo de cálculo; d = orbitais
    if c == 'DOS':
        return DOS(a, b)
    if c == 'intDOS':
        return intDOS(a, b)
    elif c == 'DOSUP':
        return DOS(a, b)
    elif c == 'DOSDW':
        return DOS(a, b)
    elif c == 'lDOS':
        return LDOS(a, b)
    elif c == 'lDOSUP':
        return LDOSUP(a, b)
    elif c == 'lDOSDW':
        return LDOSDW(a, b)
    elif c == 'pDOS':
        return PDOS(a, b, d)
