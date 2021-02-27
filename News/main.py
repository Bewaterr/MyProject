from colorama import Fore,Style
from getpass import getpass
from service.user import UserService
from service.news import NewsService
from service.role import RoleService
from service.type import TypeService
import os,sys,time,mysql

__user_service = UserService()
__news_service = NewsService()
__role_service = RoleService()
__type_service = TypeService()


def cls():
    os.system("cls")

def back_to_previous():
    print(Fore.LIGHTRED_EX,"\n\t------------------------------")
    print(Fore.LIGHTRED_EX,"\t 任意时刻输入Q/q，返回上一级")
    print(Fore.LIGHTRED_EX,"\t------------------------------")
    print(Style.RESET_ALL)
    
def page_bottom():
    print(Fore.LIGHTBLUE_EX,"\n\t----------------------------------------")
    print(Fore.LIGHTGREEN_EX,"\t%d/%d" % (page,count_page),"         prev.上一页 | next.下一页")
    print(Fore.LIGHTBLUE_EX,"\t----------------------------------------")
    print(Style.RESET_ALL)


try:
    while True:
        cls()
        # 开始界面
        print(Fore.LIGHTBLUE_EX,"\n\t====================")
        print(Fore.LIGHTBLUE_EX,"\n\t欢迎使用新闻管理系统")
        print(Fore.LIGHTBLUE_EX,"\n\t====================")
        print(Fore.LIGHTGREEN_EX,"\n\t1.登录系统")
        print(Fore.LIGHTGREEN_EX,"\n\t2.退出系统")
        print(Style.RESET_ALL)
        # 输入操作
        opt = input("\n\t输入操作编号：").strip()
        # 登陆系统，获取用户名和密码
        if opt == "1":
            username = input("\n\t用户名：")
            password = getpass("\n\t密码：")
        # 退出系统
        elif opt == "2":
            sys.exit()
        # 其他内容重新输入   
        else:
            print("\n\t输入有误，请重新输入！")
            time.sleep(1)
            continue
        # 调用登录函数，验证用户名和密码
        result = __user_service.login(username,password)
        # 结果为假，验证失败，重新登陆
        if result == False:
            print("\n\t用户名或密码错误，登录失败!（3秒后自动返回）")
            time.sleep(3)
            continue
        # 结果为真，获取身份角色
        role = __user_service.search_user_role(username)
        print("\n\t登录成功！您的身份为：%s" % role)
        time.sleep(1)

        if role == "新闻编辑员":
            while True:
                break_flag = 0
                cls()
                back_to_previous()
                print(Fore.LIGHTGREEN_EX,"\n\t1.发表新闻")
                print(Fore.LIGHTGREEN_EX,"\n\t2.编辑新闻")
                print(Style.RESET_ALL)
                # 输入操作
                opt = input("\n\t输入操作编号：").strip()
                # 输入判断
                if opt == "Q" or opt == "q":
                    break
                elif opt != "1" and opt != "2":
                    print("\n\t输入有误！请重新输入")
                elif opt == "1":
                    # 发表新闻
                    while True:
                        cls()
                        back_to_previous()
                        # 1.输入新闻标题
                        title = input("\n\t新闻标题：").strip()
                        # 新闻标题输入判断
                        if opt == "Q" or opt == "q":
                            break
                        elif len(title) == 0:
                            print("\n\t新闻标题不能为空！请重新输入")
                            time.sleep(1)
                            continue
                        
                        while True:
                            cls()
                            back_to_previous()
                            # 通过登录时输入的用户名查找用户id
                            userid = __user_service.search_userid(username)
                            # 查找新闻类型列表并打印，以选择新闻类型
                            result = __type_service.search_list()
                            for index in range(len(result)):
                                one = result[index]
                                print(Fore.LIGHTBLUE_EX,"\t%d.\t%s" % (index+1,one[1]))
                            print(Style.RESET_ALL)
                            # 2.输入新闻类型
                            opt = input("\n\t类型编号：").strip()
                            # 新闻类型输入判断
                            if opt == "Q" or opt == "q":
                                break
                            elif opt.isdigit() == False:
                                print("\n\t输入有误！请输入数字")
                                time.sleep(1)
                                continue
                            elif int(opt) <= 0 or int(opt) > len(result):
                                print("\n\t超出范围！请重新输入")
                                time.sleep(1)
                                continue
                            # 3.获取类型编号
                            type_id = result[int(opt)-1][0]

                            path = input("\n\t输入文件路径：")
                            file = open(path,"r",encoding="utf-8")
                            content = file.read()
                            file.close()

                            while True:
                                cls()
                                back_to_previous()
                                # 4.获取置顶级别
                                is_top = input("\n\t置顶级别（0-5）：").strip()
                                # 置顶级别输入判断
                                if is_top == "Q" or is_top == "q":
                                    break
                                elif is_top.isdigit() == False:
                                    print("\n\t输入有误！请输入数字")
                                    time.sleep(1)
                                    continue
                                elif int(is_top) < 0 or int(is_top) > 5:
                                        print("\n\t请输入0-5之间的数字！")
                                        time.sleep(1)
                                        continue
                                
                                while True:
                                    cls()
                                    back_to_previous()
                                    # 5.是否提交
                                    is_submit = input("\n\t是否提交（Y/N）：")
                                    # 提交输入判断
                                    if is_submit == "Q" or is_submit == "q":
                                        break
                                    elif is_submit == "Y" or is_submit == "y":
                                        __news_service.insert(title,userid,type_id,content,int(is_top))
                                        print("\n\t保存成功！（3秒自动返回)")
                                        time.sleep(3)
                                        break_flag = 1
                                        break
                                    elif is_submit == "N" or is_submit == "n":
                                        break_flag = 1
                                        break
                                    else:
                                        print("\n\t输入有误，请重新输入！")
                                        time.sleep(1)
                                        continue
                                
                                if break_flag == 1:
                                    break
                            if break_flag == 1:
                                break
                        if break_flag == 1:
                            break

                elif opt == "2":
                    while True:
                        cls()
                        back_to_previous()
                        # 获取新闻列表并打印
                        page = 1
                        count_page = __news_service.search_list_count()
                        result = __news_service.search_list(page)
                        for index in range(len(result)):
                            one = result[index]
                            print(Fore.LIGHTBLUE_EX,"\t%d\t%s\t%s\t%s" % (index+1,one[1],one[2],one[3]))
                        page_bottom()
                        # 1.输入新闻编号
                        opt = input("\n\t输入操作编号：").strip()
                        # 新闻编号输入判断
                        if opt == "Q" or opt == "q":
                            break
                        elif opt == "prev" and page > 1:
                            page -= 1
                        elif opt == "next" and page < count_page:
                            page += 1
                        elif opt.isdigit() == False:
                                print("\n\t输入有误，请输入数字！")
                                time.sleep(1)
                                continue
                        elif int(opt) < 1 or int(opt) > len(result):
                            print("\n\t超出范围，请重新输入！")
                            time.sleep(1)
                            continue
                        # 如果输入正确，获取新闻编号，新闻标题，新闻类别以及置顶级别
                        news_id = result[int(opt)-1][0]
                        result = __news_service.search_by_id(news_id)
                        title = result[0]
                        type = result[1]
                        is_top = result[2]

                        while True:
                            cls()
                            back_to_previous()
                            # 2.打印旧标题，输入新标题
                            print("\n\t新闻原标题：%s" %(title))
                            new_title = input("\n\t新闻新标题：").strip()
                            # 输入判断
                            if new_title == "Q" or new_title == "q":
                                break
                            elif len(new_title) == 0:
                                print("\n\t标题不能为空，请重新输入！")
                                time.sleep(1)
                                continue

                            while True:
                                cls()
                                back_to_previous()
                                # 3.打印旧类型，输入新类型
                                print("\n\t原类型：%s" %(type))
                                # 获取并打印类型列表
                                result = __type_service.search_list()
                                for index in range(len(result)):
                                    one = result[index]
                                    print(Fore.LIGHTBLUE_EX,"\t%d.\t%s" % (index+1,one[1]))
                                print(Style.RESET_ALL)
                                # 3.打印旧类型，输入新类型
                                new_type = input("\n\t新类型编号：").strip()
                                # 输入判断
                                if new_type == "Q" or new_type == "q":
                                    break
                                elif new_type.isdigit() == False:
                                    print("\n\t输入有误，请输入数字！")
                                    time.sleep(1)
                                    continue
                                elif int(new_type) <= 0 or int(new_type) > len(result):
                                    print("\n\t超出范围，请重新输入！")
                                    time.sleep(1)
                                    continue
                                # 获取类型id
                                type_id = result[int(opt)-1][0]
                                # TODO
                                path = input("\n\t输入内容路径")
                                file = open(path,"r",encoding="utf-8")
                                content = file.read()
                                file.close()

                                while True:
                                    cls()
                                    back_to_previous()
                                    # 4.打印旧置顶，输入新置顶
                                    print("\n\t原置顶级别：%s" %(is_top))
                                    new_is_top = input("\n\t指定级别（0-5）：")
                                    # 输入判断
                                    if new_is_top == "Q" or new_is_top == "q":
                                        break
                                    elif new_is_top.isdigit() == False:
                                        print("\n\t输入有误！请输入数字")
                                        time.sleep(1)
                                        continue
                                    elif int(new_is_top) < 0 or int(new_is_top) > 5:
                                            print("\n\t请输入0-5之间的数字！")
                                            time.sleep(1)
                                            continue
                                    
                                    while True:
                                        cls()
                                        back_to_previous()
                                        # 是否提交
                                        is_submit = input("\n\t是否提交（Y/N）：")
                                        # 输入判断
                                        if is_submit == "Q" or is_submit == "q":
                                            break
                                        elif is_submit == "Y" or is_submit == "y":
                                            __news_service.update(news_id,new_title,type_id,content,new_is_top)
                                            print("\n\t保存成功！（3秒自动返回)")
                                            time.sleep(3)
                                            break_flag = 2
                                            break
                                        elif is_submit == "N" or is_submit == "n":
                                            break_flag = 2
                                            break
                                        else:
                                            print("\n\t输入有误，请重新输入！")
                                            time.sleep(1)
                                            continue

                                    if break_flag == 2:
                                        break
                                if break_flag == 2:
                                    break
                            if break_flag == 2:
                                break

        elif role == "新闻管理员":
            while True:
                cls()
                back_to_previous()
                print(Fore.LIGHTGREEN_EX,"\n\t1.审批新闻")
                print(Fore.LIGHTGREEN_EX,"\n\t2.删除新闻")
                print(Style.RESET_ALL)

                opt = input("\n\t输入操作编号：").strip()
                if opt == "Q" or opt == "q":
                    break
                elif opt == "1":
                    cls()
                    page = 1
                    while True:
                        cls()
                        count_page = __news_service.search_unreview_list_count()
                        result = __news_service.search_unreview_list(page)
                        back_to_previous()
                        for index in range(len(result)):
                            one = result[index]
                            print(Fore.LIGHTBLUE_EX,"\t%d\t%s\t%s\t%s" % (index+1,one[1],one[2],one[3]))                 
                        page_bottom()

                        opt = input("\n\t输入操作编号：").strip()
                        if opt == "Q" or opt == "q":
                            break
                        elif opt == "prev" and page > 1:
                            page -= 1
                        elif opt == "next" and page < count_page:
                            page += 1
                        else:
                            try:
                                if int(opt) >= 1 and int(opt) <= len(result):
                                    news_id = result[int(opt) - 1][0]
                                    __news_service.update_unreview_news(news_id)
                                    print("\n\t审批成功！")
                                    time.sleep(1)
                                    result = __news_service.search_cache(news_id)
                                    title = result[0]
                                    username = result[1]
                                    type = result[2]
                                    content_id = result[3]
                                    content = __news_service.search_content_by_id(content_id)
                                    is_top = result[4]
                                    create_time = str(result[5])
                                    __news_service.cache_news(news_id,title,username,type,content,is_top,create_time)

                                else:
                                    print("\n\t输入有误，请重新输入!")
                                    time.sleep(1)
                            except Exception as e:
                                print("\n\t%s"%e)
                                print("\n\t输入有误，请重新输入!")
                                time.sleep(1)
                elif opt == "2":
                    cls()
                    page = 1
                    while True:
                        cls()
                        count_page = __news_service.search_list_count()
                        result = __news_service.search_list(page)

                        back_to_previous()
                        for index in range(len(result)):
                            one = result[index]
                            print(Fore.LIGHTBLUE_EX,"\t%d\t%s\t%s\t%s" % (index+1,one[1],one[2],one[3]))
                        page_bottom()

                        opt = input("\n\t输入操作编号：").strip()
                        if opt == "Q" or opt == "q":
                            break
                        elif opt == "prev" and page > 1:
                            page -= 1
                        elif opt == "next" and page < count_page:
                            page += 1
                        else:
                            try:
                                if int(opt) >= 1 and int(opt) <= len(result):
                                    news_id = result[int(opt) - 1][0] 
                                    __news_service.delete_by_id(news_id)
                                    # 删除redis缓存新闻
                                    __news_service.delete(news_id)
                                    print("\n\t删除成功！")
                                    time.sleep(10)
                                else:
                                    print("\n\t输入有误，请重新输入!")
                                    time.sleep(1)
                            except Exception as e:
                                print("\n\t%s"%e)
                                print("\n\t输入有误，请重新输入!")
                                time.sleep(1)
                else:
                    print("\n\t输入有误，请重新输入！")
                    time.sleep(1)

        elif role == "用户管理员":
            while True:  # 用户添加、用户修改与用户删除页面
                break_flag = 0
                cls()
                back_to_previous()
                print(Fore.LIGHTGREEN_EX,"\n\t1.用户添加")
                print(Fore.LIGHTGREEN_EX,"\n\t2.用户修改")
                print(Fore.LIGHTGREEN_EX,"\n\t3.用户删除")
                print(Style.RESET_ALL)

                opt = input("\n\t输入操作编号：").strip()

                if opt == "Q" or opt == "q":
                    break    
                
                elif opt == "1":
                    # 添加用户名
                    while True:
                        cls()
                        back_to_previous()
                        username = input("\n\t用户名：").strip()
                        if username == "Q" or username == "q":
                            break
                        elif len(username) == 0:
                            print("\n\t用户名不能为空！")
                            time.sleep(1)
                            continue
                        else:
                            result = __user_service.research_username(username)
                            if result != None:
                                print("\n\t用户名已存在，请重新输入！")
                                time.sleep(1)
                                continue
                            else:
                                print("\n\t用户名可以使用！")
                                time.sleep(1)
                    
                        # 添加密码
                        while True:
                            cls()
                            back_to_previous()
                            password = getpass("\n\t密码：").strip()
                            if password == "Q" or password == "q":
                                break
                            elif len(password) == 0:
                                print("\n\t密码不能为空！请重新输入")
                                time.sleep(1)
                                continue
                            else:
                                repassword = getpass("\n\t重复密码：").strip()
                                if repassword == "Q" or repassword == "q":
                                    break
                                elif repassword != password:
                                    print("\n\t两次密码不一致！请重新输入")
                                    time.sleep(1)
                                    continue

                            # 添加邮箱
                            while True:
                                cls()
                                back_to_previous()
                                email = input("\n\t邮箱：").strip()
                                if email == "Q" or email == "q":
                                    break
                                elif email.find("@") == -1 or not email.endswith(".com"):
                                    print("\n\t邮箱格式错误，请重新输入！")
                                    time.sleep(1)
                                    continue                           
                                # 选择角色
                                while True:
                                    cls()
                                    back_to_previous()
                                    result = __role_service.search_role()
                                    for index in range(len(result)):
                                        one = result[index]
                                        print(Fore.LIGHTBLUE_EX,"\t%d.\t%s" % (index+1,one[1]))
                                        print(Style.RESET_ALL)
                                    try:
                                        opt = input("\n\t角色编号：").strip()
                                        if opt == "Q" or opt == "q":
                                            break
                                        else:
                                            role_id = result[int(opt)-1][0]
                                            __user_service.insert(username,password,email,role_id)
                                            print("\n\t用户添加成功！")
                                            time.sleep(1)
                                    except:
                                        print("\n\t输入有误，请重新输入！")
                                        time.sleep(1)
                                        continue                                   
                                    # 继续添加
                                    while True:
                                        cls()
                                        opt = input("\n\t是否要继续添加？Y/N：").strip()
                                        if opt == "Y" or opt == "y":
                                            break_flag = 1
                                        elif opt == "N" or opt == "n":
                                            break_flag = 2
                                        else:
                                            print("\n\t输入有误！（3秒后自动返回）")
                                            time.sleep(3)
                                            break_flag = 2
                                        if break_flag == 1 or break_flag == 2:
                                            break
                                    if break_flag == 1 or break_flag == 2:
                                        break
                                if break_flag == 1 or break_flag == 2:
                                    break                           
                            if break_flag == 1 or break_flag == 2:
                                break
                        if break_flag == 2:
                            break

                elif opt == "2":
                    page = 1     
                    while True:  # 用户列表页面
                        break_flag = 0
                        cls()
                        back_to_previous()
                        count_page = __user_service.search_count_page()
                        result = __user_service.search_user_list(page)
                        for index in range(len(result)):
                            one = result[index]
                            print(Fore.LIGHTBLUE_EX,"\t%d\t%s\t%s" % (index+1,one[1],one[2]))
                        
                        page_bottom()

                        opt = input("\n\t输入操作编号：").strip()
                        if opt == "Q" or opt == "q":
                            break
                        elif opt == "prev" and page > 1:
                            page -= 1
                            continue
                        elif opt == "next" and page < count_page:
                            page += 1
                            continue                   
                        else:
                            if opt.isdigit() == True:
                                if int(opt) >= 1 and int(opt) <= len(result):
                                    user_id = result[int(opt)-1][0]
                                else:
                                    print("\n\t输入数字超出范围，请重新输入！")
                                    time.sleep(1)
                                    continue
                            else:
                                print("\n\t输入有误，请输入数字！")
                                time.sleep(1)
                                continue

                        # 新用户名
                        while True:
                            cls()
                            back_to_previous()
                            username = input("\n\t新用户名：").strip()
                            result = __user_service.research_username(username)

                            if len(username) == 0:
                                print("\n\t用户名不能为空！请重新输入")
                                time.sleep(1)
                                continue
                            elif username == "Q" or username == "q":
                                break
                            elif result != None:
                                print("\n\t用户名已存在，请重新输入！")
                                time.sleep(1)
                                continue
                            else:
                                print("\n\t用户名可以使用！")
                                time.sleep(1)

                            # 新密码
                            while True:
                                cls()
                                back_to_previous()

                                password = getpass("\n\t新密码：").strip()
                                if len(password) == 0:
                                    print("\n\t密码不能为空，请重新输入！")
                                    time.sleep(1)
                                    continue
                                elif password == "Q" or password == "q":
                                    break

                                repassword = getpass("\n\t重复密码：").strip()

                                if repassword =="Q" or repassword == "q":
                                    break
                                elif repassword != password:
                                    print("\n\t两次密码输入不一致，请重新输入！")
                                    time.sleep(1)
                                    continue

                                # 新邮箱
                                while True:
                                    cls()
                                    back_to_previous()

                                    email = input("\n\t新邮箱：").strip()
                                    if email == "Q" or email == "q":
                                        break
                                    elif email.find("@") == -1 or not email.endswith(".com"):
                                        print("\n\t邮箱格式错误，请重新输入！")
                                        time.sleep(1)
                                        continue

                                    # 新角色
                                    while True:
                                        cls()
                                        back_to_previous()                                     
                                        # 查询角色列表
                                        result = __role_service.search_role()
                                        # 打印角色列表
                                        for index in range(len(result)):
                                            one = result[index]
                                            print(Fore.LIGHTBLUE_EX,"\n\t%d.\t%s" % (index+1,one[1]))                            
                                        print(Style.RESET_ALL)
                                        
                                        try:
                                            opt = input("\n\t角色编号：").strip()
                                            if opt == "Q" or opt == "q":
                                                break
                                            role_id = result[int(opt)-1][0]
                                        except:
                                            print("\n\t输入有误，请重新输入!")
                                            time.sleep(1)
                                            continue
                                                                                      
                                        while True:
                                            cls()
                                            back_to_previous()
                                            opt = input("\n\t是否保存？(Y/N)：").strip()
                                            if opt == "Q" or opt == "q":
                                                break
                                            elif opt == "Y" or opt == "y":
                                                __user_service.update(user_id,username,password,email,role_id)
                                                print("\n\t保存成功！(3秒自动返回)")
                                                time.sleep(3)
                                                break
                                            elif opt == "N" or opt == "n":
                                                print("\n\t信息保存失败！(3秒自动返回)")
                                                time.sleep(3)
                                                break
                                            else:
                                                print("\n\t输入有误，请重新输入!")
                                                time.sleep(1)


                                        if break_flag == 0:
                                            break
                                    if break_flag == 0:
                                        break
                                if break_flag == 0:
                                    break
                            if break_flag == 0:
                                break

                elif opt == "3":
                    page = 1
                    while True:
                        count_page = __user_service.search_count_page()
                        result = __user_service.search_user_list(page)

                        cls()
                        back_to_previous()
                        for index in range(len(result)):
                            one = result[index]
                            print(Fore.LIGHTBLUE_EX,"\t%d\t%s\t%s" % (index+1,one[1],one[2]))
                        print(Style.RESET_ALL)
                        page_bottom()

                        opt = input("\n\t输入操作编号：")
                        if opt == "Q" or opt == "q":
                            break
                        elif opt == "prev" and page > 1:
                            page -= 1
                        elif opt == "next" and page < count_page:
                            page += 1
                        else:
                            if opt.isdigit() == True:
                                if int(opt) >= 1 and int(opt) <= len(result):
                                    user_id = result[int(opt)-1][0]
                                    while True:
                                        cls()
                                        opt = input("\n\t确定删除？（Y/N）：").strip()
                                        if opt == "Y" or opt == "y":
                                            __user_service.delete_by_id(user_id)
                                            print("\n\t删除成功！（3秒自动返回）")
                                            time.sleep(3)
                                            break
                                        elif opt == "N" or opt == "n":
                                            print("\n\t删除已取消")
                                            time.sleep(1)
                                            break
                                        else:
                                            print("\n\t输入有误，请重新输入！")
                                            time.sleep(1)
                                else:
                                    print("\n\t输入超出范围，请重新输入！")
                                    time.sleep(1)

                            else:
                                print("\n\t请输入数字！")
                                time.sleep(1)

                else:
                    print("\n\t输入有误，请重新输入")
                    time.sleep(1)
    
except Exception as e:
    print(e)
    time.sleep(3)
