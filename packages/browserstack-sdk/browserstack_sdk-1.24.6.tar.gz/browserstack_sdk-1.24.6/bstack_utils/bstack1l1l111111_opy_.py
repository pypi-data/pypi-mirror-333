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
from collections import deque
from bstack_utils.constants import *
class bstack11l1llllll_opy_:
    def __init__(self):
        self._11l11llll11_opy_ = deque()
        self._11l11ll1l11_opy_ = {}
        self._11l1l111111_opy_ = False
    def bstack11l11lll11l_opy_(self, test_name, bstack11l11lll1l1_opy_):
        bstack11l11ll1ll1_opy_ = self._11l11ll1l11_opy_.get(test_name, {})
        return bstack11l11ll1ll1_opy_.get(bstack11l11lll1l1_opy_, 0)
    def bstack11l11ll1l1l_opy_(self, test_name, bstack11l11lll1l1_opy_):
        bstack11l11llll1l_opy_ = self.bstack11l11lll11l_opy_(test_name, bstack11l11lll1l1_opy_)
        self.bstack11l11lll1ll_opy_(test_name, bstack11l11lll1l1_opy_)
        return bstack11l11llll1l_opy_
    def bstack11l11lll1ll_opy_(self, test_name, bstack11l11lll1l1_opy_):
        if test_name not in self._11l11ll1l11_opy_:
            self._11l11ll1l11_opy_[test_name] = {}
        bstack11l11ll1ll1_opy_ = self._11l11ll1l11_opy_[test_name]
        bstack11l11llll1l_opy_ = bstack11l11ll1ll1_opy_.get(bstack11l11lll1l1_opy_, 0)
        bstack11l11ll1ll1_opy_[bstack11l11lll1l1_opy_] = bstack11l11llll1l_opy_ + 1
    def bstack111ll1ll1_opy_(self, bstack11l11lllll1_opy_, bstack11l11lll111_opy_):
        bstack11l11ll1lll_opy_ = self.bstack11l11ll1l1l_opy_(bstack11l11lllll1_opy_, bstack11l11lll111_opy_)
        event_name = bstack1l111l1111l_opy_[bstack11l11lll111_opy_]
        bstack1ll11111ll1_opy_ = bstack11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᯑ").format(bstack11l11lllll1_opy_, event_name, bstack11l11ll1lll_opy_)
        self._11l11llll11_opy_.append(bstack1ll11111ll1_opy_)
    def bstack1ll1l1l1ll_opy_(self):
        return len(self._11l11llll11_opy_) == 0
    def bstack1lll111ll_opy_(self):
        bstack11l11llllll_opy_ = self._11l11llll11_opy_.popleft()
        return bstack11l11llllll_opy_
    def capturing(self):
        return self._11l1l111111_opy_
    def bstack1llll11l_opy_(self):
        self._11l1l111111_opy_ = True
    def bstack11l1l111l_opy_(self):
        self._11l1l111111_opy_ = False