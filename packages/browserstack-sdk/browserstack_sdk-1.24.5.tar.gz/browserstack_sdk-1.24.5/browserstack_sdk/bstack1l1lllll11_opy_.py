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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack11lll111l_opy_
from browserstack_sdk.bstack1ll1111l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1111l_opy_
class bstack1ll111ll_opy_:
    def __init__(self, args, logger, bstack111ll11111_opy_, bstack111l1llll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack111ll11111_opy_ = bstack111ll11111_opy_
        self.bstack111l1llll1_opy_ = bstack111l1llll1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1111ll1_opy_ = []
        self.bstack111l1l1ll1_opy_ = None
        self.bstack11ll11111_opy_ = []
        self.bstack111l1l1lll_opy_ = self.bstack1ll1l1ll1_opy_()
        self.bstack1lll1111_opy_ = -1
    def bstack1ll11lll1l_opy_(self, bstack111l1ll1ll_opy_):
        self.parse_args()
        self.bstack111l1lll1l_opy_()
        self.bstack111l1l11l1_opy_(bstack111l1ll1ll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack111l1l1l11_opy_():
        import importlib
        if getattr(importlib, bstack1l11l_opy_ (u"ࠪࡪ࡮ࡴࡤࡠ࡮ࡲࡥࡩ࡫ࡲࠨྦྷ"), False):
            bstack111l1lll11_opy_ = importlib.find_loader(bstack1l11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ྨ"))
        else:
            bstack111l1lll11_opy_ = importlib.util.find_spec(bstack1l11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧྩ"))
    def bstack111l1ll11l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1lll1111_opy_ = -1
        if self.bstack111l1llll1_opy_ and bstack1l11l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ྪ") in self.bstack111ll11111_opy_:
            self.bstack1lll1111_opy_ = int(self.bstack111ll11111_opy_[bstack1l11l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧྫ")])
        try:
            bstack111l1ll1l1_opy_ = [bstack1l11l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪྫྷ"), bstack1l11l_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬྭ"), bstack1l11l_opy_ (u"ࠪ࠱ࡵ࠭ྮ")]
            if self.bstack1lll1111_opy_ >= 0:
                bstack111l1ll1l1_opy_.extend([bstack1l11l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬྯ"), bstack1l11l_opy_ (u"ࠬ࠳࡮ࠨྰ")])
            for arg in bstack111l1ll1l1_opy_:
                self.bstack111l1ll11l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111l1lll1l_opy_(self):
        bstack111l1l1ll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111l1l1ll1_opy_ = bstack111l1l1ll1_opy_
        return bstack111l1l1ll1_opy_
    def bstack11ll1l1l1l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack111l1l1l11_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack111l1111l_opy_)
    def bstack111l1l11l1_opy_(self, bstack111l1ll1ll_opy_):
        bstack1ll11111ll_opy_ = Config.bstack111lll11_opy_()
        if bstack111l1ll1ll_opy_:
            self.bstack111l1l1ll1_opy_.append(bstack1l11l_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪྱ"))
            self.bstack111l1l1ll1_opy_.append(bstack1l11l_opy_ (u"ࠧࡕࡴࡸࡩࠬྲ"))
        if bstack1ll11111ll_opy_.bstack111l1l1l1l_opy_():
            self.bstack111l1l1ll1_opy_.append(bstack1l11l_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧླ"))
            self.bstack111l1l1ll1_opy_.append(bstack1l11l_opy_ (u"ࠩࡗࡶࡺ࡫ࠧྴ"))
        self.bstack111l1l1ll1_opy_.append(bstack1l11l_opy_ (u"ࠪ࠱ࡵ࠭ྵ"))
        self.bstack111l1l1ll1_opy_.append(bstack1l11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩྶ"))
        self.bstack111l1l1ll1_opy_.append(bstack1l11l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧྷ"))
        self.bstack111l1l1ll1_opy_.append(bstack1l11l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ྸ"))
        if self.bstack1lll1111_opy_ > 1:
            self.bstack111l1l1ll1_opy_.append(bstack1l11l_opy_ (u"ࠧ࠮ࡰࠪྐྵ"))
            self.bstack111l1l1ll1_opy_.append(str(self.bstack1lll1111_opy_))
    def bstack111l1l11ll_opy_(self):
        bstack11ll11111_opy_ = []
        for spec in self.bstack1l1111ll1_opy_:
            bstack1lllll1l1_opy_ = [spec]
            bstack1lllll1l1_opy_ += self.bstack111l1l1ll1_opy_
            bstack11ll11111_opy_.append(bstack1lllll1l1_opy_)
        self.bstack11ll11111_opy_ = bstack11ll11111_opy_
        return bstack11ll11111_opy_
    def bstack1ll1l1ll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111l1l1lll_opy_ = True
            return True
        except Exception as e:
            self.bstack111l1l1lll_opy_ = False
        return self.bstack111l1l1lll_opy_
    def bstack1lll1111l1_opy_(self, bstack111l1lllll_opy_, bstack1ll11lll1l_opy_):
        bstack1ll11lll1l_opy_[bstack1l11l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨྺ")] = self.bstack111ll11111_opy_
        multiprocessing.set_start_method(bstack1l11l_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨྻ"))
        bstack11111l1l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll1lll111_opy_ = manager.list()
        if bstack1l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ྼ") in self.bstack111ll11111_opy_:
            for index, platform in enumerate(self.bstack111ll11111_opy_[bstack1l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ྽")]):
                bstack11111l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111l1lllll_opy_,
                                                            args=(self.bstack111l1l1ll1_opy_, bstack1ll11lll1l_opy_, bstack1ll1lll111_opy_)))
            bstack111l1l111l_opy_ = len(self.bstack111ll11111_opy_[bstack1l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ྾")])
        else:
            bstack11111l1l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111l1lllll_opy_,
                                                        args=(self.bstack111l1l1ll1_opy_, bstack1ll11lll1l_opy_, bstack1ll1lll111_opy_)))
            bstack111l1l111l_opy_ = 1
        i = 0
        for t in bstack11111l1l_opy_:
            os.environ[bstack1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭྿")] = str(i)
            if bstack1l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ࿀") in self.bstack111ll11111_opy_:
                os.environ[bstack1l11l_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ࿁")] = json.dumps(self.bstack111ll11111_opy_[bstack1l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ࿂")][i % bstack111l1l111l_opy_])
            i += 1
            t.start()
        for t in bstack11111l1l_opy_:
            t.join()
        return list(bstack1ll1lll111_opy_)
    @staticmethod
    def bstack1l1111111l_opy_(driver, bstack111l1l1111_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ࿃"), None)
        if item and getattr(item, bstack1l11l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭࿄"), None) and not getattr(item, bstack1l11l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧ࿅"), False):
            logger.info(
                bstack1l11l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲࿆ࠧ"))
            bstack111l1ll111_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11lll111l_opy_.bstack1l11l1l1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)