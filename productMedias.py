#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################
#
# productMedias - Product Media Impex Generator
#
# Author:    takarocks
# Date:      Aug 29, 2020
# Version:   0.1
# Python:    3.7.x
#
#######################################

import sys
import getopt
import config
import os
import subprocess
import shutil

thumbnail       = os.getenv('IMAGEMAGICK_THUMBNAIL',config.IMAGEMAGICK['thumbnail'])
imagemagick_bin = os.getenv('IMAGEMAGICK_PATH',config.IMAGEMAGICK['path'])
background      = os.getenv('IMAGEMAGICK_BACKGROUND',config.IMAGEMAGICK['background'])
outputdirs      = tuple(os.getenv('IMAGEMAGICK_OUTPUTDIRS',config.IMAGEMAGICK['outputdirs']).split(','))
sizes           = tuple(os.getenv('IMAGEMAGICK_SIZES',config.IMAGEMAGICK['sizes']).split(','))

catalog         = os.getenv('HYBRIS_CATALOG',config.HYBRIS['catalog'])

def generateImpEx(filepath):
    with open('productMedia.impex','w') as impex:
        impex.write('# ImPex for Importing Product Media\n')
        impex.write('\n')
        impex.write('$productCatalog=' + catalog + '\n')
        impex.write('$ver=Staged\n')
        impex.write("$catalogVersion=catalogversion(catalog(id[default=$productCatalog]),version[default='$ver'])[unique=true,default=$productCatalog:$ver]\n")
        impex.write('$siteResource=file:////home/hybris/hybris/temp/images\n')
        impex.write('\n')
        impex.write('$thumbnail=thumbnail(code, $catalogVersion)\n')
        impex.write('$picture=picture(code, $catalogVersion)\n')
        impex.write('$thumbnails=thumbnails(code, $catalogVersion)\n')
        impex.write('$detail=detail(code, $catalogVersion)\n')
        impex.write('$normal=normal(code, $catalogVersion)\n')
        impex.write('$others=others(code, $catalogVersion)\n')
        impex.write('$data_sheet=data_sheet(code, $catalogVersion)\n')
        impex.write('$medias=medias(code, $catalogVersion)\n')
        impex.write('$galleryImages=galleryImages(qualifier, $catalogVersion)\n')
        # MEDIA IMPORT
        impex.write('\n')
        impex.write('### MEDIA IMPORT ###\n')
        impex.write("INSERT_UPDATE Media;mediaFormat(qualifier);code[unique=true];@media[translator=de.hybris.platform.impex.jalo.media.MediaDataTranslator];realfilename;mime;$catalogVersion;folder(qualifier)[default=images]\n")
        f = open(filepath, 'r')
        for line in f:
            input = line.strip().split(',')
            format = 'image/jpeg'
            if (input[1].split('.')[1] == 'png'):
                format = 'image/png'
            for d in outputdirs:
                impex.write(';' + d + ';' + d + '/' + input[1] + ';$siteResource/' + d + '/' + input[1] + ';' + input[1] + ';' + format + '\n')
        f.close()

        # MEDIA CONTAINER
        impex.write('\n')
        impex.write('### MEDIA IMPORT ###\n')
        impex.write("INSERT_UPDATE MediaContainer;qualifier[unique=true];$medias[collection-delimiter = ,];$catalogVersion;\n")
        f = open(filepath, 'r')
        for line in f:
            input = line.strip().split(',')
            container = ';' + input[1].split('.')[0] + '-container;'
            for i in range(len(outputdirs)):
                container = container + outputdirs[i] + '/' + input[1]
                if i < len(outputdirs) - 1:
                    container = container + ','
            impex.write(container + '\n')
        f.close()

        # PRODUCT MEDIA
        impex.write('\n')
        impex.write('### PRODUCT MEDIA UPDATE ###\n')
        impex.write("UPDATE Product;code[unique=true];$picture;$thumbnail;$galleryImages;$catalogVersion;;\n")
        f = open(filepath, 'r')
        for line in f:
            input = line.strip().split(',')
            impex.write(';' + input[0] + ';300Wx300H/' + input[1] + ';96Wx96H/' + input[1] + ';' + input[1].split('.')[0] + '-container\n')
        f.close()

def createImageDirectories():
    for d in outputdirs:
        if not os.path.isdir('images/' + d):
            os.makedirs('images/' + d)

def convertMedias(media):
    cwd = os.getcwd()
    for i in range(len(sizes)):
        cmd = [imagemagick_bin + 'convert',media,'-thumbnail',sizes[i] + thumbnail,'-background',background,'-gravity','center','-extent',sizes[i],'images/' + outputdirs[i] + '/' + media]
        print(cmd)
        subprocess.call(cmd, shell=False)
    shutil.make_archive('images', 'zip', root_dir='.', base_dir='images')

def main(argv):
    msg = ''
    try:
        opts, args = getopt.getopt(argv,"f:")
    except getopt.GetoptError:
        print('python productMedias.py -f FILENAME')
        sys.exit(2)

    for opt, arg in opts:
        if (opt == '-f') :
            createImageDirectories()
            f = open(arg, 'r')
            for line in f:
                media = line.strip().split(',')[1]
                print(media)
                convertMedias(media)
            f.close()
            generateImpEx(arg)
        else:
            msg = 'python productMedias.py -f FILENAME'
            print(msg)

if __name__ == "__main__":
    main(sys.argv[1:])
