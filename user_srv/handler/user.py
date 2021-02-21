import time
import grpc

from loguru import logger
from peewee import DoesNotExist

from user_srv.models.model import User
from user_srv.proto import user_pb2, user_pb2_grpc


class UserServicer(user_pb2_grpc.UserServicer):

    @logger.catch
    class UserServicer(user_pb2_grpc.UserServicer):
        def GetUserList(self, request: user_pb2.PageInfo, context):
            # 获取用户的列表
            rsp = user_pb2.UserListResponse()

            # 获取所有用户对象
            users = User.select()
            # 获取user的数量
            rsp.total = users.count()

            # 分页逻辑
            start = 0
            per_page_nums = 10  # 每页默认是个数据
            if request.pSize:
                per_page_nums = request.pSize
            if request.pn:
                start = per_page_nums * (request.pn - 1)
            users = users.limit(per_page_nums).offset(start)

            for user in users:
                # s实例UserInfoResponse对象
                user_info_rsp = user_pb2.UserInfoResponse()
                # 用户数据传入user_info_rsp对象中
                user_info_rsp.id = user.id
                user_info_rsp.password = user.password
                user_info_rsp.mobile = user.mobile
                user_info_rsp.role = user.role

                # 对不确定的数据进行处理
                if user.nick_name:
                    user_info_rsp.nickName = user.nick_name
                if user.gender:
                    user_info_rsp.gender = user.gender
                # birthday类型是datetime比较特殊，需要转化为int
                if user.birthday:
                    user_info_rsp.birthDay = int(time.mktime(user.birthday.timetuple()))

                rsp.data.append(user_info_rsp)
            return rsp

    # @logger.catch
    #     # def GetUserById(self, request: user_pb2.IdRequest, context):
    #     #     # 通过id查询用户
    #     #     try:
    #     #         user = User.get(User.id == request.id)# 用get方法就需要处理异常
    #     #
    #     #         return self.convert_user_to_rsp(user)
    #     #     except DoesNotExist as  e:
    #     #         context.set_code(grpc.StatusCode.NOT_FOUND)  # 这里是内置code，相当于404
    #     #         context.set_details("用户不存在")
    #     #         return user_pb2.UserInfoResponse()


