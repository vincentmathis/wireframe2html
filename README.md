# Installation

Die Dependencies können mit `pipenv` ([GitHub](https://github.com/pypa/pipenv), [Docs](https://pipenv.kennethreitz.org/en/latest/)) installiert werden.
```
pipenv install
```
> Das Programm beinhalted ein trainiertes Modell. Der Code für das Training ist in [train.ipynb](train.ipynb) zu finden. Jupyter Notebook gehört zu den *dev-dependencies*, welche mit `pipenv install --dev` installiert werden können. 

> Sollte die Installation der Dependencies mit `pipenv` nicht funktionieren liegt dies wahrscheinlich an den CUDA requirements der `torch` und `torchvision` packages. Die dependencies sind im [Pipfile](../Pipfile) aufgelistet. Mit `python -m venv .venv` kann manuell ein `virutalenv` angelegt werden. Die dependencies können darin mit `pip` installiert werden.

Danach kann eine `shell` in dem `virtualenv` so gestartet werden:
```
pipenv shell
```

# Verwendung

## Kommandozeile
Das Programm kann so direkt von der Kommandozeile gestartet werden:
```
python cli.py <path to image file>
```
> Beispielbilder für die Eingabe sind im Ordner [test](/test) zu finden
Standardmäßig wird die Ausgabe in `output.html` geschrieben, der Dateiname der Ausgabe kann aber auch spezifisch angegeben werden:
```
python cli.py <path to image file> -o <path to output file>
```

## GUI
Alternativ kann die experimentelle GUI so gestartet werden:
```
python gui.py
```
Über das `File` Menü können die Operationen manuell gestartet werden. Die Operationen können auch über diese Hotkeys gestartet werden:
* `Strg+O` um eine Datei zu öffnen
* `Strg+P` um Vorhersagen im Bild zu treffen
* `Strg+G` um die HTML-Datei zu generieren
