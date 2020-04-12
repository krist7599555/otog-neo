#include <algorithm>
#include <vector>

template<typename T>
class SegmentTree {
public:
  int n;
  std::vector<T> seg;
  SegmentTree(int _n, T init_value): 
    n(_n), 
    seg(_n, init_value) {};

  void set(int idx, T val) {
    seg[idx] = val;
  }

  T max(int l, int r) {
    T mx = seg[l];
    while (l < r) {
      mx = std::max<T>(mx, seg[l++]);
    }
    return mx;
    // return *std::max_element(seg.cbegin() + l, seg.cend() + r);
  }
  T min(int l, int r) {
    T mn = seg[l];
    while (l < r) {
      mn = std::min<T>(mn, seg[l++]);
    }
    return mn;
    // return *std::min_element(seg.begin() + l, seg.end() + r);
  }
};

#ifndef OTOG_SERVER
int main() {
  
}
#endif
