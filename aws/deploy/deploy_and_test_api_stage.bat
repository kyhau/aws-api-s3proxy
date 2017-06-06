@ECHO OFF
:: All commands halt the build and throw an error value.

ECHO ################################################################################

SET STAGE_NAME=test
if "%1"=="" (
  echo "Usage: test_deployed_stage.bat [stage-name]"
) else (
  SET STAGE_NAME=%1
)

ECHO TEST_STEP: Create virtual env
virtualenv -p c:\python35\python.exe env || EXIT /B 1
CALL env\Scripts\activate.bat || EXIT /B 2

ECHO TEST_STEP: Install dependencies
python -m pip install -r requirements.txt --upgrade || EXIT /B 3

ECHO TEST_STEP: Create or update a deployment stage
python deployment_helper.py --deploy %STAGE_NAME% || EXIT /B 4

ECHO TEST_STEP: Run tests on the deployed stage (TODO)
::python -m pytest -s tests\test_deployed_stage.py --junit-xml junit-stage.xml || EXIT /B 5

:: Leave build venv
deactivate || EXIT /B 6

EXIT /B 0
