# %%

import bz2
from time import sleep

from tqdmio import tqdmio

# %%

with tqdmio.open("file.txt", "rt") as fp:
    for line in fp:
        sleep(0.0000001)

with tqdmio.open("file.bz2", "rb") as fbz2:
    for line in fbz2:
        sleep(0.0000001)

with tqdmio.open("file.bz2", "rb") as fbz2:
    for line in bz2.open(fbz2, "rt"):
        sleep(0.0000001)
