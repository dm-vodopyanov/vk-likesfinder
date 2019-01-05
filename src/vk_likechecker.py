import datetime
import requests
import time
import os

from vk_requests.exceptions import VkAPIError
from src.vk_api_wrapper import VkApiWrapper
from src.html_report import HtmlReport


MAX_CONSOLE_LINE_LENGTH = 79

DEFAULT = 'all'  # it can't be vk.com/all as all is too short
NONE = 'none'  # it can't be vk.com/none as none is too short

PUBLIC_PAGES = 'public pages'
GROUPS = 'groups'
PEOPLE = 'people'

PROFILE = 'profile'
PERSON = 'person'
GROUP = 'group'
PAGE = 'page'


class VkLikeCheckerException(Exception):
    pass


class VkLikeChecker:
    def __init__(self):
        self.header = None
        self.start_time = datetime.datetime.now()
        self.login = None
        self.password = None
        self.token = None
        self.app_id = '6456882'
        self.authorization_token_file = None
        self.user = None
        self.interval = None
        self.public_pages = [DEFAULT]  # check all user's public pages by default
        self.groups = [DEFAULT]  # check all user's public pages by default
        self.people = [DEFAULT]  # check all user's friends by default
        self.vk_api_wrapper = None
        self.earliest_time = None
        self.likes_count = 0
        self.location = None
        self.html_report = HtmlReport()

    def set_login(self, login):
        self.login = login

    def set_password(self, password):
        self.password = password

    def set_app_id(self, app_id):
        self.app_id = app_id

    def set_token(self, token):
        if token:
            self.token = token
            if not os.path.exists(self.authorization_token_file):
                with open(self.authorization_token_file, 'w') as authorization_token_file:
                    authorization_token_file.write(self.token)

        elif os.path.exists(self.authorization_token_file):
            token_config = ''
            with open(self.authorization_token_file, 'r') as authorization_token_file:
                content = authorization_token_file.readlines()
                if len(content) < 1:
                    raise VkLikeCheckerException('Incorrect authorization token file. Check documentation '
                                                 'for more help.')
                else:
                    token_config = content[0].replace('\n', '')
            self.token = token_config
        else:
            pass

    def set_authorization_token_file(self, authorization_token_file):
        self.authorization_token_file = authorization_token_file

    def set_user(self, user):
        self.user = user

    def set_interval(self, interval):
        self.interval = interval

    def set_public_pages(self, public_pages):
        self.public_pages = public_pages.replace('\!', '!').split(',')

    def set_groups(self, groups):
        self.groups = groups.replace('\!', '!').split(',')

    def set_people(self, people):
        self.people = people.replace('\!', '!').split(',')

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_location(self, location):
        self.location = location

    def set_header(self, version):
        self.header = 'VK LikeChecker {}'.format(version)

    def set_earliest_time(self):
        if not self.interval:
            raise VkLikeCheckerException('Searching interval is empty')
        self.earliest_time = int(time.time()) - int(self.interval) * 3600

    @staticmethod
    def print(string='', length=MAX_CONSOLE_LINE_LENGTH, end='\n'):
        number_of_spaces = 0
        if length > len(string):
            number_of_spaces = length - len(string)
        print((string + ' ' * number_of_spaces).encode('cp866', errors='ignore').decode('cp866').encode(
            'cp1251', errors='ignore').decode('cp1251'), end=end)

    def initialize_html_report(self, stdout_on=False):
        if not self.user:
            raise VkLikeCheckerException('User is not initialized')
        if not self.location:
            raise VkLikeCheckerException('Cannot identify tool location')
        self.html_report.set_path(os.path.join(self.location, 'vk-likechecker-report-{}_{}.html'.format(
            self.user, str(self.start_time).replace(' ', '_').replace(':', '.').lower())))

        self.html_report.initialize_file(self.html_report.path)

        if stdout_on:
            self.print('HTML report created:\n    {}'.format(self.html_report.path))
            self.print()

        self.html_report.write('<html><head><meta charset="utf-8"/>'
                               '<title>{title} - Report</title></head><body>\n'.format(title=self.header))
        self.html_report.write('<h2>{title}</h2><b>Report generated:</b> {date}<br><br>\n'.format(
            title=self.header, date=self.start_time))

    def initialize_vk_api(self, stdout_on=False):
        self.vk_api_wrapper = VkApiWrapper(app_id=self.app_id, login=self.login, password=self.password,
                                           token=self.token)
        self.vk_api_wrapper.initialize_vk_api()

        if stdout_on:
            if self.vk_api_wrapper.check_if_vk_api_initialized():
                self.print('Authorized to VK successfully.')
                self.print('VK API initialized successfully.\n')
            else:
                self.print('ERROR: failed to initialize VK API')

        self.vk_api_wrapper.set_user_id(self.user)

    def show_basic_info(self, html_report_on=True, stdout_on=False):
        if not self.vk_api_wrapper:
            raise VkLikeCheckerException('VK API is not initialized')
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')
        # print user first name and last name
        checking_user = '{} {}'.format(self.vk_api_wrapper.get_user_first_name(),
                                       self.vk_api_wrapper.get_user_last_name())
        if stdout_on:
            self.print('Checking user: {}'.format(checking_user))

        if html_report_on:
            self.html_report.write('<b>Checking user: <a href="{}" target="_blank">{}</a></b><br>\n'.format(
                'https://vk.com/id{}'.format(self.vk_api_wrapper.user_id), checking_user))

        # print selected searching interval
        if stdout_on:
            self.print('Searching interval: {} hour(s) till now'.format(self.interval))
            self.print()
        if html_report_on:
            self.html_report.write('<b>Searching interval:</b> {} hour(s) till now<br><br>\n'.format(self.interval))

    def show_likes_count(self, html_report_on=True, stdout_on=False):
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')
        if stdout_on:
            self.print('\n{} like(s) were found.'.format(self.likes_count))
        if html_report_on:
            self.html_report.write('<br><br><b>{} like(s) were found.</b>\n'.format(self.likes_count))

    def get_app_id(self):
        return self.app_id

    def get_liked_public_pages_posts(self, html_report_on=True, stdout_on=False):
        if not self.vk_api_wrapper:
            raise VkLikeCheckerException('VK API is not initialized')
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')

        public_pages = self._parse_selected_pages(self.public_pages, PUBLIC_PAGES, stdout_on=stdout_on)

        if not public_pages:
            return []

        return self._get_liked_posts(public_pages, PUBLIC_PAGES, html_report_on=html_report_on,
                                     stdout_on=stdout_on)

    def get_liked_groups_posts(self, html_report_on=True, stdout_on=False):
        if not self.vk_api_wrapper:
            raise VkLikeCheckerException('VK API is not initialized')
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')

        try:
            groups = self._parse_selected_pages(self.groups, GROUPS, stdout_on=stdout_on)
        except VkAPIError as ex:
            self.print('ERROR: Failed to get user\'s groups: {message}\n'.format(message=ex.message))
            return []

        if not groups:
            return []

        return self._get_liked_posts(groups, GROUPS, html_report_on=html_report_on,
                                     stdout_on=stdout_on)

    def get_liked_people_posts(self, html_report_on=True, stdout_on=False):
        if not self.vk_api_wrapper:
            raise VkLikeCheckerException('VK API is not initialized')
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')

        people = self._parse_selected_pages(self.people, PEOPLE, stdout_on=stdout_on)

        if not people:
            return []

        return self._get_liked_posts(people, PEOPLE, html_report_on=html_report_on,
                                     stdout_on=stdout_on)

    def _parse_selected_pages(self, selected_pages, item_type, stdout_on=False):
        pages = []

        has_skip = False
        for item in selected_pages:
            if item.startswith('!'):
                has_skip = True
                break

        if [NONE] == selected_pages:
            return []

        if DEFAULT in selected_pages or has_skip:
            if PUBLIC_PAGES == item_type:
                pages.extend(self.vk_api_wrapper.get_user_public_pages().get('items'))
            elif GROUPS == item_type:
                pages.extend(self.vk_api_wrapper.get_user_groups().get('items'))
            elif PEOPLE == item_type:
                pages.extend(self.vk_api_wrapper.get_user_friends().get('items'))
            else:
                return []

            if DEFAULT in selected_pages:
                selected_pages.remove(DEFAULT)

        for item in selected_pages:
            if item.startswith('!'):
                try:
                    item = item.replace('!', '')

                    page = self._get_item_page_info(item, item_type)

                    if not page:
                        return []

                    can_skip = False
                    for _page in pages:
                        if _page.get('id') == page[0].get('id'):
                            can_skip = True
                            if stdout_on:
                                self.print('SKIPPING: {}'.format(self._get_item_name(_page)))
                            pages.remove(_page)
                            break

                    if not can_skip:
                        if stdout_on:
                            self.print('WARNING: can\'t skip {} as it is not in the default set '
                                       'of {}'.format(item, item_type))
                    # TODO: add skipping persons for public pages here
                except VkAPIError:
                    if stdout_on:
                        self.print('WARNING: {} is invalid {}'.format(item, item_type))
            else:
                try:
                    page = self._get_item_page_info(item, item_type)

                    if not page:
                        return []

                    is_duplicate = False
                    for _page in pages:
                        if _page.get('id') == page[0].get('id'):
                            is_duplicate = True
                            break

                    if not is_duplicate:
                        pages.extend(page)
                    else:
                        if stdout_on:
                            self.print('WARNING: {} already in the default set of {}'.format(item, item_type))
                except VkAPIError:
                    if stdout_on:
                        self.print('WARNING: {} is invalid {}'.format(item, item_type))
        return pages

    def _get_liked_posts(self, source, item_type, html_report_on=True, stdout_on=False):
        if not self.vk_api_wrapper:
            raise VkLikeCheckerException('VK API is not initialized')
        if not self.earliest_time:
            raise VkLikeCheckerException('Earliest time is not calculated')
        if not self.html_report.file and html_report_on:
            raise VkLikeCheckerException('HTML report is not initialized')
        if stdout_on:
            self.print('Check {} {}...'.format(len(source), item_type))
        if html_report_on:
            self.html_report.write('<br><b>Check {} {}...</b><br><br>\n'.format(len(source), item_type))
        result = []
        item_counter = 0
        for item in source:
            try:
                item_counter += 1

                item_id = self._get_item_id(item)
                name = self._get_item_name(item)

                if not item_id or not name:
                    continue

                header_printed = False

                posts_offset = 0
                while True:
                    for retry in range(10):
                        try:
                            posts = self.vk_api_wrapper.get_posts_from_wall(item_id, posts_offset)
                            break
                        except requests.exceptions.RequestException:
                            time.sleep(15)
                            if stdout_on:
                                self.print('WARNING: Read timed out. Re-initialize VK API...')
                            self.initialize_vk_api(stdout_on=False)

                    if not posts['items']:
                        break

                    is_some_post_older_earliest_time = False

                    for post in posts['items']:
                        if stdout_on:
                            status = 'Check {}/{}: {}'.format(item_counter, len(source), name)
                            self.print(status, end='\r')
                        if post['date'] >= self.earliest_time:
                            likes_offset = 0
                            while True:
                                for retry in range(10):
                                    try:
                                        likes = self.vk_api_wrapper.get_likes_from_post(item_id, post['id'],
                                                                                        likes_offset)
                                        break
                                    except requests.exceptions.RequestException:
                                        time.sleep(15)
                                        if stdout_on:
                                            self.print('WARNING: Read timed out. Re-initialize VK API...BB')
                                        self.initialize_vk_api(stdout_on=False)

                                if not likes['items']:
                                    break

                                if self.vk_api_wrapper.get_user_id() in likes['items']:
                                    if not header_printed:
                                        header_printed = True
                                        if stdout_on:
                                            self.print(name)
                                        if html_report_on:
                                            self.html_report.write('<b>{}</b><br>\n'.format(name))

                                    link = 'https://vk.com/wall{owner_id}_{item_id}'.format(
                                        owner_id=item_id, item_id=post['id'])

                                    if stdout_on:
                                        self.print('    {}'.format(link))
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
            scan_completed = 'Check {} {}... completed.'.format(len(source), item_type)
            if not len(result):
                scan_completed += ' Nothing found.'
            self.print(scan_completed, end='\r')
            self.print()
        return result

    @staticmethod
    def _get_item_id(item):
        if item.get('type') in [PROFILE] or item.get('first_name'):
            return item.get('id')
        elif item.get('type') in [PAGE, GROUP]:
            return -item.get('id')
        else:
            return None

    @staticmethod
    def _get_item_name(item):
        if item.get('type') in [PROFILE] or item.get('first_name'):
            if not item.get('first_name') or not item.get('last_name'):
                return None
            return '{} {}'.format(item.get('first_name'), item.get('last_name'))
        elif item.get('type') in [PAGE, GROUP]:
            return item.get('name')
        else:
            return None

    def _get_item_page_info(self, item, item_type):
        if item_type in [PUBLIC_PAGES, GROUPS]:
            return self.vk_api_wrapper.get_public_page_or_group_page_info(item)
        elif item_type in [PEOPLE]:
            time.sleep(0.25)
            return self.vk_api_wrapper.get_person_page_info(item)
        else:
            return None
