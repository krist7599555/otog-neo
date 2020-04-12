# what you have to write a class
```
template <typename T>
class SegmentTree {
public:
  SegmentTree(int n, T init_value); // n <= 10000
  void set(int idx, T val);
  T max(int l, int r); // 0 <= l < r <= n
  T min(int l, int r); // 0 <= l < r <= n
  + ... another method as you want ...
};
```