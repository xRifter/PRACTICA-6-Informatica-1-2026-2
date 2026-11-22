from func import *
#notes lee un parametro booleano para imprimir si se importo correctamente o no.
notes = load_notes()
if notes:
    #Print para ensayar que todo se lea correctamente
    cursos, estudiantes, notas = notes
    print(len(cursos),len(estudiantes),len(notas))
    print("Cursos: ",cursos)
    print("Estudiantes: ",estudiantes)
    print("Notas: ",notas)
