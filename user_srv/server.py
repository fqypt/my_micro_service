import sys
import os
import signal
from concurrent import futures
import logging

import grpc
from loguru import logger
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, BASE_DIR)

from user_srv.proto import user_pb2_grpc
from user_srv.handler.user import UserServicer


# 定义退出函数
def on_exit(signo, frame):
    logger.info("进程中断")
    sys.exit(0)


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',
                        nargs="?",
                        type=str,
                        default="127.0.0.1",
                        help="binding ip"
                        )
    parser.add_argument('--port',
                        nargs="?",
                        type=int,
                        default=50051,
                        help="the listening port"
                        )
    args = parser.parse_args()



    # 配置文件输出
    logger.add("logs/user_srv_{time}.log")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    server.add_insecure_port(f"{args.ip}:{args.port}")

    # 主进程退出信号监听
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    logger.info(f"启动服务：{args.ip}:{args.port}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
