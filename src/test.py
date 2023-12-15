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
# ----------------------------------------------------------------------------
import os
import datetime
from openai import OpenAI

# ----------------------------------------------------------------------------
# get openai api key per environment variable:
# ----------------------------------------------------------------------------
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
)

# ----------------------------------------------------------------------------
# get current time
# ----------------------------------------------------------------------------
current_time = datetime.datetime.now().strftime('%H:%M')
promptt = f"Es ist {current_time}."

# ----------------------------------------------------------------------------
re_1 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "assistant", "content": "Hallo Welt" },
        { "role": "user", "content": "Viele Programmierer, vor allen Anfänger, ist das erste Programm, das sie in der Programmiersprache BASIC geschrieben (PRINT \"Hallo Welt\"), immer das erste, was sie mit 'Hallo Welt' assozieren." },
    ],
    temperature = 0.7,
    max_tokens = 200,
    top_p = 1,
)
# ----------------------------------------------------------------------------
re_2 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "Was bedeutet Welt" },
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
        { "role": "system", "content": "Beschreibe mir die Welt" },
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
        { "role": "system", "content": "Beschreibe mir die Welt" },
        { "role": "user", "content": "Die Welt hat viele Facetten." },
        { "role": "user", "content": "Die Welt ist Teil der Milchstraße." },
    ],
    temperature = 0.7,
    max_tokens = 200,
    top_p = 1,
)
# ----------------------------------------------------------------------------
re_5 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "Ist die Welt noch zu retten" },
        { "role": "user", "content": "Die Welt befindet sich sehr nah am Abgrund." },
        { "role": "user", "content": "Die Welt wird durch den Kapitalismus leider sehr stark in Mitleidenschaft gezogen." },
        { "role": "user", "content": "Früher hatte die Welt mehr Eis und Schnee im Winter." },
    ],
    temperature = 0.7,
    max_tokens = 200,
    top_p = 1,
)
# ----------------------------------------------------------------------------
re_6 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": "Wieso brauchen wir die Welt" },
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
        { "role": "system", "content": "Für wem ist die Welt" },
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
