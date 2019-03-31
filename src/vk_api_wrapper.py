import vk_requests
import time

from src.locale import locale, lang

DELAY = 0.25


class VkApiWrapperException(Exception):
    pass


class VkApiWrapper:
    def __init__(self, app_id=None, login=None, password=None, token=None):
        self.app_id = app_id
        self.login = login
        self.password = password
        self.token = token
        self.api = None
        self.user_id = None

    def set_app_id(self, app_id):
        self.app_id = app_id

    def set_login(self, login):
        self.login = login

    def set_password(self, password):
        self.password = password

    def set_token(self, token):
        self.token = token

    def set_user_id(self, user):
        # TODO: requests.exceptions.ReadTimeout exception here
        self.user_id = self.api.users.get(user_ids=user)[0]['id']

    def initialize_vk_api(self):
        if self.app_id and self.login and self.password:
            self.api = vk_requests.create_api(app_id=self.app_id, login=self.login, password=self.password)
        elif self.token:
            self.api = vk_requests.create_api(service_token=self.token)
        else:
            raise VkApiWrapperException(locale[35][lang])

    def check_if_vk_api_initialized(self):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        time.sleep(DELAY)
        if self.api.users.get(user_ids=1)[0]['id']:
            return True
        else:
            return False

    def get_user_id(self):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        return self.user_id

    def get_user_first_name(self):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        if not self.user_id:
            raise VkApiWrapperException(locale[36][lang])
        time.sleep(DELAY)
        return self.api.users.get(user_ids=self.user_id)[0]['first_name']

    def get_user_last_name(self):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        if not self.user_id:
            raise VkApiWrapperException(locale[36][lang])
        time.sleep(DELAY)
        return self.api.users.get(user_ids=self.user_id)[0]['last_name']

    def get_user_avatar_small(self):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        if not self.user_id:
            raise VkApiWrapperException(locale[36][lang])
        time.sleep(DELAY)
        return self.api.users.get(user_ids=self.user_id, fields='photo_50')[0]['photo_50']

    def get_user_public_pages(self):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        if not self.user_id:
            raise VkApiWrapperException(locale[36][lang])
        time.sleep(DELAY)
        return self.api.users.getSubscriptions(user_id=self.user_id, extended=1, count=200)

    def get_user_groups(self):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        if not self.user_id:
            raise VkApiWrapperException(locale[36][lang])
        time.sleep(DELAY)
        return self.api.groups.get(user_id=self.user_id, filter='groups,', extended=1, count=1000)

    def get_user_friends(self):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        if not self.user_id:
            raise VkApiWrapperException(locale[36][lang])
        time.sleep(DELAY)
        return self.api.friends.get(user_id=self.user_id, fields='first_name,last_name')

    def get_posts_from_wall(self, item_id, posts_offset):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        time.sleep(DELAY)
        return self.api.wall.get(owner_id=item_id, count=100, offset=posts_offset)

    def get_likes_from_post(self, owner_id, item_id, likes_offset):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        time.sleep(DELAY)
        return self.api.likes.getList(type='post', owner_id=owner_id, item_id=item_id, skip_own=0, count=1000,
                                      offset=likes_offset)

    def get_public_page_or_group_page_info(self, item):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        time.sleep(DELAY)
        return self.api.groups.getById(group_id=item)

    def get_person_page_info(self, item):
        if not self.api:
            raise VkApiWrapperException(locale[10][lang])
        time.sleep(DELAY)
        return self.api.users.get(user_ids=item)
