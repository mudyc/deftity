# (c): <Unknown author>  modified by Matti J. Katila
#
# Reloads modules again,
# see http://pyunit.sourceforge.net/notes/reloading.html
# for details.
# (there was also a version wich didn't work out - a tag __do_not_reload__)
# 


import sys, __builtin__

class RollbackImporter:
    def __init__(self):
        "Creates an instance and installs as the global importer"
        self.previousModules = sys.modules.copy()
        self.realImport = __builtin__.__import__
        __builtin__.__import__ = self._import
        self.newModules = {}
        
    def _import(self, name, globals=None, locals=None, fromlist=[], level=-1):
        result = apply(self.realImport, (name, globals, locals, fromlist))
        self.newModules[name] = 1
        return result
        
    def reinit(self):
        for modname in self.newModules.keys():
            if not self.previousModules.has_key(modname):
                # Force reload when modname next imported
                #print 'delete', modname
                del(sys.modules[modname])
        self.newModules = {}
        #__builtin__.__import__ = self.realImport



