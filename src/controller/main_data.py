from flask import request,jsonify,Blueprint,current_app
from src.utility.utilities import *
import pandas as pd
import os


# Initialize Blueprint
main_data = Blueprint('main_data',__name__, url_prefix='/api/main-sheet')

def read_sheet(file_path, tab_name, column_names_data):
    xls = pd.ExcelFile(file_path)
    sheetNames = xls.sheet_names
    index = sheetNames.index(tab_name)
    sheet = xls.parse(sheetNames[index], index=False)
    if len(column_names_data) > 0:
        df = sheet[column_names_data]
    else:
        df = sheet

    return df



@main_data.before_app_request
def log_msg_before_request():
    current_app.logger.info('REQUEST----------------------')
    current_app.logger.info('Body: %s', request.get_json())


@main_data.route("/get-main-data", methods=['POST'])
def get_main_sheet_data():
    asc_order_data = ''
    desc_order_data = ''
    asc_order_data_arr = []
    desc_order_data_arr = []
    column_names= ''
    column_names_data= []
    remove_row= ''
    order = ''
    order_data = []
    tab_name=''
    agg_column_name=''
    sum_column_name=''
    avg_column_name=''
    group_by_column_arr = []


    # Parse Request Body
    request_data = request.get_json();
    url = request_data['url']
    sheet_name = request_data['sheet-name']

    if(sheet_name.endswith('.xlsx')==False):
        sheet_name = sheet_name + '.xlsx'

    # Download File and save into defined path
    _status = download_file(url, sheet_name)

    if _status:

        # Parse Json Data
        try:
            if 'columns' in request_data:
                column_names = request_data['columns']
                column_names_data = column_names.split(',')

            tab_name = request_data['tab-name']
            remove_row = request_data['remove-row']

            order = request_data['order']
            order_data = order.split(',')

            if 'pivot' in request_data:
                pivot_data = request_data['pivot']
                group_by_column = pivot_data['column']
                group_by_column_arr = group_by_column.split(',')

                sum_column_arr = pivot_data['sum'].split(',')
                avg_column_arr = pivot_data['avg'].split(',')
                agg_column_name = sum_column_arr[0]
                sum_column_name = sum_column_arr[1]
                avg_column_name = avg_column_arr[1]


        except:
            print('Exception Occured Json Parsing')


        for item in order_data:
            if item.startswith('asc'):
                asc_order_data = item[item.index('asc') + 4:len(item)]
                asc_order_data_arr = asc_order_data.split(' ')
            elif item.startswith('desc'):
                desc_order_data = item[item.index('desc') + 5:len(item)]
                desc_order_data_arr = desc_order_data.split(' ')


        # Read Data after basic cleaning
        df = read_sheet(sheet_name, tab_name, column_names_data)

        """
        Remove Row based on given condition in json
        """

        if remove_row != '':
            for key in remove_row:
                value = str(remove_row[key])

                if ',' in value:
                    value_arr = value.split(',')
                    for data in value_arr:
                        data = data.strip()

                        if data.startswith('is_empty'):
                            df.drop(df.loc[df[key] == ''].index, inplace=True)

                        elif data.startswith('contains'):
                            contains_row_value = data[data.index('contains') + 9: len(data)]
                            if ' ' in contains_row_value:
                                contains_row_value_arr = contains_row_value.split(' ')
                                for contains_data in contains_row_value_arr:
                                    df.drop(df.loc[df[key] == contains_data].index, inplace=True)
                            else:
                                df.drop(df.loc[df[key] == contains_row_value].index, inplace=True)

                        elif data.startswith('eq'):
                            eq_row_value = data[data.index('eq') + 3: len(data)]
                            if ' ' in eq_row_value:
                                eq_row_value_arr = eq_row_value.split(' ')
                                for eq_row_value in eq_row_value_arr:
                                    df.drop(df.loc[df[key] == int(eq_row_value)].index, inplace=True)
                            else:
                                df.drop(df.loc[df[key] == int(eq_row_value)].index, inplace=True)


                elif value.startswith('eq'):
                    remove_row_value = value[value.index('eq') + 3: len(value)]

                    if ' ' in remove_row_value:
                        remove_row_value_arr = remove_row_value.split(' ')
                        for eq_row_value in remove_row_value_arr:
                            df.drop(df.loc[df[key] == int(eq_row_value)].index, inplace=True)
                    else:
                        df.drop(df.loc[df[key] == int(remove_row_value)].index, inplace=True)


        """
        if pivot available in json , then group by apply over dataset
        """


        if agg_column_name != '':
            df = df.groupby(group_by_column_arr)[agg_column_name].agg(['sum', 'mean']).reset_index().rename(
                columns={'sum': sum_column_name, 'mean': avg_column_name})

        """
        Sort Values over Data, based on condition given in json
        """

        if len(asc_order_data_arr) > 0:
            df = df.sort_values(by=asc_order_data_arr, ascending=True)

        if len(desc_order_data_arr) > 0:
            df = df.sort_values(by=desc_order_data_arr, ascending=False)

        """
        After data processing, remove downloaded file
        """
        os.remove(sheet_name)

        return df.to_json(orient='records')

    else:
        return jsonify(default_message())