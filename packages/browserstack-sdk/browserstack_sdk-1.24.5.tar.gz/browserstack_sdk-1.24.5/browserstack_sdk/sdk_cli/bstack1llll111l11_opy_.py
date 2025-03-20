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
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1111l11ll1_opy_,
    bstack11111l1lll_opy_,
    bstack111l1111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llllll111l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1111111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1ll1l1lll1_opy_ import bstack1lll1ll1l11_opy_
class bstack1lll1llllll_opy_(bstack1lll1ll1l1l_opy_):
    bstack1l1ll1111ll_opy_ = bstack1l11l_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤቛ")
    bstack1l1l1lllll1_opy_ = bstack1l11l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦቜ")
    bstack1l1ll1l1l1l_opy_ = bstack1l11l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦቝ")
    def __init__(self, bstack111111l111_opy_):
        super().__init__()
        bstack1llllll111l_opy_.bstack1ll1ll1l11l_opy_((bstack1111l11ll1_opy_.bstack1111ll11ll_opy_, bstack11111l1lll_opy_.PRE), self.bstack1l1l1llll1l_opy_)
        bstack1llllll111l_opy_.bstack1ll1ll1l11l_opy_((bstack1111l11ll1_opy_.bstack111l111l11_opy_, bstack11111l1lll_opy_.PRE), self.bstack1ll1l1l11ll_opy_)
        bstack1llllll111l_opy_.bstack1ll1ll1l11l_opy_((bstack1111l11ll1_opy_.bstack111l111l11_opy_, bstack11111l1lll_opy_.POST), self.bstack1l1ll1111l1_opy_)
        bstack1llllll111l_opy_.bstack1ll1ll1l11l_opy_((bstack1111l11ll1_opy_.bstack111l111l11_opy_, bstack11111l1lll_opy_.POST), self.bstack1l1ll111l1l_opy_)
        bstack1llllll111l_opy_.bstack1ll1ll1l11l_opy_((bstack1111l11ll1_opy_.QUIT, bstack11111l1lll_opy_.POST), self.bstack1l1l1llllll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1llll1l_opy_(
        self,
        f: bstack1llllll111l_opy_,
        driver: object,
        exec: Tuple[bstack111l1111ll_opy_, str],
        bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11l_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢ቞"):
            return
        def wrapped(driver, init, *args, **kwargs):
            self.bstack1l1ll1l1l11_opy_(instance, f, kwargs)
            self.logger.debug(bstack1l11l_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷ࠴ࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡨ࠱ࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁ࠿ࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ቟") + str(kwargs) + bstack1l11l_opy_ (u"ࠢࠣበ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
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
        instance, method_name = exec
        if f.bstack1111ll111l_opy_(instance, bstack1lll1llllll_opy_.bstack1l1ll1111ll_opy_, False):
            return
        if not f.bstack111l111l1l_opy_(instance, bstack1llllll111l_opy_.bstack1ll1ll1llll_opy_):
            return
        platform_index = f.bstack1111ll111l_opy_(instance, bstack1llllll111l_opy_.bstack1ll1ll1llll_opy_)
        if f.bstack1lll1111l1l_opy_(method_name, *args) and len(args) > 1:
            bstack1ll11ll11l_opy_ = datetime.now()
            hub_url = bstack1llllll111l_opy_.hub_url(driver)
            self.logger.warning(bstack1l11l_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭࠿ࠥቡ") + str(hub_url) + bstack1l11l_opy_ (u"ࠤࠥቢ"))
            bstack1l1ll11l111_opy_ = args[1][bstack1l11l_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤባ")] if isinstance(args[1], dict) and bstack1l11l_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥቤ") in args[1] else None
            bstack1l1ll11l11l_opy_ = bstack1l11l_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥብ")
            if isinstance(bstack1l1ll11l111_opy_, dict):
                bstack1ll11ll11l_opy_ = datetime.now()
                r = self.bstack1l1ll111ll1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1l1lll11ll_opy_(bstack1l11l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦቦ"), datetime.now() - bstack1ll11ll11l_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l11l_opy_ (u"ࠢࡴࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭࠺ࠡࠤቧ") + str(r) + bstack1l11l_opy_ (u"ࠣࠤቨ"))
                        return
                    if r.hub_url:
                        f.bstack1l1ll1l11ll_opy_(instance, driver, r.hub_url)
                        f.bstack1111l1ll1l_opy_(instance, bstack1lll1llllll_opy_.bstack1l1ll1111ll_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l11l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣቩ"), e)
    def bstack1l1ll1111l1_opy_(
        self,
        f: bstack1llllll111l_opy_,
        driver: object,
        exec: Tuple[bstack111l1111ll_opy_, str],
        bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1llllll111l_opy_.session_id(driver)
            if session_id:
                bstack1l1l1llll11_opy_ = bstack1l11l_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧቪ").format(session_id)
                bstack1lll1ll1l11_opy_.mark(bstack1l1l1llll11_opy_)
    def bstack1l1ll111l1l_opy_(
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
        if f.bstack1111ll111l_opy_(instance, bstack1lll1llllll_opy_.bstack1l1l1lllll1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1llllll111l_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣቫ") + str(hub_url) + bstack1l11l_opy_ (u"ࠧࠨቬ"))
            return
        framework_session_id = bstack1llllll111l_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l11l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤቭ") + str(framework_session_id) + bstack1l11l_opy_ (u"ࠢࠣቮ"))
            return
        if bstack1llllll111l_opy_.bstack1l1ll11llll_opy_(*args) == bstack1llllll111l_opy_.bstack1l1ll1l1111_opy_:
            bstack1l1ll11ll1l_opy_ = bstack1l11l_opy_ (u"ࠣࡽࢀ࠾ࡪࡴࡤࠣቯ").format(framework_session_id)
            bstack1l1l1llll11_opy_ = bstack1l11l_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦተ").format(framework_session_id)
            bstack1lll1ll1l11_opy_.end(
                label=bstack1l11l_opy_ (u"ࠥࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳࠨቱ"),
                start=bstack1l1l1llll11_opy_,
                end=bstack1l1ll11ll1l_opy_,
                status=True,
                failure=None
            )
            bstack1ll11ll11l_opy_ = datetime.now()
            r = self.bstack1l1ll111lll_opy_(
                ref,
                f.bstack1111ll111l_opy_(instance, bstack1llllll111l_opy_.bstack1ll1ll1llll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1l1lll11ll_opy_(bstack1l11l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥቲ"), datetime.now() - bstack1ll11ll11l_opy_)
            f.bstack1111l1ll1l_opy_(instance, bstack1lll1llllll_opy_.bstack1l1l1lllll1_opy_, r.success)
    def bstack1l1l1llllll_opy_(
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
        if f.bstack1111ll111l_opy_(instance, bstack1lll1llllll_opy_.bstack1l1ll1l1l1l_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1llllll111l_opy_.session_id(driver)
        hub_url = bstack1llllll111l_opy_.hub_url(driver)
        bstack1ll11ll11l_opy_ = datetime.now()
        r = self.bstack1l1ll11l1ll_opy_(
            ref,
            f.bstack1111ll111l_opy_(instance, bstack1llllll111l_opy_.bstack1ll1ll1llll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1l1lll11ll_opy_(bstack1l11l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥታ"), datetime.now() - bstack1ll11ll11l_opy_)
        f.bstack1111l1ll1l_opy_(instance, bstack1lll1llllll_opy_.bstack1l1ll1l1l1l_opy_, r.success)
    @measure(event_name=EVENTS.bstack11lll1l1ll_opy_, stage=STAGE.bstack1111111l_opy_)
    def bstack1l1lllll1ll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l11l_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦቴ") + str(req) + bstack1l11l_opy_ (u"ࠢࠣት"))
        try:
            r = self.bstack1llllll1l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l11l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦቶ") + str(r.success) + bstack1l11l_opy_ (u"ࠤࠥቷ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣቸ") + str(e) + bstack1l11l_opy_ (u"ࠦࠧቹ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1ll1l1ll1_opy_, stage=STAGE.bstack1111111l_opy_)
    def bstack1l1ll111ll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1l1ll1ll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1l11l_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢቺ") + str(req) + bstack1l11l_opy_ (u"ࠨࠢቻ"))
        try:
            r = self.bstack1llllll1l11_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l11l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥቼ") + str(r.success) + bstack1l11l_opy_ (u"ࠣࠤች"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢቾ") + str(e) + bstack1l11l_opy_ (u"ࠥࠦቿ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1ll111111_opy_, stage=STAGE.bstack1111111l_opy_)
    def bstack1l1ll111lll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1ll1ll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l11l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸ࠿ࠦࠢኀ") + str(req) + bstack1l11l_opy_ (u"ࠧࠨኁ"))
        try:
            r = self.bstack1llllll1l11_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l11l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣኂ") + str(r) + bstack1l11l_opy_ (u"ࠢࠣኃ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨኄ") + str(e) + bstack1l11l_opy_ (u"ࠤࠥኅ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1ll11l1l1_opy_, stage=STAGE.bstack1111111l_opy_)
    def bstack1l1ll11l1ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1ll1ll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l11l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲ࠽ࠤࠧኆ") + str(req) + bstack1l11l_opy_ (u"ࠦࠧኇ"))
        try:
            r = self.bstack1llllll1l11_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l11l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢኈ") + str(r) + bstack1l11l_opy_ (u"ࠨࠢ኉"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧኊ") + str(e) + bstack1l11l_opy_ (u"ࠣࠤኋ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lllll_opy_, stage=STAGE.bstack1111111l_opy_)
    def bstack1l1ll1l1l11_opy_(self, instance: bstack111l1111ll_opy_, f: bstack1llllll111l_opy_, kwargs):
        bstack1l1ll111l11_opy_ = version.parse(f.framework_version)
        bstack1l1ll11lll1_opy_ = kwargs.get(bstack1l11l_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥኌ"))
        bstack1l1ll1l111l_opy_ = kwargs.get(bstack1l11l_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥኍ"))
        bstack1l1llllll11_opy_ = {}
        bstack1l1ll1l1lll_opy_ = {}
        bstack1l1ll11ll11_opy_ = None
        bstack1l1ll11111l_opy_ = {}
        if bstack1l1ll1l111l_opy_ is not None or bstack1l1ll11lll1_opy_ is not None: # check top level caps
            if bstack1l1ll1l111l_opy_ is not None:
                bstack1l1ll11111l_opy_[bstack1l11l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ኎")] = bstack1l1ll1l111l_opy_
            if bstack1l1ll11lll1_opy_ is not None and callable(getattr(bstack1l1ll11lll1_opy_, bstack1l11l_opy_ (u"ࠧࡺ࡯ࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ኏"))):
                bstack1l1ll11111l_opy_[bstack1l11l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡢࡵࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩነ")] = bstack1l1ll11lll1_opy_.to_capabilities()
        response = self.bstack1l1lllll1ll_opy_(f.platform_index, instance.ref(), json.dumps(bstack1l1ll11111l_opy_).encode(bstack1l11l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨኑ")))
        if response is not None and response.capabilities:
            bstack1l1llllll11_opy_ = json.loads(response.capabilities.decode(bstack1l11l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢኒ")))
            if not bstack1l1llllll11_opy_: # empty caps bstack1l1llll11ll_opy_ bstack1l1lll1ll1l_opy_ bstack1l1lll1l1l1_opy_ bstack1lll1ll111l_opy_ or error in processing
                return
            bstack1l1ll11ll11_opy_ = f.bstack111111ll11_opy_[bstack1l11l_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡪࡷࡵ࡭ࡠࡥࡤࡴࡸࠨና")](bstack1l1llllll11_opy_)
        if bstack1l1ll11lll1_opy_ is not None and bstack1l1ll111l11_opy_ >= version.parse(bstack1l11l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩኔ")):
            bstack1l1ll1l1lll_opy_ = None
        if (
                not bstack1l1ll11lll1_opy_ and not bstack1l1ll1l111l_opy_
        ) or (
                bstack1l1ll111l11_opy_ < version.parse(bstack1l11l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪን"))
        ):
            bstack1l1ll1l1lll_opy_ = {}
            bstack1l1ll1l1lll_opy_.update(bstack1l1llllll11_opy_)
        self.logger.info(bstack1111111l1_opy_)
        if os.environ.get(bstack1l11l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣኖ")).lower().__eq__(bstack1l11l_opy_ (u"ࠨࡴࡳࡷࡨࠦኗ")):
            kwargs.update(
                {
                    bstack1l11l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥኘ"): f.bstack1l1ll1l11l1_opy_,
                }
            )
        if bstack1l1ll111l11_opy_ >= version.parse(bstack1l11l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨኙ")):
            if bstack1l1ll1l111l_opy_ is not None:
                del kwargs[bstack1l11l_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤኚ")]
            kwargs.update(
                {
                    bstack1l11l_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦኛ"): bstack1l1ll11ll11_opy_,
                    bstack1l11l_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣኜ"): True,
                    bstack1l11l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧኝ"): None,
                }
            )
        elif bstack1l1ll111l11_opy_ >= version.parse(bstack1l11l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬኞ")):
            kwargs.update(
                {
                    bstack1l11l_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢኟ"): bstack1l1ll1l1lll_opy_,
                    bstack1l11l_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤአ"): bstack1l1ll11ll11_opy_,
                    bstack1l11l_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨኡ"): True,
                    bstack1l11l_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥኢ"): None,
                }
            )
        elif bstack1l1ll111l11_opy_ >= version.parse(bstack1l11l_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫኣ")):
            kwargs.update(
                {
                    bstack1l11l_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧኤ"): bstack1l1ll1l1lll_opy_,
                    bstack1l11l_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥእ"): True,
                    bstack1l11l_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢኦ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l11l_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣኧ"): bstack1l1ll1l1lll_opy_,
                    bstack1l11l_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨከ"): True,
                    bstack1l11l_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥኩ"): None,
                }
            )