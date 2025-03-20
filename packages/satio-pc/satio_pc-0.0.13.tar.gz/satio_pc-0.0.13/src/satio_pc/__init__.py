import string
import random
import concurrent.futures
from tqdm.auto import tqdm

try:
    import satio_pc.layers  # NOQA
    from satio_pc.extension import SatioTimeSeries  # noqa
except Exception:
    # skip error in make recipes that need version outside dev env
    pass

from satio_pc._version import __version__


__all__ = ['__version__']


def parallelize(f,
                my_iter,
                max_workers=4,
                progressbar=True,
                total=None,
                use_process_pool=False):

    if total is None:
        try:
            total = len(my_iter)
        except Exception:
            total = None
            progressbar = False

    if use_process_pool:
        Pool = concurrent.futures.ProcessPoolExecutor
    else:
        Pool = concurrent.futures.ThreadPoolExecutor

    with Pool(max_workers=max_workers) as ex:
        if progressbar:
            results = list(tqdm(ex.map(f, my_iter), total=total))
        else:
            results = list(ex.map(f, my_iter))
    return results


def random_string(n=8):
    x = ''.join(random.choice(string.ascii_uppercase +
                              string.ascii_lowercase +
                              string.digits) for _ in range(n))
    return x
