'''
Created on Jul 23, 2012

@author: ewilde
'''
import unittest

from google.appengine.ext import testbed
from google.appengine.api import users

from hydramodel import hydrauser
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

    def testCreateLyonnesseAdvantage(self):
        emailAddr='testCreateLyonnesseAdvantage@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testContent = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_ABSURD,
                                                                owner=testEntity)

        result = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_ABSURD,
                                                           testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( result, testContent)
        self.assertEqual( result.value, lyonnesseadvantage.LYONESSEADVANTAGE_ABSURD)
        self.assertEqual( result.valName, 'Absurd')

    def testEnumerateLyonnesseAdvantage(self):
        emailAddr='testCreateLyonnesseAdvantage@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        result = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_ABSURD,
                                                                owner=testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseadvantage.LYONESSEADVANTAGE_ABSURD)
        self.assertEqual( result.valName, 'Absurd')
    
        result = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_HARD)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseadvantage.LYONESSEADVANTAGE_HARD)
        self.assertEqual( result.valName, 'Hard')

        result = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_CHALLENGING)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseadvantage.LYONESSEADVANTAGE_CHALLENGING)
        self.assertEqual( result.valName, 'Challenging')

        result = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_NORMAL)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseadvantage.LYONESSEADVANTAGE_NORMAL)
        self.assertEqual( result.valName, 'Normal')

        result = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_EASY)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseadvantage.LYONESSEADVANTAGE_EASY)
        self.assertEqual( result.valName, 'Easy')

        result = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_ROUTINE)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseadvantage.LYONESSEADVANTAGE_ROUTINE)
        self.assertEqual( result.valName, 'Routine')

        result = lyonnesseadvantage.get_lyonnesseadvantage(lyonnesseadvantage.LYONESSEADVANTAGE_TRIVIAL)
        self.assertIsNotNone(result)
        self.assertEqual( result.value, lyonnesseadvantage.LYONESSEADVANTAGE_TRIVIAL)
        self.assertEqual( result.valName, 'Trivial')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()