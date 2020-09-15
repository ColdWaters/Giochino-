import csv, json, glob

def editor(row_local):
    temp = {}
    temp["cards__effects__influence"] = row_local.get("cards__effects__influence")
    temp["cards__effects__wealth"] = row_local.get("cards__effects__wealth")
    row_local.pop("cards__effects__influence")
    row_local.pop("cards__effects__wealth")
    row_local["effects"] = temp
    return row_local

def GetNameFaction(imput_gnf):
    temp = imput_gnf.split(" ")
    temp = temp[2].split(".")
    return temp[0].lower()

#assegna alla variabile poth_in il nome del file .csv
#se sono presenti più file CSV nello stesso percoso, il programma prende in considerazione il primo in ordine alfabetico
path_in = glob.glob('*.csv')[0]

#prende la fazione dal nome del file, eliminando estensioni di file e altre porcherie. nota: tutti i file .csv devono essere nomitati secondo la loro fazione.
faction = GetNameFaction(path_in)
jsonFilePath = f"{faction}.js"



#il dizionario data_out viene usato per assemblare i dati prima di essere trasferiti in JSON
data_out = {}

#legge il file CSV
with open(path_in) as file_csv:
    #la funzione DictReader legge il file CSV colonna per colonna
    reader = csv.DictReader(file_csv)

    rows = list(reader)

    for counter in range(len(rows)):
        editor(rows[counter])


    data_out[faction] = rows


with open(jsonFilePath, "w") as f:
    json.dump(data_out, f, indent=4)
