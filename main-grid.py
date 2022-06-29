import random
from collections import defaultdict

import Grid
import Shortest

graph = defaultdict(list)


def add_edge(g, src, dest):
    g[src].append(dest)


def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False


def start_end():
    x1 = int(input("Enter Start point :\nx: "))
    y1 = int(input("y: "))
    x2 = int(input("Enter End point :\nx: "))
    y2 = int(input("y: "))
    return x1, y1, x2, y2


def intiate_grid(x1, y1, x2, y2):
    grids = []
    for i in range(10):
        inner = []
        for j in range(10):
            inner.append(Grid.Grid())
        grids.append(inner)
    grids[y1][x1].set_type("start")
    grids[y2][x2].set_type("end")
    grids[7][9].set_type("obs")
    grids[7][8].set_type("obs")
    grids[7][7].set_type("obs")
    grids[8][7].set_type("obs")
    return grids


def phase_2(start, end):
    randomlist = [79, 78, 77, 87, start, end]
    c = 0
    while c < 20:
        n = random.randint(0, 99)
        if not search(randomlist, n):
            grids[n // 10][n % 10].set_type("obs")
            randomlist.append(n)
            c += 1
    print("Obstacles are : [", end="")
    c = 0
    for i in randomlist:
        if grids[i // 10][i % 10].get_type() == "obs":
            if c == len(randomlist) - 1:
                print("({},{})]".format(i % 10, i // 10))
            else:
                print("({},{}),".format(i % 10, i // 10), end="")
        c += 1
    return randomlist


def connect_graph(grids, graph):
    for i in range(10):
        for j in range(10):
            if grids[i][j].get_type() != "obs":
                src_ver = i * 10 + j
                if j - 1 >= 0:
                    if grids[i][j - 1].get_type() != "obs":
                        left_ver = src_ver - 1
                        add_edge(graph, src_ver, left_ver)
                    if i - 1 >= 0:
                        if grids[i - 1][j - 1].get_type() != "obs":
                            upleft_ver = src_ver - 10 - 1
                            add_edge(graph, src_ver, upleft_ver)
                    if i + 1 <= 9:
                        if grids[i + 1][j - 1].get_type() != "obs":
                            downleft_ver = src_ver + 10 - 1
                            add_edge(graph, src_ver, downleft_ver)
                if i - 1 >= 0:
                    if grids[i - 1][j].get_type() != "obs":
                        up_ver = src_ver - 10
                        add_edge(graph, src_ver, up_ver)
                if i + 1 <= 9:
                    if grids[i + 1][j].get_type() != "obs":
                        down_ver = src_ver + 10
                        add_edge(graph, src_ver, down_ver)
                if j + 1 <= 9:
                    if grids[i][j + 1].get_type() != "obs":
                        right_ver = src_ver + 1
                        add_edge(graph, src_ver, right_ver)
                    if i - 1 >= 0:
                        if grids[i - 1][j + 1].get_type() != "obs":
                            upright_ver = src_ver - 10 + 1
                            add_edge(graph, src_ver, upright_ver)
                    if i + 1 <= 9:
                        if grids[i + 1][j + 1].get_type() != "obs":
                            downright_ver = src_ver + 10 + 1
                            add_edge(graph, src_ver, downright_ver)


def phase_3(g, r_list, grid, strt, finish):
    min = 1000
    ind = 0
    for i in range(len(r_list)):
        x = r_list[i] // 10
        y = r_list[i] % 10
        if grid[x][y].get_type() == "obs":
            grid[x][y].set_type("empty")
            connect_graph(grid, g)
            f, path, length = Shortest.printShortestDistance(g, strt, finish, 100)
            if f and len(path) < min:
                min = len(path)
                ind = i
                p = path
                l = length
            grid[x][y].set_type("obs")
            g = defaultdict(list)
    grid[r_list[ind] // 10][r_list[ind] % 10].set_type("mod")
    print("Suggested obstacles to be removed that opens the path and provides shortest path is [({},{})]".format(
        r_list[ind] % 10, r_list[ind] // 10))
    print_path(p, l)
    draw_grid(grid)


def print_path(path, length):
    print("Shortest path length is : " + length)
    print("Path is : [", end=" ")
    for i in range(len(path) - 1, -1, -1):
        if i == 0:
            print(" ({},{}) ]".format(path[i] % 10, path[i] // 10))
        else:
            print(" ({},{}) ->".format(path[i] % 10, path[i] // 10), end="")

def draw_grid(grids):
    d = int(input("\n\nDo you want to draw grid?\n1-Yes\n2-No\nChoose 1 or 2: "))
    if d == 1:
        print("+ : Empty grid\n- : obstacle\n* : modified obstacle\n> : start\n< : end")
        print("X:\t|\t0\t|\t1\t|\t2\t|\t3\t|\t4\t|\t5\t|\t6\t|\t7\t|\t8\t|\t9\t|")
        print("-------------------------------------------------------------------------------------")
        for i in range(10):
            print(i, ":", end="\t|\t")
            for j in range(10):
                str = grids[i][j].get_type()
                if str == "empty":
                    print("+", end="\t|\t")
                elif str == "obs":
                    print("-", end="\t|\t")
                elif str == "mod":
                    print("*", end="\t|\t")
                elif str == "start":
                    print(">", end="\t|\t")
                else:
                    print("<", end="\t|\t")
            print("\n-------------------------------------------------------------------------------------")

if __name__ == "__main__":
    # x1, y1, x2, y2 = start_end()
    x1, y1, x2, y2 = 0, 0, 9, 9
    start = y1 * 10 + x1
    end = y2 * 10 + x2
    grids = intiate_grid(x1, y1, x2, y2)

    # phase = int(input("1) Phase 1.\n2) Phase 2.\nChoose phase: "))
    phase = 2
    if phase == 2:
        random_list = phase_2(start, end)
    connect_graph(grids, graph)
    flag, path, length = Shortest.printShortestDistance(graph, start, end, 100)
    if not flag:
        print("Given source and destination are not connected")
        phase3 = int(input("Do you want to start phase 3?\n1-Yes\n2-No\nChoose 1 or 2: "))
        if phase3 == 1:
            phase_3(graph, random_list, grids, start, end)
    else:
        print_path(path, length)
        draw_grid(grids)

