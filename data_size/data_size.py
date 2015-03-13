class data_size(int):
    '''Integer subclass that handles units appropriate for data allocation.
    Adapts popular string representations of data sizes to integer values
    supporting arithmetic and alternate string representations.
    Internally represents data amounts as an integer count of bytes.
    Parses strings given as constructor values, and also provides
    string.format() support for human-readable data quantities expressed
      in metric and IEC unit multiples of 
        bytes: (suffix ending in 'B') or 
        bits: (suffix ending in 'b')
      like 10.4TB or 128kb
    The minimum granularity is in bytes, defined as 8 bit words by default.
    
    Arithemtic methods inherit directly from int, and return int. This
      keeps this class smaller, and avoids unecessary constructor overhead.
    '''
    word_length = 8 #defaults to octet = byte for conversion to/from bits
    bit_suffix, byte_suffix = 'b','B'
    metric_prefixes = {
        # metric/decimal unit prefixes
        'k' : 1000,
        'M' : 1000**2,
        'G' : 1000**3,
        'T' : 1000**4,
        'P' : 1000**5,
        'E' : 1000**6,
        'Z' : 1000**7,
        'Y' : 1000**8,
        }
    IEC_prefixes = {
        # binary IEC unit prefixes
        'ki': 1024,
        'Mi': 1024**2,
        'Gi': 1024**3,
        'Ti': 1024**4,
        'Pi': 1024**5,
        'Ei': 1024**6,
        'Zi': 1024**7,
        'Yi': 1024**8,
        }
    nonstandard_prefixes = dict(zip((k[0] for k in IEC_prefixes.keys()),(m for m in IEC_prefixes.values())))
    unit_prefixes = metric_prefixes.copy()
    unit_prefixes.update(IEC_prefixes)
    # also make a map from unit denominations to prefix
    prefix_units = dict(zip( tuple(unit_prefixes.values()),tuple(unit_prefixes.keys())) )
    nonstandard_units = dict(zip((m for m in IEC_prefixes.values()),(k[0] for k in IEC_prefixes.keys())))
    def __bits_to_bytes__(self,b):
        B = round(b/self.word_length)
        if b % self.word_length > 0:
            B += 1
        return int(B)
    def __init__(self,spec,**kwargs):
        '''Usage: 
        min_heap = data_size('768Mib')
        max_heap = data_size('2G')
        max_heap - min_heap = high_memory_warning_limit
        sys_mem = data_size('16GiB')
        disk_sz = data_size('650GB')
        baud = data_size('25Mb')

        Optional keyword argument 'word_length' can be used
        to specify some other bits per byte than the default of 8.
        '''
        if 'word_length' in kwargs:
            self.word_length = int(kwargs['word_length'])
    def __new__(subclass,spec, **kwargs):
        '''Because data_size is a subclass of int, we must override __new__()
        to implement a string decoder that can provide an immutable integer value
        for instances.
        '''
        if 'word_length' in kwargs:
            word_length = int(kwargs['word_length'])
        else:
            word_length = data_size.word_length
        unit = 'bytes'
        multiple = 1
        try:
            raw = spec[:]
            if raw[-1] == data_size.bit_suffix:
                unit = 'bits'
            raw = raw.rstrip(data_size.bit_suffix).rstrip(data_size.byte_suffix)
            units = [unit for unit in data_size.unit_prefixes.keys()]
            units.sort(reverse=True)
            for prefix in units:
                offset = len(prefix)
                if raw[-offset:] == prefix:
                    raw = raw[:-offset]
                    multiple = data_size.unit_prefixes[prefix]
                    break
        except TypeError:
            raw = strip(spec)
            bits = bytes * word_length
        raw_number = float(raw)
        if unit == 'bits':
            bits = raw_number * multiple
        else:
            bits = raw_number * word_length * multiple
        value = data_size.__bits_to_bytes__(data_size,bits)
        return int.__new__(subclass,round(float(value + 0.5)))
    def __format__(self, code):
        '''formats as a decimal number, but recognizes data units as type format codes.
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
        '''
        base_unit = ''
        prefix = ''
        denomination = 1
        multiple = 1
        auto_modes = ('a','A')
        prefix_units = self.prefix_units
        if not code or code[-1] == 'a':
            fmt_mode = 'a'
        else:
            if code[-1] == 'A':
                fmt_mode = 'A'
                base_unit = ''
            else:
                fmt_mode = None

        if fmt_mode in auto_modes: # automatically choose a denomination/unit
            if fmt_mode == 'A':
                prefix_units = self.nonstandard_units
            code = code.rstrip(''.join(auto_modes))
            denominations = list(prefix_units.keys())
            denominations.sort(reverse=True)
            for quantity in denominations:
                if self * multiple >= quantity:
                    prefix = prefix_units[quantity]
                    denomination = quantity
                    break
        else:
            if code[-1] in ('b','B'):
                base_unit = code[-1]
                code = code[:-1] #eat the base unit
                if base_unit == 'b':
                    multiple = self.word_length
            
            units = list(self.unit_prefixes.keys())
            units.sort(reverse=True)
            for prefix in units:
                offset = len(prefix)
                if code[-offset:] == prefix:
                    code = code[:-offset]
                    denomination = self.unit_prefixes[prefix]
                    break
        print("denomination: {0}\nbase_unit: {1}\nfmt_mode: {2}".format(denomination,base_unit,fmt_mode))
        if denomination > 1 and not base_unit and fmt_mode != 'A':
            base_unit = 'B'
        value = float(self * multiple)/float(denomination)
        
        if value.is_integer(): # emit integers if we can do it cleanly
            code += 'd'
            cast = lambda x:int(x)
            code = code.split('.',1)[0] # if there is precision in the code, strip it`
        else:
            code += 'f'
            cast = lambda x: x
        format_parms = {'code': code, 'unit': prefix + base_unit}
        template = '{{:{code}}}{unit}'.format(**format_parms)
        return template.format(cast(float(value)))

