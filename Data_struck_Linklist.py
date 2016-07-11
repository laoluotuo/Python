class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Linklist:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def iter(self):
        cur = self.head
        yield cur.data
        while cur.next:
            cur = cur.next
            yield cur.data

    def insert(self, idx, data):
        cur = self.head
        cur_idx = 0
        while cur_idx < idx -1:
            cur = cur.next
            if cur is None:
                raise Exception('list is shorter than index')
            cur_idx += 1
        node = Node(data)
        node.next = cur.next
        cur.next = node
        if node.next is None:
            self.tail = node
    def remove(self, idx):
        cur = self.head
        cur_idx = 0
        while cur_idx < idx-1:
            cur = cur.next
            if cur is None:
                raise Exception('List is shorter than index')
            cur_idx += 1
        cur.next = cur.next.next
        if cur.next is None:
            self.tail = cur

    def pop(self, idx=None):
        if idx:
            print('Pop start')
            self.remove(idx)
        else:
            cur = self.head
            while True:
                cur = cur.next
                if not cur.next.next:
                    break
            cur.next =None
            self.tail = cur



if __name__ == '__main__':
    lst = Linklist()
    for i in range(10):
        lst.append(i)
    # lst.insert(3,133)
    # lst.remove(3)
    # lst.pop()
    for u in lst.iter():
        print(u)