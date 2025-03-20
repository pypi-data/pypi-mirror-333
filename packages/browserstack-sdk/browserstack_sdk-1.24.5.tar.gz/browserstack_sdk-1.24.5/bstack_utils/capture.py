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
import builtins
import logging
class bstack11l11l1l11_opy_:
    def __init__(self, handler):
        self._1l111ll1111_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1l111l1llll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l11l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᕘ"), bstack1l11l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᕙ"), bstack1l11l_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧᕚ"), bstack1l11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᕛ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1l111ll11l1_opy_
        self._1l111l1lll1_opy_()
    def _1l111ll11l1_opy_(self, *args, **kwargs):
        self._1l111ll1111_opy_(*args, **kwargs)
        message = bstack1l11l_opy_ (u"ࠨࠢࠪᕜ").join(map(str, args)) + bstack1l11l_opy_ (u"ࠩ࡟ࡲࠬᕝ")
        self._log_message(bstack1l11l_opy_ (u"ࠪࡍࡓࡌࡏࠨᕞ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᕟ"): level, bstack1l11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕠ"): msg})
    def _1l111l1lll1_opy_(self):
        for level, bstack1l111ll111l_opy_ in self._1l111l1llll_opy_.items():
            setattr(logging, level, self._1l111l1ll1l_opy_(level, bstack1l111ll111l_opy_))
    def _1l111l1ll1l_opy_(self, level, bstack1l111ll111l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1l111ll111l_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1l111ll1111_opy_
        for level, bstack1l111ll111l_opy_ in self._1l111l1llll_opy_.items():
            setattr(logging, level, bstack1l111ll111l_opy_)