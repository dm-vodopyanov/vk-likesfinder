# VK LikeChecker

VK LikeChecker is a command line tool which provides you to check which posts any VK user liked. It is written on 
Python 3 with using of [vk-requests](https://github.com/prawn-cake/vk-requests) module. 

**Download the latest VK LikeChecker release [here](https://github.com/dmitryvodop/vk_likechecker/releases).**

| Release  | Windows                          | Linux                        | macOS | Documentation |
| -------- | -------------------------------- | ---------------------------- | ------------- | --- |
| 1.0.0    | [vk_likechecker_cli_win.exe]()   | [vk_likechecker_cli_lin]()   | [vk_likechecker_cli_mac]() | [README.pdf]() |


## Getting started
1. Download ```vk_likechecker_cli_win.exe``` (for Windows) or ```vk_likechecker_cli_lin``` 
(for Linux) or ```vk_likechecker_cli_mac``` (for macOS) application.
2. Run the application in command line:
```
vk_likechecker_<PLATFORM>
    --user <user that should be checked; supports 
            short name of page (e.g., durov) or user ID (e.g., 1)> 
    --interval <searching interval in hours till now, e.g., 10>
```
where ```<PLATFORM>``` is ```win```, ```lin``` or ```mac```.   
E.g.:
```
vk_likechecker_cli_win.exe --user durov --interval 10
```
See the full list of [Supported command line options](#supported-command-line-options) for more. 
3. If you did not provide access/service token through ```--token``` option, or did not create 
```authorization_token.txt``` file with the token inside it in the directory with VK LikeChecker
binary/script, you will be redirected to user-interactive mode, where you can authorize to VK
using one of three methods (see [Authorization methods](#authorization-methods) for more):
   1. by providing login/password to VK API
   2. by generating access token through your browser
   3. by generating service token for your VK application 
3. Find the vk_likechecker_report_***.html report in the directory where application was launched.


## Key features
1. Cross-platform, supports Windows, Linux and macOS.
2. Check selected user's likes on his friends, public and group pages
3. Customize the list of public pages, groups and friends:
   1. skip some pages,
   2. add pages, selected user doesn't subscribed or people he is not friends with
4. Select the searching interval in hours
5. Clear and useful authorization process to VK API: for more see [Authorization methods](#authorization-methods)
6. Different report formats: for more see [Reports](#reports)


## Authorization methods
If you did not provide access/service token through ```--token``` option, or did not create 
```authorization_token.txt``` file with the token inside it in the directory with VK LikeChecker
binary/script, you will be redirected to the following user-interactive mode:
```
You are not authorized to access VK.

You can authorize to VK in the 3 ways:
  1. Enter login and password
  2. Use browser to generate access token and type it here (PREFERRED)
  3. Use browser to create empty VK standalone application, generate service token
     and type it here (in this case you can't access user's page if you and user
     are friends and page is private for non-friends, and you can't access
     user's groups if they are visible for you)
What would you choose? (press number): _
```
Let's look at the each of methods more deeply.  

### (1) Login/password
```
What would you choose? (press number): 1
Login: example@example.com
Password: ********************
```
You need to provide your VK login and password to VK API. Login and password is not stored anywhere - 
you need to provide them each time you run VK LikeChecker.

### (2) Access token
```
What would you choose? (press number): 2
Opening a browser...
After logging in to VK and granting the access to the VK LikeChecker app, you
need to copy access_token from address bar and paste it below.
Enter access token here: _
```
This method provides you to create your own access token - the unique character set. You will be 
re-directed to oauth.vk.com, where you need to log in and grant the access to VK LikeChecker app. 
After that you will be re-directed to the blank page. It will have the following address in 
address bar:
```
https://api.vk.com/blank.html#access_token=<ACCESS_TOKEN>&expires_in=0&user_id=<YOUR_USER_ID>
```
You need to copy ```<ACCESS_TOKEN>``` and paste it to the app:
```
Enter access token here: _
```
After that ```authorization_token.txt``` file with the token inside it in the directory with 
VK LikeChecker binary/script will be created and you don't need to generate your access token 
again. If you need to create another token, remove ```authorization_token.txt``` file.  

**Note:** the following browsers are supported only (each should be installed to default 
directory): Chrome on Windows, Firefox on Linux and Safari on macOS.  
If the browser failed to open automatically, open it manually and go to this link:  
```
https://oauth.vk.com/authorize?client_id=6456882&redirect_uri=https://vk.com&v=5.92&response_type=token&scope=friends,groups,offline
```

### (3) Service token
```
Create an Application on VK (see link below). Type anything to Title section,
e.g., VK LikeChecker, choose Platform as Standalone Application and press
Connect Application button. When press Save button. Go to Settings and copy
service_token and paste it below.

Link: https://vk.com/editapp?act=create

Enter service token here: _
```
*(experimental, not for production use)*

## Reports
VK LikeChecker supports reports in the following formats: HTML, command line and Python list.

### HTML
The similar report will be generated in the directory where application was launched:  

![Report example](https://raw.githubusercontent.com/dmitryvodop/vk_likechecker/master/images/report_example.png)

### Command line

```
root@ubuntu:~$ vk_likechecker_lin --user *** --interval 100
===============================================================================
VK LikeChecker 1.0.0
===============================================================================

HTML report created: 
    C:\vk_likechecker\vk_likechecker_report_user_2018-12-22_02.55.59.011944.html

Authorized to VK successfully.
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

Check 14 groups...
The Elder Scrolls
    https://vk.com/wall-22192347_631644
Check 14/14

Check 125 friends...
Павел Дуров
    https://vk.com/wall1_2442097
Check 125/125

14 like(s) were found.
```

### Python list
If you Python developer, you can call ```get_liked_public_pages_posts(...)``` and/or 
```get_liked_groups_posts(...)``` and/or ```get_liked_people_posts(...)``` from 
```VkLikeChecker``` class in src/vk_likechecker.py. 
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
  
[ ['The Elder Scrolls', 'https://vk.com/wall-22192347_631644'] ]
  
[ ['Павел Дуров', 'https://vk.com/wall1_2442097'] ]
```

## Supported command line options
```
usage: vk_likechecker_cli_*** [-h] [-to TOKEN] [-at AUTHORIZATION_TOKEN] -us
                              USER -in INTERVAL [-pp PUBLIC_PAGES]
                              [-gr GROUPS] [-pe PEOPLE] [-hr HTML_REPORT] [-v]

VK LikeChecker

optional arguments:
  -h, --help            show this help message and exit
  -to TOKEN, --token TOKEN
                        Your access/service token. It needs for authorization
                        to VK. If you need to obtain token or use your
                        login/password, don't mention this option, the
                        application will suggest you how you can authorize to
                        VK in user-interactive mode
  -at AUTHORIZATION_TOKEN_FILE, --authorization_token_file AUTHORIZATION_TOKEN_FILE
                        Path to text file with your access/service token for
                        accessing VK. Follow documentation to see how it
                        should be organized. Paste a token to it, and it will
                        be automatically used on authorization step. If you
                        need to obtain token, you will be moved to
                        user-interactive mode. After that
                        C:\vk_likechecker\authorization_token.txt
                        will be created automatically, and you won't need to
                        obtain your token again.
  -us USER, --user USER
                        Short name or ID of checked user
  -in INTERVAL, --interval INTERVAL
                        Searching interval in hours
  -pp PUBLIC_PAGES, --public_pages PUBLIC_PAGES
                        A list of public pages, in which likes will be
                        searched.
                        1. It's "default" by default. It means that all
                           user's public pages will be scanned.
                        2. If you want to add some custom public page, pass
                           "default,some_public_page" (comma is separator),
                           where "some_public_page" is the short name of page
                           (vk.com/some_public_page).
                        3. If you want to scan only some specific pages,
                           don't add "default", just pass short names of
                           public page: "public_page_1,public_page_2".
                        4. If you want to skip some public pages from
                           "default", add "!" symbol (or "\!" on some Linux
                           systems) at the beginning of skipping element,
                           e.g., "default,!public_page_1,!public_page_2" - in
                           this case all public pages will be scanned, except
                           two public pages with short names "public_page_1"
                           and "public_page_2".
  -gr GROUPS, --groups GROUPS
                        A list of groups, in which likes will be searched.
                        1. It's "default" by default. It means that all
                           user's groups will be scanned. NOTE - you can't
                           check user's groups using service token.
                        2. If you want to add some custom group, pass
                           "default,some_group" (comma is separator), where
                           "some_group" is the short name of group
                           (vk.com/some_group).
                        3. If you want to scan only some specific groups,
                           don't add "default", just pass short names of
                           group: "group_1,group_2".
                        4. If you want to skip some groups from "default", add
                           "!" symbol (or "\!" on some Linux systems) at the
                           beginning of skipping element, e.g.,
                           "default,!group_1,!group_2" - in this case all
                           groups will be scanned, except two groups with
                           short names "group_1" and "group_2".
  -pe PEOPLE, --people PEOPLE
                        A list of people, in which likes will be searched.
                        1. It's "default" by default. It means that all
                           user's friends will be scanned.
                        2. If you want to add some custom person, pass
                           "default,some_person" (comma is separator), where
                           "some_person" is the short name of person's page
                           (vk.com/some_person). As usual, user IDs are
                           supported.
                        3. If you want to scan only some specific people,
                           don't add "default", just pass short names/IDs of
                           people: "person_1,person_2".
                        4. If you want to skip some people from "default", add
                           "!" symbol (or "\!" on some Linux systems) at the
                           beginning of skipping element, e.g.,
                           "default,!person_1,!person_2" - in this case all
                           friends will be scanned, except two friends with
                           short names "person_1" and "person_2".
  -hr HTML_REPORT, --html_report HTML_REPORT
                        Custom path to HTML report (by default it generates in
                        the folder where VK LikeChecker binary/script is
                        located)
  -v, --version         Show VK LikeChecker version and exit
```