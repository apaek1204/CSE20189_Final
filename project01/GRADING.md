Project 01 - Grading
====================

**Score**: 16.25 / 20

Deductions
----------

* Thor

    - 0.25  Doesn't handle no arguments gracefully
    - 1.0   Not fully concurrent (fork all children, and then wait)

* Spidey

    - 0.25  Hardcoded headers
    - 0.25  Improper HTTP error status
    - 0.5   Missing error checking of system calls (fork)
    - 0.5   You have child and part backwards (pid == 0 is child)

* Report

    - 0.5   Report does not build
    - 0.5   Missing plots (throughput)

Comments
--------

* Remove dead code
