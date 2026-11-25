#Modulo para funciones y operaciones

def loadNotes(p=False,filename = './notas_estudiantes.csv'):
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
                    delElem(columnas,len(columnas)-1)

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
                                return loadError(filename,"Hay uno o varios valores repetidos en el encabezado de cursos", lread)
                        else:
                            return loadError(filename,"Hay espacios vacios en el encabezado de cursos", lread)
                    continue

                #Obtener estudiantes

                if lact == 2:
                    for estudiante in columnas:
                        estudiante = estudiante.strip()
                        if estudiante:
                            if estudiante not in estudiantes:
                                estudiantes.append(estudiante)
                            else:
                                return loadError(filename,"Hay uno o varios valores repetidos en el encabezado de documentos", lread)    
                        else:
                            return loadError(filename,"Hay espacios vacios en el encabezado de documentos", lread)    
                    continue

                #Obtener notas
                if len(cursos) == len(columnas):
                    fnota = list()
                    for nota in columnas:
                        try:
                            nota = float(nota)
                        except ValueError:
                            return loadError(filename,"Hay uno o varios valores invalidos que no son notas", lread)
                        if nota == -1 or nota == -2 or (0 <= nota <= 5.0):
                            fnota.append(nota)
                        else:
                            return loadError(filename,"Hay nota(s) fuera del rango",lread)
                    notas.append(fnota)
                else:
                    return loadError(filename,"La cantidad de notas no coincide con la cantidad de cursos",lread)
            #Si el archivo solo tiene encabezado
            if lact < 3:
                return loadError(filename,"El archivo no tiene notas o encabezado") 
            #Si no corresponden la cantidad de filas de notas con la cantidad de estudiantes.
            if len(estudiantes) != (lact-2):
                return loadError(filename,f"La cantidad de estudiantes es {len(estudiantes)} y hay {lact-2} filas de notas",2)
                    

    except FileNotFoundError:
        return loadError(filename)
    except Exception as er:
        return loadError(filename,f"Ocurrio un error desconocido al importar {filename}: {er}")
    else:
        if p:
            print("EXITO: Archivo notas_estudiantes.csv importado exitosamente!")
        return cursos, estudiantes, notas

def loadHist(p=False, filename = './hist_matriculados.csv'):
    try:
        años = list()
        csEst = list()
        #abrir con with para cierre automatico
        with open(filename, mode='r', encoding='utf-8') as filehist:
            lact = 0 #Linea valida actual 
            lread = 0 #Linea actual del archivo
            for linea in filehist:

                #Contarla siempre
                lread += 1
                
                # Separar texto
                columnas = linea.strip().split(',') 

                #Saltar lineas vacias, incompetas y el encabezado.
                if not columnas[0] or len(columnas) < 2 or len(columnas) > 2 or columnas[0] == "Año":
                    continue

                #Limpiar cola
                if not columnas[-1]:
                    delElem(columnas,len(columnas)-1)

                lact += 1

                #Obtener datos
                try:
                    año = int(columnas[0])
                    cEst = int(columnas[1])
                except ValueError:
                    return loadError(filename,"Hay uno o varios valores invalidos que no son numericos", lread)
                if año > 9999:
                    return loadError(filename,"Hay un año invalido", lread)
                if año not in años:
                    años.append(año)
                else:
                    return loadError(filename,"Hay uno varios años repetidos", lread)
                csEst.append(cEst)
            #Si el archivo solo tiene encabezado
            if lact < 2:
                return loadError(filename,"El archivo no tiene notas o encabezado")   

    except FileNotFoundError:
        return loadError(filename)
    except Exception as er:
        return loadError(filename,f"Ocurrio un error desconocido al importar {filename}: {er}")
    else:
        if p:
            print(f"EXITO: Archivo {filename} importado exitosamente!")
        return años, csEst

def loadError(filen,texto="\n", linea = None):
    if linea != None:
        print(f"ERROR: El archivo {filen} esta corrupto en la linea {linea}\n{texto}")
    else:
        print(f"ERROR: El archivo {filen} esta corrupto o no existe\n{texto}")
    return False

def delElem(lista,indice):
    if indice > -1 and indice < len(lista):
        lista[indice:] = lista[indice+1:]
        return True
    else:
        return False

def buscarId(lista,elem,r=False):
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

def saveNotes(cursos, estudiantes, notas, p = False,filename = './notas_estudiantes.csv'):
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
        return loadError(filename, "")

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

def mayor(lista,r=True):
    nmayor = lista[0]
    c = 0
    for elemento in lista:
        if elemento > nmayor:
            nmayor = elemento
            c = 1
        elif elemento == nmayor and r:
            c+=1

    if r: return nmayor, c
    else: return nmayor

def minimo(lista):
    minimo = lista[0]
    for elemento in lista:
        if elemento < minimo:
            minimo = elemento
    return minimo

#Bubble sort optimizado.
def bubbleSort(lista):
    c = 0 #Contador de iteraciones.
    n = len(lista)

    for p in range(n - 1):
        ord = True
        for i in range(n - p - 1):
            c+=1
            if lista[i] > lista[i + 1]:
                # Intercambio directo estilo Python
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                ord = False
        if ord:
            break

    return lista, c

def selSort(lista):
    division = 0
    while division < len(lista):
        for i in range(division + 1, len(lista)):
            if lista[i] < lista[division]:
                temp = lista[i]
                lista[i] = lista[division]
                lista[division] = temp
        division += 1
    return lista

#PARTE 2

def promediar(lista,r=None):
    total = 0
    promedio = 0
    if len(lista)>0:
        for elemento in lista:
            if type(elemento) == type("a"):
                promedio+=elemento
                total+=1
            else:
                print("ERROR: No se pudo promediar.")
                return
        if r:#r = Cuantos decimales contar
            promedio=round(promedio/total,r)
        else:#sin r, entero
            promedio=round(promedio/total)
    return promedio

#Tanteo a la baja con reduccion de rangos
def tanteoBaj(años, csEst):
    #Contador de llamadas a MAE
    c = 0
    #Contador de iteraciones
    k = 0
    k1 = 0
    k2 = 0
    #Centrar años
    años = [año - (promediar(años)) for año in años]

    a = (csEst[-1] - csEst[0])/(años[-1] - años[0])
    p = promediar(csEst)
    my = mae(regresion(a, p, años), csEst)

    #Inicializar variables para tanteo en bajada por zoom
    rango,centro = a
    cambiable = True
    while cambiable:
        candidatos = list()
        a1 = centro-rango
        a2 = centro-(rango/2)
        a3 = centro
        a4 = centro+(rango/2)
        a5 = centro+rango

        y1 = regresion(a1,p,años)
        y2 = regresion(a2,p,años)
        y3 = regresion(a3,p,años)
        y4 = regresion(a4,p,años)
        y5 = regresion(a5,p,años)

        candidatos = [(mae(y1, csEst), a1),(mae(y2, csEst), a2),(mae(y3, csEst), a3),(mae(y4, csEst), a4),(mae(y5, csEst), a5)]
        c+=5 #Se usa mas MAE
        my, centro= minimo(candidatos)
        if not (a == a1 or a == a5):
            rango = rango/2
        #Evaluar si finalizar
        if rango < 0.001:
            a = centro
            while True:    
                candidatos = list()
                minB = csEst[0]
                for cc in csEst:
                    if cc < minB:
                        minB = cc
                rango = (mayor(csEst) - minB) / 2
                centro = (minB + mayor(csEst)) / 2
                p1 = centro-rango
                p2 = centro-(rango/2)
                p3 = centro
                p4 = centro+(rango/2)
                p5 = centro+rango

                y1 = regresion(a,p1,años)
                y2 = regresion(a,p2,años)
                y3 = regresion(a,p3,años)
                y4 = regresion(a,p4,años)
                y5 = regresion(a,p5,años)

                candidatos = [(mae(y1, csEst), p1),(mae(y2, csEst), p2),(mae(y3, csEst), p3),(mae(y4, csEst), p4),(mae(y5, csEst), p5)]
                c+=5 #Se usa mas MAE
                my, centro= minimo(candidatos)
                if not (a == a1 or a == a5):
                    rango = rango/2
                #Evaluar si finalizar
                if rango < 0.001:
                    #Convertir p (b normalizada con la media) en b con los años REALES
                    b = centro - a*promediar(años)
                    break
            break
 
    return a,b,my,c,k,k1,k2


#tanteo a la baja INOPTIMO
def tanteoBajOriginal(años, csEst):
    #Contador de llamadas a MAE
    c = 0
    #Contador de iteraciones
    k = 0
    k1 = 0
    k2 = 0
    a = (csEst[-1] - csEst[0])/(años[-1] - años[0])
    b = csEst[-1] - (a*años[-1]) 
    my = mae(regresion(a, b, años), csEst)
    c+=1
    #paso = 1/10 del valor base
    pasoa = max(abs(a) * 0.10, 0.1)
    pasob = max(abs(b) * 0.10, 0.1)
    cambiable = True
    while cambiable:
        #mae debug
        print(my)
        k+=1
        a1 = a+pasoa
        a2 = a-pasoa

        b1 = b+pasob
        b2 = b-pasob

        y1 = regresion(a1,b1,años)
        y2 = regresion(a2,b1,años)
        y3 = regresion(a1,b2,años)
        y4 = regresion(a2,b2,años)
        y5 = regresion(a1,b,años)
        y6 = regresion(a2,b,años)
        y7 = regresion(a,b1,años)
        y8 = regresion(a,b2,años)

        candidatos = [(mae(y1, csEst), a1, b1),(mae(y2, csEst), a2, b1),(mae(y3, csEst), a1, b2),(mae(y4, csEst), a2, b2),(mae(y5, csEst), a1, b),(mae(y6, csEst), a2, b),(mae(y7, csEst), a, b1),(mae(y8, csEst), a, b2)]
        c+=8
        mejor_m, mejor_a, mejor_b = minimo(candidatos)

        #Evaluar si es menor error
        if mejor_m < my:
            a, b, my = mejor_a, mejor_b, mejor_m
            k1 += 1
        else:#Actualizar el paso o finalizar
            k2 += 1
            if pasoa > 0.001 or pasob > 0.001:
                pasoa, pasob = pasoa/2,pasob/2
            else:
                cambiable = False
    return a,b,my,c,k,k1,k2

#Regresion lineal
def regresion(a,b,xs):
    ys = list()
    for x in xs:
        ys.append(a*x+b)
    return ys

#MAE
def mae(tanteo, csEst):
    if len(tanteo) == len(csEst):
        error = 0
        for i in range(len(tanteo)):
            error += abs(csEst[i] - tanteo[i])
        return error/len(csEst)
    else:
        print("ERROR: Y tanteados no coincide con Y reales, abortando...")
        return
        