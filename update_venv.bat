
cd /d %~dp0

set VENV_DIR=myvenv

:: 检查虚拟环境是否已存在
IF EXIST "%VENV_DIR%" (
  echo 虚拟环境已存在，跳过创建步骤
) ELSE (
  echo 创建虚拟环境...
  python -m venv %VENV_DIR%
)

:: 激活虚拟环境
call %VENV_DIR%\Scripts\activate.bat

:: 继续执行其他操作，例如安装依赖、运行 Python 脚本等
:: 安装依赖
pip install -r requirements.txt

:: 执行 Python 脚本
:: python myscript.py

:: 退出虚拟环境
deactivate

pause

