class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, value):
        node = Node(value)
        node.next = self.top
        self.top = node

    def pop(self):
        node = self.top
        self.top = node.next
        return node.value


if __name__ == '__main__':
    stack = Stack()
    for i in range(5):
        stack.push(i)
    # while stack.top.next:
    print(stack.pop())
    print(stack.pop())
    print(stack.pop())
    print(stack.pop())
    print(stack.pop())
