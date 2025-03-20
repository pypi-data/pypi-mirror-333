#!/usr/bin/env python3
import mhi.pscad

pscad = mhi.pscad.launch(minimize=True)

for key, value in sorted(pscad.settings().items()):
    print("%33s: %s" % (key, value))

pscad.quit()
