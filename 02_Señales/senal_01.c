#include <stdio.h>
#include <signal.h>
#include <unistd.h>

// Manejador de la señal SIGINT
void handle_sigint(int sig) {
    printf("Se capturó SIGINT (id de señal: %d)\n", sig);
    // Puedes agregar más lógica aquí para limpiar, cerrar archivos, etc.
    printf("Salida elegante.\n");
    _exit(0); // Salida inmediata, reemplaza con "exit(0)" si no necesitas terminación inmediata
}

int main() {
   int pid;
   
    // Asigna el manejador de señal SIGINT a handle_sigint
    // signal(SIGINT, handle_sigint);
    signal(SIGINT, SIG_IGN );
    pid = getpid();
    printf("pid : %d", pid); 
     	
    // Ciclo infinito para mantener el programa ejecutándose y poder capturar la señal
    while (1) {
        printf("Esperando SIGINT. Presiona Ctrl+C para terminar.\n");
        sleep(1); // Pausa el programa por 1 segundo
    }

    return 0;
}
