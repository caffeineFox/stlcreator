# Startbefehl: python3 stlcreator.py
import numpy as np
import random as r


def vectorToStr(vector):
    # TODO: letzte Komponente bekommt auch Leerzeichen angehangen -> soll nicht
    returnStr:str = ""
    for v in vector:
        returnStr += str(int(v) if v.is_integer() else v) + " "
    return returnStr


def calcNormal(p1, p2, p3):
    # https://www.khronos.org/opengl/wiki/Calculating_a_Surface_Normal
    v:np.array = p2 - p1
    w:np.array = p3 - p1
    print(np.cross(v, w))
    return np.cross(v, w)


def safeToFile(fileName, outStr):
    outFile = open("./" + fileName + ".stl", "w")
    outFile.write(outStr)
    outFile.close()
    print("Die Datei wurde im aktuellen Arbeitsverzeichnis unter dem Name " + fileName + ".stl abgelegt.")


outStr:str
fileName:str = ""
shape:str = ""

while (fileName == ""):
    fileName:str = input("Dateiname (wird auch als Modellname verwendet): ")

outStr = "solid " + fileName + "\n"

shape = input("Soll ein Quader (q/Q) oder ein Zylinder (z/Z) erstellt werden? > ")

if (shape in "qQ"):
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
    
    while (not validInput):
        inp = input("Kantenlängen eingeben (x, y, z und mit Komma getrennt): ").replace(" ", "").split(",")
        try:
            edgeLen = list(map(float, inp))
            if (len(edgeLen) == 3):
                validInput = True
        except Exception as e:
            print("Ungültige Eingabe")


    x:float = edgeLen[0]
    y:float = edgeLen[1]
    z:float = edgeLen[2]
    
    for i in range(0, 12):
        _i:int = i % 2
        __i:int = i % 4
        vert:[np.array] = []
        if (i < 4): # mit i % 3 und etwas Magie zweiten Index bestimmen, dann kann sich Verzweigung gespart werden
            vert.append(np.array([x*bin[_i][0],
                                  y*bin[_i][1],
                                  z*bin[_i][2]]))
            vert.append(np.array([x*bin[_i+(2 if __i in [0, 1] else 4)][0],
                                  y*bin[_i+(2 if __i in [0, 1] else 4)][1],
                                  z*bin[_i+(2 if __i in [0, 1] else 4)][2]]))
            vert.append(np.array([x*bin[_i+6][0],
                                  y*bin[_i+6][1],
                                  z*bin[_i+6][2]]))
        elif (i > 3 and i < 8): # mit i % 3 zweiten Index bestimmen oder so...
            vert.append(np.array([x*bin[_i][2],
                                  y*bin[_i][0],
                                  z*bin[_i][1]]))
            vert.append(np.array([x*bin[_i+(2 if __i in [0, 1] else 4)][2],
                                  y*bin[_i+(2 if __i in [0, 1] else 4)][0],
                                  z*bin[_i+(2 if __i in [0, 1] else 4)][1]]))
            vert.append(np.array([x*bin[_i+6][2],
                                  y*bin[_i+6][0],
                                  z*bin[_i+6][1]]))
        else: # mit i % 3 zweiten Index bestimmen oder so...
            vert.append(np.array([x*bin[_i][1],
                                  y*bin[_i][2],
                                  z*bin[_i][0]]))
            vert.append(np.array([x*bin[_i+(2 if __i in [0, 1] else 4)][1],
                                  y*bin[_i+(2 if __i in [0, 1] else 4)][2],
                                  z*bin[_i+(2 if __i in [0, 1] else 4)][0]]))
            vert.append(np.array([x*bin[_i+6][1],
                                  y*bin[_i+6][2],
                                  z*bin[_i+6][0]]))

        
        outStr += "  facet normal " + vectorToStr(calcNormal(vert[0], vert[1], vert[2]))
        
        outStr += "\n    outer loop"
        for v in vert:
            outStr += "\n      vertex " + vectorToStr(v)

        outStr += "\n    endloop\n  endfacet\n"

    outStr += "endsolid " + fileName
    safeToFile(fileName, outStr)

elif (shape in "zZ"):
    pass
    #safeToFile(fileName, outStr)

else:
    print("Es wurde keiner der gegebenen Körper gewählt. Das Programm wird beendet.")
