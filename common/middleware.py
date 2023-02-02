from flask import request
from common.responses import response

import logging
from logging.handlers import TimedRotatingFileHandler
logger = logging.getLogger('flask_logger')
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler('app.log', when='D', interval=1, backupCount=7)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
# format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def middleware(app):
    @app.before_request
    def process_request():
        try:
            # request.endpoint,request.url,request.path
            api = ((request.path).split('?')[0]).split('/')
            print(api)
            logger.debug(f'Request: {request}')
            if 'store' in api:
                pass
            else:
                return response('create', 'unauthorized', {})
        except Exception as e:
            print(e)
            return response('create', 'unauthorized', {}, str(e))
    
    @app.after_request
    def logging_process(response):
        # import logging
        # logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
        # return response('retrieve','success',"Logged")

        logger.debug(f'Response: {response}')
        return response