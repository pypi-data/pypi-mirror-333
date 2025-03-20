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
class bstack1lll1111ll_opy_:
    def __init__(self, handler):
        self._11l1111l111_opy_ = None
        self.handler = handler
        self._11l11111lll_opy_ = self.bstack11l1111l11l_opy_()
        self.patch()
    def patch(self):
        self._11l1111l111_opy_ = self._11l11111lll_opy_.execute
        self._11l11111lll_opy_.execute = self.bstack11l11111ll1_opy_()
    def bstack11l11111ll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥ᱉"), driver_command, None, this, args)
            response = self._11l1111l111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥ᱊"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11l11111lll_opy_.execute = self._11l1111l111_opy_
    @staticmethod
    def bstack11l1111l11l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver