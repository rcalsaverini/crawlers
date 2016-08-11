import request
import dataset
import json
from datetime import date
from pandas import date_range
from crawler import parse

SPEECH_LIST_URL = "{base_url}/resultadoPesquisaDiscursos.asp".format(BASE_URL)
BASE_REQUEST_DATA = {"base": "plenario", "sort_field": "dtSessao", "page_size": 1000, "sorting": "DESC"}
DB = dataset.connect('sqlite:///test.db')

def initialize_queue():
    table = DB["list_of_speeches"]
    start_date = '01-01-1990'
    final_date = '01-06-2016'
    for end_date in date_range(start_date, final_date):
        register = {'start_date': str(start_date), 'end_date': str(end_date), 'fecthed': False}
        print(register)
        table.insert(register)









def get_list_of_speeches(start_date, end_date, **kwargs):
    request_params = dict(start_date=start_date, end_date=end_date, **BASE_REQUEST_DATA)
    request_params.update(**kwargs)
    html = request.get(url, params=request_params)
    return parse.list_of_speeches(html)

