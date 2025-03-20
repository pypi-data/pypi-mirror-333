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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1111lllll1_opy_,
    bstack111l1111ll_opy_,
    bstack1111l11ll1_opy_,
    bstack11111l1lll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1ll1l1lll1_opy_ import bstack1lll1ll1l11_opy_
from bstack_utils.constants import EVENTS
class bstack1llllll111l_opy_(bstack1111lllll1_opy_):
    bstack1l1l1l1l111_opy_ = bstack1l11l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᐗ")
    NAME = bstack1l11l_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᐘ")
    bstack1l1llll111l_opy_ = bstack1l11l_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᐙ")
    bstack1l1llll1l1l_opy_ = bstack1l11l_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᐚ")
    bstack1l11l1l1ll1_opy_ = bstack1l11l_opy_ (u"ࠤ࡬ࡲࡵࡻࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᐛ")
    bstack1l1llll1ll1_opy_ = bstack1l11l_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᐜ")
    bstack1l1l1ll1l1l_opy_ = bstack1l11l_opy_ (u"ࠦ࡮ࡹ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡨࡶࡤࠥᐝ")
    bstack1l11l1lll1l_opy_ = bstack1l11l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᐞ")
    bstack1l11l1lll11_opy_ = bstack1l11l_opy_ (u"ࠨࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᐟ")
    bstack1ll1ll1llll_opy_ = bstack1l11l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᐠ")
    bstack1l1ll1l1111_opy_ = bstack1l11l_opy_ (u"ࠣࡰࡨࡻࡸ࡫ࡳࡴ࡫ࡲࡲࠧᐡ")
    bstack1l11l1ll1l1_opy_ = bstack1l11l_opy_ (u"ࠤࡪࡩࡹࠨᐢ")
    bstack1ll11llllll_opy_ = bstack1l11l_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᐣ")
    bstack1l1l1l1l1ll_opy_ = bstack1l11l_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢᐤ")
    bstack1l1l1l1lll1_opy_ = bstack1l11l_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨᐥ")
    bstack1l11l1ll11l_opy_ = bstack1l11l_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᐦ")
    bstack1l11l1l1l11_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1ll1l11l1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack111111ll11_opy_: Any
    bstack1l1l1l11lll_opy_: Dict
    def __init__(
        self,
        bstack1l1ll1l11l1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack111111ll11_opy_: Dict[str, Any],
        methods=[bstack1l11l_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᐧ"), bstack1l11l_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᐨ"), bstack1l11l_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᐩ"), bstack1l11l_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᐪ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1ll1l11l1_opy_ = bstack1l1ll1l11l1_opy_
        self.platform_index = platform_index
        self.bstack11111ll11l_opy_(methods)
        self.bstack111111ll11_opy_ = bstack111111ll11_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1111lllll1_opy_.get_data(bstack1llllll111l_opy_.bstack1l1llll1l1l_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1111lllll1_opy_.get_data(bstack1llllll111l_opy_.bstack1l1llll111l_opy_, target, strict)
    @staticmethod
    def bstack1l11l1ll111_opy_(target: object, strict=True):
        return bstack1111lllll1_opy_.get_data(bstack1llllll111l_opy_.bstack1l11l1l1ll1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1111lllll1_opy_.get_data(bstack1llllll111l_opy_.bstack1l1llll1ll1_opy_, target, strict)
    @staticmethod
    def bstack1lll11111ll_opy_(instance: bstack111l1111ll_opy_) -> bool:
        return bstack1111lllll1_opy_.bstack1111ll111l_opy_(instance, bstack1llllll111l_opy_.bstack1l1l1ll1l1l_opy_, False)
    @staticmethod
    def bstack1lll1111l11_opy_(instance: bstack111l1111ll_opy_, default_value=None):
        return bstack1111lllll1_opy_.bstack1111ll111l_opy_(instance, bstack1llllll111l_opy_.bstack1l1llll111l_opy_, default_value)
    @staticmethod
    def bstack1lll11111l1_opy_(instance: bstack111l1111ll_opy_, default_value=None):
        return bstack1111lllll1_opy_.bstack1111ll111l_opy_(instance, bstack1llllll111l_opy_.bstack1l1llll1ll1_opy_, default_value)
    @staticmethod
    def bstack1ll1l1l111l_opy_(hub_url: str, bstack1l11l1l1lll_opy_=bstack1l11l_opy_ (u"ࠦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣᐫ")):
        try:
            bstack1l11l1ll1ll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l11l1ll1ll_opy_.endswith(bstack1l11l1l1lll_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1llll111_opy_(method_name: str):
        return method_name == bstack1l11l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᐬ")
    @staticmethod
    def bstack1lll1111l1l_opy_(method_name: str, *args):
        return (
            bstack1llllll111l_opy_.bstack1ll1llll111_opy_(method_name)
            and bstack1llllll111l_opy_.bstack1l1ll11llll_opy_(*args) == bstack1llllll111l_opy_.bstack1l1ll1l1111_opy_
        )
    @staticmethod
    def bstack1ll1l1lllll_opy_(method_name: str, *args):
        if not bstack1llllll111l_opy_.bstack1ll1llll111_opy_(method_name):
            return False
        if not bstack1llllll111l_opy_.bstack1l1l1l1l1ll_opy_ in bstack1llllll111l_opy_.bstack1l1ll11llll_opy_(*args):
            return False
        bstack1ll1l1l1l1l_opy_ = bstack1llllll111l_opy_.bstack1ll1l1l1ll1_opy_(*args)
        return bstack1ll1l1l1l1l_opy_ and bstack1l11l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᐭ") in bstack1ll1l1l1l1l_opy_ and bstack1l11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᐮ") in bstack1ll1l1l1l1l_opy_[bstack1l11l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᐯ")]
    @staticmethod
    def bstack1ll1ll11l1l_opy_(method_name: str, *args):
        if not bstack1llllll111l_opy_.bstack1ll1llll111_opy_(method_name):
            return False
        if not bstack1llllll111l_opy_.bstack1l1l1l1l1ll_opy_ in bstack1llllll111l_opy_.bstack1l1ll11llll_opy_(*args):
            return False
        bstack1ll1l1l1l1l_opy_ = bstack1llllll111l_opy_.bstack1ll1l1l1ll1_opy_(*args)
        return (
            bstack1ll1l1l1l1l_opy_
            and bstack1l11l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᐰ") in bstack1ll1l1l1l1l_opy_
            and bstack1l11l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᐱ") in bstack1ll1l1l1l1l_opy_[bstack1l11l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᐲ")]
        )
    @staticmethod
    def bstack1l1ll11llll_opy_(*args):
        return str(bstack1llllll111l_opy_.bstack1ll1lll1lll_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1lll1lll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11l1l1l1_opy_(driver):
        command_executor = getattr(driver, bstack1l11l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᐳ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l11l_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᐴ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l11l_opy_ (u"ࠢࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠣᐵ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l11l_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡠࡵࡨࡶࡻ࡫ࡲࡠࡣࡧࡨࡷࠨᐶ"), None)
        return hub_url
    def bstack1l1ll1l11ll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l11l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᐷ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᐸ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l11l_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᐹ")):
                setattr(command_executor, bstack1l11l_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᐺ"), hub_url)
                result = True
        if result:
            self.bstack1l1ll1l11l1_opy_ = hub_url
            bstack1llllll111l_opy_.bstack1111l1ll1l_opy_(instance, bstack1llllll111l_opy_.bstack1l1llll111l_opy_, hub_url)
            bstack1llllll111l_opy_.bstack1111l1ll1l_opy_(
                instance, bstack1llllll111l_opy_.bstack1l1l1ll1l1l_opy_, bstack1llllll111l_opy_.bstack1ll1l1l111l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l1l1l1ll1l_opy_(bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_]):
        return bstack1l11l_opy_ (u"ࠨ࠺ࠣᐻ").join((bstack1111l11ll1_opy_(bstack11111lll1l_opy_[0]).name, bstack11111l1lll_opy_(bstack11111lll1l_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll1l11l_opy_(bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_], callback: Callable):
        bstack1l1l1l1l1l1_opy_ = bstack1llllll111l_opy_.bstack1l1l1l1ll1l_opy_(bstack11111lll1l_opy_)
        if not bstack1l1l1l1l1l1_opy_ in bstack1llllll111l_opy_.bstack1l11l1l1l11_opy_:
            bstack1llllll111l_opy_.bstack1l11l1l1l11_opy_[bstack1l1l1l1l1l1_opy_] = []
        bstack1llllll111l_opy_.bstack1l11l1l1l11_opy_[bstack1l1l1l1l1l1_opy_].append(callback)
    def bstack1111lll111_opy_(self, instance: bstack111l1111ll_opy_, method_name: str, bstack1111l111ll_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l11l_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᐼ")):
            return
        cmd = args[0] if method_name == bstack1l11l_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᐽ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l11l1l1l1l_opy_ = bstack1l11l_opy_ (u"ࠤ࠽ࠦᐾ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l1lll11ll_opy_(bstack1l11l_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠦᐿ") + bstack1l11l1l1l1l_opy_, bstack1111l111ll_opy_)
    def bstack1111ll1lll_opy_(
        self,
        target: object,
        exec: Tuple[bstack111l1111ll_opy_, str],
        bstack11111lll1l_opy_: Tuple[bstack1111l11ll1_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111lll11l_opy_, bstack1l1l1ll1111_opy_ = bstack11111lll1l_opy_
        bstack1l1l1l1l1l1_opy_ = bstack1llllll111l_opy_.bstack1l1l1l1ll1l_opy_(bstack11111lll1l_opy_)
        self.logger.debug(bstack1l11l_opy_ (u"ࠦࡴࡴ࡟ࡩࡱࡲ࡯࠿ࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᑀ") + str(kwargs) + bstack1l11l_opy_ (u"ࠧࠨᑁ"))
        if bstack1111lll11l_opy_ == bstack1111l11ll1_opy_.QUIT:
            if bstack1l1l1ll1111_opy_ == bstack11111l1lll_opy_.PRE:
                bstack1ll1ll11111_opy_ = bstack1lll1ll1l11_opy_.bstack1lll111l1ll_opy_(EVENTS.bstack1l11ll111l_opy_.value)
                bstack1111lllll1_opy_.bstack1111l1ll1l_opy_(instance, EVENTS.bstack1l11ll111l_opy_.value, bstack1ll1ll11111_opy_)
                self.logger.debug(bstack1l11l_opy_ (u"ࠨࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠥᑂ").format(instance, method_name, bstack1111lll11l_opy_, bstack1l1l1ll1111_opy_))
        if bstack1111lll11l_opy_ == bstack1111l11ll1_opy_.bstack1111ll11ll_opy_:
            if bstack1l1l1ll1111_opy_ == bstack11111l1lll_opy_.POST and not bstack1llllll111l_opy_.bstack1l1llll1l1l_opy_ in instance.data:
                session_id = getattr(target, bstack1l11l_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᑃ"), None)
                if session_id:
                    instance.data[bstack1llllll111l_opy_.bstack1l1llll1l1l_opy_] = session_id
        elif (
            bstack1111lll11l_opy_ == bstack1111l11ll1_opy_.bstack111l111l11_opy_
            and bstack1llllll111l_opy_.bstack1l1ll11llll_opy_(*args) == bstack1llllll111l_opy_.bstack1l1ll1l1111_opy_
        ):
            if bstack1l1l1ll1111_opy_ == bstack11111l1lll_opy_.PRE:
                hub_url = bstack1llllll111l_opy_.bstack11l1l1l1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1llllll111l_opy_.bstack1l1llll111l_opy_: hub_url,
                            bstack1llllll111l_opy_.bstack1l1l1ll1l1l_opy_: bstack1llllll111l_opy_.bstack1ll1l1l111l_opy_(hub_url),
                            bstack1llllll111l_opy_.bstack1ll1ll1llll_opy_: int(
                                os.environ.get(bstack1l11l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᑄ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll1l1l1l1l_opy_ = bstack1llllll111l_opy_.bstack1ll1l1l1ll1_opy_(*args)
                bstack1l11l1ll111_opy_ = bstack1ll1l1l1l1l_opy_.get(bstack1l11l_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᑅ"), None) if bstack1ll1l1l1l1l_opy_ else None
                if isinstance(bstack1l11l1ll111_opy_, dict):
                    instance.data[bstack1llllll111l_opy_.bstack1l11l1l1ll1_opy_] = copy.deepcopy(bstack1l11l1ll111_opy_)
                    instance.data[bstack1llllll111l_opy_.bstack1l1llll1ll1_opy_] = bstack1l11l1ll111_opy_
            elif bstack1l1l1ll1111_opy_ == bstack11111l1lll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l11l_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᑆ"), dict()).get(bstack1l11l_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢᑇ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1llllll111l_opy_.bstack1l1llll1l1l_opy_: framework_session_id,
                                bstack1llllll111l_opy_.bstack1l11l1lll1l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1111lll11l_opy_ == bstack1111l11ll1_opy_.bstack111l111l11_opy_
            and bstack1llllll111l_opy_.bstack1l1ll11llll_opy_(*args) == bstack1llllll111l_opy_.bstack1l11l1ll11l_opy_
            and bstack1l1l1ll1111_opy_ == bstack11111l1lll_opy_.POST
        ):
            instance.data[bstack1llllll111l_opy_.bstack1l11l1lll11_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l1l1l1l1l1_opy_ in bstack1llllll111l_opy_.bstack1l11l1l1l11_opy_:
            bstack1l1l1l1ll11_opy_ = None
            for callback in bstack1llllll111l_opy_.bstack1l11l1l1l11_opy_[bstack1l1l1l1l1l1_opy_]:
                try:
                    bstack1l1l1l1llll_opy_ = callback(self, target, exec, bstack11111lll1l_opy_, result, *args, **kwargs)
                    if bstack1l1l1l1ll11_opy_ == None:
                        bstack1l1l1l1ll11_opy_ = bstack1l1l1l1llll_opy_
                except Exception as e:
                    self.logger.error(bstack1l11l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᑈ") + str(e) + bstack1l11l_opy_ (u"ࠨࠢᑉ"))
                    traceback.print_exc()
            if bstack1111lll11l_opy_ == bstack1111l11ll1_opy_.QUIT:
                if bstack1l1l1ll1111_opy_ == bstack11111l1lll_opy_.POST:
                    bstack1ll1ll11111_opy_ = bstack1111lllll1_opy_.bstack1111ll111l_opy_(instance, EVENTS.bstack1l11ll111l_opy_.value)
                    if bstack1ll1ll11111_opy_!=None:
                        bstack1lll1ll1l11_opy_.end(EVENTS.bstack1l11ll111l_opy_.value, bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᑊ"), bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᑋ"), True, None)
            if bstack1l1l1ll1111_opy_ == bstack11111l1lll_opy_.PRE and callable(bstack1l1l1l1ll11_opy_):
                return bstack1l1l1l1ll11_opy_
            elif bstack1l1l1ll1111_opy_ == bstack11111l1lll_opy_.POST and bstack1l1l1l1ll11_opy_:
                return bstack1l1l1l1ll11_opy_
    def bstack1111l1l111_opy_(
        self, method_name, previous_state: bstack1111l11ll1_opy_, *args, **kwargs
    ) -> bstack1111l11ll1_opy_:
        if method_name == bstack1l11l_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᑌ") or method_name == bstack1l11l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᑍ"):
            return bstack1111l11ll1_opy_.bstack1111ll11ll_opy_
        if method_name == bstack1l11l_opy_ (u"ࠦࡶࡻࡩࡵࠤᑎ"):
            return bstack1111l11ll1_opy_.QUIT
        if method_name == bstack1l11l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᑏ"):
            if previous_state != bstack1111l11ll1_opy_.NONE:
                bstack1ll1llll11l_opy_ = bstack1llllll111l_opy_.bstack1l1ll11llll_opy_(*args)
                if bstack1ll1llll11l_opy_ == bstack1llllll111l_opy_.bstack1l1ll1l1111_opy_:
                    return bstack1111l11ll1_opy_.bstack1111ll11ll_opy_
            return bstack1111l11ll1_opy_.bstack111l111l11_opy_
        return bstack1111l11ll1_opy_.NONE