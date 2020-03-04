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
def default_message():
    _message = {'msg':'No Data Found'}
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