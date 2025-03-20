"""
Metadata: Information on numeric data stored in a structured way.

Metadata
========

In this module, the individual metadata classes are defined which contain the
metadata for the different types of datasets:

  * :class:`EveDatasetMetadata`

What may sound like a minor detail is one key aspect of the radiometry package:
The metadata and their structure provide a **unified interface for all
functionality operating on datasets**. Reproducible research
is only possible if all information necessary is always recorded, and this
starts with all the metadata accompanying a measurement. Defining what kind
of metadata is important and needs to be recorded, together with metadata
formats easily writable by the experimenters *during* recording the data
requires a thorough understanding of both, the method and the setup(s) used.
For an overview of the structures of the dataset classes and their
corresponding metadata, see the :doc:`dataset structure </dataset-structure>`
section.


Module documentation
====================
"""
import datetime

import aspecd.metadata


class EveDatasetMetadata(aspecd.metadata.ExperimentalDatasetMetadata):
    """
    Set of all metadata for a dataset object representing an eve HDF5 file.

    Metadata as a unified structure of information coupled to the dataset are
    necessary for the understanding, analysis and processing of data.


    Attributes
    ----------
    experiment : :class:`Experiment`
        Metadata of the experiment carried out

    measurement : :class:`Measurement`
        Metadata of the measurement as a result of carrying out the experiment

    setup : :class:`Setup`
        Metadata of the setup the experiment was carried out on

    """

    def __init__(self):
        super().__init__()
        self.experiment = Experiment()
        self.measurement = Measurement()
        self.setup = Setup()


class Experiment(aspecd.metadata.Metadata):
    """
    General information available for an experiment.

    In contrast to :class:`Measurement`, an experiment is a more general
    description of an experiment, while a measurement is the act/result of
    performing such an experiment.


    Attributes
    ----------
    comment : :class:`str`
        Comment on the level of the entire experiment

        In contrast to comments during a measurement that are added to the
        list of :attr:`aspecd.dataset.Dataset.annotations` (and dubbed "life
        comment" or "log message" in eve), a comment on this level refers to
        the experiment as such.

    procedure : :class:`ScanDescription`
        Actionable description of the procedure underlying the experiment

    """

    def __init__(self, dict_=None):
        self.comment = ""
        self.procedure = ScanDescription()
        super().__init__(dict_=dict_)


class Measurement(aspecd.metadata.Measurement):
    """
    General information available for each type of measurement.

    .. note::

        Currently, only a relevant subset of the attributes of the class are
        documented here. For a full list of attributes, see the documentation
        of the parent class :class:`aspecd.metadata.Measurement`.

    Attributes
    ----------
    start : `datetime.datetime`
        Date and time of start of measurement

    end : `datetime.datetime`
        Date and time of end of measurement

    """

    @property
    def duration(self):
        """
        Duration of the measurement.

        Returns
        -------
        duration : :class:`datetime.timedelta`
            Time difference between start and end of measurement

            .. note::

                If either :attr:`start` or :attr:`end` are not set (*e.g.*, as
                a result of reading a file with eveH5 structure version <7),
                the result (and correspondingly the return type) is ``None``.

        """
        if self.start and self.end:
            return self.end - self.start


class Device(aspecd.metadata.Device):
    """
    Information on the device contributing device data.

    This class contains the metadata of the corresponding devices whose
    data are of type :class:`radiometry.dataset.DeviceData`. That class
    contains an attribute :attr:`radiometry.dataset.DeviceData.metadata`.


    Attributes
    ----------
    name : :class:`str`
        Name of the device

        TODO: What is this name? And how does it differ from :attr:`label`?

    type : :class:`str`
        Device type

        Channel or Axis

        TODO: Needs to become an enum type

    xmlid : :class:`str`
        XML id

        Some more description is necessary.

    access : :class:`str`
        PV name for CA

        Some more description is necessary.

    """

    def __init__(self, dict_=None):
        self.name = ""
        self.type = ""
        self.xmlid = ""
        self.access = ""
        super().__init__(dict_=dict_)


class ScanDescription(aspecd.metadata.Metadata):
    """
    Actionable description of a scan used in a measurement.

    A scan in eve is described using an XML file with a specific schema termed
    "SCML".

    .. note::

        Depending on the actual requirements, this class may eventually do much
        more than being a container for SCML files. Possible behaviour includes
        (partially) parsing the contained SCML/XML and extracting information,
        such as a list of devices.


    Attributes
    ----------
    filename : :class:`str`
        Name of the SCML file describing the scan.

    description : :class:`str`
        Actual description of the scan.

        This is the (multiline) string containing the actual XML/SCML.

    """

    def __init__(self, dict_=None):
        self.filename = ""
        self.description = ""
        super().__init__(dict_=dict_)


class Setup(aspecd.metadata.Metadata):
    """
    General information of the setup an experiment was carried out on.

    The setup is basically the sum of the hardware used to carry out an
    experiment resulting in a measurement/measured data.

    Attributes
    ----------
    name : :class:`str`
        Descriptive and concise name of the setup

        Example: Name of the beamline.

        Hint: This information is typically contained in the ``Location``
        attribute of the eveH5 file.

    """

    def __init__(self, dict_=None):
        self.name = ""
        self.software = EveSoftware()
        super().__init__(dict_=dict_)


class EveSoftware(aspecd.metadata.Metadata):
    """
    General information regarding the eve software used at the setup.

    More description comes here...

    TODO: Decide whether to add the version number of the eveH5 file format
    as well.


    Attributes
    ----------
    engine_version : :class:`str`
        Version number of the evEngine used at the setup

    xml_schema_version : :class:`str`
        Version number of the XML schema the setup description and SCML files
        are validated against

    """

    def __init__(self, dict_=None):
        self.engine_version = ""
        self.xml_schema_version = ""
        super().__init__(dict_=dict_)
