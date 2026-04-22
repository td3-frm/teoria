#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>

#define TRUE 1

void manejador_senial(int a){

  //printf ("Ya termino");
  write(STDOUT_FILENO, "Saliendo...", 12);
  exit(0);
}


int main ()
{
   signal(SIGSEGV, manejador_senial);
   // signal(SIGINT, manejador_senial);  //Ctrl + Z

   printf("Proceso PID = %d\n", getpid());   

   while(TRUE);
   
   exit(0);
}
