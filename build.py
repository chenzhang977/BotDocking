import PyInstaller.__main__  
  
PyInstaller.__main__.run([  
    '--name=pybot',
    '--onefile',  # 生成单个可执行文件
    '--icon=Config/icon.ico',
    'main.py',
])