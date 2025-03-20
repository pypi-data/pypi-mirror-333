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
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1111l11ll1_opy_,
    bstack11111l1lll_opy_,
    bstack1111lllll1_opy_,
    bstack111l1111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llllll111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1lll1ll1111_opy_
from browserstack_sdk.sdk_cli.bstack1111l1l1ll_opy_ import bstack1111ll1111_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1lll1ll1l1l_opy_
import weakref
class bstack1ll1l111lll_opy_(bstack1lll1ll1l1l_opy_):
    bstack1ll1l111l11_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack111l1111ll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack111l1111ll_opy_]]
    def __init__(self, bstack1ll1l111l11_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll1l11ll1l_opy_ = dict()
        self.bstack1ll1l111l11_opy_ = bstack1ll1l111l11_opy_
        self.frameworks = frameworks
        bstack1lll1ll1111_opy_.bstack1ll1ll1l11l_opy_((bstack1111l11ll1_opy_.bstack1111ll11ll_opy_, bstack11111l1lll_opy_.POST), self.__1ll1l11llll_opy_)
        if any(bstack1llllll111l_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1llllll111l_opy_.bstack1ll1ll1l11l_opy_(
                (bstack1111l11ll1_opy_.bstack111l111l11_opy_, bstack11111l1lll_opy_.PRE), self.__1ll1l11ll11_opy_
            )
            bstack1llllll111l_opy_.bstack1ll1ll1l11l_opy_(
                (bstack1111l11ll1_opy_.QUIT, bstack11111l1lll_opy_.POST), self.__1ll1l1111ll_opy_
            )
    def __1ll1l11llll_opy_(
        self,
        f: bstack1lll1ll1111_opy_,
        bstack1ll1l11l111_opy_: object,
        exec: Tuple[bstack111l1111ll_opy_, str],
        bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l11l_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤᅝ"):
                return
            contexts = bstack1ll1l11l111_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l11l_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨᅞ") in page.url:
                                self.logger.debug(bstack1l11l_opy_ (u"ࠤࡖࡸࡴࡸࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦᅟ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1111lllll1_opy_.bstack1111l1ll1l_opy_(instance, self.bstack1ll1l111l11_opy_, True)
                                self.logger.debug(bstack1l11l_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡲࡤ࡫ࡪࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᅠ") + str(instance.ref()) + bstack1l11l_opy_ (u"ࠦࠧᅡ"))
        except Exception as e:
            self.logger.debug(bstack1l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠ࠻ࠤᅢ"),e)
    def __1ll1l11ll11_opy_(
        self,
        f: bstack1llllll111l_opy_,
        driver: object,
        exec: Tuple[bstack111l1111ll_opy_, str],
        bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1111lllll1_opy_.bstack1111ll111l_opy_(instance, self.bstack1ll1l111l11_opy_, False):
            return
        if not f.bstack1ll1l1l111l_opy_(f.hub_url(driver)):
            self.bstack1ll1l11ll1l_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1111lllll1_opy_.bstack1111l1ll1l_opy_(instance, self.bstack1ll1l111l11_opy_, True)
            self.logger.debug(bstack1l11l_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᅣ") + str(instance.ref()) + bstack1l11l_opy_ (u"ࠢࠣᅤ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1111lllll1_opy_.bstack1111l1ll1l_opy_(instance, self.bstack1ll1l111l11_opy_, True)
        self.logger.debug(bstack1l11l_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᅥ") + str(instance.ref()) + bstack1l11l_opy_ (u"ࠤࠥᅦ"))
    def __1ll1l1111ll_opy_(
        self,
        f: bstack1llllll111l_opy_,
        driver: object,
        exec: Tuple[bstack111l1111ll_opy_, str],
        bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll1l11l1l1_opy_(instance)
        self.logger.debug(bstack1l11l_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡵࡺ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᅧ") + str(instance.ref()) + bstack1l11l_opy_ (u"ࠦࠧᅨ"))
    def bstack1ll1l111ll1_opy_(self, context: bstack1111ll1111_opy_, reverse=True) -> List[Tuple[Callable, bstack111l1111ll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll1l11l1ll_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1llllll111l_opy_.bstack1lll11111ll_opy_(data[1])
                    and data[1].bstack1ll1l11l1ll_opy_(context)
                    and getattr(data[0](), bstack1l11l_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᅩ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1111l1lll1_opy_, reverse=reverse)
    def bstack1ll1l11lll1_opy_(self, context: bstack1111ll1111_opy_, reverse=True) -> List[Tuple[Callable, bstack111l1111ll_opy_]]:
        matches = []
        for data in self.bstack1ll1l11ll1l_opy_.values():
            if (
                data[1].bstack1ll1l11l1ll_opy_(context)
                and getattr(data[0](), bstack1l11l_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᅪ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1111l1lll1_opy_, reverse=reverse)
    def bstack1ll1l11l11l_opy_(self, instance: bstack111l1111ll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll1l11l1l1_opy_(self, instance: bstack111l1111ll_opy_) -> bool:
        if self.bstack1ll1l11l11l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1111lllll1_opy_.bstack1111l1ll1l_opy_(instance, self.bstack1ll1l111l11_opy_, False)
            return True
        return False