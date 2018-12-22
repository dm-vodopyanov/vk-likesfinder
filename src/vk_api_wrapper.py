import vk_requests


class VkApiWrapperException(Exception):
    pass


class VkApiWrapper:
    def __init__(self, application_id, service_token):
        self.application_id = int(application_id)
        self.service_token = service_token
        self.api = None
        self.user_id = None

    def set_application_id(self, application_id):
        self.application_id = int(application_id)

    def set_service_token(self, service_token):
        self.service_token = service_token

    def set_user_id(self, user):
        self.user_id = self.api.users.get(user_ids=user)[0]['id']

    def initialize_vk_api(self):
        self.api = vk_requests.create_api(app_id=self.application_id, service_token=self.service_token)

    def check_if_vk_api_initialized(self):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        if self.api.users.get(user_ids=1)[0]['id']:
            return True
        else:
            return False

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

    def get_user_public_pages(self):
        if not self.api:
            raise VkApiWrapperException('VK API is not initialized')
        if not self.user_id:
            raise VkApiWrapperException('User ID is not initialized')
        return self.api.users.getSubscriptions(user_id=self.user_id, extended=1, count=200)

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

    def get_likes_from_post(self, owner_id, item_id, likes_offset):
        return self.api.likes.getList(type='post', owner_id=owner_id, item_id=item_id, skip_own=0, count=1000,
                                      offset=likes_offset)
