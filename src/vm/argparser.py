from argparse import ArgumentParser

def parseArgs():
   '''Parse command line arguments with argparse module.'''
   parser = ArgumentParser()
   parser.add_argument('--debug', action='store_true', default=False)
   parser.add_argument('filename', action='store')

   return parser.parse_args()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
