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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1111lllll1_opy_,
    bstack111l1111ll_opy_,
    bstack1111l11ll1_opy_,
    bstack11111l1lll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lll1ll1111_opy_(bstack1111lllll1_opy_):
    bstack1l1l1l1l111_opy_ = bstack1l11l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤዮ")
    bstack1l1llll1l1l_opy_ = bstack1l11l_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥዯ")
    bstack1l1llll111l_opy_ = bstack1l11l_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࠧደ")
    bstack1l1llll1ll1_opy_ = bstack1l11l_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዱ")
    bstack1l1l1l1l1ll_opy_ = bstack1l11l_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤዲ")
    bstack1l1l1l1lll1_opy_ = bstack1l11l_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣዳ")
    NAME = bstack1l11l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧዴ")
    bstack1l1l1l1l11l_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack111111ll11_opy_: Any
    bstack1l1l1l11lll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l11l_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤድ"), bstack1l11l_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦዶ"), bstack1l11l_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨዷ"), bstack1l11l_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦዸ"), bstack1l11l_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣዹ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack11111ll11l_opy_(methods)
    def bstack1111lll111_opy_(self, instance: bstack111l1111ll_opy_, method_name: str, bstack1111l111ll_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1111ll1lll_opy_(
        self,
        target: object,
        exec: Tuple[bstack111l1111ll_opy_, str],
        bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111lll11l_opy_, bstack1l1l1ll1111_opy_ = bstack11111lll1l_opy_
        bstack1l1l1l1l1l1_opy_ = bstack1lll1ll1111_opy_.bstack1l1l1l1ll1l_opy_(bstack11111lll1l_opy_)
        if bstack1l1l1l1l1l1_opy_ in bstack1lll1ll1111_opy_.bstack1l1l1l1l11l_opy_:
            bstack1l1l1l1ll11_opy_ = None
            for callback in bstack1lll1ll1111_opy_.bstack1l1l1l1l11l_opy_[bstack1l1l1l1l1l1_opy_]:
                try:
                    bstack1l1l1l1llll_opy_ = callback(self, target, exec, bstack11111lll1l_opy_, result, *args, **kwargs)
                    if bstack1l1l1l1ll11_opy_ == None:
                        bstack1l1l1l1ll11_opy_ = bstack1l1l1l1llll_opy_
                except Exception as e:
                    self.logger.error(bstack1l11l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧዺ") + str(e) + bstack1l11l_opy_ (u"ࠣࠤዻ"))
                    traceback.print_exc()
            if bstack1l1l1ll1111_opy_ == bstack11111l1lll_opy_.PRE and callable(bstack1l1l1l1ll11_opy_):
                return bstack1l1l1l1ll11_opy_
            elif bstack1l1l1ll1111_opy_ == bstack11111l1lll_opy_.POST and bstack1l1l1l1ll11_opy_:
                return bstack1l1l1l1ll11_opy_
    def bstack1111l1l111_opy_(
        self, method_name, previous_state: bstack1111l11ll1_opy_, *args, **kwargs
    ) -> bstack1111l11ll1_opy_:
        if method_name == bstack1l11l_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩዼ") or method_name == bstack1l11l_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫዽ") or method_name == bstack1l11l_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭ዾ"):
            return bstack1111l11ll1_opy_.bstack1111ll11ll_opy_
        if method_name == bstack1l11l_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧዿ"):
            return bstack1111l11ll1_opy_.bstack111l111111_opy_
        if method_name == bstack1l11l_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬጀ"):
            return bstack1111l11ll1_opy_.QUIT
        return bstack1111l11ll1_opy_.NONE
    @staticmethod
    def bstack1l1l1l1ll1l_opy_(bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_]):
        return bstack1l11l_opy_ (u"ࠢ࠻ࠤጁ").join((bstack1111l11ll1_opy_(bstack11111lll1l_opy_[0]).name, bstack11111l1lll_opy_(bstack11111lll1l_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll1l11l_opy_(bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_], callback: Callable):
        bstack1l1l1l1l1l1_opy_ = bstack1lll1ll1111_opy_.bstack1l1l1l1ll1l_opy_(bstack11111lll1l_opy_)
        if not bstack1l1l1l1l1l1_opy_ in bstack1lll1ll1111_opy_.bstack1l1l1l1l11l_opy_:
            bstack1lll1ll1111_opy_.bstack1l1l1l1l11l_opy_[bstack1l1l1l1l1l1_opy_] = []
        bstack1lll1ll1111_opy_.bstack1l1l1l1l11l_opy_[bstack1l1l1l1l1l1_opy_].append(callback)
    @staticmethod
    def bstack1ll1llll111_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1lll1111l1l_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1lll11111l1_opy_(instance: bstack111l1111ll_opy_, default_value=None):
        return bstack1111lllll1_opy_.bstack1111ll111l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1llll1ll1_opy_, default_value)
    @staticmethod
    def bstack1lll11111ll_opy_(instance: bstack111l1111ll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1lll1111l11_opy_(instance: bstack111l1111ll_opy_, default_value=None):
        return bstack1111lllll1_opy_.bstack1111ll111l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l1llll111l_opy_, default_value)
    @staticmethod
    def bstack1ll1lll1lll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l1lllll_opy_(method_name: str, *args):
        if not bstack1lll1ll1111_opy_.bstack1ll1llll111_opy_(method_name):
            return False
        if not bstack1lll1ll1111_opy_.bstack1l1l1l1l1ll_opy_ in bstack1lll1ll1111_opy_.bstack1l1ll11llll_opy_(*args):
            return False
        bstack1ll1l1l1l1l_opy_ = bstack1lll1ll1111_opy_.bstack1ll1l1l1ll1_opy_(*args)
        return bstack1ll1l1l1l1l_opy_ and bstack1l11l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣጂ") in bstack1ll1l1l1l1l_opy_ and bstack1l11l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥጃ") in bstack1ll1l1l1l1l_opy_[bstack1l11l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥጄ")]
    @staticmethod
    def bstack1ll1ll11l1l_opy_(method_name: str, *args):
        if not bstack1lll1ll1111_opy_.bstack1ll1llll111_opy_(method_name):
            return False
        if not bstack1lll1ll1111_opy_.bstack1l1l1l1l1ll_opy_ in bstack1lll1ll1111_opy_.bstack1l1ll11llll_opy_(*args):
            return False
        bstack1ll1l1l1l1l_opy_ = bstack1lll1ll1111_opy_.bstack1ll1l1l1ll1_opy_(*args)
        return (
            bstack1ll1l1l1l1l_opy_
            and bstack1l11l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦጅ") in bstack1ll1l1l1l1l_opy_
            and bstack1l11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣጆ") in bstack1ll1l1l1l1l_opy_[bstack1l11l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨጇ")]
        )
    @staticmethod
    def bstack1l1ll11llll_opy_(*args):
        return str(bstack1lll1ll1111_opy_.bstack1ll1lll1lll_opy_(*args)).lower()