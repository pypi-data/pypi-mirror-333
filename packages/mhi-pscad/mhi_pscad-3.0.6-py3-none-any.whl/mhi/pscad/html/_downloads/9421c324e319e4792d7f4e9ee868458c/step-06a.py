#!/usr/bin/env python3
import mhi.pscad, os, logging

# Log 'INFO' messages & above.  Include level & module name.
logging.basicConfig(level=logging.INFO,
                    format="%(levelname)-8s %(name)-26s %(message)s")

# Ignore INFO msgs from automation (eg, mhi.pscad, mhi.common, ...)
logging.getLogger('mhi').setLevel(logging.WARNING)

LOG = logging.getLogger('main')

versions = mhi.pscad.versions()
LOG.info("PSCAD Versions: %s", versions)

# Skip any 'Alpha' versions, if other choices exist
vers = [(ver, x64) for ver, x64 in versions if ver != 'Alpha']
if len(vers) > 0:
    versions = vers

# Skip any 'Beta' versions, if other choices exist
vers = [(ver, x64) for ver, x64 in versions if ver != 'Beta']
if len(vers) > 0:
    versions = vers

# Skip any 32-bit versions, if other choices exist
vers = [(ver, x64) for ver, x64 in versions if x64]
if len(vers) > 0:
    versions = vers

LOG.info("   After filtering: %s", versions)

# Of any remaining versions, choose the "lexically largest" one.
version, x64 = sorted(versions)[-1]
LOG.info("   Selected PSCAD version: %s %d-bit", version, 64 if x64 else 32)

# Get all installed FORTRAN compiler versions
fortrans = mhi.pscad.fortran_versions()
LOG.info("FORTRAN Versions: %s", fortrans)

# Skip 'GFortran' compilers, if other choices exist
vers = [ver for ver in fortrans if 'GFortran' not in ver]
if len(vers) > 0:
    fortrans = vers

LOG.info("   After filtering: %s", fortrans)

# Order the remaining compilers, choose the last one (highest revision)
fortran = sorted(fortrans)[-1]
LOG.info("   Selected FORTRAN version: %s", fortran)


# Launch PSCAD
LOG.info("Launching: %s  FORTRAN=%r", version, fortran)
settings = { 'fortran_version': fortran }
pscad = mhi.pscad.launch(minimize=True, version=version, x64=x64,
                         settings=settings)

if pscad:

    # Locate the tutorial directory
    tutorial_dir = os.path.join(pscad.examples_folder, "tutorial")
    LOG.info("Tutorial directory: %s", tutorial_dir)

    try:
        # Load the tutorial workspace
        pscad.load("Tutorial.pswx", folder=tutorial_dir)

        # Run all the simulation sets in the workspace
        pscad.run_all_simulation_sets()

    finally:
        # Exit PSCAD
        pscad.quit()

else:
    LOG.error("Failed to launch PSCAD")
