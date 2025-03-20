#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Base annotator class"""


from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Iterable

from lofar_station_client.common import CaseInsensitiveDict
from lofar_station_client.statistics.statistics_data import StatisticsDataFile

from lofar_stingray import __version__


class BaseAnnotator(ABC):
    """Base annotator class"""

    def __init__(self, station: str, antennafield: str, metadata_packets: Iterable):
        self._metadata_packets = metadata_packets
        self.station = station
        self.antennafield = antennafield
        self.metadata = CaseInsensitiveDict()

    def _load_metadata(self):
        """Load and prepare the metadata"""
        for packet in self._metadata_packets:
            for device, data in packet.items():
                if self.antennafield not in device.casefold():
                    continue

                device_name = device.split("/")[1]
                device_name = (
                    "antennafield" if device_name.startswith("af") else device_name
                )

                if device_name not in self.metadata:
                    data["name"] = device
                    self.metadata[device_name] = CaseInsensitiveDict(data)

    @staticmethod
    def format_timestamp(timestamp: datetime) -> str:
        """Round the given timestamp to the nearst millisecond."""
        return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

    @staticmethod
    def round_datetime_ms(timestamp: datetime) -> datetime:
        """Round the given timestamp to the nearst millisecond."""
        subtract_us = timestamp.microsecond - round(timestamp.microsecond, -3)
        return timestamp - timedelta(microseconds=subtract_us)

    @abstractmethod
    def write(self, statistics: StatisticsDataFile):
        """Store the matrices and metadata into the StatisticsDataFile"""

    @property
    @abstractmethod
    def mode(self):
        """Return the current packet mode"""

    def set_file_header(self, statistics: StatisticsDataFile):
        """Returns the header fields per HDF5 file."""

        self._load_metadata()
        statistics.station_name = self.station
        # statistics.station_version = _get_station_version(self.antennafield_device)
        statistics.writer_version = __version__
        statistics.mode = self.mode

        statistics.antennafield_device = self.metadata.get("antennafield", {}).get(
            "name", str()
        )
        statistics.antenna_names = self.metadata.get("antennafield", {}).get(
            "Antenna_Names_R", []
        )
        statistics.antenna_type = self.antennafield[:3].upper()
        statistics.rcu_pcb_id = self.metadata.get("antennafield", {}).get(
            "RCU_PCB_ID_R", []
        )
        statistics.rcu_pcb_version = self.metadata.get("antennafield", {}).get(
            "RCU_PCB_version_R", []
        )
        statistics.antenna_status = self.metadata.get("antennafield", {}).get(
            "Antenna_Status_R", []
        )  # noqa
        statistics.antenna_usage_mask = self.metadata.get("antennafield", {}).get(
            "Antenna_Usage_Mask_R", []
        )  # noqa
        statistics.antenna_reference_itrf = self.metadata.get("antennafield", {}).get(
            "Antenna_Reference_ITRF_R", []
        )  # noqa

        statistics.fpga_firmware_version = self.metadata.get("sdpfirmware", {}).get(
            "FPGA_firmware_version_R", []
        )
        statistics.fpga_hardware_version = self.metadata.get("sdpfirmware", {}).get(
            "FPGA_hardware_version_R", []
        )

        statistics.subband_frequencies = self.metadata.get("sdp", {}).get(
            "subband_frequency_R", [[]]
        )[0]
