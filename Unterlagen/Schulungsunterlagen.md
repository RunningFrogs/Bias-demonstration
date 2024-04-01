# Schulungsunterlagen
Diese Unterlagen dienen zur Schulung von Anwendern der Software zur Empfehlung von Gehältern.

Durch die Schulung erwerben die Anwender Kenntnisse über den Zweck, Funktionen sowie der korrekten Bedienung der Anwendung,
wie die Ergebnisse zu interpretieren sind, wie die Daten genutzt werden können und wo die Möglichkeiten und Grenzen
des Tools liegen.

Die Arbeit mit dem Programm ist nur erlaubt, sofern die Anwender die Unterweisung komplett abgeschlossen haben.

Werden weitere Informationen benötigt, können diese in der Dokumentation eingesehen werden.
Im Zweifel stehen Ansprechpartner zur Verfügung, welche ebenfalls in der Dokumentation hinterlegt sind.

## Zweck der Anwendung
Die Anwendung dient dazu, eine Empfehlung zur Einstufung der Höhe des Einkommens von Mitarbeitern eines Technologieunternehmens zu geben.

## Entstehung der Ergebnisse
Die Entstehung der Ergebnisse ist ein Prozess, welcher auf mehreren Stufen basiert.
Hier wird nur ein kurzer Überblick über die Funktionsweise gegeben, um einen Einblick in die Technologie zu erhalten.
Für tiefergehende Informationen zur Funktionsweise und der Anwendung an sich sei auf die Dokumentation oder
auf die in der Dokumentation hinterlegten Kontaktinformationen verwiesen.

### Datensammlung und -bereinigung
Ein zentraler Schritt in der Entwicklung von Machine Learning Anwendungen ist das Sammeln von Daten.
Anhand der Daten kann das Modell trainiert werden, um später Prognosen anhand unbekannter Daten zu treffen.

Die für diese Anwendung benötigten Trainingsdaten enthalten die Attribute
- Alter
- Geschlecht
- Berufserfahrung
- Berufsbezeichnung
- Bildungsabschluss
- Gehalt

Die Daten stammen aus Umfragen, Jobportalen und anderen öffentlich zugänglichen Quellen.

Nachdem die Daten gesammelt wurden folgt die Bereinigung. Diese dient dazu, die Datensätze von Unstimmigkeiten und Verzerrungen zu befreien.
Dazu werden
- Begrifflichkeiten vereinheitlicht
- Fehlerhafte Einträge entfernt
- Die Geschlechter ausgeglichen, damit sie fair repräsentiert werden
- Die Gehaltsdaten angeglichen, um die Gehaltsangaben über die Geschlechter hinweg ausgeglichen darzustellen

### Bildung des Modells
Den Kern der Anwendung bildet das Machine Learning Modell, welches mit dem sogenannten Gradient Boosting Verfahren arbeitet.
Machine Learning bezeichnet vereinfacht gesagt ein Programm, das beispielsweise mit den hier genannten Daten trainiert wird.
Es "lernt" somit die Zusammenhänge zwischen den verschiedenen Merkmalen und dem Gehalt.

Nachdem das Training abgeschlossen ist, kann man dem Programm neue, unbekannte Daten zuführen. Das Modell kann dann anhand
der übergebenen Informationen das Gehalt für die in den neuen Daten existierenden Zusammenhänge errechnen.

Das Gradient Boosting Verfahren nutzt eine Sammlung an Modellen, welche nacheinander arbeiten. Somit werden die Prognosen schrittweise
verbessert und die Genauigkeit der Prognosen wird gesteigert.

Durch bestimmte Parameter kann die Leistung des Modells optimiert werden. Mithilfe eines Verfahrens namens GridSearchCV werden
automatisch verschiedene Parameterkombinationen getestet, um die beste Konfiguration für das Modell zu finden.

Nachdem das Modell trainiert wurde, wird es evaluiert.
Hier werden spezifische Metriken wie der mittlere quadratische Fehler und das Bestimmtheitsmaß herangezogen, um zu bewerten,
wie genau das Modell arbeitet. Zudem können zur Kontrolle die sogenannten Feature Importances ausgegeben werden.
Diese geben an, wie stark der Einfluss einzelner Merkmale auf die Vorhersage ist.

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
- Berufsbezeichnzung: siehe extra Dokument "Verfügbare Berufsbezeichnungen"

### Interkativer Modus
Im interaktiven Modus werden sequenziell die für die Prognose benötigten Informationen abgefragt.

Die Anwendung wird gestartet durch den Befehl ```python3 model-adjusted.py --prognose --interactive```.
Im Anschluss werden die entsprechenden Informationen abgefragt.
Nachdem alle Daten eingegeben wurden, wird sofort eine Gehaltsangabe ausgegeben.

### Automatischer Modus
Der automatische Modus liest eine Datei mit den benötigten Daten ein und speichert die Prognosen für alle Datensätze wiederum ab.

Hierfür muss eine Datei mit der Bezeichnung *test_data_basic.csv* und *general/datasets/test_data`* gespeichert werden, welche alle benötigten Informationen beinhaltet.
Eine Vorlage mit Beispiel zum genauen Format der Datei ist unter *test_data_basic.csv* in diesen Unterlagen zu finden.

Nach dem Ablegen der Datei kann die Prognose durch ```python3 model-adjusted.py --prognose --interactive``` durchgeführt werden.
Nach der erfolgreichen Durchführung werden die prognostizierten Daten und *models/adjusted/datasets/prognosed_data* gespeichert.

## Interpretation der Ergebnisse
Die Prognosen sind das Ergebnis aus dem Training des Modells und den zugeführten Daten.

Die Ausgabe der Anwendung ist keine an Individuen angepasste Beurteilung in diesem Sinne.
Vielmehr stellt sie die wahrscheinliche Einstufung des Einkommens anhand der übergebenen Faktoren auf Basis
der Trainingsdaten dar.

Das bedeutet zum einen, dass keine Kompetenzen außerhalb der definierten Merkmale berücksichtigt werden.
Zu anderen, dass die Resultate immer nur aus Rückschlüssen von Zusammenhängen bestehen, welche in den Trainingsdaten erkannt wurden.

Die Resultate stellen also keine individuelle, zwingend gerechtfertigte Angabe zum Einkommen dar.
Vielmehr geben sie einen ersten Anhaltspunkt, um auf Basis der prognostizierten Gehälter eine Entscheidung unter Einfluss
weiterer Faktoren wie Soft-Skills und Spezialfähigkeiten zu treffen, welche bei der automatisierten Prognose nicht berücksichtigt werden.

## Nutzung der generierten Informationen
Die generierten Informationen dienen als Anhaltspunkt zur Festlegung von Gehältern für Angestellte.

Diese Informationen sind weder verbindlich, noch sollten die Daten ohne weitere Kontrolle übernommen werden.

## Automation Complacency und Automation Bias
Automation Complacency beschreibt das Phänomen, dass Menschen zu sehr auf automatisierte Systeme vertrauen und dadurch ihre eigene Wachsamkeit verringern. Dies kann dazu führen, dass Nutzer wichtige Veränderungen im System übersehen, weil sie davon ausgehen, dass die Anwendung alle Aufgaben korrekt ausführt.

Automation Bias bezeichnet die Tendenz von Menschen, Entscheidungen und Empfehlungen von automatisierten Systemen selbst dann zu folgen, wenn sie fehlerhaft sind.

Es ist wichtig, dass die Nutzer der Anwendung alle bereitgestellten Informationen stets genau überwachen und kontrollieren.
Sollten Unregelmäßigkeiten oder unklare Ausgaben auftreten, muss die Prognose immer hinterfragt und im Zweifel durch eine menschliche Instanz überstimmt werden.

## Grenzen der Anwendung
Für die Nutzung der Anwendung im alltäglichen Betrieb sind vor allem folgende Punkte zu beachten:
- Es gibt sehr wenig Erklärbarkeit hinter den Ergebnissen: Zwar ist es durch die genannten Feature Importances grundsätzlich möglich, einen gewissen Einblick in das System zu erhalten. Genaue Rückschlüsse, wieso bestimmte Resultate entstanden sind, gibt es aber in der Regel nicht.
- Unzuverlässige Prognosen: Es kann nicht sichergestellt werden, dass alle Prognosen eine ausreichende Zuverlässigkeit besitzen.
Dies kann insbesondere der Fall sein, wenn Daten aus unzulässigen Wertebereichen eingegeben werden. Jede Prognose muss werden und im Zweifel die angegebenen Werte kritisch hinterfragt werden.
- Individuelle Eigenschaften: Indiviuelle Eigenschaften und Einzelfälle, welche nicht in die definierten Wertebereiche passen, können nicht angemessen berücksichtigt werden. Spezielle Fähigkeiten oder Erfahrungen können nicht beachtet werden. Das gleiche Problem ergibt sich mit Faktoren wie unternehmensinternen Leistungsbeurteilungen oder der Qualität von Arbeitsergebnissen.

Für eine ausführliche Beschreibung der Probleme, Gefahren und Grenzen der Anwendung sei auf die Dokumentation verwiesen.
