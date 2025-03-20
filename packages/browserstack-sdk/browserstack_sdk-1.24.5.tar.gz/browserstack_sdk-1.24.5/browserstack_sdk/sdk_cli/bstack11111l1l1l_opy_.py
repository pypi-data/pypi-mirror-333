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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1111l11ll1_opy_,
    bstack11111l1lll_opy_,
    bstack111l1111ll_opy_,
)
from bstack_utils.helper import  bstack1llll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llllll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11ll11l_opy_, bstack1lllll1lll1_opy_, bstack1llll11ll1l_opy_, bstack1lllll11111_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11ll11111l_opy_ import bstack1l11111lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l111_opy_ import bstack1llll11l1l1_opy_
from bstack_utils.percy import bstack1lll111lll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll11llll1_opy_(bstack1lll1ll1l1l_opy_):
    def __init__(self, bstack1ll11111l1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1ll11111l1l_opy_ = bstack1ll11111l1l_opy_
        self.percy = bstack1lll111lll_opy_()
        self.bstack11l1lll11_opy_ = bstack1l11111lll_opy_()
        self.bstack1ll11111l11_opy_()
        bstack1llllll111l_opy_.bstack1ll1ll1l11l_opy_((bstack1111l11ll1_opy_.bstack111l111l11_opy_, bstack11111l1lll_opy_.PRE), self.bstack1l1llllll1l_opy_)
        TestFramework.bstack1ll1ll1l11l_opy_((bstack1lll11ll11l_opy_.TEST, bstack1llll11ll1l_opy_.POST), self.bstack1lll111l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11ll1l1l_opy_(self, instance: bstack111l1111ll_opy_, driver: object):
        bstack1ll11l1l1l1_opy_ = TestFramework.bstack11111lllll_opy_(instance.context)
        for t in bstack1ll11l1l1l1_opy_:
            bstack1ll111llll1_opy_ = TestFramework.bstack1111ll111l_opy_(t, bstack1llll11l1l1_opy_.bstack1ll11l111ll_opy_, [])
            if any(instance is d[1] for d in bstack1ll111llll1_opy_) or instance == driver:
                return t
    def bstack1l1llllll1l_opy_(
        self,
        f: bstack1llllll111l_opy_,
        driver: object,
        exec: Tuple[bstack111l1111ll_opy_, str],
        bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1llllll111l_opy_.bstack1ll1llll111_opy_(method_name):
                return
            platform_index = f.bstack1111ll111l_opy_(instance, bstack1llllll111l_opy_.bstack1ll1ll1llll_opy_, 0)
            bstack1ll11l1lll1_opy_ = self.bstack1ll11ll1l1l_opy_(instance, driver)
            bstack1ll1111111l_opy_ = TestFramework.bstack1111ll111l_opy_(bstack1ll11l1lll1_opy_, TestFramework.bstack1ll1111l111_opy_, None)
            if not bstack1ll1111111l_opy_:
                self.logger.debug(bstack1l11l_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥᇐ"))
                return
            driver_command = f.bstack1ll1lll1lll_opy_(*args)
            for command in bstack1111l1l1_opy_:
                if command == driver_command:
                    self.bstack1111ll1l1_opy_(driver, platform_index)
            bstack11llll1ll1_opy_ = self.percy.bstack1lllll1111_opy_()
            if driver_command in bstack1ll11ll1l_opy_[bstack11llll1ll1_opy_]:
                self.bstack11l1lll11_opy_.bstack1l1llll1ll_opy_(bstack1ll1111111l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l11l_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧᇑ"), e)
    def bstack1lll111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll1l1lll1_opy_ import bstack1lll1ll1l11_opy_
        bstack1ll111llll1_opy_ = f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll11l111ll_opy_, [])
        if not bstack1ll111llll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᇒ") + str(kwargs) + bstack1l11l_opy_ (u"ࠨࠢᇓ"))
            return
        if len(bstack1ll111llll1_opy_) > 1:
            self.logger.debug(bstack1l11l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᇔ") + str(kwargs) + bstack1l11l_opy_ (u"ࠣࠤᇕ"))
        bstack1ll1111l11l_opy_, bstack1ll111111l1_opy_ = bstack1ll111llll1_opy_[0]
        driver = bstack1ll1111l11l_opy_()
        if not driver:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᇖ") + str(kwargs) + bstack1l11l_opy_ (u"ࠥࠦᇗ"))
            return
        bstack1ll11111lll_opy_ = {
            TestFramework.bstack1lll111ll11_opy_: bstack1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᇘ"),
            TestFramework.bstack1ll1l1lll1l_opy_: bstack1l11l_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣᇙ"),
            TestFramework.bstack1ll1111l111_opy_: bstack1l11l_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣᇚ")
        }
        bstack1ll11111ll1_opy_ = { key: f.bstack1111ll111l_opy_(instance, key) for key in bstack1ll11111lll_opy_ }
        bstack1ll11111111_opy_ = [key for key, value in bstack1ll11111ll1_opy_.items() if not value]
        if bstack1ll11111111_opy_:
            for key in bstack1ll11111111_opy_:
                self.logger.debug(bstack1l11l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥᇛ") + str(key) + bstack1l11l_opy_ (u"ࠣࠤᇜ"))
            return
        platform_index = f.bstack1111ll111l_opy_(instance, bstack1llllll111l_opy_.bstack1ll1ll1llll_opy_, 0)
        if self.bstack1ll11111l1l_opy_.percy_capture_mode == bstack1l11l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᇝ"):
            bstack11lll1111_opy_ = bstack1ll11111ll1_opy_.get(TestFramework.bstack1ll1111l111_opy_) + bstack1l11l_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᇞ")
            bstack1ll1ll11111_opy_ = bstack1lll1ll1l11_opy_.bstack1lll111l1ll_opy_(EVENTS.bstack1ll111111ll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11lll1111_opy_,
                bstack11llll11l1_opy_=bstack1ll11111ll1_opy_[TestFramework.bstack1lll111ll11_opy_],
                bstack1lll11l111_opy_=bstack1ll11111ll1_opy_[TestFramework.bstack1ll1l1lll1l_opy_],
                bstack1l1111ll11_opy_=platform_index
            )
            bstack1lll1ll1l11_opy_.end(EVENTS.bstack1ll111111ll_opy_.value, bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᇟ"), bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᇠ"), True, None, None, None, None, test_name=bstack11lll1111_opy_)
    def bstack1111ll1l1_opy_(self, driver, platform_index):
        if self.bstack11l1lll11_opy_.bstack11ll11lll1_opy_() is True or self.bstack11l1lll11_opy_.capturing() is True:
            return
        self.bstack11l1lll11_opy_.bstack1l1lll1l_opy_()
        while not self.bstack11l1lll11_opy_.bstack11ll11lll1_opy_():
            bstack1ll1111111l_opy_ = self.bstack11l1lll11_opy_.bstack11lll1lll_opy_()
            self.bstack11l1l11l_opy_(driver, bstack1ll1111111l_opy_, platform_index)
        self.bstack11l1lll11_opy_.bstack1l1ll1111_opy_()
    def bstack11l1l11l_opy_(self, driver, bstack1l1111111_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll1l1lll1_opy_ import bstack1lll1ll1l11_opy_
        bstack1ll1ll11111_opy_ = bstack1lll1ll1l11_opy_.bstack1lll111l1ll_opy_(EVENTS.bstack11ll1l11_opy_.value)
        if test != None:
            bstack11llll11l1_opy_ = getattr(test, bstack1l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᇡ"), None)
            bstack1lll11l111_opy_ = getattr(test, bstack1l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᇢ"), None)
            PercySDK.screenshot(driver, bstack1l1111111_opy_, bstack11llll11l1_opy_=bstack11llll11l1_opy_, bstack1lll11l111_opy_=bstack1lll11l111_opy_, bstack1l1111ll11_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l1111111_opy_)
        bstack1lll1ll1l11_opy_.end(EVENTS.bstack11ll1l11_opy_.value, bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᇣ"), bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᇤ"), True, None, None, None, None, test_name=bstack1l1111111_opy_)
    def bstack1ll11111l11_opy_(self):
        os.environ[bstack1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᇥ")] = str(self.bstack1ll11111l1l_opy_.success)
        os.environ[bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᇦ")] = str(self.bstack1ll11111l1l_opy_.percy_capture_mode)
        self.percy.bstack1l1llllllll_opy_(self.bstack1ll11111l1l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1lllllll1_opy_(self.bstack1ll11111l1l_opy_.percy_build_id)