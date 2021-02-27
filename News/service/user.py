from dao.user import UserDao

class UserService:
    __user_dao = UserDao()
    # 验证用户登录
    def login(self,username,password):
        result = self.__user_dao.login(username,password)
        return result
    # 查询用户角色
    def search_user_role(self,username):
        role = self.__user_dao.search_user_role(username)
        return role
    # 添加用户
    def insert(self,username,password,email,role_id):
        self.__user_dao.insert(username,password,email,role_id)
    # 查询用户名
    def research_username(self,username):
        result = self.__user_dao.research_username(username)
        return result
    # 查询用户分页记录
    def search_user_list(self,page):
        result = self.__user_dao.search_user_list(page)
        return result
    # 查询用户总页数
    def search_count_page(self):
        count_page = self.__user_dao.search_count_page()
        return count_page
    # 修改用户信息
    def update(self,id,username,password,email,role_id):
        self.__user_dao.update(id,username,password,email,role_id)
    # 删除用户信息
    def delete_by_id(self,id):
        self.__user_dao.delete_by_id(id)
    # 查询用户密码
    def search_uesr_passwd(self,username):
        old_password = self.__user_dao.search_uesr_passwd(username)
        return old_password
    # 查询用户id
    def search_userid(self,username):
        userid = self.__user_dao.search_userid(username)
        return userid