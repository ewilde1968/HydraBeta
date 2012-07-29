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

from lyonnessemodel import lyonnessepc
from lyonnessemodel import lyonnessemass
from lyonnessemodel import lyonnessespeed
from lyonnessemodel import lyonnessecreaturehistory
from lyonnessemodel import lyonnesselogentry


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

    def testInsertLyonnessePC(self):
        emailAddr='testInsertLyonnessePC@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        strength = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_LARGE,
                                              owner=testEntity)
        ag = lyonnessespeed.get_lyonnessespeed( lyonnessespeed.LYONNESSESPEED_CREEPING,
                                                testEntity)
        sp = lyonnessespeed.get_lyonnessespeed( lyonnessespeed.LYONNESSESPEED_DELIBERATE)
        dur = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_LARGE)
        testName = "Instance Name"
        testDesc = "I want to ride my bicycle"
        testLE = hydracontent.create_hydra_content(lyonnesselogentry.LyonnesseLogEntry,
                                                   instanceName = testName,
                                                   description = testDesc,
                                                   owner = testEntity
                                                   )
        testLE.put()
        testHistory = hydracontent.create_hydra_content(lyonnessecreaturehistory.LyonnesseCreatureHistory,
                                                        owner = testEntity,
                                                        logEntries = [testLE.key()]
                                                        )
        testHistory.put()
        testContent = hydracontent.create_hydra_content( lyonnessepc.LyonnessePC,
                                                         strength = strength,
                                                         agility=ag,
                                                         speed=sp,
                                                         durability=dur,
                                                         wounds = 1,
                                                         fatigue = 2,
                                                         maxhits = 12,
                                                         history = testHistory,
                                                         owner = testEntity
                                                         )
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)

        result = db.get( testContent.key())
        self.assertEqual( result.owner, testEntity)
        self.assertIsInstance( result, lyonnessepc.LyonnessePC)
        self.assertEqual( result.strength, strength)
        self.assertEqual( result.agility, ag)
        self.assertEqual( result.speed, sp)
        self.assertEqual( result.durability, dur)
        self.assertEqual( result.maxhits, 12)
        self.assertEqual( result.wounds, 1)
        self.assertEqual( result.fatigue, 2)
        self.assertEqual( result.history, testHistory)

    def testCloneLyonnessePC(self):
        eAddrs=['testCloneLyonnessePC0@hydrauser.com',
                'testCloneLyonnessePC1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        strength = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_LARGE,
                                              owner=origPub)
        ag = lyonnessespeed.get_lyonnessespeed( lyonnessespeed.LYONNESSESPEED_CREEPING,
                                                origPub)
        sp = lyonnessespeed.get_lyonnessespeed( lyonnessespeed.LYONNESSESPEED_DELIBERATE)
        dur = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_LARGE)
        testName = "Instance Name"
        testDesc = "I want to ride my bicycle"
        testLE = hydracontent.create_hydra_content(lyonnesselogentry.LyonnesseLogEntry,
                                                   instanceName = testName,
                                                   description = testDesc,
                                                   owner = testEntity
                                                   )
        testLE.put()
        testHistory = hydracontent.create_hydra_content(lyonnessecreaturehistory.LyonnesseCreatureHistory,
                                                        owner = testEntity,
                                                        logEntries = [testLE.key()]
                                                        )
        testHistory.put()
        testContent = hydracontent.create_hydra_content( lyonnessepc.LyonnessePC,
                                                         owner=origPub,
                                                         originalPublisher=origPub,
                                                         strength = strength,
                                                         agility=ag,
                                                         speed=sp,
                                                         durability=dur,
                                                         wounds = 1,
                                                         fatigue = 2,
                                                         maxhits = 12,
                                                         history = testHistory,
                                                         instanceName = testName
                                                         )
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertIsInstance( result, lyonnessepc.LyonnessePC)
        self.assertEqual( result.strength, strength)
        self.assertEqual( result.agility, ag)
        self.assertEqual( result.speed, sp)
        self.assertEqual( result.durability, dur)
        self.assertEqual( result.maxhits, 12)
        self.assertEqual( result.wounds, 1)
        self.assertEqual( result.fatigue, 2)
        self.assertEqual( result.history, testHistory)
        

if __name__ == '__main__':
    unittest.main()    
