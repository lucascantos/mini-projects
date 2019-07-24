from google_credential import GoogleDrive, error_handler

class GoogleSheets(GoogleDrive):
    def grab_spreadsheet(self, spreadsheet_name, sheet_name='Somar'):
        sheetid = self._get_fileid(spreadsheet_name)
        database = self.sheet_services.spreadsheets().values().get(spreadsheetId=sheetid['id'], range=sheet_name).execute()
        database = database['values']
        self.dataframe = self._make_dataframe(database)

    def _make_dataframe(self, database):
        import pandas as pd
        df = pd.DataFrame(database, columns=database[0])
        df=df[1:]
        df.reset_index(inplace=True, drop=True)
        return df