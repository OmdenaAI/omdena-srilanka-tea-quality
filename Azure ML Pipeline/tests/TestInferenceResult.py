import unittest

from api.resources.inference import InferenceResult
from classify import ClassifierPrediction

class TestInferenceResult(unittest.TestCase):
    
    def test_ctor_with_status_and_msg(self):
        ir = InferenceResult(status='status', msg='msg')
        self.assertEqual(ir.status, 'status', "Expected 'status'")
        self.assertEqual(ir.msg, 'msg', "Expected 'msg'")
        self.assertIsNone(ir.predictions, 'Expected None')
        
    def test_ctor_with_status_and_msg_predictions(self):
        class_percents = {
            'Withered_Best': 60.0,
            'Withered_Below_Best': 15.0,
            'Withered_Poor': 25.0
        }
        cp = ClassifierPrediction(class_percents=class_percents)
        ir = InferenceResult(status='success', msg='image processed', predictions=cp)
        self.assertEqual(ir.status, 'success', "Expected 'success'")
        self.assertEqual(ir.msg, 'image processed', "Expected 'image processed'")
        self.assertIsNotNone(ir.predictions, 'Expected not None')
    
    def test_serialize_return_expected_dict(self):
        class_percents = {
            'Withered_Best': 60.0,
            'Withered_Below_Best': 15.0,
            'Withered_Poor': 25.0
        }
        cp = ClassifierPrediction(class_percents=class_percents)
        ir = InferenceResult(status='success', msg='image processed', predictions=cp)
        
        res = ir.serialize()

        exp_dict = {
            'status': 'success',
            'msg': 'image processed',
            'predictions': {
                "type": "Withered",
                "categories": {
                    "best": 60.0,
                    "below_best": 15.0,
                    "poor": 25.0
                }
            }
        }

        self.assertDictEqual(res, exp_dict, "Expected correct dict")

if __name__ == "__main__":
    unittest.main()