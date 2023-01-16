from flask import request
from common.responses import response


def middleware(app):
    @app.before_request
    def process_request():
        try:
            # request.endpoint,request.url,request.path
            api = ((request.path).split('?')[0]).split('/')
            print(api)

            if 'store' in api:
                pass
            else:
                return response('create', 'unauthorized', {})
        except Exception as e:
            print(e)
            return response('create', 'unauthorized', {}, str(e))
