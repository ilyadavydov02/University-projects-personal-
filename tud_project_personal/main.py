# Here is my student project. I will upload the task to it to the repository

import h5py
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import HDFStore
import pylab

filename = "*here is filename*"  # In the version of my code for TUD, here is the file

print('all keys:')
store = pd.HDFStore(filename)
print(store.keys())  # keys, falls der Benutzer sie nicht kennt
store.close()
print('')

with pd.HDFStore(filename) as store:  # DataFrame Werte für meinen Schlüssel
    data_1 = store['Radius_1000/Center_node_J50/Rescue_node_J128/demand']
    data_2 = store['Radius_1000/Center_node_J50/Rescue_node_J128/pressure']
    data_3 = store['Radius_1000/Center_node_J50/Rescue_node_J128/req_demand']

print('demand DataFrame (Aufgabe 1a):')
print(data_1)
print(type(data_1))
print('')

print('pressure DataFrame (Aufgabe 1a):')
print(data_2)
print(type(data_2))
print('')

print('req_demand DataFrame (Aufgabe 1a):')
print(data_3)
print(type(data_3))
print('')


def metadaten_eines_objects(Pfad, Attribute_name):
    '''Diese Funktion gibt den Wert des Attributs aus. Wenn kein Wert vorhanden ist, wird ein Fehler ausgegeben'''
    with h5py.File(filename, "r") as f:
        keys = f[Pfad].attrs.keys()
        if Attribute_name in keys:  # überprüfen, ob ein Attribut vorhanden ist
            print('Wert "', Attribute_name, '" für Pfad "', Pfad, '" :', f[Pfad].attrs[Attribute_name])
        else:
            print('Ein Attribut mit diesem Namen ist für diesen Pfad nicht vorhanden')


# Ausgaben von Werten aller Attribute, die in Aufgabe 1b angegeben sind.
# Wenn das Attribut nicht vorhanden ist, wird ein Fehler ausgegeben.
print('Aufgabe 1b:')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/demand', 'timestamp')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/pressure', 'timestamp')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/req_demand', 'timestamp')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/demand', 'simulator')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/pressure', 'simulator')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/req_demand', 'simulator')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/demand', 'py_version')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/pressure', 'py_version')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/req_demand', 'py_version')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/demand', 'wntr_version')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/pressure', 'wntr_version')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/req_demand', 'wntr_version')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/demand', ' simulator_version')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/pressure', ' simulator_version')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/req_demand', 'simulator_version')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/demand', 'quantity')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/pressure', 'quantity')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/req_demand', 'quantity')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/demand', 'units')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/pressure', 'units')
metadaten_eines_objects('Radius_1000/Center_node_J50/Rescue_node_J128/req_demand', 'units')
print('')

print('Datengültigkeitsprüfung (Aufgabe 1c):')


def datengültigkeitsprüfung(center_node_index):
    '''Diese Funktion überprüft die Gültigkeit der Daten, indem Sie die req_demand Werte für Center_node ab dem Zeitschritt von 14.400 Sekunden addiert'''
    req_demand_werte = data_3[center_node_index]
    print(req_demand_werte)
    if req_demand_werte.loc[14400.0:].sum() == 0:
        print('die Summe =', req_demand_werte.loc[14400.0:].sum(), '. Die Daten sind plausibel.')
        print('')
    else:
        print('die Summe =', req_demand_werte.loc[14400.0:].sum(), '. Die Daten sind nicht plausibel.')
        print('')


datengültigkeitsprüfung('J50')  # J50 ist mein center_node_index


def bedarfserfüllung():
    '''Diese Funktion gibt zurück ein pandas DataFrame mit der prozentualen Bedarfserfüllung für jeden
Verbraucherknoten zu jedem Zeitschritt'''
    data_1_new = data_1.drop(
        columns=['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'R1'])  # Reduzieren demand auf die Einträge für junctions
    global data_b
    data_b = data_1_new / data_3  # Bedarfserfüllung DataFrame bekommen
    data_b = data_b.dropna(axis=1,
                           how="any")  # alle Spalten, bei denen die Division durch 0 den Eintrag NaN ausgelöst hat entfernen
    print('Bedarfserfüllung DataFrame (Aufgabe 2a):')
    print(data_b)
    print('')


bedarfserfüllung()

print('Mittelwert und Standardabweichung (Aufgabe 2b):')
data_x1 = data_b.mean(axis=1)  # Mittelwert
data_x2 = data_b.std(axis=1)  # Standardabweichung
data_b_new = data_b.assign(average_value=data_x1, standardabweichung=data_x2)  # neue Spalten hinzufügen
print(data_b_new)
print('')

print('Aufgabe 2c:')


def pressure_werte(node_a, node_b, node_c, node_d, node_e):
    '''Übergeben Sie an diese Funktion die Namen von 5 Knoten, von denen 1 Rescue_mode ist,
    und erhalten Sie den Mittelwert des Drucks und Standartabweichung'''
    data_50 = data_2[node_a]  # wir erhalten die Werte jedes Knotens
    data_128 = data_2[node_b]
    data_1170 = data_2[node_c]
    data_156 = data_2[node_d]
    data_26 = data_2[node_e]
    dataa = {node_a: data_50, node_b: data_128, node_c: data_1170, node_d: data_156, node_e: data_26}
    global data_2c
    data_2c = pd.DataFrame(dataa)  # einen DataFrame erstellen
    data_xx1 = data_2c.mean(axis=1)  # Mittelwert
    data_xx2 = data_2c.std(axis=1)  # Standardabweichung
    data_2c = data_2c.assign(average_value=data_xx1, standardabweichung=data_xx2)  # neue Spalten hinzufügen
    print(data_2c)
    print('')


pressure_werte('J50', 'J128', 'J5', 'J28', 'J337')

# Aufgabe 3a
data_b_new['zeit'] = data_b_new.index  # wir fügen eine Indexspalte hinzu, um Code zu erleichtern
plt.errorbar(x=data_b_new['zeit'], y=data_b_new['average_value'], yerr=data_b_new['standardabweichung'], fmt='o-',
             ecolor='red')
plt.title('mittlere Bedarfserfüllung (mit Standardabweichung)')
plt.xlabel('Zeit')
plt.ylabel('Werten')
plt.show()

# Aufgabe 3b
data_2c['zeit'] = data_2c.index
plt.errorbar(x=data_2c['zeit'], y=data_2c['average_value'], yerr=data_2c['standardabweichung'], fmt='o-', ecolor='red')
plt.title('mittlere Druck (mit Standardabweichung)')
plt.xlabel('Zeit')
plt.ylabel('Werten')
plt.show()

# Aufgabe 3c
fig = plt.figure()

ax_1 = fig.add_subplot(3, 1, 1)
ax_2 = fig.add_subplot(2, 1, 2)

ax_1.set(title='mittlere Bedarfserfüllung (mit Standardabweichung)')
ax_1.set(xlabel='Zeit, s')
ax_1.set(ylabel='Werten')
ax_1.errorbar(x=data_b_new['zeit'], y=data_b_new['average_value'], yerr=data_b_new['standardabweichung'], fmt='o-',
              ecolor='red')
ax_2.set(title='mittlere Druck (mit Standardabweichung)')
ax_2.set(xlabel='Zeit, s')
ax_2.set(ylabel='Werten')
ax_2.errorbar(x=data_2c['zeit'], y=data_2c['average_value'], yerr=data_2c['standardabweichung'], fmt='o-', ecolor='red')

plt.show()
