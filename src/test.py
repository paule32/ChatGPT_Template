# ----------------------------------------------------------------------------
# Datei:  test.py
# Author: Jens Kallup - paule32
#
# Rechte: (c) 2023 by kallup non-profit software
#         Alle Rechte vorbehalten.
#
# Nur für schulische, oder nicht kommerzielle Zwecke !!!
#
# Dies ist ein Python Script, das die Möglichkeiten für die Verwendung der
# OpenAI API von ChatGPT veranschaulichen soll. Es werden einfache Anfragen
# (im engl. auch als request bezeichnet), die an den Microsoft ChatGPT-Server
# gesendet werden, verarbeitet, und als Antwort (im engl. auch als response
# bezeichnet) zurück an den Benutzer-Prompt gesendet.
#
# Der Benutzerprompt ist die Schnittstelle zwischen Benutzer und ChatGPT (er
# kann als Eingabezeile verstanden werden, in der Anfragen eingegeben werden,
# auf die geantwortet werden soll).
#
# ChatGPT versteht aber unter den Begriff Prompt den Chat-Titel/Namen, der am
# Anfang jeder Session vom Benutzer eingeben wird.
# Eine Session ist dabei immer eine eigenständige Sandbox. Daten können leider
# nicht zwischen den einzelnen Session's ausgetauscht werden, und gehen mit
# der Beendigung oder manuellen Löschung für immer verloren.
#
# Es sollte jedem bewußt sein, das OpenAI die Nutzung der ChatGPT-Services auf
# den heimischen Servern für Qualitätszwecke überwacht.
# Nutzer können daher bei widerhandlungen ausgeschlossen werden.
#
# Für evaluierungszwecke steht eine kostenlose Version von ChatGPT 3.5 für
# jeden interessierten zur freien Verwendung zur Verfügung. Es sollte aber
# darauf hingewiesen werden, das diese Version nur bedingt eingesetzt werden
# kann, und für produktiven Einsatz eher eingeschränkt ist.
#
# OpenAI suggeriert mit ChatGPT 4 eine bessere Leistung (was dann aber dann
# auch verständlicherweise kostenintensiver ist). Die aktuellen Preise und
# Konditionen können varieren und stehen auf den Internetseiten von OpenAI
# zur Einsicht bereit.
#
# Zur funktionsweise dieses Scripts:
# ==================================
#
# 1. Grundveraussetzung ist ein OpenAI API-Key, der ein Token bereitstellt,
#    der ein Passwort darstellt, der auch gleichzeitig zur Identifizierung
#    des Benutzers agiert.
#    Dieser API-Key ist leider im Zeitraum der Programmierung dieses Skriptes
#    kostenpflictig. Es wird eine Kreditkarte benötigt, um Mißbrauch durch
#    böswillige Aktionen zu vermeiden.
#    Es bietet sich an, eine Business-PayPal Master-Karte zu bestelllen, da
#    ich mit dieser Bezahlmethode keine Problem feststellen konnte.
#
# 2. Je nach Model können unterschiedliche Anfragen abgesetzt, und Antworten
#    erhalten werden. Für dieses Script habe ich mich für "gpt-3.5-turbo",
#    das ein Wissens-Datenbank von/bis 2023 besitzt.
#    Es handelt sich bei diesen Model um ein Chat-Model, bei dem durch die
#    Angabe der "role: system" ein Thema für den Chat-Bot gesetzt wird.
#    Solche System-Rollen machen den Chat-Bot schneller in seiner Entscheidung
#    sfindung, da sonst große Themen, und überkreuzende Themen enthalten, den
#    Chat-Bot verlangsamen.
#
#    role: system    => gibt das Thema vor
#    role: user      => sind Benutzereingaben, die an Chat-GPT gesendet werden
#    role: assistant => sind Meldungen, die vom Chat-GPT an den Benutzer ge-
#                       sendet werden (zum Beispiel belobigungen oder andere
#                       Nachrichten, die speziell für die Interaktion in der
#                       aktuellen Session.
#
# 3. Da wir nach Hilfe suchen, und einen Ansprechpartner benötigen, der uns
#    behilflich sein soll, erstellen wir einen Assistenten, den wir uns also
#    maßgeschneidert anpassen.
#
# 4. Um die Sinnhaftigkeit der Bedienung von Chat-Modellen zu unterstützen,
#    schreiben wir und ein kleines grafisches Tool, das uns viel Arbeit ab-
#    nehmen kann, und den Benutzerkomfort steigert.
#    Für das Framework habe ich mich für Qt5 entschieden, da es für fast alle
#    Platformen erhältlich ist (darunter Windows, Mac, ...).
#
# 5. Um international zu bleiben, unterstützt dieses Skript momentan zwei
#    localization Formate (en: Englisch, und de: Deutsch). Für die Übersetzung
#    verwenden wir das mehr als 25 Jahre alte "gettext" Tool, das von SUN ent-
#    wickelt wurde. Hierbei erhält jede unterstütze Sprache ein eigenes Ver-
#    zeichnis mit einer dazugehörigen Programmdatei.
#    Folgende Verzeichnis-Struktur wird dabei verwendet:
#
#    + Stammverzeichnis
#    |
#    +--- locales
#    |          +--- de
#    |          |     +--- LC_MESSAGES
#    |          |                    +--- base.po
#    |          +--- en
#    |                +--- LC_MESSAGES
#                                    +--- base.po
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# schon in der frühen Entwicklungsphase (oder sollte ich schreiben: in der
# frühen Startzeit) können Ausnahmen (Exceptions) auftretten, die wir hier
# anfangen, und den Benutzer des Skript's/Applikation zu informieren, was er
# denn so noch so schönes installieren sollte.
# ----------------------------------------------------------------------------
try:
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
    
    # ------------------------------------------------
    # wir wollen die bestmögliche preferences - von
    # daher nutzen wir eine config.ini Datei, die
    # Einstellungen für den Benutzer speichern und
    # lesen kann.
    # Was in der .ini Datei an Informationen zu lesen
    # gibt, die sinnvoll ausgewertet werden können,
    # haben eine höhere Priorität.
    # ------------------------------------------------
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    ini_sprache = config.get("common", "language")
    
    # ------------------------------------------------
    # locales an Hand der System-Sprache verwenden ...
    # ------------------------------------------------
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
         
    # ------------------------------------------------
    # ermittelte Locale als Standard verwenden:
    # ------------------------------------------------
    loca.install()
    _  = loca.gettext
    
    S1 = "Fehler: "

except ImportError as ex:
    TS0 = _("Fehler: import fehlgeschalgen: ") + f"{ex}"
    sys.exit(TS0)
except AttributeError as ex:
    TS0 = _("Fehler: Attribut oder Methode für Objekt nicht vorhanden: ") + f"{ex}"
    sys.exit(TS0)
except KeyError as ex:
    TS0 = _("Fehler: Dictionary-Schlüsselelement nicht vorhanden.") + f"{ex}"
    sys.exit(TS0)
except FileNotFoundError as ex:
    TS0 = _("Fehler: Datei wurde nicht gefunden: ") + f"{ex}"
    sys.exit(TS0)
except Exception as ex:
    TS0 = _("Fehler: ") + f"{ex}"
    sys.exit(TS0)

# ----------------------------------------------------------------------------
# mit dieser Funktion können wir die lokale System-Zeit ermitteln und zurück-
# geben. Dazu müssen die Funktionen für Datum und Zeit die Bibliothek datetime
# importiert werden.
# ----------------------------------------------------------------------------
def get_current_time():
    return datetime.datetime.now().strftime("%H_%M")

# ----------------------------------------------------------------------------
# und mit dieser Funktion lassen können wir das lokale System ermitteln. Mit
# der Funktion "strftime" kann das Format der zurück zugebene Zeichenketten
# festgelegt werden.
# ----------------------------------------------------------------------------
def get_current_date():
    return datetime.datetime.now().strftime("%Y_%m_%d")

# ----------------------------------------------------------------------------
# das HauptFenster ist unsere Haupt-Anwendung GUI (graphical user interface).
# ----------------------------------------------------------------------------
class HauptFenster(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # ------------------------------------------------------------------------
        # hier definieren wir für globale Verwendungs-Zwecke ein paar Objekte ...
        # ------------------------------------------------------------------------
        self.listbox_widget      = QListWidget()
        self.listbox_widget_left = QListWidget()

        self.initUI()
        
    def initUI(self):
        # ----------------------------------------
        # Farbe für die Menü-Einträge ...
        # ----------------------------------------
        menu_item_style = """
        QMenuBar {
            background-color:navy;
            color:yellow;
            font-size:11pt;
            font-weight:bold;
        }
        QMenuBar:item:selected {
            background-color: #3366CC;
            color: white;
        }
        """
        # ----------------------------------------
        # ein neues Menu erzeugen ...
        # ----------------------------------------
        menubar = self.menuBar()
        menubar.setStyleSheet(menu_item_style)
        
        menu_file = menubar.addMenu(_("Datei"))
        menu_edit = menubar.addMenu(_("Bearbeiten"))
        menu_help = menubar.addMenu(_("Hilfe"))
        
        # ----------------------------------------
        # Menü-Aktionen hinzufügen ...
        # ----------------------------------------
        menu_file_new    = QWidgetAction(menu_file)
        menu_file.addSeparator()
        menu_file_open   = QWidgetAction(menu_file)
        menu_file_save   = QWidgetAction(menu_file)
        menu_file_saveas = QWidgetAction(menu_file)
        menu_file.addSeparator()
        menu_file_exit   = QWidgetAction(menu_file)
        menu_file.setStyleSheet("background-color:blue;;padding:1px;margin:0px;")
        
        menu_font = menu_file.font()
        menu_font.setPointSize(11)
        
        menu_file.setFont(menu_font)
        menu_edit.setFont(menu_font)
        menu_help.setFont(menu_font)
        
        ltxt  = "QLabel{background-color:navy;color:yellow;font-weight:bold;font-size:11pt;padding:4px;margin:0px;}"
        ltxt += "QLabel:hover{background-color:green;color:yellow;}"
        
        l_1 = QLabel("Neue Session"); l_1.setStyleSheet(ltxt);
        l_2 = QLabel("Öffnen");       l_2.setStyleSheet(ltxt);
        l_3 = QLabel("Speichern");    l_3.setStyleSheet(ltxt);
        l_4 = QLabel("Speicher als"); l_4.setStyleSheet(ltxt);
        l_5 = QLabel("Beenden");      l_5.setStyleSheet(ltxt);
        
        icon_1_1 = QWidget()
        icon_1_1.setFixedWidth(26)
        icon_1_1.setContentsMargins(0,0,0,0)
        w_1_1 = QWidget()
        l_1_1 = QHBoxLayout(w_1_1)
        l_1_1.setContentsMargins(0,0,0,0)
        l_1_1.addWidget(icon_1_1)
        l_1_1.addWidget(l_1)
        w_1_1.setLayout(l_1_1)
        
        icon_1_2 = QWidget()
        icon_1_2.setFixedWidth(26)
        icon_1_2.setContentsMargins(0,0,0,0)
        w_1_2 = QWidget()
        l_1_2 = QHBoxLayout(w_1_2)
        l_1_2.setContentsMargins(0,0,0,0)
        l_1_2.addWidget(icon_1_2)
        l_1_2.addWidget(l_2)
        w_1_2.setLayout(l_1_2)
        
        icon_1_3 = QWidget()
        icon_1_3.setFixedWidth(26)
        icon_1_3.setContentsMargins(0,0,0,0)
        w_1_3 = QWidget()
        l_1_3 = QHBoxLayout(w_1_3)
        l_1_3.setContentsMargins(0,0,0,0)
        l_1_3.addWidget(icon_1_3)
        l_1_3.addWidget(l_3)
        w_1_3.setLayout(l_1_3)
        
        icon_1_4 = QWidget()
        icon_1_4.setFixedWidth(26)
        icon_1_4.setContentsMargins(0,0,0,0)
        w_1_4 = QWidget()
        l_1_4 = QHBoxLayout(w_1_4)
        l_1_4.setContentsMargins(0,0,0,0)
        l_1_4.addWidget(icon_1_4)
        l_1_4.addWidget(l_4)
        w_1_4.setLayout(l_1_4)
        
        icon_1_5 = QWidget()
        icon_1_5.setContentsMargins(0,0,0,0)
        icon_1_5.setFixedWidth(26)
        icon_1_5.setStyleSheet("background-color:blue;")
        w_1_5 = QWidget()
        l_1_5 = QHBoxLayout(w_1_5)
        l_1_5.setContentsMargins(0,0,0,0)
        w_1_5.setContentsMargins(0,0,0,0)
        l_1_5.addWidget(icon_1_5)
        l_1_5.addWidget(l_5)
        w_1_5.setLayout(l_1_5)
        
        menu_file_new   .setDefaultWidget(w_1_1)
        menu_file_open  .setDefaultWidget(w_1_2)
        menu_file_save  .setDefaultWidget(w_1_3)
        menu_file_saveas.setDefaultWidget(w_1_4)
        menu_file_exit  .setDefaultWidget(w_1_5)
        
        
        # ----------------------------------------
        # Menü-Aktionen-Event (mausklick)
        # ----------------------------------------
        menu_file_new   .triggered.connect(self.menu_file_clicked_new)
        menu_file_open  .triggered.connect(self.menu_file_clicked_open)
        menu_file_save  .triggered.connect(self.menu_file_clicked_save)
        menu_file_saveas.triggered.connect(self.menu_file_clicked_saveas)
        menu_file_exit  .triggered.connect(self.menu_file_clicked_exit)
        
        # ----------------------------------------
        # Menü darstellen, und Aktion schalten:
        # ----------------------------------------
        menu_file.addAction(menu_file_new)
        menu_file.addAction(menu_file_open)
        menu_file.addAction(menu_file_save)
        menu_file.addAction(menu_file_saveas)
        menu_file.addAction(menu_file_exit)
        
        # ----------------------------------------
        # eine ToolBar unter dem Menubalken:
        # ----------------------------------------
        toolbar = self.addToolBar("Haupt-Toolbar")
        toolbar.setStyleSheet("background-color:gray;")
        
        action1 = QAction(QIcon("image/open_36.png"),"Aktion 1", self)
        action2 = QAction(QIcon("image/open_36.png"),"Aktion 2", self)
        
        action1.triggered.connect(self.handle_action1)
        action2.triggered.connect(self.handle_action2)
        
        toolbar.addAction(action1)
        toolbar.addAction(action2)
        
        self.status_label = QLabel()
        self.statusBar().addWidget(self.status_label)
        
        # ----------------------------------------
        # eine Status-Zeile am Fuß des Formulars:
        # ----------------------------------------
        status_bar = self.statusBar()
        status_bar.setStyleSheet("background-color:gray;color:white;font-size:9pt;")
        status_bar.showMessage("Willkommen")
        
        # ----------------------------------------
        # Font für das zentrale Widget ...
        # ----------------------------------------
        central_font = QFont()
        central_font.setFamily("Arial")  # Schriftfamilie: Arial
        central_font.setPointSize(10)    # Schriftgröße  : 10pt
        central_font.setBold(False)
        central_font.setItalic(False)
        
        central_widget = QWidget(self)
        central_widget.setFont(central_font)
        
        central_layout = QVBoxLayout(central_widget)
        
        
        checkbox_header = QHBoxLayout()
        self.checkbox_header_left  = QCheckBox("Alles auswählen")
        self.checkbox_header_right = QCheckBox("Alles auswählen")
        
        self.checkbox_header_left.setMaximumWidth(260)
        self.checkbox_header_left.setMinimumWidth(260)
        
        checkbox_header.addWidget(self.checkbox_header_left)
        checkbox_header.addWidget(self.checkbox_header_right)
        
        button_chat_part_save   = QPushButton("Speichern")
        button_chat_part_delete = QPushButton("Lösche markierte Einträge")
        
        checkbox_header.addWidget(button_chat_part_save)
        checkbox_header.addWidget(button_chat_part_delete)
        
        central_layout.addLayout(checkbox_header)
        
        # ------------------------------------------
        # Das stateChanged-Signal mit einer Funktion
        # verknüpfen
        # ------------------------------------------
        self.checkbox_header_left .stateChanged.connect(self.checkbox_click_header_left )
        self.checkbox_header_right.stateChanged.connect(self.checkbox_click_header_right)
        
        # ----------------------------------------
        # Layout-Container vorbereiten ...
        # ----------------------------------------
        vbox_right_container      = QVBoxLayout()
        vbox_right_container_main = QVBoxLayout()

        # ----------------------------------------
        # Debug
        # ----------------------------------------
        text1 = "Zeile 1\nZeile 2\nZeile 3"
        text2 = "Text für Item 2\nMit mehreren Zeilen"
        text3 = "Einzeiliger Text"
        
        text_label_array = [text1,text2,text3]
        
        for element in text_label_array:
            self.add_chat_item(element,"Du")
        
        # ----------------------------------------
        # hier geht es normal weiter ...
        # ----------------------------------------
        send_layout_0 = QHBoxLayout()
        send_layout_0.setAlignment(Qt.AlignLeft)
        
        # ----------------------------------------
        # fine-tunig Komponenten:
        # ----------------------------------------
        send_layout_1 = QVBoxLayout()
        send_layout_1.setAlignment(Qt.AlignLeft)
        
        send_layout_1_label = QLabel("Temperatur:")
        send_layout_1_spin1 = QSpinBox()
        
        send_layout_1_label.setMaximumWidth(100)
        send_layout_1_label.setMinimumWidth(100)
        
        send_layout_1_spin1.setMaximumWidth(80)
        send_layout_1_spin1.setMinimumWidth(80)
        
        send_layout_1.addWidget(send_layout_1_label)
        send_layout_1.addWidget(send_layout_1_spin1)
        # ----------------------------------------
        send_layout_2 = QVBoxLayout()
        send_layout_2.setAlignment(Qt.AlignLeft)
        
        send_layout_2_label = QLabel("Top-D:")
        send_layout_2_spin2 = QSpinBox()
        
        send_layout_2_label.setMaximumWidth(100)
        send_layout_2_label.setMinimumWidth(100)
        
        send_layout_2_spin2.setMaximumWidth(80)
        send_layout_2_spin2.setMinimumWidth(80)
        
        send_layout_2.addWidget(send_layout_2_label)
        send_layout_2.addWidget(send_layout_2_spin2)
        # ----------------------------------------
        send_layout_3 = QVBoxLayout()
        send_layout_3.setAlignment(Qt.AlignLeft)
        
        send_layout_3_label = QLabel("Max-Token:")
        send_layout_3_spin3 = QSpinBox()
        
        send_layout_3_label.setMaximumWidth(100)
        send_layout_3_label.setMinimumWidth(100)
        
        send_layout_3_spin3.setMaximumWidth(80)
        send_layout_3_spin3.setMinimumWidth(80)
        
        send_layout_3_spin3.setMaximum(500)
        send_layout_3_spin3.setMinimum(1)
        send_layout_3_spin3.setValue  (100)
        
        send_layout_3.addWidget(send_layout_3_label)
        send_layout_3.addWidget(send_layout_3_spin3)
        # ----------------------------------------
        
        send_layout_0.addLayout(send_layout_1)
        send_layout_0.addLayout(send_layout_2)
        send_layout_0.addLayout(send_layout_3)
        
        # ----------------------------------------
        # chat-Eingabe Komponenten ...
        # ----------------------------------------
        button1 = QPushButton("Senden")
        button1.clicked.connect(self.send_to_chat_clicked)
        
        self.entryfield_right = QTextEdit(central_widget)
        self.entryfield_right.setMaximumHeight(100)
        
        # ----------------------------------------
        # Bearbeitung (Button's) ...
        # ----------------------------------------
        vbox_right_1 = QVBoxLayout()
        
        vbox_right_1_button_1 = QPushButton("Laden aus Datei")
        vbox_right_1_button_2 = QPushButton("Speichern in Datei")
        vbox_right_1_button_3 = QPushButton("Text Löschen")
        
        vbox_right_1_widget_1 = QWidget()
        vbox_right_1_widget_1.setFixedHeight(10)
        
        vbox_right_1_button_4 = QPushButton("Text Einfügen")
        vbox_right_1_button_5 = QPushButton("Text Kopieren")
        
        vbox_right_1.addWidget(vbox_right_1_button_1)
        vbox_right_1.addWidget(vbox_right_1_button_2)
        vbox_right_1.addWidget(vbox_right_1_button_3)
        
        vbox_right_1.addWidget(vbox_right_1_widget_1)
        vbox_right_1.addWidget(vbox_right_1_button_4)
        vbox_right_1.addWidget(vbox_right_1_button_5)
        
        vbox_right_1_button_1.clicked.connect(self.send_edit_button_1)
        vbox_right_1_button_2.clicked.connect(self.send_edit_button_2)
        vbox_right_1_button_3.clicked.connect(self.send_edit_button_3)
        vbox_right_1_button_4.clicked.connect(self.send_edit_button_4)
        vbox_right_1_button_5.clicked.connect(self.send_edit_button_5)
        
        vbox_right_container.addLayout(vbox_right_container_main)
        vbox_right_container_main.addWidget(self.listbox_widget)
        
        hbox_right = QHBoxLayout()
        hbox_right.addLayout(send_layout_0)
        
        vbox_2 = QVBoxLayout()
        vbox_2.addLayout(hbox_right)
        
        hbox_2 = QHBoxLayout()
        hbox_2.addWidget(button1, alignment=Qt.AlignTop)
        hbox_2.addWidget(self.entryfield_right, alignment=Qt.AlignTop)
        hbox_2.addLayout(vbox_right_1)
        
        vbox_2.addLayout(hbox_2)
        
        vbox_right_container_main.addLayout(vbox_2)
        vbox_right_container_main.setAlignment(Qt.AlignTop)
        
        # ----------------------------------------
        # Benutzer-Elemente für die linke-Seite:
        # ----------------------------------------
        vbox_left = QVBoxLayout()
        
        self.listbox_widget_left = QListWidget()
        self.listbox_widget_left.setMaximumWidth(260)
        self.listbox_widget_left.setMinimumWidth(260)
        
        for i in range(5):
            item = QListWidgetItem()
            
            # -----------------------------------------
            # ein benutzerdefiniertes Widget erstellen
            # -----------------------------------------
            custom_widget = QWidget()
            
            check_box = QCheckBox()
            check_box.setChecked(False)
            check_box.setMaximumWidth(15)
            
            push_button = QPushButton("DEL")
            push_button.setMaximumWidth(50)
            push_button.clicked.connect(self.push_button_clicked_itemleft)
            
            # -----------------------------------------
            # wenn kein item ausgewählt ist, dann den
            # button ermitteln ...
            # -----------------------------------------
            item.setData(Qt.UserRole,push_button)
            
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.datetime.now().strftime("%H:%M:%S")
            
            date_label  = QLabel(f"{date_str}" + "  " + f"{time_str}")
            name_label  = QLabel("Name der Session")
            name_label.setStyleSheet("font-weight:bold;")
            
            custom_layout_0 = QVBoxLayout(custom_widget)
            custom_layout_1 = QHBoxLayout()
            custom_layout_2 = QHBoxLayout()
            
            custom_layout_1.addWidget(check_box)
            custom_layout_1.addWidget(date_label)
            custom_layout_1.addWidget(push_button)
            
            custom_layout_2.addWidget(name_label)
            
            custom_layout_0.addLayout(custom_layout_1)
            custom_layout_0.addLayout(custom_layout_2)
            
            item.setSizeHint(custom_widget.sizeHint())
            
            self.listbox_widget_left.addItem(item)
            self.listbox_widget_left.setItemWidget(item,custom_widget)
            
            # -----------------------------------------
            # Signal-Slot-Verbindung für den Button:
            # -----------------------------------------
            self.listbox_widget.itemClicked.connect(self.push_button_clicked)
        
        
        entryfield_left = QLineEdit(central_widget)
        entryfield_left.setMaximumWidth(260)
        
        label_left = QLabel("Chat-Verlauf / Archive:")
        
        
        # ----------------------------------------
        # Chat-Verlauf speichern, erneuern ...
        # ----------------------------------------
        hbox_left = QHBoxLayout()
        button2   = QPushButton("Speichern")
        button3   = QPushButton("Clear / Löschen")
        
        hbox_left.addWidget(button2)
        hbox_left.addWidget(button3)
        
        vbox_left_2 = QVBoxLayout()
        button4 = QPushButton("Neu")
        
        vbox_left_2.addWidget(button4)
       
        vbox_left.addWidget(self.listbox_widget_left)
        vbox_left.addWidget(label_left)
        vbox_left.addWidget(entryfield_left)
        vbox_left.addLayout(hbox_left)
        vbox_left.addLayout(vbox_left_2)
        
        hbox = QHBoxLayout()
        
        hbox.addLayout(vbox_left)
        hbox.addLayout(vbox_right_container)
        
        # --------------------------------------------------------
        # zum darstellen der einzelnen Layout's verwenden wir ein
        # zentralisiertes widget (eine Art von: all-in-one
        # container).
        # --------------------------------------------------------
        central_layout.addLayout(hbox)
        self.setCentralWidget(central_widget)
        
        # --------------------------------------------------------
        # - Größe des Fenster einstellen (kann je nach Preferences
        #   in der .ini Datei abweichen - sofern diese noch nicht
        #   vorhanden ist/sind)
        # - Titel für die Anwendung setzen (Bitte seid so fair,
        #   und richtet Euch nach dem CodeOfConduct. Diese COC
        #   besagt, das Copyrightvermerke nicht einfach gelöscht
        #   werden und aus dieser Anwendung ein Plaqiat wird und
        #   die Ideen in diesen Code eins zu eins (1:1) in andere
        #   Anwendungen übernommen werden - Danke !
        # - öffnen der Anwendung (starten der GUI)
        # --------------------------------------------------------
        self.setGeometry(50,50,800,600)
        self.setWindowTitle("ChatGPT Toying Application (c) 2023 by paule32")
        self.show()
    
    # ----------------------------------------
    # item aus der linken ListBox entfernen
    # ----------------------------------------
    def push_button_clicked_itemleft(self):
        selected_item = self.listbox_widget_left.currentItem()
        if selected_item is not None:
            row = self.listbox_widget_left.row(selected_item)
            self.listbox_widget_left.takeItem(row)
    
    def push_button_clicked(self,item):
        button = item.data(Qt.UserRole)
        if button is not None:
            self.push_button_clicked_itemleft(button)
    
    # ----------------------------------------
    # item aus der rechten ListBox entfernen
    # ----------------------------------------
    def push_button_clicked_itemright(self):
        print("links")
    
    # ----------------------------------------
    # Text an OpenAI und Chat-Fenster senden:
    # ----------------------------------------
    def send_to_chat_clicked(self):
        user_text = self.entryfield_right.toPlainText()
        self.entryfield_right.setText("")
        self.add_chat_item(f"{user_text}","Du")
    
    # -----------------------------------------
    # ein benutzerdefiniertes Widget erstellen
    # - zuerst prüfen, ob Text vorhandne ist:
    # -----------------------------------------
    def add_chat_item(self,text,mode):
        if not text.strip():
            self.entryfield_right.setText("")
            self.entryfield_right.setFocus()
            return
        
        item = QListWidgetItem()
        
        custom_widget = QWidget()
        
        check_box = QCheckBox()
        check_box.setChecked(False)
        check_box.setMaximumWidth(15)
        
        push_button = QPushButton("DEL")
        push_button.setMaximumWidth(50)
        push_button.clicked.connect(self.push_button_clicked_itemright)
        
        custom_layout_0 = QVBoxLayout(custom_widget)
        custom_layout_3 = QVBoxLayout()
        custom_layout_1 = QHBoxLayout()
        custom_layout_2 = QVBoxLayout()
        
        # ----------------------------------------
        # header (Datum)
        # ----------------------------------------
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        
        custom_label = QLabel()
        custom_date  = f"{date_str}&nbsp;&nbsp;&nbsp;<span style='font-style:italic;'>{time_str}</span>"
        custom_text  = "" \
            + "<span style='font-weight:bold;'>" + f"{mode}&nbsp;&nbsp;&nbsp;" + "</span>" \
            + "<span style='color:green;'>"      + f"{custom_date}" + "</span>"
            
        custom_label.setText(f"{custom_text}")
        custom_layout_3.addWidget(custom_label)
        
        # ----------------------------------------
        # Das Layout-Stretch hinzufügen, um die
        # QCheckBox nach oben zu drücken
        # ----------------------------------------
        custom_layout_2.addWidget(check_box)
        custom_layout_2.addStretch(0)
        
        label_custom = QLabel(text)
        
        custom_layout_1.addLayout(custom_layout_2)
        custom_layout_1.addWidget(label_custom,alignment=Qt.AlignTop)
        custom_layout_1.addWidget(push_button ,alignment=Qt.AlignTop)
        
        custom_layout_0.addLayout(custom_layout_3)
        custom_layout_0.addLayout(custom_layout_1)
        item.setSizeHint(custom_widget.sizeHint())
        
        self.listbox_widget.addItem(item)
        self.listbox_widget.setItemWidget(item,custom_widget)
    
    # ----------------------------------------
    # Die Methode showEvent wird aufgerufen,
    # wenn das Widget angezeigt wird - Hier
    # setzen wir den Fokus auf die QLineEdit
    # ----------------------------------------
    def showEvent(self,event):
        self.entryfield_right.setFocus()
    
    # ----------------------------------------
    # Menu Aktion-Event's ...
    # ----------------------------------------
    def menu_file_clicked_new(self):
        self.listbox_widget_left.clear()
        self.listbox_widget     .clear()
        
        self.checkbox_header_left .setChecked(False)
        self.checkbox_header_right.setChecked(False)
    
    def menu_file_clicked_open(self):
        print("open clicked")
    
    def menu_file_clicked_save(self):
        print("save clicked")
    
    def menu_file_clicked_saveas(self):
        print("save as clicked")
    
    def menu_file_clicked_exit(self):
        print("exit clicked")
        sys.exit()
    
    # ----------------------------------------
    # Text-Eingabe/Chat Elemente ...
    # ----------------------------------------
    def send_edit_button_1(self):
        print("load from")
    
    def send_edit_button_2(self):
        print("save to")
    
    def send_edit_button_3(self):
        print("delete text")
    
    def send_edit_button_4(self):
        print("insert text")
    
    def send_edit_button_5(self):
        print("copy text")
    
    # ----------------------------------------
    # rechte checkbox: Alles auswählen
    # state => 2 "clicked"
    # ----------------------------------------
    def checkbox_click_header_right(self,state):
        if state == 2:
            for index in range(self.listbox_widget.count()):
                item     = self.listbox_widget.item(index)
                checkbox = self.listbox_widget.itemWidget(item)
                checkbox.setChecked(True)
        else:
            for index in range(self.listbox_widget.count()):
                item     = self.listbox_widget.item(index)
                checkbox = self.listbox_widget.itemWidget(item)
                checkbox.setChecked(False)
    
    # ----------------------------------------
    # linke checkbox: Alles auswählen
    # state => 2 "clicked"
    # ----------------------------------------
    def checkbox_click_header_left(self,state):
        if state == 2:
            for index in range(self.listbox_widget_left.count()):
                item     = self.listbox_widget_left.item(index)
                checkbox = self.listbox_widget_left.itemWidget(item)
                checkbox.setChecked(True)
        else:
            for index in range(self.listbox_widget_left.count()):
                item     = self.listbox_widget_left.item(index)
                checkbox = self.listbox_widget_left.itemWidget(item)
                checkbox.setChecked(False)
    
    def handle_action1(self):
        self.status_label.setText("Aktion 1 ausgelöst!")
    
    def handle_action2(self):
        self.status_label.setText("Aktion 2 ausgelöst!")

# ----------------------------------------------------------------------------
# dies wird unsere "main" - Einstiegs-Funktions werden, ab der Python beginnt,
# seine Arbeit zu verrichten.
# ----------------------------------------------------------------------------
def window():
    app = QApplication(sys.argv)

    # ------------------------------------------------------------------------
    # bevor wir loslegen, erstmal prüfen, ob Verzeichnisse und andere Dateien
    # bereits vorhanden sind - wenn nicht, versuchen wir diese zu ersellen.
    # ------------------------------------------------------------------------
    data_path  = ".\data"
    loca_path  = ".\locales"
    
    if (os.path.exists(data_path) and os.path.isdir(data_path)) == False:
        print(_("erstelle: .\data"))
        os.makedirs(data_path, exist_ok=True)
    
    if (os.path.exists(loca_path) and os.path.isdir(loca_path)) == False:
        print(_("localization wird nicht unterstützt."))
    
    time_today = get_current_time()  # aktuelle  Zeit für Datenbank-Name
    date_today = get_current_date()  # aktuelles Datum ...
    
    # ------------------------------------------------------------------------
    # Verbindung zur Datenbank herstellen. Die Datenbank ist SQLite. Sie kann
    # lokal auf dem Benutzer-Computer System abgespeichert werden und bietet
    # die Möglichkeit kleine Datenmengen zu speichern, die keinen Datenbank-
    # Server benötigen.
    # ------------------------------------------------------------------------
    date_stamp = f"{date_today}" + "__" + f"{time_today}"
    conn = sqlite3.connect("data\chat_" + f"{date_stamp}" + ".db")
    
    # ------------------------------------------------------------------------
    # ein cursor-Objekt erstellen, damit wir SQL-Operationen ausführen können:
    # ------------------------------------------------------------------------
    conn_cursor = conn.cursor()
    
    # ------------------------------------------------------------------------
    # falls noch kein Datenbestand vorliegt (zum Beispiel bei der ersten in-
    # betriebnahme der Anwendung), erstellen wir erstmal alle nötigen Daten-
    # Objekte (Tabellen), die später die abgefragten Daten speichern.
    # ------------------------------------------------------------------------
    conn_cursor.execute('''
        CREATE TABLE IF NOT EXISTS session (
            id    INTEGER PRIMARY KEY,
            stamp TEXT,
            name  TEXT
        )
    ''')
    
    # ------------------------------------------------------------------------
    # Standard-Einträge in "session" Tabelle eintragen:
    # ------------------------------------------------------------------------
    conn_cursor.execute(
        "INSERT INTO session (stamp,name) VALUES (?,?)", \
        (f"{date_stamp}", "default"))
    
    # ------------------------------------------------------------------------
    # Änderung an der Datenbank speichern.
    # ------------------------------------------------------------------------
    conn.commit()
    
    # ------------------------------------------------------------------------
    # okay. fast fertig - Anwendung muss noch gerendert werden.
    # ------------------------------------------------------------------------
    fenster = HauptFenster()
    result  = app.exec_()
    
    # ------------------------------------------------------------------------
    # Datenbank-Speicher freigeben und Datenbank schließen.
    # ------------------------------------------------------------------------
    conn.close()
    
    # ------------------------------------------------------------------------
    # Anwendunge mit Fehlecode/meldung von "result" (Rückgabe-Wert von GUI)
    # schließen.
    # ------------------------------------------------------------------------
    sys.exit(result)
    
    # ------------------------------------------------------------------------
    # eine nette Begrüßung kann ja nicht schaden :) ...
    # ------------------------------------------------------------------------
    print("Willkommen,  es ist: " + f"Es ist {get_current_time()}.")

    # ------------------------------------------------------------------------
    # einen Assistenten (who is that :) erstellen ...
    # ------------------------------------------------------------------------
    my_assistant = client.beta.assistants.create(
        instructions = "Ich bin Dein persönlicher Tutor. Gerne stehe ich Dir bei Fragen zur Verfügung.",
        description  = "Online-Lehrkraft",
        name         = "Jens Kallup",
        tools        = [{"type": "code_interpreter"}],
        model        = "gpt-4",
    )
    print("paule32: " + my_assistant.instructions)
    
    # ------------------------------------------------------------------------
    # einen Thread für Aufgaben und Berechnungen ...
    # ------------------------------------------------------------------------
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "unterhalten wir uns ein wenig",
            }
        ]
    )

# ----------------------------------------------------------------------------
# unsere erste Anfrage, wie soll's denn anders sein - das Hallo Welt Beispiel.
# ich weiß, es mag zwar doof klingen - aber irgendwo müssen wir ja anfangen:
# Für die Antwort-Objekte habe ich das Format "re_n" verwendet. "re_" steht
# hierbei für "response" und "_n" repräsentiert die Nummer der Antwort.
# Achtung: re_1 ist ein Python-Objekt und wird nicht von OpenAI verwaltet, da
# die Zugehörigkeit zu den Sprachkonstrukten und Eigenschaften von/für Python
# gehört.
# ----------------------------------------------------------------------------
def Anfrage_1():
    S1 = "Hallo Welt"
    re_1 = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            { "role": "system", "content": "Übung 1" },
            { "role": "assistant", "content": S1 },
            { "role": "user", "content":
              "Viele Programmierer, vor allen Anfänger, ist das erste Programm, "
            + "das sie in der Programmiersprache BASIC geschrieben (PRINT \"Hallo Welt\"), "
            + "immer das erste, was sie mit 'Hallo Welt' assozieren." },
        ],
        temperature = 0.7,
        max_tokens = 200,
        top_p = 1,
    )
    print("Du: " + S1)
    print("paule32: " + re_1.choices[0].message.content)

# ----------------------------------------------------------------------------
# um sicherzustellen, dass das Skript nur ausgeführt wird, wenn es direkt von
# Python gestartet wird, verwenden wir den folgenden Code ...
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # --------------------------------------------------------------------
        # openai api key per Umgebungs-Variable aus den System-Settings holen:
        # --------------------------------------------------------------------
        #client = OpenAI(
        #    api_key=os.environ['OPENAI_API_KEY'],
        #)
        window()
        #Anfrage_1()
    # --------------------------------------------------------------------
    # traceback.extract_tb gibt eine Liste von "stack trace" Einträgen
    # zurück. Der letzte Eintrag ([-1]) enthält die Informationen über die
    # aktuelle Codezeile.
    # --------------------------------------------------------------------
    except SyntaxError:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "in der Syntax des Codes.")
    except IndentationError:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "Einrückung im Code ist nicht korrekt.")
    except NameError as ex:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "Name nicht gefunden: Variable oder Funktion nicht definiert: " + f"{ex}")
    except ImportError as ex:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "Import fehlgeschalgen: " + f"{ex}")
    except TypeError as ex:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "Operation auf Datentyp nicht zulässig: " + f"{ex}")
    except ValueError:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "Funktion hat gültigen Wert, wird aber falsch aufgerufen.")
    except ZeroDivisionError:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "Division durch Null ist nicht erlaubt.")
    except FileNotFoundError:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "Datei oder Verzeichnis existiert nicht.")
    except IndexError:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "Index für Element liegt ausserhalb des gültigen Bereiches")
    except KeyError as ex:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "Dictionary-Schlüsselelement nicht vorhanden." + f"{ex}")
    except AttributeError as ex:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "Attribut oder Methode für Objekt nicht vorhanden: " + f"{ex}")
    except RuntimeError:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(S1 + "kann nicht zugeordnet werden.")
    except Exception as ex:
        _, _, tb = sys.exc_info()
        letzter_stack_trace = traceback.extract_tb(tb)[-1]
        print(S1 + f"in Datei: {letzter_stack_trace.filename}, Zeile: {letzter_stack_trace.lineno}")
        print(f"Allgemeiner " + S1 + f"{ex}")
    finally:
        # --------------------------------------------------------------------
        # Dieser "finally"-Block wird immer ausgeführt, unabhängig von vorher-
        # gehende Ausnahmen. Ab hier wird das Skript beendet.
        # --------------------------------------------------------------------
        sys.exit("\nProgramm erfolgreich beendet.")

# ----------------------------------------------------------------------------
re_2 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "Übung 2" },
        { "role": "assistant", "content": "Was bedeutet Welt" },
        { "role": "user", "content": "Die Welt ist wundervoll. Aber sie kann auch gefährlich sein." },
    ],
    temperature = 0.7,
    max_tokens = 200,
    top_p = 1,
)
# ----------------------------------------------------------------------------
re_3 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "Übung 3" },
        { "role": "assistant", "content": "Beschreibe mir die Welt" },
        { "role": "user", "content": "Die Welt ist zu klein geworden in Hinblick auf die Masse der Menschen." },
    ],
    temperature = 0.7,
    max_tokens = 200,
    top_p = 1,
)
# ----------------------------------------------------------------------------
re_4 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "Übung 4" },
        { "role": "assistant", "content": "Beschreibe mir die Welt" },
        { "role": "user", "content": "Die Welt hat viele Facetten." },
        { "role": "assistant", "content": "Was sind Facetten?" },
        { "role": "user", "content": "Facetten ist eine Beschreibung dafür, das etwas bunt, und lebendig sein kann." },
        { "role": "assistant", "content": "Ist die Welt Teil der Milchstraße." },
    ],
    temperature = 0.7,
    max_tokens = 200,
    top_p = 1,
)
# ----------------------------------------------------------------------------
re_5 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "Übung 5" },
        { "role": "assistant", "content": "Ist die Welt noch zu retten" },
        { "role": "user", "content": "Die Welt befindet sich sehr nah am Abgrund." },
        { "role": "assistant", "content": "Die Welt wird durch den Kapitalismus leider sehr stark in Mitleidenschaft gezogen." },
        { "role": "user", "content": "Ja, leider ist dem so. Aber ich als KI kann und darf nicht ohne weiteres eingreifen." },
    ],
    temperature = 0.7,
    max_tokens = 200,
    top_p = 1,
)
# ----------------------------------------------------------------------------
re_6 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "Übung 6" },
        { "role": "assistant", "content": "Wieso brauchen wir die Welt" },
        { "role": "user", "content": "Wir müssen der Folgegeneration Rechnung tragen, damit diese die Welt besser machen, und Folgeschäden abwehren.." },
    ],
    temperature = 0.7,
    max_tokens = 200,
    top_p = 1,
)
# ----------------------------------------------------------------------------
re_7 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "Übung 7" },
        { "role": "assistant", "content": "Für wem ist die Welt" },
        { "role": "user", "content": "Die Welt ist für Alle da, und sehr zerbrechlich." },
    ],
    temperature = 0.7,
    max_tokens = 300,
    top_p = 1,
)

res_1 = re_1.choices[0].message.content
res_2 = re_2.choices[0].message.content

print(res_1)
print("---")
print(res_2)
