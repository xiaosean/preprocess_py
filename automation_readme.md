readme
===
# use automation_cmd.py
---
    will start date_aggregate.py and marketing_filter_columns.py
# use date_aggregate.py
---
### need
    ---use sql use condition to get the month.
    preprocess_path_file.txt
    dm_subscr_moc_mly_table
    dm_subscr_mtc_mly_table

### output
    dm_subscr_moc_mly_COMPLETED_aggr.csv
    dm_subscr_mtc_mly_COMPLETED_aggr.csv

use marketing_filter_columns.py
---
### need
    preprocess_path_file.txt -> need to revise the month
    dm_subscr_moc_mly_COMPLETED_aggr.csv
    dm_subscr_mtc_mly_COMPLETED_aggr.csv
    MDS_TABLE
    CWC_CATG_CNT_TABLE
    GROUP_ID_FILE -> it will be created by kmean
    
### output
    mrk_picked_with_group_id.csv -> use it to get feature selection

