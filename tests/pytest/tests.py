import sys
import os
import random
import json
import numpy as n

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
parentmore = os.path.dirname(parent)
 
# adding the parent directory to 
# the sys.path.
sys.path.append(parentmore)



from codes.xmla import users
from codes.xmla import orders
from codes.xmla import tools
from codes.xmla import export
from codes.xmla import base
from codes.xmla import product

from codes.classes.xmlaxmllib import XmlaXmlLib

class TestClassXmla:
    def test_userCreation(self):
        # crating user        
        params = {}
        params["email"] = tools.randomletters() + "@testemail.com"
        users.createuser(params)
        
        # getting user
        newuser = users.getuser(params["email"])
        assert newuser != False

    def test_gettingProductsByTypeJson(self):
        param = {}
        param["preid"] = '1312'
        param["type"] = random.choice(["Ручки", "Кружки", "Все"])

        # load json
        jsondata = export.all(param)
        data = json.loads(jsondata)["products"]
        
        allType = True
        for p in data:
            allType = allType and product.plural(param["type"]) in p["name"]

        assert allType != False

    def test_gettingProductsByType(self):
        param = {}
        param["type"] = random.choice(["Ручки", "Кружки", ""])

        # load dict
        data = export.alldict(param)

        allType = True
        for p in data:
            allType = allType and product.plural(param["type"]) in p["name"]
        
        assert allType != False
        
    def test_ordersMake(self):
        # creating user
        params = {}
        params["email"] = tools.randomletters() + "@testemail.com"
        u = users.createuser(params)

        # getting products
        param = {}
        param["type"] = ""
        ps = export.alldict(param)

        # making products ids string
        ids = ""
        idsarray = []
        for r in range(0, random.randrange(1,5)):
            p = random.choice(ps)
            if r == 0:
                ids += str(p["id"])
            else:    
                ids += "-" + str(p["id"])
            idsarray.append(str(p["id"]))
        
        # making order
        preid = "1241234"
        for id in idsarray:
            orders.premake(id, preid)

        orderid = orders.make(ids, u["id"], preid)
        allExist = True
        for id in idsarray:
            file = base.orderspath + u["email"] + "/" + str(orderid)+ "/" + id + ".xml"
            allExist = allExist and os.path.isfile(file)

        assert allExist != False   

    def test_preOrdersMake(self):
        # creating user
        params = {}
        params["email"] = tools.randomletters() + "@testemail.com"
        u = users.createuser(params)

        # getting products
        param = {}
        param["type"] = ""
        ps = export.alldict(param)

        # making products ids string
        ids = ""
        idsarray = []
        for r in range(0, random.randrange(1,5)):
            p = random.choice(ps)
            if r == 0:
                ids += str(p["id"])
            else:    
                ids += "-" + str(p["id"])
            idsarray.append(str(p["id"]))
        
        # making order
        preid = "1241234"
        for id in idsarray:
            orders.premake(id, preid)

        allExist = True
        for id in idsarray:
            file = base.preorderspath + preid + "/" + id + ".xml"
            allExist = allExist and os.path.isfile(file)

        assert allExist != False

    def test_ordersDecline(self):
        # creating user
        params = {}
        params["email"] = tools.randomletters() + "@testemail.com"
        u = users.createuser(params)

        # getting products
        param = {}
        param["type"] = ""
        ps = export.alldict(param)

        # making products ids string
        ids = ""
        idsarray = []
        for r in range(0, random.randrange(1,5)):
            p = random.choice(ps)
            if r == 0:
                ids += str(p["id"])
            else:    
                ids += "-" + str(p["id"])
            idsarray.append(str(p["id"]))

        preid = "2432523"
        for id in idsarray:
            orders.premake(id, preid)
        
        # making order
        orderid = orders.make(ids, u["id"], preid)
        
        #  declining order 
        orders.decline(u["id"], orderid, preid)
        allNotExist = True
        for id in idsarray:
            file = base.orderspath + u["email"] + "/" + str(orderid)+ "/" + id + ".xml"
            allNotExist = allNotExist and not os.path.isfile(file)


        assert allNotExist != False

    def test_preOrdersDecline(self):
        # creating user
        params = {}
        params["email"] = tools.randomletters() + "@testemail.com"
        u = users.createuser(params)

        # getting products
        param = {}
        param["type"] = ""
        ps = export.alldict(param)

        # making products ids string
        ids = ""
        idsarray = []
        for r in range(0, random.randrange(1,5)):
            p = random.choice(ps)
            if r == 0:
                ids += str(p["id"])
            else:    
                ids += "-" + str(p["id"])
            idsarray.append(str(p["id"]))

        preid = "2432523"
        for id in idsarray:
            orders.premake(id, preid)

        for id in idsarray:
            orders.predecline(id, preid)
        
        #  declining order 
        allNotExist = True
        for id in idsarray:
            file = base.preorderspath + preid + "/" + id + ".xml"
            allNotExist = allNotExist and not os.path.isfile(file)


        assert allNotExist != False
    
    def test_ordersMakeAndDecline(self):
        # creating user
        params = {}
        params["email"] = tools.randomletters() + "@testemail.com"
        u = users.createuser(params)

        # getting products
        param = {}
        param["type"] = ""
        ps = export.alldict(param)

        # making products ids string
        ids = ""
        idsarray = []
        for r in range(0, random.randrange(1,5)):
            p = random.choice(ps)
            if r == 0:
                ids += str(p["id"])
            else:    
                ids += "-" + str(p["id"])
            idsarray.append(str(p["id"]))

        preid = "4324213"
        for id in idsarray:
            orders.premake(id, preid)
        
        # making order
        orderid = orders.make(ids, u["id"], preid)
        allExist = True
        for id in idsarray:
            file = base.orderspath + u["email"] + "/" + str(orderid)+ "/" + id + ".xml"
            allExist = allExist and os.path.isfile(file)
        
        #  declining order 
        orders.decline(u["id"], orderid, preid)
        allNotExist = True
        for id in idsarray:
            file = base.orderspath + u["email"] + "/" + str(orderid) + "/" + id + ".xml"
            allNotExist = allNotExist and not os.path.isfile(file)


        assert allExist and allNotExist != False
    
    def test_allInExport(self):
        param = {}
        param["type"] = ""
        param["preid"] = "1313314"

        # load dict
        data = json.loads(export.all(param))["products"]

        ids = []
        for p in data:
            ids.append(p["id"])

        fileids = []
        for file in os.listdir(base.productspath):
            if ".xml" in file:
                xmlfile = XmlaXmlLib.xmlfile(base.productspath + file)
                l = XmlaXmlLib.xml_to_dict(xmlfile, "product")
                fileids.append(l["id"])
        

        narr1 = n.array([ids])
        narr2 = n.array([fileids])

        assert (set(ids) == set(fileids)) != False
