from func import *
from plots import *
menu = True
notes = None
hist = None
dataHist = None
a,b,MAE = None, None, None
while menu:
    opt = validarL("Bienvenido al sistema, que deseas hacer?\n\n(1) Cargar notas\n(2) Eliminar un estudiante\n(3) Mayor nota de un estudiante\n(4) Ordenar estudiantes por promedio\n(5) Ordenar estudiantes por cantidad de cursos inscritos.\n(6) Prediccion de estudiantes\n(-1) Salir\n((7 DEBUGGEAR LOADER))\n",["1","2","3","4","5","6","7","-1"])
    #OPT SALIDA
    if opt == "-1":
        break

    #OPT CARGAR NOTAS
    elif opt == "1":
        notes = loadNotes(True)
        if notes:
            cursos, estudiantes, notas = notes
            notesprint = traducir(estudiantes,notas)
            imprimir_tabla(notesprint,13,["Estudiante"]+cursos)

    #OPT ELIMINAR ESTUDIANTE
    elif opt == "2":
        if not notes:
            notes = loadNotes(True)
            if notes:
                cursos, estudiantes, notas = notes
            else:
                continue
        if len(estudiantes) > 1:
            print("Estudiantes registrados en el sistema:")
            for est in estudiantes:
                print(est)
            qn = validarL("Digita el documento del estudiante a eliminar (-1 para salir.):\n",estudiantes+["-1"])
            if qn == "-1":
                continue
            ind = buscarId(estudiantes,qn)
            if delElem(estudiantes,ind):
                if delElem(notas,ind):
                    if saveNotes(cursos, estudiantes, notas,True):
                        pass
                    else: 
                        notes = loadNotes()
                        if notes:
                            cursos, estudiantes, notas = notes
                else:
                    print("No se pudo eliminar, se encontro un indice invalido en notas: ", ind)
            else:
                print("No se pudo eliminar, se encontro un indice invalido en estudiantes: ", ind)
        else:
            print("\nERROR: Solo hay un estudiante en el sistema, cancelando eliminacion...")

    #OPT MAYOR NOTA ESTUDIANTE
    elif opt == "3":
        if not notes:
            notes = loadNotes(True)
            if notes:
                cursos, estudiantes, notas = notes
            else:
                continue
        print("Estudiantes registrados en el sistema:")
        for est in estudiantes:
            print(est)
        qn = validarL("Digita el documento del estudiante a consultar (-1 para salir.):\n",estudiantes+["-1"])
        if qn == "-1":
            continue
        indest = buscarId(estudiantes,qn)
        nmayor, c = mayor(notas[indest])
        if nmayor > -1:
            if c == 1:
                indcur = buscarId(notas[indest],nmayor)
                print("La mayor nota del estudiante",qn,"es:",nmayor," en el curso",cursos[indcur])
            else:
                indscur = buscarId(notas[indest],nmayor,True)
                curs = ""
                n = 0
                for indd in indscur:
                    curs+=cursos[indd]
                    if n != len(indscur)-1:
                        curs+= ", "
                    n+=1
                print("La mayor nota del estudiante",qn,"es:",nmayor," en los cursos",curs)
        else:
            print("El estudiante no tiene materias matriculadas")

    #OPT ORDENAR POR PROMEDIOS
    elif opt == "4":
        if not notes:
            notes = loadNotes(True)
            if notes:
                cursos, estudiantes, notas = notes
            else:
                continue

        #Lista de pares (Promedio, Indice)
        indprom = list()
        id = 0
        for estudiante in estudiantes:
            t = 0
            p = 0
            inv = 0
            for nota in notas[id]:
                if nota>=0:
                    p+=nota
                    t+=1
                elif nota == -1 or nota == -2:
                    inv += 1
            if p > 0:
                p = round(p/t,2)
            if inv == len(notas[id]):
                p = -1#Centinela -1 = No tiene notas ND
            indprom.append( (p*-1, id) ) #-1 para que se ordenen de mayor a menor, el algoritmo burbuja ordena ascendentemente.
            id+=1

        #Ordenamiento con burbuja
        if len(indprom) == len(estudiantes):
            indprom, c = bubbleSort(indprom)
            print("\nEXITO: LISTA DE ESTUDIANTES POR PROMEDIO:\n")
        else:
            print("ERROR:La lista de promedios no coincide con la cantidad de estudiantes en el sistema. Abortando...")
            continue
        #Imprimir lista ordenada
        for x in indprom:
            pn = x[0]*-1
            if pn == -1:#Centinela -1
                print(f"El estudiante {estudiantes[x[1]]} no tiene notas en el sistema")
            else:
                print(f"El estudiante {estudiantes[x[1]]} con un promedio de {pn}")

        #DEBUGEAR ProMEDIOS
        #print("CONTADOR DE ITERACIONES: ",c)

    elif opt == "5":
        if not notes:
            notes = loadNotes(True)
            if notes:
                cursos, estudiantes, notas = notes
            else:
                continue

        #Lista de pares (Cursos Estudiante, Indice)
        idcur = list()
        id = 0
        for estudiante in estudiantes:
            c = 0
            nm = 0
            k = len(cursos)
            for nota in notas[id]:
                if nota == -1:
                    c += 1
                elif nota == -2:
                    nm +=1
            k-=c+nm
            if nm == len(notas[id]):
                k = -1 #Centinela -1: No tiene historia academica (no ha inscrito cursos)
            idcur.append( (k*-1, id) ) #-1 para que se ordenen de mayor a menor, el algoritmo burbuja ordena ascendentemente.
            id+=1

        #Selsort
        if len(idcur) == len(estudiantes):
            incur = selSort(idcur)
            print("\nEXITO: LISTA DE ESTUDIANTES POR CURSOS INSCRITOS:\n")
        else:
            print("ERROR:La lista de estudiantes por curso no coincide con la cantidad de estudiantes en el sistema. Abortando...")
            continue
        #Imprimir lista ordenada
        for x in idcur:
            pn = x[0]*-1
            if pn == -1:#Centinela -1
                print(f"El estudiante {estudiantes[x[1]]} no tiene historia academica (no ha inscrito cursos) ")
            else:
                if pn == 0:
                    print(f"El estudiante {estudiantes[x[1]]} ha cursado {pn} cursos (Tiene cursos cancelados)")
                else:
                    print(f"El estudiante {estudiantes[x[1]]} ha cursado {pn} cursos")

    elif opt == "6":
        if a is None or dataHist is None:
            hist = loadHist(True)
            if hist:
                años, cantEstu, cH = hist
                print("iteraciones de cH", cH)
            else:
                continue
            a,b,MAE,c,k,k1,k2 = tanteoBaj(años,cantEstu)
            #Matriz de datos:
            dataHist = list()
            for x in range(len(años)):
                dataHist.append([años[x],cantEstu[x]])
        #DEBUG: print(a,b,MAE,"llamadas a mae",c,"vueltas de while",k,"evaluaciones de menor error:",k1,"cambios de paso:",k2) #Debug

        #Pedir datos al usuario:
        while True:
            try:
                yr = int(input("Digita el año a consultar (-1 para salir.):\n"))
                if (yr <= años[-1] or yr > 9999) and not yr == -1:
                    print("El año debe ser mayor que",años[-1],"Y menor que 10000")
                    continue
            except ValueError:
                print("Valor invalido.")
                continue
            else:
                break
        if yr == -1:
            continue

        ayr = años+[yr]

        #Regresion:
        yS = regresion(a,b,ayr)

        try:
            plot_data(dataHist,yS,ayr,(yr,yS[-1]))
        except Exception as e:
            print("ERROR: Hubo un error al guardar el archivo:",e)
        else:
            print("Cantidad Y de estudiantes estimada:",int(round(yS[-1])))
            print("MAE de estudiantes:",MAE)
            print("EXITO: Archivo de prediccion generado exitosamente.")
            
    #DEBUGER
    elif opt == "7":
        loadNotes(True)
        loadNotes(True)
        loadNotes(True)
        loadNotes(True)
        loadNotes(True)
        loadNotes(True)
        loadNotes(True)

    print("\n")