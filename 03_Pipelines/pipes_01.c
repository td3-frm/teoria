#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

int main() {
    int fd[2];     // Array para manejar los descriptores de archivo del pipe
    pid_t cpid;    // PID del proceso hijo
    char buf;      // Buffer para leer el mensaje caracter por caracter
    char mensaje[] = "Hola, proceso hijo!\n"; // Mensaje a enviar

    printf("Creando PIPE...\n");
    // Crea el pipe
    if (pipe(fd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    // Crea el proceso hijo
    cpid = fork();
    if (cpid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (cpid == 0) {    // Código del proceso hijo
        printf("Proceso Hijo...\n");
        close(fd[1]);  // Cierra el lado de escritura del pipe no usado

        // Lee el mensaje enviado por el padre, caracter por caracter
        while (read(fd[0], &buf, 1) > 0) {
            write(STDOUT_FILENO, &buf, 1);
            write(STDOUT_FILENO, "\n", 1);
        }

        close(fd[0]); // Cierra el lado de lectura del pipe
        printf("Proceso Hijo finaliza...\n");
        _exit(EXIT_SUCCESS);

    } else {            // Código del proceso padre
        printf("Proceso Padre...\n");
        close(fd[0]);  // Cierra el lado de lectura del pipe no usado

        // Escribe el mensaje en el pipe
        write(fd[1], mensaje, strlen(mensaje));
        close(fd[1]);  // Cierra el lado de escritura, generando EOF para el lector

        wait(NULL);        // Espera a que el hijo termine

        printf("Proceso Padre finaliza...\n");
        exit(EXIT_SUCCESS);
    }
}
