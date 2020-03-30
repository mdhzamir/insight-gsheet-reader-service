from flask import jsonify,Blueprint,request, current_app
from bs4 import BeautifulSoup
import requests


# Initialize Blueprint
covid_data = Blueprint('covid_data',__name__, url_prefix='/api/covid-data')

@covid_data.route("/get-covid-data", methods=['POST'])
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







