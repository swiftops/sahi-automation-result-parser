from flask import Flask
from sahi_report.sahiRunReport import sahi_run_report,sahi_run_result,sahi_failed_report,sahi_failed_summary

app = Flask(__name__)

@app.route('/getSahiRunSummary/<version>')
def sahiRunReport(version):
    """
        URL like : http://swiftops.digite.com/sahi_automation/getSahiRunSummary/4.2.0_18
    """
    data = sahi_run_report(version)
    return data

@app.route('/getSahiRunResult/<releaseNo>/<buildNo>')
def sahiRunResult(releaseNo,buildNo):
    """
        URL like : http://swiftops.digite.com/sahi_automation/getSahiRunResult/4.2.0/18
    """
    data = sahi_run_result(releaseNo,buildNo)
    return data

@app.route('/getSahiFailedReport/<release>/<build>')
def sahiFailedReport(release,build):
    data = sahi_failed_report(release, build)
    return data

@app.route('/getSahiFailedSummary/<release>/<build>')
def sahiFailedSummary(release,build):
    """
        URL like : http://swiftops.digite.com/sahi_automation/getSahiFailedSummary/4.2.0/15
    """
    data = sahi_failed_summary(release, build)
    return data


if __name__ == "__main__":
    app.run('0.0.0.0', port=7777, debug=True)