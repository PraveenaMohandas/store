from flask import Blueprint

store = Blueprint('store-api', __name__, url_prefix='/api/v1/store/')

@store.route('test', methods=['GET','POST'])
def test():
    return "success"