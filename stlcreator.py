# Startbefehl: python3 stlcreator.py
import numpy as np
import random as r
import sys


'''
outStr:
    # (STL-) String, der zum Schluss kompletten generierten Text enthält
    # wird am Ende in Datei geschrieben
    # andere Option: Zwischenspeicherung und Reset des Strings
        # einmal mit outFile = open(..., 'w') Datei anlegen,
        # danach mit = open(..., 'a') anhängen an bestehende Datei

fileName:
    # Name für die Outputdatei und das Modell (solid ... bzw endsolid ...)
shape:
    # Auswahl, ob ein Quader oder ein Zylinder erstellt werden soll
saveMode:
    # Speichermodus, am Anfang w -> write -> existierende Datei/Dateiinhalt wird überschrieben
    # wird nach erstem Speichern auf a gesetzt -> append -> hängt an existierenden Dateiinhalt an
    # durch append wird Zwischenspeichern ermöglicht
'''

outStr:str
fileName:str = ""
shape:str = ""
saveMode:str = "w"
argv = sys.argv
x:float = 0
y:float = 0
z:float = 0
radius:float = 0
height:float = 0
validInput:bool = False


def vectorToStr(vector):
    ''' wandelt gegebenen (R3-) Vector in STL-konformen String um (gibt die Komponenten mit
    Leerzeichen getrennt zurück), glatte Floats werden zu int konvertiert'''
    returnStr:str = ""
    for v in vector:
        returnStr += str(int(v) if v == int(v) else v) + " "
    return returnStr


def calcNormal(p1, p2, p3):
    # https://www.khronos.org/opengl/wiki/Calculating_a_Surface_Normal
    ''' lässt die Normale der von p1, p2, p3 aufgespannten Fläche berechnen '''
    v:np.array = p2 - p1
    w:np.array = p3 - p1
    return np.cross(v, w)


def saveToFile():
    ''' das Ergebnis der Generation (outStr) wird in eine Datei mit der Endung .stl geschrieben '''
    global saveMode, outStr, fileName
    outFile = open("./" + fileName + ".stl", saveMode)
    outFile.write(outStr)
    outFile.close()
    outStr = ""


def degToRad(deg):
    ''' wandelt Grad in Radiant um '''
    return deg*np.pi/180


def makeCuboid():
    pass


def makeCylinder():
    pass


# Argumentliste prüfen, wenn Argumente gegeben, dann aufteilen und auswerten
# ansonsten werden alle benötigten Werte abgefragt
if len(argv) > 1:
    for i in range(1, len(argv)):
        argv[i] = argv[i].split("=")

    if argv[1][0] in "qQ":
        shape = "q"
        for j in range(2, len(argv)):
            try:
                if argv[j][0] in "xX":
                    x = float(argv[j][1])
                elif argv[j][0] in "yY":
                    y = float(argv[j][1])
                elif argv[j][0] in "zZ":
                    z = float(argv[j][1])
                elif argv[j][0] in "name":
                    fileName = argv[j][1]
                else:
                    print("Gegebenes Argument fehlerhaft für den gewählten Körper.")
                    exit(0)
            except ValueError:
                print("Fehlerhafter Argumentwert bei " + argv[j][0])
        # fehlende Werte nachfordern
        while x == 0 or y == 0 or z == 0:
            try:
                if x == 0:
                    x = float(input("Kantenlänge x eingeben: "))
                if y == 0:
                    y = float(input("Kantenlänge y eingeben: "))
                if z == 0:
                    z = float(input("Kantenlänge z eingeben: "))
            except ValueError:
                print("Ungültige Eingabe. Bitte Ganz- oder Gleitkommazahlen eingeben.")
        while fileName == "":
            fileName = input("Dateiname eingeben (wird auch als Modelname verwendet): ")

    elif argv[1][0] in "zZ":
        shape = "z"
        for j in range(2, len(argv)):
            try:
                if argv[j][0] in ["r","R","radius"]:
                    radius = float(argv[j][1])
                elif argv[j][0] in ["h","H","height"]:
                    height = float(argv[j][1])
                elif argv[j][0] in "name":
                    fileName = argv[j][1]
                else:
                    print("Gegebenes Argument fehlerhaft für den gewählten Körper.")
                    exit(0)
            except:
                print("Fehlerhafter Argumentwert bei " + argv[j][0])
        # fehlende Werte nachfordern
        while radius == 0 or height == 0:
            try:
                if radius == 0:
                    radius = float(input("Radius eingeben: "))
                if height == 0:
                    height = float(input("Höhe eingeben: "))
            except ValueError:
                print("Ungültige Eingabe. Bitte Ganz- oder Gleitkommazahlen eingeben.")
        while fileName == "":
            fileName = input("Datei- und Modelname: ")

    elif argv[1][0] in ["h", "help"]:
        print("usage: python3 stlcreator.py [shape] [arg]")
        print("arg\t: Argumente wie Kantenlänge/Radius")
        print("shape\t: q/Q für Quader, z/Z für Zylinder\n")
        print("mögliche Argumente (Angabe mit [arg]=[Wert], Argumente sind reihenfolgelos):")
        print("Quader\t: x, y, z, name")
        print("\tx   : Kantenlänge in x-Richtung")
        print("\ty   : Kantenlänge in y-Richtung")
        print("\tz   : Kantenlänge in z-Richtung")
        print("\tname: Datei- und Modelname")
        print("Zylinder: r[adius], h[eight], name")
        print("\tr[adius]: Radius des Zylinders")
        print("\th[eight]: Höhe des Zylinders (z-Richtung)")
        print("\tname    : Datei- und Modelname")
        print("Nicht mit Wert belegte Argumente werden auch nach Programmstart noch abgefragt.")
        exit(0)

    else:
        print("Gegebenes Argument fehlerhaft.", argv[1][0], "ist kein Key für Quader bzw. Zylinder.")
        exit(0)


else:
    # solange fileName leer ist, soll zur Eingabe aufgefordert werden
    while (fileName == ""):
        fileName = input("Dateiname (wird auch als Modellname verwendet): ")

    while (shape == ""):
        shape = input("Soll ein Quader (q/Q) oder ein Zylinder (z/Z) erstellt werden? > ")

    if shape in "qQ":
        ''' Zweig für Quader '''
        '''
        edgeLen:
            # speichert Kantenlängen des Quaders zwischen
        inp:
            # nimmt input für Kantenlängen als String erstmal entgegen, splittet in Strings aus Ziffern
        validInput:
            # solange falsch, bis als für sinnvoll erachtete Kantenlängenwerte (sprich (Gleitkomma-) Zahlen) eingegeben wurden
        '''
        edgeLen:[float]
        inp:[str]

        # solange wie nicht 3 Zahlen für x, y, z eingegeben wurden, wird zur Eingabe aufgefordert
        while not validInput:
            inp = input("Kantenlängen eingeben (Reihenfolge x, y, z; mit Komma getrennt): ").replace(" ", "").split(",")
            try:
                edgeLen = list(map(float, inp))
                if (len(edgeLen) == 3):
                    validInput = True
            except ValueError:
                print("Ungültige Eingabe. Bitte Ganz- oder Gleitkommazahlen eingeben.")

        # edgeLen wird der Übersicht wegen auf x, y, z aufgeteilt
        x = edgeLen[0]
        y = edgeLen[1]
        z = edgeLen[2]

    elif shape in "zZ":
        inpRadius: str
        inpHeight: str

        # solange keine Float-Zahlen eingeben werden, wiederholt sich des Prompt der Eingabe
        while not validInput:
            inpRadius = input("Radius eingeben: ")
            inpHeight = input("Höhe eingeben: ")
            try:
                radius = float(inpRadius)
                height = float(inpHeight)
                validInput = True
            except ValueError:
                print("Ungültige Eingabe. Bitte Ganz- oder Gleitkommazahlen eingeben.")

    else:
        ''' Keine der gegebenen Körper wurde zur Generierung ausgewählt '''
        print("Es wurde keiner der gegebenen Körper gewählt. Das Programm wird beendet.")
        exit(0)


# Beginn des STL-Strings einfügen
outStr = "solid " + fileName + "\n"
saveToFile()
saveMode = "a"  # saveMode umstellen


if shape in "qQ":
    '''
    bin:
        # enthält Binärdarstellung der Ziffern 0 - 7
        # zur Ermittlung der Ecken (Eckkoordinaten) ("vertex"/vertices) verwendet
    '''
    bin:[[int]] = [[0,0,0],
                   [0,0,1],
                   [0,1,0],
                   [0,1,1],
                   [1,0,0],
                   [1,0,1],
                   [1,1,0],
                   [1,1,1]]

    # indX/Y/Z:
        # verwendet, um Code zu sparen, da sonst Unterscheidung wie jetzt mit
        # i > 3 and i < 8 etc mit vertices.append etc notwendig wäre -> wäre unübersichtlicher
        # für erste 4 vertices mit Standardwert 0, 1, 2 belegt
    indX:int = 0
    indY:int = 1
    indZ:int = 2

    # es wird von 0 bis 11 iteriert, damit alle 12 Dreiecksflächen, die für einen
    # Quader nötig sind, angelegt werden
    for i in range(0, 12):
        '''
        _i, __i:
            # Hilfsvariablen zur Ebenen- und Dreiecksermittlung
        vertices:
            # hält die aktuelle Dreiermenge generierter Ecken/Eckkoordinaten
        '''
        _i:int = i % 2
        __i:int = i % 4

        if i > 3 and i < 8:
            indX = 2
            indY = 0
            indZ = 1
        elif (i > 7):
            indX = 1
            indY = 2
            indZ = 0

        vertices:[np.array] = []
        vertices.append(np.array([x*bin[_i][indX],
                                  y*bin[_i][indY],
                                  z*bin[_i][indZ]]))
        vertices.append(np.array([x*bin[_i+(2 if __i in [0, 1] else 4)][indX],
                                  y*bin[_i+(2 if __i in [0, 1] else 4)][indY],
                                  z*bin[_i+(2 if __i in [0, 1] else 4)][indZ]]))
        vertices.append(np.array([x*bin[_i+6][indX],
                                  y*bin[_i+6][indY],
                                  z*bin[_i+6][indZ]]))

        # aus den 3 zuvor erzeugten vertices wird die Normale der aufgespannten Fläche berechnet
        # und zu einem STL-konformen String umgewandelt
        outStr += "  facet normal " + vectorToStr(calcNormal(vertices[0], vertices[1], vertices[2]))

        # Beginn der neuen Dreiecksfläche
        outStr += "\n    outer loop"

        # die Eckkoordinaten werden zusammen mit dem Schlüsselwort "vertex" an den STL-String angehangen
        for v in vertices:
            outStr += "\n      vertex " + vectorToStr(v)

        # Ende der neuen Dreiecksfläche
        outStr += "\n    endloop\n  endfacet\n"

        # Zwischenspeichern
        if __i == 3:
            saveToFile()

    # Ende des STL-Strings einfügen
    outStr += "endsolid " + fileName
    saveToFile()
    print("Die Datei wurde im aktuellen Arbeitsverzeichnis unter dem Name " + fileName + ".stl abgelegt.")


elif shape in "zZ":
    prevVertexBot: [float] = [0, radius, 0]
    prevVertexTop: [float] = [0, radius, height]

    for alpha in range(18,378,18):

        vertices:[np.array] = [np.array(prevVertexBot),
                               np.array([np.sin(degToRad(alpha)) * radius, np.cos(degToRad(alpha)) * radius, 0]),
                               np.array([0, 0, 0]), np.array(prevVertexTop),
                               np.array([np.sin(degToRad(alpha)) * radius, np.cos(degToRad(alpha)) * radius, height]),
                               np.array([0, 0, height])]
        prevVertexBot = vertices[1]
        prevVertexTop = vertices[4]

        # Unten
        # siehe Kommentare in if-Zweig für Erklärungen
        outStr += "  facet normal " + vectorToStr(calcNormal(vertices[0], vertices[1], vertices[2]))
        outStr += "\n    outer loop"
        for v in vertices[0:3]:
            outStr += "\n      vertex " + vectorToStr(v)
        outStr += "\n    endloop\n  endfacet\n"

        # Oben
        outStr += "  facet normal " + vectorToStr(calcNormal(vertices[3], vertices[4], vertices[5]))
        outStr += "\n    outer loop"
        for v in vertices[3:6]:
            outStr += "\n      vertex " + vectorToStr(v)
        outStr += "\n    endloop\n  endfacet\n"

        # Seiten - erstes Dreieck
        outStr += "  facet normal " + vectorToStr(calcNormal(vertices[0], vertices[1], vertices[4]))
        outStr += "\n    outer loop"
        outStr += "\n      vertex " + vectorToStr(vertices[0])
        outStr += "\n      vertex " + vectorToStr(vertices[1])
        outStr += "\n      vertex " + vectorToStr(vertices[4])
        outStr += "\n    endloop\n  endfacet\n"

        # Seiten - zweites Dreieck
        outStr += "  facet normal " + vectorToStr(calcNormal(vertices[0], vertices[3], vertices[4]))
        outStr += "\n    outer loop"
        outStr += "\n      vertex " + vectorToStr(vertices[0])
        outStr += "\n      vertex " + vectorToStr(vertices[3])
        outStr += "\n      vertex " + vectorToStr(vertices[4])
        outStr += "\n    endloop\n  endfacet\n"
        saveToFile()

    outStr += "endsolid " + fileName
    saveToFile()
    print("Die Datei wurde im aktuellen Arbeitsverzeichnis unter dem Name " + fileName + ".stl abgelegt.")
