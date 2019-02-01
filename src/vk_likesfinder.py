import datetime
import requests
import time
import os

from vk_requests.exceptions import VkAPIError
from src.vk_api_wrapper import VkApiWrapper
from src.html_report import HtmlReport
from src.cli_report import CliReport
from src.locale import locale, lang


DEFAULT = 'all'  # it can't be vk.com/all as all is too short
NONE = 'none'  # it can't be vk.com/none as none is too short

PUBLIC_PAGES = 'public pages'
GROUPS = 'groups'
PEOPLE = 'people'

PROFILE = 'profile'
PERSON = 'person'
GROUP = 'group'
PAGE = 'page'


class VkLikesFinderException(Exception):
    pass


class VkLikesFinder:
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
        self.cli_report = CliReport()

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
                    raise VkLikesFinderException(locale[0][lang])
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
        self.header = 'VK LikesFinder {}{}'.format(version, locale[18][lang])

    def set_earliest_time(self):
        if not self.interval:
            raise VkLikesFinderException(locale[1][lang])
        self.earliest_time = int(datetime.datetime.today().timestamp()) - int(self.interval) * 3600

    def initialize_html_report(self):
        if not self.user:
            raise VkLikesFinderException(locale[2][lang])
        if not self.location:
            raise VkLikesFinderException(locale[3][lang])
        self.html_report.set_path(os.path.join(self.location, 'vk-likesfinder-report-{}_{}.html'.format(
            self.user, str(self.start_time).replace(' ', '_').replace(':', '.').lower())))

        self.html_report.initialize_file(self.html_report.path)

        if self.html_report.is_initialized:
            self.cli_report.print('{}\n    {}'.format(locale[4][lang], self.html_report.path))
            self.cli_report.print()

        self.html_report.write('<html><head><meta charset="utf-8"/>'
                               '<title>{title} - {report}</title></head><body>\n'.format(title=self.header,
                                                                                         report=locale[5][lang]))
        self.html_report.write('<h2><img src="https://raw.githubusercontent.com/dmitryvodop/vk-likechecker/master/'
                               'images/report/icon_report.png" alt="VK LikeChecker" width="19" height="16"> '
                               '{title}</h2><b>{report_generated}</b> {date}<br><br>\n'.format(
                                title=self.header, report_generated=locale[6][lang], date=self.start_time))

    def initialize_vk_api(self):
        self.vk_api_wrapper = VkApiWrapper(app_id=self.app_id, login=self.login, password=self.password,
                                           token=self.token)
        self.vk_api_wrapper.initialize_vk_api()

        if self.vk_api_wrapper.check_if_vk_api_initialized():
            self.cli_report.print(locale[7][lang])
            self.cli_report.print('{}\n'.format(locale[8][lang]))
        else:
            self.cli_report.print(locale[9][lang])

        self.vk_api_wrapper.set_user_id(self.user)

    def show_basic_info(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException(locale[10][lang])
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException(locale[11][lang])
        # print user first name and last name
        checking_user = '{} {}'.format(self.vk_api_wrapper.get_user_first_name(),
                                       self.vk_api_wrapper.get_user_last_name())
        self.cli_report.print('{}: {}'.format(locale[12][lang], checking_user))

        self.html_report.write('<b>{}:<br><br><a href="{}" target="_blank"><img style="margin-left:30px; '
                               'margin-right:10px" src="{}" alt="{}" align="left"></a> '.format(
                                locale[12][lang],
                                'https://vk.com/id{}'.format(self.vk_api_wrapper.user_id),
                                self.vk_api_wrapper.get_user_avatar_small(), checking_user))
        self.html_report.write('<a href="{}" target="_blank">{}</a></b><br><br><br>\n'.format(
            'https://vk.com/id{}'.format(self.vk_api_wrapper.user_id),
            checking_user.replace(' ', '<br>')))

        # print selected searching interval
        earliest_time_formatted = datetime.datetime.fromtimestamp(self.earliest_time)

        self.cli_report.print('{}: {} {} {})'.format(locale[13][lang], self.interval, locale[14][lang],
                                                     earliest_time_formatted))
        self.cli_report.print()

        self.html_report.write('<b>{}:</b><br><br><div style="text-indent:30px;">{} {} {})</div><br><br>\n'.format(
            locale[13][lang], self.interval, locale[14][lang], earliest_time_formatted))

    def show_likes_count(self):
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException(locale[11][lang])

        self.cli_report.print('\n{} {}'.format(self.likes_count, locale[15][lang]))

        self.html_report.write('<br><br><b>{} {}</b>\n'.format(self.likes_count, locale[15][lang]))

    def get_app_id(self):
        return self.app_id

    def get_liked_public_pages_posts(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException(locale[10][lang])
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException(locale[11][lang])

        public_pages = self._parse_selected_pages(self.public_pages, PUBLIC_PAGES)

        if not public_pages:
            return []

        return self._get_liked_posts(public_pages, PUBLIC_PAGES)

    def get_liked_groups_posts(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException(locale[10][lang])
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException(locale[11][lang])

        try:
            groups = self._parse_selected_pages(self.groups, GROUPS)
        except VkAPIError as ex:
            self.cli_report.print('Check groups...')
            self.cli_report.print('{}\n  {message}\n'.format(locale[16][lang], message=ex.message))
            return []

        if not groups:
            return []

        return self._get_liked_posts(groups, GROUPS)

    def get_liked_people_posts(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException(locale[10][lang])
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException(locale[11][lang])

        people = self._parse_selected_pages(self.people, PEOPLE)

        if not people:
            return []

        return self._get_liked_posts(people, PEOPLE)

    def _parse_selected_pages(self, selected_pages, item_type):
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

                            self.cli_report.print('{} {}'.format(locale[17][lang], self._get_item_name(_page)))
                            pages.remove(_page)
                            break

                    if not can_skip:
                        self.cli_report.print('WARNING: can\'t skip {} as it is not in the default set '
                                              'of {}'.format(item, item_type))
                    # TODO: add skipping persons for public pages here
                except VkAPIError:
                    self.cli_report.print('WARNING: {} is invalid {}'.format(item, item_type))
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
                        self.cli_report.print('WARNING: {} already in the default set of {}'.format(item, item_type))
                except VkAPIError:
                    self.cli_report.print('WARNING: {} is invalid {}'.format(item, item_type))
        return pages

    def _get_liked_posts(self, source, item_type):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException('VK API is not initialized')
        if not self.earliest_time:
            raise VkLikesFinderException('Earliest time is not calculated')
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException('HTML report is not initialized')

        self.cli_report.print('Check {} {}...'.format(len(source), item_type))
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
                            self.cli_report.print('WARNING: Read timed out. Re-initialize VK API...')
                            self.initialize_vk_api()

                    if not posts['items']:
                        break

                    is_some_post_older_earliest_time = False

                    for post in posts['items']:
                        status = 'Check {}/{}: {}'.format(item_counter, len(source), name)
                        self.cli_report.print(status, end='\r')
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
                                        self.cli_report.print('WARNING: Read timed out. Re-initialize VK API...')
                                        self.initialize_vk_api()

                                if not likes['items']:
                                    break

                                if self.vk_api_wrapper.get_user_id() in likes['items']:
                                    if not header_printed:
                                        header_printed = True
                                        self.cli_report.print(name)

                                        self.html_report.write('<b>{}</b><br>\n'.format(name))

                                    link = 'https://vk.com/wall{owner_id}_{item_id}'.format(
                                        owner_id=item_id, item_id=post['id'])

                                    self.cli_report.print('    {}'.format(link))

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

        scan_completed = 'Check {} {}... completed.'.format(len(source), item_type)
        if not len(result):
            scan_completed += ' Nothing found.'
        self.cli_report.print(scan_completed, end='\r')
        self.cli_report.print()
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
            return self.vk_api_wrapper.get_person_page_info(item)
        else:
            return None
