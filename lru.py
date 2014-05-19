"""
LRU = least recently used cache
    - cache = key/value pair
    - linked list = left is the newest
    - indext_hash = point from key to every node to look up N(1)
"""

class Node:
    def __init__(self, key, next=None, prev=None):
        self.key = key
        self.next = next
        self.prev = prev

    def __repr__(self):
        return "[{}]".format(self.key)

class IndexCache:
    def __init__(self, max_count):
        self.root = None
        self.last = None
        self.index_hash = dict()
        self.counter = 0
        self.max_count = max_count

    def insert(self, key):
        if key in self.index_hash:
            self.update(key)
            print 'update', self.index_hash
        else:
            node = Node(key)
            self.counter += 1
            if not self.root:
                self.root = node
                self.last = self.root
            else:
                node.next=self.root
                self.root.prev = node
                self.root = node
            self.index_hash[key] = node
            if self.counter >= self.max_count:
                self.retire()

    def retire(self):
        if self.last:
            self.index_hash.pop(self.last.key)
            new_last = self.last.prev
            if new_last:
                new_last.next = None
            else:
                new_last = None
            self.last = new_last
            self.counter -= 1

    def update(self, key):
        node = self.index_hash.pop(key)
        if node.prev:
            node.prev.next = node.next or None
        if node.next:
            node.next.prev = node.prev or None
        del node
        if self.root.key == key:
            self.root = self.root.next or None
        if self.last and self.last.key == key:
            self.last = self.last.prev or None

    def __repr__(self):
        node = self.root
        out = ''
        while node:
            out += '{} <-> '.format(node)
            node = node.next
        out += "\nEnd at {}".format(self.last)
        out += "\nhash: {}".format(self.index_hash)
        out += "\ntotal: {}".format(self.counter)
        return out




class Cache:
    def __init__(self, max_count):
        self._cache = dict()
        self._index_cache = IndexCache(max_count)

    def get(self, key, value=None):
        self._cache.get(key, value)

    def set(self, key, value):
        self._cache[key] = value
        self._index_cache.insert(key)

    def __repr__(self):
        return str(self._index_cache)




l = IndexCache(3)
l.insert(1)
l.insert(2)
l.insert(3)
l.retire()
l.retire()
l.retire()


print l

for i in range(10):
    l.insert(i)

print l

c = Cache(10)
for i in range(14):
    c.set(i, i)

c.set(1, 2)
c.set(2, 3)
print c
c.set(1, 3)
print c
c.set(1, 3)
print c
c.set(1, 3)
c.set(1, 3)
print c
c.set(1, 3)
c.set(1, 3)
c.set(1, 3)
c.set(1, 3)
c.set(1, 3)
c.set(1, 3)
c.set(1, 3)
print c
