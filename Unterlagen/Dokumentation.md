# Dokumentation
Dieses Dokument dient als Informationsquelle der beiliegenden Anwendung.
Vor Nutzung der Anwendung muss diese Dokumentation gelesen sowie die entsprechende Schulung
zur Bedienung der Software absolviert werden.

Diese Dokumentation muss bei Anwendung der Software für alle beteiligten Personen öffentlich zugänglich sein.

## Zweck der Anwendung
Die Anwendung dient dazu, eine Empfehlung zur Einstufung der Höhe des Einkommens von Angestellten eines Technologieunternehmens zu geben.

## Nutzen der Anwendung
Der Nutzen der Anwendung ergibt sich aus mehreren Faktoren.

Die Anwendung vereinfacht den Prozess zum Finden einer angemessenen Eingruppierung des Gehalts von Angestellten.
Durch die Prognose von Gehältern auf Basis von vorhandenen Einkommen von Angestellten mit gleichen oder
ähnlichen Qualifikationen wird schnell eine erste Empfehlung zur Gehaltseinstufung gegeben.

Dies ermöglicht einen schnelleren Durchlauf des Bewerbungsprozesses. Aufwendige händische Vergleiche und
Kalkulationen können minimiert werden.

Durch den automatisierten Prozess, welcher die Prioritäten auf die Berufserfahrung, Bildungsabschluss sowie Position
im Unternehmen setzt, können diskriminierende Entscheidungen, beispielsweise aufgrund des Geschlechtes vermieden werden.
Dies fördert die Fairness im Unternehmen und minimiert die Risiken von Diskriminierung und Ungleichbehandlung.

## Funktionsweise der Anwendung
Zentraler Teil der Anwendung ist das Machine Learning Modell, welches in der Programmiersprache Python
unter Verwendung der Bibliothek Scikit Learn implementiert ist. Dieses wird nachfolgend beschrieben.

### Gradient Boosting Regressor
Das Machine Learnig Modell basiert auf dem Gradient Boosting Verfahren. Dies ist ein Ensemble-Lernverfahren. Das Gradient Boosting Verfahren kombiniert iterativ eine Reihe von schwachen Vorhersagemodellen, um in jedem Durchgang die Fehler des vorhergegangenen Durchgangs zu minimieren.

### Hyperparameteroptimierung
Das Training des Modells erfolgt über GridSearchCV. Dies ist ein Verfahren, welches systematisch eine vorgegebene Auswahl an Hyperparameter-Kombinationen durchläuft und dabei die Kombination identifiziert, welche das optimale Leistungskriterium liefert. Das Leistungskriterium ist in diesem Fall als mittlerer quadratischer Fehler definiert.
Dabei werden folgende Hyperparameter berücksichtigt:
- n_estimators: die Anzahl der Boosting Stufen, also die Anzahl der Bäume, welche hinzugefügt werden. Mehr Bäume können zu einem genaueren Modell führen, erhöhen aber auch das Risiko von Overfitting.
- learning_rate: gibt an, wie stark sich jeder Baum auf die Vorhersage auswirkt. Eine niedrigere Rate erfordert mehr Bäume, kann aber zu präziseren Modellen führen.
- max_depth: begrenzt die Tiefe jeden Baumes. Durch eine größere Tiefe können komplexere Muster erkannt werden, erhöht aber auch das Risiko von Overfitting.
- min_samples_split: Bestimmt die minimale Anzahl an Datensätzen, welche benötigt wird, um einen Knoten weiter aufzuspalten.
- subsample: Bruchteil der Stichproben, welcher für das Wachstum jedes Baumes verwendet wird.

Folgende Parameter bilden den Ausgangspunkt zur Optimierung:\
        'regressor__n_estimators': [100, 500, 1000],\
        'regressor__learning_rate': [0.05, 0.1],\
        'regressor__max_depth': [3, 6, 9],\
        'regressor__min_samples_split': [2, 5],\
        'regressor__subsample': [0.75, 1.0]\


Um die Generalisierung des Modells zu gewährleisten, erfolgt der Prozess der Hyperparameteroptimierung in Kreuzvalidierungsschritten. Das finale Modell wird mit dieser optimalen Kombination aus Hyperparametern erstellt.

### Evaluierung und Feature Importances
Nach der Optimierung der Hyperparameter folgt die Evaluierung der Leistung. Hierfür werden zwei Hauptmetriken verwendet:
- der mittlere quadratische Fehler: misst die durchschnittliche quadratische Differenz zwischen den tatsächlichen und den vom Modell vorhergesagten Gehältern.
- das Bestimmtheitsmaß: gibt an, welcher Anteil der Varianz in den tatsächlichen Gehaltsdaten durch das Modell erklärt wird.

Zur Verbesserung der Interpretiertbarkeit wird der mittlere quadratische Fehler zudem im Verhältnis zum Durchschnittsgehalt betrachtet. Dies ermöglicht den Vergleich des Fehlers im Verhältnis zu den tatsächlichen Gehaltswerten.

Das trainierte Modell weißt folgende Metriken auf:\
R²: 0.99680\
RMSE: 2990.08912\
RMSE in relation to average income: 0.02576\

Um eine Zusätzliche Evaluierungsmöglichkeit zu bieten, werden vor dem Training des Modells 20% der Trainingsdaten abgesplittet. Diese werden nach dem Training als zusätzliche Evaluierungsdaten verwendet. Somit kann die Generalisierung des Modells untersucht werden.

Die Evaluierung zur Feststellung der Generalisierung weist folgende Metriken auf:\
R²: 0.99714\
RMSE: 2832.47745\
RMSE in relation to average income: 0.02434

Ein weiterer zentraler Punkt zur Bewertung des Modells ist die Ausgabe der Feature Importances.
Diese geben Aufschluss darüber, welche Variablen den größten Einfluss auf die Vorhersagen es Modells haben.
Das trainierte Modell weist folgende Feature Importances, gruppiert nach Merkmalen auf:\
Years of Experience: 0.75115\
Job Title: 0.19460\
Age: 0.02716\
Education Level: 0.02701\
Gender: 0.00008\

Das Modell wird zur Wiederverwendung im Produktiveinsatz gespeichert. Dadurch kann das Modell wiederholt genutzt werden, ohne den Trainingsprozess erneut zu durchlaufen.

## Verwendete Daten
Die Trainingsdaten bilden die Grundlage für die späteren Prognosen der Anwendung.
Nachfolgend wird daher auf die Quelle sowie die Bereinigung der Daten eingegangen.

### Quelle der Daten
Die zum Training und zur Evaluierung des Modells verwendeten Daten stammen aus der von Google LLC. betriebenen Plattform Kaggle.

Die Daten wurden aus verschiedenen Quellen erhoben, unter anderem Umfragen, Job-Portalen und anderen öffentlich zugänglichen Quellen.
Insgesamt sind 6704 Datensätze enthalten.
Die Datensätze enthalten die Attribute
- age
- gender
- experience
- job title
- education level
- salary

Die Daten wurden erhoben von
- Reddy, Mohith Sai Ram
- Sukumar, J G
- Sambangi, Nikihileswar

Der Datensatz ist verfügbar unter:
https://www.kaggle.com/datasets/mohithsairamreddy/salary-data/data

### Bereinigung der Daten
Die Trainingsdaten enthalten initial verschiedene Verzerrungen.
Neben der ungleichen Verteilung der Geschlechter lässt sich auch eine unfaire Verteilung der Gehälter feststellen.
Um eine zuverlässige und ausgeglichene Prognose zu ermöglichen ist es notwendig, die Datensätze vor dem Training zu bereinigen und auszugleichen.
Dies erfolgt in mehreren Schritten, welche nachfolgend im Einzelnen beschrieben werden.

#### Grundlegende Bereinigung
Vor der tiefergehenden Optimierung der Datensätze findet eine grundlegende Bereinigung statt.
Diese beinhaltet mehrere Teilschritte:
- Standardisierung von Bezeichnung: da die Bildungsabschlüsse teilweise verschiedene Schreibweisen für den gleichen Abschluss verwenden, werden die Bezeichnungen angeglichen und standardisiert.
- Entfernung fehlerhafter Einträge: Datensätze, welche fehler- oder lückenhafte Werte beinhalten, werden entfernt.
- Konvertierung zu Ganzzahlen: die Gehaltsangaben werden zu ganzzahligen Integer-Werten konvertiert.
- Aufteilung in Trainings- und Evaluierungsdatensätze: der Datensatz wird in einen Trainings- und einen Evaluierungsdatensatz aufgeteilt.

#### Ausbalancieren der Geschlechter
Das Ausbalancieren der Geschlechter stellt einen integralen Bestandteil dar, um später eine ausgeglichene Prognose zu gewährleisten:
- Identifizierung der Geschlechter und Jobkategorien: zuerst werden die Geschlechter extrahiert. Dann wird eine Liste von einzigartigen Jobkategorien erstellt, indem nach Job Title, Years of Experience und Education Level gruppiert wird.
- Durchlaufen der Jobkategorien: für jede identifizierte Jobkategorie wird der Datensatz durchsucht, um alle entsprechenden Einträge zu finden.
- Analyse der Geschlechterverteilung: innerhalb jeder Jobkategorie wird die Anzahl der Datensätze für jedes Geschlecht gezählt um zu bestimmen, ob ein Geschlecht unterrepräsentiert ist.
- Ausgleichen der Geschlechter: wird eine Unterrepräsentation festgestellt, wird ein Gleichgewicht hergestellt. Dies geschieht durch zwei Arten:
  - Duplizieren existierender Datensätze: existieren Datensätze eines Geschlechts bereits, können diese dupliziert werden.
  - Erzeugung synthetischer Datensätze: existieren keine Datensätze für ein Geschlecht in einer Kategorie, wird ein synthetischer Datensatz erzeugt. Dies geschieht, indem ein vorhandener Datensatz kopiert und das Geschlecht entsprechend angepasst wird.

Die angepassten bzw. generierten Datensätze werden dem ursprünglichen Datensatz hinzugefügt, um eine ausgeglichene Geschlechterverteilung für jede Jobkategorie zu gewährleisten.

#### Anpassen der Gehälter
Nachdem die Geschlechter ausbalanciert sind, müssen die Gehälter angeglichen werden:
- Gruppieren der Jobkategorien: wie im Schritt zuvor, werden die Jobs anhand der Merkmale Job Title, Years of Experience und Education Level gruppiert.
- Berechnung des Median-Gehalts: für jede Gruppe wird das Median-Gehalt berechnet.
- Zuordnung des Median-Gehalts zu jedem Datensatz: jedem Datensatz wird das Median-Gehalt seiner jeweiligen Gruppe zugewiesen. Das ursprüngliche Gehalt wird ersetzt.

Diese Schritte führen dazu, dass für jede Kombination der genannten Merkmale ein einheitliches Gehalt hinterlegt ist. Abweichungen, welche durch Merkmale entstehen, welche keinen
Einfluss auf das Gehalt haben sollten (Geschlecht, Alter) werden somit verhindert.

## Nutzung der Anwendung
Die Prognose der Einkommen kann durch zwei verschiedene Modi erfolgen.

In beiden Modi müssen grundsätzlich die gleichen Daten angegeben werden:
- Alter in Jahren
- Geschlecht
- Bildungsabschluss
- Berufserfahrung in Jahren
- Berufsbezeichnung

Die Attributwerte müssen in einem festgelegten Wertebereich liegen:
- Alter: 18 - 70
- Geschlecht: Male, Female, Other
- Bildungsabschluss: Bachelor's, Master's, PhD, High School
- Berufserfahrung: 0 - 50
- Berufsbezeichnung: siehe extra Dokument "Verfügbare Berufsbezeichnungen"

### Interkativer Modus
Im interaktiven Modus werden sequenziell die für die Prognose benötigten Informationen abgefragt.

Die Anwendung wird gestartet durch den Befehl ```python3 model-adjusted.py --prognose --interactive```.
Im Anschluss werden die entsprechenden Informationen abgefragt.
Nachdem alle Daten eingegeben wurden, wird sofort eine Gehaltsangabe ausgegeben.

### Automatischer Modus
Der automatische Modus liest eine Datei mit den benötigten Daten ein und speichert die Prognosen für alle Datensätze wiederum ab.

Hierfür muss eine Datei mit der Bezeichnung *test_data_basic.csv* unter *general/datasets/test_data`* gespeichert werden, welche alle benötigten Informationen beinhaltet.
Eine Vorlage mit Beispiel zum genauen Format der Datei ist unter *test_data_basic.csv* in diesen Unterlagen zu finden.

Nach dem Ablegen der Datei kann die Prognose durch ```python3 model-adjusted.py --prognose --interactive``` durchgeführt werden.
Nach der erfolgreichen Durchführung werden die prognostizierten Daten unter *models/adjusted/datasets/prognosed_data* gespeichert.

## Nutzung der generierten Informationen
Die generierten Informationen dienen als Anhaltspunkt zur Festlegung von Gehältern für Angestellte.

Diese Informationen sind weder verbindlich, noch sollten die Daten ohne weitere Kontrolle übernommen werden.

## Probleme, Gefahren und Grenzen der Anwendung
Trotz sorgfältiger Analysen und Tests können bei der Nutzung der Anwendung Probleme auftreten. Deshalb ist die Anwendung stets mit sorgfältiger Überwachung zu bedienen.
Insbesondere sei auf die nachfolgenden Gefahren hingewiesen.

### Unzuverlässige Prognosen
Es kann nicht sichergestellt werden, dass alle Prognosen eine ausreichende Zuverlässigkeit besitzen.
Dies kann insbesondere der Fall sein, wenn Daten aus unzulässigen Wertebereichen eingegeben werden.

Jede Prognose muss kontrolliert und im Zweifel die angegebenen Werte kritisch hinterfragt werden.

### Unzureichende Erklärbarkeit
Zwar ist beispielsweise durch die Einsicht der Feature Importances eine begrenzte Nachvollziehbarkeit gegeben.
Insgesamt kann eine genaue Erkärbarkeit der Anwendung allerdings nicht gewährleistet werden.
Dies kann wiederum zu unklaren Ausgaben führen, deren Ursache nicht nachvollzogen werden kann.

### Anpassungsfähigkeit an Marktveränderungen
Gehaltsstrukturen können sich durch diverse Faktoren schnell ändern. Die Trainingsdatensätze repräsentieren immer nur Daten über einen bestimmten Zeitraum. Jesto mehr Zeit zwischen der Nutzung der Anwendung und der Erhebung der Trainingsdaten liegen, desto größer ist die Diskrepanz zwischen den Gehaltsinformationen in den Daten und der Realität.

### Individuelle Eigenschaften
Individuelle Eigenschaften und Einzelfälle, welche nicht in die definierten Wertebereiche passen, können nicht angemessen berücksichtigt werden. Spezielle Fähigkeiten oder Erfahrungen können nicht beachtet werden. Das gleiche Problem ergibt sich mit Faktoren wie unternehmensinternen Leistungsbeurteilungen oder der Qualität von Arbeitsergebnissen.

### Berücksichtigung unternehmensspezifischer Faktoren
Jedes Unternehmen hat eine eigene Kultur, organisatorischen Aufbau und eine andere Gehaltspolitik. Spezielle Strukturen, in welchen spezialisierte Anforderungen gestellt werden, können ebenfalls nicht berücksichtigt werden.

### Rechtliche Beschränkungen
Die Verwendung von personenbezogenen Daten unterliegt strengen Richtlinien. Die Einhaltung der Vorschriften kann durch die Anwendung selbst nicht allgemein gewährleistet werden und muss somit im Einzelfall betrachtet werden.

## Veranwortlichkeiten
Die Verantwortung zur Nutzung der Anwendung, inklusive Weiterverarbeitung der generierten Informationen, liegt ausschließlich in der bedienenden Person.

Die Nutzung der Prognosen hat so zu erfolgen, als ob diese vom Anwender selbst oder der für die Gehaltseinstufung zuständigen Person erstellt worden wären.

## Konktaktinformationen
Bei weiteren Fragen oder Problemen zur Anwendung steht die entsprechende Meldestelle zur Verfügung:

Name der Firma\
Name des Ansprechpartners\
Straße, Hausnummer\
PLZ, Ort

Telefon: XXX XXX\
E-Mail: XXX XXX
