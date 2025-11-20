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

## Session 19: acquisition forecasting

Parse acquisition plans and check when a given area will be captured by a satellite for a time range, with data from 
https://sentinels.copernicus.eu/copernicus/sentinel-2/acquisition-plans
``` 
(_env) % python -m acquisition_forecaster.plan_parser --project eetac_27_11_25
               capture_start             capture_end                                            polygon satellite acquisition_type
1831 2025-11-27 10:44:26.245 2025-11-27 11:00:47.621  POLYGON ((12.03657 60.75446, 9.48874 61.16696,...       S2C     NOBS NOMINAL
```

Run historical analysis to acquire past capture dates
``` 
(_env) % python -m acquisition_forecaster.historical_analysis --project eetac_2025 --action acquire
``` 

Plot historical analysis results
``` 
(_env) % python -m acquisition_forecaster.historical_analysis --project eetac_2025 --action plot
```