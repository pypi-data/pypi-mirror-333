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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1111l11ll1_opy_,
    bstack11111l1lll_opy_,
    bstack1111lllll1_opy_,
    bstack111l1111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llllll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_, bstack1lllll1lll1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l111_opy_ import bstack1llll11l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll111_opy_ import bstack1lllllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1lll1ll1111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll1l1lll1_opy_ import bstack1lll1ll1l11_opy_
import grpc
import traceback
import json
class bstack1llllll11ll_opy_(bstack1lll1ll1l1l_opy_):
    bstack1lll1111lll_opy_ = False
    bstack1ll1ll1l1ll_opy_ = bstack1l11l_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵࠦႴ")
    bstack1ll1l1lll11_opy_ = bstack1l11l_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥႵ")
    bstack1ll1lll1l11_opy_ = bstack1l11l_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡱ࡭ࡹࠨႶ")
    bstack1lll111lll1_opy_ = bstack1l11l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡷࡤࡹࡣࡢࡰࡱ࡭ࡳ࡭ࠢႷ")
    bstack1ll1lll11ll_opy_ = bstack1l11l_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢ࡬ࡦࡹ࡟ࡶࡴ࡯ࠦႸ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1lll1ll11l1_opy_, bstack1lll1l11l11_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll1ll1111l_opy_ = bstack1lll1l11l11_opy_
        bstack1lll1ll11l1_opy_.bstack1ll1ll1l11l_opy_((bstack1111l11ll1_opy_.bstack111l111l11_opy_, bstack11111l1lll_opy_.PRE), self.bstack1ll1ll1ll1l_opy_)
        TestFramework.bstack1ll1ll1l11l_opy_((bstack1lll11ll11l_opy_.TEST, bstack1llll11ll1l_opy_.PRE), self.bstack1ll1llllll1_opy_)
        TestFramework.bstack1ll1ll1l11l_opy_((bstack1lll11ll11l_opy_.TEST, bstack1llll11ll1l_opy_.POST), self.bstack1lll111l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1llllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1lll1111_opy_(instance, args)
        test_framework = f.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll1llll1l1_opy_)
        if bstack1l11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨႹ") in instance.bstack1ll1ll1l1l1_opy_:
            platform_index = f.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll1ll1llll_opy_)
            self.accessibility = self.bstack1l1111l111_opy_(tags) and self.bstack1ll1lll1_opy_(self.config[bstack1l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨႺ")][platform_index])
        else:
            capabilities = self.bstack1ll1ll1111l_opy_.bstack1ll1ll1l111_opy_(f, instance, bstack11111lll1l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l11l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨႻ") + str(kwargs) + bstack1l11l_opy_ (u"ࠢࠣႼ"))
                return
            self.accessibility = self.bstack1l1111l111_opy_(tags) and self.bstack1ll1lll1_opy_(capabilities)
        if self.bstack1ll1ll1111l_opy_.pages and self.bstack1ll1ll1111l_opy_.pages.values():
            bstack1ll1lll1l1l_opy_ = list(self.bstack1ll1ll1111l_opy_.pages.values())
            if bstack1ll1lll1l1l_opy_ and isinstance(bstack1ll1lll1l1l_opy_[0], (list, tuple)) and bstack1ll1lll1l1l_opy_[0]:
                bstack1ll1l1llll1_opy_ = bstack1ll1lll1l1l_opy_[0][0]
                if callable(bstack1ll1l1llll1_opy_):
                    page = bstack1ll1l1llll1_opy_()
                    def bstack11l1l111_opy_():
                        self.get_accessibility_results(page, bstack1l11l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧႽ"))
                    def bstack1lll1111111_opy_():
                        self.get_accessibility_results_summary(page, bstack1l11l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨႾ"))
                    setattr(page, bstack1l11l_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡸࠨႿ"), bstack11l1l111_opy_)
                    setattr(page, bstack1l11l_opy_ (u"ࠦ࡬࡫ࡴࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡒࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨჀ"), bstack1lll1111111_opy_)
        self.logger.debug(bstack1l11l_opy_ (u"ࠧࡹࡨࡰࡷ࡯ࡨࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡹࡥࡱࡻࡥ࠾ࠤჁ") + str(self.accessibility) + bstack1l11l_opy_ (u"ࠨࠢჂ"))
    def bstack1ll1ll1ll1l_opy_(
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
            bstack1ll11ll11l_opy_ = datetime.now()
            self.bstack1ll1ll111ll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l1lll11ll_opy_(bstack1l11l_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥჃ"), datetime.now() - bstack1ll11ll11l_opy_)
            if (
                not f.bstack1ll1llll111_opy_(method_name)
                or f.bstack1ll1l1lllll_opy_(method_name, *args)
                or f.bstack1ll1ll11l1l_opy_(method_name, *args)
            ):
                return
            if not f.bstack1111ll111l_opy_(instance, bstack1llllll11ll_opy_.bstack1ll1lll1l11_opy_, False):
                if not bstack1llllll11ll_opy_.bstack1lll1111lll_opy_:
                    self.logger.warning(bstack1l11l_opy_ (u"ࠣ࡝ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦჄ") + str(f.platform_index) + bstack1l11l_opy_ (u"ࠤࡠࠤࡦ࠷࠱ࡺࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡪࡤࡺࡪࠦ࡮ࡰࡶࠣࡦࡪ࡫࡮ࠡࡵࡨࡸࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣჅ"))
                    bstack1llllll11ll_opy_.bstack1lll1111lll_opy_ = True
                return
            bstack1ll1lllllll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1lllllll_opy_:
                platform_index = f.bstack1111ll111l_opy_(instance, bstack1llllll111l_opy_.bstack1ll1ll1llll_opy_, 0)
                self.logger.debug(bstack1l11l_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣ჆") + str(f.framework_name) + bstack1l11l_opy_ (u"ࠦࠧჇ"))
                return
            bstack1ll1llll11l_opy_ = f.bstack1ll1lll1lll_opy_(*args)
            if not bstack1ll1llll11l_opy_:
                self.logger.debug(bstack1l11l_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࠢ჈") + str(method_name) + bstack1l11l_opy_ (u"ࠨࠢ჉"))
                return
            bstack1lll111111l_opy_ = f.bstack1111ll111l_opy_(instance, bstack1llllll11ll_opy_.bstack1ll1lll11ll_opy_, False)
            if bstack1ll1llll11l_opy_ == bstack1l11l_opy_ (u"ࠢࡨࡧࡷࠦ჊") and not bstack1lll111111l_opy_:
                f.bstack1111l1ll1l_opy_(instance, bstack1llllll11ll_opy_.bstack1ll1lll11ll_opy_, True)
            if not bstack1lll111111l_opy_:
                self.logger.debug(bstack1l11l_opy_ (u"ࠣࡰࡲࠤ࡚ࡘࡌࠡ࡮ࡲࡥࡩ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢ჋") + str(bstack1ll1llll11l_opy_) + bstack1l11l_opy_ (u"ࠤࠥ჌"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1llll11l_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l11l_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣჍ") + str(bstack1ll1llll11l_opy_) + bstack1l11l_opy_ (u"ࠦࠧ჎"))
                return
            self.logger.info(bstack1l11l_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡸࡩࡲࡪࡲࡷࡷࡤࡺ࡯ࡠࡴࡸࡲ࠮ࢃࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢ჏") + str(bstack1ll1llll11l_opy_) + bstack1l11l_opy_ (u"ࠨࠢა"))
            scripts = [(s, bstack1ll1lllllll_opy_[s]) for s in scripts_to_run if s in bstack1ll1lllllll_opy_]
            for bstack1ll1lllll1l_opy_, bstack1ll1ll1lll1_opy_ in scripts:
                try:
                    bstack1ll11ll11l_opy_ = datetime.now()
                    if bstack1ll1lllll1l_opy_ == bstack1l11l_opy_ (u"ࠢࡴࡥࡤࡲࠧბ"):
                        result = self.perform_scan(driver, method=bstack1ll1llll11l_opy_, framework_name=f.framework_name)
                    instance.bstack1l1lll11ll_opy_(bstack1l11l_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࠢგ") + bstack1ll1lllll1l_opy_, datetime.now() - bstack1ll11ll11l_opy_)
                    if isinstance(result, dict) and not result.get(bstack1l11l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥდ"), True):
                        self.logger.warning(bstack1l11l_opy_ (u"ࠥࡷࡰ࡯ࡰࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡷ࡫࡭ࡢ࡫ࡱ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺࡳ࠻ࠢࠥე") + str(result) + bstack1l11l_opy_ (u"ࠦࠧვ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1l11l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺ࠽ࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃࠠࡦࡴࡵࡳࡷࡃࠢზ") + str(e) + bstack1l11l_opy_ (u"ࠨࠢთ"))
        except Exception as e:
            self.logger.error(bstack1l11l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡪࡸࡲࡰࡴࡀࠦი") + str(e) + bstack1l11l_opy_ (u"ࠣࠤკ"))
    def bstack1lll111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        if not self.accessibility:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨლ"))
            return
        driver = self.bstack1ll1ll1111l_opy_.bstack1ll1ll1ll11_opy_(f, instance, bstack11111lll1l_opy_, *args, **kwargs)
        test_name = f.bstack1111ll111l_opy_(instance, TestFramework.bstack1lll111ll11_opy_)
        if not test_name:
            self.logger.debug(bstack1l11l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣმ"))
            return
        test_uuid = f.bstack1111ll111l_opy_(instance, TestFramework.bstack1ll1l1lll1l_opy_)
        if not test_uuid:
            self.logger.debug(bstack1l11l_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤნ"))
            return
        if isinstance(self.bstack1ll1ll1111l_opy_, bstack1lllllll11l_opy_):
            framework_name = bstack1l11l_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩო")
        else:
            framework_name = bstack1l11l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨპ")
        self.bstack1l11l1l1_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll1ll11111_opy_ = bstack1lll1ll1l11_opy_.bstack1lll111l1ll_opy_(EVENTS.bstack1lll1l1ll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1l11l_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࠣჟ"))
            return
        bstack1ll11ll11l_opy_ = datetime.now()
        bstack1ll1ll1lll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l11l_opy_ (u"ࠣࡵࡦࡥࡳࠨრ"), None)
        if not bstack1ll1ll1lll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡩࡡ࡯ࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤს") + str(framework_name) + bstack1l11l_opy_ (u"ࠥࠤࠧტ"))
            return
        instance = bstack1111lllll1_opy_.bstack1111l1llll_opy_(driver)
        if instance:
            if not bstack1111lllll1_opy_.bstack1111ll111l_opy_(instance, bstack1llllll11ll_opy_.bstack1lll111lll1_opy_, False):
                bstack1111lllll1_opy_.bstack1111l1ll1l_opy_(instance, bstack1llllll11ll_opy_.bstack1lll111lll1_opy_, True)
            else:
                self.logger.info(bstack1l11l_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡮ࠡࡲࡵࡳ࡬ࡸࡥࡴࡵࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࠽ࠣუ") + str(method) + bstack1l11l_opy_ (u"ࠧࠨფ"))
                return
        self.logger.info(bstack1l11l_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦქ") + str(method) + bstack1l11l_opy_ (u"ࠢࠣღ"))
        if framework_name == bstack1l11l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬყ"):
            result = self.bstack1ll1ll1111l_opy_.bstack1ll1ll111l1_opy_(driver, bstack1ll1ll1lll1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll1lll1_opy_, {bstack1l11l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤშ"): method if method else bstack1l11l_opy_ (u"ࠥࠦჩ")})
        bstack1lll1ll1l11_opy_.end(EVENTS.bstack1lll1l1ll_opy_.value, bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦც"), bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥძ"), True, None, command=method)
        if instance:
            bstack1111lllll1_opy_.bstack1111l1ll1l_opy_(instance, bstack1llllll11ll_opy_.bstack1lll111lll1_opy_, False)
            instance.bstack1l1lll11ll_opy_(bstack1l11l_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾ࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰࠥწ"), datetime.now() - bstack1ll11ll11l_opy_)
        return result
    @measure(event_name=EVENTS.bstack11111l11_opy_, stage=STAGE.bstack1111111l_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l11l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤჭ"))
            return
        bstack1ll1ll1lll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l11l_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧხ"), None)
        if not bstack1ll1ll1lll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣჯ") + str(framework_name) + bstack1l11l_opy_ (u"ࠥࠦჰ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll11ll11l_opy_ = datetime.now()
        if framework_name == bstack1l11l_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨჱ"):
            result = self.bstack1ll1ll1111l_opy_.bstack1ll1ll111l1_opy_(driver, bstack1ll1ll1lll1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll1lll1_opy_)
        instance = bstack1111lllll1_opy_.bstack1111l1llll_opy_(driver)
        if instance:
            instance.bstack1l1lll11ll_opy_(bstack1l11l_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࠣჲ"), datetime.now() - bstack1ll11ll11l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1llll1l1_opy_, stage=STAGE.bstack1111111l_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l11l_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤჳ"))
            return
        bstack1ll1ll1lll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l11l_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦჴ"), None)
        if not bstack1ll1ll1lll1_opy_:
            self.logger.debug(bstack1l11l_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢჵ") + str(framework_name) + bstack1l11l_opy_ (u"ࠤࠥჶ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll11ll11l_opy_ = datetime.now()
        if framework_name == bstack1l11l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧჷ"):
            result = self.bstack1ll1ll1111l_opy_.bstack1ll1ll111l1_opy_(driver, bstack1ll1ll1lll1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1ll1lll1_opy_)
        instance = bstack1111lllll1_opy_.bstack1111l1llll_opy_(driver)
        if instance:
            instance.bstack1l1lll11ll_opy_(bstack1l11l_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹࠣჸ"), datetime.now() - bstack1ll11ll11l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1lll111l111_opy_, stage=STAGE.bstack1111111l_opy_)
    def bstack1ll1lll1ll1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll1l1ll1ll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1llllll1l11_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l11l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢჹ") + str(r) + bstack1l11l_opy_ (u"ࠨࠢჺ"))
            else:
                self.bstack1ll1lll11l1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ჻") + str(e) + bstack1l11l_opy_ (u"ࠣࠤჼ"))
            traceback.print_exc()
            raise e
    def bstack1ll1lll11l1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l11l_opy_ (u"ࠤ࡯ࡳࡦࡪ࡟ࡤࡱࡱࡪ࡮࡭࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤჽ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1lll1111ll1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1ll1l1ll_opy_ and command.module == self.bstack1ll1l1lll11_opy_:
                        if command.method and not command.method in bstack1lll1111ll1_opy_:
                            bstack1lll1111ll1_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1lll1111ll1_opy_[command.method]:
                            bstack1lll1111ll1_opy_[command.method][command.name] = list()
                        bstack1lll1111ll1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1lll1111ll1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1ll111ll_opy_(
        self,
        f: bstack1llllll111l_opy_,
        exec: Tuple[bstack111l1111ll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll1ll1111l_opy_, bstack1lllllll11l_opy_) and method_name != bstack1l11l_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫჾ"):
            return
        if bstack1111lllll1_opy_.bstack111l111l1l_opy_(instance, bstack1llllll11ll_opy_.bstack1ll1lll1l11_opy_):
            return
        if not f.bstack1lll11111ll_opy_(instance):
            if not bstack1llllll11ll_opy_.bstack1lll1111lll_opy_:
                self.logger.warning(bstack1l11l_opy_ (u"ࠦࡦ࠷࠱ࡺࠢࡩࡰࡴࡽࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦ࡮ࡰࡰ࠰ࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠣჿ"))
                bstack1llllll11ll_opy_.bstack1lll1111lll_opy_ = True
            return
        if f.bstack1lll1111l1l_opy_(method_name, *args):
            bstack1ll1ll11ll1_opy_ = False
            desired_capabilities = f.bstack1lll11111l1_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1lll1111l11_opy_(instance)
                platform_index = f.bstack1111ll111l_opy_(instance, bstack1llllll111l_opy_.bstack1ll1ll1llll_opy_, 0)
                bstack1ll1ll11l11_opy_ = datetime.now()
                r = self.bstack1ll1lll1ll1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1l1lll11ll_opy_(bstack1l11l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᄀ"), datetime.now() - bstack1ll1ll11l11_opy_)
                bstack1ll1ll11ll1_opy_ = r.success
            else:
                self.logger.error(bstack1l11l_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡥࡧࡶ࡭ࡷ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠽ࠣᄁ") + str(desired_capabilities) + bstack1l11l_opy_ (u"ࠢࠣᄂ"))
            f.bstack1111l1ll1l_opy_(instance, bstack1llllll11ll_opy_.bstack1ll1lll1l11_opy_, bstack1ll1ll11ll1_opy_)
    def bstack1l1111l111_opy_(self, test_tags):
        bstack1ll1lll1ll1_opy_ = self.config.get(bstack1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᄃ"))
        if not bstack1ll1lll1ll1_opy_:
            return True
        try:
            include_tags = bstack1ll1lll1ll1_opy_[bstack1l11l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᄄ")] if bstack1l11l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᄅ") in bstack1ll1lll1ll1_opy_ and isinstance(bstack1ll1lll1ll1_opy_[bstack1l11l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᄆ")], list) else []
            exclude_tags = bstack1ll1lll1ll1_opy_[bstack1l11l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᄇ")] if bstack1l11l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᄈ") in bstack1ll1lll1ll1_opy_ and isinstance(bstack1ll1lll1ll1_opy_[bstack1l11l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᄉ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l11l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣᄊ") + str(error))
        return False
    def bstack1ll1lll1_opy_(self, caps):
        try:
            bstack1ll1lll111l_opy_ = caps.get(bstack1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᄋ"), {}).get(bstack1l11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᄌ"), caps.get(bstack1l11l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᄍ"), bstack1l11l_opy_ (u"ࠬ࠭ᄎ")))
            if bstack1ll1lll111l_opy_:
                self.logger.warning(bstack1l11l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᄏ"))
                return False
            browser = caps.get(bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᄐ"), bstack1l11l_opy_ (u"ࠨࠩᄑ")).lower()
            if browser != bstack1l11l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᄒ"):
                self.logger.warning(bstack1l11l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᄓ"))
                return False
            browser_version = caps.get(bstack1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᄔ"))
            if browser_version and browser_version != bstack1l11l_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᄕ") and int(browser_version.split(bstack1l11l_opy_ (u"࠭࠮ࠨᄖ"))[0]) <= 98:
                self.logger.warning(bstack1l11l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠻࠲ࠧᄗ"))
                return False
            bstack1lll111ll1l_opy_ = caps.get(bstack1l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᄘ"), {}).get(bstack1l11l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᄙ"))
            if bstack1lll111ll1l_opy_ and bstack1l11l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᄚ") in bstack1lll111ll1l_opy_.get(bstack1l11l_opy_ (u"ࠫࡦࡸࡧࡴࠩᄛ"), []):
                self.logger.warning(bstack1l11l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᄜ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣᄝ") + str(error))
            return False
    def bstack1l11l1l1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll1ll11111_opy_ = None
        try:
            bstack1ll1lllll11_opy_ = {
                bstack1l11l_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᄞ"): test_uuid,
                bstack1l11l_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᄟ"): os.environ.get(bstack1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᄠ"), bstack1l11l_opy_ (u"ࠪࠫᄡ")),
                bstack1l11l_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨᄢ"): os.environ.get(bstack1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᄣ"), bstack1l11l_opy_ (u"࠭ࠧᄤ"))
            }
            self.logger.debug(bstack1l11l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᄥ") + str(bstack1ll1lllll11_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            bstack1ll1ll1lll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l11l_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᄦ"), None)
            if not bstack1ll1ll1lll1_opy_:
                self.logger.debug(bstack1l11l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᄧ") + str(framework_name) + bstack1l11l_opy_ (u"ࠥࠤࠧᄨ"))
                return
            bstack1ll1ll11111_opy_ = bstack1lll1ll1l11_opy_.bstack1lll111l1ll_opy_(EVENTS.bstack1ll1ll11lll_opy_.value)
            self.bstack1ll1llll1ll_opy_(driver, bstack1ll1ll1lll1_opy_, bstack1ll1lllll11_opy_, framework_name)
            self.logger.info(bstack1l11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᄩ"))
            bstack1lll1ll1l11_opy_.end(EVENTS.bstack1ll1ll11lll_opy_.value, bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᄪ"), bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᄫ"), True, None, command=bstack1l11l_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᄬ"),test_name=name)
        except Exception as bstack1lll111l11l_opy_:
            self.logger.error(bstack1l11l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᄭ") + bstack1l11l_opy_ (u"ࠤࡶࡸࡷ࠮ࡰࡢࡶ࡫࠭ࠧᄮ") + bstack1l11l_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧᄯ") + str(bstack1lll111l11l_opy_))
            bstack1lll1ll1l11_opy_.end(EVENTS.bstack1ll1ll11lll_opy_.value, bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᄰ"), bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᄱ"), False, bstack1lll111l11l_opy_, command=bstack1l11l_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᄲ"),test_name=name)
    def bstack1ll1llll1ll_opy_(self, driver, bstack1ll1ll1lll1_opy_, bstack1ll1lllll11_opy_, framework_name):
        if framework_name == bstack1l11l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᄳ"):
            self.bstack1ll1ll1111l_opy_.bstack1ll1ll111l1_opy_(driver, bstack1ll1ll1lll1_opy_, bstack1ll1lllll11_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1ll1lll1_opy_, bstack1ll1lllll11_opy_))
    def _1ll1lll1111_opy_(self, instance: bstack1lllll1lll1_opy_, args: Tuple) -> list:
        bstack1l11l_opy_ (u"ࠣࠤࠥࡉࡽࡺࡲࡢࡥࡷࠤࡹࡧࡧࡴࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࠥࠦࠧᄴ")
        if bstack1l11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᄵ") in instance.bstack1ll1ll1l1l1_opy_:
            return args[2].tags if hasattr(args[2], bstack1l11l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᄶ")) else []
        if hasattr(args[0], bstack1l11l_opy_ (u"ࠫࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠩᄷ")):
            return [marker.name for marker in args[0].own_markers]
        return []