from flask import request,jsonify,Blueprint,current_app
from src.utility.utilities import *

# Initialize Blueprint
application_data = Blueprint('application_data',__name__, url_prefix='/api/application')


@application_data.before_app_request
def log_msg_before_request():
    current_app.logger.info('REQUEST----------------------')
    current_app.logger.info('Body: %s', request.get_json())



@application_data.route("/get-district-wise-total-application", methods=['POST'])
def get_district_wise_total_application():

    # Parse Request Body
    _request_data = request.get_json();
    _limit = _request_data['noOfRow']
    _tab_name = _request_data['tabName']
    _group_by_column = _request_data['groupByColumn']
    _column = _request_data['column']
    _url = _request_data['url']
    _file_path = '/home/shakib/Development/dataset/mutation_report.xlsx'

    # Download File and save into defined path
    _status = download_file(_url, _file_path)

    """
     Check File Download Status
     If file downloaded successfully , then extract data
     else send message no data found
    """

    if _status:
        _data = extract_data_for_district_wise_total_application(_file_path, _tab_name, _group_by_column, _column,
                                                                 _limit)
        return jsonify(_data)
    else:
        return jsonify(default_message())


@application_data.route("/get-upazilla-wise-total-application", methods=['POST'])
def get_upazilla_wise_total_application():

    # Parse Request Body
    _request_data = request.get_json();
    _tab_name = _request_data['tabName']
    _column = _request_data['column']
    _district_name = _column['District']
    _upazilla_name = _column['Upazilla']
    _coloumnName = _request_data['columnName']
    _url = _request_data['url']
    _file_path = '/home/shakib/Development/dataset/mutation_report.xlsx'

    # Download File and save into defined path
    _status = download_file(_url, _file_path)

    if _status:
        _data = extract_data_for_upazilla_wise_total_application(_file_path, _tab_name, _district_name, _upazilla_name,
                                                                 _coloumnName)
        return jsonify(_data)
    else:
        return jsonify(default_message())


@application_data.route("/get-upazilla-wise-total-application-all", methods=['POST'])
def get_upazilla_wise_total_application_all():

    # Parse Request Body
    _request_data = request.get_json();
    _tab_name = _request_data['tabName']
    _column = _request_data['column']
    _district_name = _column['District']
    _coloumnName = _request_data['columnName']
    _url = _request_data['url']
    _file_path = '/home/shakib/Development/dataset/mutation_report.xlsx'

    # Download File and save into defined path
    _status = download_file(_url, _file_path)

    if _status:
        _data = extract_data_for_upazilla_wise_total_application_by_district(_file_path, _tab_name, _district_name,
                                                                             _coloumnName)
        return jsonify(_data)
    else:
        return jsonify(default_message())


@application_data.route("/get-total-application-month-wise", methods=['POST'])
def get_total_application_month_wise():

    # Parse Request Body
    _request_data = request.get_json();
    _tab_name = 'Application'
    _url = _request_data['url']
    _group_by = _request_data['group-by']

    _row = _request_data['row']
    _row_name = _row['name']
    _row_order = _row['order']
    _row_show_details = _row['show-totals']

    _column = _request_data['column']
    _column_name = _column['name']
    _column_order = _column['order']
    _column_show_details = _column['show-totals']

    _values = _request_data['values']
    _values_name = _values['name']
    _values_summarise_by = _values['summarise-by']

    _file_path = '/home/shakib/Development/dataset/mutation_report.xlsx'

    # Download File and save into defined path
    _status = download_file(_url, _file_path)

    if _status:
        _data = extract_data_for_total_application_month_wise(_file_path,_tab_name,_group_by,
                                                              _row_name,_row_order,_row_show_details,
                                                              _column_name, _column_order, _column_show_details,
                                                              _values_name,_values_summarise_by)
        return _data.to_json(orient='records')
    else:
        return jsonify(default_message())
