#include <algorithm>

bool is_less(int, int); // this function is defined some where
void solve(int n, int* ans) {
  for (int i = 0; i < n; ++i) ans[i] = i;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      if (is_less(ans[j], ans[i])) {
        std::swap(ans[i], ans[j]);
      }
    }
  }
}

#ifndef OTOG_SERVER
bool is_less(int i, int j) {
  return true;
}
int main() {
  int ar[3];
  solve(1, ar);
}
#endif