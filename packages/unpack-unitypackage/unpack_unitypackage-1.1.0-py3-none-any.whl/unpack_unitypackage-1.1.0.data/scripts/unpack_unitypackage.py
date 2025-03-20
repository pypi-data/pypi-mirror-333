#!python
import sys
import os
import pathlib
from unitypackage_extractor.extractor import extractPackage


def main():
    # 检查是否提供了命令行参数
    if len(sys.argv) < 2:
        print("错误: 请提供文件路径作为参数")
        sys.exit(1)
    
    # 获取第一个命令行参数（文件路径）
    file_path = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)
    
    # 检查文件扩展名是否为.zip或.unitypackage
    file_extension = pathlib.Path(file_path).suffix.lower()
    if file_extension not in ['.zip', '.unitypackage']:
        print(f"错误: 文件必须是.zip或.unitypackage格式，当前文件扩展名为: {file_extension}")
        sys.exit(1)
    
    # 获取文件名（不含扩展名）和目录
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    file_name_without_ext = os.path.splitext(file_name)[0]
    
    # 创建解包目录名
    unpack_dir_name = f"{file_name_without_ext}_unpack"
    unpack_dir_path = os.path.join(file_dir, unpack_dir_name)
    
    # 创建解包目录
    try:
        os.makedirs(unpack_dir_path, exist_ok=True)
        print(f"已创建解包目录: {unpack_dir_path}")
    except Exception as e:
        print(f"创建目录时出错: {e}")
        sys.exit(1)
    
    print(f"文件 '{file_path}' 已通过验证")
    print(f"解包目录已创建: '{unpack_dir_path}'")

    unity_package_file = file_path
    # 处理ZIP文件
    if file_extension == '.zip':
        import zipfile
        import shutil
        
        print(f"正在解压ZIP文件到: {unpack_dir_path}")
        try:
            # 解压ZIP文件到目标目录
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(unpack_dir_path)
            
            print("ZIP文件解压完成")
            
            # 查找解压后的.unitypackage文件
            found_unity_package = False
            for root, dirs, files in os.walk(unpack_dir_path):
                for file in files:
                    if file.lower().endswith('.unitypackage'):
                        unity_package_file = os.path.join(root, file)
                        found_unity_package = True
                        print(f"找到Unity包文件: {unity_package_file}")
                        break
                if found_unity_package:
                    break
            
            if not found_unity_package:
                print("错误: 在解压后的文件中未找到.unitypackage文件")
                sys.exit(1)
            
        except zipfile.BadZipFile:
            print("错误: 无效的ZIP文件")
            sys.exit(1)
        except Exception as e:
            print(f"解压ZIP文件时出错: {e}")
            # 清理失败的解压目录
            shutil.rmtree(unpack_dir_path, ignore_errors=True)
            sys.exit(1)

    print("正在提取UnityPackage文件")
    extractPackage(unity_package_file, outputPath=unpack_dir_path)
    print("UnityPackage 文件提取完成")

if __name__ == "__main__":
    main()
