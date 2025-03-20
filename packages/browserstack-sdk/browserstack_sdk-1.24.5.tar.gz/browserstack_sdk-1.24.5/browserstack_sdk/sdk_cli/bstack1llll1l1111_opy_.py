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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1111l1l1ll_opy_ import bstack1111l1l1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll11ll11l_opy_,
    bstack1lllll1lll1_opy_,
    bstack1llll11ll1l_opy_,
    bstack1l11lll1ll1_opy_,
    bstack1lllll11111_opy_,
)
import traceback
from bstack_utils.bstack1ll1l1lll1_opy_ import bstack1lll1ll1l11_opy_
from bstack_utils.constants import EVENTS
from bstack_utils.bstack11l11l1ll1_opy_ import bstack11l1llllll_opy_
class bstack1llll11ll11_opy_(TestFramework):
    bstack1l11lll1111_opy_ = bstack1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥ᎞")
    bstack1l11ll1ll1l_opy_ = bstack1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤ᎟")
    bstack1l1l1111l11_opy_ = bstack1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᎠ")
    bstack1l1l1l11ll1_opy_ = bstack1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᎡ")
    bstack1l11ll1lll1_opy_ = bstack1l11l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᎢ")
    bstack1l1l11l1ll1_opy_: bool
    bstack1l1l1l11l11_opy_ = [
        bstack1lll11ll11l_opy_.BEFORE_ALL,
        bstack1lll11ll11l_opy_.AFTER_ALL,
        bstack1lll11ll11l_opy_.BEFORE_EACH,
        bstack1lll11ll11l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1l11111l1_opy_: Dict[str, str],
        bstack1ll1ll1l1l1_opy_: List[str]=[bstack1l11l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᎣ")],
    ):
        super().__init__(bstack1ll1ll1l1l1_opy_, bstack1l1l11111l1_opy_)
        self.bstack1l1l11l1ll1_opy_ = any(bstack1l11l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᎤ") in item.lower() for item in bstack1ll1ll1l1l1_opy_)
    def track_event(
        self,
        context: bstack1l11lll1ll1_opy_,
        test_framework_state: bstack1lll11ll11l_opy_,
        test_hook_state: bstack1llll11ll1l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll11ll11l_opy_.NONE:
            self.logger.warning(bstack1l11l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᎥ") + str(test_hook_state) + bstack1l11l_opy_ (u"ࠦࠧᎦ"))
            return
        if not self.bstack1l1l11l1ll1_opy_:
            self.logger.warning(bstack1l11l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᎧ") + str(str(self.bstack1ll1ll1l1l1_opy_)) + bstack1l11l_opy_ (u"ࠨࠢᎨ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l11l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᎩ") + str(kwargs) + bstack1l11l_opy_ (u"ࠣࠤᎪ"))
            return
        instance = self.__1l1l11l1lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᎫ") + str(args) + bstack1l11l_opy_ (u"ࠥࠦᎬ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1llll11ll11_opy_.bstack1l1l1l11l11_opy_ and test_hook_state == bstack1llll11ll1l_opy_.PRE:
                bstack1ll1ll11111_opy_ = bstack1lll1ll1l11_opy_.bstack1lll111l1ll_opy_(EVENTS.bstack1lll1l1l_opy_.value)
                name = str(EVENTS.bstack1lll1l1l_opy_.name)+bstack1l11l_opy_ (u"ࠦ࠿ࠨᎭ")+str(test_framework_state.name)
                TestFramework.bstack1l1l111l111_opy_(instance, name, bstack1ll1ll11111_opy_)
        except Exception as e:
            self.logger.debug(bstack1l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᎮ").format(e))
        try:
            if not TestFramework.bstack111l111l1l_opy_(instance, TestFramework.bstack1l11lll1l11_opy_) and test_hook_state == bstack1llll11ll1l_opy_.PRE:
                test = bstack1llll11ll11_opy_.__1l1l111111l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l11l_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᎯ") + str(test_hook_state) + bstack1l11l_opy_ (u"ࠢࠣᎰ"))
            if test_framework_state == bstack1lll11ll11l_opy_.TEST:
                if test_hook_state == bstack1llll11ll1l_opy_.PRE and not TestFramework.bstack111l111l1l_opy_(instance, TestFramework.bstack1ll111l111l_opy_):
                    TestFramework.bstack1111l1ll1l_opy_(instance, TestFramework.bstack1ll111l111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11l_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᎱ") + str(test_hook_state) + bstack1l11l_opy_ (u"ࠤࠥᎲ"))
                elif test_hook_state == bstack1llll11ll1l_opy_.POST and not TestFramework.bstack111l111l1l_opy_(instance, TestFramework.bstack1ll111l1lll_opy_):
                    TestFramework.bstack1111l1ll1l_opy_(instance, TestFramework.bstack1ll111l1lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11l_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᎳ") + str(test_hook_state) + bstack1l11l_opy_ (u"ࠦࠧᎴ"))
            elif test_framework_state == bstack1lll11ll11l_opy_.LOG and test_hook_state == bstack1llll11ll1l_opy_.POST:
                bstack1llll11ll11_opy_.__1l1l11l11l1_opy_(instance, *args)
            elif test_framework_state == bstack1lll11ll11l_opy_.LOG_REPORT and test_hook_state == bstack1llll11ll1l_opy_.POST:
                self.__1l1l11ll1l1_opy_(instance, *args)
            elif test_framework_state in bstack1llll11ll11_opy_.bstack1l1l1l11l11_opy_:
                self.__1l11ll11ll1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l11l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᎵ") + str(instance.ref()) + bstack1l11l_opy_ (u"ࠨࠢᎶ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11lll11ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1llll11ll11_opy_.bstack1l1l1l11l11_opy_ and test_hook_state == bstack1llll11ll1l_opy_.POST:
                name = str(EVENTS.bstack1lll1l1l_opy_.name)+bstack1l11l_opy_ (u"ࠢ࠻ࠤᎷ")+str(test_framework_state.name)
                bstack1ll1ll11111_opy_ = TestFramework.bstack1l1l1l111l1_opy_(instance, name)
                bstack1lll1ll1l11_opy_.end(EVENTS.bstack1lll1l1l_opy_.value, bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᎸ"), bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᎹ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᎺ").format(e))
    def bstack1ll1111llll_opy_(self):
        return self.bstack1l1l11l1ll1_opy_
    def __1l11lllll11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l11l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᎻ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll11l1l1ll_opy_(rep, [bstack1l11l_opy_ (u"ࠧࡽࡨࡦࡰࠥᎼ"), bstack1l11l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᎽ"), bstack1l11l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᎾ"), bstack1l11l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᎿ"), bstack1l11l_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᏀ"), bstack1l11l_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᏁ")])
        return None
    def __1l1l11ll1l1_opy_(self, instance: bstack1lllll1lll1_opy_, *args):
        result = self.__1l11lllll11_opy_(*args)
        if not result:
            return
        failure = None
        bstack111l11ll11_opy_ = None
        if result.get(bstack1l11l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᏂ"), None) == bstack1l11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᏃ") and len(args) > 1 and getattr(args[1], bstack1l11l_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢᏄ"), None) is not None:
            failure = [{bstack1l11l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᏅ"): [args[1].excinfo.exconly(), result.get(bstack1l11l_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᏆ"), None)]}]
            bstack111l11ll11_opy_ = bstack1l11l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᏇ") if bstack1l11l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᏈ") in getattr(args[1].excinfo, bstack1l11l_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨᏉ"), bstack1l11l_opy_ (u"ࠧࠨᏊ")) else bstack1l11l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᏋ")
        bstack1l11lll1lll_opy_ = result.get(bstack1l11l_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᏌ"), TestFramework.bstack1l1l1111ll1_opy_)
        if bstack1l11lll1lll_opy_ != TestFramework.bstack1l1l1111ll1_opy_:
            TestFramework.bstack1111l1ll1l_opy_(instance, TestFramework.bstack1ll11l11l11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11ll11lll_opy_(instance, {
            TestFramework.bstack1l1ll1lll11_opy_: failure,
            TestFramework.bstack1l11llll1l1_opy_: bstack111l11ll11_opy_,
            TestFramework.bstack1l1lll1111l_opy_: bstack1l11lll1lll_opy_,
        })
    def __1l1l11l1lll_opy_(
        self,
        context: bstack1l11lll1ll1_opy_,
        test_framework_state: bstack1lll11ll11l_opy_,
        test_hook_state: bstack1llll11ll1l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll11ll11l_opy_.SETUP_FIXTURE:
            instance = self.__1l1l1l1111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11ll1l1ll_opy_ bstack1l11llll1ll_opy_ this to be bstack1l11l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᏍ")
            if test_framework_state == bstack1lll11ll11l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11lll1l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll11ll11l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l11l_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᏎ"), None), bstack1l11l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᏏ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l11l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᏐ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1111l1llll_opy_(target) if target else None
        return instance
    def __1l11ll11ll1_opy_(
        self,
        instance: bstack1lllll1lll1_opy_,
        test_framework_state: bstack1lll11ll11l_opy_,
        test_hook_state: bstack1llll11ll1l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11ll11111_opy_ = TestFramework.bstack1111ll111l_opy_(instance, bstack1llll11ll11_opy_.bstack1l11ll1ll1l_opy_, {})
        if not key in bstack1l11ll11111_opy_:
            bstack1l11ll11111_opy_[key] = []
        bstack1l1l11lllll_opy_ = TestFramework.bstack1111ll111l_opy_(instance, bstack1llll11ll11_opy_.bstack1l1l1111l11_opy_, {})
        if not key in bstack1l1l11lllll_opy_:
            bstack1l1l11lllll_opy_[key] = []
        bstack1l11ll1llll_opy_ = {
            bstack1llll11ll11_opy_.bstack1l11ll1ll1l_opy_: bstack1l11ll11111_opy_,
            bstack1llll11ll11_opy_.bstack1l1l1111l11_opy_: bstack1l1l11lllll_opy_,
        }
        if test_hook_state == bstack1llll11ll1l_opy_.PRE:
            hook = {
                bstack1l11l_opy_ (u"ࠧࡱࡥࡺࠤᏑ"): key,
                TestFramework.bstack1l1l11lll11_opy_: uuid4().__str__(),
                TestFramework.bstack1l1l111lll1_opy_: TestFramework.bstack1l11ll1l111_opy_,
                TestFramework.bstack1l1l111l1l1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1l1111lll_opy_: [],
                TestFramework.bstack1l1l111l1ll_opy_: args[1] if len(args) > 1 else bstack1l11l_opy_ (u"࠭ࠧᏒ")
            }
            bstack1l11ll11111_opy_[key].append(hook)
            bstack1l11ll1llll_opy_[bstack1llll11ll11_opy_.bstack1l1l1l11ll1_opy_] = key
        elif test_hook_state == bstack1llll11ll1l_opy_.POST:
            bstack1l11llll11l_opy_ = bstack1l11ll11111_opy_.get(key, [])
            hook = bstack1l11llll11l_opy_.pop() if bstack1l11llll11l_opy_ else None
            if hook:
                result = self.__1l11lllll11_opy_(*args)
                if result:
                    bstack1l1l11l1l11_opy_ = result.get(bstack1l11l_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᏓ"), TestFramework.bstack1l11ll1l111_opy_)
                    if bstack1l1l11l1l11_opy_ != TestFramework.bstack1l11ll1l111_opy_:
                        hook[TestFramework.bstack1l1l111lll1_opy_] = bstack1l1l11l1l11_opy_
                hook[TestFramework.bstack1l1l1l111ll_opy_] = datetime.now(tz=timezone.utc)
                bstack1l1l11lllll_opy_[key].append(hook)
                bstack1l11ll1llll_opy_[bstack1llll11ll11_opy_.bstack1l11ll1lll1_opy_] = key
        TestFramework.bstack1l11ll11lll_opy_(instance, bstack1l11ll1llll_opy_)
        self.logger.debug(bstack1l11l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢᏔ") + str(bstack1l1l11lllll_opy_) + bstack1l11l_opy_ (u"ࠤࠥᏕ"))
    def __1l1l1l1111l_opy_(
        self,
        context: bstack1l11lll1ll1_opy_,
        test_framework_state: bstack1lll11ll11l_opy_,
        test_hook_state: bstack1llll11ll1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll11l1l1ll_opy_(args[0], [bstack1l11l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᏖ"), bstack1l11l_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᏗ"), bstack1l11l_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᏘ"), bstack1l11l_opy_ (u"ࠨࡩࡥࡵࠥᏙ"), bstack1l11l_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᏚ"), bstack1l11l_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᏛ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l11l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᏜ")) else fixturedef.get(bstack1l11l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᏝ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l11l_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᏞ")) else None
        node = request.node if hasattr(request, bstack1l11l_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᏟ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l11l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᏠ")) else None
        baseid = fixturedef.get(bstack1l11l_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᏡ"), None) or bstack1l11l_opy_ (u"ࠣࠤᏢ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l11l_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢᏣ")):
            target = bstack1llll11ll11_opy_.__1l1l11l1l1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l11l_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᏤ")) else None
            if target and not TestFramework.bstack1111l1llll_opy_(target):
                self.__1l11lll1l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l11l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᏥ") + str(test_hook_state) + bstack1l11l_opy_ (u"ࠧࠨᏦ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l11l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᏧ") + str(target) + bstack1l11l_opy_ (u"ࠢࠣᏨ"))
            return None
        instance = TestFramework.bstack1111l1llll_opy_(target)
        if not instance:
            self.logger.warning(bstack1l11l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᏩ") + str(target) + bstack1l11l_opy_ (u"ࠤࠥᏪ"))
            return None
        bstack1l1l1111111_opy_ = TestFramework.bstack1111ll111l_opy_(instance, bstack1llll11ll11_opy_.bstack1l11lll1111_opy_, {})
        if os.getenv(bstack1l11l_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦᏫ"), bstack1l11l_opy_ (u"ࠦ࠶ࠨᏬ")) == bstack1l11l_opy_ (u"ࠧ࠷ࠢᏭ"):
            bstack1l1l11l1111_opy_ = bstack1l11l_opy_ (u"ࠨ࠺ࠣᏮ").join((scope, fixturename))
            bstack1l11ll1l11l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11lll11l1_opy_ = {
                bstack1l11l_opy_ (u"ࠢ࡬ࡧࡼࠦᏯ"): bstack1l1l11l1111_opy_,
                bstack1l11l_opy_ (u"ࠣࡶࡤ࡫ࡸࠨᏰ"): bstack1llll11ll11_opy_.__1l11ll111ll_opy_(request.node),
                bstack1l11l_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥᏱ"): fixturedef,
                bstack1l11l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᏲ"): scope,
                bstack1l11l_opy_ (u"ࠦࡹࡿࡰࡦࠤᏳ"): None,
            }
            try:
                if test_hook_state == bstack1llll11ll1l_opy_.POST and callable(getattr(args[-1], bstack1l11l_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᏴ"), None)):
                    bstack1l11lll11l1_opy_[bstack1l11l_opy_ (u"ࠨࡴࡺࡲࡨࠦᏵ")] = TestFramework.bstack1ll11ll1l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llll11ll1l_opy_.PRE:
                bstack1l11lll11l1_opy_[bstack1l11l_opy_ (u"ࠢࡶࡷ࡬ࡨࠧ᏶")] = uuid4().__str__()
                bstack1l11lll11l1_opy_[bstack1llll11ll11_opy_.bstack1l1l111l1l1_opy_] = bstack1l11ll1l11l_opy_
            elif test_hook_state == bstack1llll11ll1l_opy_.POST:
                bstack1l11lll11l1_opy_[bstack1llll11ll11_opy_.bstack1l1l1l111ll_opy_] = bstack1l11ll1l11l_opy_
            if bstack1l1l11l1111_opy_ in bstack1l1l1111111_opy_:
                bstack1l1l1111111_opy_[bstack1l1l11l1111_opy_].update(bstack1l11lll11l1_opy_)
                self.logger.debug(bstack1l11l_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤ᏷") + str(bstack1l1l1111111_opy_[bstack1l1l11l1111_opy_]) + bstack1l11l_opy_ (u"ࠤࠥᏸ"))
            else:
                bstack1l1l1111111_opy_[bstack1l1l11l1111_opy_] = bstack1l11lll11l1_opy_
                self.logger.debug(bstack1l11l_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨᏹ") + str(len(bstack1l1l1111111_opy_)) + bstack1l11l_opy_ (u"ࠦࠧᏺ"))
        TestFramework.bstack1111l1ll1l_opy_(instance, bstack1llll11ll11_opy_.bstack1l11lll1111_opy_, bstack1l1l1111111_opy_)
        self.logger.debug(bstack1l11l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᏻ") + str(instance.ref()) + bstack1l11l_opy_ (u"ࠨࠢᏼ"))
        return instance
    def __1l11lll1l1l_opy_(
        self,
        context: bstack1l11lll1ll1_opy_,
        test_framework_state: bstack1lll11ll11l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1111l1l1l1_opy_.create_context(target)
        ob = bstack1lllll1lll1_opy_(ctx, self.bstack1ll1ll1l1l1_opy_, self.bstack1l1l11111l1_opy_, test_framework_state)
        TestFramework.bstack1l11ll11lll_opy_(ob, {
            TestFramework.bstack1ll1llll1l1_opy_: context.test_framework_name,
            TestFramework.bstack1ll111lll11_opy_: context.test_framework_version,
            TestFramework.bstack1l11llll111_opy_: [],
            bstack1llll11ll11_opy_.bstack1l11lll1111_opy_: {},
            bstack1llll11ll11_opy_.bstack1l1l1111l11_opy_: {},
            bstack1llll11ll11_opy_.bstack1l11ll1ll1l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111l1ll1l_opy_(ob, TestFramework.bstack1l11ll1l1l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111l1ll1l_opy_(ob, TestFramework.bstack1ll1ll1llll_opy_, context.platform_index)
        TestFramework.bstack11111ll1l1_opy_[ctx.id] = ob
        self.logger.debug(bstack1l11l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᏽ") + str(TestFramework.bstack11111ll1l1_opy_.keys()) + bstack1l11l_opy_ (u"ࠣࠤ᏾"))
        return ob
    def bstack1ll111ll1l1_opy_(self, instance: bstack1lllll1lll1_opy_, bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_]):
        bstack1l11llllll1_opy_ = (
            bstack1llll11ll11_opy_.bstack1l1l1l11ll1_opy_
            if bstack11111lll1l_opy_[1] == bstack1llll11ll1l_opy_.PRE
            else bstack1llll11ll11_opy_.bstack1l11ll1lll1_opy_
        )
        hook = bstack1llll11ll11_opy_.bstack1l1l11llll1_opy_(instance, bstack1l11llllll1_opy_)
        entries = hook.get(TestFramework.bstack1l1l1111lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1l11llll111_opy_, []))
        return entries
    def bstack1ll1111lll1_opy_(self, instance: bstack1lllll1lll1_opy_, bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_]):
        bstack1l11llllll1_opy_ = (
            bstack1llll11ll11_opy_.bstack1l1l1l11ll1_opy_
            if bstack11111lll1l_opy_[1] == bstack1llll11ll1l_opy_.PRE
            else bstack1llll11ll11_opy_.bstack1l11ll1lll1_opy_
        )
        bstack1llll11ll11_opy_.bstack1l1l11ll1ll_opy_(instance, bstack1l11llllll1_opy_)
        TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1l11llll111_opy_, []).clear()
    @staticmethod
    def bstack1l1l11llll1_opy_(instance: bstack1lllll1lll1_opy_, bstack1l11llllll1_opy_: str):
        bstack1l1l111ll11_opy_ = (
            bstack1llll11ll11_opy_.bstack1l1l1111l11_opy_
            if bstack1l11llllll1_opy_ == bstack1llll11ll11_opy_.bstack1l11ll1lll1_opy_
            else bstack1llll11ll11_opy_.bstack1l11ll1ll1l_opy_
        )
        bstack1l1l111llll_opy_ = TestFramework.bstack1111ll111l_opy_(instance, bstack1l11llllll1_opy_, None)
        bstack1l1l111ll1l_opy_ = TestFramework.bstack1111ll111l_opy_(instance, bstack1l1l111ll11_opy_, None) if bstack1l1l111llll_opy_ else None
        return (
            bstack1l1l111ll1l_opy_[bstack1l1l111llll_opy_][-1]
            if isinstance(bstack1l1l111ll1l_opy_, dict) and len(bstack1l1l111ll1l_opy_.get(bstack1l1l111llll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l1l11ll1ll_opy_(instance: bstack1lllll1lll1_opy_, bstack1l11llllll1_opy_: str):
        hook = bstack1llll11ll11_opy_.bstack1l1l11llll1_opy_(instance, bstack1l11llllll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1l1111lll_opy_, []).clear()
    @staticmethod
    def __1l1l11l11l1_opy_(instance: bstack1lllll1lll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l11l_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢ᏿"), None)):
            return
        if os.getenv(bstack1l11l_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢ᐀"), bstack1l11l_opy_ (u"ࠦ࠶ࠨᐁ")) != bstack1l11l_opy_ (u"ࠧ࠷ࠢᐂ"):
            bstack1llll11ll11_opy_.logger.warning(bstack1l11l_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᐃ"))
            return
        bstack1l11lllllll_opy_ = {
            bstack1l11l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᐄ"): (bstack1llll11ll11_opy_.bstack1l1l1l11ll1_opy_, bstack1llll11ll11_opy_.bstack1l11ll1ll1l_opy_),
            bstack1l11l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᐅ"): (bstack1llll11ll11_opy_.bstack1l11ll1lll1_opy_, bstack1llll11ll11_opy_.bstack1l1l1111l11_opy_),
        }
        for when in (bstack1l11l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᐆ"), bstack1l11l_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᐇ"), bstack1l11l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᐈ")):
            bstack1l11ll11l11_opy_ = args[1].get_records(when)
            if not bstack1l11ll11l11_opy_:
                continue
            records = [
                bstack1lllll11111_opy_(
                    kind=TestFramework.bstack1ll1l11111l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l11l_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᐉ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l11l_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᐊ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll11l11_opy_
                if isinstance(getattr(r, bstack1l11l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᐋ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l1l11lll1l_opy_, bstack1l1l111ll11_opy_ = bstack1l11lllllll_opy_.get(when, (None, None))
            bstack1l11ll1ll11_opy_ = TestFramework.bstack1111ll111l_opy_(instance, bstack1l1l11lll1l_opy_, None) if bstack1l1l11lll1l_opy_ else None
            bstack1l1l111ll1l_opy_ = TestFramework.bstack1111ll111l_opy_(instance, bstack1l1l111ll11_opy_, None) if bstack1l11ll1ll11_opy_ else None
            if isinstance(bstack1l1l111ll1l_opy_, dict) and len(bstack1l1l111ll1l_opy_.get(bstack1l11ll1ll11_opy_, [])) > 0:
                hook = bstack1l1l111ll1l_opy_[bstack1l11ll1ll11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1l1111lll_opy_ in hook:
                    hook[TestFramework.bstack1l1l1111lll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1l11llll111_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l1l111111l_opy_(test) -> Dict[str, Any]:
        bstack1lll1l11_opy_ = bstack1llll11ll11_opy_.__1l1l11l1l1l_opy_(test.location) if hasattr(test, bstack1l11l_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᐌ")) else getattr(test, bstack1l11l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᐍ"), None)
        test_name = test.name if hasattr(test, bstack1l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᐎ")) else None
        bstack1l11lll111l_opy_ = test.fspath.strpath if hasattr(test, bstack1l11l_opy_ (u"ࠦ࡫ࡹࡰࡢࡶ࡫ࠦᐏ")) and test.fspath else None
        if not bstack1lll1l11_opy_ or not test_name or not bstack1l11lll111l_opy_:
            return None
        code = None
        if hasattr(test, bstack1l11l_opy_ (u"ࠧࡵࡢ࡫ࠤᐐ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l11l1lllll_opy_ = []
        try:
            bstack1l11l1lllll_opy_ = bstack11l1llllll_opy_.bstack11l111l111_opy_(test)
        except:
            bstack1llll11ll11_opy_.logger.warning(bstack1l11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷ࠱ࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡥࡴࡱ࡯ࡺࡪࡪࠠࡪࡰࠣࡇࡑࡏࠢᐑ"))
        return {
            TestFramework.bstack1ll1l1lll1l_opy_: uuid4().__str__(),
            TestFramework.bstack1l11lll1l11_opy_: bstack1lll1l11_opy_,
            TestFramework.bstack1lll111ll11_opy_: test_name,
            TestFramework.bstack1ll1111l111_opy_: getattr(test, bstack1l11l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᐒ"), None),
            TestFramework.bstack1l1l111l11l_opy_: bstack1l11lll111l_opy_,
            TestFramework.bstack1l1l11111ll_opy_: bstack1llll11ll11_opy_.__1l11ll111ll_opy_(test),
            TestFramework.bstack1l1l11ll111_opy_: code,
            TestFramework.bstack1l1lll1111l_opy_: TestFramework.bstack1l1l1111ll1_opy_,
            TestFramework.bstack1l1l1lll11l_opy_: bstack1lll1l11_opy_,
            TestFramework.bstack1l11l1llll1_opy_: bstack1l11l1lllll_opy_
        }
    @staticmethod
    def __1l11ll111ll_opy_(test) -> List[str]:
        return (
            [getattr(f, bstack1l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᐓ"), None) for f in test.own_markers if getattr(f, bstack1l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᐔ"), None)]
            if isinstance(getattr(test, bstack1l11l_opy_ (u"ࠥࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠣᐕ"), None), list)
            else []
        )
    @staticmethod
    def __1l1l11l1l1l_opy_(location):
        return bstack1l11l_opy_ (u"ࠦ࠿ࡀࠢᐖ").join(filter(lambda x: isinstance(x, str), location))