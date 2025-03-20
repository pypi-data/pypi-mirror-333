# coding: UTF-8
import sys
bstack11lll_opy_ = sys.version_info [0] == 2
bstack1l_opy_ = 2048
bstack1l11lll_opy_ = 7
def bstack1l11l_opy_ (bstack11l11_opy_):
    global bstack111ll1_opy_
    bstack1111l1_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1ll1ll_opy_ = bstack11l11_opy_ [:-1]
    bstack1111111_opy_ = bstack1111l1_opy_ % len (bstack1ll1ll_opy_)
    bstack1lll_opy_ = bstack1ll1ll_opy_ [:bstack1111111_opy_] + bstack1ll1ll_opy_ [bstack1111111_opy_:]
    if bstack11lll_opy_:
        bstack1111ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l_opy_ - (bstack1ll1lll_opy_ + bstack1111l1_opy_) % bstack1l11lll_opy_) for bstack1ll1lll_opy_, char in enumerate (bstack1lll_opy_)])
    else:
        bstack1111ll1_opy_ = str () .join ([chr (ord (char) - bstack1l_opy_ - (bstack1ll1lll_opy_ + bstack1111l1_opy_) % bstack1l11lll_opy_) for bstack1ll1lll_opy_, char in enumerate (bstack1lll_opy_)])
    return eval (bstack1111ll1_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1l11111lll_opy_:
    def __init__(self):
        self._11l1l111111_opy_ = deque()
        self._11l11lll1l1_opy_ = {}
        self._11l11llllll_opy_ = False
    def bstack11l11lll1ll_opy_(self, test_name, bstack11l11llll1l_opy_):
        bstack11l11lll11l_opy_ = self._11l11lll1l1_opy_.get(test_name, {})
        return bstack11l11lll11l_opy_.get(bstack11l11llll1l_opy_, 0)
    def bstack11l11llll11_opy_(self, test_name, bstack11l11llll1l_opy_):
        bstack11l11ll1l11_opy_ = self.bstack11l11lll1ll_opy_(test_name, bstack11l11llll1l_opy_)
        self.bstack11l11lllll1_opy_(test_name, bstack11l11llll1l_opy_)
        return bstack11l11ll1l11_opy_
    def bstack11l11lllll1_opy_(self, test_name, bstack11l11llll1l_opy_):
        if test_name not in self._11l11lll1l1_opy_:
            self._11l11lll1l1_opy_[test_name] = {}
        bstack11l11lll11l_opy_ = self._11l11lll1l1_opy_[test_name]
        bstack11l11ll1l11_opy_ = bstack11l11lll11l_opy_.get(bstack11l11llll1l_opy_, 0)
        bstack11l11lll11l_opy_[bstack11l11llll1l_opy_] = bstack11l11ll1l11_opy_ + 1
    def bstack1l1llll1ll_opy_(self, bstack11l11ll1lll_opy_, bstack11l11lll111_opy_):
        bstack11l11ll1l1l_opy_ = self.bstack11l11llll11_opy_(bstack11l11ll1lll_opy_, bstack11l11lll111_opy_)
        event_name = bstack1l1111lll11_opy_[bstack11l11lll111_opy_]
        bstack1ll1111111l_opy_ = bstack1l11l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥᯐ").format(bstack11l11ll1lll_opy_, event_name, bstack11l11ll1l1l_opy_)
        self._11l1l111111_opy_.append(bstack1ll1111111l_opy_)
    def bstack11ll11lll1_opy_(self):
        return len(self._11l1l111111_opy_) == 0
    def bstack11lll1lll_opy_(self):
        bstack11l11ll1ll1_opy_ = self._11l1l111111_opy_.popleft()
        return bstack11l11ll1ll1_opy_
    def capturing(self):
        return self._11l11llllll_opy_
    def bstack1l1lll1l_opy_(self):
        self._11l11llllll_opy_ = True
    def bstack1l1ll1111_opy_(self):
        self._11l11llllll_opy_ = False