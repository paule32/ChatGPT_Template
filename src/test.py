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
    import configparser  # .ini files
    
    from PyQt5.QtWidgets import *         # Qt5 widgets
    from PyQt5.QtGui     import QIcon     # Qt5 gui
    from PyQt5.QtCore    import pyqtSlot  # Qt5 core
    
    from openai import OpenAI             # ChatGPT like AI
    
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
    
    S1 = _("Fehler: ")
    S2 = _("Programm abgebrochen.\nGrund: ")
    
except ImportError as ex:
    TS0 = S2 + _("import fehlgeschalgen: ") + f"{ex}"
    sys.exit(TS0)
except AttributeError as ex:
    TS0 = S1 + S2 + _("Attribut oder Methode für Objekt nicht vorhanden: ") + f"{ex}"
    sys.exit(TS0)
except KeyError as ex:
    TS0 = S1 + S2 + _("Dictionary-Schlüsselelement nicht vorhanden.") + f"{ex}"
    sys.exit(TS0)
except FileNotFoundError as ex:
    TS0 = "Datei wurde nicht gefunden: " + f"{ex}"
    sys.exit(TS0)
except Exception as ex:
    TS0 = "Fehler: " + f"{ex}"
    sys.exit(TS0)

# ----------------------------------------------------------------------------
# mit dieser Funktion können wir die lokale System-Zeit ermitteln und zurück-
# geben. Dazu müssen die Funktionen für Datum und Zeit die Bibliothek datetime
# importiert werden.
# ----------------------------------------------------------------------------
def get_current_time():
    return datetime.datetime.now().strftime('%H:%M')

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
        # ein neues Menu erzeugen ...
        # ----------------------------------------
        menubar = self.menuBar()
        menubar.setStyleSheet("font-size:11pt;font-weight:bold;")
        
        menu_file = menubar.addMenu(_("Datei"))
        menu_edit = menubar.addMenu(_("Bearbeiten"))
        menu_help = menubar.addMenu(_("Hilfe"))
        
        # ----------------------------------------
        # Menü-Aktionen hinzufügen ...
        # ----------------------------------------
        menu_file_new    = QAction("Neue Sitzung",self)
        menu_file_open   = QAction("Öffnen",self)
        menu_file_save   = QAction("Speichern",self)
        menu_file_saveas = QAction("Speichern als",self)
        menu_file_exit   = QAction("Beenden",self)
        
        menu_font = menu_file.font()
        menu_font.setPointSize(11);
        
        menu_file.setFont(menu_font)
        menu_edit.setFont(menu_font)
        menu_help.setFont(menu_font)
        
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
        # das zentrale Widget ...
        # ----------------------------------------
        central_widget = QWidget(self)
        
        central_layout = QVBoxLayout(central_widget)
        
        checkbox_header = QHBoxLayout()
        checkbox_header_left  = QCheckBox("Alles auswählen")
        checkbox_header_right = QCheckBox("Alles auswählen")
        
        checkbox_header_left.setMaximumWidth(200)
        checkbox_header_left.setMinimumWidth(200)
        
        checkbox_header.addWidget(checkbox_header_left)
        checkbox_header.addWidget(checkbox_header_right)
        
        button_chat_part_save   = QPushButton("Speichern")
        button_chat_part_delete = QPushButton("Löschen markierte Einträge")
        
        checkbox_header.addWidget(button_chat_part_save)
        checkbox_header.addWidget(button_chat_part_delete)
        
        central_layout.addLayout(checkbox_header)
        
        # ------------------------------------------
        # Das stateChanged-Signal mit einer Funktion
        # verknüpfen
        # ------------------------------------------
        checkbox_header_left .stateChanged.connect(self.checkbox_click_header_left )
        checkbox_header_right.stateChanged.connect(self.checkbox_click_header_right)
        
        # ----------------------------------------
        # Layout-Container vorbereiten ...
        # ----------------------------------------
        vbox_right_container      = QVBoxLayout()
        vbox_right_container_main = QVBoxLayout()
        
        for i in range(5):
            item = QListWidgetItem(f"Element {i}")
            check_box = QCheckBox()
            self.listbox_widget.addItem(item)
            self.listbox_widget.setItemWidget(item, check_box)
        
        # ----------------------------------------
        # die folgenden Zeilen sind für Debug
        # ----------------------------------------
        text1 = "    Zeile 1\n    Zeile 2\n    Zeile 3"
        text2 = "    Text für Item 2\n    Mit mehreren Zeilen"
        text3 = "    Einzeiliger Text"
        
        check_box_1 = QCheckBox()
        check_box_2 = QCheckBox()
        check_box_3 = QCheckBox()
        
        item1 = QListWidgetItem(text1)
        item2 = QListWidgetItem(text2)
        item3 = QListWidgetItem(text3)
        
        self.listbox_widget.addItem(item1); self.listbox_widget.setItemWidget(item1,check_box_1)
        self.listbox_widget.addItem(item2); self.listbox_widget.setItemWidget(item2,check_box_2)
        self.listbox_widget.addItem(item3); self.listbox_widget.setItemWidget(item3,check_box_3)
        
        # ----------------------------------------
        # hier geht es normal weiter ...
        # ----------------------------------------
        label_right      = QLabel("Chat-Eingabe:")
        button1          = QPushButton("Senden")
        entryfield_right = QLineEdit(central_widget)
        
        vbox_right_1 = QVBoxLayout()
        vbox_right_1.addWidget(label_right)
        
        hbox_right = QHBoxLayout()
        hbox_right.addWidget(button1)
        hbox_right.addWidget(entryfield_right)
        
        vbox_right_container.addLayout(vbox_right_container_main)
        
        vbox_right_container_main.addWidget(self.listbox_widget)
        vbox_right_container_main.addLayout(vbox_right_1)
        vbox_right_container_main.addLayout(hbox_right)
       
        
        vbox_left = QVBoxLayout()
        
        self.listbox_widget_left = QListWidget()
        self.listbox_widget_left.setMaximumWidth(200)
        self.listbox_widget_left.setMinimumWidth(200)
        
        for i in range(5):
            item = QListWidgetItem(f"Element {i}")
            check_box = QCheckBox()
            self.listbox_widget_left.addItem(item)
            self.listbox_widget_left.setItemWidget(item, check_box)
        
        entryfield_left = QLineEdit(central_widget)
        entryfield_left.setMaximumWidth(200)
        
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
    # Menu Aktion-Event's ...
    # ----------------------------------------
    def menu_file_clicked_new(self):
        print("new clicked")
    
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
    # rechte checkbox: Alles auswählen
    # state => 2 "clicked"
    # ----------------------------------------
    def checkbox_click_header_right(self,state):
        if state == 2:
            for index in range(self.listbox_widget.count()):
                item     = self.listbox_widget.item(index)
                checkbox = self.listbox_widget.itemWidget(item)
                checkbox.setCheckState(2)
        else:
            for index in range(self.listbox_widget.count()):
                item     = self.listbox_widget.item(index)
                checkbox = self.listbox_widget.itemWidget(item)
                checkbox.setCheckState(0)
    
    # ----------------------------------------
    # linke checkbox: Alles auswählen
    # state => 2 "clicked"
    # ----------------------------------------
    def checkbox_click_header_left(self,state):
        if state == 2:
            for index in range(self.listbox_widget_left.count()):
                item     = self.listbox_widget_left.item(index)
                checkbox = self.listbox_widget_left.itemWidget(item)
                checkbox.setCheckState(2)
        else:
            for index in range(self.listbox_widget_left.count()):
                item     = self.listbox_widget_left.item(index)
                checkbox = self.listbox_widget_left.itemWidget(item)
                checkbox.setCheckState(0)

# ----------------------------------------------------------------------------
# dies wird unsere "main" - Einstiegs-Funktions werden, ab der Python beginnt,
# seine Arbeit zu verrichten.
# ----------------------------------------------------------------------------
def window():
    app = QApplication(sys.argv)
    fenster = HauptFenster()
    sys.exit(app.exec_())
    
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
        Anfrage_1()
    except SyntaxError:
        print(S1 + "Fehler in der Syntax des Codes.")
    except IndentationError:
        print(S1 + "Einrückung im Code ist nicht korrekt.")
    except NameError as ex:
        print(S1 + "Name nicht gefunden: Variable oder Funktion nicht definiert: " + f"{ex}")
    except ImportError as ex:
        print(S1 + "Import fehlgeschalgen: " + f"{ex}")
    except TypeError as ex:
        print(S1 + "Operation auf Datentyp nicht zulässig: " + f"{ex}")
    except ValueError:
        print(S1 + "Funktion hat gültigen Wert, wird aber falsch aufgerufen.")
    except ZeroDivisionError:
        print(S1 + "Division durch Null ist nicht erlaubt.")
    except FileNotFoundError:
        print(S1 + "Datei oder Verzeichnis existiert nicht.")
    except IndexError:
        print(S1 + "Index für Element liegt ausserhalb des gültigen Bereiches")
    except KeyError as ex:
        print(S1 + "Dictionary-Schlüsselelement nicht vorhanden." + f"{ex}")
    except AttributeError as ex:
        print(S1 + "Attribut oder Methode für Objekt nicht vorhanden: " + f"{ex}")
    except RuntimeError:
        print(S1 + "kann nicht zugeordnet werden.")
    except Exception as ex:
        print(f"Allgemeiner " + S1 + "{ex}")
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
