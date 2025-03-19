# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
from lino.api import dd, rt
from lino.modlib.uploads.mixins import make_uploaded_file

try:
    from lino_book import DEMO_DATA
except ImportError:
    DEMO_DATA = None

def walk(p):
    # print("20230331", p)
    for c in sorted(p.iterdir()):
        if c.is_dir():
            for cc in walk(c):
                yield cc
        else:
            yield c

def objects():
    
    if DEMO_DATA is None:
        # logger.info("No demo data because lino_book is not installed")
        return
    if not dd.plugins.uploads.with_volumes:
        return

    Upload = rt.models.uploads.Upload
    Volume = rt.models.uploads.Volume

    def load_vol(root_dir, ref, desc, **kwargs):
        vol = Volume(ref=ref, description=desc, root_dir=root_dir)
        yield vol
        kwargs.update(volume=vol)
        chop = len(str(root_dir)) + 1
        for fn in walk(root_dir):
            fns = str(fn)[chop:]
            # print("20230325 {}".format(fn))
            yield Upload(
                library_file=fns,
                description=fns.replace('_', ' ').replace('/', ' '),
                **kwargs)

    if dd.is_installed('sources'):
        yield (luc := rt.models.sources.Author(first_name="Luc", last_name="Saffre"))
        yield (source := rt.models.sources.Source(
            author=luc, year_published="2022", title="Private collection"))
        yield load_vol(DEMO_DATA / 'photos', "photos", "Photo album", source=source)

    yield load_vol(DEMO_DATA / 'screenshots', "screenshots", "Screenshots")
