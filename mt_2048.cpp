#pragma clang diagnostic push
#pragma ide diagnostic ignored "cert-msc30-c"
#pragma clang diagnostic pop

#include <cstdio>
#include <cstdlib>
#include <iostream>

using namespace std;

int combine(int *l_state, int turn) {
    int score = 0;
    bool can_move = false;
    bool if_move = false;
    if (turn == 0) {
        for (int i = 0; i < 4; i++) {
            for (int t = 0; t < 3; t++) {
                int j = 0, k = 0;
                can_move = false;
                if (t != 1) {
                    for (j = 0; j < 4; j++) {
                        if (l_state[4 * i + j] != 0) {
                            l_state[4 * i + k] = l_state[4 * i + j];
                            k++;
                            if (can_move) {
                                if_move = true;
                            }
                        } else {
                            can_move = true;
                        }
                    }
                    while (k < 4) {
                        l_state[4 * i + k] = 0;
                        k++;
                    }
                } else
                    for (j = 0; j < 3; j++) {
                        if (l_state[4 * i + j] &&
                            l_state[4 * i + j] == l_state[4 * i + j + 1]) {
                            l_state[4 * i + j] += 1;
                            score += 1;
                            l_state[4 * i + j + 1] = 0;
                            j++;
                        }
                    }
            }
        }
    }
    if (turn == 1) {
        for (int j = 0; j < 4; j++) {
            for (int t = 0; t < 3; t++) {
                int i = 3, k = 3;
                can_move = false;
                if (t != 1) {
                    for (i = 3; i >= 0; i--) {
                        if (l_state[4 * i + j] != 0) {
                            l_state[4 * k + j] = l_state[4 * i + j];
                            k--;
                            if (can_move) {
                                if_move = true;
                            }
                        } else {
                            can_move = true;
                        }
                    }
                    while (k >= 0) {
                        l_state[4 * k + j] = 0;
                        k--;
                    }
                } else
                    for (i = 3; i >= 0; i--) {
                        if (l_state[4 * i + j] &&
                            l_state[4 * i + j] == l_state[4 * (i - 1) + j]) {
                            l_state[4 * i + j] += 1;
                            score += 1;
                            l_state[4 * (i - 1) + j] = 0;
                            i--;
                        }
                    }
            }
        }
    }
    if (turn == 2) {
        for (int i = 0; i < 4; i++) {
            for (int t = 0; t < 3; t++) {
                int j = 3, k = 3;
                can_move = false;
                if (t != 1) {
                    for (j = 3; j >= 0; j--) {
                        if (l_state[4 * i + j] != 0) {
                            l_state[4 * i + k] = l_state[4 * i + j];
                            k--;
                            if (can_move) {
                                if_move = true;
                            }
                        } else {
                            can_move = true;
                        }
                    }
                    while (k >= 0) {
                        l_state[4 * i + k] = 0;
                        k--;
                    }
                } else
                    for (j = 3; j > 0; j--)
                        if (l_state[4 * i + j] &&
                            l_state[4 * i + j] == l_state[4 * i + j - 1]) {
                            l_state[4 * i + j] += 1;
                            score += 1;
                            l_state[4 * i + j - 1] = 0;
                            j--;
                        }
            }
        }
    }
    if (turn == 3) {
        for (int j = 0; j < 4; j++) {
            for (int t = 0; t < 3; t++) {
                int i = 0, k = 0;
                can_move = false;
                if (t != 1) {
                    for (i = 0; i < 4; i++) {
                        if (l_state[4 * i + j] != 0) {
                            l_state[4 * k + j] = l_state[4 * i + j];
                            k++;
                            if (can_move) {
                                if_move = true;
                            }
                        } else {
                            can_move = true;
                        }
                    }
                    while (k < 4) {
                        l_state[4 * k + j] = 0;
                        k++;
                    }
                } else
                    for (i = 0; i < 3; i++) {
                        if (l_state[4 * i + j] &&
                            l_state[4 * i + j] == l_state[4 * (i + 1) + j]) {
                            l_state[4 * i + j] += 1;
                            score += 1;
                            l_state[4 * (i + 1) + j] = 0;
                            i++;
                        }
                    }
            }
        }
    }
    if (!if_move && score == 0) {
        score = -1;
    }
    return score;
}

int isOver(const int *state) {
    int zero_num = 0;
    bool can_combine = false;
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            if (state[4 * i + j] == 0) zero_num += 1;
            if ((j < 3 && state[4 * i + j] == state[4 * i + j + 1]) ||
                (i < 3 && state[4 * i + j] == state[4 * (i + 1) + j])) {
                can_combine = true;
            }
        }
    }
    if (zero_num == 0) {
        if (!can_combine) {
            return -1;
        } else {
            return zero_num;
        }
    }
    return zero_num;
}

void newBlock(int *state) {
    int new_num = 1;
    int r_num = rand() % 10;
    if (r_num > 8) new_num = 2;
    bool ok = false;
    while (!ok) {
        int r_place = rand() % 16;
        if (state[r_place] == 0) {
            state[r_place] = new_num;
            ok = true;
        }
    }
}

void runGame(const int *d_state, int *d_result, int search_depth, int tid) {
    int init_state = tid;
    int depth = search_depth;

    int l_state[16];
    for (int i = 0; i < 16; i++) l_state[i] = d_state[i];
    int result;
    int score = 0;
    int turn = 0;
    int zero_num = isOver(l_state);
    while (depth && zero_num != -1) {
        turn = init_state % 4;
        init_state /= 4;
        depth -= 1;
        result = combine(l_state, turn);
        if (result == -1 && depth == search_depth - 1) score -= 100;
        zero_num = isOver(l_state);
        score += result * (result > 0);
        if (zero_num > 0 && result != -1) newBlock(l_state);
    }

    int count = 0;
    while (zero_num != -1) {
        count += 1;
        turn = rand() % 4;
        result = combine(l_state, turn);
        score += result * (result > 0);
        zero_num = isOver(l_state);
        if (zero_num > 0 && result != -1) newBlock(l_state);
    }
    d_result[tid] = score;
}

void printArray(int *array, int size) {
    for (int i = 0; i < size; i++) printf("%d, ", array[i]);
    printf("\n");
}

int getBestRun(int *h_state, int exp_num = 5000, int search_depth = 2,
               bool print_flag = true) {
    int *d_state = h_state;

    const int search_kinds = (1 << (search_depth * 2));

    int *h_result = new int[search_kinds];
    for (int i = 0; i < search_kinds; i++) h_result[i] = 0;
    int *d_result = h_result;

    for (int i = 0; i < exp_num; ++i) {
        for (int j = 0; j < search_kinds; ++j) {
            runGame(d_state, d_result, search_depth, j);
        }
    }

    int max = -10000000;
    int best_way = 0;
    for (int i = 0; i < search_kinds; i++) {
        if (h_result[i] > max) {
            max = h_result[i];
            best_way = i;
        }
    }

    int best_turn = best_way % 4;

    if (print_flag) {
        printArray(h_result, search_kinds);
        printf("Best way is %d , Best score = %d , Best turn is %d \n", best_way,
               h_result[best_way], best_turn);
    }

    return best_turn;
}

int main(int argc, char *argv[]) {
    srand(time(nullptr));
    int *d_state;
    int h_state[16] = {0};

    int i = 0, k = 0;
    while (argc > 1 && argv[1][i] != '\0') {
        if (argv[1][i] != ',') {
            h_state[k] = h_state[k] * 10 + argv[1][i] - '0';
        } else {
            k += 1;
            if (k >= 16) {
                cout << "num of number exceed 16!" << endl;
            }
        }
        i = i + 1;
    }
    bool print_flag = true;
    if (argc > 2 && argv[2][0] == '1') {
        print_flag = false;
    }

    int exp_num = 3000;
    int search_depth = 2;
    if (argc > 3) {
        exp_num = 0;
        int i = 0;
        while (argv[3][i] != '\0') {
            exp_num = exp_num * 10 + argv[3][i] - '0';
            i++;
        }
    }

    if (argc > 4) {
        search_depth = argv[4][0] - '0';
    }
    int best_turn = getBestRun(h_state, exp_num, search_depth, print_flag);

    if (print_flag) {
        cout << "input h_state is:";
        printArray(h_state, 16);
    }
    printf("%d\n", best_turn);
    return best_turn;
}
