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
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1111l11ll1_opy_,
    bstack11111l1lll_opy_,
    bstack1111lllll1_opy_,
    bstack111l1111ll_opy_,
    bstack1111ll1111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llllll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_, bstack1lllll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l1l_opy_ import bstack1ll1l111lll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1111ll1l_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1llll11l1l1_opy_(bstack1ll1l111lll_opy_):
    bstack1l1ll1ll1l1_opy_ = bstack1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡶ࡮ࡼࡥࡳࡵࠥኪ")
    bstack1ll11l111ll_opy_ = bstack1l11l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦካ")
    bstack1l1ll1ll11l_opy_ = bstack1l11l_opy_ (u"ࠨ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣኬ")
    bstack1l1lll11ll1_opy_ = bstack1l11l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢክ")
    bstack1l1ll1lll1l_opy_ = bstack1l11l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡳࡧࡩࡷࠧኮ")
    bstack1ll111ll11l_opy_ = bstack1l11l_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣኯ")
    bstack1l1lll11lll_opy_ = bstack1l11l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨኰ")
    bstack1l1lll1l111_opy_ = bstack1l11l_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠤ኱")
    def __init__(self):
        super().__init__(bstack1ll1l111l11_opy_=self.bstack1l1ll1ll1l1_opy_, frameworks=[bstack1llllll111l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1ll1l11l_opy_((bstack1lll11ll11l_opy_.BEFORE_EACH, bstack1llll11ll1l_opy_.POST), self.bstack1l1l1ll1ll1_opy_)
        TestFramework.bstack1ll1ll1l11l_opy_((bstack1lll11ll11l_opy_.TEST, bstack1llll11ll1l_opy_.PRE), self.bstack1ll1llllll1_opy_)
        TestFramework.bstack1ll1ll1l11l_opy_((bstack1lll11ll11l_opy_.TEST, bstack1llll11ll1l_opy_.POST), self.bstack1lll111l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll111llll1_opy_ = self.bstack1l1l1ll11l1_opy_(instance.context)
        if not bstack1ll111llll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣኲ") + str(bstack11111lll1l_opy_) + bstack1l11l_opy_ (u"ࠨࠢኳ"))
        f.bstack1111l1ll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll11l111ll_opy_, bstack1ll111llll1_opy_)
        bstack1l1l1ll111l_opy_ = self.bstack1l1l1ll11l1_opy_(instance.context, bstack1l1l1ll1lll_opy_=False)
        f.bstack1111l1ll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1ll1ll11l_opy_, bstack1l1l1ll111l_opy_)
    def bstack1ll1llllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack11111lll1l_opy_, *args, **kwargs)
        if not f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1lll11lll_opy_, False):
            self.__1l1l1lll111_opy_(f,instance,bstack11111lll1l_opy_)
    def bstack1lll111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack11111lll1l_opy_, *args, **kwargs)
        if not f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1lll11lll_opy_, False):
            self.__1l1l1lll111_opy_(f, instance, bstack11111lll1l_opy_)
        if not f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1lll1l111_opy_, False):
            self.__1l1l1ll11ll_opy_(f, instance, bstack11111lll1l_opy_)
    def bstack1l1l1lll1l1_opy_(
        self,
        f: bstack1llllll111l_opy_,
        driver: object,
        exec: Tuple[bstack111l1111ll_opy_, str],
        bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1lll11111ll_opy_(instance):
            return
        if f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1lll1l111_opy_, False):
            return
        driver.execute_script(
            bstack1l11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧኴ").format(
                json.dumps(
                    {
                        bstack1l11l_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣኵ"): bstack1l11l_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ኶"),
                        bstack1l11l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ኷"): {bstack1l11l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦኸ"): result},
                    }
                )
            )
        )
        f.bstack1111l1ll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1lll1l111_opy_, True)
    def bstack1l1l1ll11l1_opy_(self, context: bstack1111ll1111_opy_, bstack1l1l1ll1lll_opy_= True):
        if bstack1l1l1ll1lll_opy_:
            bstack1ll111llll1_opy_ = self.bstack1ll1l111ll1_opy_(context, reverse=True)
        else:
            bstack1ll111llll1_opy_ = self.bstack1ll1l11lll1_opy_(context, reverse=True)
        return [f for f in bstack1ll111llll1_opy_ if f[1].state != bstack1111l11ll1_opy_.QUIT]
    @measure(event_name=EVENTS.bstack11ll1l111l_opy_, stage=STAGE.bstack1111111l_opy_)
    def __1l1l1ll11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
    ):
        bstack1ll111llll1_opy_ = f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll11l111ll_opy_, [])
        if not bstack1ll111llll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣኹ") + str(bstack11111lll1l_opy_) + bstack1l11l_opy_ (u"ࠨࠢኺ"))
            return
        driver = bstack1ll111llll1_opy_[0][0]()
        status = f.bstack1111ll111l_opy_(instance, TestFramework.bstack1l1lll1111l_opy_, None)
        if not status:
            self.logger.debug(bstack1l11l_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤኻ") + str(bstack11111lll1l_opy_) + bstack1l11l_opy_ (u"ࠣࠤኼ"))
            return
        bstack1l1ll1ll111_opy_ = {bstack1l11l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤኽ"): status.lower()}
        bstack1l1ll1lllll_opy_ = f.bstack1111ll111l_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_, None)
        if status.lower() == bstack1l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪኾ") and bstack1l1ll1lllll_opy_ is not None:
            bstack1l1ll1ll111_opy_[bstack1l11l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ኿")] = bstack1l1ll1lllll_opy_[0][bstack1l11l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨዀ")][0] if isinstance(bstack1l1ll1lllll_opy_, list) else str(bstack1l1ll1lllll_opy_)
        driver.execute_script(
            bstack1l11l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦ዁").format(
                json.dumps(
                    {
                        bstack1l11l_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢዂ"): bstack1l11l_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦዃ"),
                        bstack1l11l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧዄ"): bstack1l1ll1ll111_opy_,
                    }
                )
            )
        )
        f.bstack1111l1ll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1lll1l111_opy_, True)
    @measure(event_name=EVENTS.bstack1ll1lllll_opy_, stage=STAGE.bstack1111111l_opy_)
    def __1l1l1lll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_]
    ):
        test_name = f.bstack1111ll111l_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_, None)
        if not test_name:
            self.logger.debug(bstack1l11l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤዅ"))
            return
        bstack1ll111llll1_opy_ = f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll11l111ll_opy_, [])
        if not bstack1ll111llll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨ዆") + str(bstack11111lll1l_opy_) + bstack1l11l_opy_ (u"ࠧࠨ዇"))
            return
        for bstack1ll1111l11l_opy_, bstack1l1l1ll1l11_opy_ in bstack1ll111llll1_opy_:
            if not bstack1llllll111l_opy_.bstack1lll11111ll_opy_(bstack1l1l1ll1l11_opy_):
                continue
            driver = bstack1ll1111l11l_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack1l11l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦወ").format(
                    json.dumps(
                        {
                            bstack1l11l_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢዉ"): bstack1l11l_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤዊ"),
                            bstack1l11l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧዋ"): {bstack1l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣዌ"): test_name},
                        }
                    )
                )
            )
        f.bstack1111l1ll1l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1lll11lll_opy_, True)
    def bstack1ll11l11lll_opy_(
        self,
        instance: bstack1lllll1lll1_opy_,
        f: TestFramework,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack11111lll1l_opy_, *args, **kwargs)
        bstack1ll111llll1_opy_ = [d for d, _ in f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll11l111ll_opy_, [])]
        if not bstack1ll111llll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦው"))
            return
        if not bstack1ll1111ll1l_opy_():
            self.logger.debug(bstack1l11l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥዎ"))
            return
        for bstack1l1l1lll1ll_opy_ in bstack1ll111llll1_opy_:
            driver = bstack1l1l1lll1ll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l11l_opy_ (u"ࠨࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࡙ࡹ࡯ࡥ࠽ࠦዏ") + str(timestamp)
            driver.execute_script(
                bstack1l11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧዐ").format(
                    json.dumps(
                        {
                            bstack1l11l_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣዑ"): bstack1l11l_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦዒ"),
                            bstack1l11l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨዓ"): {
                                bstack1l11l_opy_ (u"ࠦࡹࡿࡰࡦࠤዔ"): bstack1l11l_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤዕ"),
                                bstack1l11l_opy_ (u"ࠨࡤࡢࡶࡤࠦዖ"): data,
                                bstack1l11l_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨ዗"): bstack1l11l_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢዘ")
                            }
                        }
                    )
                )
            )
    def bstack1ll111ll1ll_opy_(
        self,
        instance: bstack1lllll1lll1_opy_,
        f: TestFramework,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack11111lll1l_opy_, *args, **kwargs)
        bstack1ll111llll1_opy_ = [d for _, d in f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll11l111ll_opy_, [])] + [d for _, d in f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1l1ll1ll11l_opy_, [])]
        keys = [
            bstack1llll11l1l1_opy_.bstack1ll11l111ll_opy_,
            bstack1llll11l1l1_opy_.bstack1l1ll1ll11l_opy_,
        ]
        bstack1ll111llll1_opy_ = [
            d for key in keys for _, d in f.bstack1111ll111l_opy_(instance, key, [])
        ]
        if not bstack1ll111llll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡴࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣࡸࡴࠦ࡬ࡪࡰ࡮ࠦዙ"))
            return
        if f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll111ll11l_opy_, False):
            self.logger.debug(bstack1l11l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡈࡈࡔࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡦࡶࡪࡧࡴࡦࡦࠥዚ"))
            return
        self.bstack1ll1l1ll1ll_opy_()
        bstack1ll11ll11l_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll1ll1llll_opy_)
        req.test_framework_name = TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll1llll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll111lll11_opy_)
        req.test_framework_state = bstack11111lll1l_opy_[0].name
        req.test_hook_state = bstack11111lll1l_opy_[1].name
        req.test_uuid = TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll1l1lll1l_opy_)
        for driver in bstack1ll111llll1_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l11l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥዛ")
                if bstack1llllll111l_opy_.bstack1111ll111l_opy_(driver, bstack1llllll111l_opy_.bstack1l1l1ll1l1l_opy_, False)
                else bstack1l11l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠦዜ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1llllll111l_opy_.bstack1111ll111l_opy_(driver, bstack1llllll111l_opy_.bstack1l1llll111l_opy_, bstack1l11l_opy_ (u"ࠨࠢዝ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1llllll111l_opy_.bstack1111ll111l_opy_(driver, bstack1llllll111l_opy_.bstack1l1llll1l1l_opy_, bstack1l11l_opy_ (u"ࠢࠣዞ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1ll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs
    ):
        bstack1ll111llll1_opy_ = f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll11l111ll_opy_, [])
        if not bstack1ll111llll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦዟ") + str(kwargs) + bstack1l11l_opy_ (u"ࠤࠥዠ"))
            return {}
        if len(bstack1ll111llll1_opy_) > 1:
            self.logger.debug(bstack1l11l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨዡ") + str(kwargs) + bstack1l11l_opy_ (u"ࠦࠧዢ"))
            return {}
        bstack1ll1111l11l_opy_, bstack1ll111111l1_opy_ = bstack1ll111llll1_opy_[0]
        driver = bstack1ll1111l11l_opy_()
        if not driver:
            self.logger.debug(bstack1l11l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዣ") + str(kwargs) + bstack1l11l_opy_ (u"ࠨࠢዤ"))
            return {}
        capabilities = f.bstack1111ll111l_opy_(bstack1ll111111l1_opy_, bstack1llllll111l_opy_.bstack1l1llll1ll1_opy_)
        if not capabilities:
            self.logger.debug(bstack1l11l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዥ") + str(kwargs) + bstack1l11l_opy_ (u"ࠣࠤዦ"))
            return {}
        return capabilities.get(bstack1l11l_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢዧ"), {})
    def bstack1ll1ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs
    ):
        bstack1ll111llll1_opy_ = f.bstack1111ll111l_opy_(instance, bstack1llll11l1l1_opy_.bstack1ll11l111ll_opy_, [])
        if not bstack1ll111llll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨየ") + str(kwargs) + bstack1l11l_opy_ (u"ࠦࠧዩ"))
            return
        if len(bstack1ll111llll1_opy_) > 1:
            self.logger.debug(bstack1l11l_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣዪ") + str(kwargs) + bstack1l11l_opy_ (u"ࠨࠢያ"))
        bstack1ll1111l11l_opy_, bstack1ll111111l1_opy_ = bstack1ll111llll1_opy_[0]
        driver = bstack1ll1111l11l_opy_()
        if not driver:
            self.logger.debug(bstack1l11l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዬ") + str(kwargs) + bstack1l11l_opy_ (u"ࠣࠤይ"))
            return
        return driver