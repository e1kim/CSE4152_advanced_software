#define _CRT_SECURE_NO_WARNINGS 
#include <cstdio>
#include <memory>
#include <queue>
#include <utility>
#include <cmath>
 
// SegmentTree1D 구현하세요. 직접 스크래치로 전부 구현하셔도 무관합니다.
// 원소 합을 return 해주는 sum 함수와 원소 수정에 대한 modify 함수 구현

class Node {
public:
    Node(int left, int right) {

        this->left = left;
        this->right = right;
        mid = (left + right) >> 1;
        sum = 0;
        leftNode = NULL;
        rightNode = NULL;

    }
    int left, right, mid, sum;
    Node* leftNode, * rightNode;
};
typedef std::pair<int, int> pairi2; //int 형 두 개체를 단일 개체로 처리 목적

class SegmentTree1D {

public:
    SegmentTree1D(int n) {
        //n개 사이즈 만큼 할당
        this->n = n;
        m = 1;
        int temp = n;
        while (temp) {
            m <<= 1;
            temp >>= 1;
            
        }
        
        array = new int[n];
        cum_array = new int[n];
        root = new Node(0, n - 1);
        
    }

    // 초기화
    void initialize() {
        int sum = 0;
        for (int i = 0;i < n;i++) {
            sum += array[i];
            cum_array[i] = sum;
        }
        make_init(root);
    }
    int make_init(Node *cur) {
        if (cur->left == cur->right) return cur->sum = array[cur->right];
        cur->leftNode = new Node(cur->left, cur->mid);
        cur->rightNode = new Node(cur->mid + 1, cur->right);

        return cur->sum = make_init(cur->leftNode) + make_init(cur->rightNode);
    }
    int SUM(Node *cur, int x, int y) {
        if (x > cur->right || cur->left > y) return 0;
        if (x <= cur->left && cur->right <= y) return cur->sum;

        int left = SUM(cur->leftNode, x, y);
        int right = SUM(cur->rightNode, x, y);
        return left + right;

    }
    int sum(int x, int y) {
    /*
        x에서 y 까지의 합
    */
        return SUM(root, x, y);        
    }

    void modify(int idx, int num) {
    /*
        idx에 위치한 원소를 num으로 교체
    */
        if (idx > n - 1 || idx < 0) return;
        int diff = num - array[idx];
        array[idx] = num;

        Node* cur = root;
        while (cur != NULL) {
            cur->sum += diff;
            if (cur->mid < idx) cur = cur->rightNode;
            else cur = cur->leftNode;
        }
        
        
    }
    
    

    int n;
    int m;
    int* array;
    int* cum_array;
    Node* root;
};

int main() {

    int n, m;
    FILE* in = fopen("input_assignment1.txt", "r");

    if (in == NULL) {
        printf("open error\n");
        return 0;
    }
    fscanf(in, "%d", &n);
    SegmentTree1D A(n);

    int temp;
    for (int i = 0;i < n;i++) {
        fscanf(in, "%d", &temp);
        printf("%d ", temp);
        A.array[i] = temp;
    }
    printf("\n");

    A.initialize();

    fscanf(in, "%d", &m);
    for (int i = 0;i < m;i++) {

        fscanf(in, "%d\n", &temp);

        if (temp == 0) {
            int st, ed;
            fscanf(in, "%d %d", &st, &ed);
            printf("sum (%d,%d): %d\n", st, ed, A.sum(st, ed));

        }
        else {
            int idx, num;
            fscanf(in, "%d %d", &idx, &num);
            printf("change %dth elem with %d\n", idx + 1, num);
            A.modify(idx, num);
        }
    }

    return 0;

}