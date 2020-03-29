from flask import Flask
from flask_restful import Api
from src.controller.application_data import application_data
from src.controller.main_data import main_data
from src.controller.covid_data import covid_data
# import py_eureka_client.eureka_client as eureka_client


app = Flask(__name__)
app.register_blueprint(application_data)
app.register_blueprint(main_data)
app.register_blueprint(covid_data)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)


# your_rest_server_port = 5001
# eureka_client.init(eureka_server="http://insight-discovery-service:8761/eureka/",
#                                 app_name="insight-gsheet-reader-service",
#                                 instance_port=your_rest_server_port,
#                                 instance_id ="insight-gsheet-reader-service:5001")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001, debug=True)
