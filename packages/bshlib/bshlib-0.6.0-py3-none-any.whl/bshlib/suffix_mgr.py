from itertools import groupby
import re
from dataclasses import dataclass

sfx_rx = re.compile(r'(.+)_(\d+)$', re.MULTILINE)

def is_suffix(_id):
    """
    Whether ID Has suffix.

    Parameters
    -----
    _id : str
        ID to examine.

    Returns
    -----
    bool
        Whether ID Has suffix.
    """
    m = sfx_rx.match(_id)
    if m:
        return True
    else:
        return False

def extract_name(_id):
    """
    Extract `name` from `suffix id`.

    Parameters
    -----
    _id
        ID.

    Returns
    -----
    str
        Name
    """
    return sfx_rx.match(_id).group(1)

def extract_num(_id):
    """
    Extract number from `suffix id`.

    Parameters
    -----
    _id
        ID.

    Returns
    -----
    int
        Number
    """
    return int(sfx_rx.match(_id).group(2))

@dataclass
class ObjId[T]:
    """
    Bundles together an object reference and its identifier.

    String IDs cannot be traced back to the associated object after modification. This way, we mantain the relation.
    """
    obj: T
    """Object"""
    id: str
    """Id"""

class SuffixMgr[T]:
    """
    Receives a list of object-ID bundles and keeps the IDs accordant to a suffix convention.

    Glossary
    -----
    - `ID` : a string for identifying an object.
    - `basic id` : an ID with no suffix.
    - `suffix id` : an ID with a suffix.
    - `register` : the "basic" set and the `sequence` mapping.
    - `name` : non-suffix part of an ID.
    - `bundle` : object that associates an object with an ID.
    - `collection` : list of object-ID bundles.
    - `sequence` : IDs related to a `name`.
    - `sequence pointer` : the current (last) suffix number in a `sequence`.

    Info
    -----
    Keeps a register with the `basic id`s and another with the `suffix id`s and their current sequence.

    `basic id` are suffixed with a number from the end of the sequence, so they end up being the latest in the `collection`.

    Other
    -----
    Also handles adding new items, getting ID from object, getting all IDs from a `name`, etc.

    Usage
    -----
    Instantiate by bundling together every object with its ID.

    Example
    -----
    Create class `CreditCard`, create instances and bundle them with an ID, then pass it to `SuffixMgr` constructor.

    >>> from dataclasses import dataclass
    >>>
    >>> @dataclass
    >>> class CreditCard:
    >>> bank: str
    >>> number: str
    >>> balance: float
    >>>
    >>> bundle_ls = [
    >>>     ObjId(CreditCard('Banco Santander', '1231241243', 500.2), 'santander'),
    >>>     ObjId(CreditCard('Banco Santander', '5643373368', 1.0), 'santander'),
    >>>     ObjId(CreditCard('UniCredit', '9996431232', 12.0), 'unicredit_554'),
    >>>     ObjId(CreditCard('Banco Santander', '0500055441', 0.0), 'santander_21')
    >>> ]
    >>> sfm = SuffixMgr(bundle_ls)
    """
    all: list[ObjId[T]]
    """`collection`"""
    basic: set[str]
    """IDs with no suffix"""
    map: dict[str, list[int]]
    """`sequence` table"""

    def __init__(self, ls: list[ObjId[T]]):
        self.all = ls
        self.__compile()
        self.__rearrange()

    def __compile(self):
        """
        Compile register.

        Returns
        -----
        None
        """
        def name(i: ObjId[T]):
            m = sfx_rx.match(i.id)
            if m:
                return m.group(1)
            else:
                return ''

        def piece(i: ObjId[T]):
            return int(sfx_rx.match(i.id).group(2))

        basic: list[str] = []
        sfx_map: dict[str, list[int]] = {}
        _sorted = sorted(self.all, key=name)
        for k, g in groupby(_sorted, key=name):
            if k == '':
                basic.extend([p.id for p in g])
            else:
                sfx_map[k] = sorted([piece(i) for i in g])
        self.basic = set(basic)
        self.map = sfx_map

    def find(self, _id):
        """
        Fetch `bundle` with ID.

        Parameters
        -----
        _id : str
            ID to use for finding.

        Returns
        -----
        ObjId[T]
            `bundle`
        """
        try:
            return [p for p in self.all if p.id == _id][0]
        except IndexError:
            raise RuntimeError('name not found')

    def get(self, obj):
        """
        Fetch `bundle` with object.

        Parameters
        -----
        obj : T
            Object to use for finding.

        Returns
        -----
        ObjId[T]
            `bundle`
        """
        try:
            return [p for p in self.all if p.obj is obj][0]
        except IndexError:
            raise RuntimeError('object not found')

    def find_base(self, name):
        """
        Retrieve all `bundle` which ID share a `name`.

        Parameters
        -----
        name : str
            Name to use for finding.

        Returns
        -----
        list[ObjId[T]]
            `bundle` list
        """
        if name in self.basic:
            return [self.find(name)]
        elif name in self.map.keys():
            return [self.find(f'{name}_{n}') for n in self.map[name]]
        else:
            raise RuntimeError('no match')

    def __repl_by_id(self, _id, new_id):
        """
        Replace ID with a new one.

        Parameters
        -----
        _id : str
            ID to use for finding.
        new_id : str
            New ID.

        Returns
        -----
        None
        """
        self.find(_id).id = new_id

    def __repl_by_obj(self, obj, new_id):
        """
        Replace ID with a new one.

        Parameters
        -----
        obj : T
            Object to use for finding.
        new_id : str
            New ID.

        Returns
        -----
        None
        """
        self.get(obj).id = new_id

    def add(self, item):
        """
        Add new item to the `collection`.

        Parameters
        -----
        item : ObjId[T]
            `bundle` to add. The ID attribute has to be a `basic id`.

        Returns
        -----
        None
        """
        if item.id in self.basic:
            self.__repl_by_id(item.id, f'{item.id}_0')
            self.all.append(ObjId(item.obj, f'{item.id}_1'))
        elif item.id in self.map.keys():
            self.all.append(ObjId(item.obj, f'{item.id}_{self.__num(item.id)+1}'))
        else:
            self.all.append(item)
        self.__compile()

    def sequence_pointer(self, name):
        """
        Get `sequence pointer` for `name`.

        Returns `None` if the name is new.

        Returns 0 if the name exists only once as a `basic id`.

        Return any other number if the name was part of a sequence.

        Parameters
        -----
        name : str
            `name` to look up.

        Returns
        -----
        int or None
            `sequence pointer`.
        """
        if name in self.basic:
            return 0
        elif name in self.map.keys():
            return self.__num(name)
        else:
            return None

    def __num(self, name):
        """
        Get `sequence pointer` for `name`.

        Parameters
        -----
        name : str
            Name to look up.

        Returns
        -----
        int
            `sequence pointer`
        """
        return max(self.map[name])

    def list_suffixed(self):
        """
        List the `bundle` which ID is a `suffix id`.

        Returns
        -----
        list[ObjId[T]]
            `bundle` list
        """
        return [p for p in self.all if p.id not in self.basic]

    def list_basic(self):
        """
        List the `bundle` which ID is a `basic id`.

        Returns
        -----
        list[ObjId[T]]
            `bundle` list
        """
        return [p for p in self.all if p.id in self.basic]

    def __rearrange(self):
        """
        Rearrange `collection` to keep it well formed.

        Returns
        -----
        None
        """
        # fix strays
        stray = [p for p in self.all if not is_suffix(p.id) and p.id in self.map.keys()]
        for p in stray:
            old_id = p.id
            new_n = self.__num(p.id) + 1
            self.__repl_by_obj(p.obj, f'{p.id}_{new_n}')
            # quick update to avoid having to compile
            self.map[old_id].append(new_n)
        self.__compile()

        # re-sequence the suffixes
        for name, nums in self.map.items():
            c = 0
            for n in nums:
                self.__repl_by_id(f'{name}_{n}', f'{name}_{c}')
                c += 1
        self.__compile()

        # suffix the basics
        for name in self.basic:
            matches = [p for p in self.all if p.id == name]
            count = len(matches)
            if count > 1:
                for p, n in zip(matches, range(count)):
                    p.id = f'{p.id}_{n}'
        self.__compile()
