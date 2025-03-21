# SPDX-FileCopyrightText: 2024-present Proxima Fusion GmbH <info@proximafusion.com>
#
# SPDX-License-Identifier: MIT
"""How to run VMEC++ via the Python API."""

from pathlib import Path

import vmecpp

# NOTE: This resolves to src/vmecpp/cpp/vmecpp/test_data in the repo.
TEST_DATA_DIR = (
    Path(__file__).parent.parent / "src" / "vmecpp" / "cpp" / "vmecpp" / "test_data"
)


def run_vmecpp():
    # We need a VmecInput, a Python object that corresponds
    # to the classic "input.*" files.
    # We can construct it from such a classic VMEC input file
    # (Fortran namelist called INDATA):
    input_file = TEST_DATA_DIR / "input.solovev"
    input = vmecpp.VmecInput.from_file(input_file)

    # Now we can run VMEC++:
    output = vmecpp.run(input)
    # An optional parameter max_threads=N controls
    # the level of parallelism in VMEC++.
    # By default, VMEC++ runs with max_threads equal
    # to the number of logical cores on the machine.
    # Note that the actual level of parallelism is
    # limited so that each thread operates on at
    # least two flux surfaces, so VMEC++ might use
    # less threads than max_threads if there are
    # few flux surfaces.

    # We can save the output wout as a classic NetCDF
    # wout file if needed:
    output.wout.save("wout_solovev.nc")

    # Free-boundary runs work just the same, in which
    # case VmecInput will also include a path to an
    # "mgrid_*.nc" file produced by MAKEGRID.


if __name__ == "__main__":
    run_vmecpp()
