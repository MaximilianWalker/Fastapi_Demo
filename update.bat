call .\env\Scripts\activate.bat
call .\env\Scripts\pip.exe freeze > requirements.txt
call .\env\Scripts\pip.exe install -r requirements.txt --upgrade