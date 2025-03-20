"""
Datasets: units containing data and metadata.

The dataset is one key concept of the ASpecD framework and hence the radiometry
package derived from it, consisting of the data as well as the corresponding
metadata. Storing metadata in a structured way is a prerequisite for a
semantic understanding within the routines. Furthermore, a history of every
processing, analysis and annotation step is recorded as well, aiming at a
maximum of reproducibility. This is part of how the ASpecD framework and
therefore the radiometry package tries to support good scientific practice.

Therefore, each processing and analysis step of data should always be
performed using the respective methods of a dataset, at least as long as it
can be performed on a single dataset.


Datasets
========

Generally, there are two types of datasets: Those containing experimental
data and those containing calculated data.

However, in case of the radiometry package dealing with many different kinds of
datasets due to the very general nature of the measurement program (eve) used
at the PTB in Berlin and the quite different kinds of measurements, the
hierarchy of datasets deviates from the typical scenario in ASpecD.

For the time being, there is one dataset representing all information that can
possibly be contained in a measurement file (eve HDF5 file):

  * :class:`EveDataset`


Dataset factory
===============

Particularly in case of recipe-driven data analysis (c.f. :mod:`aspecd.tasks`),
there is a need to automatically retrieve datasets using nothing more than a
source string that can be, e.g., a path or LOI. This is where the
DatasetFactory comes in. This is a factory in the sense of the factory
pattern described by the "Gang of Four" in their seminal work, "Design
Patterns" (Gamma et al., 1995):

  * :class:`DatasetFactory`


Module documentation
====================
"""

import aspecd.dataset

from radiometry import metadata


class EveDataset(aspecd.dataset.Dataset):
    """
    Representation of the data and metadata contained in an eve HDF5 file.

    The idea behind this class is to represent all possible data and metadata
    contained in an eve HDF5 file, regardless of the kind of measurement
    actually performed. Therefore, dedicated other dataset classes need to be
    developed that are purpose-built for more specific kinds of measurements.

    .. note::

        This class should become the central interface between eve HDF5 files
        and processing and analysis routines, together with the corresponding
        importer. Hence, these two classes need to reflect any further update
        of the eve HDF5 format. In accord with the open-closed principle, the
        :class:`EveDataset` should only be extended, but not change existing
        structures to not impair backward compatibility.

    While representing all possible data and metadata, this class is *not* a
    mere reimplementation of the eve HDF5 file structure, but an abstraction
    taking into account the concepts of the ASpecD framework.

    For a convenient overview of the structure of this dataset, see the
    :doc:`dataset structure </dataset-structure>`.

    Attributes
    ----------
    metadata : :class:`radiometry.metadata.EveDatasetMetadata`
        Hierarchical structure containing all relevant metadata

    """

    def __init__(self):
        super().__init__()
        self.metadata = metadata.EveDatasetMetadata()


class DeviceData(aspecd.dataset.DeviceData):
    """
    One sentence (on one line) describing the class.

    More description comes here...


    Attributes
    ----------
    metadata : :class:`radiometry.metadata.Device`
        Metadata of the device used to record the additional data

    """

    def __init__(self):
        super().__init__()
        self.metadata = metadata.Device()
