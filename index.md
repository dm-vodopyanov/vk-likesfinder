---
title: About
layout: default
---

# Key features
1. Cross-platform, supports Windows, Linux and macOS.
2. Check selected user's likes on his friends, public and group pages
3. Customize the lists of public pages, groups and friends (for more see [Customize the list of public pages, groups and friends](https://dmitryvodop.github.io/vk-likesfinder/documentation#customize-the-list-of-public-pages-groups-and-friends)):
   1. skip some pages,
   2. add pages (public pages or groups), on which selected user doesn't subscribed
   3. add people with whom selected user is not friends
4. Select the searching interval in hours
5. Clear and handy authorization process to VK API: for more see [Authorization methods](https://dmitryvodop.github.io/vk-likesfinder/documentation#authorization-methods)
6. Different report formats: for more see [Reports](https://dmitryvodop.github.io/vk-likesfinder/documentation#reports)

## Getting started
1. Download ```vk-likesfinder_cli_win.exe``` (for Windows) or ```vk-likesfinder_cli_lin``` 
(for Linux) or ```vk-likesfinder_cli_mac``` (for macOS) application.
2. Run the application in command line:  
    ```vk-likesfinder-cli-<PLATFORM> --interval <INTERVAL>```,    
   where  
   ```<PLATFORM>``` is ```win```, ```lin``` or ```mac```,  
   ```<USER>``` is person that should to be checked; supports short name of page (e.g., durov) 
   or user ID (e.g., 1),  
   ```<INTERVAL>``` is searching interval in hours till now, e.g., 10.   
   E.g.: **```vk-likesfinder-cli-win.exe --user durov --interval 10```**  
   See the full list of [Supported command line options](https://dmitryvodop.github.io/vk-likesfinder/documentation#supported-command-line-options) for more.
3. If you did not provide access/service token through ```--token``` option, or did not create 
```authorization_token.txt``` file with the token inside it in the directory with VK LikesFinder
binary/script, you will be redirected to user-interactive mode, where you can authorize to VK
using one of three methods (see [Authorization methods](https://dmitryvodop.github.io/vk-likesfinder/documentation#authorization-methods) for more):
   1. by providing login/password to VK API
   2. by generating access token through your browser
   3. by generating service token for your VK application 
4. Find the vk_likesfinder_report_***.html report in the directory where application was launched.