# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.5] - 2020-04-06

### Hinzugefügt
- Versendete eMails auf Datenbank nach Sendevorgang gruppieren, Voraussetzung für Anzeige gesendeter e-Mails später
- Migrationsskript für Mailgruppierung
- Neue Qualifikation Medstudent/Arzt -> Allgemeinmedizin
- Datenbankmigration für neue Qualifikationen
- An Einrichtungen eine Kopie der ausgesendeten Mails senden
- Sprachenwahl im zentralen Menü
- Übersetzung der Auswahlboxen auf der Registrierungsseite und im Filter
- Hinweis auf Open-Source Projekt auf der Startseite: "100% ehrenamtlich und uneigennützig von Studierenden als Open-Source Projekt entwickelt"
- Neuer abgesprochener Text für Einrichtungs-Dashboard aus Testfeedback
- Erde-icon für Sprachenwahl
- Github-Link im Footer hinzugefügt
- Logo marburger bund dauerhaft eingefügt (vorher nur als hot-fix)
- ÖH-Logos auf Start-Seite
- Anzeige der Helferdetails aus der Helfersuche
- Anzeige der registrierten Einrichtungen auf der Gesuche-Karte
- Eigenes Map-Design für Einrichtungen, muss wahrscheinlich noch überarbeitet werden.
- Hackathon Teammitglieder aus Ursprungsteam zur About-Seite hinzugefügt
- Bissfest Logo hinzugefügt

### Geändert
- Herumfliegenden Text auf der "Kennwort setzen" Seite aus dem Nimbus geholt und zum Formular gepackt
- Design Seite "Datenschutzerklärung zustimmen" für Institutionen verbessert
- Überarbeitung aller Übersetzungen
- Fehlerbehebung: Limit von 200 Mails wurde irrtümlich auf Lebenszeit und nicht pro Tag berechnet
- fixes #174: Auswahlfelder für Assistenzarzt, Facharzt, usw. am Handy nicht auswählbar
- fixes #375:  Auswahlfelder für Assistenzarzt, Facharzt, usw. mit Tab nicht erreichbar
- Verschiedenste kleine Textänderungen
- Text in Bausteine aufteilen zur besseren Übersetzbarkeit
- Filterseite: "Unterkunft kann angeboten werden" statt "Unterkunft gewünscht"
- HTTPS-Links statt HTTP in Validierungsmails
- Klarere Darstellung der Trennung zwischen Opensource-Entwicklerteam und Match4healthcare als Verein
- Einrichtungskarte eingeblendet wenn man als Student angemeldet ist, als "Gesuche" in Navigationsleiste
- Tabellenanzeige in der Helfersuche verbessert
- Anzeige schalten als Einrichtung auf eigene Seite ausgelagert
- Anzeige der registrierten User jetzt nur noch validierte

### Entfernt
- viele Rechtschreibfehler
- Doppelte Logos entfernt
- Doppelter Aufruf jQuery entfernt
