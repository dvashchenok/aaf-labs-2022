class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def __getitem__(self, item):
      return self.data[item]

class Tree_list():

  def __init__(self):
    self.storage = {}

  def __getitem__(self, name):
    return self.storage[name]

  def __setitem__(self, key, value):
    tree = Tree(value)
    self.storage[key] = tree
    return f"Tree with name {{value}} appended to tree_list"

class Tree():

    def __init__(self, name):
        self.size = 0
        self.root = None
        self.name = name

    def add(self, to_add):
        node = Node(to_add)
        if self.root == None:
            self.root = node

        else: self.add_node(self.root, node, True)

    def add_node(self, subroot, point, bool):
        if (bool and (point[0] <= subroot[0])):
            if(subroot.left == None):
                subroot.left = point
                self.size +=1
                # print('Went to left')
            else: self.add_node(subroot.left, point, False)

        elif bool:
            if (subroot.right == None):
              subroot.right = point
              self.size += 1
              # print('Went to right')
            else: self.add_node(subroot.right, point, False)

        elif (not bool and (point[1] <= subroot[1])):
            if (subroot.left == None):
              subroot.left = point
              self.size += 1
              # print('Went to left')
            else: self.add_node(subroot.left, point, True)

        elif (not bool):
          if (subroot.right == None):
              subroot.right = point
              self.size += 1
              # print('Went to right')
          else: self.add_node(subroot.right, point, True)
        return f"Alles Gut"

    def contains(self, subroot, value):
        if  self.Contains(subroot, value, True) == 1:
            return True
        else:
            return False

    def Contains(self, subroot, value, bool):
      if bool:
        temp = 0
      else: temp = 1
      if value == subroot.data:
          return 1
      if (value[temp] <= subroot.data[temp]):
          if subroot.left:
              if self.Contains(subroot.left, value, temp) == 1:
                  return 1
      else:
          if subroot.right:
              if self.Contains(subroot.right, value, temp) == 1:
                  return 1
      # print(value, subroot.data)
      # if value == subroot.data:
      #   return 1
      # elif (bool and (value[0] <= subroot.data[0])):
      #   if (subroot.left != None):
      #     self.Contains(subroot.left, value, False)
      # elif bool:
      #   if (subroot.right != None):
      #     self.Contains(subroot.right, value, False)
      # elif (not bool and (value[1] <= subroot.data[1])):
      #   if (subroot.left != None):
      #    self.Contains(subroot.left, value, True)
      # elif (not bool):
      #   if (subroot.right != None):
      #     self.Contains(subroot.right, value, True)

    def recursive_search(self, point):
      print(point.data)
      if point.right != None:
          self.recursive_search(point.right)
      if point.left != None:
          self.recursive_search(point.left)

# tree_list = Tree_list()
# tree_list['ipt'] = []
#
# tree_list["ipt"].add([5, 10])
# tree_list["ipt"].add([3, 4])
# tree_list["ipt"].add([2, 7])
# tree_list["ipt"].add([1, 4])
# tree_list["ipt"].add([6, 7])
#
# tree_list["ipt"].recursive_search(tree_list["ipt"].root)
# tree_list["ipt"].contains(tree_list['ipt'].root,[5,10])
# # tree.recursive_search(tree.root)
# print(tree.contains(tree.root, [4,3]))

# print(tree.size)