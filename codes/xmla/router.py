from bottle import redirect, route, view, post, request, get, response, auth_basic
from bottle import static_file

import os
import zipfile
import shutil

from . import export
from . import orders
from . import imps
from . import users
from . import base
from . import seo


@route('/catalog/')
@view('catalog')
def catalog(name='World'):
    vals = seo.getseo()
    vals["showProduct"] = False
    vals["setFilters"] = False
    return vals
    
@route('/catalog/filter/<filters>')
@view('catalog')
def catalog(filters):
    vals = seo.getseo()
    vals["showProduct"] = False
    vals["setFilters"] = filters
    return vals

@route('/catalog/details/<xml>')
@view('catalog')
def catalog_details(xml):
    vals = seo.getseo()
    vals["showProduct"] = xml
    vals["setFilters"] = False
    return vals

@post('/catalog/out/')
def catalog_out():
    param = {}
    if (request.forms.get('type')):
        param["type"] = request.forms.get('type')
    for key, value in request.forms.allitems():
        param[key] = value
    tu = users.checktempusers(param)
    param["preid"] = tu["preid"]    
    return export.all(param)
    
@get('/catalog/rss/')
def catalog_rss():    
    response.set_header('Content-type', 'application/x-nfo')
    response.set_header('Content-Disposition', 'attachment; filename="rss.xml"')
    return export.xmlrss()

@post('/user/in/')
def user_in():
    u = {}
    for key, value in request.forms.allitems():
        u[key] = value
    user = users.createuser(u)
    return '{"id": ' + str(user["id"]) + '}'

@post('/catalog/in/')
def catalog_in():
    if (request.forms.get('file')):
        return imps.imp(request.forms.get('file'))
    elif(request.forms.get('filerun')):
        l = imps.imprun(request.forms.allitems())
        return '{"finished": ' + str(l).lower() + '}'
    elif(request.forms.get('clear')):
        shutil.rmtree(base.importpathimgs)
        os.remove(base.importpathxml)
        return '{"status": "ok"}'

# @post('/catalog/order/')
# def catalog_order():
#     opts = {}
#     for key, value in request.forms.allitems():
#         opts[key] = value
#     return '{"status": "ok", "orderId": ' + str(orders.make(opts["ids"], opts["userid"])).lower() + '}'

@post('/catalog/preorder/')
def catalog_order():
    opts = {}
    for key, value in request.forms.allitems():
        opts[key] = value    
    if (str(orders.do(opts)) == opts["preorderid"]):
        return '{"status": "ok"}'
    else:
        return '{"status": "error" }'

@post('/catalog/order/')
def catalog_order():
    opts = {}
    for key, value in request.forms.allitems():
        opts[key] = value
    return '{"status": "ok", "orderId": ' + str(orders.do(opts)).lower() + '}'


@route('/catalog/in/')
@view('imports')
def imports():
    vars = {}
    vars["hasimgs"] = os.path.exists(base.importpathimgs)
    vars["hasxml"] = os.path.exists(base.importpathxml)
    return vars


@route('/upload', method='POST')
def do_upload():
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.xml'):
        return 'File extension not allowed.'

    save_path = base.importpathxml
    upload.save(save_path) # appends upload.filename automatically
    redirect("/catalog/in/")

@route('/uploadzip', method='POST')
def do_uploadzip():
    upload     = request.files.get('uploadzip')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.zip'):
        return 'File extension not allowed.'

    save_path = base.importpathzip
    upload.save(save_path) # appends upload.filename automatically
    with zipfile.ZipFile(base.importpathzip,"r") as zip_ref:
        zip_ref.extractall(base.importpathimgs)
    os.remove(base.importpathzip)

    redirect("/catalog/in/")


# ...

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')
