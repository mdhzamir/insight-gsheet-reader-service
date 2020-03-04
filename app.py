from flask import Flask
from flask_restful import Api
from src.controller.application_data import application_data
from src.controller.main_data import main_data


app = Flask(__name__)
app.register_blueprint(application_data)
app.register_blueprint(main_data)
api = Api(app)




if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)