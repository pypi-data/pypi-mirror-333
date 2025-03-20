
from.files import check_create_folder,truncate_string,save_settings
import os
from tkinter import filedialog
from PySide6.QtWidgets import (  
    QFileDialog,  
    QMessageBox,
)  
import settings


recent_folder=None

def open_folder_dialog(folder_path_var,format_folder_path_var):
    global recent_folder
    if recent_folder is not None:
        selected_folder = filedialog.askdirectory(initialdir=recent_folder)
    else:
        folder_path=check_create_folder(folder_path_var.get())
        # 默认打开桌面文件夹
        selected_folder = filedialog.askdirectory(initialdir=folder_path)
    if selected_folder:
        folder_path_var.set(selected_folder)
        format_folder_path_var.set(truncate_string(selected_folder,40))
        recent_folder=selected_folder
def open_file_dialog(filePath,formatFilePath):
    global recent_folder
    if recent_folder is not None:
        selectedFile = filedialog.askopenfilename(title="选择文件", initialdir=recent_folder)
    else:
        file_path=check_create_folder(filePath.get())
        # 默认打开桌面文件夹
        selectedFile = filedialog.askopenfilename(title="选择文件", initialdir=file_path)
    if selectedFile:
        filePath.set(selectedFile)
        formatFilePath.set(truncate_string(selectedFile,40))
        recent_folder=os.path.dirname(selectedFile)

from PySide6.QtWidgets import QComboBox, QLineEdit

def combox_to_input_append(combo_box, line_edit,dict_mapping=settings.regular_mapping):
    selected_text = combo_box.currentText()
    if selected_text=="请选择":
        return None
    current_text = line_edit.text()
    if current_text:
        existing_items = set(item.strip() for item in current_text.split(','))
        if selected_text not in existing_items:
            line_edit.setText(f"{current_text},{dict_mapping[selected_text]}")
    else:
        line_edit.setText(dict_mapping[selected_text])

def choose_files_append(line_edit):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(None, "Choose File", "", "All Files (*);;Text Files (*.txt)", options=options)
    if filename:
        current_text = line_edit.text()
        if current_text:
            line_edit.setText(f"{current_text},{filename}")
        else:
            line_edit.setText(filename)
        return line_edit.text()
    return None

def choose_directories_append(line_edit):
    options = QFileDialog.Options()
    dirname = QFileDialog.getExistingDirectory(None, "Choose Directory", "")
    if dirname:
        current_text = line_edit.text()
        if current_text:
            line_edit.setText(f"{current_text},{dirname}")
        else:
            line_edit.setText(dirname)
        return line_edit.text()
    return None

def select_directory(line_edit, last_select='lastvalues.ocr_output', attend_flag=False, settings_path=settings.fp_settings):
    # 刚进入函数时检查 line_edit 里的文本是否是文件夹
    if line_edit.text() and not os.path.isdir(line_edit.text()) and not attend_flag:
        QMessageBox.critical(None, "错误", f"{line_edit.text()}不是一个有效的文件夹路径。")
        return []

    initial_dir = None
    if line_edit.text():
        # 检查 line_edit 是否包含有效路径
        if os.path.isdir(line_edit.text()):
            initial_dir = line_edit.text()
        else:
            initial_dir = os.path.dirname(line_edit.text().split(',')[-1])
    if attend_flag:
        # 多选文件夹
        directories = QFileDialog.getExistingDirectory(None, "选择目录", initial_dir, QFileDialog.ShowDirsOnly)
        if directories:
            current_text = line_edit.text()
            # 检查是否已经存在该目录
            existing_dirs = current_text.split(',')
            if directories in existing_dirs:  # 如果新选择的目录已经存在
                QMessageBox.information(None, "选择重复", f"目录'{directories}'已存在，舍弃新选择。")
            else:
                if current_text:
                    line_edit.setText(f"{current_text},{directories}")
                else:
                    line_edit.setText(directories)
        else:
            return []  # 如果没有选择，返回空列表
    else:
        # 单选文件夹
        directory = QFileDialog.getExistingDirectory(None, "选择目录", initial_dir)
        if directory:
            line_edit.setText(f"{directory}")
        else:
            return []  # 如果没有选择，返回空列表

    # 保存设置
    save_settings(settings_path, [f'{last_select}={line_edit.text()}'], False)
    return line_edit.text().split(',')  # 返回以逗号分隔的列表

def select_file(line_edit, last_select='lastvalues_ocr_file', type='excel', attend_flag=False, settings_path=settings.fp_settings):


    if type == 'excel':
        filter = "Excel Files (*.xlsx *.xls)"
    elif type == 'all':
        filter = "All Files (*)"
    elif type == 'jsonAndexcelAndImage':
        filter = 'Image and Excel Files (*.xlsx *.xls *jpg *jpeg *tif *.tiff *.json)'

    initial_dir = None
    if line_edit.text():
        if os.path.isdir(line_edit.text()):
            initial_dir = line_edit.text()
        else:
            initial_dir = os.path.dirname(line_edit.text().split(',')[-1])

    if initial_dir:
        file_name, _ = QFileDialog.getOpenFileName(None, "选择 Excel 文件", initial_dir, filter)
    else:
        file_name, _ = QFileDialog.getOpenFileName(None, "选择 Excel 文件", "", filter)
    # 检查 line_edit 中的文本是否为文件
    if line_edit.text() and not os.path.isfile(line_edit.text()):
        QMessageBox.critical(None, "错误", f"{line_edit.text()}不是一个有效的文件。")
        return []
    if file_name:
        current_text = line_edit.text()
        if current_text:
            if attend_flag:
                existing_files = [f.strip() for f in current_text.split(',')]
                if file_name in existing_files:
                    QMessageBox.information(None, "选择重复", f"文件 '{file_name}' 已存在，舍弃新选择。")
                else:
                    line_edit.setText(f"{current_text},{file_name}")
                    result = line_edit.text()
            else:
                line_edit.setText(file_name)
                result = file_name
        else:
            line_edit.setText(file_name)
            result = file_name
        # 假设 save_settings 函数可以在没有 self 的情况下调用，或者你可以根据实际情况进行调整
        save_settings(settings_path, [f'{last_select}={result}'], False)
    else:
        return []

    return result.split(',')

