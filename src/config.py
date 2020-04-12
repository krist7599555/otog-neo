from dataclasses import dataclass, field, asdict
from enum import Enum
import itertools
import pprint
import sys
from typing import List, Dict
import yaml
import os
from os import path

ROOT_DIR     = os.getcwd()
PROBLEMS_DIR = path.join(ROOT_DIR, 'problems')
CACHE_DIR    = path.join(ROOT_DIR, '.cache')
SUBMIT_DIR   = path.join(ROOT_DIR, 'submit')
BIN_DIR      = path.join(ROOT_DIR, 'bin')
CHECK_EQ_CMD = path.join(BIN_DIR, 'is_equal')
OUT_PROG_FILE= path.join(CACHE_DIR, 'a.out')
OUT_TEXT_FILE= path.join(CACHE_DIR, 'tmp.txt')

def env_set(key, value):
  os.environ[key] = value

class ConfigMode(Enum):
  equal       = "equal"
  interactive = "interactive"


@dataclass
class ConfigYmalTestCase:
  env: Dict[str, str] = None
  recompile: bool = False

@dataclass
class ConfigYmal:
  mode:     ConfigMode = "equal"
  compile:  str = f'g++ -w -std=c++17 -O2 "$OTOG_SUBMIT_FILE" -DOTOG_SERVER -o "$OTOG_OUT_PROG_FILE"'
  testcase: Dict[int, ConfigYmalTestCase] = field(default_factory=dict)
  timeout:  int = 1

@dataclass
class ConfigTestcase:
  testcase:    int = -1
  inp_file:    str = None
  sol_file:    str = None
  cmd_execute: str = None
  cmd_check:   str = None
  env:        dict = None
  recompile:  bool = False

@dataclass
class ConfigGrading:
  cmd_compile: str
  cmd_clear:   str
  problem_dir: str
  user:        str
  problem:     str
  timeout:     int
  path:     List[str]             = field(default_factory=list)
  testcase: List[ConfigTestcase]  = field(default_factory=list)
  def format(self):
    return pprint.pformat(asdict(self), width=150, compact=True)




def list_testcase(testcase_dir: str) -> [ConfigTestcase]:
  files = os.listdir(testcase_dir)
  keys = sorted(set(map(lambda f: int(f.split('.')[0]), files)))
  return [ConfigTestcase(
    testcase=i,
    inp_file=f"{testcase_dir}/{i}.inp" if f"{i}.inp" in files else None,
    sol_file=f"{testcase_dir}/{i}.sol" if f"{i}.sol" in files else None,
  ) for i in keys]

def grading_config(problem, submit_file):
  PROBLEM_DIR  = path.join(PROBLEMS_DIR, problem)
  TESTCASE_DIR = path.join(PROBLEM_DIR, 'testcase')
  CONFIG_FILE  = path.join(PROBLEM_DIR, 'config.yaml')
  RESOLVE_PATHS = [PROBLEM_DIR, PROBLEMS_DIR, SUBMIT_DIR, ROOT_DIR]
  SUBMIT_FILE  = submit_file if path.isabs(submit_file) else next((
    path.normpath(path.join(p, submit_file))
    for p in RESOLVE_PATHS if path.isfile(path.join(p, submit_file)))
  , "")
  
  env_set("OTOG_PROBLEM_DIR", PROBLEM_DIR)
  env_set("OTOG_SUBMIT_FILE", SUBMIT_FILE)
  env_set("OTOG_OUT_PROG_FILE", OUT_PROG_FILE)
  env_set("OTOG_OUT_TEXT_FILE", OUT_TEXT_FILE)
  env_set("OTOG_CACHE_DIR", CACHE_DIR)

  if not path.isdir(PROBLEM_DIR): raise FileExistsError(f"problem '{problem}' is not exist")
  if not path.isfile(SUBMIT_FILE): raise FileExistsError(f"submit file '{submit_file}' is not exist")
  try:
    config = ConfigYmal(**yaml.safe_load(open(CONFIG_FILE)))
  except TypeError as e:
    raise e
  except Exception as e:
    config = ConfigYmal()
  testcase = []
  for t in list_testcase(TESTCASE_DIR):
    t.cmd_execute = f"timeout {config.timeout}s {OUT_PROG_FILE} < {t.inp_file} > {OUT_TEXT_FILE}"
    t.cmd_check = {
      "equal":       f"{CHECK_EQ_CMD} {OUT_TEXT_FILE} {t.sol_file}",
      "interactive": f"cat {OUT_TEXT_FILE}"
    }.get(config.mode, None)
    if t.testcase in config.testcase:
      t2 = ConfigYmalTestCase(**config.testcase[t.testcase])
      if t2.env:       t.env       = t2.env
      if t2.recompile: t.recompile = t2.recompile
      
    t.recompile
    testcase.append(t)

  return ConfigGrading(
    cmd_compile=config.compile.replace("$1", SUBMIT_FILE),
    cmd_clear=f"rm {OUT_PROG_FILE}; rm {OUT_TEXT_FILE}",
    timeout=config.timeout,
    testcase=testcase,
    user=submit_file.split('.')[-2],
    problem=problem,
    problem_dir=PROBLEM_DIR,
    path=[
      PROBLEM_DIR,
      PROBLEMS_DIR,
      SUBMIT_DIR,
      ROOT_DIR
    ]
  )

# print(grading_config("sort_interactive", "sort_interactive.krist7599555.cpp").format())
# print(grading_config("sort_interactive", "./submit/sort_interactive.krist7599555.cpp").format())