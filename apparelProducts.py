#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################
#
# apparelProducts - Apparel Products Impex Generator
#
# Author:    takarocks
# Date:      Sep 20, 2020
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

prod_catalog         = os.getenv('HYBRIS_PROD_CATALOG',config.HYBRIS['prodcatalog'])
prod_cat_version     = os.getenv('HYBRIS_PROD_CATALOG_VERSION',config.HYBRIS['prodcatversion'])

def generateImpEx(filepath):
    with open('apparelProducts.impex','w') as impex:
        impex.write('# ImPex for Importing Apparel Products\n')
        impex.write('\n')
        impex.write('$productCatalog=' + prod_catalog + '\n')
        impex.write('$ver=' + prod_cat_version + '\n')
        impex.write("$catalogVersion=catalogversion(catalog(id[default=$productCatalog]),version[default='$ver'])[unique=true,default=$productCatalog:$ver]\n")
        impex.write("$baseProduct=baseProduct(code, catalogVersion(catalog(id[default=$productCatalog]),version[default='$ver']))\n")
        impex.write("$approved=approvalstatus(code)[default='check']\n")
        impex.write("$taxGroup=Europe1PriceFactory_PTG(code)[default=eu-vat-full]\n")
        impex.write("$prices=Europe1prices[translator=de.hybris.platform.europe1.jalo.impex.Europe1PricesTranslator]\n")
        impex.write('\n')
        # MEDIA IMPORT
        impex.write('\n')

        # Open input source file then iterate for ApparelProduct, ApparelStyleVariantProduct and ApparelSizeVariantProduct

        apparelProductHeader = False
        apparelStyleVariantProductHeader = False
        apparelSizeVariantProductHeader = False
        linenumber = 0
        header = None

        f = open(filepath, 'r')
        for line in f:
            if linenumber == 0:
                # TODO: implement logic to read CSV header line
                header = line.strip().split(',')
            else:
                data = line.strip().split(',')
                if data[0] == 'ApparelProduct':
                    if not apparelProductHeader:
                        impex.write('\n### Apparel Product - generated from source file apparelProducts.csv ###\n')
                        impex.write("INSERT_UPDATE ApparelProduct;code[unique=true];unit(code)[default='pieces'];supercategories(code,$catalogVersion)[collection-delimiter=|];varianttype(code);name[lang=en];summary[lang=en];description[lang=en];ean;$prices[collection-delimiter=|];$taxGroup;$approved;genders(code);$catalogVersion\n")
                        impex.write('\n')
                        apparelProductHeader = True
                    # TODO: Currently follow the CSV format
                    apparelProductData = data[2:14]
                    for d in apparelProductData:
                        impex.write(';' + d)
                    impex.write('\n')
                if data[0] == 'ApparelStyleVariantProduct':
                    if not apparelStyleVariantProductHeader:
                        impex.write('\n### Apparel Size Variant Product - generated from source file apparelProducts.csv ###\n')
                        impex.write("INSERT_UPDATE ApparelStyleVariantProduct;code[unique=true];unit(code)[default='pieces'];supercategories(code,$catalogVersion)[collection-delimiter=|];varianttype(code);name[lang=en];summary[lang=en];description[lang=en];ean;$prices[collection-delimiter=|];$taxGroup;$approved;$baseProduct;style[lang=en];swatchColors(code);$catalogVersion\n")
                        impex.write('\n')
                        apparelStyleVariantProductHeader = True
                    # TODO: Currently follow the CSV format
                    apparelProductData = data[2:13] + data[14:17]
                    for d in apparelProductData:
                        impex.write(';' + d)
                    impex.write('\n')
                if data[0] == 'ApparelSizeVariantProduct':
                    if not apparelSizeVariantProductHeader:
                        impex.write('\n### Apparel Size Variant Product - generated from source file apparelProducts.csv ###\n')
                        impex.write("INSERT_UPDATE ApparelSizeVariantProduct;code[unique=true];unit(code)[default='pieces'];supercategories(code,$catalogVersion)[collection-delimiter=|];varianttype(code);name[lang=en];summary[lang=en];description[lang=en];ean;$prices[collection-delimiter=|];$taxGroup;$approved;$baseProduct;style[lang=en];swatchColors(code);size[lang=en];$catalogVersion\n")
                        impex.write('\n')
                        apparelSizeVariantProductHeader = True
                    # TODO: Currently follow the CSV format
                    apparelProductData = data[2:13] + data[14:18]
                    for d in apparelProductData:
                        impex.write(';' + d)
                    impex.write('\n')


            linenumber = linenumber + 1
        f.close()

def main(argv):
    msg = ''
    try:
        opts, args = getopt.getopt(argv,"f:")
    except getopt.GetoptError:
        print('python apparelProducts.py -f FILENAME')
        sys.exit(2)

    for opt, arg in opts:
        if (opt == '-f') :
            generateImpEx(arg)
        else:
            msg = 'python apparelProducts.py -f FILENAME'
            print(msg)

if __name__ == "__main__":
    main(sys.argv[1:])
