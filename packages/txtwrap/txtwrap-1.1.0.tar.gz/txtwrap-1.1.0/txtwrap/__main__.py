from argparse import ArgumentParser
from txtwrap import printwrap, shorten

parser = ArgumentParser(
    description='Command-line tool for wrapping, aligning, or shortening text.'
)

parser.add_argument(
    'text',
    type=str,
    help='Text to be wrapped, aligned, or shorted'
)

parser.add_argument(
    '-f', '--fill',
    type=str,
    default=' ',
    metavar='<str 1 length>',
    help='Fill character (default: space)'
)

parser.add_argument(
    '-w', '--width',
    type=int,
    default=None,
    metavar='<number>',
    help='Width of the text wrapping (default: current width terminal or 70)'
)

parser.add_argument(
    '-m', '--method',
    type=str,
    choices={'word', 'mono', 'shorten'},
    default='word',
    metavar='{word|mono|shorten}',
    help='Method to be applied to the text (default: word)'
)

parser.add_argument(
    '-a', '--alignment',
    type=str,
    choices={'left', 'center', 'right', 'fill'},
    default='left',
    metavar='{left|center|right|fill}',
    help='Alignment of the text (default: left)'
)

parser.add_argument(
    '-n', '--neglect-empty',
    action='store_false',
    help='Neglect empty lines in the text'
)

parser.add_argument(
    '-s', '--start',
    type=int,
    default=0,
    metavar='<number>',
    help='start index of the text to be shorten (default: 0)'
)

parser.add_argument(
    '-p', '--placeholder',
    type=str,
    default='...',
    metavar='<str>',
    help='Placeholder to be used when shortening the text (default: ...)'
)

args = parser.parse_args()

if args.method == 'shorten':
    print(shorten(args.text, args.width, args.start, placeholder=args.placeholder))
else:
    printwrap(
        args.text,
        fill=args.fill,
        width=args.width,
        method=args.method,
        alignment=args.alignment,
        preserve_empty=args.neglect_empty
    )