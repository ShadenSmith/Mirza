class Debuggable(object):
    '''Quick and dirty implementation of debug logging'''
    def __init__(self, prelude="Log", on=False):
        if on:
            def _(msg, *args):
                '''Pass formatted argument so we don't waste time doing
                   string interpolation when we're not going to print'''
                print "%s: %s" % (prelude, msg % args)
            self.debug = _
        else:
            self.debug = lambda *args: None

