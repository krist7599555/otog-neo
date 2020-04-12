import subprocess as sp
from dataclasses import dataclass

@dataclass
class BashOutput:
  returncode: str = ""
  stdout: str = ""
  stderr: str = ""

def bash(cmd: str) -> BashOutput:
  proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True, encoding='utf-8')
  stdout, stderr = proc.communicate()
  return BashOutput(
    proc.returncode, 
    stdout, 
    stderr
  )