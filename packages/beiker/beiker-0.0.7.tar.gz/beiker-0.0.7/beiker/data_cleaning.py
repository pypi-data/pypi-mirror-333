import numpy as np
from scipy.interpolate import interp1d
from.beiker_string import generate_unique_column_name
import pandas as pd


def linear_interpolation(arr):
    """
    数组由一系列连续的数字组成，但个别位置可能是None或空字符串，用线型插值的方法补全。
    """
    # 将数组转换为浮点数类型，并将空字符串和None转换为numpy.nan
    arr = np.array([float(x) if x != '' and x is not None else np.nan for x in arr])

    # 找出所有非缺失值的索引和对应的值
    non_missing = ~np.isnan(arr)
    x = np.arange(len(arr))[non_missing]
    y = arr[non_missing]

    # 确保至少有两个非缺失值来构建插值函数
    if len(x) < 2:
        raise ValueError("至少需要两个非缺失值来构建插值函数")

    # 创建线性插值函数
    interp_func = interp1d(x, y, kind='linear', bounds_error=False, fill_value='extrapolate')

    # 对整个数组进行插值
    interpolated_arr = interp_func(np.arange(len(arr)))

    return interpolated_arr

def check_for_discontinuities(s):
    # 将Series中的None替换为NaN
    s = s.fillna(np.nan)
    
    # 尝试将Series转换为数值类型，非数字将变为NaN
    numeric_s = pd.to_numeric(s, errors='coerce')
    
    # 计算连续数字之间的差异
    diffs = numeric_s.diff().abs()
    
    # 找出差异大于1的位置，这可能是突变的位置
    jumps = diffs[diffs > 1].index
    
    # 找出NaN的位置，即原始数据中None的位置
    non_numeric = s.isna()
    
    # 找出非数字字符的位置
    non_numeric |= s.apply(lambda x: isinstance(x, str) and x.isdigit() == False)
    
    # 将突变的位置、NaN的位置和非数字字符的位置合并
    issues = non_numeric.astype('object') | jumps.to_series().astype('object')

    # 检查是否存在问题
    if issues.any():
        # 创建一个新的Series，将有问题的位置替换为''
        clean_s = s.copy()
        clean_s[issues] = ''
        # 返回False，有问题的数据，以及清理后的s
        return False, s[issues], clean_s
    else:
        # 如果没有发现问题，返回True和原始数据
        return True, s, s
    
def check_column_names(df, column_function_dict):  
    """  
    检查并更新DataFrame的列名，确保新列名唯一。  
    使用时要 import pandas as pd ，from functools import partial  
    参数:  
    df : pandas.DataFrame  
        需要检查和更新列名的DataFrame。  
    column_function_dict : dict  
        一个字典，其中键为列索引，值为处理函数。处理函数用于检查列数据并返回新的列名。字典格式如下：  
    column_function_dict = {  
        1: partial(is_labels_series, values=['男', '女'], labels=('性别', '未识别')),  
    }
    返回:  
    tuple  
        返回一个元组，包含更新后的DataFrame和新的列名列表。  
    """  

    # 创建新的列名列表，初始为DataFrame的当前列名  
    new_column_names = df.columns.tolist()  
    
    # 遍历列索引和对应的处理函数  
    for column_index, function in column_function_dict.items():  
        # 检查列索引是否在DataFrame的有效范围内  
        if column_index < len(df.columns):  
            # 获取指定列的数据作为Series  
            series = df.iloc[:, column_index]  
            
            # 调用处理函数，返回是否为子集的布尔值和新的列名  
            is_subset, label = function(series)  
            
            # 生成唯一的列名，确保新列名不与现有列名重复  
            unique_label = generate_unique_column_name(new_column_names, label)  
            
            # 更新新的列名列表中的对应列名  
            new_column_names[column_index] = unique_label  

    # 将DataFrame的列名更新为新的列名列表  
    df.columns = new_column_names  
    
    # 返回更新后的DataFrame和新的列名列表  
    return df, new_column_names

def merge_columns_to_dict_series(df, columns, new_column_name):
    """
    将给定列的数据合并成字典，并创建一个新列存储这些字典的字符串表示。

    参数:
    df : pd.DataFrame
        要处理的DataFrame。
    columns : list
        要合并的列名列表。
    new_column_name : str
        新列的列名，用于存储字典的字符串表示。

    返回:
    pd.DataFrame
        更新后的DataFrame。
    """
    # # 确保新列名不在列名列表中
    # if new_column_name in columns:
    #     raise ValueError(f"新列名 '{new_column_name}' 不能在给定列中。")
    
    # 将每一行的给定列数据合并成字典
    df[new_column_name] = df[columns].apply(lambda row: {col: row[col] for col in columns}, axis=1)
    
    # 将字典转换为字符串形式
    df[new_column_name] = df[new_column_name].apply(lambda d: str(d))
    
    # 删除给定列
    df.drop(columns=columns, axis=1, inplace=True)
    
    return df

def remove_columns_duplicates(df, columns, empty_flag=True):
    """
    删除DataFrame中指定列中的重复行，可选择忽略空值。

    参数:
    df : pd.DataFrame
        要处理的DataFrame。
    columns : list
        需要检查重复值的列名列表。
    empty_flag : bool, 默认为True
        如果为True，不处理单元格值为空的行。

    返回:
    pd.DataFrame
        删除重复行后的DataFrame。
    """
    # 创建一个副本，以免修改原始DataFrame
    df = df.copy()

    # 检查每一列是否有重复值，如果有，则只保留第一个出现的行
    for col in columns:
        # 去重前先找出所有重复项的索引
        duplicated = df.duplicated(subset=col, keep=False)
        if empty_flag:
            # 仅处理非空值
            duplicated &= df[col].notna()
        # 反向索引，即保留重复项和非空值项，删除其他项
        df = df[~duplicated]
        
        # 由于删除了重复项，需要重置索引
        df.reset_index(drop=True, inplace=True)
        
    return df