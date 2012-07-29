import unittest

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent


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

    def testInsertHydraUser(self):
        emailAddr='testInsertEntity0@hydrauser.com'
        hydrauser.create_hydra_user(users.User(email=emailAddr))
        
        result = hydrauser.get_hydra_user(emailAddr)
        self.assertIsNotNone(result)
        self.assertEqual(result.userID.email(), emailAddr)

    def testLoadAllHydraUsers(self):
        emailAddrs=['testLoadAllHydraUsers0@hydrauser.com',
                    'testLoadAllHydraUsers1@hydrauser.com',
                    'testLoadAllHydraUsers2@hydrauser.com']
        for eAddr in emailAddrs:
            hydrauser.create_hydra_user(users.User(email=eAddr))

        result = hydrauser.load_hydra_users()
        self.assertIsNotNone(result)
        self.assertEqual(len(result), len(emailAddrs))

    def testAddRemoveOwnership(self):
        eAddrs=['testAddOwnership0@hydrauser.com',
                    'testAddOwnership1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "testAddRemoveOwnership"
        testContent = hydracontent.create_hydra_content( hydracontent.HydraContent,
                            owner=origPub,
                            originalPublisher=origPub,
                            instanceName=testName)
        testContent.put()
        
        testEntity.add_ownership(testContent)
        self.assertEqual( len(testEntity.contentKeys), 1)

        content = db.get( testEntity.contentKeys[0])
        self.assertEqual(content.owner, testEntity)
        self.assertEqual(content.originalPublisher, origPub)
        self.assertEqual(content.instanceName, testName)

        testEntity.remove_access(testContent) # should not remove anything
        self.assertEqual( len(testEntity.contentKeys), 1)

        testEntity.remove_access(content)
        self.assertEqual( len(testEntity.contentKeys), 0)

if __name__ == '__main__':
    unittest.main()    
