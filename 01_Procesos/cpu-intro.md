### 4.1 The Abstraction: A Process

**Key Concepts**

- Definition of a process
- Machine state
- Address space (memory)
- Registers
- Special registers: Program Counter, Stack Pointer, Frame Pointer
- I/O information

---

**Summary**

**4.1 The Abstraction: A Process**

This section defines what a process is from an operating system perspective and breaks down the components that make up its *machine state* — everything the OS needs to track about a running program at any given moment.

- **Definition of a process:** A process is simply a running program. At any instant, it can be described by taking an inventory of all the system components it accesses or affects during execution.

- **Machine state:** Machine state refers to everything a program can read or update while it is running. Understanding machine state is essential to understanding what a process actually *is* at the hardware level.

- **Address space (memory):** Memory is a core component of a process's machine state. A program's instructions and the data it reads and writes all reside in memory. The region of memory a process can access is called its **address space**.

- **Registers:** Registers are another key part of machine state. Many instructions explicitly read from or write to registers, making them critical to the moment-to-moment execution of a process.

- **Special registers — PC, Stack Pointer, Frame Pointer:** The **Program Counter (PC)**, also called the *Instruction Pointer (IP)*, tracks which instruction will execute next. The **stack pointer** and **frame pointer** work together to manage the call stack, which holds function parameters, local variables, and return addresses.

- **I/O information:** Processes also interact with persistent storage. The OS tracks I/O-related state, such as the list of files a process currently has open, as part of the overall process description.

---


### 4.2 Process API

**Key Concepts**

- Create
- Destroy
- Wait
- Miscellaneous Control
- Status

---

**Summary**

**4.2 Process API**

This section provides a high-level overview of the essential operations that any operating system must offer for managing processes. These APIs represent the fundamental interface between the OS and the programs that run on it.

- **Create:** The OS must provide a way to create new processes. This happens whenever a user runs a command in a shell or launches an application — the OS is invoked to spin up a new process to execute the requested program.

- **Destroy:** Just as processes can be created, they can also be forcefully terminated. While many processes end on their own when finished, the OS must also provide a mechanism to kill runaway or unresponsive processes at the user's request.

- **Wait:** The OS provides an interface to wait for a process to finish running. This is useful when one process depends on the completion of another before it can safely proceed.

- **Miscellaneous Control:** Beyond creating and destroying processes, operating systems typically offer additional controls. A common example is the ability to **suspend** a process (temporarily pause it) and later **resume** it (continue its execution).

- **Status:** The OS exposes interfaces to query information about a process's current condition — for example, how long it has been running or what state it is currently in.


---


### 4.3 Process Creation: A Little More Detail

**Key Concepts**

- Loading code and static data into memory
- Eager vs. lazy loading
- Stack allocation and initialization
- Heap allocation
- I/O setup
- Transferring control to the process

---

**Summary**

**4.3 Process Creation: A Little More Detail**

This section walks through the step-by-step process of how an operating system transforms a program sitting on disk into a living, running process in memory. Each step prepares the environment the program needs before it can begin executing.

- **Loading code and static data into memory:** The first thing the OS does is read the program's instructions and any static data (such as initialized variables) from disk and place them into the process's address space in memory. Programs are stored on disk in an executable format and must be brought into memory before they can run.

- **Eager vs. lazy loading:** Early operating systems loaded the entire program into memory at once — this is called **eager loading**. Modern OSes instead use **lazy loading**, bringing in only the portions of code or data actually needed at a given moment during execution. Full understanding of lazy loading requires knowledge of *paging* and *swapping*, covered in later chapters.

- **Stack allocation and initialization:** Once the code is loaded, the OS allocates memory for the program's **run-time stack**. In C programs, the stack holds local variables, function parameters, and return addresses. The OS also initializes the stack with arguments to the `main()` function — specifically `argc` and the `argv` array.

- **Heap allocation:** The OS may also allocate initial memory for the program's **heap**, which is used for dynamically allocated data requested at runtime via `malloc()` and released via `free()`. The heap starts small and grows as the program requests more memory during execution.

- **I/O setup:** Before running the process, the OS performs some default I/O initialization. In UNIX systems, for example, every process is given three open **file descriptors** by default — for standard input, standard output, and standard error — allowing the program to read from the terminal and write to the screen immediately.

- **Transferring control to the process:** With memory loaded, the stack and heap set up, and I/O initialized, the OS performs its final step: jumping to the program's entry point, the `main()` function. At this moment, the OS hands control of the CPU over to the newly created process, and execution begins.

---

Here are the 5 image placeholders updated with the correct paths:


> 📷 [*Figure 4.1: Diagram illustrating the loading process, showing how a program's code and static data are read from disk and placed into the address space of a process in memory, alongside the CPU and the process's stack and heap.*](images/figure-4-1.png)


---


### 4.4 Process States

**Key Concepts**

- Running state
- Ready state
- Blocked state
- State transitions
- Tracing process states: CPU only example
- Tracing process states: CPU and I/O example

---

**Summary**

**4.4 Process States**

This section introduces the different states a process can be in at any given moment during its lifetime, and explains how and why a process moves between those states. Understanding process states is fundamental to understanding how an OS manages multiple running programs efficiently.

- **Running state:** A process is in the **running** state when it is actively executing instructions on a processor. At any given moment, only one process per CPU core can be in this state.

- **Ready state:** A process in the **ready** state is fully prepared to run but has not been selected by the OS to execute at that moment. It is waiting for its turn to be scheduled onto the CPU.

- **Blocked state:** A process enters the **blocked** state when it performs an operation that prevents it from running until some external event occurs. A common example is initiating a disk I/O request — the process must wait for the I/O to complete before it can continue, freeing the CPU to run other processes in the meantime.

- **State transitions:** Processes move between states based on OS decisions and external events. A process moves from **ready → running** when the OS schedules it, and from **running → ready** when it is descheduled. It moves from **running → blocked** when it initiates an I/O operation, and back from **blocked → ready** once that I/O completes.

- **Tracing process states: CPU only example:** When two processes use only the CPU with no I/O, they take turns running one at a time. The first process runs to completion, then the second runs to completion — straightforward sequential scheduling with 100% CPU utilization.

- **Tracing process states: CPU and I/O example:** When a process initiates an I/O operation, it becomes blocked and the OS switches to running another process. This overlap of I/O waiting and CPU execution by another process improves overall **resource utilization**, keeping the CPU busy rather than idle while waiting for I/O to complete.

---

> 📷 [*Figure 4.2: State transition diagram showing the three process states — Running, Ready, and Blocked — with labeled arrows indicating transitions: Scheduled, Descheduled, I/O initiated, and I/O done.*](images/figure-4-2.png)

> 📷 [*Figure 4.3: Table tracing the states of two CPU-only processes over time, showing Process0 running to completion before Process1 begins.*](images/figure-4-3.png)

> 📷 [*Figure 4.4: Table tracing the states of two processes over time where Process0 initiates an I/O, becomes blocked, and Process1 runs on the CPU meanwhile, demonstrating efficient resource utilization.*](images/figure-4-4.png)

---

### 4.5 Data Structures

**Key Concepts**

- The process list
- Process Control Block (PCB)
- Register context
- Process states in xv6
- The zombie state

---

**Summary**

**4.5 Data Structures**

This section explains how the operating system keeps track of all the processes it manages by using key data structures. It grounds these concepts in a real, minimalist OS called **xv6** to illustrate what information the OS actually needs to store about each process.

- **The process list:** The OS maintains a **process list** (also called a *task list*) to track all processes currently in the system — those that are ready to run, currently running, or blocked. This is one of the most fundamental data structures in any OS capable of running multiple programs simultaneously.

- **Process Control Block (PCB):** Each entry in the process list is represented by a **Process Control Block (PCB)** — a data structure that holds all the information the OS needs to know about a specific process. In xv6, this is implemented as a C `struct proc`, containing fields such as memory location, size, process ID, parent process, open files, and current directory.

- **Register context:** A critical part of the PCB is the **register context** — a saved snapshot of the process's CPU registers at the moment it was stopped. When the OS later resumes the process, it restores these saved register values back into the physical CPU registers, allowing execution to continue exactly where it left off. This mechanism is the foundation of the **context switch**.

- **Process states in xv6:** Beyond the three basic states (running, ready, blocked), xv6 tracks additional states for a more complete lifecycle: **UNUSED**, **EMBRYO** (being created), **SLEEPING** (blocked), **RUNNABLE** (ready), **RUNNING**, and **ZOMBIE**. These reflect the full range of situations a process can be in from creation to cleanup.

- **The zombie state:** When a process finishes executing but has not yet been cleaned up by the OS, it enters the **zombie state**. It remains in this state until its parent process calls `wait()`, reads the child's return code, and signals to the OS that it can safely remove all data structures associated with the now-finished process.

---

> 📷 [*Figure 4.5: Code listing of the xv6 `proc` structure, showing the fields the OS tracks for each process including register context, process state, process ID, parent, open files, and other metadata.*](images/figure-4-5.png)

---

## Homework (Simulation)

This program, `process-run.py`, allows you to see how process states change as programs run and either use the CPU (e.g., perform an add instruction) or do I/O (e.g., send a request to a disk and wait for it to complete). See the README for details.

### Questions

1. Run `process-run.py` with the following flags: `-l 5:100,5:100`. What should the CPU utilization be (e.g., the percent of time the CPU is in use?) Why do you know this? Use the `-c` and `-p` flags to see if you were right.

2. Now run with these flags: `./process-run.py -l 4:100,1:0`. These flags specify one process with 4 instructions (all to use the CPU), and one that simply issues an I/O and waits for it to be done. How long does it take to complete both processes? Use `-c` and `-p` to find out if you were right.

3. Switch the order of the processes: `-l 1:0,4:100`. What happens now? Does switching the order matter? Why? (As always, use `-c` and `-p` to see if you were right)

4. We'll now explore some of the other flags. One important flag is `-S`, which determines how the system reacts when a process issues an I/O. With the flag set to `SWITCH_ON_END`, the system will NOT switch to another process while one is doing I/O, instead waiting until the process is completely finished. What happens when you run the following two processes (`-l 1:0,4:100 -c -S SWITCH_ON_END`), one doing I/O and the other doing CPU work?

5. Now, run the same processes, but with the switching behavior set to switch to another process whenever one is WAITING for I/O (`-l 1:0,4:100 -c -S SWITCH_ON_IO`). What happens now? Use `-c` and `-p` to confirm that you are right.

6. One other important behavior is what to do when an I/O completes. With `-I IO_RUN_LATER`, when an I/O completes, the process that issued it is not necessarily run right away; rather, whatever was running at the time keeps running. What happens when you run this combination of processes? (`./process-run.py -l 3:0,5:100,5:100,5:100 -S SWITCH_ON_IO -c -p -I IO_RUN_LATER`) Are system resources being effectively utilized?

7. Now run the same processes, but with `-I IO_RUN_IMMEDIATE` set, which immediately runs the process that issued the I/O. How does this behavior differ? Why might running a process that just completed an I/O again be a good idea?

8. Now run with some randomly generated processes using flags `-s 1 -l 3:50,3:50` or `-s 2 -l 3:50,3:50` or `-s 3 -l 3:50,3:50`. See if you can predict how the trace will turn out. What happens when you use the flag `-I IO_RUN_IMMEDIATE` versus that flag `-I IO_RUN_LATER`? What happens when you use the flag `-S SWITCH_ON_IO` versus `-S SWITCH_ON_END`?


## References

- Arpaci-Dusseau, R. & Arpaci-Dusseau, A. (2023). *Operating Systems: Three Easy Pieces* — Chapter 4: The Abstraction: The Process. University of Wisconsin-Madison. Available at: [https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf)
