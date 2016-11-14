class Dataset():
    """---
    List container with some basic number analysis
    ---
    data <list>
    """
    def __init__(self, data):
        self.data = data
    def add(self,data) -> None: #create .add() function
        for d in data:
            self.data.append(d)
    def append(self,data) -> None: #extend .append() function
        self.data.append(data)
    def __add__(self,data) -> None: #overload + operator
        self.data.append(data)
    def __len__(self) -> int: #overload len() function
        return len(self.data)
    def __max__(self) -> float: #overload max() function
        return max(self.data)
    def __min__(self) -> float: #overload min() function
        return min(self.data)
    def tostring(self) -> str: #add tostring() function
        sl = []
        for d in self.data:
            sl.append(str(d))
            sl.append('\n')
        return ''.join(sl)
    def print(self) -> None: #add print() function
        print(self.tostring())
    def avg(self) -> float:
        """Returns the average of the data contained"""
        return sum(self.data)/len(self.data)
    def sd(self) -> float:
        """Returns 1 SD of the data contained"""
        avg = self.avg()
        va = []
        for d in self.data:
            va.append((d - avg) ** 2)
        var = 0
        for v in va:
            var += v
        var = var / len(va)
        return var ** (1/2)
    def removeoutliers(self, c=1) -> 'Dataset':
        """Returns a new Dataset, excluding any data points +- c standard deviations
        [c] <int>
        """
        avg = self.avg()
        sd = self.sd()
        new = []
        for d in self.data:
            if abs(d-avg) < sd:
                new.append(d)
        return Dataset(new)
