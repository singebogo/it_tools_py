# it_tools
## 简易记事本

##json 
   格式化  压缩  转义 反转义
   Tree显示节点

## xml
   格式化
   Tree显示节点

## 文本对比

## 打包
###打包程序
auto-py-to-exe
### 打包参数
pyinstaller --noconfirm --onefile --windowed --icon "E:/Document/Document/python/it_tools-ttkbstrap/assert/imgs/favicon.ico" --add-data "E:/Document/Document/python/it_tools-ttkbstrap/gui;gui/" --add-data "E:/Document/Document/python/it_tools-ttkbstrap/config;config/" --add-data "E:/Document/Document/python/it_tools-ttkbstrap/utils;utils/" --add-data "E:/Document/Document/python/it_tools-ttkbstrap/assert;assert/" --hidden-import "pandas" --hidden-import "numpy" --hidden-import "toml" --hidden-import "tomli" --hidden-import "ttkbootstrap" --hidden-import "chardet" --hidden-import "calendar" --hidden-import "messagebox" --hidden-import "filedialog"  "E:/Document/Document/python/it_tools-ttkbstrap/it-tools.py"