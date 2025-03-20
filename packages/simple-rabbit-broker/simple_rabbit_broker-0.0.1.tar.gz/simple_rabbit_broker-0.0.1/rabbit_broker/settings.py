import environ

env = environ.Env()

RABBIT_URL = env.str("RABBIT_URL")
SERVICE_NAME = env.str("SERVICE_NAME")
