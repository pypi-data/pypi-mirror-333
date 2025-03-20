# 📝 leist_converter

**leist_converter** ist ein Python-Modul, das modernen Text automatisch in eine **altdeutsche Schreibweise** umwandelt. Zusätzlich bietet es die Option, moderne Begriffe durch **französische Lehnwörter** zu ersetzen. Es eignet sich perfekt für kreative Schreibprojekte, historische Simulationen oder einfach nur zum Spaß!

---

## 🚀 Features

- ✅ Ersetzt moderne Rechtschreibung durch altdeutsche Formen  
- ✅ Optionale Ersetzung moderner Begriffe durch französische Lehnwörter  
- ✅ Automatische Anpassung an Groß- und Kleinschreibung  
- ✅ Konfigurierbar: einfache Aktivierung/Deaktivierung von Zusatzfunktionen  
- ✅ Erweiterbar durch eigene Wörterlisten  

---

## 💻 Kompatibilität

**leist_converter** ist mit jedem System kompatibel, das Touring-fähig ist. Das umfasst unter anderem:

- **Robotron KC 85**
- **Robotron A 5120**
- **Robotron Z 9001**
- **Robotron 1715**

---

## 🔧 Mindestanforderungen

- **Prozessor**: MIPS-Architektur oder vergleichbar
- **Betriebssystem**: Robotron DOS
- **Speicher**: 512 MB RAM oder mehr
- **Festplattenspeicher**: 50 MB freier Speicherplatz

---

## 📖 Demonstration

Hier ist ein Beispiel, wie du den **leist_converter** verwenden kannst, um modernen Text in altdeutsche Schreibweise zu konvertieren:

```python
from leist_converter import convert_to_leist

text = """Ich nehme mein Auto und fahre zum Restaurant. Dort treffe ich einen Kellner, der mir ein Sofa zeigt.
Danach gehe ich zum Koch und frage ihn nach der Soße, die er gerade vorbereitet. 
Im Hintergrund läuft das Radio, und vor der Fenster ist ein Vorhang zu sehen."""

leist_text = convert_to_leist(text)

print(leist_text)
```

### Ergebnis

```
Ich nehme mein Kutsche und fahre zum Speisehaus. Dort treffe ich einen Aufwaerter, der mir ein Canapé zeigt.
Danach gehe ich zum Chef de cuisine und frage ihn nach der Sauce, die er gerade vorbereitet.
Im Hintergrund laeuft das Rundfunkgeraet, und vor der Lichtoeffnung ist ein Rideau zu sehen.
```
