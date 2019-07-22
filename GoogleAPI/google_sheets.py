from google_credential import GoogleDrive, error_handler

class GoogleSheets(GoogleDrive):
    def grab_spreadsheet(self, spreadsheet_name, sheet_name='Somar'):
        sheetid = self.get_fileid(spreadsheet_name)
        self.database = self.sheet_services.spreadsheets().values().get(spreadsheetId=sheetid['id'], range=sheet_name).execute()
        self.database = self.database['values']

    def make_dataframe(self):
        import pandas as pd
        df = pd.DataFrame(self.database, columns=self.database[0])
        df=df[1:]
        df.reset_index(inplace=True, drop=True)
        return df