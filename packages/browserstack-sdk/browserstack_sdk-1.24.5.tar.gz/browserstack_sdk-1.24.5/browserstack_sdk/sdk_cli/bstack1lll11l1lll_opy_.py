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
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1111l11ll1_opy_,
    bstack11111l1lll_opy_,
    bstack111l1111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llllll111l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1lll1ll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1llll1l1lll_opy_(bstack1lll1ll1l1l_opy_):
    bstack1lll1111lll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1llllll111l_opy_.bstack1ll1ll1l11l_opy_((bstack1111l11ll1_opy_.bstack111l111l11_opy_, bstack11111l1lll_opy_.PRE), self.bstack1ll1l1l11ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l1l11ll_opy_(
        self,
        f: bstack1llllll111l_opy_,
        driver: object,
        exec: Tuple[bstack111l1111ll_opy_, str],
        bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll1l1l111l_opy_(hub_url):
            if not bstack1llll1l1lll_opy_.bstack1lll1111lll_opy_:
                self.logger.warning(bstack1l11l_opy_ (u"ࠧࡲ࡯ࡤࡣ࡯ࠤࡸ࡫࡬ࡧ࠯࡫ࡩࡦࡲࠠࡧ࡮ࡲࡻࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᄸ") + str(hub_url) + bstack1l11l_opy_ (u"ࠨࠢᄹ"))
                bstack1llll1l1lll_opy_.bstack1lll1111lll_opy_ = True
            return
        bstack1ll1llll11l_opy_ = f.bstack1ll1lll1lll_opy_(*args)
        bstack1ll1l1l1l1l_opy_ = f.bstack1ll1l1l1ll1_opy_(*args)
        if bstack1ll1llll11l_opy_ and bstack1ll1llll11l_opy_.lower() == bstack1l11l_opy_ (u"ࠢࡧ࡫ࡱࡨࡪࡲࡥ࡮ࡧࡱࡸࠧᄺ") and bstack1ll1l1l1l1l_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1l1l1l1l_opy_.get(bstack1l11l_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢᄻ"), None), bstack1ll1l1l1l1l_opy_.get(bstack1l11l_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᄼ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l11l_opy_ (u"ࠥࡿࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࢀ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡶࡵ࡬ࡲ࡬ࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡸࡤࡰࡺ࡫࠽ࠣᄽ") + str(locator_value) + bstack1l11l_opy_ (u"ࠦࠧᄾ"))
                return
            def bstack111l11111l_opy_(driver, bstack1ll1l1l1111_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll1l1l1111_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll1l1ll111_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l11l_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣᄿ") + str(locator_value) + bstack1l11l_opy_ (u"ࠨࠢᅀ"))
                    else:
                        self.logger.warning(bstack1l11l_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᅁ") + str(response) + bstack1l11l_opy_ (u"ࠣࠤᅂ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll1l1l1l11_opy_(
                        driver, bstack1ll1l1l1111_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack111l11111l_opy_.__name__ = bstack1ll1llll11l_opy_
            return bstack111l11111l_opy_
    def __1ll1l1l1l11_opy_(
        self,
        driver,
        bstack1ll1l1l1111_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll1l1ll111_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l11l_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡹࡸࡩࡨࡩࡨࡶࡪࡪ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᅃ") + str(locator_value) + bstack1l11l_opy_ (u"ࠥࠦᅄ"))
                bstack1ll1l1l11l1_opy_ = self.bstack1ll1l1l1lll_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢ࡫ࡩࡦࡲࡩ࡯ࡩࡢࡶࡪࡹࡵ࡭ࡶࡀࠦᅅ") + str(bstack1ll1l1l11l1_opy_) + bstack1l11l_opy_ (u"ࠧࠨᅆ"))
                if bstack1ll1l1l11l1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l11l_opy_ (u"ࠨࡵࡴ࡫ࡱ࡫ࠧᅇ"): bstack1ll1l1l11l1_opy_.locator_type,
                            bstack1l11l_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᅈ"): bstack1ll1l1l11l1_opy_.locator_value,
                        }
                    )
                    return bstack1ll1l1l1111_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l11l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡋࡢࡈࡊࡈࡕࡈࠤᅉ"), False):
                    self.logger.info(bstack1lll1l1llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠱ࡲ࡯ࡳࡴ࡫ࡱ࡫࠿ࠦࡳ࡭ࡧࡨࡴ࠭࠹࠰ࠪࠢ࡯ࡩࡹࡺࡩ࡯ࡩࠣࡽࡴࡻࠠࡪࡰࡶࡴࡪࡩࡴࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢ࡯ࡳ࡬ࡹࠢᅊ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l11l_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᅋ") + str(response) + bstack1l11l_opy_ (u"ࠦࠧᅌ"))
        except Exception as err:
            self.logger.warning(bstack1l11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡࡧࡵࡶࡴࡸ࠺ࠡࠤᅍ") + str(err) + bstack1l11l_opy_ (u"ࠨࠢᅎ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll1l1ll1l1_opy_, stage=STAGE.bstack1111111l_opy_)
    def bstack1ll1l1ll111_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l11l_opy_ (u"ࠢ࠱ࠤᅏ"),
    ):
        self.bstack1ll1l1ll1ll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l11l_opy_ (u"ࠣࠤᅐ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1llllll1l11_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l11l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᅑ") + str(r) + bstack1l11l_opy_ (u"ࠥࠦᅒ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᅓ") + str(e) + bstack1l11l_opy_ (u"ࠧࠨᅔ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1l1ll11l_opy_, stage=STAGE.bstack1111111l_opy_)
    def bstack1ll1l1l1lll_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l11l_opy_ (u"ࠨ࠰ࠣᅕ")):
        self.bstack1ll1l1ll1ll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1llllll1l11_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l11l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᅖ") + str(r) + bstack1l11l_opy_ (u"ࠣࠤᅗ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᅘ") + str(e) + bstack1l11l_opy_ (u"ࠥࠦᅙ"))
            traceback.print_exc()
            raise e