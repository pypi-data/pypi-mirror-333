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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll111lll_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1111llll1l_opy_ import (
    bstack11111ll11l_opy_,
    bstack11111l1lll_opy_,
    bstack1111lll11l_opy_,
)
from bstack_utils.helper import  bstack1llllll111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import bstack1llll11111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l11ll1_opy_, bstack1lllll1lll1_opy_, bstack111111l1ll_opy_, bstack1llll1l111l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l1l111111_opy_ import bstack11l1llllll_opy_
from browserstack_sdk.sdk_cli.bstack1111111l1l_opy_ import bstack111111llll_opy_
from bstack_utils.percy import bstack111ll1l1l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1llllll1ll1_opy_(bstack1lll11l1lll_opy_):
    def __init__(self, bstack1l1llllll1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1llllll1l_opy_ = bstack1l1llllll1l_opy_
        self.percy = bstack111ll1l1l_opy_()
        self.bstack1111111ll_opy_ = bstack11l1llllll_opy_()
        self.bstack1ll1111l111_opy_()
        bstack1llll11111l_opy_.bstack1ll1llllll1_opy_((bstack11111ll11l_opy_.bstack1111ll1l1l_opy_, bstack11111l1lll_opy_.PRE), self.bstack1ll11111l11_opy_)
        TestFramework.bstack1ll1llllll1_opy_((bstack1lll1l11ll1_opy_.TEST, bstack111111l1ll_opy_.POST), self.bstack1ll1lll11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll111lll11_opy_(self, instance: bstack1111lll11l_opy_, driver: object):
        bstack1ll1111lll1_opy_ = TestFramework.bstack11111ll111_opy_(instance.context)
        for t in bstack1ll1111lll1_opy_:
            bstack1ll11l11ll1_opy_ = TestFramework.bstack11111lll1l_opy_(t, bstack111111llll_opy_.bstack1ll11llllll_opy_, [])
            if any(instance is d[1] for d in bstack1ll11l11ll1_opy_) or instance == driver:
                return t
    def bstack1ll11111l11_opy_(
        self,
        f: bstack1llll11111l_opy_,
        driver: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1llll11111l_opy_.bstack1lll1111lll_opy_(method_name):
                return
            platform_index = f.bstack11111lll1l_opy_(instance, bstack1llll11111l_opy_.bstack1ll1llll111_opy_, 0)
            bstack1ll11l11l11_opy_ = self.bstack1ll111lll11_opy_(instance, driver)
            bstack1ll11111ll1_opy_ = TestFramework.bstack11111lll1l_opy_(bstack1ll11l11l11_opy_, TestFramework.bstack1l1lllllll1_opy_, None)
            if not bstack1ll11111ll1_opy_:
                self.logger.debug(bstack11_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡤࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩࡴࠢࡱࡳࡹࠦࡹࡦࡶࠣࡷࡹࡧࡲࡵࡧࡧࠦᇑ"))
                return
            driver_command = f.bstack1lll1111l11_opy_(*args)
            for command in bstack1lll1l11l_opy_:
                if command == driver_command:
                    self.bstack1ll1111l_opy_(driver, platform_index)
            bstack11llll1ll_opy_ = self.percy.bstack1l1lll11l_opy_()
            if driver_command in bstack1ll11llll1_opy_[bstack11llll1ll_opy_]:
                self.bstack1111111ll_opy_.bstack111ll1ll1_opy_(bstack1ll11111ll1_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡦࡴࡵࡳࡷࠨᇒ"), e)
    def bstack1ll1lll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1ll1111_opy_ import bstack11111111l1_opy_
        bstack1ll11l11ll1_opy_ = f.bstack11111lll1l_opy_(instance, bstack111111llll_opy_.bstack1ll11llllll_opy_, [])
        if not bstack1ll11l11ll1_opy_:
            self.logger.debug(bstack11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᇓ") + str(kwargs) + bstack11_opy_ (u"ࠢࠣᇔ"))
            return
        if len(bstack1ll11l11ll1_opy_) > 1:
            self.logger.debug(bstack11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᇕ") + str(kwargs) + bstack11_opy_ (u"ࠤࠥᇖ"))
        bstack1ll111111l1_opy_, bstack1l1llllllll_opy_ = bstack1ll11l11ll1_opy_[0]
        driver = bstack1ll111111l1_opy_()
        if not driver:
            self.logger.debug(bstack11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᇗ") + str(kwargs) + bstack11_opy_ (u"ࠦࠧᇘ"))
            return
        bstack1ll1111l11l_opy_ = {
            TestFramework.bstack1lll11111ll_opy_: bstack11_opy_ (u"ࠧࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣᇙ"),
            TestFramework.bstack1ll1ll1l111_opy_: bstack11_opy_ (u"ࠨࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤᇚ"),
            TestFramework.bstack1l1lllllll1_opy_: bstack11_opy_ (u"ࠢࡵࡧࡶࡸࠥࡸࡥࡳࡷࡱࠤࡳࡧ࡭ࡦࠤᇛ")
        }
        bstack1ll11111111_opy_ = { key: f.bstack11111lll1l_opy_(instance, key) for key in bstack1ll1111l11l_opy_ }
        bstack1ll11111l1l_opy_ = [key for key, value in bstack1ll11111111_opy_.items() if not value]
        if bstack1ll11111l1l_opy_:
            for key in bstack1ll11111l1l_opy_:
                self.logger.debug(bstack11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠦᇜ") + str(key) + bstack11_opy_ (u"ࠤࠥᇝ"))
            return
        platform_index = f.bstack11111lll1l_opy_(instance, bstack1llll11111l_opy_.bstack1ll1llll111_opy_, 0)
        if self.bstack1l1llllll1l_opy_.percy_capture_mode == bstack11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᇞ"):
            bstack1111l111l_opy_ = bstack1ll11111111_opy_.get(TestFramework.bstack1l1lllllll1_opy_) + bstack11_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᇟ")
            bstack1ll1l1llll1_opy_ = bstack11111111l1_opy_.bstack1ll1ll11111_opy_(EVENTS.bstack1ll1111111l_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1111l111l_opy_,
                bstack1l11111ll_opy_=bstack1ll11111111_opy_[TestFramework.bstack1lll11111ll_opy_],
                bstack1ll1111l11_opy_=bstack1ll11111111_opy_[TestFramework.bstack1ll1ll1l111_opy_],
                bstack1ll1ll1ll_opy_=platform_index
            )
            bstack11111111l1_opy_.end(EVENTS.bstack1ll1111111l_opy_.value, bstack1ll1l1llll1_opy_+bstack11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᇠ"), bstack1ll1l1llll1_opy_+bstack11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᇡ"), True, None, None, None, None, test_name=bstack1111l111l_opy_)
    def bstack1ll1111l_opy_(self, driver, platform_index):
        if self.bstack1111111ll_opy_.bstack1ll1l1l1ll_opy_() is True or self.bstack1111111ll_opy_.capturing() is True:
            return
        self.bstack1111111ll_opy_.bstack1llll11l_opy_()
        while not self.bstack1111111ll_opy_.bstack1ll1l1l1ll_opy_():
            bstack1ll11111ll1_opy_ = self.bstack1111111ll_opy_.bstack1lll111ll_opy_()
            self.bstack1111l1l1_opy_(driver, bstack1ll11111ll1_opy_, platform_index)
        self.bstack1111111ll_opy_.bstack11l1l111l_opy_()
    def bstack1111l1l1_opy_(self, driver, bstack11llll11l1_opy_, platform_index, test=None):
        from bstack_utils.bstack1l1ll1111_opy_ import bstack11111111l1_opy_
        bstack1ll1l1llll1_opy_ = bstack11111111l1_opy_.bstack1ll1ll11111_opy_(EVENTS.bstack11l1lll11_opy_.value)
        if test != None:
            bstack1l11111ll_opy_ = getattr(test, bstack11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᇢ"), None)
            bstack1ll1111l11_opy_ = getattr(test, bstack11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᇣ"), None)
            PercySDK.screenshot(driver, bstack11llll11l1_opy_, bstack1l11111ll_opy_=bstack1l11111ll_opy_, bstack1ll1111l11_opy_=bstack1ll1111l11_opy_, bstack1ll1ll1ll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11llll11l1_opy_)
        bstack11111111l1_opy_.end(EVENTS.bstack11l1lll11_opy_.value, bstack1ll1l1llll1_opy_+bstack11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᇤ"), bstack1ll1l1llll1_opy_+bstack11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᇥ"), True, None, None, None, None, test_name=bstack11llll11l1_opy_)
    def bstack1ll1111l111_opy_(self):
        os.environ[bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᇦ")] = str(self.bstack1l1llllll1l_opy_.success)
        os.environ[bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩᇧ")] = str(self.bstack1l1llllll1l_opy_.percy_capture_mode)
        self.percy.bstack1ll11111lll_opy_(self.bstack1l1llllll1l_opy_.is_percy_auto_enabled)
        self.percy.bstack1ll111111ll_opy_(self.bstack1l1llllll1l_opy_.percy_build_id)