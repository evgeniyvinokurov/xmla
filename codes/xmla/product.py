def fieldsofsetting(objs, setting):
    newobjs = []
    for o in objs:
        newo = {}
        for k,v in o.items():
            if k in setting:
                newo[setting[k]] = v
        newobjs.append(newo)
    return newobjs

def plural(param):
    return param.replace("ки", "ка")
