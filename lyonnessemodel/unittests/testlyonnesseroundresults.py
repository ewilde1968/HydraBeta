'''
Created on Jul 25, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser

from lyonnessemodel import lyonnesseroundaction
from lyonnessemodel import lyonnesseroundeffect
from lyonnessemodel import lyonnesseadvantage
from lyonnessemodel import lyonnesseroundresults


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

    def testInsertLyonnesseRoundResults(self):
        emailAddr='testInsertLyonnesseRoundResults@hydrauser.com'
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
        testEffect = lyonnesseroundeffect.LyonnesseRoundEffect(roundAction = testyAction,
                                                                wounds=0,
                                                                fatigue=1,
                                                                moveDestination=[1.0,2.0,3.0],
                                                                parent=testEntity)
        testEffect.put()
        testContent = lyonnesseroundresults.LyonnesseRoundResults(effects=[testEffect.key()],
                                                                  parent=testEntity
                                                                  )
        testContent.put()
 
        result = lyonnesseroundresults.LyonnesseRoundResults.all().get()
        self.assertIsNotNone(result)
        self.assertIsInstance( result, lyonnesseroundresults.LyonnesseRoundResults)
        self.assertEqual( db.get(result.effects[0]), testEffect)
        self.assertEqual( result, testContent)  # test __eq__
        

    def testCloneLyonnesseRoundResults(self):
        eAddrs=['testCloneLyonnesseRoundResults0@hydrauser.com',
                'testCloneLyonnesseRoundResults1@hydrauser.com']
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
        testEffect = lyonnesseroundeffect.LyonnesseRoundEffect(roundAction = testyAction,
                                                                wounds=0,
                                                                fatigue=1,
                                                                moveDestination=[1.0,2.0,3.0],
                                                                parent=origPub)
        testEffect.put()
        testContent = lyonnesseroundresults.LyonnesseRoundResults(effects=[testEffect.key()],
                                                                  parent=origPub
                                                                  )
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNotNone(result)
        self.assertIsInstance( result, lyonnesseroundresults.LyonnesseRoundResults)
        self.assertEqual( db.get( result.effects[0]), testEffect)
        self.assertEqual( result, testContent)  # test __eq__
        

if __name__ == '__main__':
    unittest.main()    
