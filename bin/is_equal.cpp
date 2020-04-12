#include <fstream>
#include <cstdio>
#include <string>
typedef std::string str;
void err(str s) {
  puts(s.c_str());
  exit(1);
}
void end(char c) {
  putchar(c);
  exit(0);
}

int main(int argn, char* argv[]) {
  std::ifstream lhs(argv[1]);
  std::ifstream rhs(argv[2]);
  if (lhs.bad()) err("not found: " + str(argv[1]));
  if (rhs.bad()) err("not found: " + str(argv[2]));
  str l, r;
  while (lhs >> l && rhs >> r) {
    if (l != r) {
      end('-');
    }
  }
  lhs >> std::ws;
  rhs >> std::ws;
  if (lhs.eof() && rhs.eof()) {
    end('P');
  } else {
    end('-');
  }
}