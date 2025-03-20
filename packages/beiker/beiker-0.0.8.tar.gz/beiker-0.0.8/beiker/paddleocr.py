from.files import read_json_file,check_file_existence,check_create_folder,find_ori_files_from_json,delete_file,save_df_with_links,text_to_docx,split_path
from.beiker_string import extract_str_by_pattern,extract_archive_class,convert_path_to_system_style
import pandas as pd
import os,re,io,json,datetime
from PIL import Image
from.log import printLog
# from functools import partial  
# from.safe import decrypt_simple
# from openpyxl import load_workbook  
# from openpyxl.utils.dataframe import dataframe_to_rows
import numpy as np
import paddle
from paddleocr import PaddleOCR
# from paddleocr import draw_ocr

def ocr_build_other_filepath(file_path, ocr_model='ali'):
    '''
    根据文件路径生成ocr识别json路径，table、cell、content、table-content路径。
    '''
    try:
        # 获取文件名（带扩展名）
        filename = os.path.basename(file_path)

        # 分离文件名和扩展名
        filename_without_extension, file_extension = os.path.splitext(filename)

        # 定义基础目录
        base_dir = os.path.dirname(file_path)
        other_dir = base_dir  # 默认为基础目录
        file_path=file_path.replace('\\', '/')

        # 如果文件扩展名是 json，调整目录和文件名处理
        if file_extension.lower() == '.json':
            ori_full_name=find_ori_files_from_json(file_path)
            ori_filename = ori_full_name[0]
            filename_without_extension,_= os.path.splitext(ori_full_name[1])
        elif file_extension.lower() in ['.jpg','.jpeg','.tif','.tiff']:
            # 定义其他文件的目录
            other_dir = os.path.join(base_dir, 'other')
            ori_filename = file_path

        else:
            print('ocr_build_other_filepath 不支持的文件格式。')
            return None
        if ocr_model == 'paddle':
            filename_without_extension = f'{filename_without_extension}-paddle'
        elif ocr_model=='ali':
            filename_without_extension = f'{filename_without_extension}-ali'
        else:
            print('ocr_build_other_filepath 不支持的ocr Model。')
            return None
        # 构建其他文件路径
        json_filename = os.path.join(other_dir, f'{filename_without_extension}-json.json')
        table_filename = os.path.join(other_dir, f'{filename_without_extension}-table.xlsx')
        cell_filename = os.path.join(other_dir, f'{filename_without_extension}-cell.xlsx')
        content_filename = os.path.join(other_dir, f'{filename_without_extension}-content.docx')
        table_content_filename = os.path.join(other_dir, f'{filename_without_extension}-table_content.xlsx')
        log_filename = os.path.join(other_dir, 'aliocr-log.xlsx')
        if ocr_model == 'paddle':
            log_filename = os.path.join(other_dir, 'paddleocr-log.xlsx')

        # 返回生成的文件路径
        return ori_filename, json_filename, table_filename, cell_filename, content_filename, log_filename, table_content_filename
    except Exception as e:
        print(f"ocr_build_other_filepath-An error occurred: {e}")
        return None
    
def paddleocr_extract_word_from_jsondata(json_data):
    '''
    将paddleocr识别的json数据转化为字符串，json_data是paddle识别后的原始json对象。
    '''

    extracted_texts=[]
    for h in json_data:
        for i in h:
            extracted_texts.append(str(i[1][0]))
    result=" ".join(extracted_texts) 
    return result

def paddle_image_to_json(filepath,fp_setting=None,other_dir='other'):
    """
    用 PaddleOCR 将 image 识别为 json 数据。
    fp_setting是配置文件路径，暂时不用。

    参数：
    - filepath (str): 要进行 OCR 识别的图像文件路径。
    - json_file_path (str, optional): 可选参数，保存结果的 JSON 文件路径。如果为 None，则不保存到文件。
    - gpu (bool): 是否使用 GPU 进行计算。
    - use_angle_cls (bool): 是否使用角度分类器。
    - lang (str): 识别的语言，默认为'ch'（中文）。
    - show_log (bool): 是否显示日志信息。
    - other_dir: 保存路径

    返回：
    - result (list): OCR 识别的结果列表。

    功能描述：
    1. 根据 gpu 参数设置设备为 GPU 或 CPU。
    2. 初始化 PaddleOCR 对象，设置相关参数。
    3. 进行 OCR 识别。
    4. 如果提供了 json_file_path，则将结果保存到文件中。
    """
    filepath = os.path.abspath(filepath) # file的绝对路径
    fn = os.path.basename(filepath)
    filename_without_extention=os.path.splitext(fn)[0] # file不带扩展名的名称
    if other_dir=='other':
        other_path=check_create_folder(os.path.join(os.path.dirname(filepath),other_dir)) # file所在文件夹下的other文件夹
    else:
        other_path=other_dir

    json_file_name=filename_without_extention+"-paddle-json.json" # json文件夹下的json文件名

    full_jsonfile_path=os.path.join(other_path,json_file_name) # json文件完整路径

    gpu=False
    use_angle_cls=True
    lang='ch'
    show_log=False
    try:
        os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE" #加入这段代码可以解决使用paddleocr时内核重启的问题
        # 学习网址 https://paddlepaddle.github.io/PaddleOCR/ppocr/quick_start.html#221
        # 或者可以尝试conda uninstall jupyter tornado  然后重新安装conda install jupyter 

        # 这里的环境变量 KMP_DUPLICATE_LIB_OK 是特定于Intel的Math Kernel Library (MKL) 的。MKL是用于科学计算的一系列例程，它被许多数据处理和机器学习库所使用，包括NumPy和一些深度学习框架。

        # 在某些情况下，如果你的系统中安装了多个版本的MKL或者其他与MKL相关的库，可能会出现动态链接库（DLL）冲突的问题。这可能会导致程序在运行时抛出错误，比如“已加载重复的MKL库”之类的消息。

        # 通过设置环境变量 KMP_DUPLICATE_LIB_OK 为 TRUE，你可以告诉程序忽略这些冲突，允许加载多个MKL库的副本。这通常是一种临时解决方案，用于在不解决底层库冲突的情况下让程序运行。
        if check_file_existence(full_jsonfile_path):
            print(f'{filepath}已存在。')
            return []
        if gpu:
            # 设置使用 GPU
            try:
                paddle.set_device('gpu')
            except paddle.fluid.core.EnforceNotMetError as e:
                # 如果设置 GPU 失败，输出错误信息并改为使用 CPU
                print(f"无法使用 GPU，错误信息：{e}. 改为使用 CPU。")
                paddle.set_device('cpu')
        
        # 初始化模型，使用指定语言识别
        ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang, show_log=show_log)

        # 进行 OCR 识别
        json_data = ocr.ocr(filepath, cls=True)
        
        if full_jsonfile_path is not None:
            # 可以选择将结果保存到文件
            try:
                with open(full_jsonfile_path, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(json_data, ensure_ascii=False))
                    print(f"paddle_image_to_json - json文件保存到：{full_jsonfile_path}")
            except IOError as e:
                print(f"保存结果到文件时出现错误：{e}")
        return json_data
        
    except Exception as e:
        print(f"发生未知错误：{e}")
        return []
    
def paddleocr_json_to_df_refine(json_pending_data,json_filepath):
    '''
    json_pending_data是函数paddle_image_to_json的返回值。
    '''

    clean_df=pd.DataFrame()
    cell_df=pd.DataFrame()

    words=paddleocr_extract_word_from_jsondata(json_pending_data)

    # 定义正则表达式模式,提取著录信息
    year_pattern = r"((?:19|20)\d{2})(?:年|普|.*名册|\-)" 
    province_pattern=r'(北京|天津|上海|重庆|河北|山西|内蒙古|辽宁|吉林|黑龙江|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南|广东|海南|四川|贵州|云南|陕西|甘肃|青海|台湾|广西|西藏|宁夏|新疆|香港|澳门|华侨港澳台|港澳台)(?:学生|.*名册|壮族|回族|维吾尔|维尔|省|自治区|市)'
    admission_pattern=r'(\S+科\S+批|\S批|批次\S+|\S+阶段|\S+类\S+|层次\S+|\S+专项|\S+计划|\科类S+)'
    province=extract_str_by_pattern(json_filepath,province_pattern)
    year=extract_str_by_pattern(words,year_pattern)
    admission_batch = extract_str_by_pattern(words, admission_pattern)  

    if province is None or province=='':
        province=extract_str_by_pattern(json_filepath,province_pattern)

    if year is None or year=='':
        year=extract_str_by_pattern(json_filepath,year_pattern)

    content_df_data = {'province': province, 'year': year, 'admission_batch':admission_batch,'content':words,'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    content_df = pd.DataFrame(data=[content_df_data])

    return clean_df,cell_df,content_df

def paddleocr_json_to_file(paddleocr_json_data,filenames,json_filepath,table_flag=False,cell_flag=False,content_flag=True,content_type='gklqmc'):
    '''
    将json数据转化为table/cell/content文件。table可以直接查询或存入数据库，cell是表格单元格详细信息，可进一步对表格进行自动处理，如遮盖选定行或列，content就是表格中所有信息文本word文件，可用来进行粗略查询。
    log_fields = ['file_path', 'json_flag', 'table_flag', 'cell_flag','table_content_log_flag', 'content_flag','db_flag','json_path','table_path','cell_path','table_content_path','content_path','log_at']
    '''
    printLog(f"paddleocr_json_to_file 开始转换 {filenames[1]} ")


    table_df,cell_df,content_df=paddleocr_json_to_df_refine(paddleocr_json_data,json_filepath)

    # 定义正则表达式来匹配特定格式（1950 - JX11.44 - 10形式）的字符，用于从文件路径中获取archiveCode
    archive_code_pattern = r'\d{4}-[A-Za-z0-9]{2}\d{2}\.[A-Za-z0-9]{2}-\d+'
    # 使用正则表达式在filepath中进行匹配，获取匹配到的archiveCode
    archiveCode = re.search(archive_code_pattern, filenames[0]).group(0) if re.search(archive_code_pattern, filenames[0]) else ""
    table_df['archiveCode']=archiveCode
    cell_df['archiveCode'] = archiveCode
    archiveClass=extract_archive_class(archiveCode)
    table_df['archiveClass']=archiveClass

    relative_path=split_path(filenames[0], 'da')
    linux_filepath= convert_path_to_system_style(relative_path,'linux')
    table_df['filePath'] = linux_filepath
    # 在DataFrame的第一列插入文件路径列
    cell_df.insert(loc=0, column='filePath', value=linux_filepath)

    json_log_flag=0
    table_log_flag=0
    cell_log_flag=0
    table_content_log_flag=0
    content_log_flag=0
    db_log_flag=0

    try:

        if content_flag==True:
            content_df['type']=content_type
            content_df['filePath']=linux_filepath
            content_df['fullPath_link']=filenames[0]
            content_df['archiveCode']=archiveCode
            content_df['archiveClass']=archiveClass
            content_df.to_excel(filenames[6], index = False)

            printLog(f"paddleocr_json_to_file处理完成： {filenames[6]} ")
            table_content_log_flag=1

    except Exception as e:
        printLog(f"paddleocr_json_to_file转换 table_content 发生错误：{e}")

    try:

        if content_flag==True:

            text_to_docx(filenames[4],str(content_df['content'].iloc[0]),head='')

            printLog(f"paddleocr_json_to_file转换 content： {filenames[4]} ")
            content_log_flag=1

    except Exception as e:
        printLog(f"paddleocr_json_to_file转换 content 发生错误：{e}")

    try:

        if table_flag==True:
            table_df.to_excel(filenames[2], index = False)
            printLog(f"paddleocr_json_to_file处理完成： {filenames[2]} ")
            table_log_flag=1
    except Exception as e:
        printLog(f"paddleocr_json_to_file转换 table 发生错误：{e}")

    try:

        if cell_flag==True:
            cell_df.to_excel(filenames[3], index = False)
            printLog(f"paddleocr_json_to_file处理完成： {filenames[3]} ")
            cell_log_flag=1
    except Exception as e:
        printLog(f"转换 cell 发生错误：{e}")
    check_json=check_file_existence(filenames[1])

    if check_json:
        json_log_flag=1
    printLog(f"paddleocr_json_to_file 处理完成. ")
    log_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return [convert_path_to_system_style(filenames[0],'linux'), json_log_flag, table_log_flag, cell_log_flag, table_content_log_flag,content_log_flag,db_log_flag,filenames[1],filenames[2], filenames[3],filenames[6],filenames[4],log_at]

def paddleocr_json_to_file_with_log(file_paths,table_flag=False,cell_flag=False,content_flag=True):
    '''
    file_paths是json文件路径列表。
    log_dict格式是{源文件名1:log_df_row,源文件名2:log_df_row}，其中log_df_row是函数paddleocr_json_to_file的返回值，是一个源文件的log记录。
    '''
    log_dict={}
    process_num=1
    total_files=len(file_paths)
    printLog(f"文件总数：{total_files}")
    for file_path in file_paths:
        printLog(f"paddleocr_json_to_file_with_log 开始处理：")
        try:
            ocr_json_data=read_json_file(file_path)
            filenames=ocr_build_other_filepath(file_path,'paddle')

            log_df_row=paddleocr_json_to_file(ocr_json_data,filenames,file_path,table_flag,cell_flag,content_flag)
            
            log_path=filenames[5]
            # 检查键是否存在，如果不存在则添加键及其初始值
            if log_path not in log_dict:
                log_dict[log_path] = [log_df_row]
            else:
                # 向键对应的二维数组添加新的子列表
                log_dict[log_path].append(log_df_row)
            printLog(f"进度: {process_num}/{total_files}")
            process_num+=1
        except Exception as e:
            printLog(f"paddleocr_json_to_file_with_log 发生错误：{e}")
            process_num+=1

    paddleocr_log(log_dict)    

def paddleocr_log(log_dict):
    '''
    log_dict格式是{源文件名1:log_df_row,源文件名2:log_df_row}，其中log_df_row是函数paddleocr_json_to_file的返回值，是一个源文件的log记录。
    '''
    log_fields = ['file_path', 'json_flag', 'table_flag', 'cell_flag','table_content_log_flag', 'content_flag','db_flag','json_path','table_path','cell_path','table_content_path','content_path','log_at']
    
    # 遍历字典
    for fp, values in log_dict.items():
    
        # 将二维数组转换为DataFrame，并指定列名
        if not values:  # 检查是否有数据
            continue
        new_data = pd.DataFrame(values, columns=log_fields)
    
        # 检查文件是否存在
        if check_file_existence(fp):
            # 文件存在，读取文件
            log_df = pd.read_excel(fp)
            # 删除列名后缀有 '_Link' 的列
            log_df = log_df.loc[:, ~log_df.columns.str.endswith('_Link')]
            # 检查待插入的数据是否已经存在
            for index, row in new_data.iterrows():
                if not log_df[log_df['file_path'] == row['file_path']].empty:
                    printLog(f"数据已存在，将进行覆盖：{row['file_path']}")
                    # 获取匹配的行的索引
                    match_index = log_df[log_df['file_path'] == row['file_path']].index[0]
                    # 更新匹配的行
                    log_df.loc[match_index, :] = row
                else:
                    log_df = pd.concat([log_df, row.to_frame().T], ignore_index=True)
            
            delete_file(fp)
        else:
            # 文件不存在，使用新的DataFrame
            log_df = new_data
        
        path_columns=['file_path','json_path','table_path','cell_path','table_content_path','content_path']
        save_df_with_links(log_df, path_columns, fp)
        printLog(f"log 文件已生成：{fp} ")

def display_rectangle_in_image(json_data, image_path, save_to_image_path=None):
    '''
    将paddleocr识别出来的矩形框画到图像上。
    '''
    try:
        result = json_data[0]
        image = Image.open(image_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, font_path='./fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        if save_to_image_path is not None:
            im_show.save(save_to_image_path)
    except Exception as e:
        print(f"An error occurred: {e}")

def check_ocr_file_existence(filenames):
    '''
    检查文件的 ocr 识别处理文件是否存在。
    filenames 是 ocr_build_other_filepath 的返回值。
    '''
    # 初始化标志变量为默认值
    json_log_flag = 0
    table_log_flag = 0
    cell_log_flag = 0
    content_log_flag = 0
    table_content_log_flag = 0
    json_size_flag = 0

    # 检查文件名列表是否为空
    if not filenames:
        return filenames[0], filenames[1], json_log_flag, table_log_flag, cell_log_flag, content_log_flag, table_content_log_flag, json_size_flag

    # 检查每个文件名对应的文件是否存在
    try:
        check_json = check_file_existence(filenames[1])
        check_table = check_file_existence(filenames[2])
        check_cell = check_file_existence(filenames[3])
        check_content = check_file_existence(filenames[4])
        check_table_content = check_file_existence(filenames[6])
    except IndexError:
        # 如果索引超出范围，说明文件名列表不完整，直接返回默认值
        return filenames[0], filenames[1], json_log_flag, table_log_flag, cell_log_flag, content_log_flag, table_content_log_flag, json_size_flag

    # 如果文件存在，进行后续处理
    if check_json:
        json_log_flag = 1
        # 尝试获取文件大小（以字节为单位）
        try:
            file_size = os.path.getsize(filenames[1])
            # 10KB 的字节数
            paddlejson_file_limit_kb = 10 * 1024
            if file_size <= paddlejson_file_limit_kb:
                json_size_flag = 0
            else:
                json_size_flag = 1
        except OSError:
            # 如果获取文件大小出错，设置标志为 0
            json_size_flag = 0

    table_log_flag = 1 if check_table else 0
    cell_log_flag = 1 if check_cell else 0
    content_log_flag = 1 if check_content else 0
    table_content_log_flag = 1 if check_table_content else 0

    return filenames[0], filenames[1], json_log_flag, table_log_flag, cell_log_flag, content_log_flag, table_content_log_flag, json_size_flag

def check_ocr_result_save_to_excel(filepaths, ocr_model='ali'):
    '''
    filenames的格式如下：
    ori_filename, json_filename, table_filename, cell_filename, content_filename, log_filename, table_content_filename
    '''
    column_names = ['fileName', 'jsonName','json_flag', 'table_flag', 'cell_flag', 'content_flag', 'table_content_flag','json_size_flag']
    df = pd.DataFrame()
    for f in filepaths:
        filenames = ocr_build_other_filepath(f, ocr_model)
        result = check_ocr_file_existence(filenames)
        temp_df = pd.DataFrame([result], columns=column_names)
        df = pd.concat([df, temp_df], ignore_index=True)
    return df



