# CS 425 MP1 - Distributed Log Querier

This project implements remote log querier on multiple machines from any one machine and unit testing. This log querier system can be used for debugging distributed systems.

## Usage
First clone this project onto each server intended to use.
### Server Deployment
Start the server before query. To do this, log onto the server and run the file [*worker.py*](worker.py):
```
python worker.py
```
Or, start all 10 servers together using [*GitScript.py*](misc/GitScript.py) in [*misc*](misc):

``` 
python GitScript.py 
```

### Remote Query
Log onto any machine, run [*starter.py*](starter.py) with the grep command:
```
python starter.py <grep command>
```
If file names to be queried are specified by regular expression, then surround the regular expression with quotation. For example:
```
python starter.py grep -n 'abc' '*.log'
```

The log messages with line counts of each remote machine at the end will be printed.


The design is single thread, due to the small size of query log file. The code is easy to be changed to multi-thread,
since sending request to each server is wrapped in a function


