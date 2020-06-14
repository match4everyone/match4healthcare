# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.7.0]



### Geändert

- Bump Django requirements to from 3.0.5 to 3.0.7
- Übersetzungen
- Trailing Whitespaces
- Dummy-User Generierung aktualisiert
- Datenschutzerklärung aktualisiert
- Neue Beschriftungen in der Helfendensuchmaske
- Name des Vereins "in Gründung" entfernt
- Kleinere Textänderungen
- Logos auf der Startseite
- Anpassungen an einheitlichen Code-Style
- Generierte Dummy-User: Kennwort gleich Username
- IS_FORK Check (see Readme) aus Log entfernt und in pre-deploy Checks migriert
- Dev/Prod Env ENUM refactored
- Readme aktualisiert
- Nutzungsbedingungen aktualisiert
- Admin-Dashboard überarbeitet
- Link auf neues Youtube Video
- Moved .env files to .env.sample files
- Travis Anpassungen
- Bissfest Logo zu Kooperationspartnern verschoben
- Slack Logger in dev and prod aktiv sobald die Env-Variable gesetzt wird
- Freezed postgres Version

### Hinzugefügt

- Link auf Datenschutzerklärung im Helfendenprofil
- Aufklärung über Datenschutzerklärung
- Datenschutzbeauftragten in Erklärung aufgenommen
- Mapbox-Token in Env-Files verlagert
- Wie funktionert es Infografik
- Verpflichtender Code-Style und Pre-Commit
- Statistik-Seite im Backend
- GitHub Templates für PRs, Issues, etc.
- Pre-Commit in Test Environment
- PEP8 Code-Style
- Automatisches Import sortieren
- Run backend docker as non root
- Don't use sendgrid and disable checks in travis of forks

### Entfernt

- Logik zum (nachträglichen) Bestätigen der Datenschutzerklärung
- Fehler bei Eingabe von Kommazahlen bei Entfernungen
- Hardcoded Mapbox Token in Seiten
- Fehler #440 

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



