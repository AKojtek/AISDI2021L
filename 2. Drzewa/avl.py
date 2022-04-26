class Node:
    def __init__(self, val, reps=1, left=None, right=None, height=1):
        self.val = val
        self.reps = reps
        self.left = left
        self.right = right
        self.height = height

    def copy(self):
        if self.left:
            n_left = (self.left).copy()
        else:
            n_left = None
        if self.right:
            n_right = (self.right).copy()
        else:
            n_right = None
        return Node(self.val, self.reps, n_left, n_right, self.height)


def height(node):
    if node is None:
        return 0
    return node.height


def most_left(root):
    # Returns most left child of root

    if root.left is None:
        # Properly used, root is never None
        return root
    return most_left(root.left)


def generate_tree(nums):
    tree = None
    for num in nums:
        inserted, tree = insert(tree, num)
    return tree


def insert(root, num):
    # Returns if whole new node was inserted and tree from given root

    if root is None:
        return True, Node(num)
    elif root.val == num:
        root.reps += 1
        return False, root
    elif root.val > num:
        new_ins, new_node = insert(root.left, num)
        if new_ins:
            root.left = new_node
    else:
        new_ins, new_node = insert(root.right, num)
        if new_ins:
            root.right = new_node

    root.height = max(height(root.left), height(root.right)) + 1

    if abs(height(root.left) - height(root.right)) > 1:
        root = balance(root)

    return new_ins, root


def remove(tree, nums):
    for num in nums:
        tree = delete(tree, num)
    return tree


def delete(root, num, rem_all=False):
    # Returns if whole node was deleted and tree from given root

    if root is None:
        return root
    elif root.val > num:
        root.left = delete(root.left, num, rem_all)
    elif root.val < num:
        root.right = delete(root.right, num, rem_all)
    elif root.val == num:
        root.reps -= 1
        if root.reps > 0 and not rem_all:
            return root
        else:
            if root.left is None:
                root = root.right
            elif root.right is None:
                root = root.left
            else:
                min_right = most_left(root.right)
                root.val = min_right.val
                root.reps = min_right.reps
                root.right = delete(root.right, root.val, True)

    if root is None:
        return root

    root.height = max(height(root.left), height(root.right)) + 1

    if abs(height(root.left) - height(root.right)) > 1:
        root = balance(root)

    return root


def balance(root):
    if height(root.left) > height(root.right):
        if height(root.left.left) < height(root.left.right):
            # Left Right case
            root.left = left_rotate(root.left)
        # Left cases
        root = right_rotate(root)
    elif height(root.left) < height(root.right):
        if height(root.right.left) > height(root.right.right):
            # Right Left case
            root.right = right_rotate(root.right)
        # Right cases
        root = left_rotate(root)
    root = update_height(root)
    return root


def left_rotate(root):
    loose_node = root.copy()
    root = root.right
    if root.left:
        loose_node.right = root.left.copy()
    else:
        loose_node.right = None
    root.left = loose_node
    return root


def right_rotate(root):
    loose_node = root.copy()
    root = root.left
    if root.right:
        loose_node.left = root.right.copy()
    else:
        loose_node.left = None
    root.right = loose_node
    return root


def find(root, num):
    if root is None:
        return root
    elif root.val > num:
        return find(root.left, num)
    elif root.val < num:
        return find(root.right, num)
    elif root.val == num:
        return root


def update_height(root):
    if root is None:
        return None
    root.left = update_height(root.left)
    root.right = update_height(root.right)

    root.height = max(height(root.left), height(root.right)) + 1
    return root


def print_tree(tree):
    # For testing purposes

    print_part_of_tree(tree)
    print()


def print_part_of_tree(root):
    # For testing purposes

    if root is None:
        print('.', end='')
        return
    print(root.val, '-', root.reps, sep='', end='')
    if root.left or root.right:
        print('(', sep='', end='')
        print_part_of_tree(root.left)
        print(' ', end='')
        print_part_of_tree(root.right)
        print(')', sep='', end='')
