class Dataset():
    """List of dicts containing any desired keys
    ex = Dataset([{'time':0,'loc':45}, {'time':1,'loc':48}])"""
    def __init__(self, datalist=[]) -> None: # init with list of dicts
        self.list = datalist
    def len(self) -> int:
        """Returns the number of data entries"""
        return len(self.list)
    def __len__(self) -> int: # overload len() function
        return self.len()
    def dim(self) -> int:
        """Returns the number of keys in the first data entry"""
        if self.len() > 0:
            return len(self.list[0])
    def max(self,key) -> float:
        """Returns the entry with the maximum value of the selected key"""
        o = self.list[0]
        for i in self.list:
            if i[key] > o[key]:
                o = i
        return o
    def min(self,key) -> float:
        """Returns the entry with the minimum value of the selected key"""
        o = self.list[0]
        for i in self.list:
            if i[key] < o[key]:
                o = i
        return o
    def mean(self,key) -> float:
        """Returns the mean value of the selected key"""
        s = self.sublist(key)
        return sum(s) / len(s)
    def calcsd(self, key) -> None:
        """Adds SD calculation based on specified key"""
        mean = self.mean(key)
        va = []
        for i in self.list:
            va.append((i[key] - mean) ** 2)
        var = 0
        for v in va:
            var += v
        var = var / len(va)
        sd = var ** (1/2)
        self.__sd__ = sd
        self.addcalc(key + '_sd', key, '(', '-' + str(mean) + ')/' + str(sd))
    def calcdelta(self, key) -> None:
        """Adds delta calculation of specified key
        delta = abs(value - mean)
        """
        mean = self.mean(key)
        self.addcalc(key + '_delta', key, 'abs(', '-' + str(mean) + ')')
    def renamekey(self, oldkey, newkey) -> None:
        """Renames a key
        ex.renamekey('time', 't')"""
        for i in self.list:
            i[newkey] = i[oldkey]
            i.pop(oldkey)
    def copy(self) -> 'Dataset':
        """Returns a new copy of this Dataset"""
        c = Dataset()
        for i in self.list:
            c.append(i)
        return c
    def add(self, **data) -> None:
        """Adds a data element to the set
        ex.add(time = 2, loc = 52)"""
        self.list.append(data)
    def addcalc(self, newkey, oldkey, precalc='', postcalc='') -> None:
        """Adds a key to existing items based on existing keys
        ex.addcalc('tplusonesquared', 't', '+1)**2', '(')"""
        for i in self.list:
            i[newkey] = eval(precalc+str(i[oldkey])+postcalc)
    def append(self, data) -> None:
        """Appends data to the set
        ex.append({'time':2, 'loc':52})
        Accepts other Dataset objects, dict objects, or lists of dict objects"""
        if type(data) is Dataset:
            self.append(data.list)
        elif type(data) is list:
            for i in data:
                self.list.append(i)
        elif type(data) is dict:
            self.list.append(data)
        else:
            print('Invalid data type supplied. Accepts Dataset, dict, or list of dicts.')
    def removeitems(self, **conditions) -> None:
        """Removes data elements from the set meeting criteria
        ex.remove(time='>1', 'loc'='==50')
        Multiple conditions are AND gated, call function again for OR usage"""
        for i in self.list:
            for c in conditions:
                rem = False
                if eval(str(i[c])+conditions[c]):
                    rem = True
            if rem:
                self.list.remove(i)
    def removekeys(self, *keys) -> None:
        """Removes specified keys from data elements
        ex.remove('time')"""
        for k in keys:
            for i in self.list:
                i.pop(k)
    def subset(self, *keys) -> 'Dataset':
        """Returns a subset of this dataset containing the requested keys
        locs = ex.subset('loc')"""
        o = []
        for i in self.list:
            d = {}
            for k in keys:
                d[k] = i[k]
            o.append(d)
        return Dataset(o)
    def sublist(self, key) -> list:
        """Returns a list of the requested key values
        locs = ex.subset('loc')"""
        o = []
        for i in self.list:
            o.append(i[key])
        return o
    def getkeys(self) -> list:
        """Returns a list of keys in the set"""
        return list(self.list[0].keys())
    def print(self, *keys) -> None:
        """Prints the contents of the dataset, optionally only certain keys
        ex.print('time')"""
        if len(keys) > 0:
            for i in self.list:
                firstkey = True
                print('{',end='')
                for k in keys:
                    if firstkey:
                        print("'"+str(k)+"'"+': '+str(i[k]),end='') # appears like a dict object
                        firstkey = False
                    else:
                        print(',',"'"+str(k)+"'"+': '+str(i[k]),end='')
                print('}')
        else:
            for i in self.list:
                print(i)

def DatasetDemo():
    d = Dataset([{'time':0,'x':8,'y':4}])
    d.add(time=1,x=2,y=3)
    d.add(time=2,x=1,y=4)
    d.add(time=3,x=5,y=0)
    d.print()
    d.removeitems(time='>1',x='<3')
    print('remove time>1 AND x<3')
    print('add time squared')
    d.addcalc('timesquared','time','','**2')
    d.addcalc('justone','time','1+0*','')
    d.calcsd('x')
    d.print()
    return d
#d = DatasetDemo()
