import xml.etree.ElementTree as ET
import os


from ..xmla import product
from ..xmla import base

from ..classes.xmlib import XmlLib



#  Xmla shop xml files works

class XmlaXmlLib(XmlLib):

    # Multi level xml files
    @staticmethod
    def browsefields(child, tag):
        if (child.tag == tag):
            return XmlaXmlLib.treefields(child)
        else:
            for chi in child:
                b = XmlaXmlLib.browsefields(chi, tag)
                if (b):
                    return b
        return False

    # Tree of one level tags
    @staticmethod
    def treefields(child):
        fields = []
        for chi in child:
            fields.append(chi.tag)
        return fields

    # Works with shop's config 
    @staticmethod
    def browseconfig(attrib = False):
        tree = ET.parse(base.configcatalogpath)
        root = tree.getroot()
        fields = []
        attribs = {}
        for chi in root:
            if (chi.attrib and ("client-path" in chi.attrib)):
                if attrib:
                    attribs[chi.attrib["client-path"]] = chi.text
                else:
                    fields.append(chi.text)
            if (chi.attrib and ("setup" in chi.attrib)):
                if attrib:
                    attribs[chi.attrib["setup"]] = chi.text
        if attrib:
            return attribs
        return fields
    
    # Get catalog config
    @staticmethod
    def getconfig():    
        configfile = XmlLib.xmlfile(base.configcatalogpath)    
        catalog = XmlLib.xml_to_dict(configfile, "catalog")
        return catalog
    
    # Removing xml file by filter param
    @staticmethod
    def removeById(type, filter):
        if type == "tempuser":
            os.remove(base.tempuserspath + filter["preid"] + ".xml")
    
    # Getting xml file by type and filter param
    @staticmethod
    def getFiles(type, filter):
        result = []
        
        if type == "product":
            for file in os.listdir(base.productspath):
                if ".xml" in file:
                    xmlfile = XmlaXmlLib.xmlfile(base.productspath + file)
                    p = XmlaXmlLib.xml_to_dict(xmlfile, "product")
                    istyped = "type" in filter            
                    if istyped:
                        filter["type"] = product.plural(filter["type"])                    
                    inname = istyped and (filter["type"] in p["name"])                               
                    if inname or not istyped:
                        result.append(p)        

        elif type == "preorder":
            for dir in os.listdir(base.preorderspath):
                predir = base.preorderspath + dir
                if os.path.isdir(predir) and dir == filter["preid"]:
                    for file in os.listdir(predir):
                        if ".xml" in file:        
                            temppreorderfile = base.preorderspath + "/" + dir + "/" + file 
                            xmlfile = XmlaXmlLib.xmlfile(temppreorderfile)            
                            p = XmlaXmlLib.xml_to_dict(xmlfile, "product")
                            result.append(p)

        elif type == "tempuser":
            for file in os.listdir(base.tempuserspath):
                if ".xml" in file:            
                    tempufile = base.tempuserspath + file 
                    xmlfile = XmlaXmlLib.xmlfile(tempufile)            
                    u = XmlaXmlLib.xml_to_dict(xmlfile, "tempuser")

                    result.append(u)
        
        elif type == "user":
            for file in os.listdir(base.userspath):
                if ".xml" in file:            
                    xmlfile = XmlaXmlLib.xmlfile(base.userspath + file)            
                    u = XmlaXmlLib.xml_to_dict(xmlfile, "user")

                    if "email" in filter:
                        if filter["email"] == u["email"]:
                            result.append(u)
                    else:
                        result.append(u)

        return result