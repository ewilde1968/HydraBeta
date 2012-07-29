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

    def testInsertLyonnesseLogEntry(self):
        emailAddr='testInsertLyonnesseLogEntry@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testName = "Instance Name"
        testDesc = "I want to ride my bicycle"
        testContent = hydracontent.create_hydra_content(lyonnesselogentry.LyonnesseLogEntry,
                                                        owner = testEntity,
                                                        instanceName = testName,
                                                        description = testDesc
                                                        )
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)

        result = db.get( testContent.key())
        self.assertEqual( result.owner, testEntity)
        self.assertIsInstance( result, lyonnesselogentry.LyonnesseLogEntry)
        self.assertEqual( result.instanceName, testName)
        self.assertEqual( result.description, testDesc)
        self.assertIsNotNone( result.eventDate)

    def testCloneLyonnesseLogEntry(self):
        eAddrs=['testCloneLyonnesseLogEntry0@hydrauser.com',
                'testCloneLyonnesseLogEntry1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "Instance Name"
        testDesc = "I want to ride my bicycle"
        testContent = hydracontent.create_hydra_content(lyonnesselogentry.LyonnesseLogEntry,
                                                        owner = origPub,
                                                        originalPublisher = origPub,
                                                        instanceName = testName,
                                                        description = testDesc
                                                        )
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertIsInstance( result, lyonnesselogentry.LyonnesseLogEntry)
        self.assertEqual( result.instanceName, testName)
        self.assertEqual( result.description, testDesc)
        self.assertIsNotNone( result.eventDate)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
