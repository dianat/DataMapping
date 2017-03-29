# -*- coding: utf-8 -*-
import re

def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'W' or direction == 'S':
        dd *= -1
    return dd;

def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def wgs84(dms):
    # input preprocessing
    # convert 43° 57′ 0″ N into 43°57'0"N
    dms = dms.replace(' ','').replace('′','\'').replace('″','\"')
    dms = re.split('[°\'" ]+', dms)
    return dms2dd(dms[0], dms[1], dms[2], dms[3])
