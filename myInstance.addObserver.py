#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import NSObject, NSKeyValueObservingOptionNew, NSKeyValueChangeNewKey

class MyClass(NSObject):
    base = objc.ivar("base", objc._C_INT)
    power = objc.ivar("power", objc._C_INT)
    result = objc.ivar("result", objc._C_INT)

    def result(self):
        return self.base ** self.power

MyClass.setKeys_triggerChangeNotificationsForDependentKey_(
    [u"base", u"power"],
    u"result"
)

class Observer(NSObject):
    def observeValueForKeyPath_ofObject_change_context_(self, path, object, changeDescription, context):
        print 'path "%s" was changed to "%s".' % (path, changeDescription[NSKeyValueChangeNewKey])

myInstance = MyClass.new()
observer = Observer.new()

myInstance.addObserver_forKeyPath_options_context_(observer, "result", NSKeyValueObservingOptionNew, 0)
myInstance.addObserver_forKeyPath_options_context_(observer, "base", NSKeyValueObservingOptionNew, 0)
myInstance.addObserver_forKeyPath_options_context_(observer, "power", NSKeyValueObservingOptionNew, 0)

myInstance.setValue_forKey_(2, "base")
myInstance.power = 4

print "%d ** %d == %d" % (myInstance.base, myInstance.valueForKey_("power"), myInstance.result())

"""

Running “untitled”…
Python 2.7.1
Theme:  
path "base" was changed to "2".
path "result" was changed to "1".
path "power" was changed to "4".
path "result" was changed to "16".
2 ** 4 == 16

2013-06-28 18:50:24.947 Python[38250:1507] An instance 0x7fc4262107f0 of class MyClass was deallocated while key value observers were still registered with it. Observation info was leaked, and may even become mistakenly attached to some other object. Set a breakpoint on NSKVODeallocateBreak to stop here in the debugger. Here's the current observation info:
<NSKeyValueObservationInfo 0x7fc4262152b0> (
<NSKeyValueObservance 0x7fc426212800: Observer: 0x7fc426211430, Key path: result, Options: <New: YES, Old: NO, Prior: NO> Context: 0x0, Property: 0x7fc426211de0>
<NSKeyValueObservance 0x7fc426215040: Observer: 0x7fc426211430, Key path: base, Options: <New: YES, Old: NO, Prior: NO> Context: 0x0, Property: 0x7fc426212140>
<NSKeyValueObservance 0x7fc426215240: Observer: 0x7fc426211430, Key path: power, Options: <New: YES, Old: NO, Prior: NO> Context: 0x0, Property: 0x7fc4262123e0>
)
copy output
Program exited with code #0 after 2.15 seconds.
"""

