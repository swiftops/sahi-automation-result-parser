'''
Created on 27-Mar-2018

@author: jpbharti
'''
import requests
from flask import Flask
import xml.dom.minidom
import configparser
from pymongo import MongoClient
from builtins import int
import json

config = configparser.ConfigParser()
config.read('sahiConfig.ini')


app = Flask(__name__)

mongo_ip = config.get("mongoParams", "mongo_ip")
mongo_port = config.get("mongoParams", "mongo_port")
db_name = config.get("mongoParams", "db_name")
db_collection = config.get("mongoParams", "db_collection")


CLIENT = MongoClient(mongo_ip,int(mongo_port))
MONGO_SAHI_DB = CLIENT[db_name]
MONGO_SAHI_COLLECTION= MONGO_SAHI_DB[db_collection]


#CLIENT = MongoClient("35.174.10.200", 27017)  #the mongo db is on same machine on aws. hence passing localhost.
#MONGO_SAHI_DB = CLIENT.sahi_automation
#MONGO_SAHI_COLLECTION= MONGO_SAHI_DB.sahi_coll

browser = config.get("SAHI", "browserType")
result_url = config.get("SAHI", "sahi_result_url")
runtime = config.get("SAHI", "runtime")
node_count = config.get("SAHI", "nodeCount")
module = config.get("SAHI", "module")

def sahi_run_report_default(version):
    return sahi_run_report(version, None)

def sahi_run_report(version):
    """This will return Sahi run detailed based on
    Module : All,ECR, Sanity, Start ect.
    Version : Combination of relaese version with build. Ex. 3.2.0_25
    Browser : chrome, FF, IE, by default it will take chrome.
    """
    jsondata = {}
    failuredata = {}
    versn=version.split("_");
    i=0
    flag=True
    while i < int(runtime):
        successdata = {}
        i += 1
        source_file_name=str(result_url).replace("#RELEASE_NUMBER#", versn[0]).replace("#BUILD_NUMBER#", versn[1]).replace("#MODULE#", module).replace("#VERSION#", version).replace("#BROWSER#", browser).replace("#COUNTER#", str(i))
        try:
            resp = requests.get(source_file_name)
        except Exception as e:
            failuredata["statuscode"] = 404
            failuredata["errormsg"] = "atlas URL is not working : " + e.__str__()
            return str(buildErrorResponse(failuredata))

        if i==1 and resp.status_code != 200:
            flag=False
            break
        elif resp.status_code != 200:
            break
        destination_file_name='RunSuite'+str(i)+'.xml'
        with open(destination_file_name, 'wb') as f:
            f.write(resp.content)

        doc = xml.dom.minidom.parse(destination_file_name)

        starttime = doc.getElementsByTagName('STARTTIME')
        successdata['STARTTIME']=str(starttime[0].childNodes[0].nodeValue)

        endtime = doc.getElementsByTagName('ENDTIME')
        successdata['ENDTIME']=str(endtime[0].childNodes[0].nodeValue)

        timetaken = doc.getElementsByTagName('TIMETAKEN')
        value=str(timetaken[0].childNodes[0].nodeValue)
        successdata['TIMETAKEN']=str(round(int(value)/60000))

        totalcount = doc.getElementsByTagName('TOTALCOUNT')
        totalscript = str(totalcount[0].childNodes[0].nodeValue)
        successdata['TOTALCOUNT']=totalscript

        scriptname = doc.getElementsByTagName('SCRIPTNAME')
        scriptstatus = doc.getElementsByTagName('SCRIPTSTATUS')

        success = [];
        failed = [];
        for x in range(0,int(totalscript)):
            if str(scriptstatus[x].childNodes[0].nodeValue) == 'SUCCESS':
                success.append(str(scriptname[x].childNodes[0].nodeValue))
            else:
                failed.append(str(scriptname[x].childNodes[0].nodeValue))

        passedcount = doc.getElementsByTagName('PASSEDCOUNT')
        successdata['PASSEDCOUNT']=str(passedcount[0].childNodes[0].nodeValue)

        successdata['PASSEDSCRIPT']=success

        failedcount = doc.getElementsByTagName('FAILEDCOUNT')
        successdata['FAILEDCOUNT']=str(failedcount[0].childNodes[0].nodeValue)

        successdata['FAILEDSCRIPT']=failed

        browsertype = doc.getElementsByTagName('BROWSERTYPE')
        successdata['BROWSERTYPE']=str(browsertype[0].childNodes[0].nodeValue)

        jsondata['RunSuite'+str(i)]= successdata

    if flag==True:
        return str(getSuccessResponse(jsondata))
    else:
        failuredata = {}
        failuredata['statuscode'] = 404
        failuredata['errormsg'] = 'Sahi automation run did not happen on  ' + version
        return str(buildErrorResponse(failuredata))

def sahi_run_result(releaseNo,buildNo):
    jsondata = {}
    failuredata = {}
    i=0
    flag=True
    while i < int(runtime):
        successdata = {}
        suitesummary = {}
        scriptSummaries = {}
        i += 1
        version = releaseNo+"_"+buildNo
        source_file_name=str(result_url).replace("#RELEASE_NUMBER#", releaseNo).replace("#BUILD_NUMBER#", buildNo).replace("#MODULE#", module).replace("#VERSION#", version).replace("#BROWSER#", browser).replace("#COUNTER#", str(i))
        try:
            resp = requests.get(source_file_name)
        except Exception as e:
            failuredata["statuscode"] = 404
            failuredata["errormsg"] = "atlas URL is not working : " + e.__str__()
            return str(buildErrorResponse(failuredata))

        if i==1 and resp.status_code != 200:
            flag=False
            break
        elif resp.status_code != 200:
            break
        destination_file_name='RunSuite'+str(i)+'.xml'
        with open(destination_file_name, 'wb') as f:
            f.write(resp.content)

        doc = xml.dom.minidom.parse(destination_file_name)
        ########################==========suitesummary=======##########################
        ids = doc.getElementsByTagName('ID')
        suitesummary['ID']=str(ids[0].childNodes[0].nodeValue)

        suitereportid = doc.getElementsByTagName('SUITEREPORTID')
        suitesummary['SUITEREPORTID']=str(suitereportid[0].childNodes[0].nodeValue)

        suitename = doc.getElementsByTagName('SUITENAME')
        suitesummary['SUITENAME']=str(suitename[0].childNodes[0].nodeValue)

        suitepath = doc.getElementsByTagName('SUITEPATH')
        suitesummary['SUITEPATH']=str(suitepath[0].childNodes[0].nodeValue)

        starttime = doc.getElementsByTagName('STARTTIME')
        suitesummary['STARTTIME']=str(starttime[0].childNodes[0].nodeValue)

        endtime = doc.getElementsByTagName('ENDTIME')
        suitesummary['ENDTIME']=str(endtime[0].childNodes[0].nodeValue)

        suitestatus = doc.getElementsByTagName('SUITESTATUS')
        suitesummary['SUITESTATUS']=str(suitestatus[0].childNodes[0].nodeValue)

        totalcount = doc.getElementsByTagName('TOTALCOUNT')
        totalscript = str(totalcount[0].childNodes[0].nodeValue)
        suitesummary['TOTALCOUNT']=totalscript

        passedcount = doc.getElementsByTagName('PASSEDCOUNT')
        suitesummary['PASSEDCOUNT']=str(passedcount[0].childNodes[0].nodeValue)

        failedcount = doc.getElementsByTagName('FAILEDCOUNT')
        suitesummary['FAILEDCOUNT']=str(failedcount[0].childNodes[0].nodeValue)

        timetaken = doc.getElementsByTagName('TIMETAKEN')
        value=str(timetaken[0].childNodes[0].nodeValue)
        suitesummary['TIMETAKEN']=value

        browsertype = doc.getElementsByTagName('BROWSERTYPE')
        suitesummary['BROWSERTYPE']=str(browsertype[0].childNodes[0].nodeValue)

        suiteinfo = doc.getElementsByTagName('SUITEINFO')
        suitesummary['SUITEINFO']=str(suiteinfo[0].childNodes[0].nodeValue)

        userdefinedid = doc.getElementsByTagName('USERDEFINEDID')
        suitesummary['USERDEFINEDID']=str(userdefinedid[0].childNodes[0].nodeValue)

        tccount = doc.getElementsByTagName('TCCOUNT')
        suitesummary['TCCOUNT']=str(tccount[0].childNodes[0].nodeValue)

        tcpassed = doc.getElementsByTagName('TCPASSED')
        suitesummary['TCPASSED']=str(tcpassed[0].childNodes[0].nodeValue)

        tcfailed = doc.getElementsByTagName('TCFAILED')
        suitesummary['TCFAILED']=str(tcfailed[0].childNodes[0].nodeValue)

        machinename = doc.getElementsByTagName('MACHINENAME')
        suitesummary['MACHINENAME']=str(machinename[0].childNodes[0].nodeValue)

        parentsuiteid = doc.getElementsByTagName('PARENTSUITEID')
        suitesummary['PARENTSUITEID']=str(parentsuiteid[0].childNodes[0].nodeValue)

        hostname = doc.getElementsByTagName('HOSTNAME')
        port = doc.getElementsByTagName('PORT')
        scriptcount = doc.getElementsByTagName('SCRIPTCOUNT')

        nodedetails = []
        nodes ={}
        for x in range(0,int(node_count)):##for 7 (master+6slave) thread
            node = {}
            node['ID']=str(ids[x+1].childNodes[0].nodeValue)
            node['SUITEREPORTID']=str(suitereportid[x+1].childNodes[0].nodeValue)
            node['HOSTNAME']=str(hostname[x].childNodes[0].nodeValue)
            node['PORT']=str(port[x].childNodes[0].nodeValue)
            node['SCRIPTCOUNT']=str(scriptcount[x].childNodes[0].nodeValue)
            #print(str(node))
            nodedetails.insert(x, node)
        nodes['node']=nodedetails
        suitesummary['nodes']=nodes
        successdata['suiteSummary']=suitesummary

        ########################==========scriptSummaries=======##########################

        scriptreportid = doc.getElementsByTagName('SCRIPTREPORTID')
        scriptname = doc.getElementsByTagName('SCRIPTNAME')
        suitename = doc.getElementsByTagName('SUITENAME')
        suitereportid = doc.getElementsByTagName('SUITEREPORTID')
        totalsteps = doc.getElementsByTagName('TOTALSTEPS')
        failures = doc.getElementsByTagName('FAILURES')
        errors = doc.getElementsByTagName('ERRORS')
        timetaken = doc.getElementsByTagName('TIMETAKEN')
        nodehost = doc.getElementsByTagName('NODEHOST')
        nodeport = doc.getElementsByTagName('NODEPORT')
        scriptstatus = doc.getElementsByTagName('SCRIPTSTATUS')
        loadcount = doc.getElementsByTagName('LOADCOUNT')
        tccount = doc.getElementsByTagName('TCCOUNT')
        tcpassed = doc.getElementsByTagName('TCPASSED')
        tcfailed = doc.getElementsByTagName('TCFAILED')
        scriptrelpath = doc.getElementsByTagName('SCRIPTRELPATH')
        starturl = doc.getElementsByTagName('STARTURL')
        launcherid = doc.getElementsByTagName('LAUNCHERID')
        scriptargs = doc.getElementsByTagName('SCRIPTARGS')
        starttime = doc.getElementsByTagName('STARTTIME')
        suiteid = doc.getElementsByTagName('SUITEID')
        suitename = doc.getElementsByTagName('SUITENAME')
        suiteinfo = doc.getElementsByTagName('SUITEINFO')

        scriptdetails = []
        for x in range(0,int(totalscript)):
            summary = {}
            summary['ID']=str(ids[x+8].childNodes[0].nodeValue)
            summary['SCRIPTREPORTID']=str(scriptreportid[x].childNodes[0].nodeValue)
            summary['SCRIPTNAME']=str(scriptname[x].childNodes[0].nodeValue)
            summary['SUITENAME']=str(suitename[x].childNodes[0].nodeValue)
            summary['SUITEREPORTID']=str(suitereportid[x].childNodes[0].nodeValue)
            summary['TOTALSTEPS']=str(totalsteps[x].childNodes[0].nodeValue)
            summary['FAILURES']=str(failures[x].childNodes[0].nodeValue)
            summary['ERRORS']=str(errors[x].childNodes[0].nodeValue)
            summary['TIMETAKEN']=str(timetaken[x+1].childNodes[0].nodeValue)
            summary['NODEHOST']=str(nodehost[x].childNodes[0].nodeValue)
            summary['NODEPORT']=str(nodeport[x].childNodes[0].nodeValue)
            summary['SCRIPTSTATUS']=str(scriptstatus[x].childNodes[0].nodeValue)
            summary['LOADCOUNT']=str(loadcount[x].childNodes[0].nodeValue)
            summary['TCCOUNT']=str(tccount[x].childNodes[0].nodeValue)
            summary['TCPASSED']=str(tcpassed[x].childNodes[0].nodeValue)
            summary['TCFAILED']=str(tcfailed[x].childNodes[0].nodeValue)
            summary['SCRIPTRELPATH']=str(scriptrelpath[x].childNodes[0].nodeValue)
            summary['STARTURL']=str(starturl[x].childNodes[0].nodeValue)
            summary['LAUNCHERID']=str(launcherid[x].childNodes[0].nodeValue)
            summary['SCRIPTARGS']=str(scriptargs[x])
            summary['STARTTIME']=str(starttime[x+1].childNodes[0].nodeValue)
            summary['SUITEID']=str(suiteid[x].childNodes[0].nodeValue)
            summary['SUITENAME']=str(suitename[x].childNodes[0].nodeValue)
            summary['SUITEINFO']=str(suiteinfo[x+1].childNodes[0].nodeValue)
            scriptdetails.insert(x, summary)

        scriptSummaries['summary']=scriptdetails
        successdata['scriptSummaries']=scriptSummaries

        ########################==========testCaseSummaries=======##########################

        testCaseSummaries = doc.getElementsByTagName('testCaseSummaries')
        successdata['testCaseSummaries']=str(testCaseSummaries)

        jsondata['RunSuite'+str(i)]= successdata

    #MONGO_SAHI_COLLECTION.insert_one(getSahiResultResponse(releaseNo,buildNo,jsondata))


    if flag==True:
        return str(getSahiResultResponse(releaseNo,buildNo,jsondata))
    else:
        failuredata = {}
        failuredata['statuscode'] = 404
        failuredata['errormsg'] = 'Sahi automation run did not happen on  '
        return str(buildErrorResponse(failuredata))

def sahi_failed_report(release,build):
    """This will return Sahi run detailed based on
    release : 4.0.0,4.2.0 ect.
    build : 1,2,3,4,5 ect
    """
    failuredata = {}
    i=1
    count = 0
    version = release+"_"+build
    source_file_name=""
    while i < int(runtime):
        source_file_name=str(result_url).replace("#RELEASE_NUMBER#", release).replace("#BUILD_NUMBER#", build).replace("#MODULE#", module).replace("#VERSION#", version).replace("#BROWSER#", browser).replace("#COUNTER#", str(i))
        resp = requests.get(source_file_name)
        if resp.status_code != 200:
            count=i-1
            #print("===============>",count, i)
            break
        i += 1
    source_file_name=str(result_url).replace("#RELEASE_NUMBER#", release).replace("#BUILD_NUMBER#", build).replace("#MODULE#", module).replace("#VERSION#", version).replace("#BROWSER#", browser).replace("#COUNTER#", str(count))
    try:
        resp = requests.get(source_file_name)
    except Exception as e:
        failuredata["statuscode"] = 404
        failuredata["errormsg"] = "atlas URL is not working : " + e.__str__()
        return str(buildErrorResponse(failuredata))

    if resp.status_code != 200:
        failuredata = {}
        failuredata['statuscode'] = 404
        failuredata['errormsg'] = 'Sahi automation run did not happened yet'
        return str(buildErrorResponse(failuredata))

    destination_file_name='RunSuite'+str(count)+'.xml'
    with open(destination_file_name, 'wb') as f:
        f.write(resp.content)

    doc = xml.dom.minidom.parse(destination_file_name)
    totalcount = doc.getElementsByTagName('TOTALCOUNT')
    totalscript = str(totalcount[0].childNodes[0].nodeValue)

    scriptname = doc.getElementsByTagName('SCRIPTNAME')
    scriptstatus = doc.getElementsByTagName('SCRIPTSTATUS')
    scriptrelpath = doc.getElementsByTagName('SCRIPTRELPATH')
    starttime = doc.getElementsByTagName('STARTTIME')
    timetaken = doc.getElementsByTagName('TIMETAKEN')
    #scriptdetails = []
    for x in range(0,int(totalscript)):
        scipttype = str(scriptrelpath[x].childNodes[0].nodeValue).split("/")
        summary = {}
        if str(scriptstatus[x].childNodes[0].nodeValue) == 'FAILURE':
            summary['script']=str(scriptname[x].childNodes[0].nodeValue)
            summary['scripttype']=scipttype[scipttype.__len__()-2]
            summary['starttime']=str(starttime[x+1].childNodes[0].nodeValue)
            summary['timetaken']=str(timetaken[x+1].childNodes[0].nodeValue)
            summary['release']=release
            summary['build']=build
            #scriptdetails.insert(x, summary)
            MONGO_SAHI_COLLECTION.insert_one(summary)
    return "Run happened successfully and result data is dumped into MONGO_SAHI_COLLECTION"
    #return str(getSuccessResponseSummary(scriptdetails))

def sahi_failed_summary(release,build):
    """This will return Sahi run detailed based on
    release : 4.0.0,4.2.0 ect.
    build : 1,2,3,4,5 ect
    """
    failuredata = {}
    successdata = {}
    version = release+"_"+build
    first_file_name=str(result_url).replace("#RELEASE_NUMBER#", release).replace("#BUILD_NUMBER#", build).replace("#MODULE#", module).replace("#VERSION#", version).replace("#BROWSER#", browser).replace("#COUNTER#", str(1))
    i=1
    count = 0

    source_file_name=""
    while i < int(runtime):
        source_file_name=str(result_url).replace("#RELEASE_NUMBER#", release).replace("#BUILD_NUMBER#", build).replace("#MODULE#", module).replace("#VERSION#", version).replace("#BROWSER#", browser).replace("#COUNTER#", str(i))
        resp = requests.get(source_file_name)
        if resp.status_code != 200:
            count=i-1
            #print("===============>",count, i)
            break
        i += 1
    source_file_name=str(result_url).replace("#RELEASE_NUMBER#", release).replace("#BUILD_NUMBER#", build).replace("#MODULE#", module).replace("#VERSION#", version).replace("#BROWSER#", browser).replace("#COUNTER#", str(count))

    try:
        resp = requests.get(source_file_name)
    except Exception as e:
        failuredata["statuscode"] = 404
        failuredata["errormsg"] = "atlas URL is not working : " + e.__str__()
        return str(buildErrorResponse(failuredata))

    if resp.status_code != 200:
        failuredata = {}
        failuredata['statuscode'] = 404
        failuredata['errormsg'] = 'Sahi automation run did not happened yet'
        return str(buildErrorResponse(failuredata))

    destination_file_name1='RunSuite1.xml'
    with open(destination_file_name1, 'wb') as f:
        resp1 = requests.get(first_file_name)
        f.write(resp1.content)

    doc1 = xml.dom.minidom.parse(destination_file_name1)

    totalcount1 = doc1.getElementsByTagName('TOTALCOUNT')
    totalscript1 = str(totalcount1[0].childNodes[0].nodeValue)
    successdata['TOTALCOUNT']=totalscript1

    destination_file_name='RunSuite'+str(count)+'.xml'
    with open(destination_file_name, 'wb') as f:
        f.write(resp.content)

    doc = xml.dom.minidom.parse(destination_file_name)

    totalcount = doc.getElementsByTagName('TOTALCOUNT')
    totalscript = str(totalcount[0].childNodes[0].nodeValue)

    failedcount = doc.getElementsByTagName('FAILEDCOUNT')
    successdata['FAILEDCOUNT']=str(failedcount[0].childNodes[0].nodeValue)

    scriptname = doc.getElementsByTagName('SCRIPTNAME')
    scriptstatus = doc.getElementsByTagName('SCRIPTSTATUS')

    failed = [];
    tabulardata = [];
    for x in range(0,int(totalscript)):
        if str(scriptstatus[x].childNodes[0].nodeValue) == 'FAILURE':
            failed.append([scriptname[x].childNodes[0].nodeValue])
    tabulardata.append(["Failed Scripts Name"])
    tabulardata.append(failed)
    successdata['tabulardata']=tabulardata
    return getSuccessResponseSummary(successdata)

def getSuccessResponse(data):
    returndata = {}
    returndata['success'] = 'true'
    returndata['data'] = data
    returndata['error'] = {}
    return returndata

def getSahiResultResponse(releaseNo,buildNo,data):
    returndata = {}
    returndata['ReleaseNo'] = releaseNo
    returndata['BuildNo'] = buildNo
    returndata['suites'] = data
    returndata['error'] = {}
    return returndata

def buildErrorResponse(data):
    returndata = {}
    returndata['success'] = 'false'
    returndata['data'] = {}
    returndata['error'] = data
    return returndata

def getSuccessResponseSummary(data):
    returndata = {}
    returndata["success"] = "true"
    returndata["data"] = data
    returndata["error"] = {}
    return json.dumps(returndata)
