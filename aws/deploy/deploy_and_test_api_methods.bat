@ECHO OFF
:: All commands halt the build and throw an error value.

ECHO ################################################################################

ECHO TEST_STEP: Create virtual env
virtualenv -p c:\python35\python.exe env || EXIT /B 1
CALL env\Scripts\activate.bat || EXIT /B 2

ECHO TEST_STEP: Install dependencies
python -m pip install -r requirements.txt --upgrade || EXIT /B 3

ECHO TEST_STEP: Re-import API Swagger file to AWS
python deployment_helper.py || EXIT /B 4

ECHO TEST_STEP: Test API methods
python -m pytest -s tests\test_invoke_methods.py --junit-xml junit-methods.xml || EXIT /B 5

:: TODO Enable the following for regenerating the API.md
::ECHO TEST_STEP: Generate API.md documentation
::swagger2markdown -i ..\..\api\DataServiceAPI_swagger.json -o ..\..\API.md

:: Leave build venv
deactivate || EXIT /B 6

EXIT /B 0
