pip install virtualenv
virtualenv env
call .\env\Scripts\activate.bat
call .\env\Scripts\pip.exe install starlette
call .\env\Scripts\pip.exe install uvicorn[standard]
call .\env\Scripts\pip.exe install pydantic
call .\env\Scripts\pip.exe install pydantic-settings
call .\env\Scripts\pip.exe install python-multipart
call .\env\Scripts\pip.exe install fastapi
call .\env\Scripts\pip.exe install mysql-connector-python
call .\env\Scripts\pip.exe install python-jose[cryptography]
call .\env\Scripts\pip.exe install passlib[argon2]
call .\env\Scripts\pip.exe install python-ffmpeg-video-streaming
call .\env\Scripts\pip.exe install moviepy
call .\env\Scripts\pip.exe install pyyaml ua-parser user-agents