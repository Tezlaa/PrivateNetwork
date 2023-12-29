from config.conf.environ import env
from config.conf.database import DOCKER_RUN


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (
                    env('CHANNEL_REDIS_HOST', cast=str, default='localhost') if DOCKER_RUN else 'localhost',
                    env('CHANNEL_REDIS_PORT', cast=int, default=6379),
                )
            ]
        }
    }
}