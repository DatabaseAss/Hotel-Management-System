import argparse
import pandas as pd
import numpy.core.defchararray as np_f
def _get_QUERY_from_csv(csv_file: str, sql_path:str, _start:int, _end: int, non_text_id: int, table) :

    frame = pd.read_csv(csv_file)
    # frame = frame.drop(['COMPANY_ID'], axis = 1)

    # header = 'PHONENUM'
    # formatted = [pnumber.replace("+84", "0").replace(' ','') for pnumber in \
    #             frame[header].values
    #     ]
    
    # frame[header] = formatted
    # frame.to_csv(csv_file)
    print(frame.head())
    HEADERS = [header for header in frame.columns]
    with open (sql_path, mode = 'w', encoding='utf-8') as writer:
        
        for idx, tuples in enumerate(frame.iloc[_start: _end].values):
            
            insert_string = 'INSERT INTO {}('.format(table)
            insert_string += HEADERS[0]
            for header in HEADERS[1:]:
                insert_string += ','+ header
            insert_string += ')'

            insert_string += ' VALUES('
            insert_string += "'{}'".format(tuples[0])

            for value_idx, value in enumerate(tuples[1:]):

                if value_idx + 1 < non_text_id:
                    insert_string += ',' + "'{}'".format(value)
                else:
                    insert_string += ',' + str(value)
            insert_string += ')\n'

            writer.writelines(insert_string)

def get_INSERT_room_type(csv_file, sql_path, _start, _end, notext):
    pass

if __name__ == '__main__':

    arg = argparse.ArgumentParser()
    arg.add_argument('--csv_path', type = str)
    arg.add_argument('--sql_path', type = str)
    arg.add_argument('--start_line', type = int, default = 1)
    arg.add_argument('--end_line', type = int, default = 11)
    arg.add_argument('--nontext', type = int, required=True)
    arg.add_argument('--table', type=str, required=True)
    parse = arg.parse_args()

    _get_QUERY_from_csv(parse.csv_path, parse.sql_path, parse.start_line, parse.end_line, parse.nontext, parse.table)