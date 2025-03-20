# h2d/__init__.py
from .converter import H2D

# 全局字体变量，默认值为 '微软雅黑'
_global_font = '微软雅黑'

def setFont(font_name_or_path):
    """设置全局字体，可以是字体名称或字体文件路径"""
    global _global_font
    _global_font = font_name_or_path

def convert(html_string):
    """将 HTML 字符串转换为 DOCX Document 对象"""
    return H2D(_global_font).convert(html_string)

# 只暴露 convert 和 setFont 函数
__all__ = ['convert', 'setFont']