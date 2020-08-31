# pyImpExGenerator
Python SAP Commerce Cloud ImpEx generator

# Prerequisite
* ImageMagick
* Python 3.7 or higher

# Version
* 0.1
  * Product medias impex including imagemagick conversion

# How to use
## Product Media ImpEx generation

### Output images

| Format | Thumbnail Option | Image |
|--|--|--|
| Source | N/A | <kbd><img src='_assets/P8150790-original.jpg'/></kbd> |
| Cut | ^ | <kbd><img src='_assets/P8150790-cut.jpg'/></kbd> |
| Padded | (blank) |  <kbd><img src='_assets/P8150790-padded.jpg'/></kbd> |


### Steps

  1. Configure *config.py* and *input.csv*. See following Configuration section for more details.
  2. Locate your source images in your python program execution directory. Do not locate the files in any subdirectory.
  3. Open Terminal or Command Prompt and execute python program as follows

     `python productMedias -f input.csv`
  4. Confirm two files produced, *images.zip* and *productMedia.impex*. You can ignore/delete images directories.
  5. Upload and extract *images.zip* onto your Commerce instance under /home/hybris/hybris/temp. Following directories are populated along with converted medias.

     ```
     images
     ├── 1200Wx1200H
     │   └── 289540.jpg
     ├── 300Wx300H
     │   └── 289540.jpg
     ├── 30Wx30H
     │   └── 289540.jpg
     ├── 515Wx515H
     │   └── 289540.jpg
     ├── 65Wx65H
     │   └── 289540.jpg
     └── 96Wx96H
         └── 289540.jpg
     ```  
  6. Import productMedia.impex through hAC or Backoffice

# Configuration
## config.py

| Section   | Option   | Example       | Description                              |
|-----------|----------|---------------|------------------------------------------|
|IMAGEMAGICK|path      |/usr/local/bin/|ImageMagick bin directory path            |
|IMAGEMAGICK|thumbnail |^              |^: Cut to fit. Blank: Padded              |
|IMAGEMAGICK|background|white|Background color in padded squire reshape           |
|IMAGEMAGICK|outputdirs|     |Do not modify unless you have different media format|
|IMAGEMAGICK|sizes     |     |Do not modify unless you have different media format|
|HYBRIS     |catalog   |electronicsProductCatalog|Product catalog name            |

## input.csv

```
product_id_1,image_filename_1
product_id_2,image_filename_2
```
