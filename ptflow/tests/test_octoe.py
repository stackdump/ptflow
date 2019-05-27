import os
import json
import unittest
import ptflow
from ptflow.storage.pgsql import Storage

class OctoeTestCase(unittest.TestCase):

    def setUp(self):
        ptflow.initialize(Storage)
        self.m = ptflow.eventstore('octoe')

    def tearDown(self):
        self.m.drop()

    def test_guards(self):
        def x_fail(action):
            res = self.m(action, roles=['*'])
            #print(action, res)
            self.assertIsNotNone(res[2])

        def x_pass(action):
            res = self.m(action, roles=['*'])
            #print(self.m.event(res[0]))
            #print(action, res)
            #print(self.m.state())
            self.assertIsNone(res[2])

        x_fail('OFF')
        x_fail('EXEC')
        x_pass('ON')
        x_pass('EXEC')

if __name__ == '__main__':
    unittest.main()
