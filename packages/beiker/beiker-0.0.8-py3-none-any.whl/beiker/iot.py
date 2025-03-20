import barcode  # pip install python-barcode  
from barcode.writer import ImageWriter  
from PIL import Image  
import os  

def convert_to_hex_ascii(s):
    '''
    将某个字符串转化为ascii值的16进制，每个字符是两个字节。
    '''
    hex_list = []
    for char in s:
        if char.isalnum() or char in ['-', '.','~']:
            hex_value = hex(ord(char))[2:].zfill(2)
            hex_list.append(hex_value)
    return "".join(hex_list)
    
def hex_ascii_to_string(hex_str):
    '''
    convert_to_hex_ascii的反向函数，将16进制数字转化为字符串。
    '''
    string = ""
    for i in range(0, len(hex_str), 2):
        hex_pair = hex_str[i:i + 2]
        char_code = int(hex_pair, 16)
        string += chr(char_code)
    return string

def string_to_barcode_jpg(string, output_filename, font_size=11.5,text_distance=7,module_height=0.05,output_width=500, output_height=100):  
    """  
    生成指定尺寸的条形码并保存为 JPG 文件。  

    :param string: 要编码的字符串  
    :param output_filename: 输出文件名  
    :param output_width: 输出图像宽度（以像素为单位）  
    :param output_height: 输出图像高度（以像素为单位）  
    """  

    # 使用 ImageWriter 生成条形码图像  
    code_format = barcode.get_barcode_class('code128')  
    writer = ImageWriter()  
    
    # 设置 writer_options，包括字体大小和条形码高度  
    writer_options = {  
        'font_size': font_size,  # 设置字体大小  
        'text_distance': text_distance,  # 字符串与条形码之间的距离 ，字符串上沿与条形码上沿的距离
        'module_height': output_height * module_height,  # 设置条形码的高度 (调整为合适的比例)  
    }  

    code = code_format(string, writer=writer)  
    
    # 生成临时 PNG 文件并应用 writer_options  
    png_filename = 'temp_barcode'  
    png_with_extension = png_filename + r'.png'  
    
    try:  
        code.save(png_filename, options=writer_options)  # 使用 writer_options 保存  

        # 检查 PNG 文件是否成功创建  
        if not os.path.exists(png_with_extension):  
            print(f"Error: Failed to create {png_with_extension}.")  
            return  

        # 使用 Pillow 读取 PNG 文件并调整其大小  
        with Image.open(png_with_extension) as img:  
            img = img.resize((output_width, output_height), Image.LANCZOS)  
            img.convert('RGB').save(output_filename, 'JPEG')  # 保存为 JPG  
    except Exception as e:  
        print(f"Error: {e}")  
    finally:  
        # 清理临时 PNG 文件  
        if os.path.exists(png_with_extension):  
            os.remove(png_with_extension)  