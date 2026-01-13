from google.cloud import bigtable
from google.oauth2.service_account import Credentials

class Database:
    def __init__(self, project_id, instance_id, table_id, credentials_path):
        credentials = Credentials.from_service_account_file(credentials_path)
        self.client = bigtable.Client(project=project_id, credentials=credentials, admin=True)
        self.instance = self.client.instance(instance_id)
        self.table = self.instance.table(table_id)

        if not self.table.exists():
            self.table.create()
            self.table.column_family("cf1").create()
        elif "cf1" not in self.table.list_column_families():
            self.table.column_family("cf1").create()

    def insert_data(self, row_key, row_data):
        bt_row = self.table.row(row_key)
        for key, value in row_data.items():
            val_bytes = str(value).encode('utf-8')
            bt_row.set_cell("cf1", key, val_bytes)
        bt_row.commit()

    def close(self):
        self.client.close()