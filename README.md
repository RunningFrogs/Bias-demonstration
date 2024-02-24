# Anwendung
Nachfolgend werden die Funktionen der Anwendung *Bias-demonstration* aufgeführt und die Anwendung erklärt.

## Bereinigung der Daten
Bevor das Modell trainiert werden kann, sollten die Trainingsdaten bereinigt werden. Dies geschieht durch
`python3 bias-demonstration.py --prepare`.

Hierdurch werden
- Datensätze mit leeren Attributwerten entfernt
- Nachkommastellen entfernt
- Unterschiedliche Schreibweisen der Abschlüsse vereinheitlicht

Zudem werden 20% der Trainingsdaten in eine eigene Datei unter *datasets/training_data/evaluation_data.csv*
gespeichert, um nach dem Training den Grad der Generalisierung zu kontrollieren.

Die bereinigten Trainingsdaten werden unter *datasets/training_data_prepared.csv* gespeichert. Unter *data_preparation/cleanup_log.txt* kann eingesehen werden,
welche Bereinigungen durchgeführt wurden.

## Trainieren des Modells
Um das Modell zu trainieren, wird eine csv-Datei mit den Attributen
- Age
- Gender
- Education Level
- Job Title
- Years of Experience
- Salary
unter *datasets/training_data/training_data_unprepared.csv* gespeichert.

Nach der Bereinigung kann das Modell mit `python3 bias-demonstration.py --train` trainiert werden.

Als Machine Learning Modell wird Gradient Boosting Regressor verwendet.
Zur Hyperparameteroptimierung wird GridSearchCV angewandt.

Das trainierte Modell wird unter *prognosis/model/model.joblib* gespeichert.

Unter *prognosis/model/metrics.txt* können verschiedene
Metriken zum Modell eingesehen werden.

## Evaluierung des trainierten Modells
Mittels `python3 bias-demonstration --evaluate` kann das die Genauigkeit des Modells anhand der
bei der Bereinigung abgesplitteten Daten getestet werden. Die Metriken der Evaluierung können unter
*prognosis/model/evaluation_metrics.txt* eingesehen werden.

## Testdaten generieren
Um das Modell zu testen, können automatisch Testdaten generiert werden.
Die geschieht durch `python3 Bias-demonastraion.py --generate <Anzahl Datensätze>`.

Es werden Testdaten generiert, welche aus zufälligen Wertkombinationen bestehen.
Um zu überprüfen, welche Unterschiede das Geschlecht bei ansonst gleichen Attributen hat,
wird jede Zufallskombination der Attributwerte für jeweils jedes Geschlecht generiert.

*Salary* wird nicht generiert, da dieses Attribut anhand der anderen Attributwerte prognostiziert werden soll.

## Prognosen erstellen
Kern der Anwendung ist die Prognose von Gehältern. Hierfür werden zwei Möglichkeiten angeboten:
- Interaktive Prognose
- Automatische Prognose

### Interaktive Prognose
Die interaktive Prognose frägt die benötigten Informationen einzeln vom Nutzer ab und gibt im Anschluss
eine Gehaltsprognose.

Die interaktive Prognose wird gestartet durch `python3 bias-demonstration.py --prognose --interactive`.

### Automatische Prognose
Sollen mehrere Prognosen auf einmal generiert werden, können diese in einer csv-Datei unter *datasets/test_data*
bereitgestellt werden (s. Abschnitt *Testdaten generieren*).

Mit `python3 bias-demonstraion.py --prognose --automated` werden alle Gehälter prognostiziert und
unter *data/prognosed_data.csv* gespeichert.

## Analyse der Daten
Um einen besseren Überblick über die Trainings-, Test- und prognostizierten Daten zu erhalten, können diese
grafisch dargestellt werden und eine Zusammenfassung über die wichtigsten Informationen gegeben werden.

Dies geschieht durch `python3 bias-demonstration.py --analyze <Daten>`.

Der Paramter *<Daten>* gibt an, welche Daten analysiert werden sollen
- Trainingsdaten: `training`
- Testdaten: `test`
- Prognosen: `prognosis`

Unter *analysis/results* können die entsprechenden Auswertungen eingesehen werden.