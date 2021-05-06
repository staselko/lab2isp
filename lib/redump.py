# #!/usr/bin/env python
# import argparse
# import Serializer


# def redump(inf, outf, outform):
#     if inf.endswith('.json') and outform == 'JSON':
#         pass
#     elif inf.endswith('.yaml') and outform == 'YAML':
#         pass
#     elif inf.endswith('.pkl') and outform == 'PICKLE':
#         pass
#     else:
#         serial = Serializer.Serializer()
#         if inf.endswith('.json'):
#             serial.form = 'JSON'
#         elif inf.endswith('.yaml'):
#             serial.form = 'Yaml'
#         elif inf.endswith('.pkl'):
#             serial.form = 'Pickle'
#         serial.load(inf, False)
#         data = serial.data
#         serial.change_form(outform)
#         serial.data = data
#         serial.dump(outf, False)


# parser = argparse.ArgumentParser(description='Parser')
# parser.add_argument('inf', type=str, help='Input file')
# parser.add_argument('outf', type=str, help='Output file')
# parser.add_argument('outform', type=str, help='Output format')
# args = parser.parse_args()

# redump(args.inf, args.outf, args.outform)
