import csv, json

import tkinter as tk
from tkinter import filedialog

#lista degli elementi che non devono essere indentati
ban_list = ["province", "confini"]

def OnlyFilenames(imput): #la funzione OnlyFilenames prende in imput i percorsi dei diversi file, e ritorna una lista con solo i namefile
    place = []
    for vac in imput:
        vac = vac.split("/")
        place.append(vac[-1])
    return place

def editor(row_local): #la funzione editor permette di indentare i valori cards__effects__influence e cards__effects__wealth nel file JSON
    temp = {}

    if faction not in ban_list:
        temp["cards__effects__influence"] = row_local.get("cards__effects__influence")
        temp["cards__effects__wealth"] = row_local.get("cards__effects__wealth")
        row_local.pop("cards__effects__influence")
        row_local.pop("cards__effects__wealth")
        row_local["card_effects"] = temp
        return row_local

    elif faction == "province":
        temp["province_influence"] = row_local.get("province_influence")
        temp["province_wealth"] = row_local.get("province_wealth")
        temp["province_population"] = row_local.get("province_population")
        row_local.pop("province_influence")
        row_local.pop("province_wealth")
        row_local.pop("province_population")
        row_local["province_value"] = temp
        return row_local

def GetNameFaction(imput_gnf): #La funziona GetNameFaction prende il nome della fazione a partire dal namefile
    temp = imput_gnf.split(" ")
    temp = temp[2].split(".")
    return temp[0].lower()

#assegna alla variabile poth_in il nome del file .csv
#il programma prende in imput una lista di file selezionati dall'utente, tramite una finestra di dialogo
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilenames(title = "Seleziona un file CSV",filetypes = (("CSV Files","*.csv"),))

for path_in in OnlyFilenames(file_path):

    #prende la fazione dal nome del file, eliminando estensioni di file e altre porcherie. nota: tutti i file .csv devono essere nomitati secondo la loro fazione.
    faction = GetNameFaction(path_in)
    jsonFilePath = f"{faction}.js"


    #il dizionario data_out viene usato per assemblare i dati prima di essere trasferiti in JSON
    data_out = {}
    data_out_2 = {}

    #legge il file CSV
    with open(path_in) as file_csv:
        #la funzione DictReader legge il file CSV colonna per colonna
        reader = csv.DictReader(file_csv)

        rows = list(reader)

        for counter in range(len(rows)):
            editor(rows[counter])

            data_out[faction] = rows

            if faction == "province":
                data_out_2["map_data"] = data_out

            elif faction == "eventi":
                data_out_2["eventi_deck"] = data_out

            elif faction == "confini":
                data_out_2["logistic"] = data_out

            else:
                data_out_2["deck"] = data_out

    with open(jsonFilePath, "w") as f:
        json.dump(data_out_2, f, indent=4)
