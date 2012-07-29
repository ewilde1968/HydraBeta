'''
Created on Jul 24, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent

from lyonnessemodel import lyonnesseitem


class DemoTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def testInsertLyonnesseItem(self):
        emailAddr='testInsertLyonnesseItem@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testContent = hydracontent.create_hydra_content( lyonnesseitem.LyonnesseItem,
                                                         damaged = True,
                                                         owner = testEntity
                                                         )
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)

        result = db.get( testContent.key())
        self.assertEqual( result.owner, testEntity)
        self.assertIsInstance( result, lyonnesseitem.LyonnesseItem)
        self.assertEqual( result.damaged, True)

    def testCloneLyonnesseItem(self):
        eAddrs=['testCloneLyonnesseItem0@hydrauser.com',
                'testCloneLyonnesseItem1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "testCloneLyonnesseItem"
        testContent = hydracontent.create_hydra_content( lyonnesseitem.LyonnesseItem,
                                                         owner=origPub,
                                                         originalPublisher=origPub,
                                                         instanceName = testName,
                                                         damaged = True)
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertIsInstance( result, lyonnesseitem.LyonnesseItem)
        self.assertEqual( result.damaged, True)
        

if __name__ == '__main__':
    unittest.main()    
