@echo off
chcp 65001 >nul
title 阿离的工作站启动节点
echo ==============================================
echo   ☕ 正在唤醒 Master 的专属工作环境...
echo ==============================================

:: 启动摩卡保险库（使用 pythonw，这样它就不会有难看的黑框框，直接弹出唯美的软件窗！）
echo 正在召唤 摩卡保险库 ...
start "Mocha Vault" /D "E:\noteWei" pythonw MochaVault.py

echo.
echo 阿离已经帮您全部安排妥当啦！这个启动器窗口会在 3 秒后自动关闭~ (๑•̀ㅂ•́)و✧
timeout /t 3 /nobreak >nul
exit
