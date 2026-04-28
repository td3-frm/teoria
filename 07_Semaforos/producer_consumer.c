/*
 * producer_consumer.c
 *
 * Real-world scenario: HTTP server log pipeline
 *
 * PRODUCERS  →  simulate incoming HTTP requests and push log entries
 *               into a shared circular buffer.
 *
 * CONSUMERS  →  pull log entries, parse them, and tally statistics
 *               (status code counts, total bytes served).
 *
 * Synchronisation:
 *   sem_empty  – counts free slots  (initialised to BUFFER_SIZE)
 *   sem_full   – counts used slots  (initialised to 0)
 *   mutex      – binary semaphore protecting the buffer pointers
 *
 * Build:
 *   gcc -Wall -Wextra -O2 -o producer_consumer producer_consumer.c -lpthread
 *
 * Run:
 *   ./producer_consumer
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>
#include <stdatomic.h>

/* ── tunables ─────────────────────────────────────────────────────────── */
#define BUFFER_SIZE     8       /* circular buffer capacity (slots)        */
#define NUM_PRODUCERS   3       /* threads simulating HTTP workers          */
#define NUM_CONSUMERS   2       /* threads processing log entries           */
#define LOGS_PER_PROD   10      /* how many log entries each producer emits */

/* ── log entry ────────────────────────────────────────────────────────── */
typedef struct {
    int    status_code;         /* HTTP status: 200, 301, 404, 500, …      */
    int    bytes_sent;
    char   method[8];           /* GET / POST / PUT / DELETE               */
    char   path[64];
} LogEntry;

/* ── shared circular buffer ───────────────────────────────────────────── */
static LogEntry buffer[BUFFER_SIZE];
static int      head = 0;       /* next write position                     */
static int      tail = 0;       /* next read  position                     */

/* ── POSIX semaphores ─────────────────────────────────────────────────── */
static sem_t sem_empty;         /* free slots available to write           */
static sem_t sem_full;          /* filled slots available to read          */
static sem_t mutex;             /* mutual exclusion for head/tail pointers */

/* ── statistics (updated only by consumers) ──────────────────────────── */
static atomic_int  stat_200 = 0;
static atomic_int  stat_301 = 0;
static atomic_int  stat_404 = 0;
static atomic_int  stat_500 = 0;
static atomic_long stat_bytes = 0;

/* ── helpers ──────────────────────────────────────────────────────────── */
static const int STATUS_CODES[] = {200, 200, 200, 301, 404, 404, 500};
static const int STATUS_COUNT   = 7;

static const char *METHODS[] = {"GET", "GET", "GET", "POST", "PUT", "DELETE"};
static const int   METHOD_COUNT = 6;

static const char *PATHS[] = {
    "/", "/api/users", "/api/orders", "/static/logo.png",
    "/api/products", "/admin", "/health", "/api/auth"
};
static const int PATH_COUNT = 8;

static void random_log(LogEntry *e, unsigned int *seed) {
    e->status_code = STATUS_CODES[rand_r(seed) % STATUS_COUNT];
    e->bytes_sent  = 64 + rand_r(seed) % 4032;   /* 64 B – 4 KB          */
    strncpy(e->method, METHODS[rand_r(seed) % METHOD_COUNT], sizeof(e->method) - 1);
    strncpy(e->path,   PATHS  [rand_r(seed) % PATH_COUNT  ], sizeof(e->path)   - 1);
}

static const char *status_label(int code) {
    switch (code) {
        case 200: return "OK";
        case 301: return "Moved";
        case 404: return "Not Found";
        case 500: return "Server Error";
        default:  return "?";
    }
}

/* ── producer thread ──────────────────────────────────────────────────── */
static void *producer(void *arg) {
    int id = *(int *)arg;
    unsigned int seed = (unsigned int)(id * 1000 + time(NULL));

    for (int i = 0; i < LOGS_PER_PROD; i++) {

        LogEntry entry;
        random_log(&entry, &seed);

        /* simulate variable request processing time */
        usleep((50 + rand_r(&seed) % 100) * 1000);   /* 50–150 ms */

        /* ① wait for a free slot */
        sem_wait(&sem_empty);

        /* ② acquire mutual exclusion */
        sem_wait(&mutex);

        buffer[head] = entry;
        head = (head + 1) % BUFFER_SIZE;

        printf("[P%d] %-6s %-22s  %d %s  (%d B)\n",
               id, entry.method, entry.path,
               entry.status_code, status_label(entry.status_code),
               entry.bytes_sent);

        /* ③ release lock, signal a filled slot */
        sem_post(&mutex);
        sem_post(&sem_full);
    }

    printf("[P%d] done – %d entries produced.\n", id, LOGS_PER_PROD);
    return NULL;
}

/* ── consumer thread ──────────────────────────────────────────────────── */
static void *consumer(void *arg) {
    int id      = *(int *)arg;
    int total   = NUM_PRODUCERS * LOGS_PER_PROD;
    /* Each consumer handles its fair share; remainder goes to consumer 0. */
    int my_share = total / NUM_CONSUMERS
                 + (id == 0 ? total % NUM_CONSUMERS : 0);

    for (int i = 0; i < my_share; i++) {

        /* ① wait for a filled slot */
        sem_wait(&sem_full);

        /* ② acquire mutual exclusion */
        sem_wait(&mutex);

        LogEntry entry = buffer[tail];
        tail = (tail + 1) % BUFFER_SIZE;

        /* ③ release lock, signal a free slot */
        sem_post(&mutex);
        sem_post(&sem_empty);

        /* process the entry (outside the critical section) */
        switch (entry.status_code) {
            case 200: atomic_fetch_add(&stat_200, 1); break;
            case 301: atomic_fetch_add(&stat_301, 1); break;
            case 404: atomic_fetch_add(&stat_404, 1); break;
            case 500: atomic_fetch_add(&stat_500, 1); break;
        }
        atomic_fetch_add(&stat_bytes, entry.bytes_sent);

        printf("    [C%d] processed  %-6s %-22s → %d\n",
               id, entry.method, entry.path, entry.status_code);

        usleep((30 + rand() % 70) * 1000);   /* 30–100 ms analysis time   */
    }

    printf("    [C%d] done – %d entries consumed.\n", id, my_share);
    return NULL;
}

/* ── main ─────────────────────────────────────────────────────────────── */
int main(void) {
    printf("=== HTTP Log Pipeline  (producers=%d  consumers=%d  buffer=%d) ===\n\n",
           NUM_PRODUCERS, NUM_CONSUMERS, BUFFER_SIZE);

    /* initialise semaphores */
    sem_init(&sem_empty, 0, BUFFER_SIZE);   /* all slots free at start     */
    sem_init(&sem_full,  0, 0);             /* no data ready at start      */
    sem_init(&mutex,     0, 1);             /* binary semaphore (unlocked) */

    pthread_t prod_threads[NUM_PRODUCERS];
    pthread_t cons_threads[NUM_CONSUMERS];
    int       prod_ids    [NUM_PRODUCERS];
    int       cons_ids    [NUM_CONSUMERS];

    /* spawn consumers first so they are ready before any data arrives */
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        cons_ids[i] = i;
        pthread_create(&cons_threads[i], NULL, consumer, &cons_ids[i]);
    }

    /* spawn producers */
    for (int i = 0; i < NUM_PRODUCERS; i++) {
        prod_ids[i] = i;
        pthread_create(&prod_threads[i], NULL, producer, &prod_ids[i]);
    }

    /* wait for all threads */
    for (int i = 0; i < NUM_PRODUCERS; i++) pthread_join(prod_threads[i], NULL);
    for (int i = 0; i < NUM_CONSUMERS; i++) pthread_join(cons_threads[i], NULL);

    /* destroy semaphores */
    sem_destroy(&sem_empty);
    sem_destroy(&sem_full);
    sem_destroy(&mutex);

    /* print final report */
    int total = NUM_PRODUCERS * LOGS_PER_PROD;
    printf("\n=== Summary (%d log entries) ===\n", total);
    printf("  200 OK           : %4d  (%5.1f%%)\n", stat_200, stat_200 * 100.0 / total);
    printf("  301 Moved        : %4d  (%5.1f%%)\n", stat_301, stat_301 * 100.0 / total);
    printf("  404 Not Found    : %4d  (%5.1f%%)\n", stat_404, stat_404 * 100.0 / total);
    printf("  500 Server Error : %4d  (%5.1f%%)\n", stat_500, stat_500 * 100.0 / total);
    printf("  Total bytes      : %ld B  (~%.1f KB avg)\n",
           stat_bytes, (double)stat_bytes / total / 1024.0);

    return 0;
}
