
class Node:
    def __init__(self, content):
        self.value = content
        self.next = None

    def __str__(self):
        return ('CONTENT:{}\n'.format(self.value))

    __repr__=__str__


class ContentItem:
    
    def __init__(self, cid, size, header, content):
        self.cid = cid
        self.size = size
        self.header = header
        self.content = content

    def __str__(self):
        return f'CONTENT ID: {self.cid} SIZE: {self.size} HEADER: {self.header} CONTENT: {self.content}'

    __repr__=__str__

    def __eq__(self, other):
        if isinstance(other, ContentItem):
            return self.cid == other.cid and self.size == other.size and self.header == other.header and self.content == other.content
        return False

    def __hash__(self):
        count=0
        for element in self.header:
            count+=ord(element)
        return count%3



class CacheList:
   
    def __init__(self, size):
        self.head = None
        self.maxSize = size
        self.remainingSpace = size
        self.numItems = 0

    def __str__(self):
        listString = ""
        current = self.head
        while current is not None:
            listString += "[" + str(current.value) + "]\n"
            current = current.next
        return 'REMAINING SPACE:{}\nITEMS:{}\nLIST:\n{}'.format(self.remainingSpace, self.numItems, listString)  

    __repr__=__str__

    def __len__(self):
        return self.numItems
    
    def put(self, content, evictionPolicy):
        new_node=Node(content)
        if content.size > self.maxSize:
            return "Insertion not allowed"


        if content.cid in self:
            return f"Content {content.cid} already in cache, insertion not allowed"
        
        if content.size > self.remainingSpace:
            while content.size > self.remainingSpace:
                if evictionPolicy=='mru':     
                    self.mruEvict()
                else:
                    self.lruEvict()
        
        
        new_node.next=self.head
        self.head=new_node
        self.remainingSpace-=new_node.value.size
        self.numItems+=1
        return f"INSERTED: {content}" 
                   


    def __contains__(self, cid):
        current=self.head
        prev=None
        while current is not None:
            if current.value.cid==cid and prev is not None:
                num=current
                prev.next=current.next
                num.next=self.head
                self.head=num
                return True
            elif current.value.cid==cid and prev is None:
                return True
            prev=current
            current=current.next
        return False


    def update(self, cid, content):
        new_node=Node(content)
        if cid in self:
            n=self.remainingSpace+self.head.value.size
            if content.size > self.maxSize or content.size > n:
                return "Cache miss!"
            elif content.size <= n:
                self.remainingSpace+=self.head.value.size
                new_node.next=self.head.next
                self.head=new_node
                self.remainingSpace-=new_node.value.size
                return f"UPDATED: {content}"
        return "Cache miss!"



    def mruEvict(self):
        self.remainingSpace+=self.head.value.size
        self.head=self.head.next
        self.numItems-=1

    
    def lruEvict(self):
        current=self.head
        prev=None
        while current is not None:
            if current.next is None and prev is not None:
                self.remainingSpace+=current.value.size
                self.numItems-=1
                prev.next=None
                return 
            elif current.next is None and prev is None:
                self.remainingSpace+=current.value.size
                self.head=None
                self.numItems-=1
                return
            prev=current
            current=current.next


    
    def clear(self):
        self.head=None
        self.numItems=0
        self.remainingSpace=self.maxSize
        return 'Cleared cache!'


class Cache:


    def __init__(self):
        self.hierarchy = [CacheList(200), CacheList(200), CacheList(200)]
        self.size = 3
    
    def __str__(self):
        return ('L1 CACHE:\n{}\nL2 CACHE:\n{}\nL3 CACHE:\n{}\n'.format(self.hierarchy[0], self.hierarchy[1], self.hierarchy[2]))
    
    __repr__=__str__


    def clear(self):
        for item in self.hierarchy:
            item.clear()
        return 'Cache cleared!'

    
    def insert(self, content, evictionPolicy):
        return self.hierarchy[hash(content)].put(content, evictionPolicy)


    def __getitem__(self, content):
        if content.cid in self.hierarchy[hash(content)]:
            return content
        return "Cache miss!"


    def updateContent(self, content):
        return self.hierarchy[hash(content)].update(content.cid, content)



