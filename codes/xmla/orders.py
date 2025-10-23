import os.path
import os
import shutil
import random

from . import base

from ..classes.xmlaxmllib import XmlaXmlLib
from ..xmla import users

def do(opts):
    if 'orderid' in opts:
        return decline(opts["userid"], opts["orderid"], opts["preorderid"])
    elif 'repre' in opts:
        return predecline(opts["id"], opts["preorderid"])
    elif 'pre' in opts:
        return premake(opts["id"], opts["preorderid"])
    else:
        return make(opts["ids"], opts["userid"], opts["preorderid"])

def getpreorders(preid):
    products = []
    for dir in os.listdir(base.preorderspath):
        predir = base.preorderspath + dir
        if os.path.isdir(predir) and dir == preid:
            for file in os.listdir(predir):
                if ".xml" in file:        
                    temppreorderfile = base.preorderspath + "/" + dir + "/" + file 
                    xmlfile = XmlaXmlLib.xmlfile(temppreorderfile)            
                    p = XmlaXmlLib.xml_to_dict(xmlfile, "product")
                    products.append(p)
    return products 

def make(ids, userId, preorderid):
    opts = {}
    opts["userid"] = userId
    opts["preorderid"] = preorderid
    products = ids.split("-")
    opts["orderid"] = str(random.sample(range(100000, 999999), 1)[0])
    full = True
    for product in products:
        full = full and orderProduct(product, opts)
    if (full):
        return opts["orderid"]
    else:
        return False
    
def premake(id, preorderid):
    opts = {}
    opts["preorderid"] = preorderid
    return preOrderProduct(id, opts)
    
def decline(userId, orderId, preorderid):
    user = users.getuser_by_id(userId)

    opts = {}
    opts["userid"] = userId
    opts["orderid"] = orderId
    opts["preorderid"] = preorderid
    opts["products"] = []
    pathorder = base.orderspath + user["email"] + "/" + str(opts["orderid"]) + "/"
    for file in os.listdir(pathorder):
        opts["products"].append(os.path.basename(file))
    cancelOrder(opts)
    return opts["orderid"]

def predecline(id, preorderId):
    opts = {}
    opts["preorderid"] = preorderId
    opts["product"] = id
    cancelPreOrder(opts)
    return opts["preorderid"]

def orderProduct(id, opts):
    file = id + ".xml"
    if (os.path.isfile(base.preorderspath + opts["preorderid"] + "/" + file)):
        moveToOrder(file, opts)
        return True
    else:
        return False
    
def preOrderProduct(id, opts):
    file = id + ".xml"
    if (os.path.isfile(base.productspath + file)):
        return moveToPreOrder(file, opts)
    else:
        return False

def cancelOrder(opts):
    user = users.getuser_by_id(opts["userid"])
    pathorder = base.orderspath + user["email"] + "/" + str(opts["orderid"]) + "/"

    for file in opts["products"]:
        if os.path.isfile(pathorder + file):
            moveBack(pathorder, file, opts["preorderid"])

def cancelPreOrder(opts):
    pathpreorder = base.preorderspath + str(opts["preorderid"]) + "/" 
    file = opts["product"] + ".xml"
    if os.path.isfile(pathpreorder + file):
        preMoveBack(pathpreorder, file)
    return opts["preorderid"]

def cancelPreOrderPreId(preid):
    for dir in os.listdir(base.preorderspath):
        predir = base.preorderspath + dir
        if os.path.isdir(predir) and dir == preid:
            for file in os.listdir(predir):
                if ".xml" in file:        
                    temppreorderfile = base.preorderspath + "/" + dir + "/" + file 
                    xmlfile = XmlaXmlLib.xmlfile(temppreorderfile)            
                    p = XmlaXmlLib.xml_to_dict(xmlfile, "product")

                    opts = {}
                    opts["preorderid"] = preid
                    opts["product"] = p["id"]

                    cancelPreOrder(opts)

def moveToOrder(file, opts):
    user = users.getuser_by_id(opts["userid"])

    pathuser = base.orderspath + user["email"] + "/"
    pathorder = base.orderspath + user["email"]+ "/" + str(opts["orderid"]) + "/"

    if (os.path.isdir(pathuser)):
        if (os.path.isdir(pathorder)):
            moveToOrderOs(file, pathorder, opts["preorderid"])
        else:
            os.mkdir(pathorder)
            moveToOrderOs(file, pathorder, opts["preorderid"])
    else:
        os.mkdir(pathuser)
        os.mkdir(pathorder)
        moveToOrderOs(file, pathorder, opts["preorderid"])

def moveToPreOrder(file, opts):
    pathpreuser = base.preorderspath + str(opts["preorderid"]) + "/"

    if (os.path.isdir(pathpreuser)):
        moveToPreOrderOs(file, pathpreuser)
    else:
        os.mkdir(pathpreuser)
        moveToPreOrderOs(file, pathpreuser)
    return opts["preorderid"]

def moveToPreOrderOs(file, pathpreorder):
    shutil.move(base.productspath + file, pathpreorder + file)

def moveToOrderOs(file, pathorder, preorderid):
    shutil.move(base.preorderspath + preorderid + "/" + file, pathorder + file)
    
    pathpreorder = base.preorderspath + preorderid + "/"
    if len(os.listdir(pathpreorder)) == 0:
        shutil.rmtree(pathpreorder)

def moveBack(pathorder, file, preorderid):
    pathproduct = base.preorderspath + preorderid + "/"  + file
    pathorder = pathorder + file

    pathpreorder = base.preorderspath + preorderid
    if not os.path.isdir(pathpreorder):
        os.mkdir(pathpreorder)

    shutil.move(pathorder, pathproduct)

def preMoveBack(pathpreorder, file):
    pathproduct = base.productspath + file
    pathpreorderfile = pathpreorder + file
    shutil.move(pathpreorderfile, pathproduct)    

    if len(os.listdir(pathpreorder)) == 0:
        shutil.rmtree(pathpreorder)




    
