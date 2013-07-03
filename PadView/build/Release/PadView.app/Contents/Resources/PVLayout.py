#!/usr/bin/env python
# encoding: utf-8
"""
PVLayout.py

Created by donb on 2010-05-25.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest

import math

 


class PVLayoutGrid(object):
    def __init__(self, n):
        self.n = n


    def grid(self):
        return  (math.floor( self.n ** .5 ) , math.ceil( self.n ** .5 )  ) # (2.0, 3.0)

    def g(self):
        return    math.ceil( self.n ** .5 )  
        
    def g2(self):
        return    math.ceil( self.n ** .5 ) ** 2.0  
        
    def g2ni(self, i):
        return   i * ( self.g2() / self.n )  

    def f(self, i):
        return  math.floor( self.g2ni(i) / self.g() )

    def gn5(self, i):
        if self.gn0p(i):  # i in (3,4):  # round to nearest 0.5 on the odd ranks
            return  0.5 + math.floor(   self.g2ni(i) )
        else:
            return  math.floor( 0.5 + self.g2ni(i) )

    def gn0(self, i):
        return  math.floor( 0.5 + self.g2ni(i) )

    def gn0p(self, i):
        """compare the number, without rounding to 0.5 less than twice g()"""
        return   self.gn0(i) >= self.g() and  self.g2ni(i) < -0.5 + 2.0 * self.g()  # generalize for k=2,4,6,..
        return   self.gn0(i) >= self.g() and  self.g2ni(i) < -0.6 + 2.0 * self.g()  # generalize for k=2,4,6,..
 #       return   self.gn0(i) >= self.g() and  self.gn0(i) < 2.0 * self.g()  # generalize for k=2,4,6,..

    def x(self, i):
        return self.gn5(i) % self.g() 

    def xn(self, i):
        #return ( self.x(i) + 0.5 ) /( self.g()  )      # on a field of azure, center rampant... 
        return ( self.x(i) + 0.5 ) /( self.g()+1.0 )      # on a field of azure, center rampant... 

    def y(self, i):
        return math.floor( self.gn5(i) / self.g() )

    def yn(self, i):
        #return ( self.x(i) + 0.5 ) /( self.g()  )      # on a field of azure, center rampant... 
        return ( self.y(i) + 0.5 ) /( self.g()+1.0 )      # on a field of azure, center rampant... 
        
    def str(self, i):
        #return "%d  %.3f  %d  %-5r %.1f (%.2f, %.2f)" % \
        return "%d  %.3f  %d  %-5r %.1f ( %.1f , %.1f ) %.3f %.3f " % \
                ( i,    self.g2ni(i), 
                        self.gn0(i), 
                        self.gn0p(i), 
                        self.gn5(i), 
                        self.x(i) ,
                        self.y(i)  ,
                        self.xn(i)  ,
                        self.yn(i)  ,
                        )   
        

    def __repr__(self):
        return "n=%d, g=%d, g2=%d" % ( self.n , self.g(), self.g2() )
 #       return "n=%d, g=%.1f, g2=%.1f" % ( self.n , self.g(), self.g2() )


class untitledTests(unittest.TestCase):
    def setUp(self):
        pass

    def test000(self):
        self.layout = PVLayoutGrid(4)
        print "PVLayoutGrid is:" , self.layout
        print "i   g2ni gn0  gn0p gn5 (  x  ,  y  ) " 
        for i in range(self.layout.n):  
            print self.layout.str(i)  

    def test001(self):
        self.layout5 = PVLayoutGrid(5)
        print "PVLayoutGrid is:" , self.layout5
        print "i   g2ni gn0  gn0p gn5 (  x ,   y ) " 
        for i in range(self.layout5.n):  # (1,9):
            print "%d  %.3f  %d  %-5r %.1f (%.2f, %.2f)" % \
                ( i,    self.layout5.g2ni(i), 
                        self.layout5.gn0(i), 
                        self.layout5.gn0p(i), 
                        self.layout5.gn5(i), 
                        self.layout5.x(i) ,
                        self.layout5.y(i)  
                        )   

 
    def test002(self):
        self.layout8 = PVLayoutGrid(8)
        print "PVLayoutGrid is:" , self.layout8
        print "i   g2ni gn0  gn0p gn5 (  x ,   y ) " 
        for i in range(self.layout8.n):  # (1,9):
            print "%d  %.3f  %d  %-5r %.1f (%.2f, %.2f)" % \
                ( i,    self.layout8.g2ni(i), 
                        self.layout8.gn0(i), 
                        self.layout8.gn0p(i), 
                        self.layout8.gn5(i), 
                        self.layout8.x(i) ,
                        self.layout8.y(i)  
                        )   

    def test003(self):
        self.layout = PVLayoutGrid(9)
        print "layout is:" , self.layout
        print "i   g2ni gn0  gn0p gn5 (  x  ,  y  ) " 
        for i in range(self.layout.n):  
            print self.layout.str(i)  
 

if __name__ == '__main__':
    unittest.main()