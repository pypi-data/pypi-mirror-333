import random,re,json,os

def detect_missing_trailing_zeros(num_list):
    """
    检测列表中数字是否存在后面的 0 缺失的情况。

    参数:
    num_list (list): 待检测的数字字符串列表。

    返回:
    list: 包含存在后面的 0 缺失的元素位置的列表。
    """
    missing_zeros_positions = []
    try:
        # 遍历列表，除了最后一个元素
        for i in range(len(num_list) - 1):
            try:
                current = int(num_list[i])
                next_num = int(num_list[i + 1])
                # 若相邻数字不连续
                if next_num != current + 1:
                    temp = next_num
                    while True:
                        temp *= 10
                        if temp == current + 1:
                            missing_zeros_positions.append(i + 1)
                            break
                        if temp > current + 1:
                            break
            except ValueError:
                print(f"列表中的元素 '{num_list[i]}' 或 '{num_list[i + 1]}' 无法转换为整数，请检查输入。")
    except IndexError:
        print("输入列表为空，请检查输入。")
    return missing_zeros_positions
    
def check_extra_spaces(input_string):
    """
    检查输入字符串中是否存在多余的空格，如2000-XZ15.14   -8.0028。

    参数:
    input_string (str): 要检查的字符串。

    返回:
    bool: 如果存在多余的空格返回 True，否则返回 False。
    """
    # 容错处理：检查输入是否为字符串类型
    if not isinstance(input_string, str):
        print("输入不是有效的字符串，请检查输入。")
        return False

    # 使用正则表达式查找连续多个空格
    pattern = re.compile(r'\s{1,}')
    if pattern.search(input_string):
        return True

    return False

def convert_path_to_system_style(path, system_type):  
    """  
    根据指定操作系统类型，将路径转换为相应的格式。  

    :param path: 待转换的路径  
    :param system_type: 指定的操作系统类型 ('linux' 或 'windows')  
    :return: 转换后的路径  
    """  
    if system_type.lower() == 'windows':  
        # 将路径中的斜杠替换为反斜杠  
        return path.replace('/', '\\')  
    elif system_type.lower() == 'linux':  
        # 将路径中的反斜杠替换为斜杠  
        return path.replace('\\', '/')  
    else:  
        raise ValueError("system_type must be either 'linux' or 'windows'.")  
        
def convert_path_to_native_style(generic_path):  
    """  
    根据当前操作系统，将通用路径转换为原生路径样式。  

    :param generic_path: 通用格式的文件路径（使用正斜杠 / 作为分隔符）  
    :return: 转换后的文件路径  
    """  
    # 检查当前操作系统  
    if os.name == 'nt':  # Windows  
        # 将通用路径转换为Windows路径  
        native_path = generic_path.replace('/', '\\')  
    else:  # Linux, macOS, etc.  
        # 将通用路径转换为Linux/Unix路径  
        native_path = generic_path.replace('\\', '/')  
    return native_path  

def convert_coords_to_json(coords_str):
    """
    Convert a string of coordinates in the format "[(x1, y1), (x2, y2), ...]" to a JSON array.

    :param coords_str: A string representing a list of coordinates.
    :return: A JSON string representing the array of coordinates.
    """
    # 去除字符串中的括号并按逗号分割成列表
    points = coords_str.strip('[]').split('), (')

    # 初始化 JSON 数组
    json_array = []

    # 遍历每个坐标点，将其转换为 JSON 对象
    for point in points:
        # 移除多余的空格和括号，然后按逗号分割 x 和 y 值
        x, y = point.strip('()').split(',')
        # 将坐标点添加到 JSON 数组中
        json_array.append({"x": int(x), "y": int(y)})

    # 将数组转换为 JSON 字符串
    return json.dumps(json_array)

def remove_all_whitespaces(input_string):
    """
    去除字符串中所有不可见字符或空格。包括：
    空格 ' '：普通的空格字符。
    制表符 '\t'：通常用于文本对齐的字符。
    换行符 '\n'：在文本中开始新行的字符。
    回车符 '\r'：在某些文本环境中用于回到行的开头。
    换页符 '\f'：用于分隔页面的字符。
    垂直制表符 '\v'：在文本中创建垂直分隔的字符。
    """
    # 创建一个转换表，将所有空白字符映射到None
    return input_string.translate(str.maketrans('', '', ' \t\n\r\f\v'))

def is_labels_series(series, values=['男', '女'], labels=('性别', '未识别')):
    """
    检查Series是否在values列表中,如果在就返回True,并将labels第一个元素返回，否则返回False,并将labels第二个元素返回。
    如果Series为空，那么返回False,并返回labels的第二个元素。

    参数:
    series : pd.Series
        要检查的Series。
    values : list
        认为是labels标签的列表，默认为['男', '女']。
    labels : tuple
        包含两个元素的元组，第一个元素是Series在values中时返回的标签，第二个元素是Series不在values中时返回的标签。

    返回:
    tuple
        包含一个布尔值和一个标签。布尔值表示Series是否完全由values中的元素组成，标签是相应的labels元素。
    """
    # 检查Series是否为空
    if series.empty:
        return False, labels[1]
    
    unique_values = series.unique()
    is_subset = set(unique_values).issubset(set(values))
    return is_subset, labels[0] if is_subset else labels[1]

def contains_empty_string(lst):
    """
    检查列表中是否包含空字符串，并返回空字符串元素的位置列表。

    参数:
    lst : list
        要检查的列表。

    返回:
    tuple
        包含一个布尔值，指示列表中是否包含空字符串，以及一个列表，包含所有空字符串元素的位置。
    """
    empty_string_positions = [index for index, value in enumerate(lst) if value == '']
    contains_empty = bool(empty_string_positions)  # 如果位置列表不为空，则包含空字符串
    return contains_empty, empty_string_positions

def generate_unique_column_name(existing_names, base_name):  
    """  
    生成一个唯一的列名，如果base_name已经存在于existing_names中，则在末尾添加随机数字。  

    参数:  
    existing_names : list  
        已存在的列名列表。  
    base_name : str  
        基础列名。  

    返回:  
    str  
        唯一的列名。  
    """  
    new_name = base_name  
    while new_name in existing_names:  
        new_name = f"{base_name}_{random.randint(1, 99)}"  # 在基础列名后添加随机数字  
    return new_name  

def extract_str_from_pattern_in_json_list(json_list, pattern): 
    """
    用正则表达式从aliocr的json中的head和tail中获取匹配的字符串。
    """ 
    # 遍历每个条目  
    for entry in json_list:  
        # 在 head 中查找匹配  
        if 'head' in entry:  
            for item in entry['head']:  
                matches = re.findall(pattern, item)  
                if matches:  
                    # 如果找到匹配，返回结果  
                    return ' '.join(matches)  

        # 在 tail 中查找匹配  
        if 'tail' in entry:  
            for item in entry['tail']:  
                matches = re.findall(pattern, item)  
                if matches:  
                    # 如果找到匹配，返回结果  
                    return ' '.join(matches)  

    # 如果没有找到匹配，返回空字符串  
    return ''  

def extract_str_by_pattern(str, regular_pattern):
    """
    从给定字符串中根据正则表达式提取内容的函数。

    参数：
    - str：要进行内容提取的源字符串。
    - regular_pattern：用于提取内容的正则表达式。

    执行过程：
    1. 使用 re.findall 方法尝试在源字符串中查找与正则表达式匹配的所有内容。
    - re.findall 会返回一个列表，其中包含所有符合正则表达式的子字符串。
    2. 判断 matches 是否为空列表：
    - 如果 matches 不为空，表示在源字符串中找到了符合正则表达式的内容。
        - 返回 matches 列表中的第一个元素，即第一个符合正则表达式的子字符串。
    - 如果 matches 为空，表示在源字符串中没有找到符合正则表达式的内容。
        - 首先尝试打印错误信息，以便在出现问题时进行调试。这里假设正则表达式可能因为各种原因不正确或者字符串格式不符合预期。
        - 返回空字符串 ''，表示没有提取到任何内容。
    """
    try:
        matches = re.findall(regular_pattern, str)
        return matches[0] if matches else ''
    except Exception as e:
        print(f"An error occurred while extracting with pattern {regular_pattern}: {e}")
        return ''
    
def extract_archive_class(s):
    """
    从给定的字符串中提取出jx13.12或jx13.gz或jx13.hz0这样的档案分类号，不区分大小写。

    参数：
    - s：一个字符串。

    返回值：
    - 如果找到符合条件的内容，返回提取出的内容；否则返回空字符串。
    """

    pattern = r'([a-zA-Z]{2}\d{2}(\.\d{2}|\.[A-Za-z]{2}\d?))'

    matches = re.findall(pattern, s)
    if matches:
        return matches[0][0]
    return ''

def extract_archive_code(s):
    """
    从给定的字符串中提取出2019-JX13.17-1或2019-JX13.17-1.1这样的档号，不区分大小写。

    参数：
    - s：文件名列表。

    返回值：
    - 匹配的内容或者空字符串。
    """
    # 定义正则表达式来匹配特定格式（1950 - JX11.44 - 10形式）的字符，用于从文件路径中获取archiveCode
    pattern = r'((19|20)\d{2}-[a-zA-Z]{2}\d{2}(\.\d{2}|\.[A-Za-z]{2}\d?)(-\d{1,4})(\.\d{1,4})?)'
    matches = re.findall(pattern, s)
    if matches:
        return matches[0][0]
    return ''

def split_list_by_length(lst, length):
    '''
    对列表按指定长度进行截取。返回的是一个二元列表。
    '''
    result = []
    for i in range(0, len(lst), length):
        result.append(lst[i:i + length])
    return result

def extract_file_archive_code(s):
    """
    从给定的字符串中提取案卷档号2019-JX13.17-1，不区分大小写。

    参数：
    - s：文件名列表。

    返回值：
    - 匹配的内容或者空字符串。
    """
    # 定义正则表达式来匹配特定格式（1950 - JX11.44 - 10形式）的字符，用于从文件路径中获取archiveCode
    pattern = r'((19|20)\d{2}-[a-zA-Z]{2}\d{2}(\.\d{2}|\.[A-Za-z]{2}\d?)(-\d{1,4}))'
    matches = re.findall(pattern, s)
    if matches:
        return matches[0][0]
    return ''