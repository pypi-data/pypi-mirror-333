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
from datetime import datetime, timezone
import os
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1111llll1l_opy_ import bstack1111lll11l_opy_, bstack11111ll11l_opy_, bstack11111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111lll_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1111111l1l_opy_ import bstack111111llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import bstack1llll11111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l11ll1_opy_, bstack1lllll1lll1_opy_, bstack111111l1ll_opy_, bstack1llll1l111l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1ll1111l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1ll11ll1111_opy_ = [bstack11_opy_ (u"ࠣࡰࡤࡱࡪࠨᅬ"), bstack11_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᅭ"), bstack11_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥᅮ"), bstack11_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࠧᅯ"), bstack11_opy_ (u"ࠧࡶࡡࡵࡪࠥᅰ")]
bstack1ll11ll1lll_opy_ = {
    bstack11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡉࡵࡧࡰࠦᅱ"): bstack1ll11ll1111_opy_,
    bstack11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡑࡣࡦ࡯ࡦ࡭ࡥࠣᅲ"): bstack1ll11ll1111_opy_,
    bstack11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡏࡲࡨࡺࡲࡥࠣᅳ"): bstack1ll11ll1111_opy_,
    bstack11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡆࡰࡦࡹࡳࠣᅴ"): bstack1ll11ll1111_opy_,
    bstack11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡊࡺࡴࡣࡵ࡫ࡲࡲࠧᅵ"): bstack1ll11ll1111_opy_
    + [
        bstack11_opy_ (u"ࠦࡴࡸࡩࡨ࡫ࡱࡥࡱࡴࡡ࡮ࡧࠥᅶ"),
        bstack11_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢᅷ"),
        bstack11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࡩ࡯ࡨࡲࠦᅸ"),
        bstack11_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤᅹ"),
        bstack11_opy_ (u"ࠣࡥࡤࡰࡱࡹࡰࡦࡥࠥᅺ"),
        bstack11_opy_ (u"ࠤࡦࡥࡱࡲ࡯ࡣ࡬ࠥᅻ"),
        bstack11_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤᅼ"),
        bstack11_opy_ (u"ࠦࡸࡺ࡯ࡱࠤᅽ"),
        bstack11_opy_ (u"ࠧࡪࡵࡳࡣࡷ࡭ࡴࡴࠢᅾ"),
        bstack11_opy_ (u"ࠨࡷࡩࡧࡱࠦᅿ"),
    ],
    bstack11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣ࡬ࡲ࠳࡙ࡥࡴࡵ࡬ࡳࡳࠨᆀ"): [bstack11_opy_ (u"ࠣࡵࡷࡥࡷࡺࡰࡢࡶ࡫ࠦᆁ"), bstack11_opy_ (u"ࠤࡷࡩࡸࡺࡳࡧࡣ࡬ࡰࡪࡪࠢᆂ"), bstack11_opy_ (u"ࠥࡸࡪࡹࡴࡴࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦᆃ"), bstack11_opy_ (u"ࠦ࡮ࡺࡥ࡮ࡵࠥᆄ")],
    bstack11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡩ࡯࡯ࡨ࡬࡫࠳ࡉ࡯࡯ࡨ࡬࡫ࠧᆅ"): [bstack11_opy_ (u"ࠨࡩ࡯ࡸࡲࡧࡦࡺࡩࡰࡰࡢࡴࡦࡸࡡ࡮ࡵࠥᆆ"), bstack11_opy_ (u"ࠢࡢࡴࡪࡷࠧᆇ")],
    bstack11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡊ࡮ࡾࡴࡶࡴࡨࡈࡪ࡬ࠢᆈ"): [bstack11_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᆉ"), bstack11_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᆊ"), bstack11_opy_ (u"ࠦ࡫ࡻ࡮ࡤࠤᆋ"), bstack11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᆌ"), bstack11_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᆍ"), bstack11_opy_ (u"ࠢࡪࡦࡶࠦᆎ")],
    bstack11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡗࡺࡨࡒࡦࡳࡸࡩࡸࡺࠢᆏ"): [bstack11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᆐ"), bstack11_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࠤᆑ"), bstack11_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡢ࡭ࡳࡪࡥࡹࠤᆒ")],
    bstack11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡸࡵ࡯ࡰࡨࡶ࠳ࡉࡡ࡭࡮ࡌࡲ࡫ࡵࠢᆓ"): [bstack11_opy_ (u"ࠨࡷࡩࡧࡱࠦᆔ"), bstack11_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࠢᆕ")],
    bstack11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡒࡴࡪࡥࡌࡧࡼࡻࡴࡸࡤࡴࠤᆖ"): [bstack11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᆗ"), bstack11_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᆘ")],
    bstack11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡍࡢࡴ࡮ࠦᆙ"): [bstack11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆚ"), bstack11_opy_ (u"ࠨࡡࡳࡩࡶࠦᆛ"), bstack11_opy_ (u"ࠢ࡬ࡹࡤࡶ࡬ࡹࠢᆜ")],
}
class bstack1lllll111l1_opy_(bstack1lll11l1lll_opy_):
    bstack1ll11ll1ll1_opy_ = bstack11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࠣᆝ")
    bstack1ll111ll1ll_opy_ = bstack11_opy_ (u"ࠤࡌࡒࡋࡕࠢᆞ")
    bstack1ll11l11111_opy_ = bstack11_opy_ (u"ࠥࡉࡗࡘࡏࡓࠤᆟ")
    bstack1ll111l1lll_opy_: Callable
    bstack1ll11ll1l11_opy_: Callable
    def __init__(self, bstack1lll1ll1l1l_opy_, bstack1lllll11l11_opy_):
        super().__init__()
        self.bstack1lll111l11l_opy_ = bstack1lllll11l11_opy_
        if os.getenv(bstack11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡓ࠶࠷࡙ࠣᆠ"), bstack11_opy_ (u"ࠧ࠷ࠢᆡ")) != bstack11_opy_ (u"ࠨ࠱ࠣᆢ") or not self.is_enabled():
            self.logger.warning(bstack11_opy_ (u"ࠢࠣᆣ") + str(self.__class__.__name__) + bstack11_opy_ (u"ࠣࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠦᆤ"))
            return
        TestFramework.bstack1ll1llllll1_opy_((bstack1lll1l11ll1_opy_.TEST, bstack111111l1ll_opy_.PRE), self.bstack1lll1111ll1_opy_)
        TestFramework.bstack1ll1llllll1_opy_((bstack1lll1l11ll1_opy_.TEST, bstack111111l1ll_opy_.POST), self.bstack1ll1lll11l1_opy_)
        for event in bstack1lll1l11ll1_opy_:
            for state in bstack111111l1ll_opy_:
                TestFramework.bstack1ll1llllll1_opy_((event, state), self.bstack1ll111l1l11_opy_)
        bstack1lll1ll1l1l_opy_.bstack1ll1llllll1_opy_((bstack11111ll11l_opy_.bstack1111ll1l1l_opy_, bstack11111l1lll_opy_.POST), self.bstack1ll111l1ll1_opy_)
        self.bstack1ll111l1lll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1ll11ll11ll_opy_(bstack1lllll111l1_opy_.bstack1ll111ll1ll_opy_, self.bstack1ll111l1lll_opy_)
        self.bstack1ll11ll1l11_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1ll11ll11ll_opy_(bstack1lllll111l1_opy_.bstack1ll11l11111_opy_, self.bstack1ll11ll1l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll111l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1ll11lll1ll_opy_() and instance:
            bstack1ll11l111l1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1111l11l11_opy_
            if test_framework_state == bstack1lll1l11ll1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll1l11ll1_opy_.LOG:
                bstack11lllll1l_opy_ = datetime.now()
                entries = f.bstack1ll11ll111l_opy_(instance, bstack1111l11l11_opy_)
                if entries:
                    self.bstack1ll1111l1ll_opy_(instance, entries)
                    instance.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࠤᆥ"), datetime.now() - bstack11lllll1l_opy_)
                    f.bstack1ll111lllll_opy_(instance, bstack1111l11l11_opy_)
                instance.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᆦ"), datetime.now() - bstack1ll11l111l1_opy_)
                return # do not send this event with the bstack1ll111ll11l_opy_ bstack1ll1l11111l_opy_
            elif (
                test_framework_state == bstack1lll1l11ll1_opy_.TEST
                and test_hook_state == bstack111111l1ll_opy_.POST
                and not f.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1111ll11_opy_)
            ):
                self.logger.warning(bstack11_opy_ (u"ࠦࡩࡸ࡯ࡱࡲ࡬ࡲ࡬ࠦࡤࡶࡧࠣࡸࡴࠦ࡬ࡢࡥ࡮ࠤࡴ࡬ࠠࡳࡧࡶࡹࡱࡺࡳࠡࠤᆧ") + str(TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1111ll11_opy_)) + bstack11_opy_ (u"ࠧࠨᆨ"))
                f.bstack1111lll1l1_opy_(instance, bstack1lllll111l1_opy_.bstack1ll11ll1ll1_opy_, True)
                return # do not send this event bstack1ll111l1111_opy_ bstack1ll11l1111l_opy_
            elif (
                f.bstack11111lll1l_opy_(instance, bstack1lllll111l1_opy_.bstack1ll11ll1ll1_opy_, False)
                and test_framework_state == bstack1lll1l11ll1_opy_.LOG_REPORT
                and test_hook_state == bstack111111l1ll_opy_.POST
                and f.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1111ll11_opy_)
            ):
                self.logger.warning(bstack11_opy_ (u"ࠨࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡕࡇࡖࡘ࠱ࠦࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡐࡐࡕࡗࠤࠧᆩ") + str(TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1111ll11_opy_)) + bstack11_opy_ (u"ࠢࠣᆪ"))
                self.bstack1ll111l1l11_opy_(f, instance, (bstack1lll1l11ll1_opy_.TEST, bstack111111l1ll_opy_.POST), *args, **kwargs)
            bstack11lllll1l_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1ll111lll1l_opy_ = sorted(
                filter(lambda x: x.get(bstack11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᆫ"), None), data.pop(bstack11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᆬ"), {}).values()),
                key=lambda x: x[bstack11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᆭ")],
            )
            if bstack111111llll_opy_.bstack1ll11llllll_opy_ in data:
                data.pop(bstack111111llll_opy_.bstack1ll11llllll_opy_)
            data.update({bstack11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᆮ"): bstack1ll111lll1l_opy_})
            instance.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᆯ"), datetime.now() - bstack11lllll1l_opy_)
            bstack11lllll1l_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1ll11l1l11l_opy_)
            instance.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤᆰ"), datetime.now() - bstack11lllll1l_opy_)
            self.bstack1ll1l11111l_opy_(instance, bstack1111l11l11_opy_, event_json=event_json)
            instance.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᆱ"), datetime.now() - bstack1ll11l111l1_opy_)
    def bstack1lll1111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1ll1111_opy_ import bstack11111111l1_opy_
        bstack1ll1l1llll1_opy_ = bstack11111111l1_opy_.bstack1ll1ll11111_opy_(EVENTS.bstack1ll1l111ll_opy_.value)
        self.bstack1lll111l11l_opy_.bstack1ll111llll1_opy_(instance, f, bstack1111l11l11_opy_, *args, **kwargs)
        bstack11111111l1_opy_.end(EVENTS.bstack1ll1l111ll_opy_.value, bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᆲ"), bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᆳ"), status=True, failure=None, test_name=None)
    def bstack1ll1lll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1lll111l11l_opy_.bstack1ll11l1l1ll_opy_(instance, f, bstack1111l11l11_opy_, *args, **kwargs)
        self.bstack1ll11lll1l1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1ll111l11ll_opy_, stage=STAGE.bstack1lll11111l_opy_)
    def bstack1ll11lll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠡࡩࡕࡔࡈࠦࡣࡢ࡮࡯࠾ࠥࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠨᆴ"))
            return
        bstack11lllll1l_opy_ = datetime.now()
        try:
            r = self.bstack11111l11ll_opy_.TestSessionEvent(req)
            instance.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡥࡷࡧࡱࡸࠧᆵ"), datetime.now() - bstack11lllll1l_opy_)
            f.bstack1111lll1l1_opy_(instance, self.bstack1lll111l11l_opy_.bstack1ll11llll11_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᆶ") + str(r) + bstack11_opy_ (u"ࠨࠢᆷ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᆸ") + str(e) + bstack11_opy_ (u"ࠣࠤᆹ"))
            traceback.print_exc()
            raise e
    def bstack1ll111l1ll1_opy_(
        self,
        f: bstack1llll11111l_opy_,
        _driver: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        _1ll111l1l1l_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1llll11111l_opy_.bstack1lll1111lll_opy_(method_name):
            return
        if f.bstack1lll1111l11_opy_(*args) != bstack1llll11111l_opy_.bstack1ll111l111l_opy_:
            return
        bstack1ll11l111l1_opy_ = datetime.now()
        screenshot = result.get(bstack11_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᆺ"), None) if isinstance(result, dict) else None
        if not isinstance(screenshot, str) or len(screenshot) <= 0:
            self.logger.warning(bstack11_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡ࡫ࡰࡥ࡬࡫ࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡶࡵࠦᆻ"))
            return
        bstack1ll11l11l11_opy_ = self.bstack1ll111lll11_opy_(instance)
        if bstack1ll11l11l11_opy_:
            entry = bstack1llll1l111l_opy_(TestFramework.bstack1ll1111ll1l_opy_, screenshot)
            self.bstack1ll1111l1ll_opy_(bstack1ll11l11l11_opy_, [entry])
            instance.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩࠧᆼ"), datetime.now() - bstack1ll11l111l1_opy_)
        else:
            self.logger.warning(bstack11_opy_ (u"ࠧࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡫ࡳࡵࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺࡨࡪࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡸࡣࡶࠤࡹࡧ࡫ࡦࡰࠣࡦࡾࠦࡤࡳ࡫ࡹࡩࡷࡃࠢᆽ") + str(instance.ref()) + bstack11_opy_ (u"ࠨࠢᆾ"))
    @measure(event_name=EVENTS.bstack1ll11ll11l1_opy_, stage=STAGE.bstack1lll11111l_opy_)
    def bstack1ll1111l1ll_opy_(
        self,
        bstack1ll11l11l11_opy_: bstack1lllll1lll1_opy_,
        entries: List[bstack1llll1l111l_opy_],
    ):
        self.bstack1ll1ll11lll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lll1l_opy_(bstack1ll11l11l11_opy_, TestFramework.bstack1ll1llll111_opy_)
        req.execution_context.hash = str(bstack1ll11l11l11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1ll11l11l11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1ll11l11l11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111lll1l_opy_(bstack1ll11l11l11_opy_, TestFramework.bstack1lll11111l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111lll1l_opy_(bstack1ll11l11l11_opy_, TestFramework.bstack1ll11lllll1_opy_)
            log_entry.uuid = TestFramework.bstack11111lll1l_opy_(bstack1ll11l11l11_opy_, TestFramework.bstack1ll1ll1l111_opy_)
            log_entry.test_framework_state = bstack1ll11l11l11_opy_.state.name
            log_entry.message = entry.message.encode(bstack11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᆿ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
        def bstack1ll11l1ll11_opy_():
            bstack11lllll1l_opy_ = datetime.now()
            try:
                self.bstack11111l11ll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1ll1111ll1l_opy_:
                    bstack1ll11l11l11_opy_.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᇀ"), datetime.now() - bstack11lllll1l_opy_)
                else:
                    bstack1ll11l11l11_opy_.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡ࡯ࡳ࡬ࠨᇁ"), datetime.now() - bstack11lllll1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᇂ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111l11l11l_opy_.enqueue(bstack1ll11l1ll11_opy_)
    @measure(event_name=EVENTS.bstack1ll1l1111l1_opy_, stage=STAGE.bstack1lll11111l_opy_)
    def bstack1ll1l11111l_opy_(
        self,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        event_json=None,
    ):
        self.bstack1ll1ll11lll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1llll111_opy_)
        req.test_framework_name = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1lll11111l1_opy_)
        req.test_framework_version = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll11lllll1_opy_)
        req.test_framework_state = bstack1111l11l11_opy_[0].name
        req.test_hook_state = bstack1111l11l11_opy_[1].name
        started_at = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll11l1lll1_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll11llll1l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1ll11l1l11l_opy_)).encode(bstack11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᇃ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1ll11l1ll11_opy_():
            bstack11lllll1l_opy_ = datetime.now()
            try:
                self.bstack11111l11ll_opy_.TestFrameworkEvent(req)
                instance.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡨࡺࡪࡴࡴࠣᇄ"), datetime.now() - bstack11lllll1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᇅ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111l11l11l_opy_.enqueue(bstack1ll11l1ll11_opy_)
    def bstack1ll111ll111_opy_(self, event_url: str, bstack111lll1l1l_opy_: dict) -> bool:
        return True # always return True so that old bstack1ll111l11l1_opy_ bstack1ll11lll111_opy_'t bstack1ll11l11l1l_opy_
    def bstack1ll111lll11_opy_(self, instance: bstack1111lll11l_opy_):
        bstack1ll1111lll1_opy_ = TestFramework.bstack11111ll111_opy_(instance.context)
        for t in bstack1ll1111lll1_opy_:
            bstack1ll11l11ll1_opy_ = TestFramework.bstack11111lll1l_opy_(t, bstack111111llll_opy_.bstack1ll11llllll_opy_, [])
            if any(instance is d[1] for d in bstack1ll11l11ll1_opy_):
                return t
    def bstack1ll11l1l1l1_opy_(self, message):
        self.bstack1ll111l1lll_opy_(message + bstack11_opy_ (u"ࠢ࡝ࡰࠥᇆ"))
    def log_error(self, message):
        self.bstack1ll11ll1l11_opy_(message + bstack11_opy_ (u"ࠣ࡞ࡱࠦᇇ"))
    def bstack1ll11ll11ll_opy_(self, level, original_func):
        def bstack1ll11l1ll1l_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1ll1111lll1_opy_ = TestFramework.bstack1ll11l111ll_opy_()
            if not bstack1ll1111lll1_opy_:
                return return_value
            bstack1ll11l11l11_opy_ = next(
                (
                    instance
                    for instance in bstack1ll1111lll1_opy_
                    if TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1ll1l111_opy_)
                ),
                None,
            )
            if not bstack1ll11l11l11_opy_:
                return
            entry = bstack1llll1l111l_opy_(TestFramework.bstack1ll111ll1l1_opy_, message, level)
            self.bstack1ll1111l1ll_opy_(bstack1ll11l11l11_opy_, [entry])
            return return_value
        return bstack1ll11l1ll1l_opy_
class bstack1ll11l1l11l_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1ll11l11lll_opy_ = set()
        kwargs[bstack11_opy_ (u"ࠤࡶ࡯࡮ࡶ࡫ࡦࡻࡶࠦᇈ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1ll11l1llll_opy_(obj, self.bstack1ll11l11lll_opy_)
def bstack1ll1l111111_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1ll11l1llll_opy_(obj, bstack1ll11l11lll_opy_=None, max_depth=3):
    if bstack1ll11l11lll_opy_ is None:
        bstack1ll11l11lll_opy_ = set()
    if id(obj) in bstack1ll11l11lll_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1ll11l11lll_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1ll1111llll_opy_ = TestFramework.bstack1ll11l1l111_opy_(obj)
    bstack1ll11ll1l1l_opy_ = next((k.lower() in bstack1ll1111llll_opy_.lower() for k in bstack1ll11ll1lll_opy_.keys()), None)
    if bstack1ll11ll1l1l_opy_:
        obj = TestFramework.bstack1ll11lll11l_opy_(obj, bstack1ll11ll1lll_opy_[bstack1ll11ll1l1l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨᇉ")):
            keys = getattr(obj, bstack11_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢᇊ"), [])
        elif hasattr(obj, bstack11_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢᇋ")):
            keys = getattr(obj, bstack11_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣᇌ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11_opy_ (u"ࠢࡠࠤᇍ"))}
        if not obj and bstack1ll1111llll_opy_ == bstack11_opy_ (u"ࠣࡲࡤࡸ࡭ࡲࡩࡣ࠰ࡓࡳࡸ࡯ࡸࡑࡣࡷ࡬ࠧᇎ"):
            obj = {bstack11_opy_ (u"ࠤࡳࡥࡹ࡮ࠢᇏ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1ll1l111111_opy_(key) or str(key).startswith(bstack11_opy_ (u"ࠥࡣࠧᇐ")):
            continue
        if value is not None and bstack1ll1l111111_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1ll11l1llll_opy_(value, bstack1ll11l11lll_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1ll11l1llll_opy_(o, bstack1ll11l11lll_opy_, max_depth) for o in value]))
    return result or None