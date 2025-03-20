#!/usr/bin/env python3
import mhi.pscad, os, logging


class Handler:

    def send(self, evt):
        if evt:
            LOG.info("%s", evt)
        else:
            LOG.info("TICK")

    def close(self):
        pass


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

# Get all installed Matlab versions
matlabs = mhi.pscad.matlab_versions()
LOG.info("Matlab Versions: %s", matlabs)

# Get the highest installed version of Matlab:
matlab = sorted(matlabs)[-1] if matlabs else ''
LOG.info("   Selected Matlab version: %s", matlab)

# Launch PSCAD
LOG.info("Launching: %s  FORTRAN=%r   Matlab=%r", version, fortran, matlab)
settings = { 'fortran_version': fortran, 'matlab_version': matlab }
pscad = mhi.pscad.launch(minimize=True, version=version, x64=x64,
                         settings=settings)

if pscad:

    handler = Handler()
    pscad.subscribe('load-events', handler)
    pscad.subscribe('build-events', handler)

    # Locate the tutorial directory
    tutorial_dir = os.path.join(pscad.examples_folder, "tutorial")
    LOG.info("Tutorial directory: %s", tutorial_dir)

    try:
        # Load only the 'voltage divider' project
        pscad.load("vdiv.pscx", folder=tutorial_dir)

        # Get the list of simulation sets
        sim_sets = pscad.simulation_sets()
        if len(sim_sets) > 0:
            LOG.info("Simulation sets: %s", sim_sets)

            # For each simulation set ...
            for sim_set_name in sim_sets:
                # ... run it
                LOG.info("Running simulation set '%s'", sim_set_name)
                sim_set = pscad.simulation_set(sim_set_name)
                sim_set.run()
                LOG.info("Simulation set '%s' complete", sim_set_name)
        else:
            # Get a list of all projects
            projects = pscad.projects()

            # Filter out libraries; only keep cases.
            cases = [prj for prj in projects if prj['type'] == 'Case']

            # For each case ...
            for case in cases:
                project = pscad.project(case['name'])

                LOG.info("Running '%s' (%s)", case['name'], case['description'])
                project.run();
                LOG.info("Run '%s' complete", case['name'])
    finally:
        # Exit PSCAD
        pscad.quit()

else:
    LOG.error("Failed to launch PSCAD")
