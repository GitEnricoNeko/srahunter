mkdir %PREFIX%\Scripts
copy %RECIPE_DIR%\scripts\*.sh %PREFIX%\Scripts
"%PYTHON%" setup.py install
if errorlevel 1 exit 1
