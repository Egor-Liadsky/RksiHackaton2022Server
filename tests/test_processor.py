from unittest import TestCase

import database.processor


class TestDataProcessor(TestCase):
    def test_validate(self):
        database.processor.DataProcessor().validate()
