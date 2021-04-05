class ElementArray:
    def __init__(self,size=1024,init=None):
        self._size=size
        self._items=[init for _ in range(size)]

    def __getitem__(self, idx):
        return self._items[idx]

    def __setitem__(self, idx, value):
        self._items[idx]=value

    def __len__(self):
        return self._size

    def __iter__(self):
        for item in self._items:
            yield item

    def clear(self):
        for i in range(len(self._items)):
            self._items[i]=None

class Ele:
    def __init__(self,k,v):
        self.key=k
        self.value=v

class Hashable:
    UNUSED=None #状态 1、位置没用过
    EMPTY=Ele(None,None) # 2、用过但是被删除了

    def __init__(self):
        self._table=ElementArray()
        self.length=0

    @property
    def _load_factor(self):
        #装载因子
        return self.length/float(len(self._table))

    def __len__(self):
        return self.length

    def _hash(self,key):
        # hash函数
        return abs(hash(key))%len(self._table)

    def __contains__(self, key):
        index=self._find_key(key)
        return index is not None

    def _find_key(self,key):
        # 查询key
        index=self._hash(key)
        _len=len(self._table)

        while self._table[index] is not Hashable.UNUSED:
            if self._table[index] is Hashable.EMPTY:
                #冲突了
                index = self._deal_conflict(index,_len) 
                continue
            elif self._table[index].key==key: #找到了
                return index
            else:
                # 冲突了
                index=self._deal_conflict(index,_len)
        return None

    def _deal_conflict(self,index,_len):
        # 开放定值法，线性探测，更省空间
        return (index*5+1)%_len

    def _find_ele_for_insert(self,key):
        #寻找可以插入的位置
        index=self._hash(key)
        _len=len(self._table)
        while not self._ele_cana_insert(index):
            index=self._deal_conflict(index,_len)
        return index

    def _ele_cana_insert(self,index):
        return self._table[index] is Hashable.EMPTY or self._table[index] is Hashable.UNUSED

    def put(self, key,value):
        #添加元素
        if key in self:
            index=self._find_key(key) #先找索引然后添加值
            self._table[index].value=value
            return False
        else:
            index=self._find_ele_for_insert(key)
            self._table[index]=Ele(key,value)
            self.length+=1
            if self._load_factor >=0.8:
                #装载因子太大了，要rehash
                self._rehash()
            return True

    def _rehash(self):
        #空间太小了
        old_table=self._table
        new_size=len(self._table)*2 #扩大一倍
        self._table=ElementArray(new_size,Hashable.UNUSED) #定义一个空的数组
        for ele in old_table:
            if ele is not Hashable.UNUSED and ele is not Hashable.EMPTY:
                index=self._find_ele_for_insert(ele.key)
                self._table[index]=ele
                self.length+=1

    def get(self,key):
        index=self._find_key(key)
        if index is None:
            return None
        else:
            return self._table[index].value

    def remove(self,key):
        """
        to-do
        :param key:
        :return:
        """
        pass

    def __iter__(self):
        for ele in self._table:
            if ele not in (Hashable.EMPTY,Hashable.UNUSED):
                yield ele.key


class ip_addr_map(Hashable):

    def __setitem__(self, key, value):
        self.put(key,value)

    def __getitem__(self, key):
        if key not in self:
            return None
        else:
            return self.get(key)




class Service:
    def __init__(self):
        self.map=ip_addr_map()
        pass

    def build(self,datas:list):
        """
        :param data:[(ip_1,'addr_1'),(ip_2,'addr_2'),...,(ip_n,'addr_n')]
        :return:
        """
        for data in datas:
            self.add(data)

    def add(self,data:tuple):
        """
        单例添加
        :param data:
        :return:
        """
        self.map[data[0]]=data[1]

    def query(self,ip:str)->str:
        """
        查询接口
        :param ip:
        :return:
        """
        return self.map[ip]





if __name__ == '__main__':
    # 测试数据
    datas=[("172.16.254.1",'A省A市A区A街道'),
           ("172.16.254.2",'B省B市B区B街道')]

    # 初始化服务
    service=Service()

    # 建立索引
    service.build(datas)

    # 查询
    print(service.query('172.16.254.1'))
