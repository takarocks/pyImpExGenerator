# pyImpExGenerator
Python SAP Commerce Cloud ImpEx generator

Set of Python command line programs help generating ImpEx files for SAP Commerce Cloud along with supplemental processes such as image conversion.

# Prerequisite
* ImageMagick
* Python 3.7 or higher

# Version
* 0.2
  * Multiple images per product supported by splitting using pipe |. See productMedias.csv section below.

# How to use
## Product Media ImpEx generation

productMedias.py helps generating ImpEx files and converting source images into various formats. config.py file provides additional configuraion options. Please modify configy.py accordingly to fit your needs.

### Output images

| Format | Thumbnail Option | Image |
|--|--|--|
| Source | N/A | <kbd><img src='_assets/P8150790-original.jpg'/></kbd> |
| Cut | ^ | <kbd><img src='_assets/P8150790-cut.jpg'/></kbd> |
| Padded | (blank) |  <kbd><img src='_assets/P8150790-padded.jpg'/></kbd> |


### Steps

  1. Configure **config.py** and **productMedias.csv**. See following Configuration section for more details.
  2. Locate your source images in your python program execution directory. Do not locate the files in any subdirectory.
  3. Open Terminal or Command Prompt and execute python program as follows

     `python productMedias.py -f productMedias.csv`
  4. Confirm two files produced, **images.zip** and **productMedias.impex**. You can ignore/delete images directories.
  5. Upload and extract **images.zip** onto your Commerce instance under /home/hybris/hybris/temp. Following directories are populated along with converted medias.

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
|IMAGEMAGICK|outputdirs|     |Do not modify this. You need to modify code as well.|
|IMAGEMAGICK|sizes     |     |Do not modify this. You need to modify code as well.|
|HYBRIS     |catalog   |electronicsProductCatalog|Product catalog name            |

## productMedias.csv

```
product_id_1,image_filename_1a.png|image_filename_1b.jpg|image_filename_1c.jpg
product_id_2,image_filename_2a.jpg
```

# History
* 0.1
  * Product medias impex generation including media conversion by ImageMagick
