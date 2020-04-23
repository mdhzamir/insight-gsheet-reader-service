import gdown
import pandas as pd


# Downloading File
def download_file(_url, _output):
    try:
        gdown.download(_url, _output, quiet=False)
        return True
    except IOError:
        return False
    except:
        return False


# Read File
def read_file(_file_path, _tab_name):
    # Read File from defined path
    _xls = pd.ExcelFile(_file_path)

    # Basic Operation Over Data
    _sheetNames = _xls.sheet_names
    _index = _sheetNames.index(_tab_name)
    _sheet = _xls.parse(_sheetNames[_index], index=False)

    return _sheet


# Default Message
def default_message(e):
    _message = {'msg':'Exception {}'.format(e)}
    return _message



# Extract Data
def extract_data_for_district_wise_total_application(_file_path, _tab_name, _group_by_column, _column, _limit):

    # Operation Over Data
    _sheet = read_file(_file_path, _tab_name)
    _group_by_sum = _sheet.groupby(_group_by_column)[_column].sum()
    _json_data = _group_by_sum.iloc[:int(_limit)]
    _data = _json_data.to_dict()

    return _data



# Extract Data
def extract_data_for_upazilla_wise_total_application(_file_path, _tab_name,_district_name, _upazilla_name, _coloumnName):

    # Operation Over Data
    _sheet = read_file(_file_path, _tab_name)
    _sheet = _sheet[(_sheet['District'] == _district_name)][(_sheet['Upazilla'] == _upazilla_name)]
    _total_value = _sheet[_coloumnName].sum()
    _value = {'Total Application': str(_total_value)}

    return _value


# Extract Data
def extract_data_for_upazilla_wise_total_application_by_district(_file_path, _tab_name,_district_name, _coloumnName):

    # Operation Over Data
    _sheet = read_file(_file_path, _tab_name)
    _sheet = _sheet[(_sheet['District'] == _district_name)].groupby('Upazilla')['Application'].sum()
    _data = _sheet.to_dict()

    return _data


# Extract Data
def extract_data_for_total_application_month_wise(_file_path, _tab_name,_group_by,
                                                  _row_name,_row_order,_row_show_details,
                                                  _column_name, _column_order, _column_show_details,
                                                  _values_name,_values_summarise_by):
    _group_by_data = _group_by.split(',')

    # Operation Over Data
    _sheet = read_file(_file_path, _tab_name)
    if _values_summarise_by == 'SUM':
        _sheet = _sheet.groupby(_group_by_data)[_values_name].sum().reset_index()
    elif _values_summarise_by == 'COUNT':
        _sheet = _sheet.groupby(_group_by_data)[_values_name].count().reset_index()
    elif _values_summarise_by == 'MAX':
        _sheet = _sheet.groupby(_group_by_data)[_values_name].max().reset_index()
    elif _values_summarise_by == 'MIN':
        _sheet = _sheet.groupby(_group_by_data)[_values_name].min().reset_index()

    _sheet = _sheet.pivot_table(index=_row_name, columns=_column_name, values=_values_name, fill_value=0)

    # Row Sort
    if _row_order == 'Ascending':
        _sheet = _sheet.sort_values(_row_name, ascending=True)
    else:
        _sheet = _sheet.sort_values(_row_name, ascending=False)


    # Column Sort
    if _column_order == 'Ascending':
        _sheet = _sheet.reindex(sorted(_sheet.columns, reverse=False), axis=1)
    else:
        _sheet = _sheet.reindex(sorted(_sheet.columns, reverse=True), axis=1)


    # Add Total in row
    if _row_show_details == 'true':
        if _values_summarise_by == 'MAX':
            _sheet.loc['Grand Total'] = _sheet.max()
        elif _values_summarise_by == 'MIN':
            _sheet.loc['Grand Total'] = _sheet.min()
        else:
            _sheet.loc['Grand Total'] = _sheet.sum()


    # Add Total in column
    if _column_show_details == 'true':
        if _values_summarise_by == 'MAX':
            _sheet['Grand Total'] = _sheet.max(axis=1)
        if _values_summarise_by == 'MIN':
            _sheet['Grand Total'] = _sheet.min(axis=1)
        else:
            _sheet['Grand Total'] = _sheet.sum(axis=1)

    _index_value = _sheet.index
    _sheet.insert(loc=0, column='District', value=_index_value)
    # Delete Extra Index
    # del _sheet.index.name

    return _sheet

# def read_sheet(file_path, tab_name, column_names_data):
#     xls = pd.ExcelFile(file_path)
#     sheetNames = xls.sheet_names
#     index = sheetNames.index(tab_name)
#     sheet = xls.parse(sheetNames[index], index=False)
#     if len(column_names_data) > 0:
#         df = sheet[column_names_data]
#         print(df.first)
#     else:
#         df = sheet
#
#     return df


def read_sheet(url, tab_name, column_names_data):
    xls_df = pd.read_excel(url, tab_name)
    if len(column_names_data) > 0:
        # print(xls_df.head())
        return xls_df[column_names_data]
    else:
        # print(xls_df.head())
        return xls_df


def remove_row_from_dataframe(remove_row, df):
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

    return df


def get_column_names(request_data):
    if 'columns' in request_data:
        return request_data['columns'].split(',')


def sort_values(df, order_data):
    asc_order_data_arr = []
    desc_order_data_arr = []

    for item in order_data:
        if item.startswith('asc'):
            asc_order_data = item[item.index('asc') + 4:len(item)]
            asc_order_data_arr = asc_order_data.split(' ')
        elif item.startswith('desc'):
            desc_order_data = item[item.index('desc') + 5:len(item)]
            desc_order_data_arr = desc_order_data.split(' ')

    if len(asc_order_data_arr) > 0:
        df = df.sort_values(by=asc_order_data_arr, ascending=True)

    if len(desc_order_data_arr) > 0:
        df = df.sort_values(by=desc_order_data_arr, ascending=False)

    return df


def pivot_dataframe(request_data, df):
    try:
        agg_column_name = ''
        avg_column_name = ''
        sum_column_name = ''
        agg_data = {}
        rename_column = {}

        pivot_data = request_data['pivot']
        group_by_column = pivot_data['column']
        group_by_column_arr = group_by_column.split(',')

        if 'sum' in pivot_data:
            sum_column_arr = pivot_data['sum'].split(',')
            sum_agg_column_name = sum_column_arr[0]
            rename_column.update({'sum': sum_column_arr[1]})

            if sum_agg_column_name in agg_data.keys():
                data = agg_data.get(sum_agg_column_name)
                data.append('sum')
                agg_data[sum_agg_column_name] = data
            else:
                agg_data.update({sum_agg_column_name: ['sum']})

        if 'avg' in pivot_data:
            avg_column_arr = pivot_data['avg'].split(',')
            avg_agg_column_name = avg_column_arr[0]
            rename_column.update({'mean': avg_column_arr[1]})

            if avg_agg_column_name in agg_data.keys():
                data = agg_data.get(avg_agg_column_name)
                data.append('mean')
                agg_data[avg_agg_column_name] = data
            else:
                agg_data.update({avg_agg_column_name: ['mean']})

        if 'count' in pivot_data:
            count_column_arr = pivot_data['count'].split(',')
            count_agg_column_name = count_column_arr[0]
            rename_column.update({'count': count_column_arr[1]})

            if count_agg_column_name in agg_data.keys():
                data = agg_data.get(count_agg_column_name)
                data.append('count')
                agg_data[count_agg_column_name] = data
            else:
                agg_data.update({count_agg_column_name: ['count']})

        if len(agg_data) > 0:
            print(agg_data)
            # df = df.groupby(group_by_column_arr)[agg_column_name].agg(['sum', 'mean']).reset_index().rename(
            #     columns={'sum': sum_column_name, 'mean': avg_column_name})

            df = df.groupby(group_by_column_arr).agg(agg_data)

            df = df.droplevel(0, axis=1)
            df = df.rename(columns=rename_column)
            df = df.reset_index()
            # print(df.head())

        return  df
    except Exception as e:
        return df




# def pivot_dataframe(df, properties):
#     pivot_data = properties['pivot']
#     group_by_column = pivot_data['column']
#     group_by_column_arr = group_by_column.split(',')
#
#     sum_column_arr = pivot_data['sum'].split(',')
#     avg_column_arr = pivot_data['avg'].split(',')
#     agg_column_name = sum_column_arr[0]
#     sum_column_name = sum_column_arr[1]
#     avg_column_name = avg_column_arr[1]
#
#     if agg_column_name != '':
#         df = df.groupby(group_by_column_arr)[agg_column_name].agg(['sum', 'mean']).reset_index().rename(
#             columns={'sum': sum_column_name, 'mean': avg_column_name})
#
#     # print(df.head())
#     return df