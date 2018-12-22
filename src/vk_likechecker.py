import datetime
import time
import os

from enum import Enum
from vk_requests.exceptions import VkAPIError
from src.vk_api_wrapper import VkApiWrapper
from src.html_report import HtmlReport


class VkLikeCheckerException(Exception):
    pass


class ItemType(Enum):
    PAGE = 'page'
    PERSON = 'person'
    UNDEFINED = 'undefined'


class VkLikeChecker:
    def __init__(self):
        self.header = None
        self.start_time = datetime.datetime.now()
        self.app_id = None
        self.service_token = None
        self.authentication_config = None
        self.user = None
        self.interval = None
        self.vk_api_wrapper = None
        self.earliest_time = None
        self.likes_count = 0
        self.location = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.html_report = HtmlReport()

    def set_app_id(self, app_id):
        self.app_id = app_id

    def set_service_token(self, service_token):
        self.service_token = service_token

    def set_authentication_config(self, authentication_config):
        self.authentication_config = authentication_config

    def set_user(self, user):
        self.user = user

    def set_interval(self, interval):
        self.interval = interval

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_header(self, version):
        self.header = 'VK LikeChecker {}'.format(version)

    def set_earliest_time(self):
        if not self.interval:
            raise VkLikeCheckerException('Searching interval is empty')
        self.earliest_time = int(time.time()) - int(self.interval) * 3600

    def initialize_html_report(self):
        if not self.user:
            raise VkLikeCheckerException('User is not initialized')
        self.html_report.set_path(os.path.join(self.location, 'vk_likechecker_report_{}_{}.html'.format(
            self.user, str(self.start_time).replace(' ', '_').replace(':', '.').lower())))

        self.html_report.initialize_file(self.html_report.path)

        self.html_report.write('<html><head><title>{title} - Report</title></head><body>\n'.format(title=self.header))
        self.html_report.write('<h2>{title}</h2><b>Report generated:</b> {date}<br><br>\n'.format(
            title=self.header, date=self.start_time))

    def initialize_vk_api(self, stdout_on=False):
        if self.app_id and self.service_token:
            # nothing to do, app_id and service_token already initialized
            pass
        elif os.path.exists(self.authentication_config):
            app_id_config = service_token_config = ''
            with open(self.authentication_config, 'r') as authentication_config_file:
                content = authentication_config_file.readlines()
                if len(content) < 2:
                    raise VkLikeCheckerException('Incorrect authentication config. Check documentation for more help')
                else:
                    app_id_config = content[0].replace('\n', '')
                    service_token_config = content[1].replace('\n', '')
            if self.app_id:
                self.service_token = service_token_config
            elif self.service_token:
                self.app_id = app_id_config
            else:
                self.app_id = app_id_config
                self.service_token = service_token_config
        else:
            raise VkLikeCheckerException('Application ID and/or service token are/is empty.')

        self.vk_api_wrapper = VkApiWrapper(self.app_id, self.service_token)
        self.vk_api_wrapper.initialize_vk_api()

        if stdout_on:
            if self.vk_api_wrapper.check_if_vk_api_initialized():
                print('Application ID and service token were applied successfully.')
                print('VK API initialized successfully.\n')
            else:
                print('ERROR: failed to initialize VK API')

        self.vk_api_wrapper.set_user_id(self.user)

    def show_basic_info(self, html_report_on=True, stdout_on=False):
        if not self.vk_api_wrapper:
            raise VkLikeCheckerException('VK API is not initialized')
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')
        # print user first name and last name
        checking_user = '{} {}'.format(self.vk_api_wrapper.get_user_first_name(),
                                       self.vk_api_wrapper.get_user_last_name())
        try:
            # TODO: fix UnicodeEncodeError error
            if stdout_on:
                print('Checking user: {}'.format(checking_user))
        except UnicodeEncodeError:
            if stdout_on:
                print('ERROR: UnicodeEncodeError: cannot print string')

        if html_report_on:
            self.html_report.write('<b>Checking user: <a href="{}" target="_blank">{}</a></b><br>\n'.format(
                'https://vk.com/id{}'.format(self.vk_api_wrapper.user_id), checking_user))

        # print selected searching interval
        if stdout_on:
            print('Searching interval: {} hour(s) till now'.format(self.interval))
        if html_report_on:
            self.html_report.write('<b>Searching interval:</b> {} hour(s) till now<br><br>\n'.format(self.interval))

    def show_likes_count(self, html_report_on=True, stdout_on=False):
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')
        if stdout_on:
            print('\n{} like(s) were found.'.format(self.likes_count))
        if html_report_on:
            self.html_report.write('<br><br><b>{} like(s) were found.</b>\n'.format(self.likes_count))

    def get_liked_user_public_pages_posts(self, html_report_on=True, stdout_on=False):
        if not self.vk_api_wrapper:
            raise VkLikeCheckerException('VK API is not initialized')
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')
        user_public_pages = self.vk_api_wrapper.get_user_public_pages()

        if stdout_on:
            print('\nCheck {} public pages...'.format(user_public_pages['count']))
        if html_report_on:
            self.html_report.write('<b>Check {} public pages...</b><br><br>\n'.format(user_public_pages['count']))

        return self._get_liked_posts(user_public_pages, html_report_on=html_report_on, stdout_on=stdout_on)

    def get_liked_user_friends_posts(self, html_report_on=True, stdout_on=False):
        if not self.vk_api_wrapper:
            raise VkLikeCheckerException('VK API is not initialized')
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')
        user_friends = self.vk_api_wrapper.get_user_friends()

        if stdout_on:
            print('\nCheck {} friends...'.format(user_friends['count']))
        if html_report_on:
            self.html_report.write('<b>Check {} friends...</b><br><br>\n'.format(user_friends['count']))

        return self._get_liked_posts(user_friends, html_report_on=html_report_on, stdout_on=stdout_on)

    def _get_liked_posts(self, source, html_report_on=True, stdout_on=False):
        if not self.vk_api_wrapper:
            raise VkLikeCheckerException('VK API is not initialized')
        if not self.earliest_time:
            raise VkLikeCheckerException('Earliest time is not calculated')
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')
        result = []
        item_counter = 0
        for item in source['items']:
            try:
                item_counter += 1
                if ItemType.UNDEFINED == self._identify_item_type(item):
                    continue
                if stdout_on:
                    status = 'Check {}/{}'.format(item_counter, len(source['items']))
                    print(self._get_string_with_fixed_size(status, 79), end='\r')
                item_id = None
                header_printed = False
                if ItemType.PAGE == self._identify_item_type(item):
                    item_id = -item['id']
                if ItemType.PERSON == self._identify_item_type(item):
                    item_id = item['id']

                name = ''
                if ItemType.PAGE == self._identify_item_type(item):
                    name = item['name']
                if ItemType.PERSON == self._identify_item_type(item):
                    name = '{} {}'.format(item['first_name'], item['last_name'])

                posts_offset = 0
                while True:
                    posts = self.vk_api_wrapper.get_posts_from_wall(item_id, posts_offset)

                    if not posts['items']:
                        break

                    is_some_post_older_earliest_time = False

                    for post in posts['items']:
                        if post['date'] >= self.earliest_time:
                            likes_offset = 0
                            while True:
                                likes = self.vk_api_wrapper.get_likes_from_post(item_id, post['id'], likes_offset)

                                if not likes['items']:
                                    break

                                if self.vk_api_wrapper.get_user_id() in likes['items']:
                                    if not header_printed:
                                        header_printed = True
                                        try:
                                            # TODO: fix UnicodeEncodeError error
                                            if stdout_on:
                                                print(self._get_string_with_fixed_size(name, 79))
                                        except UnicodeEncodeError:
                                            if stdout_on:
                                                print('ERROR: UnicodeEncodeError: cannot print string')
                                        if html_report_on:
                                            self.html_report.write('<b>{}</b><br>\n'.format(name))

                                    link = 'https://vk.com/wall{owner_id}_{item_id}'.format(
                                        owner_id=item_id,
                                        item_id=post['id'])

                                    if stdout_on:
                                        print('    {}'.format(link))
                                    if html_report_on:
                                        self.html_report.write('<div style="text-indent:30px;"><a href="{0}" '
                                                               'target="_blank">{0}</a></div>\n'.format(link))

                                    result.append([name, link])

                                    self.likes_count += 1
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
        if stdout_on:
            print()

        return result

    @staticmethod
    def _identify_item_type(item):
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
