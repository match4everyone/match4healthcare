# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.6.0]

### Geändert

- Fixed #430 Javascript problems on older iOs Devices

## [1.6.0-rc1]

### Hinzugefügt
- Links zu allen Supporterlogos auf der Startseite
- added license agreement for images
- System Checks (see Readme):
  - Mailversand über Sendgrid API Test
  - Umgebungsvariablen gesetzt
  - Aufruf in Deployment-Skript
- Model für Newsletterversand
- UI für Newsletterversand
- Sendgrid Client API für Newsletterversand
- Einstellung für Anzahl nötiger Newsletter-Genehmigungen vor Versand
- Slack Channel Log Handler für Benachrichtigung über Fehler
- JSON Routen für Einrichtungen und Helfer*innen zum dynamischen Nachladen in die Karte
- Komplett neue Implementierung der Karte mit https://github.com/Leaflet/Leaflet.markercluster und ein- und ausschaltbarer Anzeige von Helfern und Einrichtungen in einer Karte
- Logging von Anmeldeversuchen
- Neues Logfile-Format: JSON
- Neues Logfile-Format: Text mit Exceptions auf einer Zeile
- Postgres Major Version im Dockerfile fixiert
- Zeitstempel auf der Datenbank für Audit-Zwecke
- Prüfung ob Text eingegeben wurde, bevor ein Mail versendet werden kann

### Geändert
- new design for language switcher
- new logos and structure landing page
- Redirect nach Login für Einrichtungen auf Profil
- Versionen in requirements.txt eingefroren
- requirements und requirements.prod neu sortiert
- Übersetzungen
- PLZs für Wiener Stadtgebiet angepasst
- Karte im Menü einfach in Karte umbenannt (bzw. "Einrichtungen finden" für Helfer)
- Neue Logging-Konfiguration
- Log File Format in JSON geändert und Dateinamen geändert
- Sendgrid Key wird nun in Dev und Prod aus dem Environment gelesen
- Korrekte Helfer und Einrichtungsberechnung auf der Karte
- Deploy-Skript Reihenfolge von migrate und den anderen Schritten geändert

### Entfernt
- CDN Einbindung von bootstrap, jQuery, leaflet und popper entfernt aus Datenschutzgründen
- Überflüssige jQuery Einbindung
- Bug: e-mail an Einrichtungen wurden nicht in DB gespeichert nach dem Senden
- Bug: Versenden von Mails an Einrichtungen schlägt fehl, weil der Mailtext fälschlicherweise im Betreff-Feld gespeichert wird bei Längen über 200 Zeichen
- Bug: Ungültige Postleitzahlen führen zum Abbruch bei Registrierung und Profiländerung
- Filenames aus .po files für weniger Merge-Konflikte

## [1.5.1]

### Hinzugefügt
- Links zu allen Supporterlogos auf der Startseite

### Geändert

### Entfernt

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
