# Sahi automation result parser microservice

## Introduction
Sahi automation result parser project contains service to parse Sahi run result and display it in JSON format. This service is a part of SwiftOps project. There are four microservices in this project.
*  getSahiRunSummary
*  getSahiRunResult
*  getSahiFailedReport
*  getSahiFailedSummary

**getSahiRunSummary** parse StartTime, EndTime, TimeTaken, TotalCount, PassedCount, PassedScript, FailedSount and FailedScript of index.xml of Sahi run and display it in JSON format.

**getSahiRunResult** parse the complete content of index.xml of Sahi run and display it in JSON format

**getSahiFailedReport** Parse ScriptName, ScriptType, StartTime, TimeTaken, ReleaseNumber and BuildNumber of index.xml of Sahi run. After getting these data it put it into MongoDB Where db_name is sahi_automation and db_collection is sahi_coll.

**getSahiFailedSummary** parse ScriptName, FailedCount and TotalCount of index.xml of Sahi run and returns data in tabular JSON format. 

## Assumption
*  This microservice for Sahi run report. Which should be saved in XML format.

## Pre-Requisite
*  python 3.6.0 or above version.

## Installation

### Checkout Repository
Checkout project code from git.
```
$git clone https://github.com/swiftops/sahi-automation-result-parser.git
```
### Configuration
*  On MongoDB client need to create a database with name **sahi_automation** and collection with name **sahi_coll**

*  Specify sahi_result_url, iSIndexDotXmlFromHttpURL, runtime, browserType, nodeCount, module and MpngoDB Parameters in sahiConfig.ini.
```python
    [mongo_Params]
    mongo_ip = 10.0.2.10
    mongo_port = 27017
    db_name = sahi_automation
    db_collection = sahi_coll
```    
*  Install python module dependanceies

```shell
   pip install -r requirements.txt
``` 

### Run services
In order to run this script, need to run below script from command line in admin mode
To run microservice we need to go to root directory from command line. For Example -
We have project in D drive then we should run as below.

```
   D:\devops-opensource\sahi-automation-result-parser>python service.py
``` 

## How to use
There is two way to get the Sahi Index.xml
1.  By setting the HTTP path for sahi_result_url
2.  By setting the directory path for sahi_result_url

If you choose  HTTP path then need to set iSIndexDotXmlFromHttpURL=Yes otherwise NO.
For example, We have index.xml in the project directory for the sample run. To run this we need to set two parameters from sahiConfig.ini.

iSIndexDotXmlFromHttpURL=**No**

sahi_result_url=**D:\devops-opensource\sahi-automation-result-parser\index.xml**

and run below URL with the proper release and build to get the parsed result.

[For getSahiRunSummary.]: http://localhost:7777/getSahiRunSummary/#release#/#build#

[For getSahiRunResult]: http://localhost:7777/getSahiRunResult/#release#/#build#

[For getSahiFailedReport]: http://localhost:7777/getSahiFailedReport/#release#/#build#

[For getSahiFailedSummary]: http://localhost:7777/getSahiFailedSummary/#release#/#build#

where
*  release is like. _3.2.0, 4.0.0_ ect.
*  build is like. _1,2,3,4,5,... ,55_ ect.
