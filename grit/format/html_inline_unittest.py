#!/usr/bin/env python
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

'''Unit tests for grit.format.html_inline'''


import os
import re
import sys
if __name__ == '__main__':
  sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import unittest

from grit import util
from grit.format import html_inline


class HtmlInlineUnittest(unittest.TestCase):
  '''Unit tests for HtmlInline.'''

  def testGetResourceFilenames(self):
    '''Tests that all included files are returned by GetResourceFilenames.'''

    files = {
      'index.html': '''
      <!DOCTYPE HTML>
      <html>
        <head>
          <link rel="stylesheet" href="test.css">
        </head>
        <body>
          <include src="test.html">
        </body>
      </html>
      ''',

      'test.html': '''
      <include src="test2.html">
      ''',

      'test2.html': '''
      <!-- This second level resource should also be included. -->
      ''',

      'test.css': '''
      .image {
        background: url('test.png');
      }
      ''',

      'test.png': 'PNG DATA',
    }

    source_resources = set()
    tmp_dir = util.TempDir(files)
    for filename in files:
      source_resources.add(tmp_dir.GetPath(filename))

    resources = html_inline.GetResourceFilenames(tmp_dir.GetPath('index.html'))
    resources.add(tmp_dir.GetPath('index.html'))
    self.failUnlessEqual(resources, source_resources)
    tmp_dir.CleanUp()

  def testCompressedJavaScript(self):
    '''Tests that ".src=" doesn't treat as a tag.'''

    files = {
      'index.js': '''
      if(i<j)a.src="hoge.png";
      ''',
    }

    source_resources = set()
    tmp_dir = util.TempDir(files)
    for filename in files:
      source_resources.add(tmp_dir.GetPath(filename))

    resources = html_inline.GetResourceFilenames(tmp_dir.GetPath('index.js'))
    resources.add(tmp_dir.GetPath('index.js'))
    self.failUnlessEqual(resources, source_resources)
    tmp_dir.CleanUp()

  def testInlineCSSImports(self):
    '''Tests that @import directives in inlined CSS files are inlined too.
    '''

    files = {
      'index.html': '''
      <html>
      <head>
      <link rel="stylesheet" href="css/test.css">
      </head>
      </html>
      ''',

      'css/test.css': '''
      @import url('test2.css');
      blink {
        display: none;
      }
      ''',

      'css/test2.css': '''
      .image {
        background: url('../images/test.png');
      }
      '''.strip(),

      'images/test.png': 'PNG DATA'
    }

    expected_inlined = '''
      <html>
      <head>
      <style>
      .image {
        background: url('data:image/png;base64,UE5HIERBVEE=');
      }
      blink {
        display: none;
      }
      </style>
      </head>
      </html>
      '''

    source_resources = set()
    tmp_dir = util.TempDir(files)
    for filename in files:
      source_resources.add(tmp_dir.GetPath(filename))

    result = html_inline.DoInline(tmp_dir.GetPath('index.html'), None)
    resources = result.inlined_files
    resources.add(tmp_dir.GetPath('index.html'))
    self.failUnlessEqual(resources, source_resources)
    self.failUnlessEqual(expected_inlined, result.inlined_data)

    tmp_dir.CleanUp()

  def testInlineCSSLinks(self):
    '''Tests that only CSS files referenced via relative URLs are inlined.'''

    files = {
      'index.html': '''
      <html>
      <head>
      <link rel="stylesheet" href="foo.css">
      <link rel="stylesheet" href="chrome://resources/bar.css">
      </head>
      </html>
      ''',

      'foo.css': '''
      @import url(chrome://resources/blurp.css);
      blink {
        display: none;
      }
      ''',
    }

    expected_inlined = '''
      <html>
      <head>
      <style>
      @import url(chrome://resources/blurp.css);
      blink {
        display: none;
      }
      </style>
      <link rel="stylesheet" href="chrome://resources/bar.css">
      </head>
      </html>
      '''

    source_resources = set()
    tmp_dir = util.TempDir(files)
    for filename in files:
      source_resources.add(tmp_dir.GetPath(filename))

    result = html_inline.DoInline(tmp_dir.GetPath('index.html'), None)
    resources = result.inlined_files
    resources.add(tmp_dir.GetPath('index.html'))
    self.failUnlessEqual(resources, source_resources)
    self.failUnlessEqual(expected_inlined, result.inlined_data)


if __name__ == '__main__':
  unittest.main()
