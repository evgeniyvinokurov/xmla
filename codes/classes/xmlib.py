import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Union

class XmlLib:

    @staticmethod
    def xmlfile(file):
        with open(file, mode="r", encoding="utf-8") as f:
            root = ET.fromstring(f.read())
            return root


    # xml files works #

    @staticmethod
    def xmlout(xmlstr):
        prettyxmlstr = minidom.parseString(xmlstr).toprettyxml(indent="   ")
        return prettyxmlstr

    @staticmethod
    def writefile(file, xml):
        xmlstr = XmlLib.xmlout(xml)
        with open(file, mode="w", encoding="utf-8") as f:
            f.write(xmlstr)

    #  one level xml file conversions #

    @staticmethod
    def object_to_xmlstr(data: Union[dict, bool], root='object'):
        xml = f'<{root}>'
        if isinstance(data, dict):
            for key, value in data.items():
                xml += XmlLib.object_to_xmlstr(value, key)
        elif isinstance(data, (list, tuple, set)):
            for item in data:
                xml += XmlLib.object_to_xmlstr(item, 'item')
        else:
            xml += str(data)

        xml += f'</{root}>'
        return xml

    @staticmethod
    def xml_to_dict(child, tag):
        objs = []
        if (child.tag == tag):
            return XmlLib.treevalues(child)
        else:
            for chi in child:
                objs.append(XmlLib.xml_to_dict(chi, tag))
        return objs

    @staticmethod
    def treevalues(child):
        o = {}
        for chi in child:
            o[chi.tag] = XmlLib.pretext(chi.text)
        return o

    @staticmethod
    def pretext(text):
        return text.replace("\n","").strip()
