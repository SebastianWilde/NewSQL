# import random, math

outputdebug = False


def debug(msg):
    if outputdebug:
        print
        msg


class Node():
    def __init__(self, key,index):
        self.key = key
        self.indexs = []
        self.indexs.append(index)
        self.left = None
        self.right = None


class AVLTree():
    def __init__(self, *args):
        self.node = None
        self.height = -1
        self.balance = 0
        self.name = ""
        self.db_name = ""
        self.tb_name = ""
        self.colums = []
        #arg 0 lista de elementos
        #arg 1 lista de indices
        #arg 2 nombre
        #arg 3 nombre_db
        #arg 4 nombre de la tabla
        #arg 5 columnas
        if len(args) == 6:
            for i,ind in zip(args[0],args[1]):
                self.insert(i,ind)
            self.name = args[2]
            self.db_name = args[3]
            self.tb_name = args[4]
            self.colums = args[5]


    def height(self):
        if self.node:
            return self.node.height
        else:
            return 0

    def is_leaf(self):
        return (self.height == 0)

    def find_indexs(self,key):
        tree = self.node
        if tree == None:
            debug("No existe "+ str(key))
        elif key == tree.key:
            return self.node.indexs
        elif key < tree.key:
            return self.node.left.find_indexs(key)
        elif key > tree.key:
            return self.node.right.find_indexs(key)
        else:
            debug("No existe "+ str(key))

    def insert_in_block(self,keys,indexs):
        for i, ind in zip(keys, indexs):
            self.insert(i, ind)


    def insert(self, key,index):
        tree = self.node
##
        newnode = Node(key,index)

        if tree == None:
            self.node = newnode
            self.node.left = AVLTree()
            self.node.right = AVLTree()
            debug("Inserted key [" + str(key) + "]")
        elif key == tree.key:
            self.node.indexs.append(index)

        elif key < tree.key:
            self.node.left.insert(key,index)

        elif key > tree.key:
            self.node.right.insert(key,index)

        else:
            debug("Key [" + str(key) + "] already in tree.")

        self.rebalance()

    def recontruir(self,key,index):
        self.node = None
        self.insert_in_block(key,index)

    def rebalance(self):
        '''
        Rebalance a particular (sub)tree
        '''
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.lrotate()  # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()

            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rrotate()  # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()

    def rrotate(self):
        # Rotate left pivoting on self
        debug('Rotating ' + str(self.node.key) + ' right')
        A = self.node
        B = self.node.left.node
        T = B.right.node

        self.node = B
        B.right.node = A
        A.left.node = T

    def lrotate(self):
        # Rotate left pivoting on self
        debug('Rotating ' + str(self.node.key) + ' left')
        A = self.node
        B = self.node.right.node
        T = B.left.node

        self.node = B
        B.left.node = A
        A.right.node = T

    def update_heights(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()

            self.height = max(self.node.left.height,
                              self.node.right.height) + 1
        else:
            self.height = -1

    def update_balances(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0

    def delete(self, key,index=None):
        # debug("Trying to delete at node: " + str(self.node.key))
        if self.node != None:
            if self.node.key == key:
                if len(self.node.indexs) > 1 and index!=None:
                    self.node.indexs.remove(index)
                    return
                debug("Deleting ... " + str(key))
                if self.node.left.node == None and self.node.right.node == None:
                    self.node = None  # leaves can be killed at will
                # if only one subtree, take that
                elif self.node.left.node == None:
                    self.node = self.node.right.node
                elif self.node.right.node == None:
                    self.node = self.node.left.node

                # worst-case: both children present. Find logical successor
                else:
                    replacement = self.logical_successor(self.node)
                    if replacement != None:  # sanity check
                        debug("Found replacement for " + str(key) + " -> " + str(replacement.key))
                        self.node.key = replacement.key

                        # replaced. Now delete the key from right child
                        self.node.right.delete(replacement.key)

                self.rebalance()
                return
            elif key < self.node.key:
                self.node.left.delete(key,index)
            elif key > self.node.key:
                self.node.right.delete(key,index)

            self.rebalance()
        else:
            return

    def logical_predecessor(self, node):
        '''
        Find the biggest valued node in LEFT child
        '''
        node = node.left.node
        if node != None:
            while node.right != None:
                if node.right.node == None:
                    return node
                else:
                    node = node.right.node
        return node

    def logical_successor(self, node):
        '''
        Find the smallese valued node in RIGHT child
        '''
        node = node.right.node
        if node != None:  # just a sanity check

            while node.left != None:
                debug("LS: traversing: " + str(node.key))
                if node.left.node == None:
                    return node
                else:
                    node = node.left.node
        return node

    def check_balanced(self):
        if self == None or self.node == None:
            return True

        # We always need to make sure we are balanced
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())

    def inorder_traverse(self):
        if self.node == None:
            return []

        inlist = []
        l = self.node.left.inorder_traverse()
        for i in l:
            inlist.append(i)

        inlist.append(self.node.key)

        l = self.node.right.inorder_traverse()
        for i in l:
            inlist.append(i)

        return inlist

    def display(self, level=0, pref=''):
        '''
        Display the whole tree. Uses recursive def.
        TODO: create a better display using breadth-first search
        '''
        self.update_heights()  # Must update heights before balances
        self.update_balances()
        if (self.node != None):
            print('-' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(
                self.balance) + "]", 'L' if self.is_leaf() else ' ')
            if self.node.left != None:
                self.node.left.display(level + 1, '<')
            if self.node.left != None:
                self.node.right.display(level + 1, '>')

"""
# Usage example
if __name__ == "__main__":
    #a = AVLTree()
    print("----- Inserting -------")
    # inlist = [5, 2, 12, -4, 3, 21, 19, 25]
    inlist = [7, 5, 2, 6, 3, 4, 1, 8, 9, 0]
    indexs = [7, 5, 2, 6, 3, 4, 1, 8, 9, 0]
    a = AVLTree(inlist,indexs,"avl1")
    #for i in inlist:
    #    a.insert(i,1)
    a.display()
    a.insert(5,2)
    print("------Finding--------")
    print(a.find_indexs(5)==None)
    print("----- Deleting -------")
    a.delete(5)
    print("------Finding--------")
    print(a.find_indexs(5)==None)
    print("----- Deleting -------")
    a.delete(3,1)
    a.delete(4,1)
    # a.delete(5)
    a.display()

    print(
    "Inorder traversal:", a.inorder_traverse())
"""