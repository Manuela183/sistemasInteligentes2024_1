## CREADO Versión inicial NDD Sept 2020
## Modificaciones posteriores 13 de marzo de 2024
## Realizado por: Manuela Marulanda Aguirre y Paulina Osorio Rodriguez

import random
import numpy as np

#Función para generar poblacion inicial
def generar_poblacion_inicial(n, x, pesos):
  poblInicial = np.random.randint(0, 2, (n, x))
  print("Población inicial: ", poblInicial)
  for i in range(n):
    pesoIndividuo = 0
    for j in range(x):
      pesoIndividuo += poblInicial[i][j] * pesos[j]
      

    while pesoIndividuo > 15:
      poblInicial[i] = np.random.randint(0, 2, (1, x))
      pesoIndividuo = 0
      for m in range(n):
        pesoIndividuo += poblInicial[i][m] * pesos[m]

  return poblInicial


##### FUNCIONES PARA OPERADORES

#Consigo el fitness de la poblacion
def calculo_tabla(n,x,poblIt,utilidad,pesos):
    peso = 0
    suma = 0
    total = 0
    for i in range(0, n):
      for j in range(0,x):
        suma += poblIt[i,j] * utilidad[j]
        peso += poblIt[i,j] * pesos[j]
      fitness[i] = suma
      total += suma
      suma = 0
      pesoFinal[i] = peso
      peso = 0
      
    return fitness,total,pesoFinal

#Imprimo la tabla con la probabilidad
def imprime(n,total,fitness,poblIt, pesoFinal):
    #Tabla de evaluación de la Población
    acumula = 0
    print ("\n",'Tabla Iteración:',"\n")
    for i in range(0, n):
      probab = fitness[i]/total
      acumula += probab
      print([i + 1]," ",poblIt[i],"  ",fitness[i]," ",pesoFinal[i]," ", "{0:.3f}".format(probab)," ","{0:.3f}".format(acumula))
      acumulado[i] = acumula
    print("Total Fitness:      ", total, "\n")
    return acumulado

#Genera un numero aleatorio para seleccionar el padre
def seleccion(acumulado):
  print("\nOPERACION SELECCION")
  escoje=np.random.rand()
  print("escoje:      ", escoje)
    
  for i in range(0,n):
    if acumulado[i] > escoje:
      padre=poblIt[i]
      break
  return (padre)
    
    
def cruce(random,papa1,papa2,n):
    print("\nOPERACION CRUCE")
    if random < Pcruce:
      print("Mas grande", Pcruce, "que ", random, "-> Si Cruzan")
      puntocorte = np.random.randint(1, n-1)
      print("Punto de corte: ", puntocorte)
      temp1 = papa1[0:puntocorte] # [i:j] corta desde [i a j)
      temp2 = papa1[puntocorte:n] # puedo poner n así el vector vaya hasta una posición antes, ya que es no inclusivo
      print(temp1,temp2)
      temp3 = papa2[0:puntocorte]
      temp4 = papa2[puntocorte:n]
      print(temp3,temp4)
      hijo1 = list(temp1)
      hijo1.extend(list(temp4))
      hijo2 = list(temp3)
      hijo2.extend(list(temp2))

    else:
      print("Menor", Pcruce, "que ", random, "-> NO Cruzan")
      hijo1 = papa1
      hijo2 = papa2
    
    return hijo1,hijo2
    
def mutacion(hijoA,hijoB,Pmuta,n):
  print("\nOPERACION MUTACION")
  hijoAMuta = np.random.uniform(0, 1 + 0.00000001, (n)) 
  hijoBMuta = np.random.uniform(0, 1 + 0.00000001, (n))
  print("Matrices de probabilidad de mutación: ")
  print("Matriz de hijo A: ", hijoAMuta)
  print("Matriz de hijo B: ", hijoBMuta)
  banderaHijoAMuta = 0
  banderaHijoBMuta = 0

  for i in range(n):

    if hijoAMuta[i] < Pmuta:
      banderaHijoAMuta += 1
      if hijoA[i] == 0:
        hijoA[i] = 1
      else:
        hijoA[i] = 0

    if hijoBMuta[i] < Pmuta:
      banderaHijoBMuta += 1
      if hijoB[i] == 0:
        hijoB[i] = 1
      else:
        hijoB[i] = 0
  
  if banderaHijoAMuta > 0:
    print("Hijo A mutó: ", hijoA)
  else:
    print("Hijo A no mutó")

  if banderaHijoBMuta > 0:
    print("Hijo B mutó: ", hijoB)
  else:
    print("Hijo B no mutó")

  return hijoA,hijoB

# El número de filas de individuos debe ser igual al numero de filas de pesos
def calcular_Peso_Individuo(individuo, pesos):  
  pesoIndividuo = 0
  for i in range(len(individuo)):
    pesoIndividuo += individuo[i] * pesos[i]

  return pesoIndividuo

def evaluar_aceptacion_individuo(pesoHijoA, pesoHijoB, pesoMochila, nueva_generacion):
  print("\nEVALUACION DE ACEPTACION DE HIJOS")
  if pesoHijoA <= pesoMochila:
    nueva_generacion.append(hijoA)
    print("Hijo A aceptado en la nueva generación")
  else:
    print("El hijo A excedió el peso no será aceptado en la nueva generación")
            
  if pesoHijoB <= pesoMochila and len(nueva_generacion) < 4:
    print("Hijo B aceptado en la nueva generación")
    nueva_generacion.append(hijoB)
  elif pesoHijoB <= pesoMochila and len(nueva_generacion) == 4:
    print("El hijo B no será agregado porque la nueva generación ha sido completada")
  else:
    print("El hijo B excedió el peso no será aceptado en la nueva generación")
    
  return nueva_generacion

    
#### Parametros #####
x = 4  # Numero de variables de decision - Elementos diferentes: x - 4 objetos
n = 4  # Numero de individuos en la poblacion - cromosomas: n - problación de 4 individuos
Pcruce = 0.98  # Probabilidad de Cruce
Pmuta = 0.1   # Probabilidad de Mutación
PesoMochila = 15 # Peso máximo de la mochila


fitness = np.empty((n))
acumulado = np.empty((n))
pesoFinal = np.empty((n))
suma = 0
total = 0

# Ingresar los datos del Problema de la Mochila - Peso y Utilidad de los Elementos
pesos = [7, 6, 8, 2]
utilidad = [4, 5, 6, 3]

#poblIt = generar_poblacion_inicial(n, x, pesos)

poblInicial = np.random.randint(0, 2, (n, x))
print("Poblacion inicial Aleatoria:","\n", poblInicial)
print("\n","Utilidad:", utilidad) 
print("\n","Pesos", pesos )   
poblIt=poblInicial


'''print("Poblacion inicial:","\n", poblIt)
print("\n","Utilidad:", utilidad)
print("\n","Pesos", pesos )'''

######  FIN DE LOS DATOS INICIALES  ######

##Llama función evalua, para calcular el fitness de cada individuo
fitness,total,pesoFinal=calculo_tabla(n,x,poblIt,utilidad,pesos)


##### imprime la tabla de la iteracion 
imprime(n,total,fitness,poblIt, pesoFinal)

##### ***************************************
# Inicia Iteraciones

for iter in range(2):
  print("----------------- Generación ", iter+1, " -----------------\n")
  nueva_generacion = []
  iteracion = iter+1
  
  while(len(nueva_generacion) < n):
    print("\nIteración ", iteracion, "\n")
    papa1=seleccion(acumulado) # Padre 1
    print("padre 1:", papa1)
    papa2=seleccion(acumulado) # Padre 2
    print("padre 2:", papa2)
      
    hijoA,hijoB=cruce(np.random.rand(),papa1,papa2,n)
    print("hijo1: ", hijoA)
    #poblIt[i]=hijoA
    print("hijo2: ", hijoB)
    #poblIt[i+1]=hijoB

    hijoA,hijoB=mutacion(hijoA,hijoB,Pmuta,n)
    print("\nCALCULO DE PESO DE HIJOS")
    pesoHijoA = calcular_Peso_Individuo(hijoA, pesos)
    pesoHijoB = calcular_Peso_Individuo(hijoB, pesos)

    print("Peso Hijo A: ", pesoHijoA)
    print("Peso Hijo B: ", pesoHijoB)

    nueva_generacion = evaluar_aceptacion_individuo(pesoHijoA, pesoHijoB, PesoMochila, nueva_generacion)
    iteracion += 1    
    print("\nPeso Final de generación después de recorrer cada hijo: ", pesoFinal)

  poblIt = np.array(nueva_generacion)
  print("\n","Nueva poblacion Iteración ", iter+1,"\n", poblIt, "Nuevo Peso Final: ", pesoFinal)
  fitness,total, pesoFinal=calculo_tabla(n,x,poblIt,utilidad,pesos)

  ##### imprime la tabla de la iteracion
  imprime(n,total,fitness,poblIt,pesoFinal)
