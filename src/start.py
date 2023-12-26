# ----------------------------------------------------------------------------
# Datei:  start.py
# Author: Jens Kallup - paule32
#
# Rechte: (c) 2023 by kallup non-profit software
#         Alle Rechte vorbehalten.
#
# Nur für schulische, oder nicht kommerzielle Zwecke !!!
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# schon in der frühen Entwicklungsphase (oder sollte ich schreiben: in der
# frühen Startzeit) können Ausnahmen (Exceptions) auftretten, die wir hier
# anfangen, und den Benutzer des Skript's/Applikation zu informieren, was er
# denn so noch so schönes installieren sollte.
# ----------------------------------------------------------------------------
import os            # operating system stuff
import sys           # system specifies
import datetime      # date, and time routines
import gettext       # localization
import locale        # internal system locale
import sqlite3       # database: sqlite
import configparser  # .ini files
import traceback     # stack exception trace back

from PyQt5.QtWidgets import *             # Qt5 widgets
from PyQt5.QtGui     import QIcon, QFont  # Qt5 gui
from PyQt5.QtCore    import pyqtSlot, Qt  # Qt5 core

from openai import OpenAI                 # ChatGPT like AI

from main import *

# ------------------------------------------------
# locales an Hand der System-Sprache verwenden ...
# ------------------------------------------------
def handle_language(ini_sprache):
    system_sprache, _ = locale.getdefaultlocale()
    if   system_sprache.lower() == "en_us":
         if ini_sprache.lower() == "en":
            loca = gettext.translation("base", localedir="locales", languages=["en"])  # english
         if ini_sprache.lower() == "de":
            loca = gettext.translation("base", localedir="locales", languages=["de"])  # german
    elif system_sprache.lower() == "de_de":
         if ini_sprache.lower() == "en":
            loca = gettext.translation("base", localedir="locales", languages=["en"])  # english
         if ini_sprache.lower() == "de":
            loca = gettext.translation("base", localedir="locales", languages=["de"])  # german
    else:
            loca = gettext.translation("base", localedir="locales", languages=["en"])  # fallback
    
    loca.install()
    return loca

# ------------------------------------------------
# wir wollen die bestmögliche preferences - von
# daher nutzen wir eine config.ini Datei, die
# Einstellungen für den Benutzer speichern und
# lesen kann.
# Was in der .ini Datei an Informationen zu lesen
# gibt, die sinnvoll ausgewertet werden können,
# haben eine höhere Priorität.
# ------------------------------------------------
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    ini_sprache = config.get("common", "language")
   
    loca = handle_language(ini_sprache)
    _    = loca.gettext
        
    main_function()
