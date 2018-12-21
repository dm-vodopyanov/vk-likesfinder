import vk_requests
import traceback
import argparse
import datetime
import time
import sys

from enum import Enum
from vk_requests.exceptions import VkAPIError


__version__ = '0.0.1'


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('ERROR: %s\n' % message)
        self.print_help()
        sys.exit(-2)


class ItemType(Enum):
    PAGE = 'page'
    PERSON = 'person'
    UNDEFINED = 'undefined'


class LikeChecker:
    def __init__(self):
        self.api = None
        self.html_report = None
        self.like_count = 0
        self.args = self.create_parser().parse_args()
        self.earliest_time = int(time.time()) - int(self.args.interval) * 3600
        self.exit_code = 0

    @staticmethod
    def create_parser():
        parser = DefaultHelpParser(prog='vk_like_checker', description='VK LikeChecker',
                                   formatter_class=argparse.RawTextHelpFormatter, add_help=True)
        parser.add_argument('-ai', '--app_id', required=True, default=None,
                            help='ID of application')
        parser.add_argument('-st', '--service_token', required=True, default=None,
                            help='Service token of application')
        parser.add_argument('-us', '--user', required=True, default=None,
                            help='ID or short name of checked user')
        parser.add_argument('-in', '--interval', required=True, default=None,
                            help='Interval in hours')
        parser.add_argument('-hr', '--html_report', required=False, default=None,
                            help='Path to HTML report, which generates in the folder with script by default')
        parser.add_argument('-v', '--version', action='version', help='Show version and exit', version=__version__)
        return parser

    @staticmethod
    def identify_item_type(item):
        if item.get('name'):
            return ItemType.PAGE
        elif item.get('first_name'):
            return ItemType.PERSON
        return ItemType.UNDEFINED

    @staticmethod
    def _get_string_with_fixed_size(string, length):
        number_of_spaces = 0
        if length > len(string):
            number_of_spaces = length - len(string)
        return string + ' ' * number_of_spaces

    def get_liked_posts(self, source):
        counter = 0
        for item in source['items']:
            try:
                counter += 1
                if ItemType.UNDEFINED == self.identify_item_type(item):
                    continue
                status = 'Check {}/{}'.format(counter, len(source['items']))
                print(self._get_string_with_fixed_size(status, 79), end='\r')
                item_id = None
                header_printed = False
                if ItemType.PAGE == self.identify_item_type(item):
                    item_id = -item['id']
                if ItemType.PERSON == self.identify_item_type(item):
                    item_id = item['id']

                posts_offset = 0
                while True:
                    posts = self.api.wall.get(owner_id=item_id, count=100, offset=posts_offset)

                    if not posts['items']:
                        break

                    is_some_post_older_earliest_time = False

                    for post in posts['items']:
                        if post['date'] >= self.earliest_time:
                            likes_offset = 0
                            while True:
                                likes = self.api.likes.getList(type='post', owner_id=item_id, item_id=post['id'],
                                                               skip_own=0, count=1000, offset=likes_offset)

                                if not likes['items']:
                                    break

                                if self.args.user in likes['items']:
                                    if not header_printed:
                                        header_printed = True
                                        name = ''
                                        if ItemType.PAGE == self.identify_item_type(item):
                                            name = item['name']
                                        if ItemType.PERSON == self.identify_item_type(item):
                                            name = '{} {}'.format(item['first_name'], item['last_name'])
                                        try:
                                            # TODO: fix UnicodeEncodeError error
                                            print(self._get_string_with_fixed_size(name, 79))
                                        except UnicodeEncodeError:
                                            print('ERROR: UnicodeEncodeError: cannot print string')
                                        self.html_report.write('<b>{}</b><br>\n'.format(name).encode('utf-8').decode(
                                            'utf-8', errors='ignore'))

                                    link = 'https://vk.com/wall{owner_id}_{item_id}'.format(
                                        owner_id=item_id,
                                        item_id=post['id'])
                                    print('    {}'.format(link))
                                    self.html_report.write('<div style="text-indent:30px;"><a href="{0}" '
                                                           'target="_blank">{0}</a></div>\n'.format(link))
                                    self.like_count += 1
                                    break

                                likes_offset += 1000
                        else:
                            if not post.get('is_pinned'):
                                is_some_post_older_earliest_time = True
                                break

                    if is_some_post_older_earliest_time:
                        break

                    posts_offset += 100
            except VkAPIError:
                pass
        print()

    def main(self):
        header = 'VK LikeChecker {}'.format(__version__)

        print('=' * 79)
        print(header)
        print('=' * 79)
        print()

        if not self.args.html_report:
            self.args.html_report = 'vk_likes_checker_report_{}_{}.html'.format(self.args.user,
                                                                                str(datetime.datetime.now()).replace(
                                                                                    ' ', '_').replace(
                                                                                    ':', '.').lower())
        self.html_report = open(self.args.html_report, 'w', encoding='utf-8', buffering=1)

        self.html_report.write('<html><head><title>{title} - Report</title></head><body>\n'.format(title=header))
        self.html_report.write('<h2>{title}</h2><b>Report generated:</b> {date}<br><br>\n'.format(
            title=header, date=datetime.datetime.now()))

        try:
            self.api = vk_requests.create_api(app_id=int(self.args.app_id), service_token=self.args.service_token)
            print('Application ID and service token were applied successfully.\n')

            self.args.user = self.api.users.get(user_ids=self.args.user)[0]['id']

            checking_user = '{} {}'.format(self.api.users.get(user_ids=self.args.user)[0]['first_name'],
                                           self.api.users.get(user_ids=self.args.user)[0]['last_name'])
            try:
                # TODO: fix UnicodeEncodeError error
                print('Checking user: {}'.format(checking_user))
            except UnicodeEncodeError:
                print('ERROR: UnicodeEncodeError: cannot print string')
            self.html_report.write('<b>Checking user: <a href="{}" target="_blank">{}</a></b><br>\n'.format(
                'https://vk.com/id{}'.format(self.args.user), checking_user).encode('utf-8').decode(
                'utf-8', errors='ignore'))

            print('Searching interval: {} hour(s) till now'.format(self.args.interval))
            self.html_report.write('<b>Searching interval:</b> {} hour(s) till now<br><br>\n'.format(
                self.args.interval))

            pages = self.api.users.getSubscriptions(user_id=self.args.user, extended=1, count=200)

            print('\nCheck {} public pages...'.format(pages['count']))
            self.html_report.write('<b>Check {} public pages...</b><br><br>\n'.format(pages['count']))
            self.get_liked_posts(pages)

            friends = self.api.friends.get(user_id=self.args.user, fields='first_name,last_name')

            print('\nCheck {} friends...'.format(friends['count']))
            self.html_report.write('<br><br><b>Check {} friends...</b><br><br>\n'.format(friends['count']))
            self.get_liked_posts(friends)

            print('\n{} like(s) were found.'.format(self.like_count))
            self.html_report.write('<br><br><b>{} like(s) were found.</b>\n'.format(self.like_count))

        except KeyboardInterrupt:
            print('ERROR: The program was interrupted by user')
            self.exit_code = -1
        except VkAPIError as ex:
            print('ERROR: VkAPIError: {message}. Error code is {error_code}'.format(message=ex.message,
                                                                                    error_code=ex.code))
            self.exit_code = -2
        except Exception as ex:
            print('ERROR: Something goes wrong: {} '.format(ex))
            print('ERROR: {}'.format(traceback.format_exc()))
            self.exit_code = -2
        finally:
            self.html_report.write('</body></html>\n')
            self.html_report.close()
            return self.exit_code


if __name__ == '__main__':
    sys.exit(LikeChecker().main())
