class Node:
    def __init__(self, data):
        self.data = data
        self.left_child = None
        self.right_child = None
        self.iterator = 1


def generate_tree(array):
    root = insert(None, array[0])
    for element in array[1:]:
        insert(root, element)
    return root


def insert(parent, new_value):
    if parent is None:
        parent = Node(new_value)
        return parent
    if new_value == parent.data:
        parent.iterator += 1
    elif new_value < parent.data:
        parent.left_child = insert(parent.left_child, new_value)
    else:
        parent.right_child = insert(parent.right_child, new_value)
    return parent


def find_largest_value(node):
    if node.right_child is None:
        return node
    else:
        return find_largest_value(node.right_child)


def remove(tree, nums):
    for num in nums:
        tree = delete_node(tree, num)
    return tree


def delete_node(node, value):
    if node is None:
        print("Tree is empty")
        return node
    if value < node.data:
        node.left_child = delete_node(node.left_child, value)
    elif(value > node.data):
        node.right_child = delete_node(node.right_child, value)
    else:
        if node.iterator > 1:
            node.iterator -= 1
            return node
        elif node.left_child is None:
            temp = node.right_child
            node = None
            return temp
        elif node.right_child is None:
            temp = node.left_child
            node = None
            return temp
        temp = find_largest_value(node.left_child)
        node.data = temp.data
        node.iterator = temp.iterator
        node.left_child = delete_node(node.left_child, temp.data)
    return node


def find(node, value):
    if node is None:
        return None
    if node.data == value:
        return node
    elif value > node.data:
        return find(node.right_child, value)
    elif value < node.data:
        return find(node.left_child, value)


def print_tree(root):
    if root:
        print_tree(root.left_child)
        print(root.data)
        print_tree(root.right_child)
