'''
Created on Jul 25, 2012

@author: ewilde
'''
import unittest

from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser

from lyonnessemodel import lyonnesseroundaction
from lyonnessemodel import lyonnesseroundeffect
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

    def testInsertLyonnesseRoundEffect(self):
        emailAddr='testInsertLyonnesseRoundEffect@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testAdv = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_ABSURD,
                                                            testEntity)
        testyAction = lyonnesseroundaction.LyonnesseRoundAction( moveDestination = [1.0,2.0,3.0],
                                                                 action = lyonnesseroundaction.LYONNESSEROUNDACTION_ATTACK,
                                                                 strengthEffort = True,
                                                                 agilityEffort = False,
                                                                 speedEffort = True,
                                                                 poised = True,
                                                                 repeat = False,
                                                                 advantage = testAdv,
                                                                 parent = testEntity
                                                                )
        testyAction.put()
        testContent = lyonnesseroundeffect.LyonnesseRoundEffect(roundAction = testyAction,
                                                                wounds=0,
                                                                fatigue=1,
                                                                moveDestination=[1.0,2.0,3.0],
                                                                parent=testEntity)
        testContent.put()
 
        result = lyonnesseroundeffect.LyonnesseRoundEffect.all().get()
        self.assertIsNotNone(result)
        self.assertIsInstance( result, lyonnesseroundeffect.LyonnesseRoundEffect)
        self.assertEqual( result.roundAction, testyAction)
        self.assertEqual( result.wounds, 0)
        self.assertEqual( result.fatigue, 1)
        self.assertEqual( result, testContent)  # test __eq__
        

    def testCloneLyonnesseRoundEffect(self):
        eAddrs=['testCloneLyonnesseRoundEffect0@hydrauser.com',
                'testCloneLyonnesseRoundEffect1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testAdv = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_ABSURD,
                                                            origPub)
        testyAction = lyonnesseroundaction.LyonnesseRoundAction( moveDestination = [1.0,2.0,3.0],
                                                                 action = lyonnesseroundaction.LYONNESSEROUNDACTION_ATTACK,
                                                                 strengthEffort = True,
                                                                 agilityEffort = False,
                                                                 speedEffort = True,
                                                                 poised = True,
                                                                 repeat = False,
                                                                 advantage = testAdv,
                                                                 parent = origPub
                                                                )
        testyAction.put()
        testContent = lyonnesseroundeffect.LyonnesseRoundEffect(roundAction = testyAction,
                                                                wounds=0,
                                                                fatigue=1,
                                                                moveDestination=[1.0,2.0,3.0],
                                                                parent=origPub)
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNotNone(result)
        self.assertIsInstance( result, lyonnesseroundeffect.LyonnesseRoundEffect)
        self.assertEqual( result.roundAction, testyAction)
        self.assertEqual( result.wounds, 0)
        self.assertEqual( result.fatigue, 1)
        self.assertEqual( result, testContent)  # test __eq__
        

if __name__ == '__main__':
    unittest.main()    
