import unittest

from classify import ClassifierPrediction

class TestClassifierPrediction(unittest.TestCase):
    
    def test_ctor_with_class_percents_none(self):
        cp = ClassifierPrediction(class_percents=None)
        self.assertIsNone(cp.type, "Expected type to be None")
        self.assertDictEqual(cp.categories, {}, "Expected categories to be empty")

    def test_ctor_with_class_percents_empty(self):
        cp = ClassifierPrediction(class_percents={})
        self.assertIsNone(cp.type, "Expected type to be None")
        self.assertDictEqual(cp.categories, {}, "Expected categories to be empty")

    def test_ctor_with_class_percents_withered_best_only(self):
        class_percents = {
            'Withered_Best': 100.0
        }
        cp = ClassifierPrediction(class_percents=class_percents)
        self.assertEqual(cp.type, "Withered", "Expected type to be 'Withered'")
        self.assertDictEqual(cp.categories, {'best':100.0}, "Expected categories to be best:100.0")

    def test_ctor_with_class_percents_withered_all_categories(self):
        class_percents = {
            'Withered_Best': 60.0,
            'Withered_Below_Best': 15.0,
            'Withered_Poor': 25.0
        }
        cp = ClassifierPrediction(class_percents=class_percents)
        self.assertEqual(cp.type, "Withered", "Expected type to be 'Withered'")
        exp_categories = {
            'best':60.0,
            'below_best':15.0,
            'poor':25.0
        }
        self.assertDictEqual(cp.categories, exp_categories, "Expected categories to include all categories")

    def test_ctor_with_class_percents_fresh_best_only(self):
        class_percents = {
            'Fresh_Best': 100.0
        }
        cp = ClassifierPrediction(class_percents=class_percents)
        self.assertEqual(cp.type, "Fresh", "Expected type to be 'Fresh'")
        self.assertDictEqual(cp.categories, {'best':100.0}, "Expected categories to be best:100.0")

    def test_ctor_with_class_percents_fresh_all_categories(self):
        class_percents = {
            'Fresh_Best': 60.0,
            'Fresh_Below_Best': 15.0,
            'Fresh_Poor': 25.0
        }
        cp = ClassifierPrediction(class_percents=class_percents)
        self.assertEqual(cp.type, "Fresh", "Expected type to be 'Fresh'")
        exp_categories = {
            'best':60.0,
            'below_best':15.0,
            'poor':25.0
        }
        self.assertDictEqual(cp.categories, exp_categories, "Expected categories to include all categories")

    def test_serialize_return_expected_dict(self):
        class_percents = {
            'Fresh_Best': 60.0,
            'Fresh_Below_Best': 15.0,
            'Fresh_Poor': 25.0
        }
        cp = ClassifierPrediction(class_percents=class_percents)
        
        res = cp.serialize()

        exp_dict = {"type": "Fresh", "categories": {"best": 60.0, "below_best": 15.0, "poor": 25.0}}
        self.assertDictEqual(res, exp_dict, "Expected correct dict")


if __name__ == "__main__":
    unittest.main()