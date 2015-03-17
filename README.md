# DataSize
Python integer subclass to handle arithmetic and formatting of integers with data size units

Provides parsing, arithmetic and comparison oprations, and formatting of human readable data size strings for logic that depends on comparisons of values given in common units of data allocation. There are other solutions, but they are either not complete, or too heavy or awkward for casual use. A string like "14GiB" is really an integer representing a data allocation. 

DataSize supports metric and IEC units in both bits and bytes and nonstandard abbreviated IEC units (for legacy Java -Xmx). There is support for variable word-lengths, but because I thought it would get confusing, converting between two different word lengths is not supported. The word length constructor keyword argument will allow converting counts of weird (actually non-byte) word or symbol bit lengths to bit rates, which can then be explicitly converted to standard 8-bit bytes.

The really sweet feature that everyone should love is the Python string.format() support!
```
Help on method __format__ in module datasize.DataSize:

__format__(self, code) unbound datasize.__data_size__.DataSize method
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
>>> from datasize import DataSize
>>> 'My new {0:GB} SSD really only stores {1:.2GiB} of data.'.format(DataSize('750GB'),data_size(DataSize('750GB') * 0.8))
'My new 750GB SSD really only stores 558.79GiB of data.'
>>>
```
