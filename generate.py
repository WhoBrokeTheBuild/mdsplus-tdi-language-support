
import csv
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '--opcodes',
    required=True,
    help='Path to opcodes.csv'
)

args = parser.parse_args()

opcodes_filename = args.opcodes

opcodes_file = open(opcodes_filename, newline='')
reader = csv.DictReader(opcodes_file)

keywords = {}
for line in reader:
    regex = line['builtin'].replace('$', '\\$')
    builtin = line['builtin'].lower()
    f1 = line['f1'].lower()
    max_args = int(line['m2'].split('+')[0])

    group = 'keyword.control'

    if builtin in ['public', 'optional', 'in', 'out', 'as_is']:
        group = 'storage.modifier'
    elif builtin in ['if', 'if_error', 'else', 'not', 'for', 'while', 'return', 'break', 'continue', 'switch', 'case']:
        group = 'keyword.control'
    elif f1 in ['constant', 'value', '$this']:
        group = 'constant.language'
    elif max_args > 0:
        group = 'support.function'

    group += '.mdsplus-tdi'
    if group not in keywords:
        keywords[group] = []
    keywords[group].append(regex)


syntax_filename = 'syntaxes/mdsplus-tdi.tmLanguage.json'

syntax_file = open(syntax_filename, 'r')
syntax = json.load(syntax_file)

keyword_patterns = []
for name, match in keywords.items():

    if name.startswith('constant.language'):
        match = '(?i)(' + '|'.join(match) + ')'
    else:
        match = '(?i)\\b(' + '|'.join(match) + ')\\b'

    keyword_patterns.append({
        'name': name,
        'match': match,
    })

syntax['repository']['keywords']['patterns'] = keyword_patterns

file = open(syntax_filename, 'w')
json.dump(syntax, file, indent=4)