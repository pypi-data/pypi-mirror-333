import re, json
import importlib.resources as pkg_resources
from . import resources

# Basisersetzungen (Umlaute, ß)
REPLACEMENTS = {
    "ß": "ss",
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "Ä": "Ae",
    "Ö": "Oe",
    "Ü": "Ue"
}

def load_woerterbuch():
    with pkg_resources.open_text(resources, "word_mappings.json", encoding="utf-8") as file:
        return json.load(file)

# Lade die Wörter aus der JSON-Datei
woerter = load_woerterbuch()

# Veraltete Wörter und französische Lehnwörter
OLD_WORDS = {k.lower(): v for k, v in woerter['old_words'].items()}
FRENCH_WORDS = {k.lower(): v for k, v in woerter['french_words'].items()}

def convert_to_leist(text: str, *, erweitern: bool = True, franz_modus: bool = True) -> str:
    """
    Konvertiert modernen Text in altdeutsche Schreibweise, mit französischem Modus.
    
    :param text: Der Eingabetext.
    :param erweitern: Wendet zusätzliche alte Rechtschreibregeln an.
    :param franz_modus: Ersetzt moderne Begriffe durch französische Lehnwörter.
    :return: Der umgewandelte Text.
    """

    # Umlaute und ß ersetzen
    for original, replacement in REPLACEMENTS.items():
        text = text.replace(original, replacement)

    # Erweiterte Altdeutsche Regeln
    if erweitern:
        text = _anwenden_alte_rechtschreibung(text)

    # Französische Wörter
    if franz_modus:
        text = _ersetze_franzoesische_lehnwoerter(text)

    return text

def _anwenden_alte_rechtschreibung(text: str) -> str:
    # Erzeuge ein Pattern mit allen alten Wörtern
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, OLD_WORDS.keys())) + r')\b', re.IGNORECASE)

    # Ersetze die Wörter, unter Beibehaltung des Original-Casings
    return pattern.sub(lambda m: _case_preserve(m.group(), OLD_WORDS[m.group().lower()]), text)

def _ersetze_franzoesische_lehnwoerter(text: str) -> str:
    # Erzeuge ein Pattern mit allen französischen Wörtern
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, FRENCH_WORDS.keys())) + r')\b', re.IGNORECASE)

    # Ersetze die Wörter, unter Beibehaltung des Original-Casings
    return pattern.sub(lambda m: _case_preserve(m.group(), FRENCH_WORDS[m.group().lower()]), text)

def _case_preserve(original: str, replacement: str) -> str:
    """Passt die Groß-/Kleinschreibung des Replacements an das Originalwort an."""
    if original.isupper():
        return replacement.upper()
    elif original[0].isupper():
        return replacement.capitalize()
    else:
        return replacement.lower()
