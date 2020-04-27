import datetime
import os

from vk_api.exceptions import VkApiError
from vk_api.exceptions import ApiError
from src.vk_api_wrapper import VkApiWrapper
from src.html_report import HtmlReport
from src.cli_report import CliReport


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
                    raise VkLikesFinderException('Incorrect authorization token file. Check documentation '
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
        self.header = 'VK LikesFinder {}'.format(version)

    def set_earliest_time(self):
        if not self.interval:
            raise VkLikesFinderException('Searching interval is empty')
        self.earliest_time = int(datetime.datetime.today().timestamp()) - int(self.interval) * 3600

    def initialize_html_report(self):
        if not self.user:
            raise VkLikesFinderException('User is not initialized')
        if not self.location:
            raise VkLikesFinderException('Cannot identify tool location')
        self.html_report.set_path(os.path.join(self.location, 'vk-likesfinder-report-{}_{}.html'.format(
            self.user, str(self.start_time).replace(' ', '_').replace(':', '.').lower())))

        self.html_report.initialize_file(self.html_report.path)

        if self.html_report.is_initialized:
            self.cli_report.print('HTML report created:\n    {}'.format(self.html_report.path))
            self.cli_report.print()

        self.html_report.write('<html><head><meta charset="utf-8"/>'
                               '<title>{title} - Report</title></head><body>\n'.format(title=self.header))
        self.html_report.write('<h2><img src="https://raw.githubusercontent.com/dm-vodopyanov/vk-likesfinder/master/'
                               'images/report/icon_report.png" alt="VK LikeChecker" width="19" height="16"> '
                               '{title}</h2><b>Report generated:</b> {date}<br><br>\n'.format(
                                title=self.header, date=self.start_time))

    def initialize_vk_api(self):
        self.vk_api_wrapper = VkApiWrapper(app_id=self.app_id, login=self.login, password=self.password,
                                           token=self.token)
        self.vk_api_wrapper.initialize_vk_api()

        if self.vk_api_wrapper.check_if_vk_api_initialized():
            self.cli_report.print('Authorized to VK successfully.')
            self.cli_report.print('VK API initialized successfully.\n')
        else:
            self.cli_report.print('ERROR: Failed to initialize VK API')

        self.vk_api_wrapper.set_user_id(self.user)

    def generate_friends_list(self):
        if not self.user:
            raise VkLikesFinderException('User is not initialized')
        self.vk_api_wrapper.get_user_friends().get('items')

        report_file_name = 'vk-friends-report-{}-{}'.format(self.vk_api_wrapper.get_user_id(), self.user)
        report_path = os.path.join(self.location, )
        for friend in self.vk_api_wrapper.get_user_friends().get('items'):
            print(friend['id'])

    def show_basic_info_cli(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException('VK API is not initialized')

        # print user first name and last name
        checking_user = '{} {}'.format(self.vk_api_wrapper.get_user_first_name(),
                                       self.vk_api_wrapper.get_user_last_name())
        self.cli_report.print('{}: {}'.format('Checking user', checking_user))

    def show_basic_info_html(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException('VK API is not initialized')
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException('HTML report is not initialized')
        # print user first name and last name
        checking_user = '{} {}'.format(self.vk_api_wrapper.get_user_first_name(),
                                       self.vk_api_wrapper.get_user_last_name())

        self.html_report.write('<b>Checking user:<br><br><a href="{}" target="_blank"><img style="margin-left:30px; '
                               'margin-right:10px" src="{}" alt="{}" align="left"></a> '.format(
                                'https://vk.com/id{}'.format(self.vk_api_wrapper.user_id),
                                self.vk_api_wrapper.get_user_avatar_small(), checking_user))
        self.html_report.write('<a href="{}" target="_blank">{}</a></b><br><br><br>\n'.format(
            'https://vk.com/id{}'.format(self.vk_api_wrapper.user_id),
            checking_user.replace(' ', '<br>')))

    def show_extended_info_cli(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException('VK API is not initialized')

        # print selected searching interval
        earliest_time_formatted = datetime.datetime.fromtimestamp(self.earliest_time)

        self.cli_report.print('Searching interval: {} hour(s) till now (since {})'.format(self.interval,
                                                                                          earliest_time_formatted))
        self.cli_report.print()

    def show_extended_info_html(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException('VK API is not initialized')
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException('HTML report is not initialized')

        # print selected searching interval
        earliest_time_formatted = datetime.datetime.fromtimestamp(self.earliest_time)

        self.html_report.write('<b>Searching interval:</b><br><br><div style="text-indent:30px;">{} hour(s) till now '
                               '(since {})</div><br>\n'.format(self.interval, earliest_time_formatted))

    def show_likes_count(self):
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException('HTML report is not initialized')

        self.cli_report.print('{} like(s) were found.'.format(self.likes_count))

        self.html_report.write('<br><b>{} like(s) were found.</b>\n'.format(self.likes_count))

    def get_app_id(self):
        return self.app_id

    def get_liked_public_pages_posts(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException('VK API is not initialized')
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException('HTML report is not initialized')

        public_pages = self._parse_selected_pages(self.public_pages, PUBLIC_PAGES)

        if not public_pages:
            return []

        return self._get_liked_posts(public_pages, PUBLIC_PAGES)

    def get_liked_groups_posts(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException('VK API is not initialized')
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException('HTML report is not initialized')

        try:
            groups = self._parse_selected_pages(self.groups, GROUPS)
        except ApiError as ex:
            self.cli_report.print('Checking groups...')
            self.cli_report.print('ERROR: Failed to get user\'s groups:\n  {message}\n'.format(message=ex))
            return []

        if not groups:
            return []

        return self._get_liked_posts(groups, GROUPS)

    def get_liked_people_posts(self):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException('VK API is not initialized')
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException('HTML report is not initialized')

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

                            self.cli_report.print('SKIPPING: {}'.format(self._get_item_name(_page)))
                            pages.remove(_page)
                            break

                    if not can_skip:
                        self.cli_report.print('WARNING: can\'t skip {} as it is not in '
                                              'the default set of {}'.format(item, item_type))
                    # TODO: add skipping persons for public pages here
                except VkApiError:
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
                        self.cli_report.print('WARNING: can\'t skip {} as it is not in '
                                              'the default set of {}'.format(item, item_type))
                except VkApiError:
                    self.cli_report.print('WARNING: {} is invalid {}'.format(item, item_type))
        return pages

    def _get_liked_posts(self, source, item_type):
        if not self.vk_api_wrapper:
            raise VkLikesFinderException('VK API is not initialized')
        if not self.earliest_time:
            raise VkLikesFinderException('Earliest time is not calculated')
        if not self.html_report.file and self.html_report.is_initialized:
            raise VkLikesFinderException('HTML report is not initialized')

        self.cli_report.print('Checking {} {}...'.format(len(source), item_type))
        self.html_report.write('<br><b>Checking {} {}...</b><br><br>\n'.format(len(source), item_type))
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
                posts_count = 0
                while True:
                    posts = self.vk_api_wrapper.get_posts_from_wall(item_id, posts_offset)

                    if not posts['items']:
                        break

                    is_some_post_older_earliest_time = False

                    for post in posts['items']:
                        status = 'Checking {}/{}: {}: {} posts were analyzed'.format(item_counter, len(source),
                                                                                     name, posts_count)
                        self.cli_report.print(status, end='\r')
                        posts_count = posts_count + 1
                        if post['date'] >= self.earliest_time:
                            if self.vk_api_wrapper.is_post_liked_by_user(owner_id=item_id, item_id=post['id']):
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
                        else:
                            if not post.get('is_pinned'):
                                is_some_post_older_earliest_time = True
                                break

                    if is_some_post_older_earliest_time:
                        break

                    posts_offset += 100
            except VkApiError:
                pass

        scan_completed = 'Checking {} {}... completed.'.format(len(source), item_type)
        if not len(result):
            scan_completed += ' Nothing found.'
        self.cli_report.print(scan_completed)
        self.cli_report.print()
        self.html_report.write('<br><b>{}</b><br><br>\n'.format(scan_completed))
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
