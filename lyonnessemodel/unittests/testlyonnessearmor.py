'''
Created on Jul 23, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.api import users

from hydramodel import hydrauser
from hydramodel import hydracontent
from lyonnessemodel import lyonnessearmor
from lyonnessemodel import lyonnessemass
from lyonnessemodel import lyonnesseprotection


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

    def testInsertLyonnesseArmor(self):
        emailAddr='testInsertLyonnesseArmor@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testMass = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_LARGE,
                                                   owner=testEntity)
        testProt = lyonnesseprotection.get_lyonnesseprotection(lyonnesseprotection.LYONESSEPROTECTION_MEDIUM,
                                                               testEntity)
        testContent = hydracontent.create_hydra_content(
                                                        lyonnessearmor.LyonnesseArmor,
                                                        owner = testEntity,
                                                        mass = testMass,
                                                        protection = testProt,
                                                        cover = "Full Body"
                                                        )
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)

        result = db.get( testContent.key())
        self.assertEqual( result.owner, testEntity)
        self.assertIsInstance( result, lyonnessearmor.LyonnesseArmor)
        self.assertEqual( result.cover, "Full Body")
        self.assertEqual( result.mass, testMass)
        self.assertEqual( result.protection, testProt)

    def testCloneLyonnesseArmor(self):
        eAddrs=['testCloneLyonnesseArmor0@hydrauser.com',
                'testCloneLyonnesseArmor1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "testCloneLyonnesseArmor"
        testContent = hydracontent.create_hydra_content(
                            lyonnessearmor.LyonnesseArmor,
                            mass = lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_TINY, owner=testEntity),
                            cover = "Shield",
                            owner=origPub,
                            originalPublisher=origPub,
                            instanceName = testName)
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertIsInstance( result, lyonnessearmor.LyonnesseArmor)
        self.assertEqual( result.mass, lyonnessemass.get_lyonnessemass(lyonnessemass.LYONNESSEMASS_TINY))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
