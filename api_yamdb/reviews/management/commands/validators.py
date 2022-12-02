import sys
from csv import reader


def data_validation(path, required_fields):

    try:
        with open(path, "r") as csv_file:
            data = list(reader(csv_file, delimiter=","))
            if not data:
                raise ValueError('No data available')
    except IOError:
        print('Could not open file')
        sys.exit()
    columns_names = list(data[0])
    for field in required_fields:
        if field not in columns_names:
            raise ValueError(f'Missing required column: {field}')
    return data
