from random import choices
from collections import deque
from dearpygui.dearpygui import *


class PriorityQueue:
    def __init__(self, mass=None, reverse=False):
        if mass is None:
            self.mass = []
        else:
            self.mass = deque(mass[:min(len(mass), 15)])
        self.reverse = reverse
        for i in range(len(self.mass) // 2 - 1, -1, -1):
            self.heapify(i)

    def cmp(self, a, b):
        if self.reverse:
            return self.mass[a] < self.mass[b]
        return self.mass[a] > self.mass[b]

    def get_mass(self):
        return list(self.mass)

    def get_parent(self, i):
        return (i - 1) // 2

    def left(self, i):
        return i * 2 + 1

    def right(self, i):
        return i * 2 + 2

    def heapify(self, i):
        l = self.left(i)
        r = self.right(i)
        current = i

        if l < len(self.mass) and self.cmp(l, current):
            current = l
        if r < len(self.mass) and self.cmp(r, current):
            current = r

        if current != i:
            self.mass[i], self.mass[current] = self.mass[current], self.mass[i]
            self.heapify(current)

    def heap_shift_up(self, i):
        while i > 0 and self.cmp(i, self.get_parent(i)):
            self.mass[i], self.mass[self.get_parent(i)] = self.mass[self.get_parent(i)], self.mass[i]
            i = self.get_parent(i)

    def insert(self, elem):
        if len(self.mass) >= 15:
            return
        self.mass.append(elem)
        self.heap_shift_up(len(self.mass) - 1)

    def heap_get(self):
        return self.mass[0]

    def pop(self):
        if len(self.mass) == 0:
            print("Leaf not found")
            return
        e = self.heap_get()
        self.mass[0] = self.mass[-1]
        self.mass.pop()
        self.heapify(0)
        return e

    def clear(self):
        self.mass = deque()

    def change(self, i, new_elem):
        if i < 0 or i >= len(self.mass):
            return
        self.mass[i] = new_elem
        self.heap_shift_up(i)
        self.heapify(i)

    def get_binary_tree(self):
        ret = ""
        children = deque()
        children.append(0)
        i = 1
        while len(children) and children[0] < len(self.mass):
            if i == 0:
                i = len(children)
                ret += "\n"
            children.append(self.left(children[0]))
            children.append(self.right(children[0]))
            ret += str(self.mass[children[0]]) + " "
            children.popleft()
            i -= 1
        return ret


m = choices(range(999), k=15)
a = PriorityQueue(m, reverse=True)
take_mass = []


def pop():
    elem = a.pop()
    if elem:
        take_mass.append(elem)
    render(a)


def generate_new_queue(sender, data, user_data):
    global m, a, take_mass
    m = choices(range(999), k=get_value(user_data))
    a = PriorityQueue(m, reverse=True)
    take_mass = []
    render(a)


def clear():
    global a, take_mass
    a.clear()
    take_mass = []
    render(a)


def add(sender, data, user_data):
    global a
    a.insert(get_value(user_data))
    render(a)


def change(sender, data, user_data):
    global a
    a.change(get_value(user_data[0]) - 1, get_value(user_data[1]))
    render(a)


def render(a):
    with window(label="Main Window", width=800, no_resize=True, ):
        add_text("Mass: " + str(a.get_mass()))
        add_button(label="Pop", callback=pop)
        add_text("Pop_Mass: " + str(take_mass))
        size = add_input_int(label="Mass_size", max_value=15, min_value=1, default_value=15, width=100)
        add_same_line()
        add_button(label="Generate_new_mass", callback=generate_new_queue, user_data=size)
        elem = add_input_int(label="Add Element", max_value=999, min_value=0, default_value=10, width=100)
        add_same_line()
        add_button(label="Add", callback=add, user_data=elem)
        index = add_input_int(label="Element Index", max_value=999, min_value=0, default_value=10, width=100)
        add_same_line()
        new_elem = add_input_int(label="New Value", max_value=999, min_value=0, default_value=10, width=100)
        add_same_line()
        add_button(label="Change", callback=change, user_data=[index, new_elem])
        add_button(label="Clear", callback=clear)
    with viewport_drawlist(front=False):
        draw_rectangle((0, 0), (800, 680), color=(0, 0, 0, 255), fill=(0, 0, 0, 255))
        tree = a.get_binary_tree().split("\n")
        height = 300
        for i in range(len(tree)):
            width = 800 // (2 ** i + 1)
            b = tree[i].split()
            for j in range(len(b)):
                draw_text((width * (j + 1) - 12.5, height - 12.5), text=b[j], size=20)
                draw_circle((width * (j + 1), height), 25, color=(255, 255, 255, 255))
                if (2 ** i + j - 1) * 2 + 1 < len(a.mass):
                    draw_arrow(((800 // (2 ** (i + 1) + 1)) * (j * 2 + 1), height + 75),
                               (width * (j + 1) - 18, height + 18))
                if (2 ** i + j - 1) * 2 + 2 < len(a.mass):
                    draw_arrow(((800 // (2 ** (i + 1) + 1)) * (j * 2 + 2), height + 75),
                               (width * (j + 1) + 18, height + 18))
            height += 100


create_context()
create_viewport(title='Custom Title', min_width=800, min_height=680, max_width=800, max_height=680)

render(a)

add_viewport_drawlist(front=False, tag="viewport_back")

setup_dearpygui()
show_viewport()
start_dearpygui()
destroy_context()
