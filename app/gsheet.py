import gspread
import pandas as pd
import pprint as pp

AUTH_JSON = 'app/config/gs.json'
SHEET_KEY = '1dLiRvIaTeSsBQEhic4iRYQbWVj2_qYT8h7mRIrkcC0g'

class GSheet(object):
    def __init__(self, sheet_key, auth_json):
        self.sheet_key = sheet_key
        self.auth_json = auth_json
        self.sheet = self.sheet()

    def sheet(self):
        gc = gspread.service_account(filename=self.auth_json)
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
        cols_list = [col.replace(find, replacement) in cols_list]
    return cols_list


def main():
    gc = GSheet(SHEET_KEY, AUTH_JSON)
    form_data = gc.wks('Responses').get_all_records()
    form_df = pd.Dataframe(form_data)
    form_df.columns = clean_cols(form_df.columns.tolist())


if __name__ == "__main__":
    main()