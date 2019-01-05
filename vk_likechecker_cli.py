import webbrowser
import traceback
import platform
import argparse
import sys
import os

from vk_requests.exceptions import VkAPIError
from vk_requests.exceptions import VkAuthError
from src.vk_likechecker import VkLikeCheckerException
from src.vk_api_wrapper import VkApiWrapperException
from src.html_report import HtmlReportException

from src.getpass_cross_platform import getpass
from src.vk_likechecker import VkLikeChecker
from src.vk_likechecker import MAX_CONSOLE_LINE_LENGTH
from src.vk_likechecker import DEFAULT

__version__ = '1.0.0'


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('ERROR: %s\n' % message)
        self.print_help()
        sys.exit(-2)


class VkLikeCheckerCliException(Exception):
    pass


class LikeCheckerCli:
    def __init__(self):
        self.location = os.path.dirname(os.path.realpath(__file__))

        args = self.create_parser().parse_args()

        self.vk_likechecker = VkLikeChecker()
        self.vk_likechecker.set_authorization_token_file(args.authorization_token_file)
        self.vk_likechecker.set_token(args.token)
        self.vk_likechecker.set_user(args.user)
        self.vk_likechecker.set_interval(args.interval)
        self.vk_likechecker.set_public_pages(args.public_pages)
        self.vk_likechecker.set_groups(args.groups)
        self.vk_likechecker.set_people(args.people)
        self.vk_likechecker.set_earliest_time()
        self.vk_likechecker.set_location(self.location)
        self.vk_likechecker.set_header(__version__)

        self.exit_code = 0

    def create_parser(self):
        current_system = self.get_platform_name()[:3]
        parser = DefaultHelpParser(prog='vk-likechecker-{}-cli-{}'.format(__version__, current_system),
                                   description='VK LikeChecker {}'.format(__version__),
                                   formatter_class=argparse.RawTextHelpFormatter, add_help=True)
        parser.add_argument('-to', '--token', required=False, default=None,
                            help='Your access/service token. It needs for authorization\n'
                                 'to VK. If you need to obtain token or use your\n'
                                 'login/password, don\'t mention this option, the\n'
                                 'application will suggest you how you can authorize to\n'
                                 'VK in user-interactive mode')
        authorization_token_file = os.path.join(self.location, 'authorization_token.txt')
        parser.add_argument('-at', '--authorization_token_file', required=False,
                            default=authorization_token_file,
                            help='Path to text file with your access/service token for\n'
                                 'accessing VK. Follow documentation to see how it\n'
                                 'should be organized. Paste a token to it, and it will\n'
                                 'be automatically used on authorization step. If you\n'
                                 'need to obtain token, you will be moved to\n'
                                 'user-interactive mode. After that\n'
                                 '{}\n'
                                 'will be created automatically, and you won\'t need to\n'
                                 'obtain your token again.'.format(authorization_token_file))
        parser.add_argument('-us', '--user', required=True, default=None,
                            help='Short name or ID of checked user')
        parser.add_argument('-in', '--interval', required=True, default=None,
                            help='Searching interval in hours')
        parser.add_argument('-pp', '--public_pages', required=False, default=DEFAULT,
                            help='A list of public pages, in which likes will be\n'
                                 'searched.\n'
                                 '1. It\'s "all" by default. It means that all\n'
                                 '   user\'s public pages will be scanned.\n'
                                 '2. If you want to add some custom public page, pass\n'
                                 '   "all,some_public_page" (comma is separator),\n'
                                 '   where "some_public_page" is the short name of page\n'
                                 '   (vk.com/some_public_page).\n'
                                 '3. If you want to scan only some specific pages,\n'
                                 '   don\'t add "all", just pass short names of\n'
                                 '   public page: "public_page_1,public_page_2".\n'
                                 '4. If you want to skip some public pages from\n'
                                 '   "all", add "!" symbol (or "\!" on some Linux\n'
                                 '   systems) at the beginning of skipping element,\n'
                                 '   e.g., "!public_page_1,!public_page_2"  or\n'
                                 '   "all,!public_page_1,!public_page_2" - in\n'
                                 '   this case all public pages will be scanned, except\n'
                                 '   two public pages with short names "public_page_1"\n'
                                 '   and "public_page_2".\n'
                                 '5. If you want to completely skip checking of public\n'
                                 '   pages, pass "none".')
        parser.add_argument('-gr', '--groups', required=False, default=DEFAULT,
                            help='A list of groups, in which likes will be searched.\n'
                                 '1. It\'s "all" by default. It means that all\n'
                                 '   user\'s groups will be scanned. NOTE - you can\'t\n'
                                 '   check user\'s groups using service token.\n'
                                 '2. If you want to add some custom group, pass\n'
                                 '   "all,some_group" (comma is separator), where\n'
                                 '   "some_group" is the short name of group\n'
                                 '   (vk.com/some_group).\n'
                                 '3. If you want to scan only some specific groups,\n'
                                 '   don\'t add "all", just pass short names of\n'
                                 '   group: "group_1,group_2".\n'
                                 '4. If you want to skip some groups from "all", add\n'
                                 '   "!" symbol (or "\!" on some Linux systems) at the\n'
                                 '   beginning of skipping element, e.g.,\n'
                                 '   "!group_1,!group_2" or "all,!group_1,!group_2" -\n'
                                 '   in this case all groups will be scanned, except\n'
                                 '   two groups with short names "group_1" and\n'
                                 '   "group_2".\n'
                                 '5. If you want to completely skip checking of groups,\n'
                                 '   pass "none".')
        parser.add_argument('-pe', '--people', required=False, default=DEFAULT,
                            help='A list of people, in which likes will be searched.\n'
                                 '1. It\'s "all" by default. It means that all\n'
                                 '   user\'s friends will be scanned.\n'
                                 '2. If you want to add some custom person, pass\n'
                                 '   "all,some_person" (comma is separator), where\n'
                                 '   "some_person" is the short name of person\'s page\n'
                                 '   (vk.com/some_person). As usual, user IDs are\n'
                                 '   supported.\n'
                                 '3. If you want to scan only some specific people,\n'
                                 '   don\'t add "all", just pass short names/IDs of\n'
                                 '   people: "person_1,person_2".\n'
                                 '4. If you want to skip some people from "all", add\n'
                                 '   "!" symbol (or "\!" on some Linux systems) at the\n'
                                 '   beginning of skipping element, e.g.,\n'
                                 '   "!person_1,!person_2" or\n'
                                 '   "default,!person_1,!person_2" - in this case all\n'
                                 '   friends will be scanned, except two friends with\n'
                                 '   short names "person_1" and "person_2".\n'
                                 '5. If you want to completely skip checking of people,\n'
                                 '   pass "none".')
        parser.add_argument('-hr', '--html_report', required=False, default=None,
                            help='Custom path to HTML report (by default it generates in\n'
                                 'the folder where VK LikeChecker binary/script is\n'
                                 'located)')
        parser.add_argument('-v', '--version', action='version', help='Show VK LikeChecker version and exit',
                            version=__version__)
        return parser

    @staticmethod
    def get_platform_name():
        return platform.system().lower().replace('darwin', 'mac')

    def print_header_cli(self):
        self.vk_likechecker.print('=' * MAX_CONSOLE_LINE_LENGTH)
        self.vk_likechecker.print(self.vk_likechecker.header)
        self.vk_likechecker.print('=' * MAX_CONSOLE_LINE_LENGTH)
        self.vk_likechecker.print()

    def obtain_token(self):
        self.vk_likechecker.print('You are not authorized to access VK.')
        self.vk_likechecker.print()
        self.vk_likechecker.print('You can authorize to VK in the 3 ways:')
        self.vk_likechecker.print('  1. Enter login and password')
        self.vk_likechecker.print('  2. Use browser to generate access token and type it here (PREFERRED)')
        self.vk_likechecker.print('  3. Use browser to create empty VK standalone application, generate service\n'
                                  '     token and type it here (in this case you can\'t access user\'s page if\n'
                                  '     you and user are friends and page is private for non-friends, and you\n'
                                  '     can\'t access user\'s groups if they are visible for you)')
        while True:
            try:
                authorize_method = eval(input('What would you choose? (press number): '))
                if authorize_method not in [1, 2, 3]:
                    raise VkLikeCheckerCliException
                break
            except NameError:
                self.vk_likechecker.print('ERROR: Wrong input - please enter a number. Try again.')
            except VkLikeCheckerCliException:
                self.vk_likechecker.print('ERROR: Wrong number. Try again.')

        if 1 == authorize_method:
            self.vk_likechecker.set_login(str(input('Login: ')))
            self.vk_likechecker.set_password(getpass(prompt='Password: '))
        elif 2 == authorize_method:
            self.vk_likechecker.print('Opening a browser...')
            browser_location = {'default': {'windows': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s',
                                            'linux': '/usr/bin/firefox %s',
                                            'mac': 'open -a /Applications/Safari.app %s'}}

            link = 'https://oauth.vk.com/authorize?client_id={client_id}&redirect_uri=https://vk.com&v=5.92&' \
                   'response_type=token&scope={scope}'.format(client_id=self.vk_likechecker.get_app_id(),
                                                              scope='friends,groups,offline')
            try:
                webbrowser.get(browser_location.get('default').get(self.get_platform_name()))
                webbrowser.open(link)
            except webbrowser.Error:
                self.vk_likechecker.print('ERROR: Failed to open browser.')
                self.vk_likechecker.print('Please open your browser manually and follow this link:')
                self.vk_likechecker.print(link)

            self.vk_likechecker.print('After logging in to VK and granting the access to the VK LikeChecker app, you\n'
                                      'need to copy access_token from address bar and paste it below.')
            self.vk_likechecker.set_token(getpass(prompt='Enter access token here: '))
            self.vk_likechecker.print()
            self.vk_likechecker.print('Access token was written to {}'.format(
                self.vk_likechecker.authorization_token_file))
        elif 3 == authorize_method:
            self.vk_likechecker.print()
            self.vk_likechecker.print('Create an Application on VK (see link below). Type anything to Title section,\n'
                                      'e.g., VK LikeChecker, choose Platform as Standalone Application and press\n'
                                      'Connect Application button. When press Save button. Go to Settings and copy\n'
                                      'service_token and paste it below.')
            self.vk_likechecker.print()
            self.vk_likechecker.print('Link: https://vk.com/editapp?act=create')
            self.vk_likechecker.print()
            self.vk_likechecker.set_token(getpass(prompt='Enter service token here: '))
            self.vk_likechecker.print()
            self.vk_likechecker.print('Service token was written to {}'.format(
                self.vk_likechecker.authorization_token_file))
        else:
            # do nothing
            pass
        self.vk_likechecker.print()

    def main(self):
        try:
            self.print_header_cli()

            self.vk_likechecker.initialize_html_report(stdout_on=True)
            if not self.vk_likechecker.token:
                self.obtain_token()
            self.vk_likechecker.initialize_vk_api(stdout_on=True)
            self.vk_likechecker.show_basic_info(html_report_on=True, stdout_on=True)

            self.vk_likechecker.get_liked_public_pages_posts(html_report_on=True, stdout_on=True)
            self.vk_likechecker.get_liked_groups_posts(html_report_on=True, stdout_on=True)
            self.vk_likechecker.get_liked_people_posts(html_report_on=True, stdout_on=True)

            self.vk_likechecker.show_likes_count(html_report_on=True, stdout_on=True)
        except KeyboardInterrupt:
            self.vk_likechecker.print('ERROR: The program was interrupted by user')
            self.exit_code = -1
        except VkAPIError as ex:
            self.vk_likechecker.print('ERROR: VkAPIError: {message}. Error code is {error_code}'.format(
                message=ex.message, error_code=ex.code))
            self.vk_likechecker.print('ERROR: {}'.format(traceback.format_exc()))
            self.exit_code = -2
        except VkAuthError as ex:
            self.vk_likechecker.print('ERROR: VkAuthError: {message}'.format(message=ex))
            self.exit_code = -2
        except VkApiWrapperException as ex:
            self.vk_likechecker.print('Error: VkApiWrapperException: {message}'.format(message=ex))
            self.exit_code = -2
        except VkLikeCheckerException as ex:
            self.vk_likechecker.print('Error: VkLikeCheckerException: {message}'.format(message=ex))
            self.exit_code = -2
        except VkLikeCheckerCliException as ex:
            self.vk_likechecker.print('Error: VkLikeCheckerCliException: {message}'.format(message=ex))
            self.exit_code = -2
        except HtmlReportException as ex:
            self.vk_likechecker.print('Error: HtmlReportException: {message}'.format(message=ex))
            self.exit_code = -2
        except Exception as ex:
            self.vk_likechecker.print('ERROR: Something goes wrong: {} '.format(ex))
            self.vk_likechecker.print('ERROR: {}'.format(traceback.format_exc()))
            self.exit_code = -2
        finally:
            self.vk_likechecker.html_report.close_file()
            return self.exit_code


if __name__ == '__main__':
    sys.exit(LikeCheckerCli().main())
