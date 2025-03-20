# pytest_realtime_result.py
import pytest
from datetime import datetime


class RealTimeResultPlugin:
    def __init__(self):
        self.result_file = "result.txt"
    def pytest_runtest_logreport(self, report):
        """receive test report and write to file"""
  
        # if exist worker_id, will not record result. sub_process will record result
        if hasattr(report, "worker_id"):
            return
       
        if report.when == "call" or (report.when == "setup" and report.skipped):
            nodeid = report.nodeid
            outcome = report.outcome
            
     
            if outcome == "passed" and not hasattr(report, "wasxfail"):
                status = "PASS"
            elif outcome == "failed":
                if hasattr(report, "wasxfail"):
                    status = "XPASS"
                else:
                    status = "FAIL"
            elif outcome == "skipped":
                status = "SKIP"
   
            elif getattr(report, "rerun", None) is not None:
                status = "RERUN"
                return   #rerun will not record result
            
            else:
                status = outcome.upper()
            
            # 检查xfail标记
            if hasattr(report, "wasxfail") and outcome == "skipped":
                status = "XFAIL"

            with open(self.result_file, "a", encoding="utf-8") as f: 
                f.write(f"{status} - {nodeid}\n")

@pytest.hookimpl
def pytest_configure(config):
    plugin = RealTimeResultPlugin()
    config.pluginmanager.register(plugin, "realtime_result_plugin")