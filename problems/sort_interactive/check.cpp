#include <cstdio>
#include <sstream>
#include <fstream>
#include <iostream>

namespace otog { // util class
  std::streambuf* _old_stdout;
  std::stringstream _bin_stream;
  void mute_stdout() {
    _old_stdout = std::cout.rdbuf();
    std::cout.rdbuf(_bin_stream.rdbuf());
  }
  void unmute_stdout() {
    std::cout.rdbuf(_old_stdout); 
  }
  void read_file(std::istream& f, char* filename) {
    f.read(filename, UINT_MAX);
  }
  void read_file(std::istream& f, std::istream& cin) {
    f.rdbuf(cin.rdbuf());
  }
}

namespace { // task valiable
  int _n;
  int _value[100];
  int _output[100];
}

void solve(int, int*); // user implement

bool is_less(int idx1, int idx2) {
  return _value[idx1] < _value[idx2];
}

bool is_answer_ok() {
  for (int i = 1; i < _n; ++i) {
    if (_value[_output[i-1]] > _value[_output[i]]) {
      return false;
    }
  }
  std::sort(_output, _output + _n);
  for (int i = 0; i < _n; ++i) {
    if (_output[i] != i) return false;
  }
  return true;
}

int main(int argn, char* argv[]) {
  otog::mute_stdout();
  std::ifstream file_input(argv[1]);
  std::istream& inp = file_input.good() ? file_input : std::cin;
  std::string result = "";
  while (inp >> _n) {
    for (int i = 0; i < _n; ++i) {
      inp >> _value[i];
    }
    solve(_n, _output);
    result += is_answer_ok() ? 'P' : '-';
  }
  otog::unmute_stdout();
  std::cout << result;
}


