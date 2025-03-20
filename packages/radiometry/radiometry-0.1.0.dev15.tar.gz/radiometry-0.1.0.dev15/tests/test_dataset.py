import unittest

from radiometry import dataset, metadata


class TestEveDataset(unittest.TestCase):
    def setUp(self):
        self.dataset = dataset.EveDataset()

    def test_instantiate_class(self):
        pass

    def test_metadata_is_EveDatasetMetadata(self):
        self.assertTrue(
            isinstance(
                self.dataset.metadata,
                metadata.EveDatasetMetadata,
            )
        )


class TestDeviceData(unittest.TestCase):
    def setUp(self):
        self.device_data = dataset.DeviceData()

    def test_instantiate_class(self):
        pass

    def test_has_attributes(self):
        attributes = ["data", "axes", "metadata"]
        for attribute in attributes:
            with self.subTest(attribute=attribute):
                self.assertTrue(hasattr(self.device_data, attribute))

    def test_metadata_property_is_device_metadata(self):
        self.assertIsInstance(self.device_data.metadata, metadata.Device)
