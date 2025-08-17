@echo off
:: Initialize Conda, activate the base environment, and run the Python script
CALL conda activate base
python C:\projects\orph.in\jarjamorp.github.io\_python\trending.py >>C:\projects\orph.in\jarjamorp.github.io\_python\logfile.log 2>&1
