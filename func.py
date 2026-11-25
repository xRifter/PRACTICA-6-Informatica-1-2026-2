#Modulo para funciones y operaciones
'''
Modulo de funciones y operaciones de la practica 6.

Parte 1: carga y guardado de notas_estudiantes.csv, busqueda, eliminacion,
mayor nota, impresion de tablas y ordenamientos (burbuja y seleccion).
Parte 2: carga de hist_matriculados.csv, regresion lineal, MAE y tanteo
a la baja para hallar la recta que mejor se ajusta a los datos.

Estructura de datos base (EED): 3 listas paralelas, cursos, estudiantes y
notas. La posicion i de estudiantes corresponde a la fila notas[i].
Notas especiales: -1 = curso cancelado, -2 = no matriculo.
'''

#PARTE 1

def loadNotes(p=False,filename = './notas_estudiantes.csv'):
    '''
    Carga el archivo de notas en memoria y valida su estructura. Si una
    sola comprobacion falla, rechaza el archivo completo.

    Comprueba: que no haya cursos ni documentos repetidos o vacios, que la
    cantidad de notas de cada fila coincida con la cantidad de cursos, que
    las notas sean validas (-1, -2 o entre 0 y 5) y que la cantidad de filas
    de notas coincida con la cantidad de estudiantes. Ignora lineas vacias
    y tolera una sola coma sobrante al final de la linea.

    Argumentos:
        p: Booleano. Si es True imprime un mensaje de exito al cargar
        filename: Ruta del archivo de notas

    Retorna:
        Tupla (cursos, estudiantes, notas) si todo salio bien, o False si
        hubo algun error (el error se reporta con loadError). Por eso el
        retorno se debe guardar primero en una variable antes de
        desempaquetar.
    '''
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

#loadHist Optimizado
def loadHist(p=False, filename = './hist_matriculados.csv'):
    '''
    Carga el historico de matriculados (version OPTIMIZADA). Construye 2
    listas simultaneamente para que sus indices se correspondan.

    Para revisar años repetidos usa una tabla de 10000 casillas booleanas
    donde cada año es su propia posicion, asi cada consulta cuesta 1 sola
    comprobacion en lugar de recorrer la lista de años. A cambio ocupa
    siempre 10000 casillas de memoria, por lo que solo vale la pena a
    partir de unas 140 filas. Ignora lineas vacias, incompletas y el
    encabezado.

    Argumentos:
        p: Booleano. Si es True imprime un mensaje de exito al cargar
        filename: Ruta del archivo del historico

    Retorna:
        Tupla (años, csEst, c) donde c es la cantidad de consultas hechas a
        la tabla de casillas, o False si hubo algun error.
    '''
    #Contador de consultas a Años:
    c = 0
    #Crear tabla de casillas:
    cas = list()
    for _ in range(10000): #Cada año correspondera a su posicion y el valor sera para ver si ya esta.
        cas.append(False)
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
                if año > 9999 or año < 0:
                    return loadError(filename,"Hay un año invalido", lread)
                #Comparar con la tabla de casillas por años
                c+=1 #1 consulta a cas.
                if not cas[año]:
                    años.append(año)
                    cas[año] = True
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
        return años, csEst, c

#LoadHist ineficiente
def loadHistOG(p=False, filename = './hist_matriculados.csv'):
    '''
    Carga el historico de matriculados (version ORIGINAL sin optimizar).
    Se conserva para comparar eficiencia con loadHist.

    Para revisar años repetidos usa "not in" sobre la lista de años, asi que
    en cada fila recorre todos los años ya cargados: con n datos hace
    n*(n-1)/2 consultas (4950 con 100 datos, 499500 con 1000).

    Argumentos:
        p: Booleano. Si es True imprime un mensaje de exito al cargar
        filename: Ruta del archivo del historico

    Retorna:
        Tupla (años, csEst, c) donde c es la cantidad de consultas hechas a
        la lista de años, o False si hubo algun error.
    '''
    #Contador de consultas a años:
    c = 0
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
                if año > 9999 or año < 0:
                    return loadError(filename,"Hay un año invalido", lread)
                #Por cada ejecucion se hacen len(años) consultas:
                c+=len(años)
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
        return años, csEst, c

def loadError(filen,texto="\n", linea = None):
    '''
    Funcion auxiliar para reportar errores al cargar archivos, evita repetir
    el mismo bloque en cada comprobacion de los cargadores.

    Argumentos:
        filen: Nombre del archivo que fallo
        texto: Descripcion del error especifico
        linea: Linea del archivo donde esta el error (opcional). Si es None
            el mensaje indica que el archivo esta corrupto o no existe

    Retorna:
        Siempre False, para que los cargadores lo devuelvan directamente.
    '''
    if linea != None:
        print(f"ERROR: El archivo {filen} esta corrupto en la linea {linea}\n{texto}")
    else:
        print(f"ERROR: El archivo {filen} esta corrupto o no existe\n{texto}")
    return False

def delElem(lista,indice):
    '''
    Elimina el elemento de una posicion modificando la lista original con
    cortes, asi no hay que reasignar la variable en main.

    Argumentos:
        lista: Lista a modificar
        indice: Posicion a eliminar. No acepta negativos

    Retorna:
        True si se elimino, False si el indice es inaccesible.
    '''
    if indice > -1 and indice < len(lista):
        lista[indice:] = lista[indice+1:]
        return True
    else:
        return False

def buscarId(lista,elem,r=False):
    '''
    Busqueda lineal de un elemento en una lista.

    Argumentos:
        lista: Lista donde se busca
        elem: Elemento a buscar
        r: Booleano. Por defecto (False) se detiene en la primera
            coincidencia. Si es True recorre toda la lista porque puede
            haber elementos repetidos

    Retorna:
        El indice si hubo una sola coincidencia, una lista de indices si
        hubo varias (solo con r=True), o -1 si no hubo coincidencias.
    '''
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
    '''
    Pide una entrada por teclado hasta que sea una de las opciones validas.
    La entrada se convierte a minusculas antes de comparar.

    Argumentos:
        strinput: Texto que se muestra al pedir la entrada
        datosvalidos: Lista de opciones validas. Puede contener strings o
            listas anidadas de strings
        digito: Si es verdadero, ademas exige que la entrada sea un digito

    Retorna:
        La entrada (string en minusculas) que paso la validacion.
    '''
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
    '''
    Guarda la estructura de datos en el archivo de notas, para que los
    cambios (por ejemplo eliminar un estudiante) persistan al recargar.

    Antes de escribir guarda el contenido original del archivo en una
    variable; si ocurre algun error durante la escritura, restaura el
    archivo y avisa al usuario.

    Argumentos:
        cursos: Lista de cursos (primera linea del archivo)
        estudiantes: Lista de documentos (segunda linea del archivo)
        notas: Lista de listas con las notas de cada estudiante
        p: Booleano. Si es True imprime un mensaje de exito al guardar
        filename: Ruta del archivo de notas

    Retorna:
        True si se guardo correctamente, False si hubo algun error.
    '''
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
    '''
    Arma la tabla lista para imprimir, reemplazando las notas especiales por
    texto: -1 por "Cancelada" y -2 por "No Matriculó".

    Argumentos:
        estudiantes: Lista de documentos de los estudiantes
        notas: Lista de listas con las notas de cada estudiante

    Retorna:
        Lista de filas, cada una [estudiante, nota1, nota2, ...]. Las
        estructuras originales no se modifican.
    '''
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
    '''
    Halla el mayor elemento de una lista recorriendola una sola vez.

    Argumentos:
        lista: Lista no vacia de elementos comparables
        r: Booleano. Si es True tambien cuenta cuantas veces se repite el
            mayor

    Retorna:
        Con r=True una tupla (mayor, veces que aparece); con r=False solo
        el mayor.
    '''
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
    '''
    Halla el menor elemento de una lista recorriendola una sola vez. Si los
    elementos son tuplas, compara por el primer valor y desempata con los
    siguientes.

    Argumentos:
        lista: Lista no vacia de elementos comparables

    Retorna:
        El menor elemento de la lista.
    '''
    minimo = lista[0]
    for elemento in lista:
        if elemento < minimo:
            minimo = elemento
    return minimo

#Bubble sort optimizado.
def bubbleSort(lista):
    '''
    Ordena la lista de menor a mayor con burbuja optimizado: si en una
    pasada no hubo intercambios, la lista ya esta ordenada y se detiene.
    Modifica la lista original.

    Argumentos:
        lista: Lista de elementos comparables (por ejemplo tuplas
            (valor, indice))

    Retorna:
        Tupla (lista ordenada, c) donde c es la cantidad de comparaciones
        realizadas.
    '''
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
    '''
    Ordena la lista de menor a mayor con ordenamiento por seleccion: fija
    una posicion (division) y la intercambia con cualquier elemento menor
    que encuentre a su derecha. Modifica la lista original.

    Argumentos:
        lista: Lista de elementos comparables (por ejemplo tuplas
            (valor, indice))

    Retorna:
        La misma lista, ya ordenada.
    '''
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
    '''
    Calcula el promedio de una lista de enteros.

    Argumentos:
        lista: Lista de numeros enteros. Si encuentra un valor que no es
            entero imprime un error y termina
        r: Cantidad de decimales a conservar. Si no se especifica, el
            promedio se redondea a un entero

    Retorna:
        El promedio, 0 si la lista esta vacia, o None si hubo un valor
        invalido.
    '''
    total = 0
    promedio = 0
    if len(lista)>0:
        for elemento in lista:
            if type(elemento) == type(123):
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
    '''
    Tanteo a la baja OPTIMIZADO para hallar la recta y = ax+b que minimiza
    el MAE sobre los datos.

    Optimizaciones: centra los años restandoles su media (asi a solo gira la
    recta alrededor del centro) y usa un zoom: evalua 5 puntos alrededor del
    centro (centro-rango, centro-rango/2, centro, centro+rango/2,
    centro+rango) y, si el ganador no es un extremo, reduce el rango a la
    mitad. Se detiene cuando los rangos de a y de p son menores a 0.001.
    Como el candidato central siempre es la solucion actual, el MAE nunca
    sube entre vueltas. Al final convierte p (b normalizada) en b con los
    años reales.

    Argumentos:
        años: Lista de años (valores X)
        csEst: Lista con la cantidad de estudiantes de cada año (valores Y)

    Retorna:
        Tupla (a, b, my, c, k, k1, k2):
            a, b: pendiente y corte de la recta hallada (años reales)
            my: MAE final
            c: cantidad de llamadas a mae
            k: vueltas del while
            k1: veces que el centro se movio
            k2: veces que el centro se quedo quieto (hace zoom)
    '''
    #Contador de llamadas a MAE
    c = 0
    #Contador de iteraciones
    k = 0
    #Veces que el centro se mueve (a1, a2, a4, a5)
    k1 = 0
    #Veces que el centro se queda quieto y hace Zoom
    k2 = 0
    #Centrar años
    pa = promediar(años)
    años = [año - pa for año in años]

    a = (csEst[-1] - csEst[0])/(años[-1] - años[0])
    p0 = promediar(csEst)
    minB = minimo(csEst)
    maxB = mayor(csEst,False)
    pAct = (minB + maxB) / 2
    my = mae(regresion(a, pAct, años), csEst)
    c+=1

    #Inicializar variables para tanteo en bajada por zoom
    rangoA,centroA = abs(a),a
    rangoB = (maxB - minB) / 2
    centroB = pAct
    while rangoA>=0.001 or rangoB>=0.001:
        k+=1
        if rangoA >= 0.001:
            candidatos = list()
            a1 = centroA-rangoA
            a2 = centroA-(rangoA/2)
            a3 = centroA
            a4 = centroA+(rangoA/2)
            a5 = centroA+rangoA

            y1 = regresion(a1,pAct,años)
            y2 = regresion(a2,pAct,años)
            y3 = regresion(a3,pAct,años)
            y4 = regresion(a4,pAct,años)
            y5 = regresion(a5,pAct,años)

            candidatos = [(mae(y1, csEst), a1),(mae(y2, csEst), a2),(mae(y3, csEst), a3),(mae(y4, csEst), a4),(mae(y5, csEst), a5)]
            c+=5 #Se usa mas MAE
            ganador = minimo(candidatos)
            if ganador[1] == centroA:
                k2+=1
            else:
                k1+=1
            print(my)
            my, centroA= ganador
            print(my)
            if not (centroA == a1 or centroA == a5):
                rangoA = rangoA/2
            if a != centroA:
                a = centroA 

        if rangoB >= 0.001:
            candidatos = list()
            p1 = centroB-rangoB
            p2 = centroB-(rangoB/2)
            p3 = centroB
            p4 = centroB+(rangoB/2)
            p5 = centroB+rangoB

            y1 = regresion(a,p1,años)
            y2 = regresion(a,p2,años)
            y3 = regresion(a,p3,años)
            y4 = regresion(a,p4,años)
            y5 = regresion(a,p5,años)

            candidatos = [(mae(y1, csEst), p1),(mae(y2, csEst), p2),(mae(y3, csEst), p3),(mae(y4, csEst), p4),(mae(y5, csEst), p5)]
            c+=5 #Se usa mas MAE
            ganador = minimo(candidatos)
            if ganador[1] == centroB:
                k2+=1
            else:
                k1+=1
            my, centroB= ganador
            if not (centroB == p1 or centroB == p5):
                rangoB = rangoB/2
            if pAct != centroB:
                pAct = centroB 
    #Convertir p (b normalizada con la media) en b con los años REALES
    b = centroB - a*pa
 
    return a,b,my,c,k,k1,k2


#tanteo a la baja INOPTIMO
def tanteoBajOriginal(años, csEst):
    '''
    Tanteo a la baja ORIGINAL (sin optimizar). Se conserva para comparar
    eficiencia con tanteoBaj.

    Parte de a = Delta(csEst)/Delta(años) y b de la recta que pasa por el
    ultimo punto. Define un paso de 1/10 del valor de a y de b (minimo
    0.1). En cada vuelta evalua 8 combinaciones de (a +/- paso, b +/- paso)
    y se queda con la de menor MAE; si ninguna mejora el error, reduce los
    pasos a la mitad. Termina cuando ambos pasos son menores o iguales a
    0.001.

    Argumentos:
        años: Lista de años (valores X)
        csEst: Lista con la cantidad de estudiantes de cada año (valores Y)

    Retorna:
        Tupla (a, b, my, c, k, k1, k2):
            a, b: pendiente y corte de la recta hallada
            my: MAE final
            c: cantidad de llamadas a mae
            k: vueltas del while
            k1: veces que se encontro un menor error
            k2: veces que se cambio el paso
    '''
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
    '''
    Evalua la recta y = ax+b para cada valor de X. Es generica para
    reutilizarla en varios puntos de la parte 2.

    Argumentos:
        a: Pendiente de la recta
        b: Corte de la recta con el eje Y
        xs: Lista de valores X

    Retorna:
        Lista con un valor Y por cada X.
    '''
    ys = list()
    for x in xs:
        ys.append(a*x+b)
    return ys

#MAE
def mae(tanteo, csEst):
    '''
    Calcula el error absoluto medio (MAE): promedio de la diferencia en
    valor absoluto entre cada Y tanteado y su Y real gemelo.

    Argumentos:
        tanteo: Lista de Y obtenidas con la recta tanteada
        csEst: Lista de Y reales

    Retorna:
        El MAE, o None si las listas no tienen el mismo tamaño.
    '''
    if len(tanteo) == len(csEst):
        error = 0
        for i in range(len(tanteo)):
            error += abs(csEst[i] - tanteo[i])
        return error/len(csEst)
    else:
        print("ERROR: Y tanteados no coincide con Y reales, abortando...")
        return