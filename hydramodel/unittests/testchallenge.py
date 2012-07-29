import unittest

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent
from hydramodel import challenge


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

    def testInsertChallenge(self):
        emailAddr='testInsertChallenge0@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testContent = hydracontent.create_hydra_content(
                            challenge.Challenge,
                            owner=testEntity)

        dummy = hydracontent.create_hydra_content(
            challenge.Challenge,
            owner=testEntity,
            instanceName='dummy')
        testContent.modifiers = []
        testContent.modifiers.append( dummy.put())
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( len(result), 2)

        result = db.get( testContent.key())
        self.assertEqual( result.owner, testEntity)
        self.assertIsInstance( result, challenge.Challenge)
        self.assertEqual( len(result.modifiers), 1)
        self.assertEqual( db.get(result.modifiers[0]), dummy)

    def testCloneChallenge(self):
        eAddrs=['testCloneChallenge0@hydrauser.com',
                'testCloneChallenge1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "testCloneChallenge"
        testContent = hydracontent.create_hydra_content(
                            challenge.Challenge,
                            owner=origPub,
                            originalPublisher=origPub,
                            instanceName = testName)

        dummy = hydracontent.create_hydra_content(
            challenge.Challenge,
            owner=testEntity,
            instanceName='dummy')
        testContent.modifiers = []
        testContent.modifiers.append( dummy.put())
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertIsInstance( result, challenge.Challenge)
        self.assertEqual( len(result.modifiers), 1)
        self.assertEqual( result.modifiers[0], dummy)
        

if __name__ == '__main__':
    unittest.main()    
