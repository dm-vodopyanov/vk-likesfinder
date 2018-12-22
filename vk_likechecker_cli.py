import traceback
import argparse
import sys
import os

from vk_requests.exceptions import VkAPIError
from src.vk_likechecker import VkLikeCheckerException
from src.vk_api_wrapper import VkApiWrapperException
from src.html_report import HtmlReportException

from src.vk_likechecker import VkLikeChecker

__version__ = '0.0.2'


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('ERROR: %s\n' % message)
        self.print_help()
        sys.exit(-2)


class LikeCheckerCli:
    def __init__(self):
        self.location = os.path.dirname(os.path.realpath(__file__))

        args = self.create_parser().parse_args()

        self.vk_likechecker = VkLikeChecker()
        self.vk_likechecker.set_authentication_config(args.authentication_config)
        self.vk_likechecker.set_app_id(args.app_id)
        self.vk_likechecker.set_service_token(args.service_token)
        self.vk_likechecker.set_user(args.user)
        self.vk_likechecker.set_interval(args.interval)
        self.vk_likechecker.set_earliest_time()
        self.vk_likechecker.set_header(__version__)

        self.exit_code = 0

    def create_parser(self):
        parser = DefaultHelpParser(prog='vk_likechecker', description='VK LikeChecker',
                                   formatter_class=argparse.RawTextHelpFormatter, add_help=True)
        parser.add_argument('-ac', '--authentication_config', required=False,
                            default=os.path.join(self.location, 'authentication_config.txt'),
                            help='Path to authentication config which have Application ID and Service token (register '
                                 'your application to access the tool at https://vk.com/editapp?act=create)')
        parser.add_argument('-ai', '--app_id', required=False, default=None,
                            help='Application ID')
        parser.add_argument('-st', '--service_token', required=False, default=None,
                            help='Service token of application')
        parser.add_argument('-us', '--user', required=True, default=None,
                            help='Short name or ID of checked user')
        parser.add_argument('-in', '--interval', required=True, default=None,
                            help='Searching interval in hours')
        parser.add_argument('-hr', '--html_report', required=False, default=None,
                            help='Path to HTML report (generates in the folder with script by default)')
        parser.add_argument('-v', '--version', action='version', help='Show tool version and exit', version=__version__)
        return parser

    def print_header_cli(self):
        print('=' * 79)
        print(self.vk_likechecker.header)
        print('=' * 79)
        print()

    def main(self):
        try:
            self.print_header_cli()

            self.vk_likechecker.initialize_html_report()
            self.vk_likechecker.initialize_vk_api(stdout_on=True)
            self.vk_likechecker.show_basic_info(html_report_on=True, stdout_on=True)

            self.vk_likechecker.get_liked_user_public_pages_posts(html_report_on=True, stdout_on=True)
            self.vk_likechecker.get_liked_user_friends_posts(html_report_on=True, stdout_on=True)

            self.vk_likechecker.show_likes_count(html_report_on=True, stdout_on=True)
        except KeyboardInterrupt:
            print('ERROR: The program was interrupted by user')
            self.exit_code = -1
        except VkAPIError as ex:
            print('ERROR: VkAPIError: {message}. Error code is {error_code}'.format(message=ex.message,
                                                                                    error_code=ex.code))
            self.exit_code = -2
        except VkApiWrapperException as ex:
            print('Error: VkApiWrapperException: {message}'.format(message=ex))
            self.exit_code = -2
        except VkLikeCheckerException as ex:
            print('Error: VkLikeCheckerException: {message}'.format(message=ex))
            self.exit_code = -2
        except HtmlReportException as ex:
            print('Error: HtmlReportException: {message}'.format(message=ex))
            self.exit_code = -2
        except Exception as ex:
            print('ERROR: Something goes wrong: {} '.format(ex))
            print('ERROR: {}'.format(traceback.format_exc()))
            self.exit_code = -2
        finally:
            self.vk_likechecker.html_report.close_file()
            return self.exit_code


if __name__ == '__main__':
    sys.exit(LikeCheckerCli().main())
