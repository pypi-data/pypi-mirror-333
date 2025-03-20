
class TypeList():
    """
    A list comprised of only type objects

    Args:
        t (type)
        list (list) = []
    """
    def __init__(self, t: type, l: list = []):
        self.t = t
        self.list = l


        for item in l:
            self.__check_for_type__(item)
    
    def __check_for_type__(self, item):
        if not isinstance(item, self.t):
            raise Exception(f"Error: All items of list dont match specifed type '{self.t}'.")

    def append(self, item):
        """
        Add item to end of list

        Args:
            item
        """
        self.__check_for_type__(item)

        self.list.append(item)

    def insert(self, index: int, item):
        """
        Insert item at index

        Args:
            index (int)
            item
        """
        self.__check_for_type__(item)


        self.list.insert(index, item)

    def remove(self, item):
        """
        Remove item

        Args:
            item
        """
        self.__check_for_type__(item)


        self.list.remove(item)

    
    def pop(self, index: int = 0):
        """
        Pop item from list at index

        Args:
            index (int) = 0
        """
        self.list.pop(index)


    def sort(self):
        """
        Sort list
        """
        self.list.sort()
    
    def get(self, index: int):
        """
        Get item at index

        Args:
            index (int)
        """
        return self.list[index]
    

    def reverse(self):
        """
        Reverse list
        """
        self.list.reverse()

    def __repr__(self) -> str:
        return str(self.list)
    
    def __iter__(self):
        return iter(self.list)
    
    def __len__(self):
        return len(self.list)

class StringList(TypeList):
    def __init__(self, l: list = []):
        super().__init__(str, l)

class IntList(TypeList):
    def __init__(self, l: list = []):
        super().__init__(int, l)

class FloatList(TypeList):
    def __init__(self, l: list = []):
        super().__init__(float, l)

class BoolList(TypeList):
    def __init__(self, l: list = []):
        super().__init__(bool, l)

class DictList(TypeList):
    def __init__(self, l: list = []):
        super().__init__(dict, l)