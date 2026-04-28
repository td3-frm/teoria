/* Ejercicio 1 del TP de semaforos sin nombre */

//---------------- Uso de semáforos sin nombre ----------------//

#include <stdio.h>
#include <pthread.h>    
#include <unistd.h>
#include <stdlib.h>
#include <semaphore.h>
#include <sys/stat.h>
#include <fcntl.h>

//------- variables globales

pthread_t pth;
sem_t sem;


//---------------- Hilo ---------------------------//

void * HILO(){

	int s, sval;

	sleep(10);
	
	printf ("Soy el HILO voy a incrementar semaforo\n");

//------lee valor de sem 
	sem_getvalue(&sem, &sval);
	printf("Valor de semaforo: %d\n", sval);
	
//------ Se incrementa sem 
	s=sem_post(&sem);
	if (s != 0) {
		printf("ERROR sem_post()\n");
		exit(-1);     }
	
	pthread_exit (NULL);
}

//-----------------------------------------------------------//

int main() {
	
	int s, sval, rc;
	
	printf ("Main crea el semaforo\n");

//------ inicializa el sem sin nombre 
	s=sem_init(&sem, 0, 0);
	if (s != 0) {
		printf("ERROR sem_init()\n");
		exit(-1);     }

//------lee valor de sem 
	sem_getvalue(&sem, &sval);
	printf("Valor de semaforo: %d\n", sval);

//------ Crea los hilos 
	rc = pthread_create(&pth, NULL, HILO, NULL);
	if (rc)    {
		printf ("ERROR; pthread_create() = %d\n", rc);
		exit (-1);    }
	
	printf ("Soy el main voy a decrementar semaforo\n");

//------decremento de sem
	s = sem_wait(&sem);
	if (s != 0) {
		printf("ERROR sem_wait()\n");
		exit(-1);     }

	printf ("Soy el main, sigo ejecutando\n");

//------elimina de sem
	printf("Se elimina el semaforo\n");
	s=sem_destroy(&sem);
	if (s != 0) {
		printf("ERROR sem_unlink()\n");
		exit(-1);  }

//--------------------------------------------
   
	pthread_join (pth, NULL);
	
	printf("Fin del main() \n");
	
	pthread_exit (NULL);
}


