P = int(input("Ingrese Principal:"))
while P < 0:
             print ("Error, el valor debe ser positivo, vuelva a intentarlo")
             P = int(input("Ingrese Principal:"))


r = float(input("Ingrese Tasa de Interes Anual (en %):"))/100
while r < 0: 
             print ("Error, el valor debe ser positivo, vuelva a intentarlo")
             r = float(input("Ingrese Tasa de Interes Anual:"))/100


n = float(input("Ingrese Numero de Veces que se Capitaliza el Interes al Año:"))
while n < 0:
              print ("Error, el valor debe ser positivo, vuelva a intentarlo")
              n = float(input("Ingrese Numero de Veces que se Capitaliza el Interes al Año:"))


t = int(input("Ingrese Numero de años de la Inversion:"))
while t < 0:
             print ("Error, el valor debe ser positivo, vuelva a intentarlo")
             t = int(input("Ingrese Numero de años de la Inversion:"))


A = P*(1+r/n)**(n*t)

print (f"El monto acumulado es: {A:.2f}")
