import os
from blue_options.env import load_config, load_env, get_env

load_env(__name__)
load_config(__name__)


BLUE_GAN_LIST_OF_ALGO = str(get_env("BLUE_GAN_LIST_OF_ALGO")).split("+")
