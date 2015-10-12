import unittest
from ClassStandingClassifierStuff.ClassifyClassStatusTrainFirst import ClassifyClassStatusTrainFirst


class TestStringMethods(unittest.TestCase):
    def test_trainFreshmanModel(self):
        testClassify = ClassifyClassStatusTrainFirst(classStatus='Freshman', trainingPercentage=0.99,
                                           modelSaveFile='ClassifierTrainedModels\FreshmanClassStatusTrainedLRModel')
        testClassify.trainAndSaveModel()


if __name__ == '__main__':
    unittest.main()
