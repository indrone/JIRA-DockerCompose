# Version -
## [0.0.1] - 12.04.2020

### Features

- Basic test case module.
- Docstring and logger added.
- Code issues resolved.
- Test and Demo are in sync.
- Separate yaml file for corpus.

## [0.0.2] - 07.08.2020

### Features

- Restructured codebase into fine grained microservice (infrastructure based load distribution)
- Added event_publish service for live monitoring
- Added health check handler in Main Service
- Added jenkins start file and automatically stop previous container and delete image
- Added https support
- SRC directory contains the main business/domain logic
- Calculated field logic incorporated
- Unmapped Item incorporated
- Mapped incorporated
- Signage incorporated
- Dynamic template feature introduced
- BS classification updated with independent search for classes (no depenency on previous class)
- IS classification updated.
- Multiple format support : Schedule III, T-form (Tally/Others),Other Vertical Format
- Removed obsolete files


## [0.0.3] - 21.09.2020

### Features

- For [T-form (Tally),Other vertical format] logic changed if profit & loss comes under Current Liabilities
- Temporary fix for "TOTAL" keyword extraction
- Short term borrowing has been added in current liability corpus and global variable fix and mapping issue fix
- total_any_level has been modified and added all totals in global variable II
- Issue for Equity residual was resolved
- total_any_level has been modified ,added all totals in global variable, switch ON/OFF for print class and binarization fixed
- Rule 3 will not work in cogs classification in T-form, CF change
- Template fix and binarization fix
- Updated bs/is/cf classification and mapping code inside src
- Code Structure Updated for deployment
- XREV 188, 183, 177, 176, 171 done 

## [0.0.4] - 23.11.2020

### Features

- XREV-369
- XREV-367
- XREV-368
- XREV-363
- XREV-293
- XREV-359
- XREV-360
- XREV-361
- XREV-354
- XREV-330
- XREV-331
- XREV-332
- XREV-333
- XREV-326
- XREV-315
- XREV-316
- XREV-317
- XREV-318
- XREV-319
- XREV-320
- XREV-321
- XREV-322
- XREV-323
- XREV-324
- Extraction is replaced by classification
- Disabled XREV-293, XREV-302
- XREV-297
- XREV-298
- XREV-299
- XREV-300
- XREV-301
- Added classification_queue to mount
- Added spacy 2.3.2
- XREV-294
- XREV-291
- XREV-292
- XREV-293
- Added Docker Image names
- XREV-279
- XREV-281
- XREV-280
- XREV-283
- XREV-282
- XREV-284
- XREV-285
- XREV-287
- XREV-278
- Disabled XREV-272
- XREV-272
- XREV-273
- XREV-274
- XREV-275
- XREV-256
- XREV-254
- XREV-253
- XREV-251
- XREV-252
- XREV-242 and Modified the log in classification
- XREV-236
- filename added in dict_search
- Added PYTHONUNBUFFERED=1
- XREV-225
- Repositioned the try except block for outer calculated field
- Initialized logger at @app.before_first_request
- XREV-235
- XREV-234
- XREV 230
- XREV-233
- XREV-229
- XREV-228, (km_index,finance_cost_index)+1 if lineitem removed
- XREV-221
- XREV-222
- XREV-223

## [0.0.5] - 22.12.2020

### Features

- XREV-388
- XREV-389
- XREV-390
- XREV-393
- XREV-394
- XREV-395
- XREV-397
- XREV-398 
- XREV-404
- XREV-414
- XREV-415
- XREV-416
- XREV-417
- XREV-418	
- XREV-420
- XREV-421
- XREV-422
- XREV-430
- XREV-431
- XREV-432
- XREV-433
- XREV-434
- XREV-436
- XREV-406
- XREV-418
- XREV-438
- XREV-447
- XREV-450
- XREV-457
- XREV-459
- XREV-461
- XREV-462
- XREV-463
- Redeployed XREV-448
- Added nltk downloader all

## [0.0.6] - 12.01.2021

### Features

- XREV-504
- XREV-505
- XREV-506
- XREV-507
- XREV-508
- XREV-532
- XREV-533
- XREV-540
- XREV-541
- XREV-542
- XREV-543
- XREV-544
- XREV-545
- XREV-546
- XREV-552
- XREV-553
- XREV-555
- XREV-552:Removed 'data'
- XREV-568
- XREV-577
- XREV-578
- XREV-579
- XREV-580

## [0.0.7] - 02.02.2021

### Features

- XREV-607
- XREV-608
- XREV-609
- XREV-610
- XREV-611
- XREV-613
- XREV-614
- XREV-620
- XREV-621
- XREV-622
- XREV-626
- XREV-627
- XREV-630
- XREV-631
- XREV-632
- XREV-630: Changed print
- XREV-633
- XREV-635
- XREV-638
- XREV-639
- XREV-642

## [0.0.8] - 11.02.2021

### Features

- XREV-671

## [0.0.9] - 02.03.2021

### Features

- XREV-675
- XREV-676
- XREV-677
- XREV-707
- XREV-709

## [0.1.0] - 07.05.2021

### Features

- XREV-727
- XREV-728
- XREV-729
- XREV-730
- XREV-731
- XREV-733
- XREV-734
- XREV-749
- XREV-750
- XREV-751
- XREV-752
- XREV-757
- XREV-769
- XREV-776
- XREV-799
- XREV-817
- XREV-796:Added output routing key
- XREV-826
- XREV-827
- XREV-849
- XREV-851
- XREV-853
- XREV-818
- XREV-818
- XREV-873
- XREV-886
- XREV-889
- XREV-894
- XREV-898
- XREV-889: Redefined the list index

## [0.1.1] - 07.05.2021

### Features

- XREV-908	
- XREV-909	
- XREV-911	
- XREV-926	
- XREV-927	
- XREV-929
- XREV-930	
- XREV-931	
- XREV-934	
- XREV-939: Revenue corpus added for revenue search	
- XREV-944
- XREV-949	
- XREV-952	
- XREV-955	
- XREV-957	
- XREV-959:token set replaced by sort	
- XREV-964	
- XREV-966:Replaced all True by False if all values are zero	
- XREV-968	
- XREV-970	
- XREV-976	
- XREV-980	
- XREV-983	
- XREV-985	
- XREV-986	
- XREV-987	
- XREV-988

## [0.1.2] - 20.05.2021

### Features

- XREV-997	
- XREV-1005	
- XREV-1032	
- XREV-1032:Indentation added	
- XREV-1032:Type changed	
- XREV-1040	
- XREV-1048	
- XREV-1018	
- XREV-1050	
- XREV-1018:Added list length check	
- XREV-1048:Added Parentheses	
- XREV-1053

## [0.1.3] - 11.06.2021

### Features

- XREV-1076	
- XREV-1077	
- XREV-1081	
- XREV-1084	
- XREV-1087	
- XREV-1090	
- XREV-1097	
- XREV-1110	
- XREV-1113

## [0.1.4] - 25.06.2021

### Features

- XREV-1148	
- XREV-1151	
- XREV-1169	
- XREV-1181	
- XREV-1186	
- XREV-1190

## [0.1.5] - 13.07.2021

### Features

- XREV-1209	
- XREV-1210	
- XREV-1169	
- XREV-1211	
- XREV-1148
- XREV-1221
- XREV-1222
- XREV-1223
- XREV-1242	
- XREV-1249
- XREV-1253
- XREV-1257
- XREV-1263
- XREV-1265

## [0.1.6] - 27.07.2021

### Features

- XREV-1000
- XREV-1277	
- XREV-1286	
- XREV-1293	
- XREV-1301	
- XREV-1302	
- XREV-1303
- XREV-1306
- XREV-1307
- XREV-1313
- XREV-1315
- XREV-1319	
- XREV-1323
- XREV-1339	
- XREV-1349	
- XREV-1350	
- XREV-1354	
- XREV-1385	
- XREV-1387	
- XREV-1391	
- XREV-1392	
- XREV-1400	
- XREV-1411	
- XREV-1431	
- XREV-1434

## [0.1.7] - 10.08.2021

### Features

- XREV-1450	
- XREV-1453	
- XREV-1437	
- XREV-1414
- XREV-1472	
- XREV-1473	

## [0.1.8] - 23.08.2021

### Features

- XREV-1477	
- XREV-1469	
- XREV-1488	
- XREV-1478
- XREV-1484
- XREV-1497
- XREV-1500
- XREV-1377
- XREV-1505
- XREV-1492
- XREV-1510
- XREV-1511
- XREV-1543
- XREV-1544
- XREV-1560
- XREV-1541
- XREV-1563
- XREV-1567
- XREV-1568
- XREV-1572
- XREV-1576
- XREV-1580
- XREV-1582

