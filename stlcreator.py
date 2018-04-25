# Startbefehl: python3 stlcreator.py
import numpy as np
import random as r


def vectorToStr(vector):
    ### possible fix: letzte Komponente bekommt auch Leerzeichen angehangen -> soll nicht
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
    
    while (not validInput):
        inp = input("Kantenlängen eingeben (mit Komma getrennt): ").replace(" ", "").split(",")
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
        classI:int = i % 2
        vert:[np.array] = []
        for j in range(0, 3):
            vert.append(np.array([x*r.randint(0,1), y*r.randint(0,1), z*r.randint(0,1)]))
                # vertex-loop
                # generiere p1x - p3z
                # vert.append

        outStr += "  facet normal " + vectorToStr(calcNormal(vert[0], vert[1], vert[2]))

        for v in vert:
            outStr += "\n      vertex " + vectorToStr(v)

        outStr += "\n    outer loop"

        outStr += "\n    endloop\n  endfacet\n"




    outStr += "endsolid " + fileName
    safeToFile(fileName, outStr)

elif (shape in "zZ"):
    pass
    #safeToFile(fileName, outStr)

else:
    print("Es wurde keiner der gegebenen Körper gewählt. Das Programm wird beendet.")
