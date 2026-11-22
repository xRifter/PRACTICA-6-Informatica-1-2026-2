#Modulo para funciones y operaciones

def load_notes(p=False):
    try:
        cursos = list()
        estudiantes = list()
        notas = list()
        filename = './notas_estudiantes.csv'
        #abrir con with para cierre automatico
        with open(filename, mode='r', encoding='utf-8') as filenotas:
            lact = 0 #Linea valida actual 
            lread = 0 #Linea actual del archivo
            for linea in filenotas:

                #Contarla siempre
                lread += 1
                
                # Separar texto
                columnas = linea.strip().split(',') 

                #Saltar lineas vacias.
                if not columnas[0] and len(columnas) < 2:
                    continue

                #Limpiar cola
                if not columnas[-1]:
                    columnas.pop()

                lact += 1

                #Obtener cursos

                if lact == 1:
                    #Validacion:
                    for curso in columnas:
                        curso = curso.strip()
                        if curso:
                            cursos.append(curso)
                        else:
                            return load_error(filename,"Hay espacios vacios en el encabezado de cursos", lread)
                    continue

                #Obtener estudiantes

                if lact == 2:
                    for estudiante in columnas:
                        estudiante = estudiante.strip()
                        if estudiante:
                            if estudiante not in estudiantes:
                                estudiantes.append(estudiante)
                            else:
                                return load_error(filename,"Hay uno o varios valores repetidos en el encabezado de documentos", lread)    
                        else:
                            return load_error(filename,"Hay espacios vacios", lread)    
                    continue

                #Obtener notas
                if len(cursos) == len(columnas):
                    fnota = list()
                    for nota in columnas:
                        try:
                            nota = float(nota)
                        except ValueError:
                            return load_error(filename,"Hay uno o varios valores invalidos que no son notas", lread)
                        if nota == -1 or nota == -2 or (0 <= nota <= 5.0):
                            fnota.append(nota)
                        else:
                            return load_error(filename,"Hay nota(s) fuera del rango",lread)
                    notas.append(fnota)
                else:
                    return load_error(filename,"La cantidad de notas no coincide con la cantidad de cursos",lread)
            #Si el archivo solo tiene encabezado
            if lact < 3:
                return load_error(filename,"El archivo no tiene notas o encabezado") 
            #Si no corresponden la cantidad de filas de notas con la cantidad de estudiantes.
            if len(estudiantes) != (lact-2):
                return load_error(filename,f"La cantidad de estudiantes es {len(estudiantes)} y hay {lact-2} filas de notas")
                    

    except FileNotFoundError:
        return load_error(filename, "EL archivo no existe.")
    except Exception as er:
        return load_error(filename,f"Ocurrio un error desconocido al importar {filename}: {er}")
    else:
        if p:
            print("EXITO: Archivo notas_estudiantes.csv importado exitosamente!")
        return cursos, estudiantes, notas

def load_error(filen,texto, linea = None):
    if linea != None:
        print(f"ERROR: El archivo {filen} esta corrupto en la linea {linea}\n{texto}")
    else:
        print(f"ERROR: El archivo {filen} esta corrupto\n{texto}")
    return False

#    filehist = open('./hist_matriculados.csv', mode='r', encoding='utf-8')