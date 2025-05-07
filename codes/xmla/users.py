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
    user = getuser(user["email"])    
    if user:
        return user
    
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

def checkip(ip, preid):
    tempusers = XmlaXmlLib.getFiles("tempuser", [])
    for tu in tempusers:
        if tu["ip"] == ip:
            return tu
            
    return tempuser(preid)
            

def checktempusers(param):
    tempusers = XmlaXmlLib.getFiles("tempuser", [])
    for tu in tempusers:            
        dtime = datetime.datetime.strptime(tu["time"], "%Y-%m-%d  %H:%M:%S")
        deltatime = (datetime.datetime.now() - dtime).total_seconds()
        minutes = round(deltatime / (60))

        if minutes > 15:
            XmlaXmlLib.removeById("tempuser", tu)
            orders.cancelPreOrderPreId(tu["preid"])
    
    return checkip(request.remote_addr, param["preid"])      


def getuser(email):
    param = {}
    param["email"] = email
    users = XmlaXmlLib.getFiles("user", param)    

    if len(users) > 0:
        return users[0]

    return False           
