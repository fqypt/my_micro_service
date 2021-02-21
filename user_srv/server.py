import sys
import logging
import os
import signal
from concurrent import futures

import grpc
from loguru import logger


#sys.path.insert(0,"F:/develop/python/mxshop_srvs")
#BASE_DIR = os.path.dirname(__file__)
#print(BASE_DIR)   #F:/develop/python/mxshop_srvs/user_srv

# BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# sys.path.insert(0,BASE_DIR)



from user_srv.proto import user_pb2_grpc
from user_srv.handler.user import UserServicer

# def on_exit(signo,frame):
#     logger.info("进程中断")
#     #退出服务
#     sys.exit(0)


def serve():
    #配置文件输出
    # logger.add("logs/user_srv_{time}.log")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(),server)
    server.add_insecure_port('0.0.0.0:50051')

    #主进程退出信号监听
    '''
        windows下支持的信号量是有限的：
            SIGINT：ctrl+C中断
            SIGTERM：程序kill发出的软件终止
        这里停止不能用pycharm中的停止，是一个强杀命令，无法被监听，
        需要在terminal中运行
    '''
    #运行这两个命令就会产生一个信号，然后就会运行on_exit方法，停止服务
    # signal.signal(signal.SIGINT,on_exit)
    # signal.signal(signal.SIGTERM, on_exit)
    #
    # logger.info(f"启动服务：127.0.0.1：50051")
    print(f"启动服务：127.0.0.1：50051")
    server.start()
    server.wait_for_termination()


# @logger.catch
# def my_function(x, y, z):
#     # An error? It's caught anyway!
#     return 1 / (x + y + z)

if __name__ == '__main__':
    # logger.debug("调试信息")
    # logger.info("普通信息")
    # logger.warning("警告信息")
    # logger.error("错误信息")
    # logger.critical("严重错误信息")
    # my_function(0,0,0)
    logging.basicConfig()
    serve()