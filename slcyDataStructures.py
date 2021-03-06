# Python 2.7.1

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
    def __init__(self, datalist=[]): # init with list of dicts
        self.list = datalist
    def len(self):
        """Returns the number of data entries
        ex. L = Dataset.len()"""
        return len(self.list)
    def __len__(self): # overload len() function
        return self.len()
    def dim(self):
        """Returns the number of keys in the first data entry
        ex. D = Dataset.dim()"""
        if self.len() > 0:
            return len(self.list[0])
    def exportdataraw(self, file='dataraw.txt'):
        """Exports the dataset as a raw text string
        ex. Dataset.exportdataraw('rawtext.txt')"""
        with open(file,'w') as f:
            f.write(str(self.list))
    def exportdatasheet(self, file='datasheet.txt'):
        """Exports the dataset as a tab-separated format, suitable for pasting into a spreadsheet
        ex. Dataset.exportdatasheet('datasheet.txt')"""
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
    def importdataraw(self, file='dataraw.txt'):
        """Imports a dataset from a raw text string file
        ex. Dataset.importdataraw('dataraw.txt')"""
        with open(file,encoding='utf8') as f:
            text = f.read()
        self.list = []
        items = text.split('}, {')
        #print('split input into',len(items),'items:',items)
        for i in items:
            #print('processing item:',i)
            for c in "[]{}'":
                i = i.replace(c,'')
            #print('finished processing item:',i)
            elements = i.split(', ')
            t = {}
            for e in elements:
                #print('processing element:',e)
                k,v = e.split(': ')
                try:
                    v = float(v)
                except:
                    pass
                t[k] = v
            self.list.append(t)
    def plot2d(self, keyx, keyy, title=''):
        """Generates a 2d plot of data by key
        ex. Dataset.plot2d('time', 'position', 'Position vs Time')"""
        x = [i[keyx] for i in self.list]
        y = [i[keyy] for i in self.list]
        if title == '':
            title = keyy + ' vs ' + keyx
        plot2d(x, y, xlabel = keyx, ylabel = keyy, title = title)
    def plot3d(self, keyx, keyy, keyz, title=''):
        """Generates a 3d plot of data by key
        ex. Dataset.plot3d('time', 'height', 'distance', 'Location by Time')"""
        x = [i[keyx] for i in self.list]
        y = [i[keyy] for i in self.list]
        z = [i[keyz] for i in self.list]
        if title == '':
            title = keyz + ' vs ' + keyy + ' vs ' + keyx
        plot3d(x, y, z, xlabel = keyx, ylabel = keyy, zlabel = keyz, title = title)
    def max(self,key):
        """Returns the entry with the maximum value of the selected key
        ex. M = Dataset.max('temp')"""
        o = self.list[0]
        for i in self.list:
            if i[key] > o[key]:
                o = i
        return o
    def min(self,key):
        """Returns the entry with the minimum value of the selected key
        ex. N = Dataset.min('temp')"""
        o = self.list[0]
        for i in self.list:
            if i[key] < o[key]:
                o = i
        return o
    def mean(self,key):
        """Returns the mean value of the selected key
        ex. A = Dataset.mean('temp')"""
        s = self.sublist(key)
        return sum(s) / len(s)
    def linearmap(self, oldkey, newkey, r1, r2):
        """Maps values of key in range r1 to range r2 using a linear transformation
        ex. Dataset.linearmap('radians', 'degrees', [0,3.1415], [0,180])"""
        r1n, r1x = r1
        r2n, r2x = r2
        d1 = r1x - r1n
        d2 = r2x - r2n
        # return ((n - r1n) * (d2 / d1)) + r2n
        fprestring = '(('
        fpoststring = ' - ' + str(r1n) + ') * (' + str(d2) + ' / ' + str(d1) +')) + '+ str(r2n)
        self.addcalc(newkey, oldkey, fprestring, fpoststring)
    def calcsd(self, key):
        """Adds SD calculation based on specified key
        ex. Dataset.calcsd('measurement')"""
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
    def calcdelta(self, key):
        """Adds delta calculation of specified key
        delta = abs(value - mean)
        ex. Dataset.calcdelta('distance')"""
        mean = self.mean(key)
        self.addcalc(key + '_delta', key, 'abs(', '-' + str(mean) + ')')
    def renamekey(self, oldkey, newkey):
        """Renames a key
        ex. Dataset.renamekey('time', 't')"""
        for i in self.list:
            i[newkey] = i[oldkey]
            i.pop(oldkey)
    def copy(self):
        """Returns a new copy of this Dataset
        ex. D = Dataset.copy()"""
        c = Dataset()
        for i in self.list:
            c.append(i)
        return c
    def add(self, **data):
        """Adds a data element to the set
        ex. Dataset.add(time = 2, loc = 52)"""
        self.list.append(data)
    def addcalc(self, newkey, oldkey, precalc='', postcalc=''):
        """Adds a key to existing items based on existing keys
        ex. Dataset.addcalc('tplusonesquared', 't', '(', '+1)**2')"""
        for i in self.list:
            i[newkey] = eval(precalc+str(i[oldkey])+postcalc)
    def append(self, data):
        """Appends data to the set
        ex. Dataset.append({'time':2, 'loc':52})
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
    def removeitems(self, **conditions):
        """Removes data elements from the set meeting criteria
        ex. Dataset.remove(time='>1', 'loc'='==50')
        Multiple conditions are AND gated, call function again for OR usage"""
        for i in self.list:
            for c in conditions:
                rem = False
                if eval(str(i[c])+conditions[c]):
                    rem = True
            if rem:
                self.list.remove(i)
    def removekeys(self, *keys):
        """Removes specified keys from data elements
        ex. Dataset.remove('time')"""
        for k in keys:
            for i in self.list:
                i.pop(k)
    def subset(self, *keys):
        """Returns a subset of this dataset containing the requested keys
        ex. L = Dataset.subset('loc')"""
        o = []
        for i in self.list:
            d = {}
            for k in keys:
                d[k] = i[k]
            o.append(d)
        return Dataset(o)
    def sublist(self, key):
        """Returns a list of the requested key values
        ex. L = Dataset.sublist('loc')"""
        o = []
        for i in self.list:
            o.append(i[key])
        return o
    def getkeys(self):
        """Returns a list of keys in the set
        ex. K = Dataset.getkeys()"""
        return list(self.list[0].keys())
    def prnt(self, *keys):
        """Prints the contents of the dataset, optionally only certain keys
        ex. Dataset.prnt()
        ex. Dataset.prnt('time', 'position')"""
        if len(keys) > 0:
            for i in self.list:
                firstkey = True
                sys.stdout.write('{',end='')
                for k in keys:
                    if firstkey:
                        sys.stdout.write("'"+str(k)+"'"+': '+str(i[k]),end='') # appears like a dict object
                        firstkey = False
                    else:
                        sys.stdout.write(',',"'"+str(k)+"'"+': '+str(i[k]),end='')
                print('}')
        else:
            for i in self.list:
                print(i)

def DatasetDemo():
    d = Dataset([{'time':0,'x':8,'y':4}])
    d.add(time=1,x=2,y=3)
    d.add(time=2,x=1,y=4)
    d.add(time=3,x=5,y=0)
    d.prnt()
    d.removeitems(time='>1',x='<3')
    print('remove time>1 AND x<3')
    print('add time squared')
    d.addcalc('timesquared','time','','**2')
    d.addcalc('justone','time','1+0*','')
    d.calcsd('x')
    d.prnt()
    return d
d = DatasetDemo()
