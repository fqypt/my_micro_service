from peewee import *
from user_srv.settings import settings


class BaseModel(Model):
    class Meta:
        database = settings.DB


class User(BaseModel):
    # 用户模型
    GENDER_CHOICES = (
        ("female", "女"),
        ("male", "男")
    )

    ROLE_CHOICES = (
        (1, "普通用户"),
        (2, "管理员")
    )

    mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号码")
    password = CharField(max_length=100, verbose_name="密码")  # 密码设置要注意两点：密码需要是密文；密文不可被反解
    nick_name = CharField(max_length=20, null=True, verbose_name="昵称")
    head_url = CharField(max_length=200, null=True, verbose_name="头像")
    birthday = DateField(null=True, verbose_name="生日")
    address = CharField(max_length=200, null=True, verbose_name="地址")
    desc = TextField(null=True, verbose_name="个人简介")
    gender = CharField(max_length=6, choices=GENDER_CHOICES, null=True, verbose_name="性别")
    role = IntegerField(default=1, choices=ROLE_CHOICES, verbose_name="用户角色")


if __name__ == '__main__':
    settings.DB.create_tables([User])
    #加密方式：1、对称加密   2、非对称加密
    #md5
    # import hashlib
    # m = hashlib.md5()
    # salt = "gwoow"
    # password = "123456"
    # m.update((salt + password).encode("utf8"))
    # # 暴力破解 彩虹表
    # print(m.hexdigest())

    # from passlib.hash import pbkdf2_sha256
    # for i in range(10):
    #     user = User()
    #     user.nick_name = f"bobby{i}"
    #     user.mobile = f"1878222222{i}"
    #     user.password = pbkdf2_sha256.hash("admin123")
    #     user.save()
    #
    # for user in User.select():
    #     print(pbkdf2_sha256.verify("admin123",user.password))

    # 验证时间可以转化的伪代码：
    # for user in User.select():
    #     import time
    #     from datetime import date
    #     if user.birthday:
    #         print(user.birthday)   #2021-02-19
    #         u_time = int(time.mktime(user.birthday.timetuple()))
    #         print(u_time)   #1613664000
    #         print(date.fromtimestamp(u_time)) #2021-02-19

    #伪代码
    # users = User.select()
    # users = users.limit(2).offset(2)
    # for user in users:
    #     print(user.mobile)