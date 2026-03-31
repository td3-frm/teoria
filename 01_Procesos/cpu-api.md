
## Process API


### 5.1 The fork() System Call

**Key Concepts**

- The `fork()` system call and its purpose
- Parent and child processes
- Process identifiers (PID)
- Non-determinism in process execution
- Return values of `fork()`

---

**Summary**

**5.1 The fork() System Call**

This section introduces `fork()`, the primary UNIX system call for creating new processes, explaining how it works, what it produces, and why its behavior can be surprising.

- **The `fork()` system call**: `fork()` is provided by the OS to create a new process. It is described as one of the strangest routines a programmer will ever call, because the newly created process does not start from `main()` — instead, it appears as if it too had just called `fork()` itself.

- **Parent and child processes**: When `fork()` is called, the OS creates an almost exact copy of the calling process. The original is called the **parent** and the new one is called the **child**. Both continue executing from the point right after the `fork()` call.

- **Process identifiers (PID)**: Every process in a UNIX system has a unique numeric identifier called a **PID** (Process ID). The `getpid()` call retrieves it. PIDs are used to reference and manage processes (e.g., stopping them).

- **Return values of `fork()`**: The parent and child are distinguished by what `fork()` returns. The **parent** receives the PID of the newly created child; the **child** receives a return value of **zero**. A negative return value signals that the fork failed.

- **Non-determinism in process execution**: After `fork()`, both processes are ready to run, but the CPU scheduler decides which one runs first. This means the order of output between parent and child is **not guaranteed** — it is non-deterministic and can vary between runs.

---

> 📷 [*C source code of p1.c demonstrating a basic fork() call with output from parent and child processes*](images/figure-5-1)


### 5.2 The wait() System Call

**Key Concepts**

- The `wait()` system call and its purpose
- Deterministic ordering of parent and child execution
- The `waitpid()` system call (brief mention)

---

**Summary**

**5.2 The wait() System Call**

This section introduces the `wait()` system call, explaining how a parent process can use it to pause its own execution until a child process finishes, and how this eliminates the non-determinism seen with `fork()` alone.

- **The `wait()` system call**: `wait()` allows a parent process to deliberately delay its own execution until one of its child processes has finished running. Once the child exits, `wait()` returns to the parent, allowing it to continue. This is useful whenever the parent depends on the child completing its work first.

- **Deterministic ordering of parent and child execution**: By adding `wait()`, the output order becomes **predictable**. If the child runs first, it completes normally. If the parent runs first, it immediately calls `wait()` and blocks until the child finishes — guaranteeing the child always prints its output before the parent.

- **The `waitpid()` system call**: The section briefly mentions `waitpid()` as a more complete sibling of `wait()`, offering additional control over which child process to wait for. Further details are left for the reader to explore via man pages.

---

> 📷 [*C source code of p2.c demonstrating fork() used together with wait(), ensuring deterministic child-before-parent output ordering*](images/figure-5-2)

### 5.3 The exec() System Call

**Key Concepts**

- The `exec()` system call and its purpose
- How `exec()` transforms a running process
- The relationship between `fork()` and `exec()`
- Variants of `exec()` on Linux

---

**Summary**

**5.3 The exec() System Call**

This section introduces `exec()`, the third key process API call in UNIX, explaining how it allows a process to run a completely different program rather than continuing as a copy of its parent.

- **The `exec()` system call and its purpose**: `exec()` is used when a process wants to run a **different program** entirely, not just a copy of itself. In the example shown, the child process calls `execvp()` to run the `wc` (word count) program on a source file, producing a count of lines, words, and bytes.

- **How `exec()` transforms a running process**: When `exec()` is called, it loads the code and static data of the specified executable and **overwrites** the current process's code segment with it. The heap, stack, and memory space are re-initialized, and the OS then runs the new program. Critically, `exec()` does **not** create a new process — it transforms the existing one. A successful call to `exec()` never returns.

- **The relationship between `fork()` and `exec()`**: The two calls complement each other. `fork()` creates a copy of the current process, and `exec()` replaces that copy with a new program. Together they form a powerful and flexible mechanism for process creation and program execution in UNIX systems.

- **Variants of `exec()` on Linux**: Linux provides six variants of `exec()`: `execl()`, `execlp()`, `execle()`, `execv()`, `execvp()`, and `execvpe()`. The section directs readers to the man pages for details on each variant.

---

> 📷 [*C source code of p3.c demonstrating fork() combined with wait() and execvp() to run the wc program from within a child process*](images/figure-5-3)


### 5.4 Why? Motivating The API

**Key Concepts**

- The motivation behind separating `fork()` and `exec()`
- How the UNIX shell works internally
- Output redirection using file descriptors
- UNIX pipes and the `pipe()` system call

---

**Summary**

**5.4 Why? Motivating The API**

This section explains the reasoning behind the seemingly unusual design of the UNIX process API, showing how the separation of `fork()` and `exec()` enables powerful shell features like output redirection and pipes.

- **The motivation behind separating `fork()` and `exec()`**: The gap between calling `fork()` and calling `exec()` gives the shell a window to **modify the environment** of the about-to-be-run program. This separation is what makes it possible to build powerful features without changing anything about the programs being run themselves.

- **How the UNIX shell works internally**: The shell is simply a user program that prints a prompt, reads a command, calls `fork()` to create a child process, calls `exec()` to run the requested program in that child, and then calls `wait()` until the command completes. Once `wait()` returns, the shell prints the prompt again and is ready for the next command.

- **Output redirection using file descriptors**: Between `fork()` and `exec()`, the child process can close its standard output and open a file in its place. Because UNIX looks for free file descriptors starting at zero, the file takes the place of standard output, and all subsequent output from the program is transparently written to the file instead of the screen. Open file descriptors are preserved across an `exec()` call, enabling this behavior.

- **UNIX pipes and the `pipe()` system call**: Pipes work similarly to redirection, but connect two processes together. The output of one process is written to an in-kernel queue (the pipe), and the input of the next process reads from that same pipe. This allows long chains of commands to be strung together, such as `grep -o foo file | wc -l`.

---


> 📷 [*C source code of p4.c demonstrating output redirection by closing STDOUT and opening a file before calling execvp() in the child process*](images/figure-5-4)


### 5.5 Process Control And Users

**Key Concepts**

- The `kill()` system call and signals
- Common signal types and keyboard shortcuts
- The signals subsystem
- The concept of a user and process ownership
- The superuser (root)

---

**Summary**

**5.5 Process Control And Users**

This section goes beyond `fork()`, `exec()`, and `wait()` to cover additional mechanisms for controlling processes in UNIX, including signals and the user-based security model that governs who can control which processes.

- **The `kill()` system call and signals**: The `kill()` system call is used to send **signals** to a process, instructing it to pause, terminate, or respond to other directives. Signals provide a way for external events to be delivered to and handled by running processes.

- **Common signal types and keyboard shortcuts**: UNIX shells map certain keyboard combinations to specific signals for convenience. Pressing **control-c** sends a `SIGINT` (interrupt) signal, which normally terminates the process. Pressing **control-z** sends a `SIGTSTP` (stop) signal, which pauses the process mid-execution and allows it to be resumed later, for example with the `fg` command.

- **The signals subsystem**: The signals subsystem provides a rich infrastructure for delivering events to processes. A process can use the `signal()` system call to register a handler — a specific piece of code to run when a particular signal arrives — allowing it to respond gracefully rather than simply terminating.

- **The concept of a user and process ownership**: UNIX systems support multiple simultaneous users, each of whom logs in with credentials and can launch and control their own processes. To protect usability and security, users can generally **only send signals to their own processes**, preventing one user from arbitrarily disrupting another's work.

- **The superuser (root)**: A special user known as the **superuser** (or root) exists to administer the system. Root can send signals to any process, run privileged commands like `shutdown`, and exercise powers unavailable to regular users. Because of the risks involved, it is recommended to operate as a regular user whenever possible and assume root access only when strictly necessary.



### 5.6 Useful Tools

**Key Concepts**

- The `ps` command for viewing running processes
- The `top` command for monitoring resource usage
- The `kill` and `killall` commands
- CPU meter tools

---

**Summary**

**5.6 Useful Tools**

This section provides a brief overview of practical command-line and graphical tools that help users observe and manage processes running on a UNIX system.

- **The `ps` command for viewing running processes**: The `ps` command allows a user to see which processes are currently running on the system. It supports various flags that control the detail and format of its output, and readers are directed to its man pages to learn about the most useful options.

- **The `top` command for monitoring resource usage**: The `top` command displays a live, updating view of running processes along with how much CPU and other system resources each one is consuming. It is particularly useful for quickly identifying which processes are placing the heaviest load on the system.

- **The `kill` and `killall` commands**: The `kill` command can be used from the command line to send arbitrary signals to specific processes. The `killall` command offers a slightly more user-friendly alternative. Both must be used carefully, as accidentally sending a signal to a critical process such as a window manager can make the system very difficult to use.

- **CPU meter tools**: Beyond command-line tools, graphical CPU meters provide a quick at-a-glance view of system load. The section mentions **MenuMeters** as an example of such a tool running on macOS, reflecting the general principle that having more information about system activity is always beneficial.

## Homework (Simulation)

This simulation homework focuses on `fork.py`, a simple process creation simulator that shows how processes are related in a single "familial" tree. Read the relevant README for details about how to run the simulator.

### Questions

1. Run `./fork.py -s 10` and see which actions are taken. Can you predict what the process tree looks like at each step? Use the `-c` flag to check your answers. Try some different random seeds (`-s`) or add more actions (`-a`) to get the hang of it.

2. One control the simulator gives you is the fork percentage, controlled by the `-f` flag. The higher it is, the more likely the next action is a fork; the lower it is, the more likely the action is an exit. Run the simulator with a large number of actions (e.g., `-a 100`) and vary the fork percentage from 0.1 to 0.9. What do you think the resulting final process trees will look like as the percentage changes? Check your answer with `-c`.

3. Now, switch the output by using the `-t` flag (e.g., run `./fork.py -t`). Given a set of process trees, can you tell which actions were taken?

4. One interesting thing to note is what happens when a child exits; what happens to its children in the process tree? To study this, let's create a specific example: `./fork.py -A a+b,b+c,c+d,c+e,c-`. This example has process `a` create `b`, which in turn creates `c`, which then creates `d` and `e`. However, then, `c` exits. What do you think the process tree should look like after the exit? What if you use the `-R` flag? Learn more about what happens to orphaned processes on your own to add more context.

5. One last flag to explore is the `-F` flag, which skips intermediate steps and only asks to fill in the final process tree. Run `./fork.py -F` and see if you can write down the final tree by looking at the series of actions generated. Use different random seeds to try this a few times.

6. Finally, use both `-t` and `-F` together. This shows the final process tree, but then asks you to fill in the actions that took place. By looking at the tree, can you determine the exact actions that took place? In which cases can you tell? In which can't you tell? Try some different random seeds to delve into this question.

---

## Homework (Code)

In this homework, you are to gain some familiarity with the process management APIs about which you just read. Don't worry – it's even more fun than it sounds! You'll in general be much better off if you find as much time as you can to write some code, so why not start now?

### Questions

1. Write a program that calls `fork()`. Before calling `fork()`, have the main process access a variable (e.g., `x`) and set its value to something (e.g., 100). What value is the variable in the child process? What happens to the variable when both the child and parent change the value of `x`?

2. Write a program that opens a file (with the `open()` system call) and then calls `fork()` to create a new process. Can both the child and parent access the file descriptor returned by `open()`? What happens when they are writing to the file concurrently, i.e., at the same time?

3. Write another program using `fork()`. The child process should print `"hello"`; the parent process should print `"goodbye"`. You should try to ensure that the child process always prints first; can you do this without calling `wait()` in the parent?

4. Write a program that calls `fork()` and then calls some form of `exec()` to run the program `/bin/ls`. See if you can try all of the variants of `exec()`, including (on Linux) `execl()`, `execle()`, `execlp()`, `execv()`, `execvp()`, and `execvpe()`. Why do you think there are so many variants of the same basic call?

5. Now write a program that uses `wait()` to wait for the child process to finish in the parent. What does `wait()` return? What happens if you use `wait()` in the child?

6. Write a slight modification of the previous program, this time using `waitpid()` instead of `wait()`. When would `waitpid()` be useful?

7. Write a program that creates a child process, and then in the child closes standard output (`STDOUT_FILENO`). What happens if the child calls `printf()` to print some output after closing the descriptor?

8. Write a program that creates two children, and connects the standard output of one to the standard input of the other, using the `pipe()` system call.


## References

- Arpaci-Dusseau, R. & Arpaci-Dusseau, A. (2023). *Operating Systems: Three Easy Pieces* — Chapter 5: Process API. University of Wisconsin-Madison. Available at: [https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-api.pdf)




