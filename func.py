#Modulo para funciones y operaciones

def load_notes(p=False,filename = './notas_estudiantes.csv'):
    try:
        cursos = list()
        estudiantes = list()
        notas = list()
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
                    eliminar_elemento(columnas,len(columnas)-1)

                lact += 1

                #Obtener cursos

                if lact == 1:
                    #Validacion:
                    for curso in columnas:
                        curso = curso.strip()
                        if curso:
                            if curso not in cursos:
                                cursos.append(curso)
                            else:
                                return load_error(filename,"Hay uno o varios valores repetidos en el encabezado de cursos", lread)
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
                            return load_error(filename,"Hay espacios vacios en el encabezado de documentos", lread)    
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
        return load_error(filename)
    except Exception as er:
        return load_error(filename,f"Ocurrio un error desconocido al importar {filename}: {er}")
    else:
        if p:
            print("EXITO: Archivo notas_estudiantes.csv importado exitosamente!")
        return cursos, estudiantes, notas

def load_error(filen,texto="\n", linea = None):
    if linea != None:
        print(f"ERROR: El archivo {filen} esta corrupto en la linea {linea}\n{texto}")
    else:
        print(f"ERROR: El archivo {filen} esta corrupto o no existe\n{texto}")
    return False

#    filehist = open('./hist_matriculados.csv', mode='r', encoding='utf-8')

def eliminar_elemento(lista,indice):
    if indice > -1 and indice < len(lista):
        lista[indice:] = lista[indice+1:]
        return True
    else:
        return False

def buscar_indice(lista,elem,r=False):
    indice = 0
    if r:
        indices = list()
        for x in lista:
            if x == elem:
                indices.append(indice)
            indice+=1
        if len(indices) == 1:
            return indices[0]
        elif len(indices) > 1:
            return indices
        else:
            return -1
    else:
        for x in lista:
            if x == elem:
                return indice
            indice+=1
        return -1

#Validar si el input es valido recorriendo una lista o listas anidadas
def validarL(strinput,datosvalidos=["si","no","s","n"],digito=None):
    invalido = True
    while invalido:
        opt = str(input(strinput)).lower()
        for elemento in datosvalidos:
            iterable = (type(elemento) != type("a"))
            if iterable:
                if digito:
                    if opt.isdigit() and opt in elemento:
                        return opt
                else:
                    if opt in elemento:
                        return opt
        if digito:
            if opt.isdigit() and opt in datosvalidos:
                return opt
        else:
            if opt in datosvalidos:
                return opt
        print("Entrada invalida.")

#Imprimir tabla, traido de la practica 5:
def imprimir_tabla(tabla, ancho, encabezado=None):  
    ''' 
    Imprime en pantalla un tabla con los datos pasados, ajustado a los tamaños deseados.
    
    Argumentos:
        tabla: Lista que representa la tabla. Cada elemento es una fila
        ancho: Lista con el tamaño deseado para cada columna. Si se especifica
            un entero, todas las columnas quedan de ese tamaño
        encabezado: Lista con el encabezado de la tabla
    '''
    def dividir_fila(ancho,sep='-'):
        '''
        ancho: Lista con el tamaño de cada columna
        sep: Caracter con el que se van a formar las líneas que 
            separan las filas
        '''
        linea = ''
        for i in range(len(ancho)):
            linea += ('+'+sep*(ancho[i]-1))
        linea = linea[:-1]+'+'
        print(linea)
        
    def imprimir_celda(texto, impresos, relleno):
        '''
        texto: Texto que se va a colocar en la celda
        impresos: cantidad de caracteres ya impresos del texto
        relleno: cantidad de caracteres que se agregan automáticamente,
            para separar los textos del borde de las celda.
        '''        
        # Imprimir celda
        texto = str(texto)
        texto = texto.replace('\n',' ').replace('\t',' ')
        if impresos+relleno < len(texto):
            print(texto[impresos:impresos+relleno],end='')
            impresos+=relleno
        elif impresos >= len(texto):
            print(' '*(relleno),end='')
        else:
            print(texto[impresos:], end='')
            print(' '*(relleno-(len(texto) - impresos)),end='')
            impresos = len(texto)
        return impresos
    
    def imprimir_fila(fila):
        '''
        fila: Lista con los textos de las celdas de la fila
        '''
        impresos = []   
        alto = 1
        for i in range(len(fila)):
            impresos.append(0)
            if type(fila[i]) == type(0.0):
                texto = '{:7.2f}'.format(fila[i])
            else:
                texto = str(fila[i])
            alto1 = len(texto)//(ancho[i]-4)
            if len(texto)%(ancho[i]-4) != 0:
                alto1+=1
            if alto1 > alto:
                alto = alto1
        for i in range(alto):
            print('| ',end='')
            for j in range(len(fila)):
                relleno = ancho[j]-3
                if j == len(fila)-1:
                    relleno = ancho[j] -4
                    impresos[j] = imprimir_celda(fila[j], impresos[j], relleno)
                    print(' |')
                else:
                    impresos[j] = imprimir_celda(fila[j], impresos[j], relleno)
                    print(' | ',end='')   
    if not len(tabla) > 0:
        return
    if not type(tabla[0]) is list:
        return
    ncols = len(tabla[0])
    if type(ancho) == type(0):
        ancho = [ancho+3]*ncols 
    elif type(ancho) is list:
        for i in range(len(ancho)):
            ancho[i]+=3
    else:
        print('Error. El ancho debe ser un entero o una lista de enteros')
        return
    assert len(ancho) == ncols, 'La cantidad de columnas no coincide con los tamaños dados'
    ancho[-1] += 1
    if encabezado != None:
        dividir_fila(ancho,'=')
        imprimir_fila(encabezado)
        dividir_fila(ancho,'=')
    else:
        dividir_fila(ancho)
    for fila in tabla:
        imprimir_fila(fila)
        dividir_fila(ancho)

def save_notes(cursos, estudiantes, notas, p = False,filename = './notas_estudiantes.csv'):
    try:
        #Repuesto en caso de error:
        rr = open(filename,"r", encoding='utf-8')
        repuesto = rr.read()
        rr.close()

        #abrir con with para cierre automatico
        with open(filename, mode='w', encoding='utf-8') as filenotas:
            i = 0
            for curso in cursos:
                if i < len(cursos)-1:
                    filenotas.write(curso+",")
                else:
                    filenotas.write(curso+"\n")
                i += 1
            i = 0
            for doc in estudiantes:
                if i < len(estudiantes)-1:
                    filenotas.write(doc+",")
                else:
                    filenotas.write(doc+"\n")
                i += 1
            for lisnotas in notas:
                i = 0
                for nota in lisnotas:
                    if i < len(lisnotas)-1:
                        filenotas.write(str(nota)+",")
                    else:
                        filenotas.write(str(nota)+"\n")
                    i += 1   

    except FileNotFoundError:
        return load_error(filename, "")

    except Exception as e:
        print("Ocurrio un error: ",e,"\nRestaurando el archivo...")
        try:
            filenotas = open(filename, mode='w', encoding='utf-8')
            filenotas.write(repuesto)
            filenotas.close()
        except Exception as er:
            print("ERROR FATAL: No se pudo restaurar el archivo: ",er)
        else:
            print("Archivo restaurado. No se elimino el estudiante.")
        return False
    else:
        if p:
            print("EXITO: Archivo notas_estudiantes.csv actualizado exitosamente!")
        return True
        
#Traducir la tabla de notas (-1 para Cancelado, -2 para No matriculo)
def traducir(estudiantes,notas):
    notesprint = list()
    i = 0
    for estudiante in estudiantes:
        notasclean = list()
        for nota in notas[i]:
            if nota == -1:
                notasclean.append("Cancelada")
            elif nota == -2:
                notasclean.append("No Matriculó")
            else:
                notasclean.append(nota)
        notesprint.append([estudiante]+notasclean)
        i+=1
    return notesprint

def mayor(lista):
    nmayor = lista[0]
    c = 0
    for elemento in lista:
        if elemento > nmayor:
            nmayor = elemento
            c = 1
        elif elemento == nmayor:
            c+=1

    return nmayor, c