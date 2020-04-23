from flask import request,jsonify,Blueprint,current_app
from src.utility.utilities import *
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests


# Initialize Blueprint
main_data = Blueprint('main_data',__name__, url_prefix='/api/main-sheet')

@main_data.route("/get-main-data", methods=['POST'])
def get_main_sheet_data():
    try:
        asc_order_data_arr = []
        desc_order_data_arr = []
        column_names_data = []
        remove_row = ''
        order_data = []
        tab_name = ''

        # Parse Request Body
        request_data = request.get_json();
        url = request_data['url']
        if 'columns' in request_data:
            column_names = request_data['columns']
            column_names_data = column_names.split(',')
        if 'tab-name' in request_data:
            tab_name = request_data['tab-name']
        if 'remove-row' in request_data:
            remove_row = request_data['remove-row']
        if 'order' in request_data:
            order = request_data['order']
            order_data = order.split(',')

        for item in order_data:
            if item.startswith('asc'):
                asc_order_data = item[item.index('asc') + 4:len(item)]
                asc_order_data_arr = asc_order_data.split(' ')
            elif item.startswith('desc'):
                desc_order_data = item[item.index('desc') + 5:len(item)]
                desc_order_data_arr = desc_order_data.split(' ')

        # Read Data after basic cleaning
        df = read_sheet(url, tab_name, column_names_data)

        # Remove Row based on given condition in json
        if remove_row != '':
            df = remove_row_from_dataframe(remove_row, df)

        # if pivot available in json , then group by apply over dataset
        if 'pivot' in request_data:
            df = pivot_dataframe(request_data, df)

        # Sort Values over Data, based on condition given in json
        if len(asc_order_data_arr) > 0:
            df = df.sort_values(by=asc_order_data_arr, ascending=True)
        if len(desc_order_data_arr) > 0:
            df = df.sort_values(by=desc_order_data_arr, ascending=False)

        return df.to_json(orient='records')

    except Exception as e:
        print('Exception Occured' , e)
        return default_message(e)


@main_data.route("/get-covid-data", methods=['POST'])
def get_covid_data():
    try:
        current_app.logger.info('Step 1 Got Request  -------')
        response = []
        column_names = []

        # Parse Request Body
        request_data = request.get_json();
        url = request_data['url']
        table_id = request_data['table-id']

        current_app.logger.info('Step 2 Parse Request Body {} {}'.format(url, table_id))

        # Download Page Source
        page = requests.get(url)
        html_doc = page.content
        current_app.logger.info('Step 3 Html Content {}'.format(html_doc))

        # Create beautiful soup instance and parse page source to beautifulsoup
        soup = BeautifulSoup(html_doc, 'html.parser')
        table = soup.find('table', id = table_id)
        rows = table.find_all('tr')

        current_app.logger.info('Step 4 ------ ')

        # Extract Column names from table
        for tx in table.find_all('th'):
            table_header_text = tx.get_text()
            if ',' in table_header_text:
                table_header_text = table_header_text.replace(',', '/')
            if '\xa0' in table_header_text:
                table_header_text = table_header_text.replace('\xa0', '')
            column_names.append(table_header_text)

        # current_app.logger.info('Step 5 all rows ', column_names)
        current_app.logger.info('Step 5 ------ ')

        # Extract Data from table
        for row in rows:
            i = 0
            data = row.find_all("td")
            data_length = len(data)
            response_dict = {}
            if data_length > 0:
                for d in data:
                    text = d.get_text()
                    if text == '':
                        text = str(0)
                    if ',' in text:
                        text = text.replace(',', '')
                    if '+' in text:
                        text = text.replace('+', '')
                    if '\n' in text:
                        text = text.replace('\n', '')
                    if '\xa0' in text:
                        text = text.replace('\xa0', '')
                    if i < len(column_names):
                        response_dict[str(column_names[i])] = str(text)
                    i += 1
                response.append(response_dict)
        # current_app.logger.info('Step 6 final response ---', response)
        current_app.logger.info('Step 6 ------ ')
        return jsonify(response)
    except Exception as e:
        current_app.logger.info('Exception  ---', e)
        return {'status':'Error'}



@main_data.route("/pivot-data", methods=['POST'])
def pivot_data():
    order_data = ''

    try:
        # Parse Request Body
        request_data = request.get_json();
        properties = request_data['properties']
        data = request_data['data']['listData']

        if 'order' in properties:
            order = properties['order']
            order_data = order.split(',')

        df = pd.DataFrame.from_dict(data, orient='columns')

        # Pivot Dataframe based on condition
        if 'pivot' in properties:
           df = pivot_dataframe(properties, df)

        # Sort Data Based On Condition
        if len(order_data) > 0 :
            df = sort_values(df, order_data)

        return df.to_json(orient='records')

    except Exception as e:
        return jsonify(default_message())
