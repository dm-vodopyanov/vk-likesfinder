import vk_api


class VkApiWrapperException(Exception):
    pass


class VkApiWrapper:
    def __init__(self, app_id=None, login=None, password=None, token=None):
        self.app_id = app_id
        self.login = login
        self.password = password
        self.token = token
        self.api = None
        self.api_version = None
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
        self.user_id = self.api.users.get(user_ids=user)[0]['id']

    def initialize_vk_api(self):
        if self.app_id and self.login and self.password:
            api = vk_api.VkApi(app_id=self.app_id, login=self.login, password=self.password)
            token_only = False
        elif self.token:
            api = vk_api.VkApi(token=self.token)
            token_only = True
        else:
            raise VkApiWrapperException('Login/password or token are empty.')
        try:
            self.api_version = api.api_version
            api.auth(token_only=token_only)
        except vk_api.AuthError as error_msg:
            raise VkApiWrapperException(error_msg)
        self.api = api.get_api()

    def check_if_vk_api_initialized(self):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        if self.api.users.get(user_ids=1)[0]['id'] == 1:
            return True
        else:
            return False

    def is_post_liked_by_user(self, owner_id, item_id):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        return self.api.likes.isLiked(type='post', user_id=self.user_id, owner_id=owner_id, item_id=item_id)['liked']

    def get_user_id(self):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        return self.user_id

    def get_user_first_name(self):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        if not self.user_id:
            raise VkApiWrapperException('User ID is not initialized')
        return self.api.users.get(user_ids=self.user_id)[0]['first_name']

    def get_user_last_name(self):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        if not self.user_id:
            raise VkApiWrapperException('User ID is not initialized')
        return self.api.users.get(user_ids=self.user_id)[0]['last_name']

    def get_user_avatar_small(self):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        if not self.user_id:
            raise VkApiWrapperException('User ID is not initialized')
        return self.api.users.get(user_ids=self.user_id, fields='photo_50')[0]['photo_50']

    def get_user_public_pages(self):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        if not self.user_id:
            raise VkApiWrapperException('User ID is not initialized')
        return self.api.users.getSubscriptions(user_id=self.user_id, extended=1, count=200)

    def get_user_groups(self):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        if not self.user_id:
            raise VkApiWrapperException('User ID is not initialized')
        return self.api.groups.get(user_id=self.user_id, filter='groups,', extended=1, count=1000)

    def get_user_friends(self):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        if not self.user_id:
            raise VkApiWrapperException('User ID is not initialized')
        return self.api.friends.get(user_id=self.user_id, fields='first_name,last_name')

    def get_posts_from_wall(self, item_id, posts_offset):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        return self.api.wall.get(owner_id=item_id, count=100, offset=posts_offset)

    def get_public_page_or_group_page_info(self, item):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        return self.api.groups.getById(group_id=item)

    def get_person_page_info(self, item):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        return self.api.users.get(user_ids=item)
