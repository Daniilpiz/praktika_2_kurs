class TreeNode:
    """Узел бинарного дерева поиска."""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(root, key):
    """Вставка ключа в BST. Возвращает корень дерева."""
    if root is None:
        return TreeNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        # Дубликаты отправляем в правое поддерево
        root.right = insert(root.right, key)
    return root

def inorder_traversal(root, sorted_list):
    """Симметричный обход: заполняет список отсортированными ключами."""
    if root is not None:
        inorder_traversal(root.left, sorted_list)
        sorted_list.append(root.key)
        inorder_traversal(root.right, sorted_list)

def binary_tree_sort(arr):
    """Основная функция сортировки с помощью BST."""
    if not arr:
        return []
    root = None
    for item in arr:
        root = insert(root, item)
    result = []
    inorder_traversal(root, result)
    return result

# Пример использования
if __name__ == "__main__":
    data = [5, 2, 8, 3, 5, 1, 9, 2]
    sorted_data = binary_tree_sort(data)
    print("Исходный массив:", data)
    print("Отсортированный:", sorted_data)