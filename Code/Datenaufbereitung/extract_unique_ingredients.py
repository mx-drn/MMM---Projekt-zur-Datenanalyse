import re
import json
from bs4 import BeautifulSoup as bs

def setstatus(str):
    switcher = {
        '== Description ==\n': 1,
        '=== Ingredients ===\n': 2,
        '== Directions ==\n': 3,
        '== See also ==\n': 4
    }
    return switcher.get(str)

def zutaten():
    zutaten = []


    zutatenunique = []



    with open("Unique_Zutaten.txt", "r", encoding='utf8') as zutatentxt:
        content = zutatentxt.readlines()

        for zutat in content:
            istzutat = re.search("\[\[(.*?)\]\]", zutat)

            # wenn zutaten durch | separiert
            zutatistmehrere = re.search("|", zutat)

            if istzutat:
                if zutatistmehrere:
                    zut = istzutat.group(1)
                    str = zut.replace("|", "\n")
                    zutaten.append(str)
                    continue

                if istzutat.group(1) in zutaten:
                    continue
                else:
                    zutaten.append(istzutat.group(1))

    with open("Unique_Zutaten_clean.txt", "w", encoding='utf8') as zutatentxt:
        for zutat in zutaten:
            i = i+1
            zutatlow = zutat.lower()
            zutatenunique.append(zutatlow)

            if zutatenunique.count(zutatlow) > 1:
                continue
            else:
                if ":" in zutat:
                    continue
                else:
                    zutatentxt.write(zutatlow + '\n')


def kategorien():
    kategorien = []
    zutaten = []

    with open("Unique_Zutaten_clean.txt", "r", encoding='utf8') as zutatentxt:
        context = zutatentxt.readlines()

        for line in context:
            zutaten.append(line)


    with open("cleantext.txt", "r", encoding='utf8') as file:
        context = file.readlines()

        for line in context:
            istkategorie = re.search("\[\[(Category:(.*?))\]\]", line)

            kategorieistmehrere = re.search("|", line )

            if istkategorie:
                if kategorieistmehrere:
                    kat = istkategorie.group(2)
                    str = kat.replace("|", "")
                    kategorien.append(str)
                    continue
                if istkategorie.group(2) in kategorien:
                    continue
                else:
                    kategorien.append(istkategorie.group(2))

    wichtige_kategorien = []

    with open("Verteilung_Kategorien.json", "w", encoding='utf8') as file:
        kategorien_verteilung = {}
        kategorien_relevant = {}
        kategorien_txt = []

        for kat in kategorien:
            if kat not in zutaten:
                if kat.lower() in kategorien_verteilung:
                    kategorien_verteilung[kat.lower()] = kategorien_verteilung[kat.lower()]+1
                    if kategorien_verteilung[kat.lower()] > 20:
                        wichtige_kategorien.append(kat.lower)
                else:
                    kategorien_verteilung[kat.lower()] = 1
        counter = 0
        for kat in kategorien_verteilung:
            if kategorien_verteilung.get(kat) > 100:
                kategorien_relevant[kat] = kategorien_verteilung.get(kat)
                kategorien_txt.append(kat.lower())
                counter += 1


        kat_unqiue = list(set(wichtige_kategorien))
        wichtige_kategorien = kat_unqiue

        versuch = {kategorie: anzahl for kategorie, anzahl in sorted(kategorien_verteilung.items(), key=lambda item: item[1])}
        relevant = {kategorie: anzahl for kategorie, anzahl in sorted(kategorien_relevant.items(), key=lambda item: item[1])}

        with open("Kategorien_relevant.json", "w", encoding='utf8') as rel:
            json.dump(relevant, rel)
        #print(len(kategorien_relevant))
        json.dump(versuch, file)

        kategorien_txt = list(set(kategorien_txt))

        with open("Wichtige_Kategorien.txt", "w", encoding="utf8") as txt:
            for kat in kategorien_txt:
                if kat.replace("recipes", "").strip()+'\n' in zutaten:
                    continue
                else:
                    txt.write(kat + "\n")



def trainingsdaten():
    with open("cookbook_2019.xml", "r", encoding='utf8') as file:
        # with open("cookbook_2019 - Kopie.xml", "r", encoding='utf8') as file:
        content = file.readlines()
        content = "".join(content)

        print("parsing with lxml")
        bs_content = bs(content, "lxml")

        print("finding text-tags!")
        texttag = bs_content.find_all("text")

        zutaten = []
        kategorien = []
        idcounter = 0
        dictlist = []


        with open("Unique_Zutaten_clean.txt", "r", encoding="utf8") as zutatentxt:
            context = zutatentxt.readlines()

            for zeile in context:
                zutaten.append(zeile.replace("\n", ""))

        with open("Wichtige_Kategorien.txt", "r", encoding="utf8") as kategorientxt:
            context = kategorientxt.readlines()

            for zeile in context:
                kategorien.append(zeile.replace("\n", ""))

        for element in texttag:
            textvonelement = element.text
            templistzutat = []
            #finden aller matches auf das regex
            matches = re.findall("\[\[(.*?)\]\]", textvonelement)
            tempkategorien = list(set(re.findall("\[\[(Category:(.*?))\]\]", textvonelement)))

            tempgemischt = []

            #alle weiteren matches appenden
            for e in matches:
                # test ob ein | vorhanden ist -> meistens bei Zutaten
                istmehrere = re.search("|", e)

                # falls | vorhanden
                if istmehrere:
                    templist = e.split("|")

                    for temp in templist:
                        tempgemischt.append(temp)
                    continue


                tempgemischt.append(e)

            #duplikate löschen
            tempgemischt = list(set(tempgemischt))

            #aussortieren der Kategorien und uninteressanten Zutaten
            for e in tempgemischt:
                if e.lower() in zutaten:
                    templistzutat.append(e.lower())

            tempkategorien = list(set(tempkategorien))
            tempkatliste = []

            #Zusammenstellen des dict
            for k in tempkategorien:
                if "Category:" not in k:
                    tempkatliste.append(k[1].lower())


            aussortiert = []

            for t in tempkatliste:
                if t in kategorien:
                    aussortiert.append(t)


            if len(aussortiert) == 0 or len(templistzutat) == 0:
                continue



            tempdict = {}

            #id vergeben
            tempdict["id"] = idcounter


            #id weiterlaufen lassen
            idcounter += 1

            #Kategorie vergeben
            tempdict["category"] = aussortiert

            #Zutaten vergeben
            tempdict["ingredients"] = templistzutat

            dictlist.append(tempdict)


            #templistzutat.clear()
            #tempgemischt.clear()



    with open("Trainingsdaten_800.json", "w", encoding="utf8") as dumpfile:
        json.dump(dictlist, dumpfile, indent=2)


def trainingsdaten_split():
    with open("cookbook_2019.xml", "r", encoding='utf8') as file:
        # with open("cookbook_2019 - Kopie.xml", "r", encoding='utf8') as file:
        content = file.readlines()
        content = "".join(content)

        print("parsing with lxml")
        bs_content = bs(content, "lxml")

        print("finding text-tags!")
        texttag = bs_content.find_all("text")

        zutaten = []
        kategorien = []
        idcounter = 0
        vocablist = []

        #Kategorien fürs splitten
        gangart = []
        laender = []
        mahlzeit = []
        sonstige = []
        vegan = []

        #listen für alle Splits
        listgang = []
        listlaender = []
        listmahlzeit = []
        listsonstige = []
        listvegan = []

        with open("cookingvocabulary.txt", "r", encoding="utf8") as vocab:
            context = vocab.readlines()

            for line in context:
                vocablist.append(line.replace("\n", ""))


        #Befüllen von Daten aus extrahierten txt Dateien
        with open("Gangart.txt", "r", encoding="utf8") as gangtxt:
            context = gangtxt.readlines()
            templist = []

            for line in context:
                if line == "#\n":
                    gangart.append(templist)
                    templist = []
                    continue
                templist.append(line.replace("\n", ""))

        with open("Laender.txt", "r", encoding="utf8") as landtxt:
            context = landtxt.readlines()
            templist = []

            for line in context:
                if line == "#\n":
                    laender.append(templist)
                    templist = []
                    continue

                templist.append(line.replace("\n", ""))

        with open("Mahlzeit.txt", "r", encoding="utf8") as mahltxt:
            context = mahltxt.readlines()

            for line in context:
                mahlzeit.append(line.replace("\n", ""))

        with open("Sonstige.txt", "r", encoding="utf8") as sonsttxt:
            context = sonsttxt.readlines()

            for line in context:
                sonstige.append(line.replace("\n", ""))

        with open("Vegan.txt", "r", encoding="utf8") as vegtxt:
            context = vegtxt.readlines()
            templist = []

            for line in context:
                if line == "#\n":
                    vegan.append(templist)
                    templist = []
                    continue

                templist.append(line.replace("\n", ""))

        #Extrahieren der Zutaten und aller gültigen Categories
        with open("Unique_Zutaten_clean.txt", "r", encoding="utf8") as zutatentxt:
            context = zutatentxt.readlines()

            for zeile in context:
                zutaten.append(zeile.replace("\n", ""))

        with open("Wichtige_Kategorien.txt", "r", encoding="utf8") as kategorientxt:
            context = kategorientxt.readlines()

            for zeile in context:
                kategorien.append(zeile.replace("\n", ""))
        counttag = 0
        for element in texttag:

            textvonelement = element.text
            templistzutat = []
            anweisunglist = []

            #finden aller matches auf das regex
            matches = re.findall("\[\[(.*?)\]\]", textvonelement)
            tempkategorien = list(set(re.findall("\[\[(Category:(.*?))\]\]", textvonelement)))

            istdirection = re.search("^(== Directions ==).(.*?)(\n)$", textvonelement, re.MULTILINE | re.DOTALL)
            tempanweisunglist = []

            if istdirection:
                # Matchen der Kochanweisungen über Regex
                tempanweisung = re.findall("^(== Directions ==).(.*?)(\n)$", textvonelement, re.MULTILINE | re.DOTALL)
                tempanweisung = tempanweisung[0][1]
                tempanweisung = tempanweisung.replace("\n", "")
                tempanweisung = tempanweisung.replace("#", "")
                tempanweisung = tempanweisung.replace("[", "")
                tempanweisung = tempanweisung.replace("]", "")
                tempanweisung = tempanweisung.replace("|", " or ")
                anweisungen = tempanweisung.replace("&nbsp;", " ")

                tempanweisunglist = anweisungen.split()

            for wort in tempanweisunglist:
                if wort in vocablist:
                    anweisunglist.append(wort)

            tempgemischt = []

            #alle weiteren matches appenden
            for e in matches:
                # test ob ein | vorhanden ist -> meistens bei Zutaten
                istmehrere = re.search("|", e)

                # falls | vorhanden
                if istmehrere:
                    templist = e.split("|")

                    for temp in templist:
                        tempgemischt.append(temp)
                    continue


                tempgemischt.append(e)

            #duplikate löschen
            tempgemischt = list(set(tempgemischt))

            #aussortieren der Kategorien und uninteressanten Zutaten
            for e in tempgemischt:
                if e.lower() in zutaten:
                    templistzutat.append(e.lower())

            tempkategorien = list(set(tempkategorien))
            tempkatliste = []

            #Zusammenstellen des dict
            for k in tempkategorien:
                if "Category:" not in k:
                    tempkatliste.append(k[1].lower())


            aussortiert = []

            for t in tempkatliste:
                if t in kategorien:
                    aussortiert.append(t)

            if len(aussortiert) == 0 or len(templistzutat) == 0:
                continue

            for kat in aussortiert:
                namekat = []

                #liste um Später in alle jsons die richtigen Rezepte einzufügen
                listezugehoerigkeit = []

                #Unterscheidung Gangart
                if any(kat in sublist for sublist in gangart):

                    listezugehoerigkeit.append("gangart")

                    if kat in gangart[0]:
                        namekat.append("dessert")

                    if kat in gangart[1]:
                        namekat.append("snack")

                    if kat in gangart[2]:
                        namekat.append("main dish")

                    if kat in gangart[3]:
                        namekat.append("soup")

                    if kat in gangart[4]:
                        namekat.append("appetizer")

                    if kat in gangart[5]:
                        namekat.append("salad")

                    if kat in gangart[6]:
                        namekat.append("side dish")

                #Unterscheidung Länder
                if any(kat in sublist for sublist in laender):
                    listezugehoerigkeit.append("laender")

                    if kat in laender[0]:
                        namekat.append("german")

                    if kat in laender[1]:
                        namekat.append("asian")

                    if kat in laender[2]:
                        namekat.append("american")

                    if kat in laender[3]:
                        namekat.append("romanian")

                    if kat in laender[4]:
                        namekat.append("mexican")

                    if kat in laender[5]:
                        namekat.append("italian")

                    if kat in laender[6]:
                        namekat.append("spanish")

                    if kat in laender[7]:
                        namekat.append("indian")

                    if kat in laender[8]:
                        namekat.append("french")

                #Unterscheidung Lunch
                if kat in mahlzeit:
                    listezugehoerigkeit.append("mahlzeit")

                    namekat.append(kat.replace("recipes", "").strip())

                #Unterscheidung Sonstige
                if kat in sonstige:
                    listezugehoerigkeit.append("sonstige")

                    namekat.append(kat)

                #Unterscheidung Vegan

                if any(kat in sublist for sublist in vegan):
                    listezugehoerigkeit.append("vegan")

                    if kat in vegan[0]:
                        namekat.append("meat")

                    if kat in vegan[1]:
                        namekat.append("vegetarian")

                    if kat in vegan[2]:
                        namekat.append("vegan")

            tempc = 0
            for z in listezugehoerigkeit:

                tempdict = {}

                # id vergeben
                tempdict["id"] = idcounter

                # id weiterlaufen lassen
                idcounter += 1

                # Zutaten vergeben
                tempdict["ingredients"] = templistzutat

                # Anweisungen vergeben : Liste
                tempdict["directions_list"] = list(set(anweisunglist))

                # Anweisungen vergeben : String
                tempdict["directions_string"] = anweisungen

                # Kategorie vergeben
                if z == "gangart":
                    tempdict["category"] = namekat[tempc]

                    listgang.append(tempdict)

                if z == "laender":
                    tempdict["category"] = namekat[tempc]

                    listlaender.append(tempdict)

                if z == "mahlzeit":
                    tempdict["category"] = namekat[tempc]

                    listmahlzeit.append(tempdict)

                if z == "sonstige":
                    tempdict["category"] = namekat[tempc]

                    listsonstige.append(tempdict)

                if z == "vegan":
                    tempdict["category"] = namekat[tempc]

                    listvegan.append(tempdict)

                #Counter erhöhen
                tempc += 1


    with open("Gangart.json", "w", encoding="utf8") as dumpfile:
        json.dump(listgang, dumpfile, indent=2)

    with open("Laender.json", "w", encoding="utf8") as dumpfile:
        json.dump(listlaender, dumpfile, indent=2)

    with open("Mahlzeit.json", "w", encoding="utf8") as dumpfile:
        print(listmahlzeit)
        print(len(listmahlzeit))
        json.dump(listmahlzeit, dumpfile, indent=2)

    with open("Sonstige.json", "w", encoding="utf8") as dumpfile:
        json.dump(listsonstige, dumpfile, indent=2)

    with open("Vegan.json", "w", encoding="utf8") as dumpfile:
        json.dump(listvegan, dumpfile, indent=2)

    print(counttag)


#Regex zum Matchen des Texts: ^(== Directions ==).*?(\[)

#kategorien()
#trainingsdaten()
trainingsdaten_split()

