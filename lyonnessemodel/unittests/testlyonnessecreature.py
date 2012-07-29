'''
Created on Jul 24, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.api import users

from hydramodel import hydrauser
from hydramodel import hydracontent
from lyonnessemodel import lyonnessecreature
from lyonnessemodel import lyonnessemass
from lyonnessemodel import lyonnessespeed


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

    def testInsertLyonnesseCreature(self):
        emailAddr='testInsertLyonnesseCreature@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        strength = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_LARGE,
                                              owner=testEntity)
        ag = lyonnessespeed.get_lyonnessespeed( lyonnessespeed.LYONNESSESPEED_CREEPING,
                                                testEntity)
        sp = lyonnessespeed.get_lyonnessespeed( lyonnessespeed.LYONNESSESPEED_DELIBERATE)
        dur = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_LARGE)

        testContent = hydracontent.create_hydra_content(lyonnessecreature.LyonnesseCreature,
                                                        owner = testEntity,
                                                        strength = strength,
                                                        agility=ag,
                                                        speed=sp,
                                                        durability=dur,
                                                        wounds = 1,
                                                        fatigue = 2,
                                                        maxhits = 12
                                                        )
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)

        result = db.get( testContent.key())
        self.assertEqual( result.owner, testEntity)
        self.assertIsInstance( result, lyonnessecreature.LyonnesseCreature)
        self.assertEqual( result.strength, strength)
        self.assertEqual( result.agility, ag)
        self.assertEqual( result.speed, sp)
        self.assertEqual( result.durability, dur)
        self.assertEqual( result.maxhits, 12)
        self.assertEqual( result.wounds, 1)
        self.assertEqual( result.fatigue, 2)

    def testCloneLyonnesseCreature(self):
        eAddrs=['testCloneLyonnesseCreature0@hydrauser.com',
                'testCloneLyonnesseCreature1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        strength = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_LARGE,
                                              owner=origPub)
        ag = lyonnessespeed.get_lyonnessespeed( lyonnessespeed.LYONNESSESPEED_CREEPING,
                                                origPub)
        sp = lyonnessespeed.get_lyonnessespeed( lyonnessespeed.LYONNESSESPEED_DELIBERATE)
        dur = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_LARGE, origPub)

        testContent = hydracontent.create_hydra_content(lyonnessecreature.LyonnesseCreature,
                                                        owner = origPub,
                                                        originalPublisher = origPub,
                                                        strength = strength,
                                                        agility=ag,
                                                        speed=sp,
                                                        durability=dur,
                                                        wounds = 1,
                                                        fatigue = 2,
                                                        maxhits = 12
                                                        )
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertIsInstance( result, lyonnessecreature.LyonnesseCreature)
        self.assertEqual( result.strength, strength)
        self.assertEqual( result.agility, ag)
        self.assertEqual( result.speed, sp)
        self.assertEqual( result.durability, dur)
        self.assertEqual( result.maxhits, 12)
        self.assertEqual( result.wounds, 1)
        self.assertEqual( result.fatigue, 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
