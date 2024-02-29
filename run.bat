cd /d %~dp0

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


:: 执行 Python 脚本
::python run.py
poetry run python -u run.py

:: 退出虚拟环境
::deactivate

pause

