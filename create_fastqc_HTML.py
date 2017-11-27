#!/usr/bin/env python

"""
Created on Tue Sep 01 11:17:48 2015

@author: Robert
"""

import os
from optparse import OptionParser


def createImageGridHTML(write_dir, dirlist, img_filename, html_filename, title, ncols, img_width):
    """Creates an HTML page that displays all specified images in a grid/table
    Input:
    write_dir (str): path to dir where fastqc output dirs are located (also where html pages will be written)
    dirlist (list): list of fastqc dir names
    img_filename (str): name of image file (e.g., 'image.png')
    html_filename (str): name of html file
    title (str): title string that will be placed at the top of the page
	ncols (int): number of images to display in each row of the grid
	img_width (int): number of pixels wide to display the thumbnail image (aspect ratio maintained)
    """
    with open(os.path.join(write_dir, html_filename), 'w') as f_out:
        f_out.write('<html>\n')
        f_out.write('<body>\n')
        f_out.write('\t<h1>{0}</h1>\n'.format(title))
        
        # Begin table
        f_out.write('\t<table>\n')

        count = 1
        for path in dirlist:
            if count % ncols == 1:
                # add a new table row
                f_out.write('\t\t<tr>\n')
            
            # insert thumbnail image
            img_filepath = os.path.join(path, 'Images', img_filename)
            f_out.write('\t\t\t<td><a href="{0}">{1}<img width={2} src="{3}" title="{4}"></a></td>\n'.format(
                img_filepath, count, img_width, img_filepath, path))

            if count % ncols == 0:
                # close the table row
                f_out.write('\t\t</tr>\n')
            
            count += 1
        
        # End table
        f_out.write('\t</table>\n')

        # End page
        f_out.write('</body>\n')
        f_out.write('</html>\n')


def main():
 
    # parse the command line arguments
    usage = 'usage: %prog [options]'
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--input-dir", dest="input_dir",
                      help='path to directory containing the unzipped fastqc output directories.\
                      DEFAULT is current working directory', default=os.path.abspath(os.getcwd()))
    parser.add_option("-c", "--cols", dest="ncols",
                      help='# of thumbnail images to display horizontally in each comparison grid. \
                      Must be 1 to 10. DEFAULT is 4', default=4)
    parser.add_option("-w", "--img-width", dest="img_width",
                      help='width (in pixels) of each thumbnail image. Must be >= 50. DEFAULT is 350 px', default=350)
    (options, args) = parser.parse_args()

    # Get absolute path of input directory
    input_dir = os.path.abspath(options.input_dir)
    if not os.path.exists(input_dir):
        print 'input dir does not exist'
        return

    # List subdirectories (only) within input dir
    tmpdirlist = sorted(next(os.walk(input_dir))[1])  # get all directories (sorted)
    
    # only keep directories that have an "Images" subfolder and a "fastqc_data.txt" file
    dirlist = []
    for path in tmpdirlist:
        testpath = os.path.join(input_dir, path, 'Images')
        testfile = os.path.join(input_dir, path, 'fastqc_data.txt')

        if os.path.exists(testpath) and os.path.isfile(testfile):
            dirlist.append(path)
    
    if not dirlist:
        print 'No fastqc directories found'
        return

    # Check ncols option
    options.ncols = int(options.ncols)
    assert 1 <= options.ncols <= 10

    # Check image width
    options.img_width = int(options.img_width)
    assert options.img_width >= 50  # arbitrary cutoff
    
    ########################################################################
    # Create the home page
    ########################################################################
    fname = os.path.join(input_dir, 'index.html')
    with open(fname, 'w') as f:
        f.write('<html>\n')
        f.write('<body>\n')
        f.write('\t<h1>Fastqc summary report</h1>\n')
    
        # Links to comparison webpages
        f.write('\t<h2>Comparison tables:</h2>')
        f.write('\t<a href="compare_basic_stats.html">Basic statistics</a><br>\n')
        f.write('\t<a href="compare_per_base_sequence_quality.html">Per base sequence quality</a><br>\n')
        f.write('\t<a href="compare_per_sequence_quality.html">Per sequence quality</a><br>\n')
        f.write('\t<a href="compare_sequence_content.html">Per base sequence content</a><br>\n')
        f.write('\t<a href="compare_per_base_gc_content.html">Per base GC content</a><br>\n')
        f.write('\t<a href="compare_per_sequence_gc_content.html">Per sequence GC content</a><br>\n')
        f.write('\t<a href="compare_per_base_n_content.html">Per base N content</a><br>\n')
        f.write('\t<a href="compare_sequence_length_distribution.html">Sequence length distribution</a><br>\n')
        f.write('\t<a href="compare_sequence_duplication_levels.html">Sequence duplication levels</a><br>\n')
        f.write('\t<a href="compare_overrepresented_seqs.html">Overrepresented sequences</a><br>\n')
        f.write('\t<a href="compare_kmer_content.html">Kmer content</a><br>\n')
    
        # Create a hyperlink to each fastqc report
        f.write('\t<h2>Individual fastqc reports:</h2>\n')
        
        count = 1
        for path in dirlist:
            fastqc_report_path = os.path.join(path, 'fastqc_report.html')
            f.write('\t{0}.&nbsp&nbsp&nbsp&nbsp<a href="{1}">{2}</a><br>\n'.format(count,
                                                                                   fastqc_report_path,
                                                                                   fastqc_report_path))
            count += 1
            
        # End html page
        f.write('</body>\n')
        f.write('</html>\n')

    ########################################################################
    # Build html page to compare "basic statistics"
    ########################################################################
    fname = os.path.join(input_dir, 'compare_basic_stats.html')
    with open(fname, 'w') as f:
        f.write('<html>\n')
        f.write('<body>\n')
        f.write('\t<h1>Basic statistics</h1>\n')
        
        # Create table
        f.write('\t<table border="1" cellpadding="5">\n')
    
        # Table headers
        f.write('\t\t<tr>\n')
        f.write('\t\t\t<td><b>Filename</b></td>\n')
        f.write('\t\t\t<td><b>Total Sequences</b></td>\n')
        f.write('\t\t\t<td><b>Sequence Length</b></td>\n')
        f.write('\t\t\t<td><b>%GC</b></td>\n')
        f.write('\t\t</tr>\n')
        
        # Table data
        sum_total_reads = 0

        for path in dirlist:
            txt_file_path = os.path.join(input_dir, path, 'fastqc_data.txt')
            with open(txt_file_path, 'r') as f_in:
                allLines = f_in.readlines()
                
                tmp = [s for s in allLines if 'Filename' in s]
                filename = tmp[0].strip().split()[1]
                
                tmp = [s for s in allLines if 'Total Sequences' in s]
                totalSeqs = int(tmp[0].strip().split()[2])
                sum_total_reads += totalSeqs
    
                tmp = [s for s in allLines if 'Sequence length' in s]
                seqLength = tmp[0].strip().split()[2]
    
                tmp = [s for s in allLines if '%GC' in s]
                pctGC = int(tmp[0].strip().split()[1])
                
                f.write('\t\t<tr>\n')
                f.write('\t\t\t<td>{0}</td>\n'.format(filename))
                f.write('\t\t\t<td align="right">{0:,}</td>\n'.format(totalSeqs))
                f.write('\t\t\t<td align="right">{0}</td>\n'.format(seqLength))
                f.write('\t\t\t<td align="right">{0}</td>\n'.format(pctGC))
                f.write('\t\t</tr>\n')
                
        # Output the sum of all reads analyzed
        f.write('\t\t<tr>\n')
        f.write('\t\t\t<td><b>Total reads processed</b></td>\n')
        f.write('\t\t\t<td align="right"><b>{0:,}</b></td>\n'.format(sum_total_reads))
        f.write('\t\t\t<td align="right"></td>\n')
        f.write('\t\t\t<td align="right"></td>\n')
        f.write('\t\t</tr>\n')
        
        # End table
        f.write('\t</table>\n')
    
        # End html page
        f.write('</body>\n')
        f.write('</html>\n')
    
    ########################################################################
    # Build html page to compare "overrepresented sequences"
    ########################################################################
    fname = os.path.join(input_dir, 'compare_overrepresented_seqs.html')
    with open(fname, 'w') as f:
        f.write('<html>\n')
        f.write('<body>\n')
        f.write('\t<h1>Overrepresented sequences</h1>\n')
        
        # Create local (same page) hyperlinks to table entries
        for path in dirlist:
            f.write('\t<a href="#{0}">{1}</a><br>\n'.format(path, path))
        f.write('\t<br>\n')
        
        # Create table
        f.write('\t<table border="1" cellpadding="5">\n')
    
        # Table headers
        f.write('\t\t<tr>\n')
        f.write('\t\t\t<td><b>Filename</b></td>\n')
        f.write('\t\t\t<td><b>Sequence</b></td>\n')
        f.write('\t\t\t<td><b>Count</b></td>\n')
        f.write('\t\t\t<td><b>Percentage</b></td>\n')
        f.write('\t\t\t<td><b>Possible Source</b></td>\n')
        f.write('\t\t</tr>\n')
        
        # Find the overrepresented sequences
        for path in dirlist:
            txt_file_path = os.path.join(input_dir, path, 'fastqc_data.txt')
            with open(txt_file_path, 'r') as f_in:
                seqs = []
                counts = []
                pcts = []
                sources = []
                while True:
                    tmpLine = f_in.readline()
                    if not tmpLine: 
                        break
                    if tmpLine.startswith('>>Overrepresented sequences'):
                        f_in.readline()  # header line
                        
                        while True:
                            tmpLine = f_in.readline()
                            if not tmpLine or tmpLine.startswith('>>'):
                                break
                            tmp = tmpLine.strip().split('\t')

                            seqs.append(tmp[0])
                            counts.append(tmp[1])
                            pcts.append(tmp[2])
                            sources.append(tmp[3])
                        break
                
                if not seqs:
                    seqs = ['']
                    counts = ['']
                    pcts = ['']
                    sources = ['']
                
                # Print table rows
                for i in range(len(seqs)):
                    f.write('\t\t<tr>\n')
                    if i == 0:
                        f.write('\t\t\t<td><a id="{0}">{1}</a></td>\n'.format(path, path))
                    else:
                        f.write('\t\t\t<td></td>\n')
                    f.write('\t\t\t<td>{0}</td>\n'.format(seqs[i]))
                    f.write('\t\t\t<td align="right">{0}</td>\n'.format(counts[i]))
                    f.write('\t\t\t<td align="right">{0}</td>\n'.format(pcts[i]))
                    f.write('\t\t\t<td>{0}</td>\n'.format(sources[i]))
                    f.write('\t\t</tr>\n')
                
        # End table
        f.write('\t</table>\n')
    
        # End html page
        f.write('</body>\n')
        f.write('</html>\n')
    
    ########################################################################
    # Create web pages containing a grid of thumbnail images
    ########################################################################
    
    # Per base sequence quality
    img_file = 'per_base_quality.png'
    html_file = 'compare_per_base_sequence_quality.html'
    mytitle = 'Per base sequence quality'
    createImageGridHTML(input_dir, dirlist, img_file, html_file, mytitle, options.ncols, options.img_width)
    
    # Per sequence quality
    img_file = 'per_sequence_quality.png'
    html_file = 'compare_per_sequence_quality.html'
    mytitle = 'Per sequence quality'
    createImageGridHTML(input_dir, dirlist, img_file, html_file, mytitle, options.ncols, options.img_width)
    
    # Per sequence content
    img_file = 'per_base_sequence_content.png'
    html_file = 'compare_sequence_content.html'
    mytitle = 'Per base sequence content'
    createImageGridHTML(input_dir, dirlist, img_file, html_file, mytitle, options.ncols, options.img_width)
    
    # Per sequence GC content
    img_file = 'per_sequence_gc_content.png'
    html_file = 'compare_per_sequence_gc_content.html'
    mytitle = 'Per sequence GC content'
    createImageGridHTML(input_dir, dirlist, img_file, html_file, mytitle, options.ncols, options.img_width)
    
    # Per base N content
    img_file = 'per_base_n_content.png'
    html_file = 'compare_per_base_n_content.html'
    mytitle = 'Per base N content'
    createImageGridHTML(input_dir, dirlist, img_file, html_file, mytitle, options.ncols, options.img_width)
    
    # Sequence length distribution
    img_file = 'sequence_length_distribution.png'
    html_file = 'compare_sequence_length_distribution.html'
    mytitle = 'Sequence length distribution'
    createImageGridHTML(input_dir, dirlist, img_file, html_file, mytitle, options.ncols, options.img_width)
    
    # Sequence duplication levels
    img_file = 'duplication_levels.png'
    html_file = 'compare_sequence_duplication_levels.html'
    mytitle = 'Sequence duplication levels'
    createImageGridHTML(input_dir, dirlist, img_file, html_file, mytitle, options.ncols, options.img_width)
    
    # Kmer content
    img_file = 'kmer_profiles.png'
    html_file = 'compare_kmer_content.html'
    mytitle = 'Kmer content'
    createImageGridHTML(input_dir, dirlist, img_file, html_file, mytitle, options.ncols, options.img_width)


if __name__ == '__main__':
    main()
