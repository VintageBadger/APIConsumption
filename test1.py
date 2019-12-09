import unittest
import apiconsumption

class Testing(unittest.TestCase):
    def test_example(self):
        a = 1
        b = 1
        self.assertEqual(a,b)

    def test_validRoute(self):
        #pass a known valid route
        output = apiconsumption.validRoute('METRO Blue Line')
        print(output)
        self.assertEqual(output, {'Description': 'METRO Blue Line', 'ProviderID': '8', 'Route': '901'})
        


if __name__ == '__main__':
    unittest.main()
