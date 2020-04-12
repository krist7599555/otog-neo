#include <algorithm>
#include <vector>
template<typename T>
class SegmentTree {
public:
  int n;
  std::vector<T> seg_min, seg_max;
  SegmentTree(int _n, T init_value): 
    n(_n), 
    seg_min(_n * 2, init_value),
    seg_max(_n * 2, init_value) {};

  void set(int idx, T val) {
    idx += n;
    seg_min[idx] = val;
    seg_max[idx] = val;
    for (; idx > 1; idx /= 2) {
      seg_min[idx >> 1] = std::min(seg_min[idx], seg_min[idx ^ 1]);
      seg_max[idx >> 1] = std::max(seg_max[idx], seg_max[idx ^ 1]);
    }
  }
  template <typename F>
  void travel(int l, int r, F func) {
    for (l += n, r += n; l < r; l /= 2, r /= 2) {
      if (l & 1) func(l++);
      if (r & 1) func(--r);
    }
  }
  T max(int l, int r) {
    T res = seg_max[n + l];
    travel(l, r, [&](int idx) {
      res = std::max<T>(res, seg_max[idx]);
    });
    return res;
  }
  T min(int l, int r) {
    T res = seg_min[n + l];
    travel(l, r, [&](int idx) {
      res = std::min<T>(res, seg_min[idx]);
    });
    return res;
  }
};

#ifndef OTOG_SERVER
int main() {
  
}
#endif
