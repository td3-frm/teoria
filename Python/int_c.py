import math

#Capital Inicial
print ("Ingrese el capital inicial ")
ci=input()


while int(ci) < 0 :
    print("El capital no puede ser negativo, ingrese nuevamente:")
    ci=input()

#Tasa anual
print ("Ingrese la tasa anual (%) ")
i=float(input())

while i < 0 :
    print("La tasa no puede ser negativa, ingrese nuevamente:")
    i=float(input())
    
#Periodo de Tiempo
print ("Ingrese el numero de años: ")
t=input()


while int(t) < 0 :
    print("El tiempo no puede ser negativo ni cero , ingrese nuevamente:")
    t=input()

 #Capitalizacion
print ("Ingrese el numero de veces que se capitalizara por año: ")
n=float(input())


while float(n) < 0 :
    print("La capitalizacion no puede ser negativa ni cero , ingrese nuevamente:")
    n=input()
   

print()
print("///  Datos  ///")
print()
print ("Capital inicial: $",ci,)
i = round (i, 2)  
print("Tasa anual:", i,"%")
print("Tiempo:", t,"años")
print("Numero de veces que se capitalizara por año:",n,)
print()
print("///////////////////")
print()
#Calculo
i=i/100


cf= float(ci)*(1+i/n) ** (n*float(t))

cf = round (cf, 2) 

print("Al cabo de ",t,"años , el capital acumulado sera : $",cf,)
