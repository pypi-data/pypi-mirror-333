import mysql.connector  # pip install mysql-connector-python
from.beiker_string import convert_coords_to_json

# 定义DatabaseQuery类，用于对数据库进行各种操作
class DatabaseQuery:
    def __init__(self, db):
        """
        类的构造函数，用于初始化DatabaseQuery类的实例。

        :param db: 数据库连接对象，类型为mysql.connector.connect()返回的对象，这个对象将被用于后续的数据库操作。
        """
        self.db = db
    def get_column_values(self, table, column_name, condition=None, id='id', batch=500):
        """
        从指定表中获取特定列的所有值，返回值为一个字典，键为主键id，值为column_name列的值。
    
        :param table: 表名，字符串类型。
        :param column_name: 列名，字符串类型，表示需要获取值的列的名称。
        :param condition: 可选参数，查询条件，字符串类型。
        :param id: 代表主键，默认是'id'。
        :param batch: 每次使用fetchmany获取的行数，默认是100行。
        :return: 一个字典，每个元素的键是主键id，每个元素的值是column_name列的值。
        """
        try:
            mycursor = self.db.cursor()
            select_query = f"SELECT {id}, {column_name} FROM {table}"
            if condition:
                select_query += f" WHERE {condition}"
            mycursor.execute(select_query)
            value_dict = {}
            rows = mycursor.fetchmany(batch)
            while rows:
                for row in rows:
                    value_dict[row[0]] = row[1]
                rows = mycursor.fetchmany(batch)
            return value_dict
        except Exception as err:
            return {str(err): None}
        
    def is_table_empty(self, table_name):  
        """ 检查指定的数据表是否为空。 """  
        cursor = self.db.cursor()  
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")  
        count = cursor.fetchone()[0]  
        cursor.close()  
        return count == 0  

    def get_table_row(self, table):
        """
        从指定的表中获取所有行的数据。

        :param table: 表名，字符串类型，表示要查询的数据库表的名称。
        :return: 返回查询到的所有行的数据，是一个包含元组的列表，每个元组代表一行数据。
        """
        mycursor = self.db.cursor()
        mycursor.execute("SELECT * FROM " + table)
        result = mycursor.fetchall()
        return result

    def get_table_structure(self, table):
        """
        获取指定表的结构，即列名。

        :param table: 表名，字符串类型，表示要查询结构的数据库表的名称。
        :return: 返回一个包含列名的列表，其中每个元素是一个字符串，表示表中的列名。
        """
        mycursor = self.db.cursor()
        mycursor.execute("SHOW COLUMNS FROM " + table)
        result = [x[0] for x in mycursor.fetchall()]
        return result

    def insert_row(self, table, data):
        """
        向指定的表中插入一行或多行数据。

        :param table: 表名，字符串类型，表示要插入数据的数据库表的名称。
        :param data: 要插入的数据，可以是一个字典（表示插入一行数据）或者一个字典列表（表示插入多行数据）。
        :return: 如果插入成功则返回True，如果发生异常则返回异常信息的字符串表示。
        """
        try:
            mycursor = self.db.cursor()
            if isinstance(data, list):
                # 如果是插入多行数据，获取列名并连接成字符串，例如 "col1, col2, col3"
                columns = ', '.join(data[0].keys())
                values_list = []
                for row_data in data:
                    # 对于每一行数据，将值转换为带引号的字符串并连接成括号内的值，例如 "(value1, value2, value3)"
                    values = ', '.join([f"'{v}'" for v in row_data.values()])
                    values_list.append(f"({values})")
                # 将所有行的值连接成一个字符串，例如 "(value1, value2, value3), (value4, value5, value6)"
                values_str = ', '.join(values_list)
            else:
                # 如果是插入一行数据，获取列名并连接成字符串
                columns = ', '.join(data.keys())
                # 将值转换为带引号的字符串并连接成括号内的值
                values = ', '.join([f"'{v}'" for v in data.values()])
                values_str = f"({values})"
            # 构建插入数据的SQL查询语句
            insert_query = f"INSERT INTO {table} ({columns}) VALUES {values_str}"
            mycursor.execute(insert_query)
            self.db.commit()
            return True
        except Exception as err:
            return str(err)

    def delete_row(self, table, condition=None, limit=None):
        """
        从指定的表中删除一行或多行数据。

        :param table: 表名，字符串类型，表示要删除数据的数据库表的名称。
        :param condition: 可选参数，删除数据的条件，字符串类型，表示SQL中的WHERE子句内容，如果不提供则删除所有行。
        :param limit: 可选参数，要删除的行数限制，整数类型，如果不提供则不限制删除的行数。
        :return: 如果删除成功则返回True，如果发生异常则返回异常信息的字符串表示。
        """
        try:
            mycursor = self.db.cursor()
            delete_query = f"DELETE FROM {table}"
            if condition:
                delete_query += f" WHERE {condition}"
            if limit:
                delete_query += f" LIMIT {limit}"
            mycursor.execute(delete_query)
            self.db.commit()
            return True
        except Exception as err:
            return str(err)

    def update_row(self, table, update_data, condition=None):
        """
        更新指定表中的一行或多行数据。

        :param table: 表名，字符串类型，表示要更新数据的数据库表的名称。
        :param update_data: 要更新的数据，是一个字典，键为列名，值为要更新的值。
        :param condition: 可选参数，更新数据的条件，字符串类型，表示SQL中的WHERE子句内容，如果不提供则更新所有行。
        :return: 如果更新成功则返回True，如果发生异常则返回异常信息的字符串表示。
        """
        try:
            mycursor = self.db.cursor()
            # 将更新数据构建成SQL中的SET子句内容，例如 "col1 = 'value1', col2 = 'value2'"
            set_values = ', '.join([f"{key} = '{value}'" for key, value in update_data.items()])
            update_query = f"UPDATE {table} SET {set_values}"
            if condition:
                update_query += f" WHERE {condition}"
            mycursor.execute(update_query)
            self.db.commit()
            return True
        except Exception as err:
            return str(err)

    def append_value(self, table, column, value_to_append, condition=None):
        """
        在指定表的指定列后追加一个值。

        :param table: 表名，字符串类型，表示要操作的数据库表的名称。
        :param column: 列名，字符串类型，表示要追加值的列的名称。
        :param value_to_append: 要追加的值，字符串类型，表示要追加到列后面的值。
        :param condition: 可选参数，操作的条件，字符串类型，表示SQL中的WHERE子句内容，如果不提供则对所有行进行操作。
        :return: 如果操作成功则返回True，如果发生异常则返回异常信息的字符串表示。
        """
        try:
            mycursor = self.db.cursor()
            if condition:
                update_query = f"UPDATE {table} SET {column} = CONCAT({column}, '{value_to_append}') WHERE {condition}"
            else:
                update_query = f"UPDATE {table} SET {column} = CONCAT({column}, '{value_to_append}')"
            mycursor.execute(update_query)
            self.db.commit()
            return True
        except mysql.connector.Error as err:
            return str(err)

    def exec_query(self, query):
        """
        执行一个自定义的SQL查询语句并返回结果。

        :param query: 要执行的SQL查询语句，字符串类型，表示任意合法的SQL查询语句。
        :return: 返回查询结果，是一个包含元组的列表，每个元组代表一行查询结果。
        """
        mycursor = self.db.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        return result

    def query_data(self, table, select_fields='*', condition=None):
        """
        从指定的表中查询指定字段的数据。

        :param table: 表名，字符串类型，表示要查询的数据库表的名称。
        :param select_fields: 可选参数，要查询的字段，字符串类型，默认为'*'表示查询所有字段，可以指定为逗号分隔的字段名列表，例如 "col1, col2"。
        :param condition: 可选参数，查询的条件，字符串类型，表示SQL中的WHERE子句内容，如果不提供则查询所有行。
        :return: 返回查询结果，是一个包含元组的列表，每个元组代表一行查询结果。
        """
        mycursor = self.db.cursor()
        select_query = f"SELECT {select_fields} FROM {table}"
        if condition:
            select_query += f" WHERE {condition}"
        mycursor.execute(select_query)
        result = mycursor.fetchall()
        return result

    def check_table_existence(self, table_name):
        """
        检查指定的表是否存在于数据库中。

        :param table_name: 表名，字符串类型，表示要检查是否存在的数据库表的名称。
        :return: 如果表存在则返回True，否则返回False。
        """
        mycursor = self.db.cursor()
        # 执行查询语句检查数据表是否存在，使用了占位符 %s 来防止SQL注入攻击
        mycursor.execute("SHOW TABLES LIKE %s", (table_name,))
        result = mycursor.fetchone()
        return bool(result)

    def begin_transaction(self):
        """
        开始数据库事务。
        """
        self.db.start_transaction()

    def commit_transaction(self):
        """
        提交数据库事务。
        """
        self.db.commit()

    def rollback_transaction(self):
        """
        回滚数据库事务。
        """
        self.db.rollback()
    def close_connection(self):
        """
        关闭数据库连接。

        :param self: 当前DatabaseQuery类的实例。
        :return: 无返回值。
        """
        if self.db:
            self.db.close()

def update_column(db_query,table,column,id='id',batch=500):
    '''
    将数据表中的[(x1,y1),(x2,y2),(x3,y3),(x4,y4)]转化成json数据形式{[x1,y1],[x2,y2],[x3,y3],[x4,y4]}
    '''
    # 假设db_query是一个databasequery类的实例
    db_query.begin_transaction()
    try:
        cursor = db_query.db.cursor()
        # 查询所有需要处理的数据行（这里查询所有的id和axes列数据）
        query = f"SELECT {id}, {column} FROM {table}"
        cursor.execute(query)
        pattern =r'\[\(\d+,\s*\d+\)(,\s*\(\d+,\s*\d+\))*\]'
        all_sub_json_results = {}
        while True:
            sub_json_results = {}
            sub_column_values={}
            # 按批次获取数据
            batch_data = cursor.fetchmany(batch)
            if not batch_data:
                break
            # print(batch_data)
            sub_column_values = {str(row[0]): row[1] for row in batch_data}
            # print(sub_column_values)
            for key, value in sub_column_values.items():
                if value:
                    match = re.fullmatch(pattern, value)
                    if match:
                        sub_json_results[key] = convert_coords_to_json(value)
                    else:
                        print("字符串格式不匹配.")
            all_sub_json_results.update(sub_json_results)            
        # print(all_sub_json_results)
    
        # 假设我们有一个包含所有更新操作的参数列表
        all_params = [(json_result, id) for id, json_result in all_sub_json_results.items()]
        
    
        # 准备更新语句
        update_query = f"UPDATE {table} SET {column} = %s WHERE {id} = %s"
        
        # 分批执行
        for i in range(0, len(all_params), batch):
            # 获取当前批次的参数
            batch_params = all_params[i:i + batch]
            # 执行批量更新
            cursor.executemany(update_query, batch_params)
            # 提交事务以确保当前批次的更新被保存
            db_query.commit_transaction()
            
    except Exception as e:
        print(f"查询或处理数据时出错: {e}")
        db_query.rollback_transaction()
    finally:
        cursor.close()
        db_query.close_connection()

def df_to_db(df, database_query, table_name, columns_list, key):
    """
    将 DataFrame 存入数据库表中。

    参数：
    - df：要存入数据库的 DataFrame。
    - database_query：DatabaseQuery 类的实例，用于操作数据库。
    - table_name：数据库表名称。
    - columns_list：对应数据库中的列名列表。
    - key：数据表中的列名，用于检查是否已存在该值。

    功能：
    1. 检查 DataFrame 的列名是否与传入的列名列表一致，如果不一致则抛出异常。
    2. 逐行将 DataFrame 的数据插入到数据库表中，但在插入前检查指定列的值是否已存在于数据库表中，如果存在则不插入该行数据。如果插入过程中出现错误，进行适当的错误处理。
    """
    df_columns = df.columns.tolist()
    if set(df_columns)!= set(columns_list):
        raise ValueError("DataFrame 的列名与传入的列名列表不一致。")

    try:
        for index, row in df.iterrows():
            data_dict = dict(zip(columns_list, row))
            # 检查指定列的值是否已存在于数据库表中
            value_dict = database_query.get_column_values(table_name, key)
            if data_dict[key] in value_dict.values():
                print(f"值 {data_dict[key]} 在数据库中已存在，跳过插入该行数据。")
                continue
            insert_result = database_query.insert_row(table_name, data_dict)
            if not insert_result:
                raise Exception(f"插入第 {index + 1} 行数据时出现错误：{insert_result}")
        return True
    except Exception as e:
        print(f"存入数据库时出现错误：{e}")
        return False
