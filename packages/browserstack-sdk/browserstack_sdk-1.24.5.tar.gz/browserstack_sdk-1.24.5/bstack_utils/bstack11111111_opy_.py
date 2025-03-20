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
class bstack1l11ll1111_opy_:
    def __init__(self, handler):
        self._11l11111lll_opy_ = None
        self.handler = handler
        self._11l1111l111_opy_ = self.bstack11l1111l11l_opy_()
        self.patch()
    def patch(self):
        self._11l11111lll_opy_ = self._11l1111l111_opy_.execute
        self._11l1111l111_opy_.execute = self.bstack11l11111ll1_opy_()
    def bstack11l11111ll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l11l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࠤ᱈"), driver_command, None, this, args)
            response = self._11l11111lll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l11l_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࠤ᱉"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11l1111l111_opy_.execute = self._11l11111lll_opy_
    @staticmethod
    def bstack11l1111l11l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver