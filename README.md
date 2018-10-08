# Sahi automation result parser microservice

### Indoduction
There are four microservice which used to get Sahi run report data based on release and build. 
These are-
* getSahiRunSummary
* getSahiRunResult
* getSahiFailedReport
* getSahiFailedSummary

##### What does getSahiRunSummary do?
It returns the summary of particular Sahi run in dictionary format. Which includes 8 parameters from index.xml of that run. These are  STARTTIME , ENDTIME, TIMETAKEN, TOTALCOUNT, PASSEDCOUNT, PASSEDSCRIPT, FAILEDCOUNT, FAILEDSCRIPT
If scheduling a run with  4 reruns then we get above data five times.

##### What does getSahiRunResult do?
It returns the complete content of index.xml of Sahi run
If scheduling a run with  4 reruns then we get above data five times.

##### What does getSahiFailedReport do?
It brings information about the failures in the last Sahi run suites which mainly have information about ScriptName, ScriptType, StartTime, TimeTaken, Release Number and Build Number. After retiving these data it saves it to MongoDB for further use

##### What does getSahiFailedSummary do?
It brings information about the failures in the last Sahi run suites which mainly have information about ScriptName, FailedCount and TotalCount. After retiving these data it saves it to MongoDB for further use.

### Assumption

* This microservice for Sahi Automation run. So It is assumed that Sahi Pro has been installed on your system.
* Sahi run report should be saved in XML format.


### Pre-Requisite

* To run above microservice we need to installed the python 3.6.0 or above. After that need to set path in environment variable.


### Installation
##### Checkout Repository
Checkout project code from git.
```
$git clone https://github.com/swiftops/sahi-automation-result-parser.git
```
##### Configuration
You have to specify your database ip,port,db name, collection name, sahi_result_url,runtime, browserType, nodeCount and module in sahiConfig.ini file which is present at root directory.

##### Run services
In order to run this script, need to run below script from command line in admin mode
To run microservice we need to go to root directory from command line. For Example -
We have project in D drive then we should run as below.

```
   D:\GitHub\sahi-automation-result-parser>python services.py
``` 

### How to use
In order to call above microservices. we just need to hit below URL  from the browser

```
For getSahiRunSummary
    http://localhost:7777/getSahiRunSummary/<version>
For getSahiRunResult
    http://localhost:7777/getSahiRunResult/<release>/<build>
For getSahiFailedReport
    http://localhost:7777/getSahiFailedReport/<release>/<build>
For getSahiFailedSummary
    http://localhost:7777/getSahiFailedSummary/<release>/<build>
```
where
* version is like. _3.2.0_26, 4.0.0_17_ ect.
* release is like. _3.2.0, 4.0.0_ ect.
* build is like. _1,2,3,4,5,... ,55_ ect.
