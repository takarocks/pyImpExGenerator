#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################
#
# productMedias - Product Media Impex Generator
#
# Author:    takarocks
# Date:      Aug 29, 2020
# Version:   0.2
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
    with open('productMedias.impex','w') as impex:
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
            # Split by comma and get images
            input = line.strip().split(',')
            # 0.2 Split by pipe | to get multiple images
            images = input[1].strip().split('|')
            for image in images:
                format = 'image/jpeg'
                if (image.split('.')[1].lower() == 'png'):
                    format = 'image/png'
                for d in outputdirs:
                    impex.write(';' + d + ';' + d + '/' + image + ';$siteResource/' + d + '/' + image + ';' + image + ';' + format + '\n')
        f.close()

        # MEDIA CONTAINER
        impex.write('\n')
        impex.write('### MEDIA IMPORT ###\n')
        impex.write("INSERT_UPDATE MediaContainer;qualifier[unique=true];$medias[collection-delimiter = ,];$catalogVersion;\n")
        f = open(filepath, 'r')
        for line in f:
            # Split by comma and get images9
            input = line.strip().split(',')
            # 0.2 Split by pipe | to get multiple images
            images = input[1].strip().split('|')
            for image in images:
                container = ';' + image.split('.')[0] + '-container;'
                for i in range(len(outputdirs)):
                    container = container + outputdirs[i] + '/' + image
                    if i < len(outputdirs) - 1:
                        container = container + ','
                impex.write(container + '\n')
        f.close()

        # PRODUCT MEDIA
        impex.write('\n')
        impex.write('### PRODUCT MEDIA UPDATE ###\n')
#        impex.write("UPDATE Product;code[unique=true];$picture;$thumbnail;$galleryImages;$catalogVersion;;\n")
        impex.write("UPDATE Product;code[unique=true];$picture;$thumbnail;$normal;$detail;$thumbnails;$others;$galleryImages;$catalogVersion;;\n")
        f = open(filepath, 'r')
        for line in f:
            input = line.strip().split(',')
            # 0.2 Split by pipe | to get multiple images, iterate for containers but use the first one for other images
            images = input[1].strip().split('|')
            # code
            impex.write(';' + input[0])
            # picture
            impex.write(';300Wx300H/' + images[0])
            # thumbnail
            impex.write(';96Wx96H/' + images[0])
            # normal
            impex.write(';300Wx300H/' + images[0])
            # detail
            impex.write(';1200Wx1200H/' + images[0])
            # thumbnails
            impex.write(';96Wx96H/' + images[0])
            # others
            impex.write(';1200Wx1200H/' + images[0] + ',515Wx515H/' + images[0] + ',300Wx300H/' + images[0] + ',96Wx96H/' + images[0] + ',65Wx65H/' + images[0] + ',30Wx30H/' + images[0])
            # galleryImages
            impex.write(';')
            i = 1
            for image in images:
                print(image)
                impex.write(image.split('.')[0] + '-container')
                if i < len(images):
                    impex.write(',')
                else:
                    impex.write('\n')
                i = i + 1
        f.close()

def createImageDirectories():
    for d in outputdirs:
        if not os.path.isdir('images/' + d):
            os.makedirs('images/' + d)

def convertMedias(media):
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
