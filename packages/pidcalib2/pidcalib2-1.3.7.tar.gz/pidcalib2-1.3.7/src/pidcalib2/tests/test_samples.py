###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import os
import json
from pathlib import Path
from pyxrootd import client

import pytest


@pytest.fixture
def test_path():
    return Path(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.xrootd
@pytest.mark.slow
def test_samples(test_path):
    sample_config_filepath = test_path / "../data/samples.json"
    fs = client.FileSystem("root://eoslhcb.cern.ch/")
    with open(sample_config_filepath, "rb") as f:
        samples = json.load(f)
    for name in samples.keys():
        if "2023" in name or "2024" in name:  # only check for run 3
            for s in samples[name]["sweight_dir"]:
                dirname = s.split(".ch/")[-1]
                assert fs.stat(dirname), f"{dirname} not a directory"
            for f in samples[name]["files"]:
                filepath = f.split(".ch/")[-1]
                assert fs.stat(filepath), f"{filepath} not found"
                filename = filepath.split("/")[-1]
                sweights_filename = filename.replace(".root", "_sweights.root")
                sweights_filepath = f"{dirname}{sweights_filename}"
                assert fs.stat(sweights_filepath), f"{sweights_filepath} not found"
