from environ import Env

from config.conf.boilerplate import BASE_DIR


env: Env = Env(
    DEBUG=(bool, False),
)

envpath = BASE_DIR / '.env'

if envpath.exists():
    Env.read_env(envpath)
else:
    Env.read_env()

__all__ = (
    'env',
)