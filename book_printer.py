# /usr/bin/env python

import sys
import os

# Extract path to *.ps file
path_to_book = sys.argv[1]
print path_to_book

# Set work directory
os.chdir(os.path.split(path_to_book)[0])

# Create new work directory
dir_name = os.path.splitext(os.path.basename(path_to_book))[0]
work_dir = os.path.join(os.getcwd(), dir_name)
os.mkdir(work_dir)

# Set new work directory
os.chdir(work_dir)

# Get pages in book
pages = int(raw_input("Enter number of pages..."))

# Get pages in byklet
byklet_pages = int(raw_input("Enter byklet pages ..."))

# Add some empty pages
while divmod(pages, 8)[1] != 0:
    pages += 1

print pages

# Get byklets pages
page = 0
byklets = []
while page <= pages:
    page += 1
    from_page = page
    page += byklet_pages - 1
    to_page = page
    byklets.append((from_page, to_page))
print byklets

# Get byklets
all_output_files = []
for i in byklets:
    output_file = os.path.join(work_dir, str(i[0]) + '_' + str(i[1])+ ".ps")
    all_output_files.append(output_file)
    
    os.spawnv(os.P_WAIT, '/usr/bin/psselect',
              ['/usr/bin/psselect',
               '-p',
               str(i[0]) + '-' + str(i[1]),
               path_to_book,
               output_file,])

# Get byklets format
all_byklet_files = []
for in_file in all_output_files:
    f_name = os.path.basename(in_file)
    output_file = os.path.join(
        os.path.split(in_file)[0], 'byklet_' + f_name)
    
    all_byklet_files.append(output_file)
    
    os.spawnv(os.P_WAIT, '/usr/bin/psbook',
              ['/usr/bin/psbook',
               in_file,
               output_file,])

# 1 list formats A4 -> 2 lists format A5
for in_byklet_file in all_byklet_files:
    f_name = os.path.basename(in_byklet_file)
    output_file_rez = os.path.join(
        os.path.split(in_byklet_file)[0], 'rez_' + f_name)
    
    os.spawnv(os.P_WAIT, '/usr/bin/psnup',
              ['/usr/bin/psnup',
               '-l4',
               '-2',
               in_byklet_file,
               output_file_rez,])


# Delay others files
print "Deleyting output files"
for p in all_output_files:
    os.remove(p)
    print ".",
    
print "\nDeleyting byklet files"
for p in all_byklet_files:
    os.remove(p)
    print ".",
