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
from browserstack_sdk.sdk_cli.bstack1llll111lll_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1111llll1l_opy_ import (
    bstack11111ll11l_opy_,
    bstack11111l1lll_opy_,
    bstack1111lll11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import bstack1llll11111l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll111lll_opy_ import bstack1lll11l1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lllllllll1_opy_(bstack1lll11l1lll_opy_):
    bstack1ll1l1lll11_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1llll11111l_opy_.bstack1ll1llllll1_opy_((bstack11111ll11l_opy_.bstack1111ll1l1l_opy_, bstack11111l1lll_opy_.PRE), self.bstack1ll1l1l1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l1l1l1l_opy_(
        self,
        f: bstack1llll11111l_opy_,
        driver: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll1l1l1111_opy_(hub_url):
            if not bstack1lllllllll1_opy_.bstack1ll1l1lll11_opy_:
                self.logger.warning(bstack11_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࠥࡹࡥ࡭ࡨ࠰࡬ࡪࡧ࡬ࠡࡨ࡯ࡳࡼࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡮ࡴࡦࡳࡣࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᄹ") + str(hub_url) + bstack11_opy_ (u"ࠢࠣᄺ"))
                bstack1lllllllll1_opy_.bstack1ll1l1lll11_opy_ = True
            return
        bstack1ll1l1lllll_opy_ = f.bstack1lll1111l11_opy_(*args)
        bstack1ll1l1ll111_opy_ = f.bstack1ll1l1l1lll_opy_(*args)
        if bstack1ll1l1lllll_opy_ and bstack1ll1l1lllll_opy_.lower() == bstack11_opy_ (u"ࠣࡨ࡬ࡲࡩ࡫࡬ࡦ࡯ࡨࡲࡹࠨᄻ") and bstack1ll1l1ll111_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1l1ll111_opy_.get(bstack11_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᄼ"), None), bstack1ll1l1ll111_opy_.get(bstack11_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᄽ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11_opy_ (u"ࠦࢀࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡷࡶ࡭ࡳ࡭࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡹࡥࡱࡻࡥ࠾ࠤᄾ") + str(locator_value) + bstack11_opy_ (u"ࠧࠨᄿ"))
                return
            def bstack1111ll11ll_opy_(driver, bstack1ll1l1l11l1_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll1l1l11l1_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll1l1l111l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᅀ") + str(locator_value) + bstack11_opy_ (u"ࠢࠣᅁ"))
                    else:
                        self.logger.warning(bstack11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦᅂ") + str(response) + bstack11_opy_ (u"ࠤࠥᅃ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll1l1ll1l1_opy_(
                        driver, bstack1ll1l1l11l1_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1111ll11ll_opy_.__name__ = bstack1ll1l1lllll_opy_
            return bstack1111ll11ll_opy_
    def __1ll1l1ll1l1_opy_(
        self,
        driver,
        bstack1ll1l1l11l1_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll1l1l111l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡺࡲࡪࡩࡪࡩࡷ࡫ࡤ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥᅄ") + str(locator_value) + bstack11_opy_ (u"ࠦࠧᅅ"))
                bstack1ll1l1ll11l_opy_ = self.bstack1ll1l1l1ll1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣ࡬ࡪࡧ࡬ࡪࡰࡪࡣࡷ࡫ࡳࡶ࡮ࡷࡁࠧᅆ") + str(bstack1ll1l1ll11l_opy_) + bstack11_opy_ (u"ࠨࠢᅇ"))
                if bstack1ll1l1ll11l_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨᅈ"): bstack1ll1l1ll11l_opy_.locator_type,
                            bstack11_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᅉ"): bstack1ll1l1ll11l_opy_.locator_value,
                        }
                    )
                    return bstack1ll1l1l11l1_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡌࡣࡉࡋࡂࡖࡉࠥᅊ"), False):
                    self.logger.info(bstack11111l1ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠲ࡳࡩࡴࡵ࡬ࡲ࡬ࡀࠠࡴ࡮ࡨࡩࡵ࠮࠳࠱ࠫࠣࡰࡪࡺࡴࡪࡰࡪࠤࡾࡵࡵࠡ࡫ࡱࡷࡵ࡫ࡣࡵࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡦࡺࡷࡩࡳࡹࡩࡰࡰࠣࡰࡴ࡭ࡳࠣᅋ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢᅌ") + str(response) + bstack11_opy_ (u"ࠧࠨᅍ"))
        except Exception as err:
            self.logger.warning(bstack11_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥᅎ") + str(err) + bstack11_opy_ (u"ࠢࠣᅏ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll1l1l1l11_opy_, stage=STAGE.bstack1lll11111l_opy_)
    def bstack1ll1l1l111l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11_opy_ (u"ࠣ࠲ࠥᅐ"),
    ):
        self.bstack1ll1ll11lll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11_opy_ (u"ࠤࠥᅑ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack11111l11ll_opy_.AISelfHealStep(req)
            self.logger.info(bstack11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᅒ") + str(r) + bstack11_opy_ (u"ࠦࠧᅓ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᅔ") + str(e) + bstack11_opy_ (u"ࠨࠢᅕ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1l1l11ll_opy_, stage=STAGE.bstack1lll11111l_opy_)
    def bstack1ll1l1l1ll1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11_opy_ (u"ࠢ࠱ࠤᅖ")):
        self.bstack1ll1ll11lll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack11111l11ll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᅗ") + str(r) + bstack11_opy_ (u"ࠤࠥᅘ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᅙ") + str(e) + bstack11_opy_ (u"ࠦࠧᅚ"))
            traceback.print_exc()
            raise e