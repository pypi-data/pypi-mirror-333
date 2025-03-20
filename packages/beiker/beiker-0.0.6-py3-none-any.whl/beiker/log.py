import logging,datetime,os

def configure_logging(log_file_path, info):
    """
    此函数用于配置日志记录器并记录一条信息日志。

    :param log_file_path: 日志文件的路径，字符串类型，指定了日志将被记录到哪个文件中。
    :param info: 要记录的信息内容，字符串类型，表示要记录到日志中的具体信息。

    函数内部逻辑如下：
    1. 首先使用 `logging.basicConfig` 函数来配置日志记录器。
       - `filename=log_file_path`：指定日志文件的路径。
       - `level=logging.INFO`：设置日志记录级别为INFO，这意味着INFO级别及更高级别（如WARNING、ERROR）的日志消息将被记录。
       - `format='%(asctime)s - %(levelname)s - %(message)s'`：定义了日志消息的格式，其中包括时间戳、日志级别和具体消息内容。
       - `encoding='utf-8'`：指定日志文件的编码为UTF - 8。
    2. 然后使用 `logging.info` 函数记录传入的信息内容。
    """
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    logging.info(info)

def printLog(*args, **kwargs):
    """
    此函数用于将信息同时打印到控制台和日志文件中。

    :param *args: 可变参数，表示要打印和记录的信息内容，可以是多个不同类型的参数，这些参数将被转换为字符串并拼接在一起。
    :param **kwargs: 关键字参数，用于传递给 `print` 函数的其他参数，例如 `end`、`sep` 等。

    函数内部逻辑如下：
    1. 首先将可变参数 `*args` 中的所有元素转换为字符串并使用空格拼接在一起，得到要打印和记录的日志消息 `log_message`。
    2. 使用 `print` 函数将日志消息打印到控制台，同时传递 `**kwargs` 中的其他参数（如果有）。
    3. 使用 `with open` 语句以追加模式（'a'）打开名为 'log.log' 的日志文件，编码为 'utf - 8'。
       - 在文件中写入当前的日期和时间（`str(datetime.datetime.now())`）以及日志消息，并添加换行符（`'\n'`）。
    """
    try:
        # 检查 log.log 文件大小，如果超过 2M 就删除文件
        if os.path.exists('log.log'):
            file_size = os.path.getsize('log.log')
            if file_size > 2 * 1024 * 1024:
                os.remove('log.log')
        log_message = " ".join(map(str, args))
        print(log_message, **kwargs)
        with open('log.log', 'a', encoding='utf-8') as file:
            file.write(str(datetime.datetime.now()) + " " + log_message + '\n')
    except Exception as e:
        print(f"An error occurred: {e}")