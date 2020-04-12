#! /usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
g++ "$DIR/is_equal.cpp" -o "$DIR/is_equal"
if [[ "$OSTYPE" == "darwin"* ]]; then
  brew install libyaml
  brew install gcc@8
else
  sudo apt install python3.7
  sudo apt install gcc-8
fi

export PYTHONPATH="/usr/local/lib/python3.6/site-packages:$PYTHONPATH"
export PYTHONPATH="/usr/local/lib/python3.7/site-packages:$PYTHONPATH"
export PYTHONPATH="/usr/local/lib/python3.8/site-packages:$PYTHONPATH"
export PYTHONPATH="/usr/local/lib/python3.9/site-packages:$PYTHONPATH"

pip3 install pyyaml
pip3 install click
pip3 uninstall typing