from PIL import Image, ImageDraw

def get_image_file_size(image_obj):  
    """  
    获取Image对象对应的图像文件大小，ocr识别图像应小于10240KB  

    Args:  
        image_obj (BufferedReader): 已通过 open(filepath, 'rb') 打开的文件对象  

    Returns:  
        int: 图像文件的大小，单位为KB  
    """  
    
    # 首先获取当前文件指针位置，这会返回已读取的字节数  
    current_position = image_obj.tell()  # 获取当前指针位置  

    # 获取文件的总长度, 将指针移动到文件开始位置  
    image_obj.seek(0, 2)  # 将指针移动到文件的末尾  
    file_size_in_bytes = image_obj.tell()  # 获取总字节数  
    image_obj.seek(current_position)  # 将指针重新移回到原始位置  
    
    # 将字节大小转换为KB，除以1024  
    return file_size_in_bytes / 1024  # 返回大小以KB为单位 

def resize_image_to_target_size(image, target_size_kb=10240,max_attempts=100):
    """
    调整图像大小，使其文件大小尽可能接近但不超过指定的千字节数。
    有待完善。
    :param image: PIL.Image 对象
    :param target_size_kb: 目标文件大小（千字节）
    :param max_attempts: 最大尝试次数
    :return: 调整后的 PIL.Image 对象
    """
    
    # 将目标大小从KB转换为字节
    target_size_bytes = target_size_kb * 1024

    # 初始设置
    quality = 95  # 初始质量设置为较高值
    initial_step = 1  # 初始步长
    min_quality = 60  # 最低质量限制
    attempts = 0

    # 尝试不同的质量和尺寸，直到文件大小满足要求或达到最大尝试次数
    while attempts < max_attempts:
        # 使用内存缓冲区保存图像
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=quality)
        file_size = buffer.tell()

        if file_size <= target_size_bytes:
            break

        # 计算新的步长
        if file_size > target_size_bytes * 1.1:  # 如果文件大小明显超过目标值，使用较大的步长
            step = initial_step
        else:  # 如果文件大小接近目标值，使用较小的步长
            step = 1

        # 减少质量
        quality -= step

        # 如果质量已经很低但文件仍然很大，则尝试缩小图像尺寸
        if quality <= min_quality:
            width, height = image.size
            new_width = int(width * 0.9)  # 缩小10%
            new_height = int(height * 0.9)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
            quality = 95  # 重置质量

        attempts += 1

    buffer.seek(0)
    return Image.open(buffer)

def extract_positions(data):
    '''
    提取坐标值。
    从json数据格式[[{'pos': [{'x': 968, 'y': 191}, {'x': 1109, 'y': 191}, {'x': 1106, 'y': 389}, {'x': 968, 'y': 389}], 'tableCellId': 0, 'word': '报名区', 'xec': 3, 'xsc': 3, 'yec': 1, 'ysc': 0},...]]
    提取tableCellId和pos，返回json格式如下：
    {0: [{'x': 968, 'y': 191}, {'x': 1109, 'y': 191}, {'x': 1106, 'y': 389}, {'x': 968, 'y': 389}], ......}
    '''
    result = {}
    for item in data[0]:
        result[item['tableCellId']] = item['pos']
    return result

def draw_quadrilaterals(image,data):
    """
    在给定的图像上绘制绿色的四边形框。
    data格式为{
        0: [{'x': 968, 'y': 191}, {'x': 1109, 'y': 191}, {'x': 1106, 'y': 389}, {'x': 968, 'y': 389}],
        ......
    }
    参数：
    - image：要绘制四边形框的`PIL`图像对象。

    功能：
    1. 遍历给定的字典数据，每个键值对代表一个四边形框，值是四边形的四个顶点坐标。
    2. 对于每个四边形框，提取四个顶点坐标，组成一个元组列表。
    3. 使用`ImageDraw`对象在图像上绘制多边形（这里的多边形实际是四边形），线条颜色为绿色且宽度较粗以增强可见性。
    """
    draw = ImageDraw.Draw(image)
    # for key, points_data in data.items():
    #     points = [(points_data[0]['x'], points_data[0]['y']),
    #               (points_data[1]['x'], points_data[1]['y']),
    #               (points_data[2]['x'], points_data[2]['y']),
    #               (points_data[3]['x'], points_data[3]['y'])]
        # draw.polygon(points, outline='green', width=3)  # 绘制绿色多边形，宽度为 3
    for key, points_data in data.items():
        points = [(points_data[0]['x'], points_data[0]['y']),
                  (points_data[1]['x'], points_data[1]['y']),
                  (points_data[2]['x'], points_data[2]['y']),
                  (points_data[3]['x'], points_data[3]['y']),
                  (points_data[0]['x'], points_data[0]['y'])]
        draw.line(points, fill='green', width=10) 