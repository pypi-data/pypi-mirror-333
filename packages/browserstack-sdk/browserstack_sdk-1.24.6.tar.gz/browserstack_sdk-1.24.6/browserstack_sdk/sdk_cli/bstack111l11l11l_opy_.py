# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack1l11_opy_ = 2048
bstack111l_opy_ = 7
def bstack11_opy_ (bstack111_opy_):
    global bstack111ll1l_opy_
    bstack1llll1l_opy_ = ord (bstack111_opy_ [-1])
    bstack11ll1ll_opy_ = bstack111_opy_ [:-1]
    bstack11l1l1_opy_ = bstack1llll1l_opy_ % len (bstack11ll1ll_opy_)
    bstack111111_opy_ = bstack11ll1ll_opy_ [:bstack11l1l1_opy_] + bstack11ll1ll_opy_ [bstack11l1l1_opy_:]
    if bstack11ll1l1_opy_:
        bstack1ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11_opy_ - (bstack11l1lll_opy_ + bstack1llll1l_opy_) % bstack111l_opy_) for bstack11l1lll_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1ll111_opy_ = str () .join ([chr (ord (char) - bstack1l11_opy_ - (bstack11l1lll_opy_ + bstack1llll1l_opy_) % bstack111l_opy_) for bstack11l1lll_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1ll111_opy_)
import threading
import queue
from typing import Callable, Union
class bstack111l11l1l1_opy_:
    timeout: int
    bstack111l11l111_opy_: Union[None, Callable]
    bstack111l111ll1_opy_: Union[None, Callable]
    def __init__(self, timeout=1, bstack111l11l1ll_opy_=1, bstack111l11l111_opy_=None, bstack111l111ll1_opy_=None):
        self.timeout = timeout
        self.bstack111l11l1ll_opy_ = bstack111l11l1ll_opy_
        self.bstack111l11l111_opy_ = bstack111l11l111_opy_
        self.bstack111l111ll1_opy_ = bstack111l111ll1_opy_
        self.queue = queue.Queue()
        self.bstack111l111lll_opy_ = threading.Event()
        self.threads = []
    def enqueue(self, job: Callable):
        if not callable(job):
            raise ValueError(bstack11_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠ࡫ࡱࡥ࠾ࠥࠨ࿍") + type(job))
        self.queue.put(job)
    def start(self):
        if self.threads:
            return
        self.threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.bstack111l11l1ll_opy_)]
        for thread in self.threads:
            thread.start()
    def stop(self):
        if not self.threads:
            return
        if not self.queue.empty():
            self.queue.join()
        self.bstack111l111lll_opy_.set()
        for _ in self.threads:
            self.queue.put(None)
        for thread in self.threads:
            thread.join()
        self.threads.clear()
    def worker(self):
        while not self.bstack111l111lll_opy_.is_set():
            try:
                job = self.queue.get(block=True, timeout=self.timeout)
                if job is None:
                    break
                try:
                    job()
                except Exception as e:
                    if callable(self.bstack111l11l111_opy_):
                        self.bstack111l11l111_opy_(e, job)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                if callable(self.bstack111l111ll1_opy_):
                    self.bstack111l111ll1_opy_(e)