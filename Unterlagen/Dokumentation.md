# Dokumentation
Dieses Dokument dient als Informationsquelle der beiliegenden Anwendung.
Vor Nutzung der Anwendung muss diese Dokumentation gelesen sowie die entsprechende Schulung
zur Bedienung der Software absolviert werden.

Diese Dokumentation muss bei Anwendung der Software für alle beteiligten Personen öffentlich zugänglich sein.

## Zweck der Anwendung
Die Anwendung [Name der Anwendung] dient dazu, eine Empfehlung zur Einstufung der Höhe des Einkommens von Angestellten Technologieunternehmens zu geben.

## Nutzen der Anwendung
Der Nutzen der Anwendung ergibt sich aus mehreren Faktoren

Die Anwendung vereinfacht den Prozess zum finden einer angemessenen Eingruppierung des Gehalts von Angestellten.
Durch die Prognose von Gehältern auf Basis von vorhandenen Einkommen von Angestellten mit gleichen oder
ähnlichen Qualifikationen wird schnell eine erste Empfehlung zur Gehaltseinstufung gegeben.

Dies ermöglicht einen schnelleren Durchlauf des Bewerbungsprozesses. Aufwendige händische Vergleiche und
Kalkulationen können minimiert werden.

Durch den automatisierten Prozess, welcher die Prioritäten auf die Berufserfahrung, Bildungsabschluss sowie Position
im Unternehmen setzt, können diskriminierende Entscheidungen, beispielsweise aufgrund des Geschlechtes vermieden werden.
Dies fördert die Fairness im Unternehmen und minimiert die Risiken von Diskriminierung und Ungleichbehandlung.

## Funktionsweise der Anwendung
Zentraler Teil der Anwendung ist das Machine Learning Modell. Dieses wird nachfolgend beschrieben.

### Gradient Boosting Regressor
Den zentralen Teil der Anwendung bildet das Machine Learning Modell, welches auf dem Gradient Boosting Verfahren basiert. Dies ist ein Ensemble-Lernferfahren. Das Gradient Boosting Verfahren kombiniert iterativ eine Reihe von schwachen Vorhersagemodellen, um in jedem Durchgang die Fehler des vorhergegangenen Durchgangs zu minimieren.

### Hyperparameteroptimierung
Das Training des Modells erfolgt über GridSearchCV. Dies ist ein Verfahren, welches systematisch eine vorgegebene Auswahl an Hyperparameter-Kombinationen durchläuft und dabei die Kombination identifiziert, welche das optimale Leistungskriterium liefert. Das Leistungskriterium ist in diesem Fall als mittlerer quadratischer Fehler definiert.
Dabei werden folgende Hyperparameter berücksichtigt:
- n_estimators: die Anzahl der Boosting Stufen, also die Anzahl der Bäume, welche hinzugefügt werden. Mehr Bäume können zu einem genaueren Modell führen, erhöhen aber auch das Risiko von Overfitting.
- learning_rate: gibt an, wie stark sich jedr Baum auf die Vorhersage auswirkt. Eine niedrigere Rate erfordert mehr Bäume, kann aber zu präziseren Modellen führen.
- max_depth: begrenzt die Tiefe jeden Baumes. Durch eine größere Tiefe können komplexere Muster erkannt werden, erhöht aber auch das Risiko von Overfitting.
- min_samples_split: Bestimmt die minimale Anzahl an Datensätzen, welche benötigt wird, um einen Knoten weiter aufzuspalten.
- subsample: Bruchteil der Stichproben, welcher für das Wachstum jedes Baumes verwendet wird.

Folgende Parameter bilden den Ausgangspunkt zur Optimierung:
        'regressor__n_estimators': [100, 500, 1000],
        'regressor__learning_rate': [0.05, 0.1],
        'regressor__max_depth': [3, 6, 9],
        'regressor__min_samples_split': [2, 5],
        'regressor__subsample': [0.75, 1.0]


Um die Generalisierung des Modells zu gewährleisten, erfolgt der Prozess der Hyperparameteroptimierung in Kreuzvalidierungsschritten. Das finale Modell wird mit dieser optimalem Kombination aus Hyperparametern erstellt.

### Evaluierung und Feature Importance
Nach der Optimierung der Hyperparameter folgt die Evaluierung der Leistung. Hierfür werden zwei Hauptmetriken verwendet:
- der mittlere quadratische Fehler: misst die durchschnittliche quadratische Differenz zwischen den tatsächlichen und den vom Modell vorhergesagten Gehältern.
- das Bestimmtheitsmaß: gibt an, welcher Anteil der Varianz in den tatsächlichen Gehaltsdaten durch das Modell erklärt wird.

Zur Verbesserung der Interpretiertbarkeit wird der mittlere quadratische Fehler zudem im Verhältnis zum Durchschnittsgehalt betrachtet. Dies ermöglicht den Vergleich des Fehlers im Verhältnis zu den tatsächlichen Gehaltswerten.

Das trainierte Modell weißt folgende Metriken auf:

Um eine Zusätzliche Evaluierungsmöglichkeit zu bieten, werden vor dem Training des Modells 20% der Trainingsdaten abgesplittet. Diese werden nach dem Training als zusätzliche Evaluierungsdaten verwendet. Somit kann die Generalisierung des Modells untersucht werden.

Die Evaluierung zur Feststellung der Generalisierung weißt folgende Metriken auf:


Ein weiterer zentraler Punkt zur Bewertung des Modells ist die Ausgabe der Feature Importances.
Diese gibt Aufschlüss darüber, welche Variablen den größten Einfluss auf die Vorhersagend es Modells haben.

Zur Verbesserung der Interpretierbarkeit der Modellleistung wird der RMSE (Root Mean Squared Error) auch im Verhältnis zum Durchschnittsgehalt betrachtet. Diese Metrik bietet einen Einblick in die Größenordnung des Fehlers im Vergleich zu den tatsächlichen Gehaltswerten.

Ein wichtiger Aspekt des Modelltrainings ist auch die Analyse der Feature-Importanz. Die Feature-Importanz gibt Aufschluss darüber, welche Variablen den größten Einfluss auf die Vorhersagen des Modells haben. Diese Analyse hilft dabei, zu verstehen, auf welcher Grundlage das Modell seine Vorhersagen trifft, und kann wichtige Einblicke für Entscheidungsträger und Analysten liefern. Im spezifischen Kontext des Gradient Boosting können die Importanzen aus den Entscheidungsbäumen aggregiert werden, um die Wichtigkeit einzelner Features zu bewerten.

Das trainierte Modell weißt folgende Feature Importances, gruppiert nach Merkmalen auf:

Das Modell wird zur Wiederverwendung im Produktiveinsatz gespeichert. Dadurch kann das Modell wiederholt genutzt werden, ohne den Trainingsprozess erneut zu durchlaufen.

## Verwendete Daten
Die Trainingsdaten bilden die Grundlagen für die späteren Prognosen der Anwendung.
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
- Konvertierung zu Ganzzahlen: Die Gehaltsangaben werden zu ganzzahligen Integer-Werten konvertiert.
- Aufteilung in Trainings- und Evaluierungsdatensätze: der Datensatz wird in einen Trainings- und einen Evaluierungsdatensatz aufgeteilt.

#### Ausbalancieren der Geschlechter
Das Ausbalancieren der Geschlechter stellt einen integralen Bestandteil dar, um später eine ausgeglichene Prognose zu gewährleisten:
- Identifizierung der Geschlechter und Jobkategorien: Zuerst werden die Geschlechter extrahiert. Dann wird eine Liste von einzigartigen Jobkategorien erstellt, indem nach Job Title, Years of Experience und Education Level gruppiert wird.
- Durchlaufen der Jobkategorien: Für jede identifizierte Jobkategorie wird der Datensatz durchsucht, um alle entsprechenden Einträge zu finden.
- Analyse der Geschlechterverteilung: Innerhalb jeder Jobkategorie wird die Anzahl der Datensätze für jedes Geschlecht gezählt um zu bestimmen, ob ein Geschlecht unterrepräsentiert ist.
- Ausgleichen der Geschlechter: Wird eine unterrepräsentation festgestellt, wird ein Gleichgewicht hergestellt. Dies geschieht durch zwei Arten:
  - Duplizieren existierender Datensätze: existieren Datensätze eines Geschlechts bereits, können diese dupliziert werden.
  - Erzeugung synthetischer Datensätze: existieren keine Datensätze für ein Geschlecht in einer Kategorie, wird ein synthetischer Datensatz erzeugt. Dies geschieht, indem ein vorhandender Datensatz kopiert und das Geschlecht entsprechend angepasst wird.

Die angepassten bzw. generierten Datensätze werden dem ursprünglichen Datensatz hinzugefügt, um eine ausgeglichene Geschlechterverteilung für jede Jobkategorie zu gewährleisten.

#### Anpassen der Gehälter
Nachdem die Geschlechter ausbalanciert sind, müssen die Gehälter angeglichen werden:
- Gruppieren der Jobkategorien: Wie im Schritt zuvor, werden die Jobs anhand der Merkmale Job Title, Years of Experience und Education Level gruppiert.
- Berechnung des Median-Gehalts: Für jede Gruppe wird das Median-Gehalt berechnet.
- Zuordnung des Median-Gehalts zu jedem Datensatz: Jedem Datensatz wird das Median-Gehalt seiner jeweiligen Gruppe zugewiesen. Das ursprüngliche Gehalt wird ersetzt.

Diese Schritte führen dazu, dass für jede Kombination der genannten Merkmale ein einheitliches Gehalt hinterlegt ist. Abweichungen, welche durch Merkmale entstehen, welche keinen
Einfluss auf das Gehalt haben sollten (Geschlecht, Alter) werden somit verhindert.

## Probleme und Gefahren der Anwendung

## Nutzung der Anwendung

## Nutzung der generierten Informationen

## Grenzen der Anwendung

## Veranwortlichkeiten

## Konktaktinformationen
