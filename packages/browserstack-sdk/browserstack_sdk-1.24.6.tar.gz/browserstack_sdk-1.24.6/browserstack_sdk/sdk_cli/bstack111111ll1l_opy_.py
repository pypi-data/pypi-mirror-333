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
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll111lll_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1111llll1l_opy_ import (
    bstack11111ll11l_opy_,
    bstack11111l1lll_opy_,
    bstack1111lll11l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1llllllll11_opy_ import bstack111111l11l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll11lll1_opy_
from bstack_utils.helper import bstack1ll1111l1l1_opy_
import threading
import os
import urllib.parse
class bstack1lllllll11l_opy_(bstack1lll11l1lll_opy_):
    def __init__(self, bstack1lllll11l11_opy_):
        super().__init__()
        bstack111111l11l_opy_.bstack1ll1llllll1_opy_((bstack11111ll11l_opy_.bstack1111ll1ll1_opy_, bstack11111l1lll_opy_.PRE), self.bstack1l1lll1ll1l_opy_)
        bstack111111l11l_opy_.bstack1ll1llllll1_opy_((bstack11111ll11l_opy_.bstack1111ll1ll1_opy_, bstack11111l1lll_opy_.PRE), self.bstack1l1lll1lll1_opy_)
        bstack111111l11l_opy_.bstack1ll1llllll1_opy_((bstack11111ll11l_opy_.bstack111l111111_opy_, bstack11111l1lll_opy_.PRE), self.bstack1l1lll1llll_opy_)
        bstack111111l11l_opy_.bstack1ll1llllll1_opy_((bstack11111ll11l_opy_.bstack1111ll1l1l_opy_, bstack11111l1lll_opy_.PRE), self.bstack1l1llllll11_opy_)
        bstack111111l11l_opy_.bstack1ll1llllll1_opy_((bstack11111ll11l_opy_.bstack1111ll1ll1_opy_, bstack11111l1lll_opy_.PRE), self.bstack1l1lll1ll11_opy_)
        bstack111111l11l_opy_.bstack1ll1llllll1_opy_((bstack11111ll11l_opy_.QUIT, bstack11111l1lll_opy_.PRE), self.on_close)
        self.bstack1lllll11l11_opy_ = bstack1lllll11l11_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll1ll1l_opy_(
        self,
        f: bstack111111l11l_opy_,
        bstack1l1llll1111_opy_: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨᇨ"):
            return
        if not bstack1ll1111l1l1_opy_():
            self.logger.debug(bstack11_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡬ࡢࡷࡱࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᇩ"))
            return
        def wrapped(bstack1l1llll1111_opy_, launch, *args, **kwargs):
            response = self.bstack1l1llll11l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack11_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᇪ"): True}).encode(bstack11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᇫ")))
            if response is not None and response.capabilities:
                if not bstack1ll1111l1l1_opy_():
                    browser = launch(bstack1l1llll1111_opy_)
                    return browser
                bstack1l1llll1l1l_opy_ = json.loads(response.capabilities.decode(bstack11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᇬ")))
                if not bstack1l1llll1l1l_opy_: # empty caps bstack1l1llll1l11_opy_ bstack1l1llll111l_opy_ bstack1l1lllll1l1_opy_ bstack1llll11l1ll_opy_ or error in processing
                    return
                bstack1l1lllll111_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1llll1l1l_opy_))
                f.bstack1111lll1l1_opy_(instance, bstack111111l11l_opy_.bstack1l1llll1ll1_opy_, bstack1l1lllll111_opy_)
                f.bstack1111lll1l1_opy_(instance, bstack111111l11l_opy_.bstack1l1llll11ll_opy_, bstack1l1llll1l1l_opy_)
                browser = bstack1l1llll1111_opy_.connect(bstack1l1lllll111_opy_)
                return browser
        return wrapped
    def bstack1l1lll1llll_opy_(
        self,
        f: bstack111111l11l_opy_,
        Connection: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨᇭ"):
            self.logger.debug(bstack11_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᇮ"))
            return
        if not bstack1ll1111l1l1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11_opy_ (u"࠭ࡰࡢࡴࡤࡱࡸ࠭ᇯ"), {}).get(bstack11_opy_ (u"ࠧࡣࡵࡓࡥࡷࡧ࡭ࡴࠩᇰ")):
                    bstack1l1lllll11l_opy_ = args[0][bstack11_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᇱ")][bstack11_opy_ (u"ࠤࡥࡷࡕࡧࡲࡢ࡯ࡶࠦᇲ")]
                    session_id = bstack1l1lllll11l_opy_.get(bstack11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨᇳ"))
                    f.bstack1111lll1l1_opy_(instance, bstack111111l11l_opy_.bstack1l1lll1l1ll_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢᇴ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1lll1ll11_opy_(
        self,
        f: bstack111111l11l_opy_,
        bstack1l1llll1111_opy_: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨᇵ"):
            return
        if not bstack1ll1111l1l1_opy_():
            self.logger.debug(bstack11_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡯࡯ࡰࡨࡧࡹࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᇶ"))
            return
        def wrapped(bstack1l1llll1111_opy_, connect, *args, **kwargs):
            response = self.bstack1l1llll11l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᇷ"): True}).encode(bstack11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᇸ")))
            if response is not None and response.capabilities:
                bstack1l1llll1l1l_opy_ = json.loads(response.capabilities.decode(bstack11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᇹ")))
                if not bstack1l1llll1l1l_opy_:
                    return
                bstack1l1lllll111_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1llll1l1l_opy_))
                if bstack1l1llll1l1l_opy_.get(bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᇺ")):
                    browser = bstack1l1llll1111_opy_.bstack1l1llll1lll_opy_(bstack1l1lllll111_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1lllll111_opy_
                    return connect(bstack1l1llll1111_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1lll1lll1_opy_(
        self,
        f: bstack111111l11l_opy_,
        bstack1ll1l111l1l_opy_: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᇻ"):
            return
        if not bstack1ll1111l1l1_opy_():
            self.logger.debug(bstack11_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᇼ"))
            return
        def wrapped(bstack1ll1l111l1l_opy_, bstack1l1lll1l1l1_opy_, *args, **kwargs):
            contexts = bstack1ll1l111l1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack11_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦᇽ") in page.url:
                                    return page
                    else:
                        return bstack1l1lll1l1l1_opy_(bstack1ll1l111l1l_opy_)
        return wrapped
    def bstack1l1llll11l1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᇾ") + str(req) + bstack11_opy_ (u"ࠣࠤᇿ"))
        try:
            r = self.bstack11111l11ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧሀ") + str(r.success) + bstack11_opy_ (u"ࠥࠦሁ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤሂ") + str(e) + bstack11_opy_ (u"ࠧࠨሃ"))
            traceback.print_exc()
            raise e
    def bstack1l1llllll11_opy_(
        self,
        f: bstack111111l11l_opy_,
        Connection: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤሄ"):
            return
        if not bstack1ll1111l1l1_opy_():
            return
        def wrapped(Connection, bstack1l1lllll1ll_opy_, *args, **kwargs):
            return bstack1l1lllll1ll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack111111l11l_opy_,
        bstack1l1llll1111_opy_: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨህ"):
            return
        if not bstack1ll1111l1l1_opy_():
            self.logger.debug(bstack11_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦሆ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped