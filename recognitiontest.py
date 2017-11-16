#! /usr/bin/env python3

from adstrip.recognition import TemplateRecognizer

tr = TemplateRecognizer()
tr.test('screengrab.png', 'patterns/cnn_live.png')
