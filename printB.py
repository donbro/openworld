

def printB(label,b,add=[],subtract=[],only=[], all_names=False):
    """printB("App", NSApp(), add=['mainWindow'])"""
    
    s4 = "    "
    s3 = "   "
    print
    print "--------------\n\n"+s4+label
    print "\n"+s3+repr( b) # , type(b)

    obj=b
    print_setters(obj, add=add,subtract=subtract,only=only, all_names=all_names)
    
def xx(obj):
    return [ k for k in obj.__dict__.keys() if ( k[-1]!='_') and ( k[-1]!=':') ]    
    
def print_setters(obj, add=[],subtract=[],only=[],all_names=False):


    if all_names:
    
        mro = [obj] + list(obj.__class__.__mro__ )
        mro.reverse()       # reverse in place
    
        print
        for cls in mro:
            if hasattr(cls , "__dict__" ):
                rt = repr(cls)
                if  'class NIL' in rt or "type 'object'" in rt or "class NSObject" in rt:
                    pass
                else:

                    print rt
                    print
                    # print obj.allPropertyKeys()
                    # print
                    print xx(cls)
                    print
        
        return
        
    
    s4 = "    "

    if all_names:
        

        names_list = [(k,v) for (k, v) in obj.__class__.__dict__.items() if  k[-1]!='_' ]
        
        print
        for k,v in sorted( set(names_list) ):
            # try:
                print s4+"%-32s" % k
            # except e:
                # print k, e                # obj-c exceptions don't raise to Python?
                
            # print s4+"%-32s : %r"  % (k, getattr(obj, k)() )
        
    # print "print_setters(obj, add=%r,subtract=%r,only=%r)" % (add,subtract,only)
    
    if len(only) != 0:
        theList = only
        setters = theList
        add = theList
    else:
    
        setters = [k[3:-1].lower() for (k, v) in obj.__class__.__dict__.items() if  k[0:3] == 'set']
    
        theList =  [k for (k, v) in obj.__class__.__dict__.items() if k[-1]!='_' and k[0:3] != 'set']

        theList =  set(theList + add)

        theList =  theList - set(subtract)


    print
    for k in sorted(theList):
        if ((k is not 'canCycle' and  k.lower() in setters ) or k in add ) and  hasattr(obj, k) :
                print s4+"%-32s : %r"  % (k, getattr(obj, k)())


