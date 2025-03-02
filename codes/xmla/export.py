import json
import os

from . import base
from . import orders
from . import product

from ..classes.xmlaxmllib import XmlaXmlLib

def all(param):    
    jsonstr = '{ "products": ['
    count = 0
    
    for file in os.listdir(base.productspath):
        if ".xml" in file:
            xmlfile = XmlaXmlLib.xmlfile(base.productspath + file)
            l = XmlaXmlLib.xml_to_dict(xmlfile, "product")
            
            istyped = "type" in param            
            if istyped:
                param["type"] = product.plural(param["type"])               
            
            inname = istyped and (param["type"] in l["name"])    
                        
            if inname or not istyped:
                if (count != 0):
                    jsonstr += ","
                jsonstr += json.dumps(l)
                count += 1

    preorders = orders.getpreorders(param["preid"])
    
    for l in preorders:
        istyped = "type" in param            
        if istyped:
            param["type"] = product.plural(param["type"])               
        
        inname = istyped and (param["type"] in l["name"])    
                    
        if inname or not istyped:
            if (count != 0):
                jsonstr += ","
            jsonstr += json.dumps(l)
            count += 1

                
    config = XmlaXmlLib.browseconfig(True)
    jsonstr += '], "cart": ' + json.dumps(preorders) + ' ,"preid":"' + param["preid"] + '", "config": ' + json.dumps(config) + '}'
    return jsonstr

def alldict(param):
    ps = []
    
    for file in os.listdir(base.productspath):
        if ".xml" in file:
            xmlfile = XmlaXmlLib.xmlfile(base.productspath + file)
            l = XmlaXmlLib.xml_to_dict(xmlfile, "product")
            
            istyped = "type" in param            
            if istyped:
                param["type"] = product.plural(param["type"])               
            
            inname = istyped and (param["type"] in l["name"])    
                        
            if inname or not istyped:
                ps.append(l)
                
    return ps
    
def xmlrss():
     xmlstr = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE products><products>'
     for file in os.listdir(base.productspath):
         with open(base.productspath + file, "r") as f:
             xmlfile = f.read()
             xmlstr += xmlfile
     xmlstr += '</products>'
     return xmlstr
