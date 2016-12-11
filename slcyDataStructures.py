import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot2d(x, y, lines=False, xlabel='X', ylabel='Y', title='', color='k', marker = '.'):
    """Creates a 2D scatter or line plot
    x, y <list> or <tuple>
    xlabel, ylabel <str>
    color <str> [krgbcmyw] or '#FFFFFF' or (0:1,0:1,0:1)
    marker <str> [.,ov^<>12348sp*hH+xDd|_]
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if lines:
        ax.plot(x, y, c=color, marker=marker)
    else:
        ax.scatter(x, y, c=color, marker=marker)
    fig.suptitle(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def plot3d(x, y, z, lines=False, xlabel='X', ylabel='Y', zlabel='Z', title='', color='k', marker = '.'):
    """Creates a 3D scatter or line plot
    x, y, z <list> or <tuple>
    xlabel, ylabel, zlabel <str>
    color <str> [krgbcmyw] or '#FFFFFF' or (0:1,0:1,0:1)
    marker <str> [.,ov^<>12348sp*hH+xDd|_]
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if lines:
        ax.plot(x, y, z, c=color, marker=marker)
    else:
        ax.scatter(x, y, z, c=color, marker=marker)
    fig.suptitle(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.show()

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
    def exportdataraw(self, file='temp.data') -> None:
        """Exports the dataset as a raw text string"""
        with open(file,'w') as f:
            f.write(str(self.list))
    def exportdatasheet(self, file='temp2.data') -> None:
        """Exports the dataset as a tab-separated format, suitable for pasting into a spreadsheet"""
        o = ''
        headers = list(self.list[0].keys())
        o += '\t'.join(headers)
        for i in self.list:
            o += '\n'
            for h in headers:
                o += str(i[h]) + '\t'
            o = o[:-1]
        with open(file,'w') as f:
            f.write(o)
    def importdata(self, file='temp.data') -> None:
        """Imports a dataset from a raw text string file"""
        with open(file,encoding='utf8') as f:
            text = f.read()
        self.list = []
        items = text.split('}, {')
        print('split input into',len(items),'items:',items)
        for i in items:
            print('processing item:',i)
            for c in "[]{}'":
                i = i.replace(c,'')
            print('finished processing item:',i)
            elements = i.split(', ')
            t = {}
            for e in elements:
                print('processing element:',e)
                k,v = e.split(': ')
                try:
                    v = float(v)
                except:
                    pass
                t[k] = v
            self.list.append(t)
    def plot2d(self, keyx, keyy, title='') -> None:
        x = [i[keyx] for i in self.list]
        y = [i[keyy] for i in self.list]
        if title == '':
            title = keyy + ' vs ' + keyx
        plot2d(x, y, xlabel = keyx, ylabel = keyy, title = title)
    def plot3d(self, keyx, keyy, keyz, title='') -> None:
        x = [i[keyx] for i in self.list]
        y = [i[keyy] for i in self.list]
        z = [i[keyz] for i in self.list]
        if title == '':
            title = keyz + ' vs ' + keyy + ' vs ' + keyx
        plot3d(x, y, z, xlabel = keyx, ylabel = keyy, zlabel = keyz, title = title)
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
        """Returns the mean value of the selected key
        key <str>"""
        s = self.sublist(key)
        return sum(s) / len(s)
    def linearmap(self, oldkey:str, newkey:str, r1:list, r2:list) -> None:
        """Maps values of key in range r1 to range r2 using a linear transformation
        ex.linearmap('radians', 'degrees', [0,3.1415], [0,180])"""
        r1n, r1x = r1
        r2n, r2x = r2
        d1 = r1x - r1n
        d2 = r2x - r2n
        # return ((n - r1n) * (d2 / d1)) + r2n
        fprestring = '(('
        fpoststring = ' - ' + str(r1n) + ') * (' + str(d2) + ' / ' + str(d1) +')) + '+ str(r2n)
        self.addcalc(newkey, oldkey, fprestring, fpoststring)
    def calcsd(self, key:str) -> None:
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
    def calcdelta(self, key:str) -> None:
        """Adds delta calculation of specified key
        delta = abs(value - mean)"""
        mean = self.mean(key)
        self.addcalc(key + '_delta', key, 'abs(', '-' + str(mean) + ')')
    def renamekey(self, oldkey:str, newkey:str) -> None:
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
d = DatasetDemo()
