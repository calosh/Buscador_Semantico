# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

reload(sys)
sys.setdefaultencoding('utf8')


import json
from snips_nlu import load_resources, SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_ES

import io

load_resources("es")

with io.open("dataset.json") as f:
    dataset = json.load(f)

engine = SnipsNLUEngine(config=CONFIG_ES)

engine.fit(dataset)

engine_json = json.dumps(engine.to_dict())
with io.open("trained.json", mode="w") as f:
    f.write(unicode(engine_json))