import unittest

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent
from hydramodel import trap


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

    def testInsertTrap(self):
        emailAddr='testInsertTrap0@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testContent = hydracontent.create_hydra_content(
                            trap.Trap,
                            owner=testEntity)
        testContent.challenges = []

        dummy = hydracontent.create_hydra_content(
            trap.Trap,
            owner=testEntity,
            instanceName='dummy')
        dummy.put()
        testContent.challenges.append( dummy.key())
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( len(result), 2)

        result = db.get( testContent.key())
        self.assertEqual( result.owner, testEntity)
        self.assertIsInstance( result, trap.Trap)
        self.assertEqual( len(result.challenges), 1)
        self.assertEqual( db.get(result.challenges[0]), dummy)

    def testCloneTrap(self):
        eAddrs=['testCloneTrap0@hydrauser.com',
                'testCloneTrap1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "testCloneEncountertestCloneTrap"
        testContent = hydracontent.create_hydra_content(
                            trap.Trap,
                            owner=origPub,
                            originalPublisher=origPub,
                            instanceName = testName)

        dummy = hydracontent.create_hydra_content(
            trap.Trap,
            owner=testEntity,
            instanceName='dummy')
        dummy.put()
        testContent.challenges = []
        testContent.challenges.append( dummy.key())
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertIsInstance( result, trap.Trap)
        self.assertEqual( len(result.challenges), 1)
        self.assertEqual( result.challenges[0], dummy)
        

if __name__ == '__main__':
    unittest.main()    
