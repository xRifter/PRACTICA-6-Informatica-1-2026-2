from func import *
menu = True
notes = None
while menu:
    opt = validarL("Bienvenido al sistema, que deseas hacer (CAMBIAR TEXTO LUEGO)\n\n(1) Cargar notas\n(2) Eliminar un estudiante\n(3) Mayor nota de un estudiante\n(-1) Salir\n((7 DEBUGGEAR LOADER))\n",["1","2","3","4","5","-1","7"])
    #OPT SALIDA
    if opt == "-1":
        break

    #OPT CARGAR NOTAS
    elif opt == "1":
        notes = load_notes(True)
        if notes:
            cursos, estudiantes, notas = notes
            notesprint = traducir(estudiantes,notas)
            imprimir_tabla(notesprint,13,["Estudiante"]+cursos)
        
        print("\n")

    #OPT ELIMINAR ESTUDIANTE
    elif opt == "2":
        if not notes:
            notes = load_notes(True)
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
            ind = buscar_indice(estudiantes,qn)
            if eliminar_elemento(estudiantes,ind):
                if eliminar_elemento(notas,ind):
                    if save_notes(cursos, estudiantes, notas,True):
                        pass
                    else: 
                        notes = load_notes()
                        if notes:
                            cursos, estudiantes, notas = notes
                else:
                    print("No se pudo eliminar, se encontro un indice invalido en notas: ", ind)
            else:
                print("No se pudo eliminar, se encontro un indice invalido en estudiantes: ", ind)
        else:
            print("\nERROR: Solo hay un estudiante en el sistema, cancelando eliminacion...")

    elif opt == "3":
        if not notes:
            notes = load_notes(True)
            if notes:
                cursos, estudiantes, notas = notes
            else:
                continue
        print("Estudiantes registrados en el sistema:")
        for est in estudiantes:
            print(est)
        qn = validarL("Digita el documento del estudiante a consultar (-1 para salir.):\n",estudiantes+["-1"])
        print("\n")
        if qn == "-1":
            continue
        indest = buscar_indice(estudiantes,qn)
        nmayor, c = mayor(notas[indest])
        if nmayor > -1:
            if c == 1:
                indcur = buscar_indice(notas[indest],nmayor)
                print("La mayor nota del estudiante",qn,"es:",nmayor," en el curso",cursos[indcur])
            else:
                indscur = buscar_indice(notas[indest],nmayor,True)
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
        
            
        
        print("\n")

    #DEBUGER
    elif opt == "7":
        load_notes(True)
        load_notes(True)
        load_notes(True)
        load_notes(True)
        load_notes(True)
        load_notes(True)
        load_notes(True)