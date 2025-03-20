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
from pyexpat import features
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
class PytestBDDFramework(TestFramework):
    bstack1l11lll1111_opy_ = bstack1l11l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢገ")
    bstack1l11ll1ll1l_opy_ = bstack1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨጉ")
    bstack1l1l1111l11_opy_ = bstack1l11l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣጊ")
    bstack1l1l1l11ll1_opy_ = bstack1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧጋ")
    bstack1l11ll1lll1_opy_ = bstack1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢጌ")
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
        bstack1ll1ll1l1l1_opy_: List[str]=[bstack1l11l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤግ")],
    ):
        super().__init__(bstack1ll1ll1l1l1_opy_, bstack1l1l11111l1_opy_)
        self.bstack1l1l11l1ll1_opy_ = any(bstack1l11l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥጎ") in item.lower() for item in bstack1ll1ll1l1l1_opy_)
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
            self.logger.warning(bstack1l11l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣጏ") + str(test_hook_state) + bstack1l11l_opy_ (u"ࠣࠤጐ"))
            return
        if not self.bstack1l1l11l1ll1_opy_:
            self.logger.warning(bstack1l11l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥ጑") + str(str(self.bstack1ll1ll1l1l1_opy_)) + bstack1l11l_opy_ (u"ࠥࠦጒ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l11l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጓ") + str(kwargs) + bstack1l11l_opy_ (u"ࠧࠨጔ"))
            return
        instance = self.__1l1l11l1lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l11l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧጕ") + str(args) + bstack1l11l_opy_ (u"ࠢࠣ጖"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1l1l11l11_opy_ and test_hook_state == bstack1llll11ll1l_opy_.PRE:
                bstack1ll1ll11111_opy_ = bstack1lll1ll1l11_opy_.bstack1lll111l1ll_opy_(EVENTS.bstack1lll1l1l_opy_.value)
                name = str(EVENTS.bstack1lll1l1l_opy_.name)+bstack1l11l_opy_ (u"ࠣ࠼ࠥ጗")+str(test_framework_state.name)
                TestFramework.bstack1l1l111l111_opy_(instance, name, bstack1ll1ll11111_opy_)
        except Exception as e:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨጘ").format(e))
        try:
            if test_framework_state == bstack1lll11ll11l_opy_.TEST:
                if not TestFramework.bstack111l111l1l_opy_(instance, TestFramework.bstack1l11lll1l11_opy_) and test_hook_state == bstack1llll11ll1l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l1l111111l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l11l_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥጙ") + str(test_hook_state) + bstack1l11l_opy_ (u"ࠦࠧጚ"))
                if test_hook_state == bstack1llll11ll1l_opy_.PRE and not TestFramework.bstack111l111l1l_opy_(instance, TestFramework.bstack1ll111l111l_opy_):
                    TestFramework.bstack1111l1ll1l_opy_(instance, TestFramework.bstack1ll111l111l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11lllll1l_opy_(instance, args)
                    self.logger.debug(bstack1l11l_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥጛ") + str(test_hook_state) + bstack1l11l_opy_ (u"ࠨࠢጜ"))
                elif test_hook_state == bstack1llll11ll1l_opy_.POST and not TestFramework.bstack111l111l1l_opy_(instance, TestFramework.bstack1ll111l1lll_opy_):
                    TestFramework.bstack1111l1ll1l_opy_(instance, TestFramework.bstack1ll111l1lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11l_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥጝ") + str(test_hook_state) + bstack1l11l_opy_ (u"ࠣࠤጞ"))
            elif test_framework_state == bstack1lll11ll11l_opy_.STEP:
                if test_hook_state == bstack1llll11ll1l_opy_.PRE:
                    PytestBDDFramework.__1l1l1111l1l_opy_(instance, args)
                elif test_hook_state == bstack1llll11ll1l_opy_.POST:
                    PytestBDDFramework.__1l11ll1111l_opy_(instance, args)
            elif test_framework_state == bstack1lll11ll11l_opy_.LOG and test_hook_state == bstack1llll11ll1l_opy_.POST:
                PytestBDDFramework.__1l1l11l11l1_opy_(instance, *args)
            elif test_framework_state == bstack1lll11ll11l_opy_.LOG_REPORT and test_hook_state == bstack1llll11ll1l_opy_.POST:
                self.__1l1l11ll1l1_opy_(instance, *args)
            elif test_framework_state in PytestBDDFramework.bstack1l1l1l11l11_opy_:
                self.__1l11ll11ll1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥጟ") + str(instance.ref()) + bstack1l11l_opy_ (u"ࠥࠦጠ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11lll11ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1l1l11l11_opy_ and test_hook_state == bstack1llll11ll1l_opy_.POST:
                name = str(EVENTS.bstack1lll1l1l_opy_.name)+bstack1l11l_opy_ (u"ࠦ࠿ࠨጡ")+str(test_framework_state.name)
                bstack1ll1ll11111_opy_ = TestFramework.bstack1l1l1l111l1_opy_(instance, name)
                bstack1lll1ll1l11_opy_.end(EVENTS.bstack1lll1l1l_opy_.value, bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧጢ"), bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦጣ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢጤ").format(e))
    def bstack1ll1111llll_opy_(self):
        return self.bstack1l1l11l1ll1_opy_
    def __1l11lllll11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l11l_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧጥ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll11l1l1ll_opy_(rep, [bstack1l11l_opy_ (u"ࠤࡺ࡬ࡪࡴࠢጦ"), bstack1l11l_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦጧ"), bstack1l11l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦጨ"), bstack1l11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧጩ"), bstack1l11l_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢጪ"), bstack1l11l_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨጫ")])
        return None
    def __1l1l11ll1l1_opy_(self, instance: bstack1lllll1lll1_opy_, *args):
        result = self.__1l11lllll11_opy_(*args)
        if not result:
            return
        failure = None
        bstack111l11ll11_opy_ = None
        if result.get(bstack1l11l_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤጬ"), None) == bstack1l11l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤጭ") and len(args) > 1 and getattr(args[1], bstack1l11l_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦጮ"), None) is not None:
            failure = [{bstack1l11l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧጯ"): [args[1].excinfo.exconly(), result.get(bstack1l11l_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦጰ"), None)]}]
            bstack111l11ll11_opy_ = bstack1l11l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢጱ") if bstack1l11l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥጲ") in getattr(args[1].excinfo, bstack1l11l_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥጳ"), bstack1l11l_opy_ (u"ࠤࠥጴ")) else bstack1l11l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦጵ")
        bstack1l11lll1lll_opy_ = result.get(bstack1l11l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧጶ"), TestFramework.bstack1l1l1111ll1_opy_)
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
            target = None # bstack1l11ll1l1ll_opy_ bstack1l11llll1ll_opy_ this to be bstack1l11l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧጷ")
            if test_framework_state == bstack1lll11ll11l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11lll1l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll11ll11l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l11l_opy_ (u"ࠨ࡮ࡰࡦࡨࠦጸ"), None), bstack1l11l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢጹ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l11l_opy_ (u"ࠣࡰࡲࡨࡪࠨጺ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l11l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤጻ"), None):
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
        bstack1l11ll11111_opy_ = TestFramework.bstack1111ll111l_opy_(instance, PytestBDDFramework.bstack1l11ll1ll1l_opy_, {})
        if not key in bstack1l11ll11111_opy_:
            bstack1l11ll11111_opy_[key] = []
        bstack1l1l11lllll_opy_ = TestFramework.bstack1111ll111l_opy_(instance, PytestBDDFramework.bstack1l1l1111l11_opy_, {})
        if not key in bstack1l1l11lllll_opy_:
            bstack1l1l11lllll_opy_[key] = []
        bstack1l11ll1llll_opy_ = {
            PytestBDDFramework.bstack1l11ll1ll1l_opy_: bstack1l11ll11111_opy_,
            PytestBDDFramework.bstack1l1l1111l11_opy_: bstack1l1l11lllll_opy_,
        }
        if test_hook_state == bstack1llll11ll1l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l11l_opy_ (u"ࠥ࡯ࡪࡿࠢጼ"): key,
                TestFramework.bstack1l1l11lll11_opy_: uuid4().__str__(),
                TestFramework.bstack1l1l111lll1_opy_: TestFramework.bstack1l11ll1l111_opy_,
                TestFramework.bstack1l1l111l1l1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1l1111lll_opy_: [],
                TestFramework.bstack1l1l111l1ll_opy_: hook_name
            }
            bstack1l11ll11111_opy_[key].append(hook)
            bstack1l11ll1llll_opy_[PytestBDDFramework.bstack1l1l1l11ll1_opy_] = key
        elif test_hook_state == bstack1llll11ll1l_opy_.POST:
            bstack1l11llll11l_opy_ = bstack1l11ll11111_opy_.get(key, [])
            hook = bstack1l11llll11l_opy_.pop() if bstack1l11llll11l_opy_ else None
            if hook:
                result = self.__1l11lllll11_opy_(*args)
                if result:
                    bstack1l1l11l1l11_opy_ = result.get(bstack1l11l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧጽ"), TestFramework.bstack1l11ll1l111_opy_)
                    if bstack1l1l11l1l11_opy_ != TestFramework.bstack1l11ll1l111_opy_:
                        hook[TestFramework.bstack1l1l111lll1_opy_] = bstack1l1l11l1l11_opy_
                hook[TestFramework.bstack1l1l1l111ll_opy_] = datetime.now(tz=timezone.utc)
                bstack1l1l11lllll_opy_[key].append(hook)
                bstack1l11ll1llll_opy_[PytestBDDFramework.bstack1l11ll1lll1_opy_] = key
        TestFramework.bstack1l11ll11lll_opy_(instance, bstack1l11ll1llll_opy_)
        self.logger.debug(bstack1l11l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦጾ") + str(bstack1l1l11lllll_opy_) + bstack1l11l_opy_ (u"ࠨࠢጿ"))
    def __1l1l1l1111l_opy_(
        self,
        context: bstack1l11lll1ll1_opy_,
        test_framework_state: bstack1lll11ll11l_opy_,
        test_hook_state: bstack1llll11ll1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll11l1l1ll_opy_(args[0], [bstack1l11l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨፀ"), bstack1l11l_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤፁ"), bstack1l11l_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤፂ"), bstack1l11l_opy_ (u"ࠥ࡭ࡩࡹࠢፃ"), bstack1l11l_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨፄ"), bstack1l11l_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧፅ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l11l_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧፆ")) else fixturedef.get(bstack1l11l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨፇ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l11l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨፈ")) else None
        node = request.node if hasattr(request, bstack1l11l_opy_ (u"ࠤࡱࡳࡩ࡫ࠢፉ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l11l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥፊ")) else None
        baseid = fixturedef.get(bstack1l11l_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦፋ"), None) or bstack1l11l_opy_ (u"ࠧࠨፌ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l11l_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦፍ")):
            target = PytestBDDFramework.__1l1l11l1l1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l11l_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤፎ")) else None
            if target and not TestFramework.bstack1111l1llll_opy_(target):
                self.__1l11lll1l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l11l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥፏ") + str(test_hook_state) + bstack1l11l_opy_ (u"ࠤࠥፐ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l11l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣፑ") + str(target) + bstack1l11l_opy_ (u"ࠦࠧፒ"))
            return None
        instance = TestFramework.bstack1111l1llll_opy_(target)
        if not instance:
            self.logger.warning(bstack1l11l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢፓ") + str(target) + bstack1l11l_opy_ (u"ࠨࠢፔ"))
            return None
        bstack1l1l1111111_opy_ = TestFramework.bstack1111ll111l_opy_(instance, PytestBDDFramework.bstack1l11lll1111_opy_, {})
        if os.getenv(bstack1l11l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣፕ"), bstack1l11l_opy_ (u"ࠣ࠳ࠥፖ")) == bstack1l11l_opy_ (u"ࠤ࠴ࠦፗ"):
            bstack1l1l11l1111_opy_ = bstack1l11l_opy_ (u"ࠥ࠾ࠧፘ").join((scope, fixturename))
            bstack1l11ll1l11l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11lll11l1_opy_ = {
                bstack1l11l_opy_ (u"ࠦࡰ࡫ࡹࠣፙ"): bstack1l1l11l1111_opy_,
                bstack1l11l_opy_ (u"ࠧࡺࡡࡨࡵࠥፚ"): PytestBDDFramework.__1l11ll111ll_opy_(request.node, scenario),
                bstack1l11l_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢ፛"): fixturedef,
                bstack1l11l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ፜"): scope,
                bstack1l11l_opy_ (u"ࠣࡶࡼࡴࡪࠨ፝"): None,
            }
            try:
                if test_hook_state == bstack1llll11ll1l_opy_.POST and callable(getattr(args[-1], bstack1l11l_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨ፞"), None)):
                    bstack1l11lll11l1_opy_[bstack1l11l_opy_ (u"ࠥࡸࡾࡶࡥࠣ፟")] = TestFramework.bstack1ll11ll1l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llll11ll1l_opy_.PRE:
                bstack1l11lll11l1_opy_[bstack1l11l_opy_ (u"ࠦࡺࡻࡩࡥࠤ፠")] = uuid4().__str__()
                bstack1l11lll11l1_opy_[PytestBDDFramework.bstack1l1l111l1l1_opy_] = bstack1l11ll1l11l_opy_
            elif test_hook_state == bstack1llll11ll1l_opy_.POST:
                bstack1l11lll11l1_opy_[PytestBDDFramework.bstack1l1l1l111ll_opy_] = bstack1l11ll1l11l_opy_
            if bstack1l1l11l1111_opy_ in bstack1l1l1111111_opy_:
                bstack1l1l1111111_opy_[bstack1l1l11l1111_opy_].update(bstack1l11lll11l1_opy_)
                self.logger.debug(bstack1l11l_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨ፡") + str(bstack1l1l1111111_opy_[bstack1l1l11l1111_opy_]) + bstack1l11l_opy_ (u"ࠨࠢ።"))
            else:
                bstack1l1l1111111_opy_[bstack1l1l11l1111_opy_] = bstack1l11lll11l1_opy_
                self.logger.debug(bstack1l11l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥ፣") + str(len(bstack1l1l1111111_opy_)) + bstack1l11l_opy_ (u"ࠣࠤ፤"))
        TestFramework.bstack1111l1ll1l_opy_(instance, PytestBDDFramework.bstack1l11lll1111_opy_, bstack1l1l1111111_opy_)
        self.logger.debug(bstack1l11l_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ፥") + str(instance.ref()) + bstack1l11l_opy_ (u"ࠥࠦ፦"))
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
            PytestBDDFramework.bstack1l11lll1111_opy_: {},
            PytestBDDFramework.bstack1l1l1111l11_opy_: {},
            PytestBDDFramework.bstack1l11ll1ll1l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111l1ll1l_opy_(ob, TestFramework.bstack1l11ll1l1l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111l1ll1l_opy_(ob, TestFramework.bstack1ll1ll1llll_opy_, context.platform_index)
        TestFramework.bstack11111ll1l1_opy_[ctx.id] = ob
        self.logger.debug(bstack1l11l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦ፧") + str(TestFramework.bstack11111ll1l1_opy_.keys()) + bstack1l11l_opy_ (u"ࠧࠨ፨"))
        return ob
    @staticmethod
    def __1l11lllll1l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l11l_opy_ (u"࠭ࡩࡥࠩ፩"): id(step),
                bstack1l11l_opy_ (u"ࠧࡵࡧࡻࡸࠬ፪"): step.name,
                bstack1l11l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ፫"): step.keyword,
            })
        meta = {
            bstack1l11l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ፬"): {
                bstack1l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨ፭"): feature.name,
                bstack1l11l_opy_ (u"ࠫࡵࡧࡴࡩࠩ፮"): feature.filename,
                bstack1l11l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ፯"): feature.description
            },
            bstack1l11l_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ፰"): {
                bstack1l11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ፱"): scenario.name
            },
            bstack1l11l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ፲"): steps,
            bstack1l11l_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫ፳"): PytestBDDFramework.__1l11ll11l1l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l1l1l11l1l_opy_: meta
            }
        )
    @staticmethod
    def __1l1l1111l1l_opy_(instance, args):
        request, bstack1l11ll111l1_opy_ = args
        bstack1l1l11l11ll_opy_ = id(bstack1l11ll111l1_opy_)
        bstack1l1l11l111l_opy_ = instance.data[TestFramework.bstack1l1l1l11l1l_opy_]
        step = next(filter(lambda st: st[bstack1l11l_opy_ (u"ࠪ࡭ࡩ࠭፴")] == bstack1l1l11l11ll_opy_, bstack1l1l11l111l_opy_[bstack1l11l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ፵")]), None)
        step.update({
            bstack1l11l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ፶"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l1l11l111l_opy_[bstack1l11l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ፷")]) if st[bstack1l11l_opy_ (u"ࠧࡪࡦࠪ፸")] == step[bstack1l11l_opy_ (u"ࠨ࡫ࡧࠫ፹")]), None)
        if index is not None:
            bstack1l1l11l111l_opy_[bstack1l11l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ፺")][index] = step
        instance.data[TestFramework.bstack1l1l1l11l1l_opy_] = bstack1l1l11l111l_opy_
    @staticmethod
    def __1l11ll1111l_opy_(instance, args):
        bstack1l11l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸࡪࡨࡲࠥࡲࡥ࡯ࠢࡤࡶ࡬ࡹࠠࡪࡵࠣ࠶࠱ࠦࡩࡵࠢࡶ࡭࡬ࡴࡩࡧ࡫ࡨࡷࠥࡺࡨࡦࡴࡨࠤ࡮ࡹࠠ࡯ࡱࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠭ࠡ࡝ࡵࡩࡶࡻࡥࡴࡶ࠯ࠤࡸࡺࡥࡱ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮࡬ࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠶ࠤࡹ࡮ࡥ࡯ࠢࡷ࡬ࡪࠦ࡬ࡢࡵࡷࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡸࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ፻")
        bstack1l1l1l11111_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11ll111l1_opy_ = args[1]
        bstack1l1l11l11ll_opy_ = id(bstack1l11ll111l1_opy_)
        bstack1l1l11l111l_opy_ = instance.data[TestFramework.bstack1l1l1l11l1l_opy_]
        step = None
        if bstack1l1l11l11ll_opy_ is not None and bstack1l1l11l111l_opy_.get(bstack1l11l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ፼")):
            step = next(filter(lambda st: st[bstack1l11l_opy_ (u"ࠬ࡯ࡤࠨ፽")] == bstack1l1l11l11ll_opy_, bstack1l1l11l111l_opy_[bstack1l11l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ፾")]), None)
            step.update({
                bstack1l11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ፿"): bstack1l1l1l11111_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l11l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᎀ"): bstack1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᎁ"),
                bstack1l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᎂ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᎃ"): bstack1l11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᎄ"),
                })
        index = next((i for i, st in enumerate(bstack1l1l11l111l_opy_[bstack1l11l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᎅ")]) if st[bstack1l11l_opy_ (u"ࠧࡪࡦࠪᎆ")] == step[bstack1l11l_opy_ (u"ࠨ࡫ࡧࠫᎇ")]), None)
        if index is not None:
            bstack1l1l11l111l_opy_[bstack1l11l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᎈ")][index] = step
        instance.data[TestFramework.bstack1l1l1l11l1l_opy_] = bstack1l1l11l111l_opy_
    @staticmethod
    def __1l11ll11l1l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l11l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᎉ")):
                examples = list(node.callspec.params[bstack1l11l_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᎊ")].values())
            return examples
        except:
            return []
    def bstack1ll111ll1l1_opy_(self, instance: bstack1lllll1lll1_opy_, bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_]):
        bstack1l11llllll1_opy_ = (
            PytestBDDFramework.bstack1l1l1l11ll1_opy_
            if bstack11111lll1l_opy_[1] == bstack1llll11ll1l_opy_.PRE
            else PytestBDDFramework.bstack1l11ll1lll1_opy_
        )
        hook = PytestBDDFramework.bstack1l1l11llll1_opy_(instance, bstack1l11llllll1_opy_)
        entries = hook.get(TestFramework.bstack1l1l1111lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1l11llll111_opy_, []))
        return entries
    def bstack1ll1111lll1_opy_(self, instance: bstack1lllll1lll1_opy_, bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_]):
        bstack1l11llllll1_opy_ = (
            PytestBDDFramework.bstack1l1l1l11ll1_opy_
            if bstack11111lll1l_opy_[1] == bstack1llll11ll1l_opy_.PRE
            else PytestBDDFramework.bstack1l11ll1lll1_opy_
        )
        PytestBDDFramework.bstack1l1l11ll1ll_opy_(instance, bstack1l11llllll1_opy_)
        TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1l11llll111_opy_, []).clear()
    @staticmethod
    def bstack1l1l11llll1_opy_(instance: bstack1lllll1lll1_opy_, bstack1l11llllll1_opy_: str):
        bstack1l1l111ll11_opy_ = (
            PytestBDDFramework.bstack1l1l1111l11_opy_
            if bstack1l11llllll1_opy_ == PytestBDDFramework.bstack1l11ll1lll1_opy_
            else PytestBDDFramework.bstack1l11ll1ll1l_opy_
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
        hook = PytestBDDFramework.bstack1l1l11llll1_opy_(instance, bstack1l11llllll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1l1111lll_opy_, []).clear()
    @staticmethod
    def __1l1l11l11l1_opy_(instance: bstack1lllll1lll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l11l_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᎋ"), None)):
            return
        if os.getenv(bstack1l11l_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᎌ"), bstack1l11l_opy_ (u"ࠢ࠲ࠤᎍ")) != bstack1l11l_opy_ (u"ࠣ࠳ࠥᎎ"):
            PytestBDDFramework.logger.warning(bstack1l11l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᎏ"))
            return
        bstack1l11lllllll_opy_ = {
            bstack1l11l_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ᎐"): (PytestBDDFramework.bstack1l1l1l11ll1_opy_, PytestBDDFramework.bstack1l11ll1ll1l_opy_),
            bstack1l11l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ᎑"): (PytestBDDFramework.bstack1l11ll1lll1_opy_, PytestBDDFramework.bstack1l1l1111l11_opy_),
        }
        for when in (bstack1l11l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ᎒"), bstack1l11l_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ᎓"), bstack1l11l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ᎔")):
            bstack1l11ll11l11_opy_ = args[1].get_records(when)
            if not bstack1l11ll11l11_opy_:
                continue
            records = [
                bstack1lllll11111_opy_(
                    kind=TestFramework.bstack1ll1l11111l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l11l_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦ᎕")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l11l_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥ᎖")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll11l11_opy_
                if isinstance(getattr(r, bstack1l11l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ᎗"), None), str) and r.message.strip()
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
    def __1l1l111111l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1lll1l11_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l1l11ll11l_opy_(request.node, scenario)
        bstack1l11lll111l_opy_ = feature.filename
        if not bstack1lll1l11_opy_ or not test_name or not bstack1l11lll111l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1l1lll1l_opy_: uuid4().__str__(),
            TestFramework.bstack1l11lll1l11_opy_: bstack1lll1l11_opy_,
            TestFramework.bstack1lll111ll11_opy_: test_name,
            TestFramework.bstack1ll1111l111_opy_: bstack1lll1l11_opy_,
            TestFramework.bstack1l1l111l11l_opy_: bstack1l11lll111l_opy_,
            TestFramework.bstack1l1l11111ll_opy_: PytestBDDFramework.__1l11ll111ll_opy_(feature, scenario),
            TestFramework.bstack1l1l11ll111_opy_: code,
            TestFramework.bstack1l1lll1111l_opy_: TestFramework.bstack1l1l1111ll1_opy_,
            TestFramework.bstack1l1l1lll11l_opy_: test_name
        }
    @staticmethod
    def __1l1l11ll11l_opy_(node, scenario):
        if hasattr(node, bstack1l11l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭᎘")):
            parts = node.nodeid.rsplit(bstack1l11l_opy_ (u"ࠧࡡࠢ᎙"))
            params = parts[-1]
            return bstack1l11l_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨ᎚").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11ll111ll_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l11l_opy_ (u"ࠧࡵࡣࡪࡷࠬ᎛")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l11l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭᎜")) else [])
    @staticmethod
    def __1l1l11l1l1l_opy_(location):
        return bstack1l11l_opy_ (u"ࠤ࠽࠾ࠧ᎝").join(filter(lambda x: isinstance(x, str), location))