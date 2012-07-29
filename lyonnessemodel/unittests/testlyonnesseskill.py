'''
Created on Jul 25, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent

from lyonnessemodel import lyonnesseskill
from lyonnessemodel import lyonnesseskilllevel


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

    def testInsertLyonnesseSkill(self):
        emailAddr='testInsertLyonnesseSkill@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testSL = lyonnesseskilllevel.get_lyonnesseskilllevel(lyonnesseskilllevel.LYONNESSESKILLLEVEL_NEOPHYTE,
                                                             owner=testEntity
                                                             )
        testContent = hydracontent.create_hydra_content(lyonnesseskill.LyonnesseSkill,
                                                        owner=testEntity,
                                                        skillLevel=testSL
                                                        )
        testContent.put()
 
        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)

        result = db.get( testContent.key())
        self.assertIsNotNone(result)
        self.assertIsInstance( result, lyonnesseskill.LyonnesseSkill)
        self.assertEqual( result.skillLevel, testSL)
        self.assertEqual( result, testContent)  # test __eq__
        

    def testCloneLyonnesseSkill(self):
        eAddrs=['testCloneLyonnesseSkill0@hydrauser.com',
                'testCloneLyonnesseSkill1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testSL = lyonnesseskilllevel.get_lyonnesseskilllevel(lyonnesseskilllevel.LYONNESSESKILLLEVEL_NEOPHYTE,
                                                             owner=origPub
                                                             )
        testContent = hydracontent.create_hydra_content(lyonnesseskill.LyonnesseSkill,
                                                        owner=origPub,
                                                        originalPublisher=origPub,
                                                        skillLevel=testSL
                                                        )
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNotNone(result)
        self.assertIsInstance( result, lyonnesseskill.LyonnesseSkill)
        self.assertEqual( result.owner, testEntity)
        self.assertEqual( result.originalPublisher, origPub)
        self.assertEqual( result.skillLevel, testSL)
        

if __name__ == '__main__':
    unittest.main()    
