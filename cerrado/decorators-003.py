def static(func):
    annotations = func.__annotations__
    code = func.__code__
    argname = code.co_varnames[0]
    argtype = annotations[argname]
    restype = annotations['return']

    def decorated(x):
        if isinstance(x, argtype):
            res = func(x)
            if isinstance(res, restype):
                return res
        raise TypeError
    return decorated


@static
def double(x: float) -> float:
    result: float = x + x
    return result


def get_my_foo_class():
    def __init__(self, x):
        self.data = x

    name = 'Foo'
    bases = ()
    namespace = {'__init__': __init__,
                 'double': lambda self: self.data * 2}

    return my_class


x = get_my_foo(42)
y = get_my_foo(21)


class MySmartInt(int):
    ...


MySmartInt = type('MySmartInt', (int,),
                  {'get_answer': lambda self: 42})

x = MySmartInt()

x.get_answer()


def numbers(a, _, b):
    return range(a, b + 1)


for x in numbers(1, ..., 10):
    print(x)


def clean_ns(dic):
    return {k: v for k, v in dic.items()
            if not k.startswith('_')}


@clean_ns
class NotAClass(metaclass=lambda name, bases, ns: ns):
    x = 1
    y = 1
    fibs = [1]
    for _ in range(10):
        x, y = y, x + y
        fibs.append(y)


from collections import defaultdict, Mapping, MutableMapping
from random import random


class MyDict(MutableMapping):
    def __init__(self, data={}, fset=lambda attr, v: None):
        self._data = {}
        self._data.update(data)
        self._fset = fset

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __delitem__(self, key):
        del self._data[key]

    def __setitem__(self, key, value):
        self._fset(key, value)
        self._data[key] = value

    def __repr__(self):
        return f'MyDict({self._data})'


d = MyDict({'x': 1, 'y': 2}, fset=print)
d['answer'] = 42
d


class Meta(type):
    def __new__(cls, name, base, namespace):
        cleaned = {k: v for k, v in namespace.items()
                   if not k.startswith('_')}
        print(namespace.get('__annotations__'))
        return cleaned

    def __init__(self, name, bases, ns):
        print(f'{name} foi criada')

    def __prepare__(name, bases):
        def on_annotation(name, tt):
            if name in ns:
                value = ns[name]
                if not isinstance(value, tt):
                    raise TypeError(value, tt)
            print(f'{name}:: {tt.__name__}')

        def on_setattr(name, value):
            if name not in annotations:
                annotations[name] = type(value)
            tt = annotations.get(name, object)
            if not isinstance(value, tt):
                raise TypeError(name, value)
            if not name.startswith('_'):
                print(f'{name} = {value!r}')

        annotations = MyDict(fset=on_annotation)
        ns = MyDict({'__annotations__': annotations},
                    fset=on_setattr)
        return ns


from numbers import Number


class FiboDebbugger(metaclass=Meta):
    answer: Number = 42.0
    not_answer: Number = 17

    x, y = 1, 1
    for _ in range(1, 11):
        x, y = y, x + y + 0.1


FiboDebbugger
