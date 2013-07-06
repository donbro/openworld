
all_objs = {}
s4 = "    "
s3 = "   "

def printBX(label,obj,add=[],subtract=[],only=[], all_names=False):
    """printB("App", NSApp(), add=['mainWindow'])"""
    
    if obj not in all_objs:
        print_all_names()
    
    print
    print "--------------\n\n"+s4+label
    print "\n"+s3+repr( b) # , type(b)

    obj=b
    print_setters(obj, add=add,subtract=subtract,only=only, all_names=all_names)
    
    
def cls_repr(cls):

        rt = repr(cls)

        if rt[0] == '<' and rt[-1] == '>':
            rt = rt[1:-1]
        # print "rt is", rt

        rts = rt.split()

        # print "rts is", rts, "rts[0] == 'type' is", rts[0] == 'type'
        
        # print "rts[0:2] is", rts[0:2], "rts[0:2] == ['objective-c', 'class'] is", rts[0:2] == ['objective-c', 'class']
        
         
        rt2 = " ".join(rts[1:-1])
        
        if rt == 'objective-c class NIL':
            pass
       
        elif rts[0] == 'type':
            rt = rts[1]
        elif rts[0:2] == ['objective-c', 'class']:
            rt = "%-8s %-24s %s" % ('class', rts[2], rts[-1][-7:])
        else:
            rt = "%-8s %-24s %s" % ('object', rts[0], rts[-1][-7:])
            
        return rt
    
def obj_attrs0(obj):
    if hasattr(obj , "__dict__" ):
        return sorted([ k for k in obj.__dict__.keys() if ( k[-1]!='_') and ( k[-1]!=':') ]    )
    else:
        print "obj_attrs0: '" + cls_repr(obj.__class__) + "' object has no attribute '__dict__'"
        return []
        
        
    
def obj_all_names(obj):
    
        mro = [obj] + list(obj.__class__.__mro__ )
        mro.reverse()       # reverse in place
    
        print
        for cls in mro:
            if hasattr(cls , "__dict__" ):
                rt = repr(cls)
                if  'class NIL' in rt or "type 'object'" in rt or "class NSObject" in rt:
                    pass
                else:
                    if rt.startswith('<objective-c class '):
                        rt = 'class '+rt[19:-1]

                    print rt
                    print
                    z =  obj.allPropertyKeys()
                    if len(z) > 0:
                        print obj.allPropertyKeys()
                        print
                    print obj_attrs0(cls)
                    print
        
        return
    
    
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
                    if rt.startswith('<objective-c class '):
                        rt = 'class '+rt[19:-1]

                    print rt
                    print
                    z =  obj.allPropertyKeys()
                    if len(z) > 0:
                        print obj.allPropertyKeys()
                        print
                    print obj_attrs0(cls)
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



import unittest

import objc
from Foundation import NSObject, NSRect
from AppKit import NSApplication



my_application_names = [ 'activationPolicy', 'applicationIconImage', 'areCursorRectsEnabled', 'canEnterFullScreenMode', 'completeStateRestoration', 'context', 'contextID', 'currentEvent', 'currentSystemPresentationOptions', 'deactivate', 'dealloc', 'delayWindowOrdering', 'delegate', 'disableAutomaticTermination', 'disableCursorRects', 'disableRelaunchOnLogin', 'dockTile', 'enableAutomaticTermination', 'enableCursorRects', 'enableRelaunchOnLogin', 'enabledRemoteNotificationTypes', 'extendStateRestoration', 'finalize', 'finishLaunching', 'frontWindow', 'gestureEventMask', 'helpMenu', 'init', 'isActive', 'isDefaultHelpBookSearchEnabled', 'isFullKeyboardAccessEnabled', 'isHidden', 'isRunning', 'isSpeaking', 'keyWindow', 'mainMenu', 'mainWindow', 'menu', 'modalWindow', 'orderedDocuments', 'orderedWindows', 'presentationOptions', 'preventWindowOrdering', 'run', 'servicesMenu', 'servicesProvider', 'shouldRestoreStateOnNextLaunch', 'stopModal', 'unhide', 'unhideWithoutActivation', 'unregisterForRemoteNotifications', 'updateWindows', 'userInterfaceLayoutDirection', 'windows', 'windowsMenu']

def xx_cls(list_of_cls, skip_classes= (type,  objc.objc_class,  type(NSObject))):
    return [cls for cls in list_of_cls if type(cls) not in skip_classes and hasattr(cls,"__dict__") ]


D = {}

def printB(label,theObj,add=[],subtract=[],only=[], all_names=False):

    if len(label) > 0:
        print "--------------"
        print 
        print s4+label
        print
    else:
        print "--------------\n"

    print s4+cls_repr(theObj)

    if type(theObj) != NSApplication:
        print "%s%r" % (s4 , type(theObj))
        return
        
    mro = list(theObj.__class__.__mro__  )
    mro.reverse()
    mro.append(theObj)


    for partialClass in xx_cls(mro, skip_classes=(type,  objc.objc_class)):
        
        print
        

# (<NSApplication: 0x7fad96a13cd0>, <objective-c class NSObject at 0x7fff7e328b68>)
        
         
        # if type(partialClass) in [type,  objc.objc_class,  type(NSObject) ]: # also: 'objc_class', 'objc_object'
        #     print "skipping class", type(partialClass)
        # else: 
        print s4 + "-"*24
        if hasattr(partialClass, 'description'):
            print s4+partialClass.description()
        else:
            print s4+cls_repr(partialClass)
        print s4 + "-"*24
        # print

        the_names =  obj_attrs0(partialClass)
        
        # if (theObj, partialClass) not in D:
        #     D [(theObj, partialClass)] = the_names
        # else:
        #     keys = set(        D [(theObj, partialClass)] ) - 
        
        # print the_names
        # for k in sorted(the_names):
        #     print k                         # need list to go through when crashes!

        xx(theObj,the_names)

def xx(partialClass, obj,the_names):
    
        for k in sorted(the_names):
            
            if   hasattr(obj, k) and (k not in ['finalize' ,  'dealloc', 'init', 'run', 
                            'allowsWeakReference', 'clearProperties', 'retainWeakReference', 'copy', 'mutableCopy',
                            'autorelease', 'release', 'canCycle', 'gState', 'makeKeyWindow', 'makeMainWindow',
                            'windowRef', 'layoutSubtreeIfNeeded', 'lockFocus', 'becomeKeyWindow', 'becomeMainWindow',
                            'composition', 'retain'
                            ]) and not k.startswith('accessibility') \
                                and not k.startswith('enable') \
                                and not k.startswith('disable'):
    
                # print k, 
                print "    "+"%-32s : "  % (k,),
                
                print MyGetAttr(obj,k)
                
               
            else:
                if not hasattr(obj, k):
                    print "no", k , "in", obj
            #         print "    "+"%-32s : %r"  % (k, getattr(obj, k)())

def MyGetAttr(obj,k):
    
    try:
        zz = getattr(obj, k)()

        if type(zz) == NSRect:
            return "NSRect[ (%r, %r), (%r, %r) ]" % (zz.origin.x, zz.origin.y, zz.size.width, zz.size.height)
        elif type(zz) in ( int, bool, long, type(None), tuple, objc.pyobjc_unicode):
            return zz
        else:
            zzr = repr(zz)
            if zzr.startswith('<objective-c class'): 
                zzr = cls_repr(zz)
                return zzr
            elif   'class __NSArray' in repr(type(zz)):
                if len(zz) == 0:
                    return "()"
                else:
                    return zzr 
            else:
                return type(zz), zzr
    except (TypeError, ValueError) as e:

        return e
        
        
        
class do_parse_args_TestCase( unittest.TestCase ):
    """ Class to test relation_dict """

    def setUp(self):
        pass
        
    
    def test_010_do_parse_args(self):

        s = u'/Users/donb/Ashley+Roberts/'
        map ( lambda x: x == 2 , ('1', 'b', '4') )
    
        obj = NSApplication 
        the_names =  obj_attrs0(obj)
        all_application_class_names = ['abortAllToolTips', 'abortModal', 'accessibilityActionNames', 'accessibilityAttributeNames', 'accessibilityChildrenAttribute', 'accessibilityEnhancedUserInterfaceAttribute', 'accessibilityFocusedUIElement', 'accessibilityFocusedUIElementAttribute', 'accessibilityFocusedWindowAttribute', 'accessibilityFrontmostAttribute', 'accessibilityHiddenAttribute', 'accessibilityHitTest', 'accessibilityIsChildrenAttributeSettable', 'accessibilityIsEnhancedUserInterfaceAttributeSettable', 'accessibilityIsFocusedUIElementAttributeSettable', 'accessibilityIsFocusedWindowAttributeSettable', 'accessibilityIsFrontmostAttributeSettable', 'accessibilityIsHiddenAttributeSettable', 'accessibilityIsIgnored', 'accessibilityIsMainWindowAttributeSettable', 'accessibilityIsMenuBarAttributeSettable', 'accessibilityIsRoleAttributeSettable', 'accessibilityIsRoleDescriptionAttributeSettable', 'accessibilityIsTitleAttributeSettable', 'accessibilityIsWindowsAttributeSettable', 'accessibilityMainWindowAttribute', 'accessibilityMenuBarAttribute', 'accessibilityRoleAttribute', 'accessibilityRoleDescriptionAttribute', 'accessibilityShouldUseUniqueId', 'accessibilityTitleAttribute', 'accessibilityWindowsAttribute', 'activationPolicy', 'applicationIconImage', 'areCursorRectsEnabled', 'canEnterFullScreenMode', 'completeStateRestoration', 'context', 'contextID', 'currentEvent', 'currentSystemPresentationOptions', 'deactivate', 'dealloc', 'delayWindowOrdering', 'delegate', 'disableAutomaticTermination', 'disableCursorRects', 'disableRelaunchOnLogin', 'dockTile', 'enableAutomaticTermination', 'enableCursorRects', 'enableRelaunchOnLogin', 'enabledRemoteNotificationTypes', 'extendStateRestoration', 'finalize', 'finishLaunching', 'frontWindow', 'gestureEventMask', 'helpMenu', 'init', 'isActive', 'isDefaultHelpBookSearchEnabled', 'isFullKeyboardAccessEnabled', 'isHidden', 'isRunning', 'isSpeaking', 'keyWindow', 'mainMenu', 'mainWindow', 'menu', 'modalWindow', 'orderedDocuments', 'orderedWindows', 'presentationOptions', 'preventWindowOrdering', 'run', 'servicesMenu', 'servicesProvider', 'shouldRestoreStateOnNextLaunch', 'stopModal', 'unhide', 'unhideWithoutActivation', 'unregisterForRemoteNotifications', 'updateWindows', 'userInterfaceLayoutDirection', 'windows', 'windowsMenu']
        
        self.assertEqual( the_names , all_application_class_names )
        
    
        
    def test_020_do_parse_args(self):

        s = u'/Users/donb/Ashley+Roberts/'
        map ( lambda x: x == 2 , ('1', 'b', '4') )
    
        app = NSApplication.sharedApplication()
        obj = app
        
        # print "type(app) is", type(NSApplication), type(NSObject)
        
        printB("test_020", obj)



if __name__ == '__main__':
    unittest.main()    