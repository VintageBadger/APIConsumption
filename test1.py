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
        #print(output)
        self.assertEqual(output, {'Description': 'METRO Blue Line', 'ProviderID': '8', 'Route': '901'})
        
    def test_validDirection(self):
        output = apiconsumption.validDirection({'Description': 'METRO Blue Line', 'ProviderID': '8', 'Route': '901'}, 'south')
        #print(output)
        self.assertEqual(output, {'Text': 'SOUTHBOUND', 'Value': '1'})
    
    def test_invalidDirection(self):
        output = apiconsumption.validDirection({'Description': 'METRO Blue Line', 'ProviderID': '8', 'Route': '901'}, 'west')
        #print(output)
        self.assertEqual(output, None)
    
    def test_validStop(self):
        output = apiconsumption.validStop(
            {'Description': 'METRO Blue Line', 'ProviderID': '8', 'Route': '901'},
            {'Text': 'SOUTHBOUND', 'Value': '1'},
            "Target Field Station Platform 1"
        )
        #print(output)
        self.assertEqual(output, {'Text': 'Target Field Station Platform 1', 'Value': 'TF12'})


if __name__ == '__main__':
    unittest.main()
