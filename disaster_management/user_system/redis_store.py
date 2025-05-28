import redis
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables from .env file
redis_host = os.getenv('REDIS_HOST')

class RedisUserData:

    def __init__(self, host=redis_host):
        self.redis_client = redis.Redis(host=host, port=6379, db=0)

    def get_user_data(self, user_id):
        # Get user data from Redis
        user_data = self.redis_client.get(user_id)
        return user_data.decode() if user_data else None

    def set_user_data(self, user_id, data):
        # Set user data in Redis
        self.redis_client.set(user_id, data)

    def delete_user_data(self, user_id):
        # Delete user data from Redis
        self.redis_client.delete(user_id)

    def get_all_user_data(self):
        # Get all user data from Redis
        # all_user_data = self.redis_client.keys('*')
        return [key.decode() for key in self.redis_client.keys('*')]
        

