import json
import shutil
import zipfile

from . import product
from . import base

from ..classes.xmlaxmllib import XmlaXmlLib

####################################### PRE IMPORT ########################################

def imp(file):
    xmlfile = XmlaXmlLib.xmlfile(file)
    l = XmlaXmlLib.browsefields(xmlfile, "product")
    m = XmlaXmlLib.browseconfig()
    return '{"fields-file": ' + json.dumps(l) + ', "fields-config": ' + json.dumps(m) + '}'


####################################### IMPORT #######################################3

def imprun(formitems):
    setting = {}
    for key, value in formitems:
        setting[key] = value
    file = setting['filerun']
    xmlfile = XmlaXmlLib.xmlfile(file)
    objs = XmlaXmlLib.xml_to_dict(xmlfile, "product")
    if len(setting) > 1:
        objs = product.fieldsofsetting(objs, setting)
    for p in objs:
        picstr = ""
        countpics = int(p["pics"])
        for i in range(0, countpics):
            numstr = "." + str((i + 1))
            separator = "|"
            if (i == countpics - 1):
                separator = ""
            if (i == 0):
                numstr = "" 
            picstr += base.imagespath + str(p["id"]) + numstr + ".png" + separator

        p["pic"] = picstr
        p["page"] = "/catalog/details/" + str(p["id"]) + ".xml"
        
        file = base.productspath + p["id"] + ".xml"

        xmlstr = XmlaXmlLib.object_to_xmlstr(p, "product")
        XmlaXmlLib.writefile(file, xmlstr)
        copyimgs(p, p["pics"])
    return True

def copyimgs(product, num):
    istr = ""
    for i in range(1, int(num) + 1 ):
        if i != 1:
            istr = "." + str(i)
        else:
            istr = ""
        shutil.copyfile(f'./imports/pics/{product["id"]}{istr}.png', f'./static/pics/{product["id"]}{istr}.png')

def testimport():    
    for path in base.testfilespaths:
        xml = path + "in.xml"
        zip = path + "pics.zip"

        with zipfile.ZipFile(zip, "r") as zip_ref:
            zip_ref.extractall(base.importpathimgs)

        xmlfile = XmlaXmlLib.xmlfile(xml)
        objs = XmlaXmlLib.xml_to_dict(xmlfile, "product")
        
        for p in objs:
            picstr = ""
            countpics = int(p["pics"])
            for i in range(0, countpics):
                numstr = "." + str((i + 1))
                separator = "|"
                if (i == countpics - 1):
                    separator = ""
                if (i == 0):
                    numstr = "" 
                picstr += base.imagespath + str(p["id"]) + numstr + ".png" + separator

            p["pic"] = picstr
            p["page"] = "/catalog/details/" + str(p["id"]) + ".xml"
            
            file = base.productspath + p["id"] + ".xml"

            xmlstr = XmlaXmlLib.object_to_xmlstr(p, "product")
            XmlaXmlLib.writefile(file, xmlstr)
            copyimgs(p, p["pics"])
