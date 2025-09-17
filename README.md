# Software utils for the Bachelor's Degree in Satellite's Engineering CDIO-1 subject

## Session 2: Programming basics

The following sections explain how to compile and run the provided code examples.

Execution times for the programs can be timed as follows:
```
time ./<outputfile>     # for compiled languages like C
time python <filename.py>  # for interpreted languages like Python
```
Which will output something like:
```
real    0m0.123s
user    0m0.120s
sys     0m0.003s
```
Where `real` is the total elapsed time, `user` is the time spent in user mode, and `sys` is the time spent in kernel 
mode.


### C code

Compile it with:
```  
gcc <filename.c> -o <outputfile>    # for linux
clang <filename.c> -o <outputfile>  # for macOS
```

Run it:
```
./<outputfile>
```

### Python code

Run it with:
```
python <filename.py>
```

