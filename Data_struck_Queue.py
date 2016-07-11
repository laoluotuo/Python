class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def put(self,value):
        node = Node(value)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def pop(self):
        node = self.head
        if self.head is None:
            raise Exception('Queue is empty')
        else:
            self.head = self.head.next
            return node.value
            # yield self.head.value
            # self.head = self.head.next

    def iter(self):
        cur = self.head
        if self.head is None:
            raise Exception('Queue is empty')
        else:
            while True:
                yield cur.value
                if cur.next:
                    cur = cur.next
                else:
                    break

if __name__ == '__main__':
    q = Queue()
    for i in range(8):
        q.put(i)
    print(q.pop(), 'OK')
    print(q.pop(), 'OK')
    for a in q.iter():
        print(a)

