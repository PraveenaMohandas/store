from settings.build_app import create_app

app = create_app()
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app,db)

# UPLOAD_FOLDER = '/home/divum/Documents'

# app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)

