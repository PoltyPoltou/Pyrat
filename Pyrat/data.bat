@echo OFF
cd C:\Users\poltg\Documents\imt code\Pyrat
C:
set /A j = 1
:loop
set /A j = %j% + 1
start "%j%" cmd /K "python pyrat.py --rat AIs/bruteforce.py -p %j% --nodrawing --preparation_time 60000"
if %j% == 10 (pause) else (goto :loop)