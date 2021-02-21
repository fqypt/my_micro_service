import grpc
import time
from loguru import logger


from user_srv.proto import user_pb2,user_pb2_grpc
from user_srv.models.model import User

class UserServicer(user_pb2_grpc.UserServicer):
    @logger.catch
    def GetUserList(self, request: user_pb2.PageInfo, context):
        #获取用户列表功能
        rsp = user_pb2.UserListResponse()

        users = User.select()
        rsp.total = users.count()

        #分页逻辑
        start = 0
        per_page_nums = 10
        if request.pSize:
            per_page_nums = request.pSize
        if request.pn:
            start = per_page_nums*(request.pn-1)
        users = users.limit(per_page_nums).offset(start)


        #返回用户信息
        for user in users:
            user_info_rsp = user_pb2.UserInfoResponse()
            user_info_rsp.id = user.id
            user_info_rsp.password = user.password
            user_info_rsp.mobile = user.mobile
            user_info_rsp.role = user.role

            if user.nick_name:
                user_info_rsp.nickName = user.nick_name
            if user.gender:
                user_info_rsp.gender = user.gender
            if user.birthday:
                user_info_rsp.birthDay = int(time.mktime(user.birthday.timetuple()))

            rsp.data.append(user_info_rsp)
        return rsp