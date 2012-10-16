#!/usr/bin/env python
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Formats as a .json file that can be used to localize Google Chrome
extensions."""

import re
import types

from grit import util
from grit.format import interface
from grit.node import message

class StringTable(interface.ItemFormatter):
  """Writes out the string table."""

  def Format(self, item, lang='en', output_dir='.'):
    out = []
    out.append('{\n')

    format = ('  "%s": {\n'
              '    "message": "%s"\n'
              '  }')
    for child in item.children:
      if isinstance(child, message.MessageNode):
        loc_message = child.Translate(lang)
        loc_message = re.sub(r'\\', r'\\\\', loc_message)
        loc_message = re.sub(r'"', r'\"', loc_message)

        id = child.attrs['name']
        if id.startswith('IDR_'):
          id = id[4:]

        if len(out) > 1:
          out.append(',\n')
        out.append(format % (id, loc_message))

    out.append('\n}\n')
    return ''.join(out)
