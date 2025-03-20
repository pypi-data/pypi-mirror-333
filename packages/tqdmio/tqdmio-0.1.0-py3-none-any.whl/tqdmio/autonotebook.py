from tqdm.autonotebook import tqdm

from ._tqdmio import tqdmio as _tqdmio


class tqdmio(_tqdmio):
    def _init_tqdm(self, *args, **kwargs):
        self._tqdm = tqdm(*args, **kwargs)
