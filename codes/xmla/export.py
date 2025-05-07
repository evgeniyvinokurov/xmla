import json
import os

from . import base
from . import orders
from . import product

from ..classes.xmlaxmllib import XmlaXmlLib

def all(param):    
    products = XmlaXmlLib.getFiles("product", param)
    preorders = XmlaXmlLib.getFiles("preorder", param)
                
    config = XmlaXmlLib.browseconfig(True)
    jsonstr = '{ "products": ' + json.dumps(products) + ', "cart": ' + json.dumps(preorders) + ' ,"preid":"' + param["preid"] + '", "config": ' + json.dumps(config) + '}'

    return jsonstr

def alldict(param):
    ps = XmlaXmlLib.getFiles("product", param)                
    return ps
    
def xmlrss():
    products = XmlaXmlLib.getFiles("product", [])
    xmlstr = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE products><products>'
    for p in products:        
        xmlfile = XmlaXmlLib.xmlout(XmlaXmlLib.object_to_xmlstr(p, "product"))
        xmlstr += xmlfile
    xmlstr += '</products>'
    return xmlstr
