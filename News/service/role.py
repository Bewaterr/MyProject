from dao.role import RoleDao

class RoleService:
    __role_dao = RoleDao()

    # 查询角色列表
    def search_role(self):
        result = self.__role_dao.search_role()
        return result