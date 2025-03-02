import random
import os
import datetime

from bottle import request

from time import gmtime, strftime
 

from . import base
from . import orders

from ..classes.xmlaxmllib import XmlaXmlLib

def createuser(user):
    u = {}
    u["email"] = user["email"]
    u["id"] = random.randint(1000000, 9999999)
    userxmlstr = XmlaXmlLib.object_to_xmlstr(u, "user")
    XmlaXmlLib.writefile(base.userspath + str(u["id"]) + ".xml", userxmlstr)
    return u

def tempuser(preid):
    u = {}
    u["preid"] = preid
    u["time"] = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    u["ip"] = request.remote_addr

    userxmlstr = XmlaXmlLib.object_to_xmlstr(u, "tempuser")
    XmlaXmlLib.writefile(base.tempuserspath + str(u["preid"]) + ".xml", userxmlstr)
    return u

def checkip(ip , preid):
    for file in os.listdir(base.tempuserspath):
        if ".xml" in file:            
            tempufile = base.tempuserspath + file 
            xmlfile = XmlaXmlLib.xmlfile(tempufile)            
            tu = XmlaXmlLib.xml_to_dict(xmlfile, "tempuser")

            if tu["ip"] == ip:
                return tu
            
    return tempuser(preid)
            

def checktempusers(param):
    for file in os.listdir(base.tempuserspath):
        if ".xml" in file:            
            tempufile = base.tempuserspath + file 
            xmlfile = XmlaXmlLib.xmlfile(tempufile)            
            u = XmlaXmlLib.xml_to_dict(xmlfile, "tempuser")
            
            dtime = datetime.datetime.strptime(u["time"], "%Y-%m-%d  %H:%M:%S")
            deltatime = (datetime.datetime.now() - dtime).total_seconds()
            minutes = round(deltatime / (60))

            if minutes > 15:
                os.remove(tempufile)
                orders.cancelPreOrderPreId(u["preid"])

    
    return checkip(request.remote_addr, param["preid"])
        



def getuser(email):    
    for file in os.listdir(base.userspath):
        if ".xml" in file:            
            xmlfile = XmlaXmlLib.xmlfile(base.userspath + file)            
            u = XmlaXmlLib.xml_to_dict(xmlfile, "user")
            if u["email"] == email:
                return u 
    return False           
