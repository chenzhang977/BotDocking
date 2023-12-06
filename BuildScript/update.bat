@echo off
:: 检查是否在运行
set "process_name=pybot.exe"   
:loop  
tasklist | findstr /i "%process_name%" >nul  
if %errorlevel%==0 (  
    timeout /t 1 >nul
    echo %process_name% is running, sleep.
    goto loop  
)

:: 初始化变量
set "root=%~dp0"
set "app=pybot.exe"
set "backup=%root%backup"
set "dist=%root%dist"

::备份
if exist "%root%../Run/%app%" (  
    if not exist "%backup%" (  
        mkdir "%backup%"  
    )
    echo "%root%..\Run\%app%"
    echo "%backup%"

    copy "%root%..\Run\%app%" "%backup%" /y >nul  
    echo %app% copied to %backup%  
) else (  
    echo %app% not found  
)
::拉取代码编译
cd ../../
git pull --rebase
cd ./BuildAndRun/Build
python "build.py"

::编译的exe挪出来
if exist "%dist%\%app%" (  
    if not exist "%root%../Run" (  
        mkdir "%root%../Run" 
    )
    copy "%dist%\%app%" "%root%../Run" /y >nul
    echo %app% copied to %root%
) else (
    echo %app% not found  
)
:: 执行
if exist "%root%..\Run\%app%" (
    echo "%root%..\Run\%app%"
    cd ../Run
    start %root%..\Run\%app%
)
::休眠三秒，检查是否运行，判断是否需要回滚
timeout /t 3 >nul
tasklist | findstr /i "%process_name%" >nul
if %errorlevel%==1 (
    echo %process_name% is not running.
	::回滚备份
    copy "%backup%\%app%" "%root%..\Run"/y >nul
    start %root%../Run/%app%
    git reset --hard HEAD~1
)
pause