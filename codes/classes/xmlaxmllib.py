import xml.etree.ElementTree as ET

from ..xmla import base
from ..classes.xmlib import XmlLib

class XmlaXmlLib(XmlLib):
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

    @staticmethod
    def treefields(child):
        fields = []
        for chi in child:
            fields.append(chi.tag)
        return fields

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
    
    @staticmethod
    def getconfig():    
        configfile = XmlLib.xmlfile(base.configcatalogpath)    
        catalog = XmlLib.xml_to_dict(configfile, "catalog")
        return catalog