/*  
 * Ejercicio 1 del TP Hilos
 *
 */

#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void * hola(void * nro) {
  
   sleep(3);
   printf("Hola, soy el hilo %d\n", *((int*) nro) );
   pthread_exit(NULL);
   //exit(0);

}

int main() {

    pthread_t pth;
    int rc, t;

    t = 100;
     
    printf("Main creando el hilo nro %d\n", t);
        
    rc = pthread_create(&pth, NULL, hola , (void *)(&t)  );
     
    if (rc != 0){
         printf("ERROR; pthread_create() = %d\n", rc);
         exit(-1);        
    };
  
   printf("Espera a que termine hilo\n");

   pthread_join(pth, NULL);

   printf("Termina hilo main\n");

   pthread_exit(NULL);
   
   return 0;
}
