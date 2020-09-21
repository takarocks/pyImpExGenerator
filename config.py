#!/usr/bin/env python
# -*- coding: utf-8 -*-

# thumbnail
#    '^': Cut to fit, if the image is not square, longer edge is cut and fit in square
#    '' : Longer edge is used for the length and shorter edge is padded with specified 'background' color

IMAGEMAGICK = {
  'path'      : '/usr/local/bin/',
  'thumbnail' : '',
  'background': 'white',
  'outputdirs': '30Wx30H,65Wx65H,96Wx96H,300Wx300H,515Wx515H,1200Wx1200H',
  'sizes'     : '30x30,65x65,96x96,300x300,515x515,1200x1200'
}

HYBRIS = {
  'prodcatalog'   : 'electronicsProductCatalog',
  'prodcatversion': 'Staged'
}
