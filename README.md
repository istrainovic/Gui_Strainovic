# 🏀 Textadventure goes GUI – Basketball RPG

## 🎮 Projektidee

Dieses Projekt ist eine moderne Erweiterung eines klassischen Textadventures – komplett umgesetzt mit einer grafischen Benutzeroberfläche (GUI) in **Python** mithilfe von **CustomTkinter (CTk)**.  
Im Zentrum steht ein aufstrebender Basketballspieler, der sich durch Training, Sponsorenverträge und gute Presse bis zum Star hocharbeiten will.

---

## 💻 Features (GUI)

- 🖱️ **Komplette Steuerung über Buttons, Dropdowns und Labels**
- 🎨 **Individuelle Spielerstellung** (Name, Position, Herkunft, Style, Accessoire, Größe, Gewicht)
- 🏋 **Gym** – Training mit XP-Gewinn und Energieverbrauch
- 💼 **Agentur** – Verträge mit Follower-Anforderungen
- 🛍️ **Shop** – Items & Skins kaufen, abhängig vom Geld, mit Feedback
- 🧼 **Locker Room** – Ausrüstung über simuliertes Drag & Drop anlegen/entfernen
- 🎯 **Field** – Minigame mit Aktionen (Werfen, Passen, Verteidigen)
- 📰 **Pressekonferenz** – Fragen beantworten, Follower gewinnen oder verlieren
- 🎮 **Lounge** – Musik, Entspannung, Wiederherstellung
- 📈 **Dynamische Statusleiste** (XP, Energie, Follower, Geld, Rückennr.)

---

## 🧑‍💻 Technische Umsetzung

- ✅ **GUI-Framework**: [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- ✅ **Eigene GUI-Klasse**, erbt korrekt von `ctk.CTk`
- ✅ **Strukturierte Raum-Module** (`modules/room/`)
- ✅ **Trennung von Logik & Oberfläche**
- ✅ **Skalierbares Design**: Fenstergrößen anpassbar (klein/mittel/vollbild)
- ✅ **Soundeffekte**: Bei Events wie Vertragsabschluss, Trainingserfolg, Fehlversuch

---

## 📝 Aufgabenstellung (abgedeckt)

> 📌 *„Erweitere dein bisheriges Textadventure um eine GUI mit CTk. Kein Terminal, nur GUI.“*

✅ Alle Ein- und Ausgaben laufen **ausschließlich** über die GUI  
✅ GUI ist modular, sauber strukturiert und vollständig spielbar  
✅ **Kein Terminal** wird benötigt

---

## 🛠️ Installation

```bash
pip install customtkinter pygame pillow
