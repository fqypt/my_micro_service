import grpc

from user_srv.proto import user_pb2_grpc,user_pb2

#user_pb2_grpc里面主要发stub的server
#user_pb2里面主要放message

class UserTest:
    def __init__(self):
        #连接grpc服务
        channel = grpc.insecure_channel("127.0.0.1:50051")
        '''
        grpc之间是内部服务，所以可以用insecure（不安全服务），
        如果有要求可以安装grpc证书，确保服务安全
        '''
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo(pn=2,pSize=2))
        print(rsp.total)
        for user in rsp.data:
            print(user.mobile, user.birthDay)

if __name__ == "__main__":
    user = UserTest()
    user.user_list()


# import grpc
#
# from user_srv.proto import user_pb2_grpc, user_pb2


# user_pb2_grpc里面主要发stub的server
# user_pb2里面主要放message

# class UserTest:
#     def __init__(self):
#         # 连接grpc服务
#         channel = grpc.insecure_channel("127.0.0.1:50051")
#         '''
#         grpc之间是内部服务，所以可以用insecure（不安全服务），
#         如果有要求可以安装grpc证书，确保服务安全
#         '''
#         self.stub = user_pb2_grpc.UserStub(channel)
#
#     def user_list(self):
#         rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo())
#         print(rsp.total)
#         for user in rsp.data:
#             print(user.mobile, user.birthDay)
#
#
# if __name__ == "__main__":
#     user = UserTest()
#     user.user_list()
