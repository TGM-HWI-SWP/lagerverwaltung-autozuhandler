# Changelog - Julian

Persönliches Changelog für **Julian**, Rolle: **GUI & Interaktion**

---

## [v0.1] - 2026-03-05

### Implementiert
- Erste lokale GUI mit Tkinter eingebaut und mit `src.main` verbunden
- Run-Script ergänzt
- Grundstruktur für die lokale Benutzeroberfläche vorbereitet

### Tests geschrieben
- Manuelle Tests für:
  - Start der Anwendung
  - Öffnen der GUI
  - Grundlegende Interaktion mit der Oberfläche

### Commits
```text
- feat(gui): add tkinter UI and wire app via src.main
- add run script
```

### Mergekonflikt(e)
- Keine

---

## [v0.2] - 2026-03-06

### Implementiert
- README aktualisiert
- Erste Gradio-Dummy-UI erstellt
- Beginn der Umstellung von lokaler GUI auf browserbasierte Oberfläche

### Tests geschrieben
- Manuelle Tests für:
  - Start mit Gradio
  - Sichtbarkeit der Oberfläche
  - grundlegendes Verhalten der Dummy-UI

### Commits
```text
- update README
- feat: add gradio dummy ui
```

### Mergekonflikt(e)
- Keine

---

## [v0.3] - 2026-03-10

### Implementiert
- Gradio-Datei erweitert
- Benutzeroberfläche inhaltlich ausgebaut
- Oberfläche auf weitere Funktionen vorbereitet

### Tests geschrieben
- Manuelle Tests für:
  - Layout
  - Felddarstellung
  - Startverhalten der erweiterten Gradio-Oberfläche

### Commits
```text
- gradio datei erweitern
```

### Mergekonflikt(e)
- Keine

---

## [v0.4] - 2026-03-11

### Implementiert
- Nextcloud mit Collabora verbunden
- Buttons in der Oberfläche überarbeitet
- Admin-Namen angepasst
- Fehlende Felder bei Outputs ergänzt
- Kleine GUI-Details verbessert
- Titel der Anwendung geändert

### Tests geschrieben
- Manuelle Tests für:
  - Buttons
  - Ausgabe-Felder
  - Titelanzeige
  - Nextcloud-/Collabora-Anbindung
  - Eingabe- und Ausgabevollständigkeit

### Commits
```text
- nextcloud mit collabora
- buttons geändert
- Admin Namen geändert
- fehlende felder hinzufügen bei outputs
- einfaches detail geändert
- Titel geändert
```

### Mergekonflikt(e)
- Keine größeren dokumentierten Konflikte

---

## [v0.5] - 2026-03-13

### Implementiert
- GUI mit Gradio in die neue Projektstruktur eingebunden
- Oberfläche an die modulare Architektur angepasst
- GUI für die Zusammenarbeit mit `app_context`, Services und Reports vorbereitet

### Tests geschrieben
- Manuelle Integrationstests für:
  - Start mit neuer Ordnerstruktur
  - GUI-Verhalten nach Strukturänderung
  - Zusammenspiel mit der neuen Architektur

### Commits
```text
- GUI mit gradio implementiert
```

### Mergekonflikt(e)
- Kleinere Integrationskonflikte durch neue Struktur
- Lösung: GUI an neue Architektur angepasst

---

## [v0.6] - 2026-03-20

### Implementiert
- Changelog-Dateien mit vorbereitet
- Merge-Konflikte gelöst und lokale Architektur beibehalten
- Services aus GUI-Sicht überarbeitet
- Schnittstellen mit GUI zusammengesetzt
- Oberfläche weiter an die modulare Architektur angepasst

### Tests geschrieben
- Manuelle Tests für:
  - GUI nach Konfliktlösung
  - Startverhalten nach Architekturänderungen
  - Zusammenspiel von GUI, Services und Reports

### Commits
```text
- changelog files
- Resolve merge conflicts keeping local architecture
- Resolve merge conflicts keeping local architecture
- Überarbeitung der Services
```

### Mergekonflikt(e)
- `src/adapters/memory_repositories.py`: Konflikt zwischen lokalem und Remote-Stand, lokal gelöst
- `src/app_context.py`: Konflikt in der Integrationslogik, lokal gelöst
- `src/ports/repositories.py`: Konflikt in der Schnittstellenstruktur, lokal gelöst

---

## [v0.7] - 2026-03-27

### Implementiert
- Eigenes Changelog weitergeführt
- Persönliche Dokumentation ergänzt
- Eigene Arbeit nachvollziehbar dokumentiert

### Tests geschrieben
- Keine neuen technischen Tests
- Dokumentationskontrolle durchgeführt

### Commits
```text
- Changelog Pavek
```

### Mergekonflikt(e)
- Keine

---

## [v0.8] - 2026-04-24

### Implementiert
- Report B und MongoDB in den Projektstand integriert
- Finale GUI-nahe Gesamtintegration unterstützt
- Anwendung auf erweiterten Endstand vorbereitet

### Tests geschrieben
- Manuelle End-to-End-Tests für:
  - Start der App
  - GUI-Gesamtverhalten
  - Integration neuer Funktionen
  - Stabilität nach Erweiterung um Report B und MongoDB

### Commits
```text
- report b und mongodb
- changelog vollendet
```

### Mergekonflikt(e)
- Späte Integrationsanpassungen im Gesamtprojekt
- Lösung: Anpassung an den finalen Projektstand

---

## Zusammenfassung

**Gesamt implementierte Features:** 15  
**Gesamt geschriebene Tests:** 0 automatisierte, mehrere manuelle GUI- und Integrationstests  
**Gesamt Commits:** 13 relevante eigene Commits  
**Größte Herausforderung:** Die GUI parallel zur Umstellung auf die modulare Architektur funktionsfähig zu halten und Konflikte sauber aufzulösen  
**Schönste Code-Zeile:**  
```python
demo = create_ui(app_context)
```

---

**Changelog erstellt von:** Julian  
**Letzte Aktualisierung:** 2026-04-24