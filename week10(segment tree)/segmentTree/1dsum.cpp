#define _CRT_SECURE_NO_WARNINGS 
#include <cstdio>
#include <cmath>
#include <vector>
#include <memory>
#include <queue>
#include <utility>

using namespace std;

long long init(vector<long long>& a, vector<long long>& tree, int node, int start, int end) {
    int mid = (start + end) >> 1;
    if (start == end) {
        return tree[node] = a[start];
    }
    else {
        return tree[node] = init(a, tree, node * 2, start, mid) + init(a, tree, node * 2 + 1, mid + 1, end);
    }
}
void update(vector<long long>& tree, int node, int start, int end, int index, long long diff) {
    if (index < start || index > end) return;
    tree[node] = tree[node] + diff;

    int mid = (start + end) >> 1;
    if (start != end) {
        update(tree, node * 2, start, mid, index, diff);
        update(tree, node * 2 + 1, mid + 1, end, index, diff);
    }
}
long long sum(vector<long long>& tree, int node, int start, int end, int left, int right) {
    int mid = (start + end) >> 1;
    if (left > end || right < start) {
        return 0;
    }
    if (left <= start && end <= right) {
        return tree[node];
    }
    return sum(tree, node * 2, start, mid, left, right) + sum(tree, node * 2 + 1, mid + 1, end, left, right);
}
int main() {
    int n, m;
    FILE* in = fopen("input1.txt", "r");

    if (in == NULL) {
        printf("open error\n");
        return 0;
    }
    fscanf(in, "%d", &n);

    vector<long long> a(n);
    int h = (int)ceil(log2(n));
    int tree_size = (1 << (h + 1));

    int temp;
    for (int i = 0; i < n; i++) {
        fscanf(in, "%d", &temp);
        printf("%d ", temp);
        a[i] = temp;
    }
    printf("\n");
    vector<long long> tree(tree_size);
    fscanf(in, "%d", &m);
    
    init(a, tree, 1, 0, n - 1);
    while (m--) {
        int t1, t2, t3;
        fscanf(in,"%d ", &t1);
        if (t1 == 1) {
            int t2;
            int t3;
            fscanf(in, "%d %d", &t2, &t3);
            int diff = t3 - a[t2];
            a[t2] = t3;

            printf("change %dth elem with %d\n", t2, t3);
            update(tree, 1, 0, n - 1, t2, diff);
        }
        else if (t1 == 0) {
            int t2, t3;
            fscanf(in, "%d %d", &t2, &t3);
            
            printf("sum (%d,%d): %d\n", t2, t3, sum(tree, 1, 0, n - 1, t2 , t3 ));
        }
    }
    return 0;
}