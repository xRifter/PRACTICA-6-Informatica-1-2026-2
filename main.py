from func import *
menu = True
notes = None
while menu:
    opt = validarL("Bienvenido al sistema, que deseas hacer (CAMBIAR TEXTO LUEGO)\n\n(1) Cargar notas\n(2) Eliminar un estudiante\n(-1) Salir\n",["1","2","3","4","5","-1"])
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
                    cursos, estudiantes, notas = load_notes()


        
                


