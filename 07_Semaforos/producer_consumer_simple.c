/*
 * prod_cons_simple.c
 *
 * One producer, one consumer, circular buffer of 4 slots.
 *
 * Build:
 *   gcc -o prod_cons_simple prod_cons_simple.c -lpthread
 * Run:
 *   ./prod_cons_simple
 */

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define BUFFER_SIZE  4
#define NUM_ITEMS   10

/* ── shared state ───────────────────────────────── */
static int buffer[BUFFER_SIZE];
static int head = 0;   /* next write position */
static int tail = 0;   /* next read  position */

static sem_t sem_empty;   /* free slots  (init = BUFFER_SIZE) */
static sem_t sem_full;    /* filled slots (init = 0)          */
static sem_t mutex;       /* mutual exclusion  (init = 1)     */

/* ── producer ───────────────────────────────────── */
static void *producer(void *arg) {
    (void)arg;

    for (int item = 1; item <= NUM_ITEMS; item++) {
        sleep(0.5);   /* simulate work */

        sem_wait(&sem_empty);   /* wait for a free slot   */
        sem_wait(&mutex);

        buffer[head] = item;
        head = (head + 1) % BUFFER_SIZE;
        printf("[P] produced %d\n", item);

        sem_post(&mutex);
        sem_post(&sem_full);    /* signal a new item is ready */
    }
    return NULL;
}

/* ── consumer ───────────────────────────────────── */
static void *consumer(void *arg) {
    (void)arg;

    for (int i = 0; i < NUM_ITEMS; i++) {
		//sleep(2);   /* simulate work */
		
        sem_wait(&sem_full);    /* wait for an item       */
        sem_wait(&mutex);

        int item = buffer[tail];
        tail = (tail + 1) % BUFFER_SIZE;
        printf("        [C] consumed %d\n", item);

        sem_post(&mutex);
        sem_post(&sem_empty);   /* signal a slot is free  */
    }
    return NULL;
}

/* ── main ───────────────────────────────────────── */
int main(void) {
    sem_init(&sem_empty, 0, BUFFER_SIZE);
    sem_init(&sem_full,  0, 0);
    sem_init(&mutex,     0, 1);

    pthread_t prod, cons;
    pthread_create(&prod, NULL, producer, NULL);
    pthread_create(&cons, NULL, consumer, NULL);

    pthread_join(prod, NULL);
    pthread_join(cons, NULL);

    sem_destroy(&sem_empty);
    sem_destroy(&sem_full);
    sem_destroy(&mutex);

    return 0;
}
