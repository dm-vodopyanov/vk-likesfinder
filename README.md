# VK LikeChecker

VK LikeChecker is a command line tool which provides you to check which posts any VK user liked. It is written on 
Python 3 with using of [vk-requests](https://github.com/prawn-cake/vk-requests) module. 

**Download the latest VK LikeChecker release [here](https://github.com/dmitryvodop/vk_likechecker/releases).**

## How to use
1. Create an Application on VK. It needs for secure connection to VK through VK API. Type anything to Title section, 
e.g., VK LikeChecker, choose Platform as Standalone Application and press Connect Application button. When press Save button
2. Go to Settings. To connect to VK API we will need Application ID and Service token on the Step 4.
3. Download vk_likechecker_win.exe (for Windows) or vk_likechecker_lin (for Linux) application
4. Run the application in command line, e.g.,
```
vk_likechecker_win.exe
    --app_id <Application ID from Step 2> 
    --service_token <Service token from Step 2> 
    --user <user that should be checked; supports 
            short name of page (e.g., durov) or user ID (e.g., 1)> 
    --interval <Searching interval in hours till now, e.g., 10>
```
5. The vk_likechecker_report_***_***.html report will be generated in the directory where application was launched

## HTML Report Example
The similar report will be generated:  

![Report example](https://raw.githubusercontent.com/dmitryvodop/vk_likechecker/master/images/report_example.png)