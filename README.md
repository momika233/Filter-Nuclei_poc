# Filter-Nuclei_poc
https://x.com/momika233

This script is used to process Nuclei POC files, and its main functions include:

1. Traverse all. yaml files in the specified directory
2. Extract partial content of requests: or http: from the file
3. Remove annotation content
4. Calculate the MD5 hash value of the content
5. Deduce based on hash value and copy non duplicate files to the directory of step 1
6. Extract the security level of POC and move non info level POCs to the directory in step 2
7. Analyze the keywords in POC and move the files that meet the criteria to the directory in step 3

## Process flow

### 1. * * Phase 1 * *: File deduplication
-Traverse all YAML files
-Extract key content and calculate MD5
-Save to the directory of step 1 after deduplication

### 2. * * Phase 2 * *: Security Level Screening
-Read files from the directory of step 1
-Extract security level information
-Move non info level POCs to the step2 directory

### 3. * * Phase 3 * *: Keyword Analysis
-Read files from the directory in step 2
-Check HTTP related keywords
-Exclude files containing/readme.txt or/style. css
-Move eligible files to the directory of step 3
