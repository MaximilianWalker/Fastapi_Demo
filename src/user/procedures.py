from database import Database


class UserProcedures(Database):

    def __init__(self):
        super().__init__()

    def username_exists(self, username):
        return list(self.execute_procedure("Username_Exists", username, 0).arguments.values())[1] == 1

    def email_exists(self, email):
        return list(self.execute_procedure("Email_Exists", email, 0).arguments.values())[1] == 1

    def create_user(self, username, email, password_hash):
        self.execute_procedure("Create_User", username, email, password_hash)

    def get_user(self, username):
        return self.execute_procedure("Get_User", username, hasResult=True).result[0]

    def get_role_permissions(self, role):
        result = self.execute_procedure("Get_Role_Permissions", role).result
        return set(result.values()) if result is not None else ()

    def change_user_role(self, user_id, role_id):
        self.execute_procedure("Change_User_Role", user_id, role)

    def change_user_password(self, user_id, new_password):
        self.execute_procedure("Change_User_Password", user_id, role)

    def delete_user(self, user_id):
        self.execute_procedure("Delete_User", user_id)
