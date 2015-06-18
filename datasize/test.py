from datasize.__datasize__ import DataSize

def value_equivalence_check(a,b):
    assert a == b

def string_format_check(a,b,c):
    assert a.format(DataSize(b)) == c

__default_autoformat__ = ' 20.4a'
def test_parse_and_format():
    from datasize.__expected_test_results__ import parse_and_format_results
    for example in parse_and_format_results.keys():
        formatted_string = parse_and_format_results[example]
        parsed_string = '{}{}{}'.format(*example)
        format_code_str ='{{:{}}}'.format(__default_autoformat__)
        yield string_format_check, format_code_str, parsed_string, formatted_string

example_values = (1, 2, 4, 16, 64, 1024, 65536, 0.1, 0.25, 0.125, 56.65)
prefixes = list(DataSize.unit_prefixes.keys())
bases = ('B','b')

if __name__ == '__main__':
    ''' Save the output of this to __expected_test_results__.py to generate
        static test data. Check it manually, and make manual adjustments as necessary
        before running unit tests against it.'''
    print('parse_and_format_results = {')
    for i in [{'n':n,'p':p,'b':b} for n in example_values for p in prefixes for b in bases]:
        i['DS'] = DataSize('{n}{p}{b}'.format(**i))
        fmt_code_str = '"{{DS:{}}}"'.format(__default_autoformat__)
        print('\t'.join(('','({n},','"{p}",','"{b}"):',fmt_code_str,',')).format(**i))
    print('}')
