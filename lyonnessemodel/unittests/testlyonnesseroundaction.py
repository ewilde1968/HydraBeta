'''
Created on Jul 25, 2012

@author: ewilde
'''
import unittest

from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser

from lyonnessemodel import lyonnesseroundaction
from lyonnessemodel import lyonnesseadvantage


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

    def testInsertLyonnesseRoundAction(self):
        emailAddr='testInsertLyonnesseRoundAction@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testAdv = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_ABSURD,
                                                            testEntity)
        testContent = lyonnesseroundaction.LyonnesseRoundAction( moveDestination = [1.0,2.0,3.0],
                                                                 action = lyonnesseroundaction.LYONNESSEROUNDACTION_ATTACK,
                                                                 strengthEffort = True,
                                                                 agilityEffort = False,
                                                                 speedEffort = True,
                                                                 poised = True,
                                                                 repeat = False,
                                                                 advantage = testAdv,
                                                                 parent = testEntity
                                                                )
        testContent.put()
 
        result = lyonnesseroundaction.LyonnesseRoundAction.all().get()
        self.assertIsNotNone(result)
        self.assertIsInstance( result, lyonnesseroundaction.LyonnesseRoundAction)
        self.assertEqual( result.action, lyonnesseroundaction.LYONNESSEROUNDACTION_ATTACK)
        self.assertEqual( result.strengthEffort, True)
        self.assertEqual( result.agilityEffort, False)
        self.assertEqual( result.speedEffort, True)
        self.assertEqual( result.poised, True)
        self.assertEqual( result.repeat, False)
        self.assertEqual( result.advantage, testAdv)
        self.assertEqual( result, testContent)  # test __eq__

    def testCloneLyonnesseRoundAction(self):
        eAddrs=['testCloneLyonnesseRoundAction0@hydrauser.com',
                'testCloneLyonnesseRoundAction1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testAdv = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_ABSURD,
                                                            origPub)
        testContent = lyonnesseroundaction.LyonnesseRoundAction( moveDestination = [1.0,2.0,3.0],
                                                                 action = lyonnesseroundaction.LYONNESSEROUNDACTION_ATTACK,
                                                                 strengthEffort = True,
                                                                 agilityEffort = False,
                                                                 speedEffort = True,
                                                                 poised = True,
                                                                 repeat = False,
                                                                 advantage = testAdv,
                                                                 parent = origPub
                                                                )
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNotNone(result)
        self.assertIsNot( result, testContent)
        self.assertIsInstance( result, lyonnesseroundaction.LyonnesseRoundAction)
        self.assertEqual( result.action, lyonnesseroundaction.LYONNESSEROUNDACTION_ATTACK)
        self.assertEqual( result.strengthEffort, True)
        self.assertEqual( result.agilityEffort, False)
        self.assertEqual( result.speedEffort, True)
        self.assertEqual( result.poised, True)
        self.assertEqual( result.repeat, False)
        self.assertEqual( result.advantage, testAdv)
        self.assertEqual( result, testContent)  # test __eq__
        

if __name__ == '__main__':
    unittest.main()    
