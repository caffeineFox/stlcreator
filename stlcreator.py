# Startbefehl: python3 stlcreator.py
import numpy as np
import random as r


def vectorToStr(vector):
    # TODO: letzte Komponente bekommt auch Leerzeichen angehangen -> soll nicht
    ''' wandelt gegebenen (R3-) Vector in STL-konformen String um (gibt die Komponenten mit
    Leerzeichen getrennt zurück)'''
    returnStr:str = ""
    for v in vector:
        returnStr += str(int(v) if v.is_integer() else v) + " "
    return returnStr


def calcNormal(p1, p2, p3):
    # https://www.khronos.org/opengl/wiki/Calculating_a_Surface_Normal
    ''' lässt die Normale der von p1, p2, p3 aufgespannten Fläche berechnen '''
    v:np.array = p2 - p1
    w:np.array = p3 - p1
    print(np.cross(v, w))
    return np.cross(v, w)


def safeToFile(fileName, outStr):
    ''' das Ergebnis der Generation (outStr) wird in eine Datei mit der Endung .stl geschrieben '''
    outFile = open("./" + fileName + ".stl", "w")
    outFile.write(outStr)
    outFile.close()
    print("Die Datei wurde im aktuellen Arbeitsverzeichnis unter dem Name " + fileName + ".stl abgelegt.")

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
'''
outStr:str
fileName:str = ""
shape:str = ""

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
            print("Ungültige Eingabe")


    # edgeLen wird der Übersicht wegen auf x, y, z aufgeteilt
    x:float = edgeLen[0]
    y:float = edgeLen[1]
    z:float = edgeLen[2]
    
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
        vertices:[np.array] = []
        if (i < 4): # mit i % 3 und etwas Magie zweiten Index bestimmen, dann kann sich Verzweigung gespart werden
            vertices.append(np.array([x*bin[_i][0],
                                      y*bin[_i][1],
                                      z*bin[_i][2]]))
            vertices.append(np.array([x*bin[_i+(2 if __i in [0, 1] else 4)][0],
                                      y*bin[_i+(2 if __i in [0, 1] else 4)][1],
                                      z*bin[_i+(2 if __i in [0, 1] else 4)][2]]))
            vertices.append(np.array([x*bin[_i+6][0],
                                      y*bin[_i+6][1],
                                      z*bin[_i+6][2]]))
        elif (i > 3 and i < 8):
            vertices.append(np.array([x*bin[_i][2],
                                      y*bin[_i][0],
                                      z*bin[_i][1]]))
            vertices.append(np.array([x*bin[_i+(2 if __i in [0, 1] else 4)][2],
                                      y*bin[_i+(2 if __i in [0, 1] else 4)][0],
                                      z*bin[_i+(2 if __i in [0, 1] else 4)][1]]))
            vertices.append(np.array([x*bin[_i+6][2],
                                      y*bin[_i+6][0],
                                      z*bin[_i+6][1]]))
        else:
            vertices.append(np.array([x*bin[_i][1],
                                      y*bin[_i][2],
                                      z*bin[_i][0]]))
            vertices.append(np.array([x*bin[_i+(2 if __i in [0, 1] else 4)][1],
                                      y*bin[_i+(2 if __i in [0, 1] else 4)][2],
                                      z*bin[_i+(2 if __i in [0, 1] else 4)][0]]))
            vertices.append(np.array([x*bin[_i+6][1],
                                      y*bin[_i+6][2],
                                      z*bin[_i+6][0]]))

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

    # Ende des STL-Strings einfügen
    outStr += "endsolid " + fileName
    safeToFile(fileName, outStr)



elif (shape in "zZ"):
    pass
    #safeToFile(fileName, outStr)



else:
    ''' Keine der gegebenen Körper wurde zur Generation ausgewählt '''
    print("Es wurde keiner der gegebenen Körper gewählt. Das Programm wird beendet.")
