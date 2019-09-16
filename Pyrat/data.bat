@echo OFF
cd C:\Users\poltg\Documents\imt code\Pyrat
C:
set /A j = 1
:loop
set /A j = %j% +2 
start "%j%" cmd /K "python pyrat.py --rat AIs/BFSai.py -x %j% -y %j% -p 1 --mud_density 0 --nodrawing --test 20"
if %j% == 51 (pause) else (goto :loop)