@ECHO off

start BUTTON_ONE_EXECUTION.bat

ping 127.0.0.1 -n 5 > nul

start BUTTON_ROBOT_ONE_START.bat
start Error_monitor_start.bat




