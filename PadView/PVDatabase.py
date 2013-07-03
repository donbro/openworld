#
#  PVDatabase.py
#  PadView
#
#  Created by donb on 2010.05.08.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

#from objc import YES, NO, IBAction, IBOutlet
#from Foundation import *
#from AppKit import *

import MySQLdb

class create_conn ( object ):
    
    def __init__(self, host = "localhost", user = "root", passwd = "",  db = "nodes"):
        print "class create_conn: received __init__"
        self.conn = MySQLdb.connect (host = host,
                                     user = user,
                                     passwd = passwd,
                                     db = db )
        
        """OperationalError: (2002, "Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)") """
    
    def __del__(self):
        print "class create_conn: received __del__"
        self.conn.close ()
   
    def execute_and_fetchall( self , sql , use_dict_cursor = False):
        
        if use_dict_cursor:
            cursor = self.conn.cursor (MySQLdb.cursors.DictCursor)
        else:
            cursor = self.conn.cursor()
                
        cursor.execute (sql)
                
        rows = cursor.fetchall()
        
        
        cursor.close ()
        
        return rows
            
 

__author__ = 'donb'

import copy

import cPickle


DEFAULT_DATA = {
    'node0001': {
        'name': 'TV Shows',
        'pw': 'secret',
        'is_author': False,
        'is_admin': True,
        'subsets' : ['node0002', 'node0003']
    },
   'sardo': {
        'name': 'Miss Sardo',
        'pw': 'odras',
        'is_author': True,
        'is_admin': False,
        'private_snippet': 'I hate my brother Romano.',
        'web_site': 'http://www.google.com/search?q="pecorino+sardo"',
        'color': 'red',
        'snippets': [],
    },
    'brie': {
        'name': 'Brie',
        'pw': 'briebrie',
        'is_author': True,
        'is_admin': False,
        'private_snippet': 'I use the same password for all my accounts.',
        'web_site': 'http://news.google.com/news/search?q=brie',
        'color': 'red; text-decoration:underline',
        'snippets': [
            'Brie is the queen of the cheeses<span style=color:red>!!!</span>'
        ],
    },
}


def DefaultData():
  """Provides default data for Jarlsberg."""
  return copy.deepcopy(DEFAULT_DATA)

global StoredData

from Cocoa import NSBundle, NSLog

def LoadDatabase():
    """Load the database from stored-data.txt.

    Returns:
    The loaded database.
    """

    
    textResourcesFilePaths = NSBundle.mainBundle().pathsForResourcesOfType_inDirectory_("txt", None)
    
    databaseFilePath = textResourcesFilePaths[0]
    
    NSLog ( "LoadDatabase: databaseFilePath is: %s " % (databaseFilePath, ) )

    #fn = "database.pickle.txt"

    try:
        f = open( databaseFilePath , "r" )

        #StoredData = cPickle.load(f)
        r = f.read()
        f.close()
        #print "read %d bytes from %s" % ( len(r), fn )
    except (IOError, ValueError):
        print "Could not read from file: %r." % (  databaseFilePath,  )
        StoredData = None
        f.close()
        return StoredData

    try:
        StoredData = eval(r)

    except (IOError, ValueError):
        StoredData = None
    return StoredData



def SaveDatabase(save_database):
    """Save the database to stored-data.txt.

    Args:
    save_database: the database to save.
    """
    fn = "database.pickle.txt"

    try:
        f = open(fn, 'w')

        #cPickle.dump(save_database, f, 0)  # 0 is oldest, ASCII format.  better for hand-editing?
        r = repr(save_database)
        f.write(r)
        f.close()
        print "wrote database to file %s" % fn
    except IOError:
        _Log('Couldn\'t save data')




def get_top_level_nodes():

    conn = create_conn( host = "localhost", user = "root", passwd = "",  db = "nodes" )

    print "conn is: " , conn
    
    #
    #   nodes
    #
    
    sql = """ select *  
              from nodes.nodes
              """
    
    rows = conn.execute_and_fetchall(sql, use_dict_cursor=True)

    print "Number of nodes:  %d" % len( rows )

    #
    #   links
    #
    
    sql = """ select node_id_up, node_name_up, relation_phrase_down, node_id_down, node_name_down, 
                rel_dir_key, relation_phrase_up, dimension_id, rel_id  
              from nodes.links_up_down
              where dimension_id = 'd1'
              """
    
    rows_dict = conn.execute_and_fetchall(sql, use_dict_cursor=True)
    rows = conn.execute_and_fetchall(sql, use_dict_cursor=False)

    print "Number of links up: %d" % len( rows )

    # Number of links up: 34

    #   {'relation_phrase_up': 'example is', 'rel_dir_key': 'r2yx', 
    #    'relation_phrase_down': 'is an example of', 'dimension_id': 'd1', 
    #    'node_name_up': 'package management system', 'node_id_up': 'node0605', 
    #    'node_id_down': 'node0615', 'rel_id': 'r2', 'node_name_down': 'BSD ports'}

    #get node up names only, don't need node down names for this result...
    
    nodes = {}
    subsets = {}
    for r in rows_dict:
        node_id_up  = r['node_id_up']
        nodes[node_id_up] = r['node_name_up']
        
        if subsets.has_key(node_id_up):
            if subsets[node_id_up].has_key('node_name'):
                subsets[node_id_up]['subsets'] += [ r['node_id_down'] ]                
            else:
                subsets[node_id_up]['subsets'] = [ r['node_id_down'] ] # won't really happen.
                
            #subsets[node_id_up] += [  r['node_id_down']  ]
            #subsets[node_id_up] += [ ( r['node_id_down'], r['node_name_down'] ) ]
        else:
            subsets[node_id_up] = {'node_name':  r['node_name_up'] , 'subsets': [ r['node_id_down'] ] }
            #subsets[node_id_up] = [  r['node_id_down']  ]
            #subsets[node_id_up] = [ (r['node_id_down'], r['node_name_down']) ]
        
     
#    print "nodes: (%d) %r" % ( len(nodes) , nodes )
#    print "subsets: (%d) %r" % ( len(subsets) , subsets )
            
    # package management system example is BSD ports
    # Sci-Fi TV Series has subset Mutant/Superhero TV Series
    # operating system example is FreeBSD
    # operating system example is Mac OS X

   # ('node0605', 'package management system', 'is an example of', 'node0615', 'BSD ports', 'r2yx', 'example is', 'd1', 'r2')

    ( node_id_up, node_name_up, relation_phrase_down, node_id_down, node_name_down, 
                rel_dir_key, relation_phrase_up, dimension_id, rel_id) \
                        =  zip(*rows) 
 
    theUpIDs =  set( node_id_up ) - set( node_id_down )   # those above who are not below any others

    r =  [( node_id_up,   subsets[node_id_up]   ) for node_id_up in theUpIDs]
    #r =  [( node_id_up, (nodes[node_id_up], subsets[node_id_up] ) ) for node_id_up in theUpIDs]
    
    return dict( r )

    #d = dict(zip(('one', 'two'), (2, 3)))
    #d = dict([['two', 3], ['one', 2]])    
    

import pprint
# prevent these actions from happening when we are just importing this script into another file:
if __name__ == '__main__':

    top_level_nodes = get_top_level_nodes()

    print "top level nodes: (%d) %r" % ( len(top_level_nodes) , top_level_nodes )

    for (i,n) in enumerate( top_level_nodes ):
        print (i,n)
        
    pprint.pprint( top_level_nodes )    
