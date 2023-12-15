::python "%USERPROFILE%\AppData\Local\Programs\Python\Python310\Tools\i18n\pygettext.py" -d base -o locales/base.pot test.py
cd locales\de\LC_MESSAGES
python "%USERPROFILE%\AppData\Local\Programs\Python\Python310\Tools\i18n\msgfmt.py" -o base.mo base
cd ..\..
cd en\LC_MESSAGES
python "%USERPROFILE%\AppData\Local\Programs\Python\Python310\Tools\i18n\msgfmt.py" -o base.mo base
