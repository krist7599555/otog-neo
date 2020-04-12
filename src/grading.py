#! /usr/bin/env python3 -u
import os
import localprocess as lpc
import time
from config import grading_config
from dataclasses import dataclass, asdict
import json

@dataclass
class GradingOutput:
  result:  str = ""
  problem: str = ""
  user:    str = ""
  detail:  str = ""
  timestamp: int = int(time.time())

def grading(problem: str, submit_code_path: str) -> GradingOutput:
  config = grading_config(problem, submit_code_path)
  output = GradingOutput(
    problem=config.problem,
    user   =config.user
  )

  is_compile = False
  def do_compile():
    curr_dir = os.getcwd()
    os.chdir(config.problem_dir)
    # print("[COMPILE]", config.cmd_compile)
    # print("[ENV]", os.environ)
    compile_result = lpc.bash(config.cmd_compile)
    os.chdir(curr_dir)
    if compile_result.returncode != 0:
      output.result += "C"
      output.detail += compile_result.stderr.replace(curr_dir, ".")
      return False
    is_compile = True
    return True

  for t in config.testcase:

    if t.env:
      for key, value in t.env.items():
        # print('[SET] env', key, value)
        os.environ[key] = value

    if not is_compile or t.recompile:
      if not do_compile():
        continue

    runtime_result = lpc.bash(t.cmd_execute)
    # print(t.cmd_execute)
    if runtime_result.returncode == 124:
      output.result += 'T'
      output.detail += f"testcase {t.testcase}: exitcode={runtime_result.returncode}; timeout {config.timeout}s\n"
    elif runtime_result.returncode == 139:
      output.result += 'X'
      output.detail += f"testcase {t.testcase}: exitcode={runtime_result.returncode}; out of memory\n"
    elif runtime_result.returncode != 0:
      output.result += 'X'
      output.detail += f"testcase {t.testcase}: exitcode={runtime_result.returncode}; runtime error\n"
      output.detail += runtime_result.stderr + "\n"
    else:
      output.result += lpc.bash(t.cmd_check).stdout
  # lpc.bash(config.cmd_clear)

  return output

import click
import sys

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

@click.command()
@click.option('-f', '--format', 'format_', type=click.Choice(['cli', 'json', 'csv']), default='cli')
@click.option("-e", "--ext", 'ext_', multiple=True, default=[".cpp", ".c"])
@click.argument('filename', nargs=-1, type=click.Path())
@click.pass_context
def cli(ctx, format_, ext_, filename):
  filename = [f for f in filename if os.path.isfile(f) and os.path.splitext(f)[1] in ext_]
  if not filename:
    click.echo(ctx.get_help())
    ctx.exit()
  if format_ == "json": print("[", end="")
  if format_ == "csv":  print("timestamp,problem,user,result")
  
  for idx, file in enumerate(filename, 1):
    name = os.path.split(file)[-1]
    problem, *res = name.split('.')
    out = grading(problem, file)

    if   format_ == "cli":  print(str(idx).ljust(3), out.problem.ljust(20), out.user.ljust(15), ':', out.result)
    elif format_ == "csv":  print(",".join([str(out.timestamp), out.problem, out.user, out.result]))
    elif format_ == "json": print(json.dumps(asdict(out), ensure_ascii=False, separators=(',',':')), end=","if idx!=len(filename) else"]")
    if   format_ == "cli" and out.detail: print(f'{bcolors.FAIL}{out.detail}{bcolors.ENDC}', file=sys.stderr)

if __name__ == '__main__':
  cli()