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
class bstack11ll11l11l_opy_(threading.Thread):
    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exc = e
    def join(self, timeout=None):
        super(bstack11ll11l11l_opy_, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret