from src.utility.utilities import download_file


def test():
    _url = 'https://drive.google.com/uc?id=1yqaJhFlS2WgIcqNZWuFbOuqHTCq7HyYO1'
    _file_path = '/home/shakib/Development/dataset/mutation_report.xlsx'
    _status = download_file(_url, _file_path)

    assert _status == True
