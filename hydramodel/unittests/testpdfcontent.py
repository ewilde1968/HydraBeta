import unittest

from google.appengine.api import users
from google.appengine.ext import testbed

from hydramodel import hydrauser
from hydramodel import hydracontent
from hydramodel import pdfcontent


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

    def testInsertPDFContent(self):
        emailAddr='testInsertPDFContent0@hydrauser.com'
        testEntity = hydrauser.create_hydra_user(users.User(email=emailAddr))

        testContent = hydracontent.create_hydra_content(
                            pdfcontent.PDFContent,
                            owner=testEntity)
        testContent.put()

        result = hydracontent.load_hydra_content( testEntity)
        self.assertIsNotNone(result)
        self.assertEqual( len(result), 1)
        self.assertEqual( result[0].owner, testEntity)
        self.assertIsInstance( result[0], pdfcontent.PDFContent)

    def testCloneGameSystem(self):
        eAddrs=['testInsertPDFContent0@hydrauser.com',
                'testInsertPDFContent1@hydrauser.com']
        testEntity = hydrauser.create_hydra_user(users.User(email=eAddrs[0]))
        origPub = hydrauser.create_hydra_user(users.User(email=eAddrs[1]))

        testName = "testInsertPDFContent"
        testContent = hydracontent.create_hydra_content(
                            pdfcontent.PDFContent,
                            owner=origPub,
                            originalPublisher=origPub,
                            instanceName = testName)
        testContent.put()

        result = testContent.clone( testEntity)
        self.assertIsNot( result, testContent)
        self.assertEqual(result.owner, testEntity)
        self.assertEqual(result.originalPublisher, origPub)
        self.assertEqual(result.instanceName, testName)
        self.assertIsInstance( result, pdfcontent.PDFContent)


if __name__ == '__main__':
    unittest.main()    
