# Startbefehl: python3 stlcreator.py
import numpy as np
import random as r


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
'''

outStr:str
fileName:str = ""
shape:str = ""
saveMode:str = "w"

def vectorToStr(vector, shape):
    ''' wandelt gegebenen (R3-) Vector in STL-konformen String um (gibt die Komponenten mit
    Leerzeichen getrennt zurück)'''
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


def saveToFile(fileName):
    ''' das Ergebnis der Generation (outStr) wird in eine Datei mit der Endung .stl geschrieben '''
    global saveMode, outStr
    outFile = open("./" + fileName + ".stl", saveMode)
    outFile.write(outStr)
    outFile.close()
    outStr = ""


def degToRad(deg):
    ''' wandelt Grad in Radiant um '''
    return deg*np.pi/180


# solange fileName leer ist, soll zur Eingabe aufgefordert werden
while (fileName == ""):
    fileName:str = input("Dateiname (wird auch als Modellname verwendet): ")

# Beginn des STL-Strings einfügen
outStr = "solid " + fileName + "\n"

shape = input("Soll ein Quader (q/Q) oder ein Zylinder (z/Z) erstellt werden? > ")

if (shape in "qQ"):
    ''' Zweig für Quader '''
    '''
    edgeLen:
        # speichert Kantenlängen des Quaders zwischen
    inp:
        # nimmt input für Kantenlängen als String erstmal entgegen, splittet in Strings aus Ziffern
    validInput:
        # solange falsch, bis als für sinnvoll erachtete Kantenlängenwerte (sprich (Gleitkomma-) Zahlen) eingegeben wurden
    bin:
        # enthält Binärdarstellung der Ziffern 0 - 7
        # zur Ermittlung der Ecken (Eckkoordinaten) ("vertex"/vertices) verwendet
    '''
    edgeLen:[float]
    inp:[str]
    validInput:bool = False
    bin:[[int]] = [[0,0,0],
                   [0,0,1],
                   [0,1,0],
                   [0,1,1],
                   [1,0,0],
                   [1,0,1],
                   [1,1,0],
                   [1,1,1]]


    # solange wie nicht 3 Zahlen für x, y, z eingegeben wurden, wird zur Eingabe aufgefordert
    while (not validInput):
        inp = input("Kantenlängen eingeben (x, y, z und mit Komma getrennt): ").replace(" ", "").split(",")
        try:
            edgeLen = list(map(float, inp))
            if (len(edgeLen) == 3):
                validInput = True
        except Exception as e:
            print("Ungültige Eingabe. Bitte Ganz- oder Gleitkommazahlen eingeben.")


    # edgeLen wird der Übersicht wegen auf x, y, z aufgeteilt
    x:float = edgeLen[0]
    y:float = edgeLen[1]
    z:float = edgeLen[2]

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
            # Hilfsvariablen
        vertices:
            # hält die aktuelle Dreiermenge generierter Ecken/Eckkoordinaten
        '''
        _i:int = i % 2
        __i:int = i % 4

        if (i > 3 and i < 8):
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
        outStr += "  facet normal " + vectorToStr(calcNormal(vertices[0], vertices[1], vertices[2]), shape)

        # Beginn der neuen Dreiecksfläche
        outStr += "\n    outer loop"

        # die Eckkoordinaten werden zusammen mit dem Schlüsselwort "vertex" an den STL-String angehangen
        for v in vertices:
            outStr += "\n      vertex " + vectorToStr(v, shape)

        # Ende der neuen Dreiecksfläche
        outStr += "\n    endloop\n  endfacet\n"

        # Zwischenspeichern
        if __i == 3:
            saveToFile(fileName)

    # Ende des STL-Strings einfügen
    outStr += "endsolid " + fileName
    saveToFile(fileName)
    print("Die Datei wurde im aktuellen Arbeitsverzeichnis unter dem Name " + fileName + ".stl abgelegt.")

elif (shape in "zZ"):

    radius: float
    height: float
    inpRadius: str
    inpHeight: str
    validInput: bool = False

    # solange keine Float-Zahlen eingeben werden, wiederholt sich des Prompt der Eingabe
    while (not validInput):
        inpRadius = input("Radius eingeben: ")
        inpHeight = input("Höhe eingeben: ")
        try:
            radius = float(inpRadius)
            height = float(inpHeight)
            validInput = True
        except ValueError as e:
            print("Ungültige Eingabe. Bitte Ganz- oder Gleitkommazahlen eingeben.")

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
        outStr += "  facet normal " + vectorToStr(calcNormal(vertices[0], vertices[1], vertices[2]), shape)
        outStr += "\n    outer loop"
        for v in vertices[0:3]:
            outStr += "\n      vertex " + vectorToStr(v, shape)
        outStr += "\n    endloop\n  endfacet\n"

        # Oben
        outStr += "  facet normal " + vectorToStr(calcNormal(vertices[3], vertices[4], vertices[5]), shape)
        outStr += "\n    outer loop"
        for v in vertices[3:6]:
            outStr += "\n      vertex " + vectorToStr(v, shape)
        outStr += "\n    endloop\n  endfacet\n"

        # Seiten - erstes Dreieck
        outStr += "  facet normal " + vectorToStr(calcNormal(vertices[0], vertices[1], vertices[4]), shape)
        outStr += "\n    outer loop"
        outStr += "\n      vertex " + vectorToStr(vertices[0], shape)
        outStr += "\n      vertex " + vectorToStr(vertices[1], shape)
        outStr += "\n      vertex " + vectorToStr(vertices[4], shape)
        outStr += "\n    endloop\n  endfacet\n"

        # Seiten - zweites Dreieck
        outStr += "  facet normal " + vectorToStr(calcNormal(vertices[0], vertices[3], vertices[4]), shape)
        outStr += "\n    outer loop"
        outStr += "\n      vertex " + vectorToStr(vertices[0], shape)
        outStr += "\n      vertex " + vectorToStr(vertices[3], shape)
        outStr += "\n      vertex " + vectorToStr(vertices[4], shape)
        outStr += "\n    endloop\n  endfacet\n"
        saveToFile(fileName)

    outStr += "endsolid " + fileName
    saveToFile(fileName)
    print("Die Datei wurde im aktuellen Arbeitsverzeichnis unter dem Name " + fileName + ".stl abgelegt.")

else:
    ''' Keine der gegebenen Körper wurde zur Generierung ausgewählt '''
    print("Es wurde keiner der gegebenen Körper gewählt. Das Programm wird beendet.")
