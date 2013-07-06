
all_objs = {}
s4 = "    "
s3 = "   "

def printB(label,obj,add=[],subtract=[],only=[], all_names=False):
    """printB("App", NSApp(), add=['mainWindow'])"""
    
    if obj not in all_objs:
        print_all_names()
    
    print
    print "--------------\n\n"+s4+label
    print "\n"+s3+repr( b) # , type(b)

    obj=b
    print_setters(obj, add=add,subtract=subtract,only=only, all_names=all_names)
    
    
def repr_cls(cls):

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
        print "obj_attrs0: '" + repr_cls(obj.__class__) + "' object has no attribute '__dict__'"
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
from Foundation import NSObject, NSURL
from AppKit import NSApplication

def xx_cls(list_of_cls, skip_classes= (type,  objc.objc_class,  type(NSObject))):
    return [cls for cls in list_of_cls if type(cls) not in skip_classes and hasattr(cls,"__dict__") ]

all_application_class_names = ['abortAllToolTips', 'abortModal', 'accessibilityActionNames', 'accessibilityAttributeNames', 'accessibilityChildrenAttribute', 'accessibilityEnhancedUserInterfaceAttribute', 'accessibilityFocusedUIElement', 'accessibilityFocusedUIElementAttribute', 'accessibilityFocusedWindowAttribute', 'accessibilityFrontmostAttribute', 'accessibilityHiddenAttribute', 'accessibilityHitTest', 'accessibilityIsChildrenAttributeSettable', 'accessibilityIsEnhancedUserInterfaceAttributeSettable', 'accessibilityIsFocusedUIElementAttributeSettable', 'accessibilityIsFocusedWindowAttributeSettable', 'accessibilityIsFrontmostAttributeSettable', 'accessibilityIsHiddenAttributeSettable', 'accessibilityIsIgnored', 'accessibilityIsMainWindowAttributeSettable', 'accessibilityIsMenuBarAttributeSettable', 'accessibilityIsRoleAttributeSettable', 'accessibilityIsRoleDescriptionAttributeSettable', 'accessibilityIsTitleAttributeSettable', 'accessibilityIsWindowsAttributeSettable', 'accessibilityMainWindowAttribute', 'accessibilityMenuBarAttribute', 'accessibilityRoleAttribute', 'accessibilityRoleDescriptionAttribute', 'accessibilityShouldUseUniqueId', 'accessibilityTitleAttribute', 'accessibilityWindowsAttribute', 'activationPolicy', 'applicationIconImage', 'areCursorRectsEnabled', 'canEnterFullScreenMode', 'completeStateRestoration', 'context', 'contextID', 'currentEvent', 'currentSystemPresentationOptions', 'deactivate', 'dealloc', 'delayWindowOrdering', 'delegate', 'disableAutomaticTermination', 'disableCursorRects', 'disableRelaunchOnLogin', 'dockTile', 'enableAutomaticTermination', 'enableCursorRects', 'enableRelaunchOnLogin', 'enabledRemoteNotificationTypes', 'extendStateRestoration', 'finalize', 'finishLaunching', 'frontWindow', 'gestureEventMask', 'helpMenu', 'init', 'isActive', 'isDefaultHelpBookSearchEnabled', 'isFullKeyboardAccessEnabled', 'isHidden', 'isRunning', 'isSpeaking', 'keyWindow', 'mainMenu', 'mainWindow', 'menu', 'modalWindow', 'orderedDocuments', 'orderedWindows', 'presentationOptions', 'preventWindowOrdering', 'run', 'servicesMenu', 'servicesProvider', 'shouldRestoreStateOnNextLaunch', 'stopModal', 'unhide', 'unhideWithoutActivation', 'unregisterForRemoteNotifications', 'updateWindows', 'userInterfaceLayoutDirection', 'windows', 'windowsMenu']

my_application_names = [ 'activationPolicy', 'applicationIconImage', 'areCursorRectsEnabled', 'canEnterFullScreenMode', 'completeStateRestoration', 'context', 'contextID', 'currentEvent', 'currentSystemPresentationOptions', 'deactivate', 'dealloc', 'delayWindowOrdering', 'delegate', 'disableAutomaticTermination', 'disableCursorRects', 'disableRelaunchOnLogin', 'dockTile', 'enableAutomaticTermination', 'enableCursorRects', 'enableRelaunchOnLogin', 'enabledRemoteNotificationTypes', 'extendStateRestoration', 'finalize', 'finishLaunching', 'frontWindow', 'gestureEventMask', 'helpMenu', 'init', 'isActive', 'isDefaultHelpBookSearchEnabled', 'isFullKeyboardAccessEnabled', 'isHidden', 'isRunning', 'isSpeaking', 'keyWindow', 'mainMenu', 'mainWindow', 'menu', 'modalWindow', 'orderedDocuments', 'orderedWindows', 'presentationOptions', 'preventWindowOrdering', 'run', 'servicesMenu', 'servicesProvider', 'shouldRestoreStateOnNextLaunch', 'stopModal', 'unhide', 'unhideWithoutActivation', 'unregisterForRemoteNotifications', 'updateWindows', 'userInterfaceLayoutDirection', 'windows', 'windowsMenu']
        
class do_parse_args_TestCase( unittest.TestCase ):
    """ Class to test relation_dict """

    def setUp(self):
        pass
        
    
    def test_010_do_parse_args(self):

        s = u'/Users/donb/Ashley+Roberts/'
        map ( lambda x: x == 2 , ('1', 'b', '4') )
    
        obj = NSApplication 
        the_names =  obj_attrs0(obj)
        self.assertEqual( the_names , all_application_class_names )
        
    
        
    def test_020_do_parse_args(self):

        s = u'/Users/donb/Ashley+Roberts/'
        map ( lambda x: x == 2 , ('1', 'b', '4') )
    
        app = NSApplication.sharedApplication()
        obj = app

        mro = list(obj.__class__.__mro__  )
        mro.reverse()
        mro.append(obj)
        # print objc.objc_class
        # print [(type(cls), (type(cls) in [type,  objc.objc_class,  type(NSObject) ] ) )for cls in mro]
        # print mro, type(mro[0]), type(mro[2])  ==type(NSObject)
        
        # print type(NSObject)
        
        label = ''
    
        if len(label) > 0:
            print "--------------\n\n"+s4+label
            print
        else:
            print "--------------\n"
            
        print s4+repr_cls(obj)
        
        for cls in xx_cls(mro, skip_classes=[]):
            print
            
            if type(cls) in [type,  objc.objc_class,  type(NSObject) ]: # also: 'objc_class', 'objc_object'
                print "skipping class", type(cls)
            else: 
                print s4+repr_cls(cls)
                print
                the_names =  obj_attrs0(cls)
                print the_names

        
        # self.assertEqual( the_names , all_application_names )
        
        the_names = my_application_names

        for k in sorted(the_names):
            print k
        for k in sorted(the_names):
            print k, getattr(obj, k)()
            # if   hasattr(obj, k) :
            #         print "    "+"%-32s : %r"  % (k, getattr(obj, k)())



if __name__ == '__main__':
    unittest.main()    