from database import Database

class FileProcedures(Database):

    def __init__(self):
        super().__init__()

    def create_file(self, upload_user_id, file_type, file_name, path):
        cursor = self.connection.cursor()
        procedure = "CALL Create_File(%s)"
        cursor.execute(procedure, (upload_user_id, file_type, file_name, path))
        self.connection.commit()
        cursor.close()