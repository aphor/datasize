# data_size
Python integer subclass to handle arithmetic and formatting of integers with data size units

I need this class to provide parsing, arithmetic and comparison oprations, and formatting of human readable data size strings for some Salt states I am writing. I found some other solutions, but they were either not complete, too heavy or awkward to use. A string like "14GiB" is really an integer representing a data allocation.

There is support for metric and IEC units in both bits and bytes and nonstandard abbreviated IEC units (for legacy Java -Xmx). There is support for variable word-lengths, but because I thought it would get confusing, converting between two different word lengths is not supported. The word length constructor keyword argument will allow converting counts of weird (actually non-byte) word or symbol bit lengths to bit rates, which can then be explicitly converted to standard 8-bit bytes.

The really sweet feature that everyone (now everybody's me!) should love is the Python 3 string.format() support!
```
Help on method __format__ in module data_size.data_size:

__format__(self, code) unbound data_size.data_size.data_size method
    formats as a decimal number, but recognizes data units as type format codes.
    Precision is ignored for integer multiples of the unit specified in the format code.
    format codes:  
    a    autoformat will choose a unit defaulting to the largest
          size with a quantity >= 1 (default)
    A    abbreviated number of bytes (implied IEC units, and implied 'B' bytes suffix omitted)
    B    bytes      (1)
    kiB  kibibytes  (1024)
    kB   kilobytes  (1000)
    ...
    GiB  Gibibytes  (1024**3)
    GB   Gigabytes  (10**9)
    ...
    YiB  Yobibytes  (1024**8)
    YB   Yottabytes (10**24)
```
```
>>> from data_size_lib import data_size
>>> 'My new {0:GB} SSD really only stores {1:.2GiB} of data.'.format(data_size('750GB'),data_size(data_size('750GB') * 0.8))
'My new 750GB SSD really only stores 558.79GiB of data.'
>>>
```
