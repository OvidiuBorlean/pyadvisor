import json
import re
import subprocess
import sys

cmdline = "kubectl get --raw".split(" ")
fileName = "/tmp/rawmetrics"
def getmetrics(cmd):
  full_cmd = cmdline + [cmd]
  process = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
  if process.returncode == 3:
      raise ValueError("invalid arguments: {}".format(cmdline))
  if process.returncode == 4:
      raise OSError("fping reported syscall error: {}".format(process.stderr))
  file1 = open(fileName, "w")
  file1.write(process.stdout)
  file1.close()
  return process.stdout

def lookfor(word):
  word = 'container_cpu_cfs_throttled_seconds_total'
  with open(fileName, 'r') as fp:
      lines = fp.readlines()
      for line in lines:
          if line.find(word) != -1:
             if line.find("#") == -1:
               values = line.split(" ")
               marker1 = '{'
               marker2 = '}'
               regexPattern = marker1 + '(.+?)' + marker2
               str_found = re.search(regexPattern, line).group(1)
               column = str_found.split(",")
               print(column[5], "  ",values[1])

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python cadvisor.py nodeName")
  else:
    nodeName = sys.argv[1]
    apicall = "/api/v1/nodes/" + nodeName + "/proxy/metrics/cadvisor"
    metric_output = getmetrics(apicall)
    lookfor("container_cpu_cfs_throttled_seconds_total")
