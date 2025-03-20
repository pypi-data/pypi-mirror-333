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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111llll1l_opy_ import (
    bstack11111lll11_opy_,
    bstack1111lll11l_opy_,
    bstack11111ll11l_opy_,
    bstack11111l1lll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack111111l11l_opy_(bstack11111lll11_opy_):
    bstack1l1l1l1ll11_opy_ = bstack11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥዯ")
    bstack1l1lll1l1ll_opy_ = bstack11_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦደ")
    bstack1l1llll1ll1_opy_ = bstack11_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨዱ")
    bstack1l1llll11ll_opy_ = bstack11_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧዲ")
    bstack1l1l1ll1111_opy_ = bstack11_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥዳ")
    bstack1l1l1l1l1l1_opy_ = bstack11_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤዴ")
    NAME = bstack11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨድ")
    bstack1l1l1l1l1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lllll11lll_opy_: Any
    bstack1l1l1l1lll1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥዶ"), bstack11_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧዷ"), bstack11_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢዸ"), bstack11_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧዹ"), bstack11_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤዺ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1111l11ll1_opy_(methods)
    def bstack1111l1ll11_opy_(self, instance: bstack1111lll11l_opy_, method_name: str, bstack1111l1l1l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1111l1ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111l11111_opy_, bstack1l1l1l1llll_opy_ = bstack1111l11l11_opy_
        bstack1l1l1l1ll1l_opy_ = bstack111111l11l_opy_.bstack1l1l1l1l11l_opy_(bstack1111l11l11_opy_)
        if bstack1l1l1l1ll1l_opy_ in bstack111111l11l_opy_.bstack1l1l1l1l1ll_opy_:
            bstack1l1l1l1l111_opy_ = None
            for callback in bstack111111l11l_opy_.bstack1l1l1l1l1ll_opy_[bstack1l1l1l1ll1l_opy_]:
                try:
                    bstack1l1l1l11lll_opy_ = callback(self, target, exec, bstack1111l11l11_opy_, result, *args, **kwargs)
                    if bstack1l1l1l1l111_opy_ == None:
                        bstack1l1l1l1l111_opy_ = bstack1l1l1l11lll_opy_
                except Exception as e:
                    self.logger.error(bstack11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨዻ") + str(e) + bstack11_opy_ (u"ࠤࠥዼ"))
                    traceback.print_exc()
            if bstack1l1l1l1llll_opy_ == bstack11111l1lll_opy_.PRE and callable(bstack1l1l1l1l111_opy_):
                return bstack1l1l1l1l111_opy_
            elif bstack1l1l1l1llll_opy_ == bstack11111l1lll_opy_.POST and bstack1l1l1l1l111_opy_:
                return bstack1l1l1l1l111_opy_
    def bstack1111lll111_opy_(
        self, method_name, previous_state: bstack11111ll11l_opy_, *args, **kwargs
    ) -> bstack11111ll11l_opy_:
        if method_name == bstack11_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࠪዽ") or method_name == bstack11_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬዾ") or method_name == bstack11_opy_ (u"ࠬࡴࡥࡸࡡࡳࡥ࡬࡫ࠧዿ"):
            return bstack11111ll11l_opy_.bstack1111ll1ll1_opy_
        if method_name == bstack11_opy_ (u"࠭ࡤࡪࡵࡳࡥࡹࡩࡨࠨጀ"):
            return bstack11111ll11l_opy_.bstack111l111111_opy_
        if method_name == bstack11_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭ጁ"):
            return bstack11111ll11l_opy_.QUIT
        return bstack11111ll11l_opy_.NONE
    @staticmethod
    def bstack1l1l1l1l11l_opy_(bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_]):
        return bstack11_opy_ (u"ࠣ࠼ࠥጂ").join((bstack11111ll11l_opy_(bstack1111l11l11_opy_[0]).name, bstack11111l1lll_opy_(bstack1111l11l11_opy_[1]).name))
    @staticmethod
    def bstack1ll1llllll1_opy_(bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_], callback: Callable):
        bstack1l1l1l1ll1l_opy_ = bstack111111l11l_opy_.bstack1l1l1l1l11l_opy_(bstack1111l11l11_opy_)
        if not bstack1l1l1l1ll1l_opy_ in bstack111111l11l_opy_.bstack1l1l1l1l1ll_opy_:
            bstack111111l11l_opy_.bstack1l1l1l1l1ll_opy_[bstack1l1l1l1ll1l_opy_] = []
        bstack111111l11l_opy_.bstack1l1l1l1l1ll_opy_[bstack1l1l1l1ll1l_opy_].append(callback)
    @staticmethod
    def bstack1lll1111lll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1lll111ll11_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1llll11l_opy_(instance: bstack1111lll11l_opy_, default_value=None):
        return bstack11111lll11_opy_.bstack11111lll1l_opy_(instance, bstack111111l11l_opy_.bstack1l1llll11ll_opy_, default_value)
    @staticmethod
    def bstack1ll1ll1l1ll_opy_(instance: bstack1111lll11l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1lllll11_opy_(instance: bstack1111lll11l_opy_, default_value=None):
        return bstack11111lll11_opy_.bstack11111lll1l_opy_(instance, bstack111111l11l_opy_.bstack1l1llll1ll1_opy_, default_value)
    @staticmethod
    def bstack1lll1111l11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1ll111l1_opy_(method_name: str, *args):
        if not bstack111111l11l_opy_.bstack1lll1111lll_opy_(method_name):
            return False
        if not bstack111111l11l_opy_.bstack1l1l1ll1111_opy_ in bstack111111l11l_opy_.bstack1l1ll11ll1l_opy_(*args):
            return False
        bstack1ll1l1ll111_opy_ = bstack111111l11l_opy_.bstack1ll1l1l1lll_opy_(*args)
        return bstack1ll1l1ll111_opy_ and bstack11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤጃ") in bstack1ll1l1ll111_opy_ and bstack11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦጄ") in bstack1ll1l1ll111_opy_[bstack11_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦጅ")]
    @staticmethod
    def bstack1lll111111l_opy_(method_name: str, *args):
        if not bstack111111l11l_opy_.bstack1lll1111lll_opy_(method_name):
            return False
        if not bstack111111l11l_opy_.bstack1l1l1ll1111_opy_ in bstack111111l11l_opy_.bstack1l1ll11ll1l_opy_(*args):
            return False
        bstack1ll1l1ll111_opy_ = bstack111111l11l_opy_.bstack1ll1l1l1lll_opy_(*args)
        return (
            bstack1ll1l1ll111_opy_
            and bstack11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧጆ") in bstack1ll1l1ll111_opy_
            and bstack11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤጇ") in bstack1ll1l1ll111_opy_[bstack11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢገ")]
        )
    @staticmethod
    def bstack1l1ll11ll1l_opy_(*args):
        return str(bstack111111l11l_opy_.bstack1lll1111l11_opy_(*args)).lower()