@echo off
cd /d %~dp0

::rem 设置 需要打包 脚本路径
set PYTHON_SCRIPT=UI\MDM_Run.py

:: 获取上一级目录虚拟路径名称
REM @echo off
setlocal EnableDelayedExpansion

set "keyword=telpo-android-automation"
set "current_dir=%cd%"
for %%G in ("%current_dir%\..\poetry_venv") do set "parent_dir=%%~fG"

for /d %%a in ("%parent_dir%\*%keyword%*") do (
    set "ENV_FOLDER_NAME=%%~nxa"
    echo Folder in parent directory containing keyword "%keyword%": !ENV_FOLDER_NAME!
)

:: 激活虚拟环境
set "PUBLIC_ENV=..\poetry_venv\!ENV_FOLDER_NAME!"
echo Folder NAME: %PUBLIC_ENV%

call %PUBLIC_ENV%\Scripts\activate

:: 继续执行其他操作，例如安装依赖、运行 Python 脚本等
:: 安装依赖
REM ::设置目标文件夹路径
set DEST_FOLDER_DIST=dist\MDM_Run
set DEST_FOLDER_BUILD=build\MDM_Run
set DEST_FOLDER_INTERNAL=_internal
set FILE_NAME=MDM_Run.spec
set EXE_NAME=MDM_Run.exe
REM
REM ::清除已存在的exe文件夹（如果存在）
if exist "%DEST_FOLDER_DIST%" rmdir /s /q "%DEST_FOLDER_DIST%"
if exist "%DEST_FOLDER_BUILD%" rmdir /s /q "%DEST_FOLDER_BUILD%"
if exist "%DEST_FOLDER_INTERNAL%" rmdir /s /q "%DEST_FOLDER_INTERNAL%"
if exist "%FILE_NAME%" del /q "%FILE_NAME%"
if exist "%EXE_NAME%" del /q "%EXE_NAME%"

REM ::打包exe文件
poetry run pyinstaller %PYTHON_SCRIPT%
REM
echo copy file operation！！！
::拷贝文件夹，文件到当前目录下
set SOURCE_DICT_EXE=dist\MDM_Run\MDM_Run.exe
set SOURCE_DICT_INTERNAL=dist\MDM_Run\_internal
set DEST_INTERNAL=_internal
REM
::复制dist下的exe文件和文件夹
if exist "%SOURCE_DICT_EXE%" copy "%SOURCE_DICT_EXE%" "%cd%"
if not exist "%DEST_INTERNAL%" mkdir "%DEST_INTERNAL%"
if exist "%SOURCE_DICT_INTERNAL%" xcopy "%SOURCE_DICT_INTERNAL%" "%DEST_INTERNAL%" /s /e
echo success to copy file !!!

:: 退出虚拟环境
deactivate

pause