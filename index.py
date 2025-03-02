from bottle import default_app, run

import codes.xmla.router

application = default_app()
application.run()

#for docker
# run(host='0.0.0.0', port=8000, debug=True, reloader=True)