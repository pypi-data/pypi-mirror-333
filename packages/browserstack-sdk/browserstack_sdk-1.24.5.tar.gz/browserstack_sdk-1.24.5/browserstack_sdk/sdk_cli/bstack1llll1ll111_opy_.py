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
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1111l11ll1_opy_,
    bstack11111l1lll_opy_,
    bstack111l1111ll_opy_,
    bstack1111ll1111_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1111ll1l_opy_, bstack1lll1lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llllll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_, bstack1lllll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1lll1ll1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l1l_opy_ import bstack1ll1l111lll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack11l11111l_opy_ import bstack1l1lll1111_opy_, bstack1ll1ll1lll_opy_, bstack111ll11l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1lllllll11l_opy_(bstack1ll1l111lll_opy_):
    bstack1l1ll1ll1l1_opy_ = bstack1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢሆ")
    bstack1ll11l111ll_opy_ = bstack1l11l_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣሇ")
    bstack1l1ll1ll11l_opy_ = bstack1l11l_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧለ")
    bstack1l1lll11ll1_opy_ = bstack1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦሉ")
    bstack1l1ll1lll1l_opy_ = bstack1l11l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤሊ")
    bstack1ll111ll11l_opy_ = bstack1l11l_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧላ")
    bstack1l1lll11lll_opy_ = bstack1l11l_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥሌ")
    bstack1l1lll1l111_opy_ = bstack1l11l_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨል")
    def __init__(self):
        super().__init__(bstack1ll1l111l11_opy_=self.bstack1l1ll1ll1l1_opy_, frameworks=[bstack1llllll111l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1ll1l11l_opy_((bstack1lll11ll11l_opy_.BEFORE_EACH, bstack1llll11ll1l_opy_.POST), self.bstack1l1lll11l11_opy_)
        if bstack1lll1lll1l_opy_():
            TestFramework.bstack1ll1ll1l11l_opy_((bstack1lll11ll11l_opy_.TEST, bstack1llll11ll1l_opy_.POST), self.bstack1ll1llllll1_opy_)
        else:
            TestFramework.bstack1ll1ll1l11l_opy_((bstack1lll11ll11l_opy_.TEST, bstack1llll11ll1l_opy_.PRE), self.bstack1ll1llllll1_opy_)
        TestFramework.bstack1ll1ll1l11l_opy_((bstack1lll11ll11l_opy_.TEST, bstack1llll11ll1l_opy_.POST), self.bstack1lll111l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1lll111l1_opy_ = self.bstack1l1ll1llll1_opy_(instance.context)
        if not bstack1l1lll111l1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢሎ") + str(bstack11111lll1l_opy_) + bstack1l11l_opy_ (u"ࠥࠦሏ"))
            return
        f.bstack1111l1ll1l_opy_(instance, bstack1lllllll11l_opy_.bstack1ll11l111ll_opy_, bstack1l1lll111l1_opy_)
    def bstack1l1ll1llll1_opy_(self, context: bstack1111ll1111_opy_, bstack1l1lll11l1l_opy_= True):
        if bstack1l1lll11l1l_opy_:
            bstack1l1lll111l1_opy_ = self.bstack1ll1l111ll1_opy_(context, reverse=True)
        else:
            bstack1l1lll111l1_opy_ = self.bstack1ll1l11lll1_opy_(context, reverse=True)
        return [f for f in bstack1l1lll111l1_opy_ if f[1].state != bstack1111l11ll1_opy_.QUIT]
    def bstack1ll1llllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1lll11l11_opy_(f, instance, bstack11111lll1l_opy_, *args, **kwargs)
        if not bstack1ll1111ll1l_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢሐ") + str(kwargs) + bstack1l11l_opy_ (u"ࠧࠨሑ"))
            return
        bstack1l1lll111l1_opy_ = f.bstack1111ll111l_opy_(instance, bstack1lllllll11l_opy_.bstack1ll11l111ll_opy_, [])
        if not bstack1l1lll111l1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤሒ") + str(kwargs) + bstack1l11l_opy_ (u"ࠢࠣሓ"))
            return
        if len(bstack1l1lll111l1_opy_) > 1:
            self.logger.debug(
                bstack1lll1l1llll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥሔ"))
        bstack1l1lll1l11l_opy_, bstack1ll111111l1_opy_ = bstack1l1lll111l1_opy_[0]
        page = bstack1l1lll1l11l_opy_()
        if not page:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤሕ") + str(kwargs) + bstack1l11l_opy_ (u"ࠥࠦሖ"))
            return
        bstack1l11l1l1l_opy_ = getattr(args[0], bstack1l11l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦሗ"), None)
        try:
            page.evaluate(bstack1l11l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨመ"),
                        bstack1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪሙ") + json.dumps(
                            bstack1l11l1l1l_opy_) + bstack1l11l_opy_ (u"ࠢࡾࡿࠥሚ"))
        except Exception as e:
            self.logger.debug(bstack1l11l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨማ"), e)
    def bstack1lll111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1lll11l11_opy_(f, instance, bstack11111lll1l_opy_, *args, **kwargs)
        if not bstack1ll1111ll1l_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧሜ") + str(kwargs) + bstack1l11l_opy_ (u"ࠥࠦም"))
            return
        bstack1l1lll111l1_opy_ = f.bstack1111ll111l_opy_(instance, bstack1lllllll11l_opy_.bstack1ll11l111ll_opy_, [])
        if not bstack1l1lll111l1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢሞ") + str(kwargs) + bstack1l11l_opy_ (u"ࠧࠨሟ"))
            return
        if len(bstack1l1lll111l1_opy_) > 1:
            self.logger.debug(
                bstack1lll1l1llll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣሠ"))
        bstack1l1lll1l11l_opy_, bstack1ll111111l1_opy_ = bstack1l1lll111l1_opy_[0]
        page = bstack1l1lll1l11l_opy_()
        if not page:
            self.logger.debug(bstack1l11l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢሡ") + str(kwargs) + bstack1l11l_opy_ (u"ࠣࠤሢ"))
            return
        status = f.bstack1111ll111l_opy_(instance, TestFramework.bstack1l1lll1111l_opy_, None)
        if not status:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧሣ") + str(bstack11111lll1l_opy_) + bstack1l11l_opy_ (u"ࠥࠦሤ"))
            return
        bstack1l1ll1ll111_opy_ = {bstack1l11l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦሥ"): status.lower()}
        bstack1l1ll1lllll_opy_ = f.bstack1111ll111l_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_, None)
        if status.lower() == bstack1l11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬሦ") and bstack1l1ll1lllll_opy_ is not None:
            bstack1l1ll1ll111_opy_[bstack1l11l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ሧ")] = bstack1l1ll1lllll_opy_[0][bstack1l11l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪረ")][0] if isinstance(bstack1l1ll1lllll_opy_, list) else str(bstack1l1ll1lllll_opy_)
        try:
              page.evaluate(
                    bstack1l11l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤሩ"),
                    bstack1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࠧሪ")
                    + json.dumps(bstack1l1ll1ll111_opy_)
                    + bstack1l11l_opy_ (u"ࠥࢁࠧራ")
                )
        except Exception as e:
            self.logger.debug(bstack1l11l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠦሬ"), e)
    def bstack1ll11l11lll_opy_(
        self,
        instance: bstack1lllll1lll1_opy_,
        f: TestFramework,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1lll11l11_opy_(f, instance, bstack11111lll1l_opy_, *args, **kwargs)
        if not bstack1ll1111ll1l_opy_:
            self.logger.debug(
                bstack1lll1l1llll_opy_ (u"ࠧࡳࡡࡳ࡭ࡢࡳ࠶࠷ࡹࡠࡵࡼࡲࡨࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨር"))
            return
        bstack1l1lll111l1_opy_ = f.bstack1111ll111l_opy_(instance, bstack1lllllll11l_opy_.bstack1ll11l111ll_opy_, [])
        if not bstack1l1lll111l1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤሮ") + str(kwargs) + bstack1l11l_opy_ (u"ࠢࠣሯ"))
            return
        if len(bstack1l1lll111l1_opy_) > 1:
            self.logger.debug(
                bstack1lll1l1llll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥሰ"))
        bstack1l1lll1l11l_opy_, bstack1ll111111l1_opy_ = bstack1l1lll111l1_opy_[0]
        page = bstack1l1lll1l11l_opy_()
        if not page:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡰࡥࡷࡱ࡟ࡰ࠳࠴ࡽࡤࡹࡹ࡯ࡥ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤሱ") + str(kwargs) + bstack1l11l_opy_ (u"ࠥࠦሲ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l11l_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤሳ") + str(timestamp)
        try:
            page.evaluate(
                bstack1l11l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨሴ"),
                bstack1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫስ").format(
                    json.dumps(
                        {
                            bstack1l11l_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢሶ"): bstack1l11l_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥሷ"),
                            bstack1l11l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧሸ"): {
                                bstack1l11l_opy_ (u"ࠥࡸࡾࡶࡥࠣሹ"): bstack1l11l_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣሺ"),
                                bstack1l11l_opy_ (u"ࠧࡪࡡࡵࡣࠥሻ"): data,
                                bstack1l11l_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧሼ"): bstack1l11l_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨሽ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l11l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡴ࠷࠱ࡺࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡼࡿࠥሾ"), e)
    def bstack1ll111ll1ll_opy_(
        self,
        instance: bstack1lllll1lll1_opy_,
        f: TestFramework,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1lll11l11_opy_(f, instance, bstack11111lll1l_opy_, *args, **kwargs)
        if f.bstack1111ll111l_opy_(instance, bstack1lllllll11l_opy_.bstack1ll111ll11l_opy_, False):
            return
        self.bstack1ll1l1ll1ll_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll1ll1llll_opy_)
        req.test_framework_name = TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll1llll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll111lll11_opy_)
        req.test_framework_state = bstack11111lll1l_opy_[0].name
        req.test_hook_state = bstack11111lll1l_opy_[1].name
        req.test_uuid = TestFramework.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll1l1lll1l_opy_)
        for bstack1l1lll111ll_opy_ in bstack1lll1ll1111_opy_.bstack11111ll1l1_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l11l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣሿ")
                if bstack1ll1111ll1l_opy_
                else bstack1l11l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤቀ")
            )
            session.ref = bstack1l1lll111ll_opy_.ref()
            session.hub_url = bstack1lll1ll1111_opy_.bstack1111ll111l_opy_(bstack1l1lll111ll_opy_, bstack1lll1ll1111_opy_.bstack1l1llll111l_opy_, bstack1l11l_opy_ (u"ࠦࠧቁ"))
            session.framework_name = bstack1l1lll111ll_opy_.framework_name
            session.framework_version = bstack1l1lll111ll_opy_.framework_version
            session.framework_session_id = bstack1lll1ll1111_opy_.bstack1111ll111l_opy_(bstack1l1lll111ll_opy_, bstack1lll1ll1111_opy_.bstack1l1llll1l1l_opy_, bstack1l11l_opy_ (u"ࠧࠨቂ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll111l1_opy_ = f.bstack1111ll111l_opy_(instance, bstack1lllllll11l_opy_.bstack1ll11l111ll_opy_, [])
        if not bstack1l1lll111l1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢቃ") + str(kwargs) + bstack1l11l_opy_ (u"ࠢࠣቄ"))
            return
        if len(bstack1l1lll111l1_opy_) > 1:
            self.logger.debug(bstack1l11l_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤቅ") + str(kwargs) + bstack1l11l_opy_ (u"ࠤࠥቆ"))
        bstack1l1lll1l11l_opy_, bstack1ll111111l1_opy_ = bstack1l1lll111l1_opy_[0]
        page = bstack1l1lll1l11l_opy_()
        if not page:
            self.logger.debug(bstack1l11l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥቇ") + str(kwargs) + bstack1l11l_opy_ (u"ࠦࠧቈ"))
            return
        return page
    def bstack1ll1ll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1ll1ll1ll_opy_ = {}
        for bstack1l1lll111ll_opy_ in bstack1lll1ll1111_opy_.bstack11111ll1l1_opy_.values():
            caps = bstack1lll1ll1111_opy_.bstack1111ll111l_opy_(bstack1l1lll111ll_opy_, bstack1lll1ll1111_opy_.bstack1l1llll1ll1_opy_, bstack1l11l_opy_ (u"ࠧࠨ቉"))
        bstack1l1ll1ll1ll_opy_[bstack1l11l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦቊ")] = caps.get(bstack1l11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣቋ"), bstack1l11l_opy_ (u"ࠣࠤቌ"))
        bstack1l1ll1ll1ll_opy_[bstack1l11l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣቍ")] = caps.get(bstack1l11l_opy_ (u"ࠥࡳࡸࠨ቎"), bstack1l11l_opy_ (u"ࠦࠧ቏"))
        bstack1l1ll1ll1ll_opy_[bstack1l11l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢቐ")] = caps.get(bstack1l11l_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥቑ"), bstack1l11l_opy_ (u"ࠢࠣቒ"))
        bstack1l1ll1ll1ll_opy_[bstack1l11l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤቓ")] = caps.get(bstack1l11l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦቔ"), bstack1l11l_opy_ (u"ࠥࠦቕ"))
        return bstack1l1ll1ll1ll_opy_
    def bstack1ll1ll111l1_opy_(self, page: object, bstack1ll1ll1lll1_opy_, args={}):
        try:
            bstack1l1lll11111_opy_ = bstack1l11l_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡵࡷࡵࡲࠥࡴࡥࡸࠢࡓࡶࡴࡳࡩࡴࡧࠫࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠳ࡶࡵࡴࡪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢁࡦ࡯ࡡࡥࡳࡩࡿࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࡾࠫࠫࡿࡦࡸࡧࡠ࡬ࡶࡳࡳࢃࠩࠣࠤࠥቖ")
            bstack1ll1ll1lll1_opy_ = bstack1ll1ll1lll1_opy_.replace(bstack1l11l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ቗"), bstack1l11l_opy_ (u"ࠨࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸࠨቘ"))
            script = bstack1l1lll11111_opy_.format(fn_body=bstack1ll1ll1lll1_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l11l_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡹࡣࡳ࡫ࡳࡸࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡆࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷ࠰ࠥࠨ቙") + str(e) + bstack1l11l_opy_ (u"ࠣࠤቚ"))