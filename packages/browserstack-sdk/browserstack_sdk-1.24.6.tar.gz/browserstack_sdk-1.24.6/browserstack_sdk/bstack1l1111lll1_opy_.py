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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack1111l1111_opy_
from browserstack_sdk.bstack1ll1llllll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llll111ll_opy_
class bstack11l11l1ll_opy_:
    def __init__(self, args, logger, bstack111l1l1l11_opy_, bstack111l1l1lll_opy_):
        self.args = args
        self.logger = logger
        self.bstack111l1l1l11_opy_ = bstack111l1l1l11_opy_
        self.bstack111l1l1lll_opy_ = bstack111l1l1lll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lllll1l11_opy_ = []
        self.bstack111l1llll1_opy_ = None
        self.bstack1lll1l1l1_opy_ = []
        self.bstack111l1lll1l_opy_ = self.bstack1l11ll1l11_opy_()
        self.bstack1l1l111l1l_opy_ = -1
    def bstack1l1ll1l11_opy_(self, bstack111l1ll1ll_opy_):
        self.parse_args()
        self.bstack111l1l11ll_opy_()
        self.bstack111l1ll11l_opy_(bstack111l1ll1ll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack111l1lllll_opy_():
        import importlib
        if getattr(importlib, bstack11_opy_ (u"ࠫ࡫࡯࡮ࡥࡡ࡯ࡳࡦࡪࡥࡳࠩྨ"), False):
            bstack111l1l11l1_opy_ = importlib.find_loader(bstack11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧྩ"))
        else:
            bstack111l1l11l1_opy_ = importlib.util.find_spec(bstack11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨྪ"))
    def bstack111l1ll111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1l111l1l_opy_ = -1
        if self.bstack111l1l1lll_opy_ and bstack11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧྫ") in self.bstack111l1l1l11_opy_:
            self.bstack1l1l111l1l_opy_ = int(self.bstack111l1l1l11_opy_[bstack11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨྫྷ")])
        try:
            bstack111l1l1111_opy_ = [bstack11_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫྭ"), bstack11_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ྮ"), bstack11_opy_ (u"ࠫ࠲ࡶࠧྯ")]
            if self.bstack1l1l111l1l_opy_ >= 0:
                bstack111l1l1111_opy_.extend([bstack11_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ྰ"), bstack11_opy_ (u"࠭࠭࡯ࠩྱ")])
            for arg in bstack111l1l1111_opy_:
                self.bstack111l1ll111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111l1l11ll_opy_(self):
        bstack111l1llll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111l1llll1_opy_ = bstack111l1llll1_opy_
        return bstack111l1llll1_opy_
    def bstack1l11ll1111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack111l1lllll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1llll111ll_opy_)
    def bstack111l1ll11l_opy_(self, bstack111l1ll1ll_opy_):
        bstack1l1l1lll1_opy_ = Config.bstack11l111l11_opy_()
        if bstack111l1ll1ll_opy_:
            self.bstack111l1llll1_opy_.append(bstack11_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫྲ"))
            self.bstack111l1llll1_opy_.append(bstack11_opy_ (u"ࠨࡖࡵࡹࡪ࠭ླ"))
        if bstack1l1l1lll1_opy_.bstack111l1lll11_opy_():
            self.bstack111l1llll1_opy_.append(bstack11_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨྴ"))
            self.bstack111l1llll1_opy_.append(bstack11_opy_ (u"ࠪࡘࡷࡻࡥࠨྵ"))
        self.bstack111l1llll1_opy_.append(bstack11_opy_ (u"ࠫ࠲ࡶࠧྶ"))
        self.bstack111l1llll1_opy_.append(bstack11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠪྷ"))
        self.bstack111l1llll1_opy_.append(bstack11_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨྸ"))
        self.bstack111l1llll1_opy_.append(bstack11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧྐྵ"))
        if self.bstack1l1l111l1l_opy_ > 1:
            self.bstack111l1llll1_opy_.append(bstack11_opy_ (u"ࠨ࠯ࡱࠫྺ"))
            self.bstack111l1llll1_opy_.append(str(self.bstack1l1l111l1l_opy_))
    def bstack111l1l111l_opy_(self):
        bstack1lll1l1l1_opy_ = []
        for spec in self.bstack1lllll1l11_opy_:
            bstack11lllll11l_opy_ = [spec]
            bstack11lllll11l_opy_ += self.bstack111l1llll1_opy_
            bstack1lll1l1l1_opy_.append(bstack11lllll11l_opy_)
        self.bstack1lll1l1l1_opy_ = bstack1lll1l1l1_opy_
        return bstack1lll1l1l1_opy_
    def bstack1l11ll1l11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111l1lll1l_opy_ = True
            return True
        except Exception as e:
            self.bstack111l1lll1l_opy_ = False
        return self.bstack111l1lll1l_opy_
    def bstack1lll1111_opy_(self, bstack111l1l1l1l_opy_, bstack1l1ll1l11_opy_):
        bstack1l1ll1l11_opy_[bstack11_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩྻ")] = self.bstack111l1l1l11_opy_
        multiprocessing.set_start_method(bstack11_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩྼ"))
        bstack1llll1ll1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1l1l11_opy_ = manager.list()
        if bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ྽") in self.bstack111l1l1l11_opy_:
            for index, platform in enumerate(self.bstack111l1l1l11_opy_[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ྾")]):
                bstack1llll1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111l1l1l1l_opy_,
                                                            args=(self.bstack111l1llll1_opy_, bstack1l1ll1l11_opy_, bstack1lll1l1l11_opy_)))
            bstack111l1l1ll1_opy_ = len(self.bstack111l1l1l11_opy_[bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ྿")])
        else:
            bstack1llll1ll1_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111l1l1l1l_opy_,
                                                        args=(self.bstack111l1llll1_opy_, bstack1l1ll1l11_opy_, bstack1lll1l1l11_opy_)))
            bstack111l1l1ll1_opy_ = 1
        i = 0
        for t in bstack1llll1ll1_opy_:
            os.environ[bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ࿀")] = str(i)
            if bstack11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ࿁") in self.bstack111l1l1l11_opy_:
                os.environ[bstack11_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ࿂")] = json.dumps(self.bstack111l1l1l11_opy_[bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭࿃")][i % bstack111l1l1ll1_opy_])
            i += 1
            t.start()
        for t in bstack1llll1ll1_opy_:
            t.join()
        return list(bstack1lll1l1l11_opy_)
    @staticmethod
    def bstack1lll111l_opy_(driver, bstack111ll11111_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ࿄"), None)
        if item and getattr(item, bstack11_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧ࿅"), None) and not getattr(item, bstack11_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨ࿆"), False):
            logger.info(
                bstack11_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨ࿇"))
            bstack111l1ll1l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1111l1111_opy_.bstack1l1llll1l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)