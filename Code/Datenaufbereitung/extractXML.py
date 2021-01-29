# from lxml
from bs4 import BeautifulSoup as bs


def status(i):
    switcher = {
        0: None,
        1: 'de',
        2: 'in',
        3: 'di',
        4: 'sa'
    }
    return switcher.get(i)


def setstatus(str):
    switcher = {
        '== Description ==\n': 1,
        '=== Ingredients ===\n': 2,
        '== Directions ==\n': 3,
        '== See also ==\n': 4
    }
    return switcher.get(str)

def first_function_prototype():
    with open("cookbook_2019.xml", "r", encoding='utf8') as file:
    #with open("cookbook_2019 - Kopie.xml", "r", encoding='utf8') as file:
        content = file.readlines()

        content = "".join(content)
        bs_content = bs(content, "xml")

        print("parsing with lxml")

        bs_content = bs(content, "lxml")

        print("finding text-tags!")

        texttag = bs_content.find_all("text")

        # immmer selbe Reihenfolge: Description -> Ingredients -> Directions -> See also
        # dafür status Nutzung, für Kontrolle bei welchem Schritt man ist

        # status kann vier werte annehmen 0(nichts), 1(Description), 2(Ingredients), 3(Directions), 4(See also)
        status = 0
        zutaten = []

        print(texttag[3])

        with open("cleantext.txt", "w", encoding='utf8') as txt:
            print("writing cleantext txt!")
            for element in texttag:
                textvomelement = element.text
                txt.write(textvomelement + '\n')

        with open("cleantext.txt", "r", encoding='utf8') as file:
            content = file.readlines()
            print('Writing Ingriedients!')

            for zeile in content:

                # setzen des Status
                statusvorher = status
                if setstatus(zeile) != None:
                    status = setstatus(zeile)

                # statusbezogene Vorhergehensweise:

                # Zutaten
                if status == 2:
                    if zeile in zutaten:
                        continue
                    else:
                        zutaten.append(zeile)

            with open("Unique_Zutaten.txt", "w", encoding='utf8') as zutatentxt:
                for zutat in zutaten:
                    zutatentxt.write(zutat + '\n')
