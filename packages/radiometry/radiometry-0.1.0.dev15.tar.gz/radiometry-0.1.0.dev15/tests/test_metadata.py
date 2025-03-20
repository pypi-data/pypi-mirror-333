import datetime
import unittest

from radiometry import metadata


class TestEveDatasetMetadata(unittest.TestCase):
    def setUp(self):
        self.metadata = metadata.EveDatasetMetadata()

    def test_instantiate_class(self):
        pass

    def test_has_measurement_metadata(self):
        self.assertTrue(
            isinstance(
                self.metadata.measurement,
                metadata.Measurement,
            )
        )

    def test_has_experiment_metadata(self):
        self.assertTrue(
            isinstance(
                self.metadata.experiment,
                metadata.Experiment,
            )
        )

    def test_has_setup_metadata(self):
        self.assertTrue(
            isinstance(
                self.metadata.setup,
                metadata.Setup,
            )
        )


class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.experiment = metadata.Experiment()

    def test_instantiate_class(self):
        pass

    def test_has_attributes(self):
        attributes = [
            "comment",
            "procedure",
        ]
        for attribute in attributes:
            with self.subTest(attribute=attribute):
                self.assertTrue(hasattr(self.experiment, attribute))

    def test_instantiate_properties_from_dict(self):
        dict_ = {
            "comment": "Lorem ipsum",
        }
        experiment = metadata.Experiment(dict_)
        for key in dict_:
            self.assertEqual(getattr(experiment, key), dict_[key])

    def test_set_properties_from_dict(self):
        dict_ = {
            "comment": "Lorem ipsum",
        }
        self.experiment.from_dict(dict_)
        for key in dict_:
            self.assertEqual(getattr(self.experiment, key), dict_[key])


class TestMeasurement(unittest.TestCase):
    def setUp(self):
        self.measurement = metadata.Measurement()

    def test_instantiate_class(self):
        pass

    def test_has_additional_attributes(self):
        attributes = [
            "start",
            "end",
            "duration",
        ]
        for attribute in attributes:
            with self.subTest(attribute=attribute):
                self.assertTrue(hasattr(self.measurement, attribute))

    def test_instantiate_properties_from_dict(self):
        dict_ = {
            "purpose": "Kill time",
            "operator": "John Doe",
            "labbook_entry": "loi:42.1001/foo/bar",
        }
        measurement = metadata.Measurement(dict_)
        for key in dict_:
            self.assertEqual(getattr(measurement, key), dict_[key])

    def test_set_properties_from_dict(self):
        dict_ = {
            "purpose": "Kill time",
            "operator": "John Doe",
            "labbook_entry": "loi:42.1001/foo/bar",
        }
        self.measurement.from_dict(dict_)
        for key in dict_:
            self.assertEqual(getattr(self.measurement, key), dict_[key])

    def test_duration_returns_correct_time_delta(self):
        now = datetime.datetime.now()
        self.measurement.start = now.replace(minute=now.minute - 1)
        self.measurement.end = now
        self.assertEqual(
            self.measurement.end - self.measurement.start,
            self.measurement.duration,
        )


class TestDevice(unittest.TestCase):
    def setUp(self):
        self.device = metadata.Device()

    def test_instantiate_class(self):
        pass

    def test_instantiate_properties_from_dict(self):
        dict_ = {"label": "foo"}
        device = metadata.Device(dict_)
        for key in dict_:
            self.assertEqual(getattr(device, key), dict_[key])

    def test_set_properties_from_dict(self):
        dict_ = {"label": "foo"}
        self.device.from_dict(dict_)
        for key in dict_:
            self.assertEqual(getattr(self.device, key), dict_[key])

    def test_has_additional_attributes(self):
        attributes = [
            "name",
            "type",
            "xmlid",
            "access",
        ]
        for attribute in attributes:
            with self.subTest(attribute=attribute):
                self.assertTrue(hasattr(self.device, attribute))


class TestScanDescription(unittest.TestCase):
    def setUp(self):
        self.scan_description = metadata.ScanDescription()

    def test_instantiate_class(self):
        pass

    def test_has_attributes(self):
        attributes = [
            "filename",
            "description",
        ]
        for attribute in attributes:
            with self.subTest(attribute=attribute):
                self.assertTrue(hasattr(self.scan_description, attribute))

    def test_instantiate_properties_from_dict(self):
        dict_ = {
            "filename": "foo",
            "description": "Lorem ipsum",
        }
        scan_description = metadata.ScanDescription(dict_)
        for key in dict_:
            self.assertEqual(getattr(scan_description, key), dict_[key])

    def test_set_properties_from_dict(self):
        dict_ = {
            "filename": "foo",
            "description": "Lorem ipsum",
        }
        self.scan_description.from_dict(dict_)
        for key in dict_:
            self.assertEqual(getattr(self.scan_description, key), dict_[key])


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.setup = metadata.Setup()

    def test_instantiate_class(self):
        pass

    def test_has_attributes(self):
        attributes = [
            "name",
            "software",
        ]
        for attribute in attributes:
            with self.subTest(attribute=attribute):
                self.assertTrue(hasattr(self.setup, attribute))

    def test_instantiate_properties_from_dict(self):
        dict_ = {
            "name": "foo",
        }
        setup = metadata.Setup(dict_)
        for key in dict_:
            self.assertEqual(getattr(setup, key), dict_[key])

    def test_set_properties_from_dict(self):
        dict_ = {
            "name": "foo",
        }
        self.setup.from_dict(dict_)
        for key in dict_:
            self.assertEqual(getattr(self.setup, key), dict_[key])


class TestEveSoftware(unittest.TestCase):
    def setUp(self):
        self.eve_software = metadata.EveSoftware()

    def test_instantiate_class(self):
        pass

    def test_has_attributes(self):
        attributes = [
            "engine_version",
            "xml_schema_version",
        ]
        for attribute in attributes:
            with self.subTest(attribute=attribute):
                self.assertTrue(hasattr(self.eve_software, attribute))

    def test_instantiate_properties_from_dict(self):
        dict_ = {"engine_version": "1.39.1", "xml_schema_version": "9.2"}
        eve_software = metadata.EveSoftware(dict_)
        for key in dict_:
            self.assertEqual(getattr(eve_software, key), dict_[key])

    def test_set_properties_from_dict(self):
        dict_ = {"engine_version": "1.39.1", "xml_schema_version": "9.2"}
        self.eve_software.from_dict(dict_)
        for key in dict_:
            self.assertEqual(getattr(self.eve_software, key), dict_[key])
