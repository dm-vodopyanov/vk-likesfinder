import webbrowser
import traceback
import platform
import argparse
import sys
import os

from vk_api.exceptions import VkApiError
from src.vk_likesfinder import VkLikesFinderException
from src.vk_api_wrapper import VkApiWrapperException
from src.html_report import HtmlReportException

from src.getpass_cross_platform import getpass
from src.vk_likesfinder import VkLikesFinder
from src.vk_likesfinder import DEFAULT
from src.cli_report import MAX_CONSOLE_LINE_LENGTH

__version__ = '2.0.0'


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('ERROR: %s\n' % message)
        self.print_help()
        sys.exit(-2)


class VkLikesFinderCliException(Exception):
    pass


class LikesFinderCli:
    def __init__(self):
        self.location = os.path.dirname(os.path.realpath(__file__))
        self.vk_likesfinder = VkLikesFinder()
        self.vk_likesfinder.set_header(__version__)

        self.interactive_mode = True if len(sys.argv) < 2 else False

        if self.interactive_mode:
            self.vk_likesfinder.cli_report.is_initialized = True
            self.print_header_cli()
            self.launch_interactive_mode()
        args = self.create_parser().parse_args()
        self.friends_list = args.friends_list
        self.vk_likesfinder.set_authorization_token_file(args.authorization_token_file)
        self.vk_likesfinder.set_token(args.token)
        self.vk_likesfinder.set_user(args.user)
        self.vk_likesfinder.set_interval(args.interval)
        self.vk_likesfinder.set_public_pages(args.public_pages)
        self.vk_likesfinder.set_groups(args.groups)
        self.vk_likesfinder.set_people(args.people)
        self.vk_likesfinder.set_earliest_time()
        self.vk_likesfinder.set_location(self.location)

        self.exit_code = 0

    def launch_interactive_mode(self):
        self.vk_likesfinder.cli_report.print('Hello! Do you want to find the likes of some VK user? There are two '
                                             'steps:\n')
        user = input('1. Enter short name or ID of the user (e.g., durov or 1): ')
        interval = input('2. Specify searching interval in hours (e.g., 10): ')
        self.vk_likesfinder.cli_report.print('\nNOTE: use command line options to customize the search. E.g., '
                                             'include \nor filter some public pages, groups or people.\n')
        sys.argv = ['', '-us', user, '-in', interval]

    def create_parser(self):
        current_system = self.get_platform_name()[:3]
        parser = DefaultHelpParser(prog='vk-likesfinder-{}-cli-{}'.format(__version__, current_system),
                                   description='VK LikesFinder {}'.format(__version__),
                                   formatter_class=argparse.RawTextHelpFormatter, add_help=True)
        parser.add_argument('-to', '--token', required=False, default=None,
                            help='Your access/service token. It needs for authorization\n'
                                 'to VK. If you need to obtain a token or want to use\n'
                                 'your login/password, don\'t mention this option, the\n'
                                 'application will suggest you how you can authorize to\n'
                                 'VK in user-interactive mode')
        authorization_token_file = os.path.join(self.location, 'authorization_token.txt')
        parser.add_argument('-at', '--authorization-token-file', required=False,
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
                            help='Short name or ID of selected user')
        parser.add_argument('-fl', '--friends-list', required=False, action='store_true',
                            help='Generate friends list of selected user')
        parser.add_argument('-in', '--interval', required=True, default=None,
                            help='Searching interval in hours till now')
        parser.add_argument('-pp', '--public-pages', required=False, default=DEFAULT,
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
        parser.add_argument('-hr', '--html-report', required=False, default=None,
                            help='Custom path to HTML report (by default it generates in\n'
                                 'the folder where VK LikesFinder binary/script is\n'
                                 'located)')
        parser.add_argument('-v', '--version', action='version', help='Show VK LikesFinder version and exit',
                            version=__version__)
        return parser

    @staticmethod
    def get_platform_name():
        return platform.system().lower().replace('darwin', 'mac')

    def print_header_cli(self):
        self.vk_likesfinder.cli_report.print('=' * MAX_CONSOLE_LINE_LENGTH)
        self.vk_likesfinder.cli_report.print(self.vk_likesfinder.header)
        self.vk_likesfinder.cli_report.print('=' * MAX_CONSOLE_LINE_LENGTH)
        self.vk_likesfinder.cli_report.print()

    def obtain_token(self):
        self.vk_likesfinder.cli_report.print('You are not authorized to access VK.')
        self.vk_likesfinder.cli_report.print()
        self.vk_likesfinder.cli_report.print('You can authorize to VK in 3 ways:')
        self.vk_likesfinder.cli_report.print('  1. Enter login and password')
        self.vk_likesfinder.cli_report.print('  2. Use browser to generate access token and type it here (PREFERRED)')
        self.vk_likesfinder.cli_report.print('  3. Use browser to create empty VK standalone application, generate '
                                             'service\n'
                                             '     token and type it here (in this case you can\'t access user\'s page '
                                             'if\n'
                                             '     you and user are friends and page is private for non-friends, and '
                                             'you\n'
                                             '     can\'t access user\'s groups if they are visible for you)')
        while True:
            try:
                authorize_method = eval(input('What do you choose? (press number): '))
                if authorize_method not in [1, 2, 3]:
                    raise VkLikesFinderCliException
                break
            except NameError:
                self.vk_likesfinder.cli_report.print('ERROR: Wrong input - please enter a number. Try again.')
            except VkLikesFinderCliException:
                self.vk_likesfinder.cli_report.print('ERROR: Wrong number. Try again.')

        if 1 == authorize_method:
            self.vk_likesfinder.set_login(str(input('Login: ')))
            self.vk_likesfinder.set_password(getpass(prompt='Password: '))
        elif 2 == authorize_method:
            self.vk_likesfinder.cli_report.print('Opening a browser...')
            browser_location = {'default': {'windows': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s',
                                            'linux': '/usr/bin/firefox %s',
                                            'mac': 'open -a /Applications/Safari.app %s'}}

            link = 'https://oauth.vk.com/authorize?client_id={client_id}&redirect_uri=https://vk.com&v=5.92&' \
                   'response_type=token&scope={scope}'.format(client_id=self.vk_likesfinder.get_app_id(),
                                                              scope='friends,groups,offline')
            try:
                webbrowser.get(browser_location.get('default').get(self.get_platform_name()))
                webbrowser.open(link)
            except webbrowser.Error:
                self.vk_likesfinder.cli_report.print('ERROR: Failed to open browser.')
                self.vk_likesfinder.cli_report.print('Please open your browser manually and follow this link:')
                self.vk_likesfinder.cli_report.print(link)

            self.vk_likesfinder.cli_report.print('After logging in to VK and granting the access to the VK LikesFinder '
                                                 'app, you\n'
                                                 'need to copy access_token from address bar and paste it below.')
            self.vk_likesfinder.set_token(getpass(prompt='Enter access token here: '))
            self.vk_likesfinder.cli_report.print()
            self.vk_likesfinder.cli_report.print('Access token was written to {}'.format(
                self.vk_likesfinder.authorization_token_file))
        elif 3 == authorize_method:
            self.vk_likesfinder.cli_report.print()
            self.vk_likesfinder.cli_report.print('Create an Application on VK (see link below). Type anything to Title '
                                                 'section,\n'
                                                 'e.g., VK LikesFinder, choose Platform as Standalone Application and '
                                                 'press\n'
                                                 'Connect Application button. When press Save button. Go to Settings '
                                                 'and copy\n'
                                                 'service_token and paste it below.')
            self.vk_likesfinder.cli_report.print()
            self.vk_likesfinder.cli_report.print('Link: https://vk.com/editapp?act=create')
            self.vk_likesfinder.cli_report.print()
            self.vk_likesfinder.set_token(getpass(prompt='Enter service token here: '))
            self.vk_likesfinder.cli_report.print()
            self.vk_likesfinder.cli_report.print('Service token was written to {}'.format(
                self.vk_likesfinder.authorization_token_file))
        else:
            # do nothing
            pass
        self.vk_likesfinder.cli_report.print()

    def main(self):
        try:
            self.vk_likesfinder.html_report.is_initialized = True
            self.vk_likesfinder.cli_report.is_initialized = True

            if not self.interactive_mode:
                self.print_header_cli()

            if not self.vk_likesfinder.token:
                self.obtain_token()
            self.vk_likesfinder.initialize_vk_api()

            self.vk_likesfinder.show_basic_info_cli()

            # generate friends list
            if self.friends_list:
                self.vk_likesfinder.generate_friends_list()

            else:
                self.vk_likesfinder.show_extended_info_cli()

                self.vk_likesfinder.initialize_html_report()
                self.vk_likesfinder.show_basic_info_html()
                self.vk_likesfinder.show_extended_info_html()

                self.vk_likesfinder.get_liked_public_pages_posts()
                self.vk_likesfinder.get_liked_groups_posts()
                self.vk_likesfinder.get_liked_people_posts()

                self.vk_likesfinder.show_likes_count()
        except KeyboardInterrupt:
            self.vk_likesfinder.cli_report.print('ERROR: The program was interrupted by user')
            self.vk_likesfinder.html_report.write('<br><b>ERROR: The program was interrupted by user</b><br>\n')
            self.exit_code = -1
        except VkApiError:
            self.vk_likesfinder.cli_report.print('ERROR: VkAPIError')
            self.vk_likesfinder.cli_report.print('ERROR: {}'.format(traceback.format_exc()))
            self.exit_code = -2
        except VkApiWrapperException as ex:
            self.vk_likesfinder.cli_report.print('Error: VkApiWrapperException: {message}'.format(message=ex))
            self.exit_code = -2
        except VkLikesFinderException as ex:
            self.vk_likesfinder.cli_report.print('Error: VkLikesFinderException: {message}'.format(message=ex))
            self.exit_code = -2
        except VkLikesFinderCliException as ex:
            self.vk_likesfinder.cli_report.print('Error: VkLikesFinderCliException: {message}'.format(message=ex))
            self.exit_code = -2
        except HtmlReportException as ex:
            self.vk_likesfinder.cli_report.print('Error: HtmlReportException: {message}'.format(message=ex))
            self.exit_code = -2
        except Exception as ex:
            self.vk_likesfinder.cli_report.print('ERROR: Something goes wrong: {} '.format(ex))
            self.vk_likesfinder.cli_report.print('ERROR: {}'.format(traceback.format_exc()))
            self.exit_code = -2
        finally:
            if self.interactive_mode:
                os.system('pause')
            return self.exit_code


if __name__ == '__main__':
    sys.exit(LikesFinderCli().main())
