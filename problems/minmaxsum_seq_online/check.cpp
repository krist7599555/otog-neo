#include <string>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>

// template<typename T>
// class SegmentTree;

template<typename T>
class SegmentTree_SOL {
public:
  int n;
  std::vector<T> seg_min, seg_max;
  SegmentTree_SOL(int _n, T init_value): 
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

#ifndef Type
#define Type int
#endif
#ifndef Random
#define Random {-1000, -100000, -1, 0, 1, 2, 3, 200, 2000, 10000}
#endif

typedef Type OtogType;

template <typename T>
void assert_equal(const T& a, const T& b) {
  // std::cout << a << ' ' << b << '\n';
  if (a != b) {
    putchar('-');
    exit(0);
  }
}

const std::vector<OtogType> randv = Random;
int main() {
  int n = 10, q = 20, seed = 1000;
  std::cin >> n >> q >> seed;  
  std::srand(seed);
  SegmentTree_SOL<OtogType> seg1(n, OtogType());
  SegmentTree<OtogType> seg2(n, OtogType());
  while (q--) {
    int rnd = std::rand() & 3;
    switch(rnd & 1) {
      case 0: {
        int idx = std::rand() % n;
        Type val = randv[std::rand() % randv.size()];
        seg1.set(idx, val);
        seg2.set(idx, val);
        break;
      }
      case 1: {
        int l = std::rand() % n,  
            r = std::rand() % n;
        int ll = std::min(l, r);
        int rr = std::max(l, r) + 1;
        switch(rnd & 2) {
          case 0: assert_equal(seg1.min(ll, rr), seg2.min(ll, rr)); break;
          case 2: assert_equal(seg1.max(ll, rr), seg2.max(ll, rr)); break;
        }
        break;
      }
    }
  }
  putchar('P');
}