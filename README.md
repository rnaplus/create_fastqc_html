# create_fastqc_html
Automatically create an HTML web site from fastqc output that the user can easily navigate and use to visualize their Illumina sequencing QC results.  
  
## Example usage:  
`./create_fastqc_HTML.py -i fastqc_example/ -c 2 -w 400`  
  
  
## Help message:  
```
Usage: create_fastqc_HTML.py [options]  
  
Options:  
  -h, --help            show this help message and exit  
  -i INPUT_DIR, --input-dir=INPUT_DIR  
                        path to directory containing the unzipped fastqc  
                        output directories. DEFAULT is current working directory  
  -c NCOLS, --cols=NCOLS  
                        # of thumbnail images to display horizontally in each  
                        comparison grid. Must be 1 to 10. DEFAULT is 4  
  -w IMG_WIDTH, --img-width=IMG_WIDTH  
                        width (in pixels) of each thumbnail image. Must be >=  
                        50. DEFAULT is 350 px  
```
