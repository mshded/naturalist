@echo off
setlocal enabledelayedexpansion

echo     EXPERIMENT SETUP
echo ========================================

:: Get current date and time
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do (
    set DATE=%%c%%b%%a
)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set TIME=%%a%%b
)

:: Request experiment name
set /p EXP_PREFIX="Enter experiment prefix (e.g., efficientnet_aug): "
set EXP_NAME=%DATE%_%TIME%_%EXP_PREFIX%

echo.
echo Creating experiment: %EXP_NAME%
echo.

:: Step 1: Create experiment folder
mkdir experiments\%EXP_NAME% 2>nul
if exist experiments\%EXP_NAME% (
    echo [OK] Experiment folder created
) else (
    echo [ERROR] Failed to create folder
    pause
    exit /b 1
)

:: Step 2: Copy configuration
copy params.yaml experiments\%EXP_NAME%\params.yaml >nul
echo [OK] Configuration saved

:: Step 3: Request parameter changes
echo.
echo Current parameters:
type params.yaml | findstr /B "model: training: data:"
echo.
set /p CONFIRM="Edit parameters? (y/n): "
if /i "!CONFIRM!"=="y" (
    notepad experiments\%EXP_NAME%\params.yaml
)

:: Step 4: Run experiment
echo.
echo ========================================
echo     RUNNING EXPERIMENT
echo ========================================

:: Create backup of current params.yaml
copy params.yaml params.yaml.backup >nul

:: Replace with experimental configuration
copy experiments\%EXP_NAME%\params.yaml params.yaml /Y >nul
echo [OK] Experimental configuration applied

:: Run training
echo.
echo Starting training...
dvc repro train_model
if !errorlevel! neq 0 (
    echo [ERROR] Training failed
    goto :cleanup
)

:: Run evaluation
echo.
echo Starting evaluation...
python src/evaluate.py --model models/best_model.pth
if !errorlevel! neq 0 (
    echo [ERROR] Evaluation failed
    goto :cleanup
)

:: Step 5: Save results
echo.
echo ========================================
echo     SAVING RESULTS
echo ========================================

mkdir experiments\%EXP_NAME%\models 2>nul
mkdir experiments\%EXP_NAME%\plots 2>nul
mkdir experiments\%EXP_NAME%\metrics 2>nul

:: Copy results
copy models\best_model.pth experiments\%EXP_NAME%\models\ >nul
copy models\training_history.pth experiments\%EXP_NAME%\models\ >nul
copy plots\*.png experiments\%EXP_NAME%\plots\ >nul
copy metrics\*.json experiments\%EXP_NAME%\metrics\ >nul

:: Save DVC metrics
dvc metrics show > experiments\%EXP_NAME%\metrics\dvc_metrics.txt 2>nul

:: Create README
(
    echo # Experiment: %EXP_NAME%
    echo.
    echo ## Date and time: %date% %time%
    echo.
    echo ## Configuration:
    echo.
    type params.yaml
    echo.
    echo ## Metrics:
    echo.
    type experiments\%EXP_NAME%\metrics\test_metrics.json
) > experiments\%EXP_NAME%\README.md

echo [OK] Results saved to experiments\%EXP_NAME%

:: Step 6: Git commit
echo.
set /p DO_COMMIT="Create Git commit? (y/n): "
if /i "!DO_COMMIT!"=="y" (
    set /p COMMIT_MSG="Enter commit message: "
    git add experiments\%EXP_NAME% params.yaml dvc.lock
    git commit -m "Experiment: %EXP_NAME% - !COMMIT_MSG!"
    git push origin main
    dvc push
    echo [OK] Changes committed to Git
)

:cleanup
:: Restore original params.yaml
copy params.yaml.backup params.yaml /Y >nul
del params.yaml.backup >nul

echo.
echo ========================================
echo     EXPERIMENT COMPLETED
echo ========================================
echo Name: %EXP_NAME%
echo Folder: experiments\%EXP_NAME%
echo.
pause