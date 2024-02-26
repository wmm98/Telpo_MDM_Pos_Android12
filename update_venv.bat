cd /d %~dp0

::安装poetry
pip install poetry -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

set VENV_NAME=poetry_venv

echo Creating virtual environment...
if not exist "%VENV_NAME%" poetry config virtualenvs.path %CD%\%VENV_NAME%
poetry env use python
echo Virtual environment created at %CD%\%VENV_NAME%

:: 安装依赖库
poetry install

pause

