import mysql.connector
from.database import DatabaseQuery

# 定义bbt类，其中包含一个静态方法make，用于创建不同类型的对象（目前只用于创建DatabaseQuery对象）
class bbt:
    @staticmethod
    def make(obj_type, *args, **kwargs):
        """
        静态方法，根据传入的对象类型创建相应的对象。

        :param obj_type: 要创建的对象类型，字符串类型，目前只支持 "DatabaseQuery"。
        :param args: 可变参数，用于传递创建对象所需的位置参数，例如数据库连接所需的主机名、用户名等。
        :param kwargs: 关键字参数，用于传递创建对象所需的关键字参数，例如数据库连接所需的密码等。
        :return: 如果obj_type为 "DatabaseQuery"，则返回一个DatabaseQuery类的实例；否则抛出ValueError异常。
        """
        if obj_type == "DatabaseQuery":
            db = mysql.connector.connect(*args, **kwargs)
            return DatabaseQuery(db)
        # 如果需要创建其他类型的对象，可以在这里添加更多的elif条件
        else:
            raise ValueError("Invalid object type")