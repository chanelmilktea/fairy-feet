import os
import json
import gspread
import pandas as pd

AUTH_JSON = json.loads(os.environ['GS_JSON'])
SHEET_KEY = os.environ['GS_SHEET_KEY']

class GSheet(object):
    def __init__(self, sheet_key, auth_json):
        self.sheet_key = sheet_key
        self.auth_json = auth_json
        self.sheet = self.sheet()

    def sheet(self):
        gc = gspread.service_account_from_dict(self.auth_json)
        return gc.open_by_key(self.sheet_key)

    def wks(self, wks_name):
        return self.sheet.worksheet(wks_name)


def clean_cols(cols_list):
    cols_list = [col.lower() for col in cols_list]
    subs = {
        '?': '',
        ' ': '_',
        '\'': ''
    }
    for find, replacement in subs.items():
        cols_list = [col.replace(find, replacement) for col in cols_list]
    return cols_list


def form_df():
    gc = GSheet(SHEET_KEY, AUTH_JSON)
    form_data = gc.wks('Responses').get_all_records()
    form_df = pd.DataFrame(form_data)
    form_df.columns = clean_cols(form_df.columns.tolist())
    form_df['shoe_size'].replace({None: 'Normal'})
    return form_df

def agg_form_df():
    df = form_df()
    df2 = df.groupby(['shoe_type','shoe_size', 'shoe_width', 'skate_brand']).agg(['mean', 'median'])
    return df2

def get_recs(gender, size, width):
    print(gender, size, width)
    df = agg_form_df()
    return df.loc[(gender, size, width), :]
