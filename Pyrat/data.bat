@echo OFF
cd C:\Users\poltg\Documents\imt code\Pyrat
C:
set /A j = 1
:loop
set /A j = %j% +2 
start "%j%" cmd /K "python pyrat.py --rat AIs/bfsai.py -x %j% -y %j% -p 1 -md 0 -d 0 --nodrawing"
if %j% == 25 (pause) else (goto :loop)