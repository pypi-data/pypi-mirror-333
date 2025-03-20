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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1111llll1l_opy_ import (
    bstack11111ll11l_opy_,
    bstack11111l1lll_opy_,
    bstack1111lll11l_opy_,
    bstack1111l1lll1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1111l1l1_opy_, bstack11l1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import bstack1llll11111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_, bstack1lllll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllllll11_opy_ import bstack111111l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111lll_opy_ import bstack1ll1l11ll1l_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l111l11ll_opy_ import bstack1l1ll1llll_opy_, bstack1l111l111_opy_, bstack1ll11ll1ll_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lllllll1l1_opy_(bstack1ll1l11ll1l_opy_):
    bstack1l1lll11l1l_opy_ = bstack11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣሇ")
    bstack1ll11llllll_opy_ = bstack11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤለ")
    bstack1l1ll1llll1_opy_ = bstack11_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨሉ")
    bstack1l1lll1111l_opy_ = bstack11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧሊ")
    bstack1l1lll111l1_opy_ = bstack11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥላ")
    bstack1ll11llll11_opy_ = bstack11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨሌ")
    bstack1l1lll1l11l_opy_ = bstack11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦል")
    bstack1l1lll11111_opy_ = bstack11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢሎ")
    def __init__(self):
        super().__init__(bstack1ll1l11llll_opy_=self.bstack1l1lll11l1l_opy_, frameworks=[bstack1llll11111l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1llllll1_opy_((bstack1lll1l11ll1_opy_.BEFORE_EACH, bstack111111l1ll_opy_.POST), self.bstack1l1lll11ll1_opy_)
        if bstack11l1ll11ll_opy_():
            TestFramework.bstack1ll1llllll1_opy_((bstack1lll1l11ll1_opy_.TEST, bstack111111l1ll_opy_.POST), self.bstack1lll1111ll1_opy_)
        else:
            TestFramework.bstack1ll1llllll1_opy_((bstack1lll1l11ll1_opy_.TEST, bstack111111l1ll_opy_.PRE), self.bstack1lll1111ll1_opy_)
        TestFramework.bstack1ll1llllll1_opy_((bstack1lll1l11ll1_opy_.TEST, bstack111111l1ll_opy_.POST), self.bstack1ll1lll11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll11ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1ll1lll1l_opy_ = self.bstack1l1lll11l11_opy_(instance.context)
        if not bstack1l1ll1lll1l_opy_:
            self.logger.debug(bstack11_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣሏ") + str(bstack1111l11l11_opy_) + bstack11_opy_ (u"ࠦࠧሐ"))
            return
        f.bstack1111lll1l1_opy_(instance, bstack1lllllll1l1_opy_.bstack1ll11llllll_opy_, bstack1l1ll1lll1l_opy_)
    def bstack1l1lll11l11_opy_(self, context: bstack1111l1lll1_opy_, bstack1l1ll1ll111_opy_= True):
        if bstack1l1ll1ll111_opy_:
            bstack1l1ll1lll1l_opy_ = self.bstack1ll1l11l111_opy_(context, reverse=True)
        else:
            bstack1l1ll1lll1l_opy_ = self.bstack1ll1l111l11_opy_(context, reverse=True)
        return [f for f in bstack1l1ll1lll1l_opy_ if f[1].state != bstack11111ll11l_opy_.QUIT]
    def bstack1lll1111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1lll11ll1_opy_(f, instance, bstack1111l11l11_opy_, *args, **kwargs)
        if not bstack1ll1111l1l1_opy_:
            self.logger.debug(bstack11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣሑ") + str(kwargs) + bstack11_opy_ (u"ࠨࠢሒ"))
            return
        bstack1l1ll1lll1l_opy_ = f.bstack11111lll1l_opy_(instance, bstack1lllllll1l1_opy_.bstack1ll11llllll_opy_, [])
        if not bstack1l1ll1lll1l_opy_:
            self.logger.debug(bstack11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥሓ") + str(kwargs) + bstack11_opy_ (u"ࠣࠤሔ"))
            return
        if len(bstack1l1ll1lll1l_opy_) > 1:
            self.logger.debug(
                bstack11111l1ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦሕ"))
        bstack1l1lll11lll_opy_, bstack1l1llllllll_opy_ = bstack1l1ll1lll1l_opy_[0]
        page = bstack1l1lll11lll_opy_()
        if not page:
            self.logger.debug(bstack11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥሖ") + str(kwargs) + bstack11_opy_ (u"ࠦࠧሗ"))
            return
        bstack1ll111llll_opy_ = getattr(args[0], bstack11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧመ"), None)
        try:
            page.evaluate(bstack11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢሙ"),
                        bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫሚ") + json.dumps(
                            bstack1ll111llll_opy_) + bstack11_opy_ (u"ࠣࡿࢀࠦማ"))
        except Exception as e:
            self.logger.debug(bstack11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢሜ"), e)
    def bstack1ll1lll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1lll11ll1_opy_(f, instance, bstack1111l11l11_opy_, *args, **kwargs)
        if not bstack1ll1111l1l1_opy_:
            self.logger.debug(bstack11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨም") + str(kwargs) + bstack11_opy_ (u"ࠦࠧሞ"))
            return
        bstack1l1ll1lll1l_opy_ = f.bstack11111lll1l_opy_(instance, bstack1lllllll1l1_opy_.bstack1ll11llllll_opy_, [])
        if not bstack1l1ll1lll1l_opy_:
            self.logger.debug(bstack11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣሟ") + str(kwargs) + bstack11_opy_ (u"ࠨࠢሠ"))
            return
        if len(bstack1l1ll1lll1l_opy_) > 1:
            self.logger.debug(
                bstack11111l1ll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤሡ"))
        bstack1l1lll11lll_opy_, bstack1l1llllllll_opy_ = bstack1l1ll1lll1l_opy_[0]
        page = bstack1l1lll11lll_opy_()
        if not page:
            self.logger.debug(bstack11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣሢ") + str(kwargs) + bstack11_opy_ (u"ࠤࠥሣ"))
            return
        status = f.bstack11111lll1l_opy_(instance, TestFramework.bstack1l1ll1ll1ll_opy_, None)
        if not status:
            self.logger.debug(bstack11_opy_ (u"ࠥࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨሤ") + str(bstack1111l11l11_opy_) + bstack11_opy_ (u"ࠦࠧሥ"))
            return
        bstack1l1ll1ll11l_opy_ = {bstack11_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧሦ"): status.lower()}
        bstack1l1lll1l111_opy_ = f.bstack11111lll1l_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_, None)
        if status.lower() == bstack11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ሧ") and bstack1l1lll1l111_opy_ is not None:
            bstack1l1ll1ll11l_opy_[bstack11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧረ")] = bstack1l1lll1l111_opy_[0][bstack11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫሩ")][0] if isinstance(bstack1l1lll1l111_opy_, list) else str(bstack1l1lll1l111_opy_)
        try:
              page.evaluate(
                    bstack11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥሪ"),
                    bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࠨራ")
                    + json.dumps(bstack1l1ll1ll11l_opy_)
                    + bstack11_opy_ (u"ࠦࢂࠨሬ")
                )
        except Exception as e:
            self.logger.debug(bstack11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧር"), e)
    def bstack1ll111llll1_opy_(
        self,
        instance: bstack1lllll1lll1_opy_,
        f: TestFramework,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1lll11ll1_opy_(f, instance, bstack1111l11l11_opy_, *args, **kwargs)
        if not bstack1ll1111l1l1_opy_:
            self.logger.debug(
                bstack11111l1ll1_opy_ (u"ࠨ࡭ࡢࡴ࡮ࡣࡴ࠷࠱ࡺࡡࡶࡽࡳࡩ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢሮ"))
            return
        bstack1l1ll1lll1l_opy_ = f.bstack11111lll1l_opy_(instance, bstack1lllllll1l1_opy_.bstack1ll11llllll_opy_, [])
        if not bstack1l1ll1lll1l_opy_:
            self.logger.debug(bstack11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥሯ") + str(kwargs) + bstack11_opy_ (u"ࠣࠤሰ"))
            return
        if len(bstack1l1ll1lll1l_opy_) > 1:
            self.logger.debug(
                bstack11111l1ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦሱ"))
        bstack1l1lll11lll_opy_, bstack1l1llllllll_opy_ = bstack1l1ll1lll1l_opy_[0]
        page = bstack1l1lll11lll_opy_()
        if not page:
            self.logger.debug(bstack11_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥሲ") + str(kwargs) + bstack11_opy_ (u"ࠦࠧሳ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥሴ") + str(timestamp)
        try:
            page.evaluate(
                bstack11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢስ"),
                bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬሶ").format(
                    json.dumps(
                        {
                            bstack11_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣሷ"): bstack11_opy_ (u"ࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦሸ"),
                            bstack11_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨሹ"): {
                                bstack11_opy_ (u"ࠦࡹࡿࡰࡦࠤሺ"): bstack11_opy_ (u"ࠧࡇ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠤሻ"),
                                bstack11_opy_ (u"ࠨࡤࡢࡶࡤࠦሼ"): data,
                                bstack11_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨሽ"): bstack11_opy_ (u"ࠣࡦࡨࡦࡺ࡭ࠢሾ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡵ࠱࠲ࡻࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡽࢀࠦሿ"), e)
    def bstack1ll11l1l1ll_opy_(
        self,
        instance: bstack1lllll1lll1_opy_,
        f: TestFramework,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1lll11ll1_opy_(f, instance, bstack1111l11l11_opy_, *args, **kwargs)
        if f.bstack11111lll1l_opy_(instance, bstack1lllllll1l1_opy_.bstack1ll11llll11_opy_, False):
            return
        self.bstack1ll1ll11lll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1llll111_opy_)
        req.test_framework_name = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1lll11111l1_opy_)
        req.test_framework_version = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll11lllll1_opy_)
        req.test_framework_state = bstack1111l11l11_opy_[0].name
        req.test_hook_state = bstack1111l11l11_opy_[1].name
        req.test_uuid = TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll1ll1l111_opy_)
        for bstack1l1lll111ll_opy_ in bstack111111l11l_opy_.bstack111l11111l_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤቀ")
                if bstack1ll1111l1l1_opy_
                else bstack11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥቁ")
            )
            session.ref = bstack1l1lll111ll_opy_.ref()
            session.hub_url = bstack111111l11l_opy_.bstack11111lll1l_opy_(bstack1l1lll111ll_opy_, bstack111111l11l_opy_.bstack1l1llll1ll1_opy_, bstack11_opy_ (u"ࠧࠨቂ"))
            session.framework_name = bstack1l1lll111ll_opy_.framework_name
            session.framework_version = bstack1l1lll111ll_opy_.framework_version
            session.framework_session_id = bstack111111l11l_opy_.bstack11111lll1l_opy_(bstack1l1lll111ll_opy_, bstack111111l11l_opy_.bstack1l1lll1l1ll_opy_, bstack11_opy_ (u"ࠨࠢቃ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1lll1111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll1lll1l_opy_ = f.bstack11111lll1l_opy_(instance, bstack1lllllll1l1_opy_.bstack1ll11llllll_opy_, [])
        if not bstack1l1ll1lll1l_opy_:
            self.logger.debug(bstack11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣቄ") + str(kwargs) + bstack11_opy_ (u"ࠣࠤቅ"))
            return
        if len(bstack1l1ll1lll1l_opy_) > 1:
            self.logger.debug(bstack11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥቆ") + str(kwargs) + bstack11_opy_ (u"ࠥࠦቇ"))
        bstack1l1lll11lll_opy_, bstack1l1llllllll_opy_ = bstack1l1ll1lll1l_opy_[0]
        page = bstack1l1lll11lll_opy_()
        if not page:
            self.logger.debug(bstack11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቈ") + str(kwargs) + bstack11_opy_ (u"ࠧࠨ቉"))
            return
        return page
    def bstack1ll1lll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1ll1lllll_opy_ = {}
        for bstack1l1lll111ll_opy_ in bstack111111l11l_opy_.bstack111l11111l_opy_.values():
            caps = bstack111111l11l_opy_.bstack11111lll1l_opy_(bstack1l1lll111ll_opy_, bstack111111l11l_opy_.bstack1l1llll11ll_opy_, bstack11_opy_ (u"ࠨࠢቊ"))
        bstack1l1ll1lllll_opy_[bstack11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧቋ")] = caps.get(bstack11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤቌ"), bstack11_opy_ (u"ࠤࠥቍ"))
        bstack1l1ll1lllll_opy_[bstack11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ቎")] = caps.get(bstack11_opy_ (u"ࠦࡴࡹࠢ቏"), bstack11_opy_ (u"ࠧࠨቐ"))
        bstack1l1ll1lllll_opy_[bstack11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣቑ")] = caps.get(bstack11_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦቒ"), bstack11_opy_ (u"ࠣࠤቓ"))
        bstack1l1ll1lllll_opy_[bstack11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥቔ")] = caps.get(bstack11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧቕ"), bstack11_opy_ (u"ࠦࠧቖ"))
        return bstack1l1ll1lllll_opy_
    def bstack1ll1ll1111l_opy_(self, page: object, bstack1ll1lll1lll_opy_, args={}):
        try:
            bstack1l1ll1lll11_opy_ = bstack11_opy_ (u"ࠧࠨࠢࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬ࠳࠴࠮ࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠩࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠴ࡰࡶࡵ࡫ࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡻࡧࡰࡢࡦࡴࡪࡹࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࡿࠬࠬࢀࡧࡲࡨࡡ࡭ࡷࡴࡴࡽࠪࠤࠥࠦ቗")
            bstack1ll1lll1lll_opy_ = bstack1ll1lll1lll_opy_.replace(bstack11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤቘ"), bstack11_opy_ (u"ࠢࡣࡵࡷࡥࡨࡱࡓࡥ࡭ࡄࡶ࡬ࡹࠢ቙"))
            script = bstack1l1ll1lll11_opy_.format(fn_body=bstack1ll1lll1lll_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11_opy_ (u"ࠣࡣ࠴࠵ࡾࡥࡳࡤࡴ࡬ࡴࡹࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡇࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸ࠱ࠦࠢቚ") + str(e) + bstack11_opy_ (u"ࠤࠥቛ"))