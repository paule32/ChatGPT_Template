@echo off
set PYTHONNOFAULTHANDLER=1
rem python "%USERPROFILE%\AppData\Local\Programs\Python\Python310\Tools\i18n\pygettext.py" -d base -o locales/base.pot test.py
echo erstelle LC_MESSAGES
cd locales\de\LC_MESSAGES
@python -X nofaulthandler "%USERPROFILE%\AppData\Local\Programs\Python\Python310\Tools\i18n\msgfmt.py" -o base.mo base > NUL
if %errorlevel% neq 0 ( goto fehler_lc_messages )
cd ..\..
cd en\LC_MESSAGES
@python -X nofaulthandler "%USERPROFILE%\AppData\Local\Programs\Python\Python310\Tools\i18n\msgfmt.py" -o base.mo base > NUL
if %errorlevel% neq 0 ( goto fehler_lc_messages )
cd ..\..\..
@python -m compileall main.py
if %errorlevel% neq 0 ( goto fehler_compile_cache )
@python -m compileall start.py
if %errorlevel% neq 0 ( goto fehler_compile_cache )
goto Ende

:fehler_lc_messages
echo Fehler aufgetretten: LC_MESSAGES
goto skipper

:fehler_compile_cache
echo "Fehler aufgetretten: compile Python Skript
goto skipper

:Ende
echo ohne Fehler beendet, fertig.
goto skipper

:skipper
