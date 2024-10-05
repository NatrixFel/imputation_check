# imputation_check
**Compare two tables (pre-imputation and post-imputation) to add IMP flags to SNP with Beagle imputation**

The first script compare tables before and after imputation (it just same tables)

The second script compare tables before imputation and after some filtering steps except imputation (tables with different number of rows)


usage: beagle_check_script_transform.py [-h] file1 file2

positional arguments:
  
  **file1**       Path to the pre-imputation table file
  
  **file2**       Path to the post-imputation table file

options:
  -h, --help  show this help message and exit
