@echo off
REM Set fixed folder names for input and output relative to the batch file
set "data_folder=data"
set "output_folder=outputs"

REM Prompt the user for the input image file name (only the file name with extension)
echo Enter the image file name (e.g., 31.jpg):
set /p image_name=

REM Prompt the user for the output file base name (Tesseract will append the extension)
echo Enter the result file base name (e.g., result):
set /p result_name=

REM Prompt for the language code, default to eng if nothing entered
echo Enter the language code (default is eng):
set /p lang=
if "%lang%"=="" (
    set lang=eng
)

REM Construct full paths using the fixed folders
set "input_image=%data_folder%\%image_name%"
set "output_base=%output_folder%\%result_name%"

REM Run Tesseract using the absolute path to tesseract.exe
echo Running Tesseract...
"C:\Program Files\Tesseract-OCR\tesseract.exe" "%input_image%" "%output_base%" -l %lang%

echo.
echo Tesseract processing complete.
pause
