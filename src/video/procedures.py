from database import Database

class VideoProcedures(Database):

    def __init__(self):
        super().__init__()

    def get_video(self, video_id):
        cursor = self.connection.cursor()
        procedure = "CALL Get_Video(%s)"
        cursor.execute(procedure, (video_id))
        self.connection.commit()
        cursor.close()