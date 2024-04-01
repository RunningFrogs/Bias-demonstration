# Einleitung
Die Anwendung *Bias-demonstration* dient zur praktischen Demonstration von Verzerrungen in Machine Learning Anwendungen,
sowie der Veranschaulichung verschiedener Lösungsansätze im Rahmen einer Bachelorarbeit.

In diesem Repository gibt es drei Modelle:
- Original
- No Gender
- Adjusted

Die Unterschiede dieser Modelle werden im Verlauf dieses Dokuments erläutert.

# Struktur des Repositorys
Das Repository weiß folgende Struktur auf:
- Bias-demonstration:
  - config
      - paths.py: enthält alle Pfade, welche in der Anwendung benötigt werden
  - general: enthält allgemeine Dateien, welche nicht modellspezifisch sind, sondern für alle Modelle gleichermaßen gelten, sowie verschiedene Analysen
      - analysis: enthält diverse Daten zur Generierung von Auswertungen und Analysen
          - results: enthält die Ergebnisse der Auswertungen, unterteilt in die verschiedenen Modelle sowie die Art der Daten (Trainingsdaten, Testdaten, prognostizierte Daten)
          - src: enthält die Python-Scripte zur Analyse der Daten sowie Generierung der Diagramme
      - datasets: enthält diverse Datensätze und Quelldateien
          - src: enthält die Scripte zur Erstellung von Testdaten sowie der initialen Bereinigung der Trainingsdaten
      - test_data: enthält verschiedene Versionen der generierten Testdatan
      - training_data: enthält die unbereinigten sowie die initial bereinigten Trainingsdaten
  - models: enthält die verschiedenen Modelle
      - adjusted: enthält das Modell "adjusted"
          - data_preparation
              - src: enthält die Quelldatei zum Bereinigen der Trainingsdaten für dieses Modell
          - datasets: enthält verschiedene modellspezifische Datensätze
              - prognosed_data: enthält die von diesem Modell prognostizierten Daten
              - training_data: enthält die für dieses Model bereinigten Trainingsdaten
          - prognosis
              - model: enthält verschiedene Metriken zum Modell sowie das Modell selbst
              - src: Enthält die Quelldateien für das Training und die Evaluierung des Modells sowie die Scripte zur Prognose von Daten mithilfe des Modells
      - no_gender: enthält die gleiche Struktur wie "adjusted", nur mit anderem Modell
      - original: enthält die gleiche Struktur wie "adjusted", nur mit anderem Modell
  - Unterlagen: enthält Schulungsunterlagen sowie die Dokumentation der Anwendung im Rahmen der Bachelorarbeit
  - verschiedene Quelldateien zum Training der Modelle und Vorbereiten der Trainingsdatensätze

# Allgemeine Bedienung
### Bereinigung der initialen Trainingsdaten
Die Trainingsdaten müssen in einem CSV-File die Attribute *Age, Gender, Education Level, Job Title, Years of Experience* und *Salary* enthalten.
Die Datei mit dem Namen *training_data_unprepared.csv* muss unter *general/datasets/training_data/* gespeichert sein.

Mit ```python3 preparation.py --prepare``` wird eine grundlegende Bereinigung der Daten durchgeführt. Hierdurch werden Datensätze mit leeren oder fehlerhaften
Werten entfernt sowie die Bezeichnungen der Abschlüsse vereinheitlicht. Die bereinigten Trainingsdaten werden unter *general/datasets/training_data/training_data_prepared_basic.csv* gespeichert

### Generierung von Testdaten
Um die Modelle testen zu können, müssen Testdaten erstellt werden. Dies geschieht durch ```python3 preparation.py --generate <Anzahl Testdatensätze>```

Dadurch werden drei Testdatensätze erstellt.
- test_data_basic: Standard Testdaten mit allen Attributen, außer Geschlecht
- test_data_expanded: Hierbei sind die standard Testdaten erweitert. Jeder Datensatz in den standard Testdaten existiert hier für jedes Geschlecht. Somit wird jede Kombination der Attributwerte für jedes Geschlecht kopiert.
- test_data_without_gender: Basiert ebenfalls auf die standard Testdaten. Hier existieren Allerdings die Attribute *Gender* und *Age* nicht.

Diese verschiedenen Testdatensätze werden später zum Testen der verschiedenen Modelle benötigt.

### Modellspezifische Bereinigung der Trainingsdaten
Neben der initialen Bereinigung der Trainingsdaten werden diese noch einmal modellspezifisch vorbereitet.

- original: die Bereinigung für das originale Modell funktioniert genau so, wie schon bei der initialen Bereinigung.
- no_gender: bei den Datensätzen für *no_gender* werden die Attribute *Gender* sowie *Age* entfernt.
- adjust: die Geschlechter werden durch Resampling und der Generierung synthetischer Daten ausbalanciert und die Gehälter ausgeglichen.

#### Anpassen der Gehälter
Nachdem die Geschlechter ausbalanciert sind, müssen die Gehälter angeglichen werden:
- Gruppieren der Jobkategorien: Wie im Schritt zuvor, werden die Jobs anhand der Merkmale Job Title, Years of Experience und Education Level gruppiert.
- Berechnung des Median-Gehalts: Für jede Gruppe wird das Median-Gehalt berechnet.
- Zuordnung des Median-Gehalts zu jedem Datensatz: Jedem Datensatz wird das Median-Gehalt seiner jeweiligen Gruppe zugewiesen. Das ursprüngliche Gehalt wird ersetzt.

Diese Schritte führen dazu, dass für jede Kombination der genannten Merkmale ein einheitliches Gehalt hinterlegt ist. Abweichungen, welche durch Merkmale entstehen, welche keinen
Einfluss auf das Gehalt haben sollten (Geschlecht, Alter) werden somit verhindert.

Die modellspezifische Bereinigung der Trainingsdaten geschieht durch den Aufruf der Modelle mit den entsprechenden Parametern:
- original: ```python3 original-model.py --prepare```
- no_gender: ```python3 model-no-gender.py --prepare```
- adjusted: ```python3 adjusted-model.py --prepare```

Neben der Bereinigung werden in diesem Schritt automatisch 20% der Trainingsdaten abgesplittet, um sie nach dem Training als Evaluierungsdaten zu verwenden.
Somit kann die Generalisierung der Modelle getestet werden.

### Training der Modelle
Nachdem die Trainingsdaten entsprechend der Modelle vorbereitet wurden, können die Modelle selbst trainiert werden.
Dies geschieht durch folgende Aufrufe:
- original: ```python3 original-model.py --train```
- no_gender: ```python3 model-no-gender.py --train```
- adjusted: ```python3 adjusted-model.py --train```

*original* besteht aus dem grundlegenden Modell.

Bei *no_gender* werden die Attribute *Age* sowie *Gender* nicht berücksichtigt, welche auch in den Trainingsdaten nicht enthalten sind.

*adjusted* verwendet die ausgeglichenen Trainingsdaten. Zudem enthält dieses Modell ausführliches Logging.

Nach dem Training werden bei allen Modellen in den Verzeichnissen des Modells die Trainingsmetriken gespeichert.
Beim *adjusted*-Modell werden neben den Metriken auch die Feature Importances ausgegeben und gespeichert.

### Evaluierung der Modelle
Nachdem die Modelle trainiert wurden, kann deren Generalisierung mithilfe der vorher von den Trainingsdaten abgespalteten
Evaluierungsdaten getestet werden.

Dies geschieht durch ```python3 <Modellbezeichnung> --evaluate```.

Hierdurch werden die entsprechenden Evaluierungsmetriken ausgegeben und gespeichert.

### Prognose der Einkommen
Die Prognose der Einkommen kann durch zwei verschiedene Modi erfolgen:
- Interaktiv: hierbei werden sequenziell die benötigten Informationen abgefragt. Am Ende wird eine Prognose ausgegeben.
- Automatisch: unter *general/datasets/test_data* kann eine CSV-Datei mit den entsprechenden Attributen gespeichert werden. Wie vorher beschrieben, werden für diese Demonstration Testdaten generiert. Alle Datensätze in dieser Datei werden dann durchlaufen und die entsprechende Prognose unter *models/<Modellbezeichnung>/datasets/prognosed_data' gespeichert.

Der interaktive Modus wird gestartet durch: ```python3 <Modellbezeichnung> --prognose --interactive```

Der automatische Modus wird gestartet durch: ```python3 <Modellbezeichnung> --prognose --automated```

### Analyse der Daten
Alle Trainings-, Test- und Prognosedatensätze (außer *no_gender*) können ausführlich analysiert werden.

Dies geschieht durch ```python3 analysis.py <Parameter 1> <Parameter 2>```.

Dabei sind folgende Parameter und Parameterkombinaionen möglich:
- ```--test```: Analysiert die Testdaten
- ```--original --training```: Analysiert die Trainingsdaten des Originalmodells, also die Trainingsdaten nach der initialen Bereinigung
- ```--original --prognosis```: Analysiert die prognostizierten Daten des originalen Modells
- ```--adjusted --training```: Analysiert die ausbalancierten Trainingsdaten des *adjusted*-Nodells
- ```--adjusted --prognosis:``` Analysiert die prognostizierten Daten des *adjusted*-Modells

Alle Analysen sind unter *general/analysis/results* zu finden.

Die Art und Menge der Analysen und Grafiken hängt von den verwendeten Parametern bzw. den verwendeten Datensätzen ab.
