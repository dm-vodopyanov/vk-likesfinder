# VK LikeChecker

VK LikeChecker is a command line tool which provides you to check which posts any VK user liked. It is written on 
Python 3 with using of [vk-requests](https://github.com/prawn-cake/vk-requests) module. 

**Download the latest VK LikeChecker 0.0.2 release [here](https://github.com/dmitryvodop/vk_likechecker/releases).**

## How to use
1. [Create an Application](https://vk.com/editapp?act=create) on VK. It needs for secure connection to VK through VK API. Type anything to Title section, 
e.g., VK LikeChecker, choose Platform as Standalone Application and press Connect Application button. When press Save button
2. Go to Settings. To connect to VK API we will need Application ID and Service token on the Step 4.
3. Download vk_likechecker_win.exe (for Windows) or vk_likechecker_lin (for Linux) application
4. Create ```authentication_config.txt``` file in the same folder with binary on Step 3. It should contain 2 lines: 
Application ID on the first line and Service token on the second, e.g.:   
(data is not real)
```
1234567
a598096bf9674987aa313bbffaa88104bc4875d6506adc07900f76875aaccff86a54aa8
```
5. Run the application in command line:
```
vk_likechecker_win.exe
    --user <user that should be checked; supports 
            short name of page (e.g., durov) or user ID (e.g., 1)> 
    --interval <Searching interval in hours till now, e.g., 10>
```
The full list of options see [here](#supported-command-line-options).
E.g.:
```
vk_likechecker_win.exe --user durov --interval 10
```
6. Find the vk_likechecker_report_***.html report in the directory where application was launched


## Reports
VK LikeChecker supports reports in the following formats: HTML, command line and Python list.

### HTML
The similar report will be generated in the directory where application was launched:  

![Report example](https://raw.githubusercontent.com/dmitryvodop/vk_likechecker/master/images/report_example.png)

### Command line

```
root@ubuntu:~$ vk_likechecker_lin --user *** --interval 100
===============================================================================
VK LikeChecker 0.0.1
===============================================================================

HTML report created: C:\vk_likechecker\vk_likechecker_report_user_2018-12-22_02.55.59.011944.html

Application ID and service token were applied successfully.
VK API initialized successfully.

Checking user: Name Surname
Searching interval: 100 hour(s) till now

Check 43 public pages...
Пикабу
    https://vk.com/wall-31480508_387695
    https://vk.com/wall-31480508_387689
    https://vk.com/wall-31480508_387686
    https://vk.com/wall-31480508_387685
    https://vk.com/wall-31480508_387679
    https://vk.com/wall-31480508_387678
    https://vk.com/wall-31480508_387677
    https://vk.com/wall-31480508_387675
    https://vk.com/wall-31480508_387674
Лепра
    https://vk.com/wall-30022666_298305
    https://vk.com/wall-30022666_298299
    https://vk.com/wall-30022666_298297
9GAG
    https://vk.com/wall-32041317_500984
Check 43/43

Check 125 friends...
Павел Дуров
    https://vk.com/wall1_2442097
Check 125/125

13 like(s) were found.
```

## Python list
If you Python developer, you can call ```get_liked_user_public_pages_posts(...)``` and/or 
```get_liked_user_friends_posts(...)``` from ```VkLikeChecker``` class in src/vk_likechecker.py. 
The following will return:
```
[ ['Пикабу', 'https://vk.com/wall-31480508_387695'],
  ['Пикабу', 'https://vk.com/wall-31480508_387689'],
  ['Пикабу', 'https://vk.com/wall-31480508_387686'],
  ['Пикабу', 'https://vk.com/wall-31480508_387685'],
  ['Пикабу', 'https://vk.com/wall-31480508_387679'],
  ['Пикабу', 'https://vk.com/wall-31480508_387678'],
  ['Пикабу', 'https://vk.com/wall-31480508_387677'],
  ['Пикабу', 'https://vk.com/wall-31480508_387675'],
  ['Пикабу', 'https://vk.com/wall-31480508_387674'],
  ['Лепра', 'https://vk.com/wall-30022666_298305'],
  ['Лепра', 'https://vk.com/wall-30022666_298299'],
  ['Лепра', 'https://vk.com/wall-30022666_298297'],
  ['9GAG', 'https://vk.com/wall-32041317_500984'] ]
  
[ ['Павел Дуров', 'https://vk.com/wall1_2442097'] ]
```

### Supported command line options
```
usage: vk_likechecker [-h] [-ac AUTHENTICATION_CONFIG] [-ai APP_ID]
                      [-st SERVICE_TOKEN] -us USER -in INTERVAL
                      [-hr HTML_REPORT] [-v]

VK LikeChecker

optional arguments:
  -h, --help            show this help message and exit
  -ac AUTHENTICATION_CONFIG, --authentication_config AUTHENTICATION_CONFIG
                        Path to authentication config which have Application ID and Service token (register your application to access the tool at https://vk.com/editapp?act=create)
  -ai APP_ID, --app_id APP_ID
                        Application ID
  -st SERVICE_TOKEN, --service_token SERVICE_TOKEN
                        Service token of application
  -us USER, --user USER
                        Short name or ID of checked user
  -in INTERVAL, --interval INTERVAL
                        Searching interval in hours
  -hr HTML_REPORT, --html_report HTML_REPORT
                        Path to HTML report (generates in the folder with script by default)
  -v, --version         Show tool version and exit
```