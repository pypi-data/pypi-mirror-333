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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11l1l11l1l_opy_ import bstack11l1l1l1l1_opy_, bstack11l11lll11_opy_
from bstack_utils.bstack11l11l1l1l_opy_ import bstack1ll11l1l1_opy_
from bstack_utils.helper import bstack1llllll111_opy_, bstack1lllll11ll_opy_, Result
from bstack_utils.bstack11l11l111l_opy_ import bstack111lllll1_opy_
from bstack_utils.capture import bstack11l1l111l1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack111lll1l_opy_:
    def __init__(self):
        self.bstack11l11l11ll_opy_ = bstack11l1l111l1_opy_(self.bstack11l11lllll_opy_)
        self.tests = {}
    @staticmethod
    def bstack11l11lllll_opy_(log):
        if not (log[bstack11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຌ")] and log[bstack11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩຍ")].strip()):
            return
        active = bstack1ll11l1l1_opy_.bstack11l11llll1_opy_()
        log = {
            bstack11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨຎ"): log[bstack11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩຏ")],
            bstack11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧຐ"): bstack1lllll11ll_opy_(),
            bstack11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຑ"): log[bstack11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧຒ")],
        }
        if active:
            if active[bstack11_opy_ (u"ࠧࡵࡻࡳࡩࠬຓ")] == bstack11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ດ"):
                log[bstack11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩຕ")] = active[bstack11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪຖ")]
            elif active[bstack11_opy_ (u"ࠫࡹࡿࡰࡦࠩທ")] == bstack11_opy_ (u"ࠬࡺࡥࡴࡶࠪຘ"):
                log[bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ນ")] = active[bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧບ")]
        bstack111lllll1_opy_.bstack1l1l11ll11_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack11l11l11ll_opy_.start()
        driver = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧປ"), None)
        bstack11l1l11l1l_opy_ = bstack11l11lll11_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1lllll11ll_opy_(),
            file_path=attrs.feature.filename,
            result=bstack11_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥຜ"),
            framework=bstack11_opy_ (u"ࠪࡆࡪ࡮ࡡࡷࡧࠪຝ"),
            scope=[attrs.feature.name],
            bstack11l1l11111_opy_=bstack111lllll1_opy_.bstack11l1l11lll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧພ")] = bstack11l1l11l1l_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack111lllll1_opy_.bstack11l1l1111l_opy_(bstack11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ຟ"), bstack11l1l11l1l_opy_)
    def end_test(self, attrs):
        bstack11l11l1ll1_opy_ = {
            bstack11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦຠ"): attrs.feature.name,
            bstack11_opy_ (u"ࠢࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧມ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11l1l11l1l_opy_ = self.tests[current_test_uuid][bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫຢ")]
        meta = {
            bstack11_opy_ (u"ࠤࡩࡩࡦࡺࡵࡳࡧࠥຣ"): bstack11l11l1ll1_opy_,
            bstack11_opy_ (u"ࠥࡷࡹ࡫ࡰࡴࠤ຤"): bstack11l1l11l1l_opy_.meta.get(bstack11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪລ"), []),
            bstack11_opy_ (u"ࠧࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ຦"): {
                bstack11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦວ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11l1l11l1l_opy_.bstack11l1l1l111_opy_(meta)
        bstack11l1l11l1l_opy_.bstack11l1l11ll1_opy_(bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬຨ"), []))
        bstack11l11l1lll_opy_, exception = self._11l11ll1l1_opy_(attrs)
        bstack11l1l1l11l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l11l1l11_opy_=[bstack11l11l1lll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫຩ")].stop(time=bstack1lllll11ll_opy_(), duration=int(attrs.duration)*1000, result=bstack11l1l1l11l_opy_)
        bstack111lllll1_opy_.bstack11l1l1111l_opy_(bstack11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫສ"), self.tests[threading.current_thread().current_test_uuid][bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ຫ")])
    def bstack1lllll11l_opy_(self, attrs):
        bstack11l1l111ll_opy_ = {
            bstack11_opy_ (u"ࠫ࡮ࡪࠧຬ"): uuid4().__str__(),
            bstack11_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ອ"): attrs.keyword,
            bstack11_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭ຮ"): [],
            bstack11_opy_ (u"ࠧࡵࡧࡻࡸࠬຯ"): attrs.name,
            bstack11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬະ"): bstack1lllll11ll_opy_(),
            bstack11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩັ"): bstack11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫາ"),
            bstack11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩຳ"): bstack11_opy_ (u"ࠬ࠭ິ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩີ")].add_step(bstack11l1l111ll_opy_)
        threading.current_thread().current_step_uuid = bstack11l1l111ll_opy_[bstack11_opy_ (u"ࠧࡪࡦࠪຶ")]
    def bstack1ll1ll1l_opy_(self, attrs):
        current_test_id = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬື"), None)
        current_step_uuid = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩຸ࠭"), None)
        bstack11l11l1lll_opy_, exception = self._11l11ll1l1_opy_(attrs)
        bstack11l1l1l11l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l11l1l11_opy_=[bstack11l11l1lll_opy_])
        self.tests[current_test_id][bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦູ࠭")].bstack11l11ll111_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11l1l1l11l_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1ll11l1ll_opy_(self, name, attrs):
        try:
            bstack11l11lll1l_opy_ = uuid4().__str__()
            self.tests[bstack11l11lll1l_opy_] = {}
            self.bstack11l11l11ll_opy_.start()
            scopes = []
            driver = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴ຺ࠪ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪົ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l11lll1l_opy_)
            if name in [bstack11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥຼ"), bstack11_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠥຽ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ຾"), bstack11_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠤ຿")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫເ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11l1l1l1l1_opy_(
                name=name,
                uuid=bstack11l11lll1l_opy_,
                started_at=bstack1lllll11ll_opy_(),
                file_path=file_path,
                framework=bstack11_opy_ (u"ࠦࡇ࡫ࡨࡢࡸࡨࠦແ"),
                bstack11l1l11111_opy_=bstack111lllll1_opy_.bstack11l1l11lll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨໂ"),
                hook_type=name
            )
            self.tests[bstack11l11lll1l_opy_][bstack11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡧࡴࡢࠤໃ")] = hook_data
            current_test_id = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠢࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠦໄ"), None)
            if current_test_id:
                hook_data.bstack11l11ll11l_opy_(current_test_id)
            if name == bstack11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ໅"):
                threading.current_thread().before_all_hook_uuid = bstack11l11lll1l_opy_
            threading.current_thread().current_hook_uuid = bstack11l11lll1l_opy_
            bstack111lllll1_opy_.bstack11l1l1111l_opy_(bstack11_opy_ (u"ࠤࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠥໆ"), hook_data)
        except Exception as e:
            logger.debug(bstack11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤ࡮ࡴࠠࡴࡶࡤࡶࡹࠦࡨࡰࡱ࡮ࠤࡪࡼࡥ࡯ࡶࡶ࠰ࠥ࡮࡯ࡰ࡭ࠣࡲࡦࡳࡥ࠻ࠢࠨࡷ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠥࡴࠤ໇"), name, e)
    def bstack111111l1l_opy_(self, attrs):
        bstack11l11l11l1_opy_ = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ່"), None)
        hook_data = self.tests[bstack11l11l11l1_opy_][bstack11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ້")]
        status = bstack11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ໊")
        exception = None
        bstack11l11l1lll_opy_ = None
        if hook_data.name == bstack11_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡡ࡭࡮໋ࠥ"):
            self.bstack11l11l11ll_opy_.reset()
            bstack11l1l11l11_opy_ = self.tests[bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ໌"), None)][bstack11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬໍ")].result.result
            if bstack11l1l11l11_opy_ == bstack11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ໎"):
                if attrs.hook_failures == 1:
                    status = bstack11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ໏")
                elif attrs.hook_failures == 2:
                    status = bstack11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ໐")
            elif attrs.bstack11l11ll1ll_opy_:
                status = bstack11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ໑")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫ໒") and attrs.hook_failures == 1:
                status = bstack11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ໓")
            elif hasattr(attrs, bstack11_opy_ (u"ࠩࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦࠩ໔")) and attrs.error_message:
                status = bstack11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ໕")
            bstack11l11l1lll_opy_, exception = self._11l11ll1l1_opy_(attrs)
        bstack11l1l1l11l_opy_ = Result(result=status, exception=exception, bstack11l11l1l11_opy_=[bstack11l11l1lll_opy_])
        hook_data.stop(time=bstack1lllll11ll_opy_(), duration=0, result=bstack11l1l1l11l_opy_)
        bstack111lllll1_opy_.bstack11l1l1111l_opy_(bstack11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭໖"), self.tests[bstack11l11l11l1_opy_][bstack11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ໗")])
        threading.current_thread().current_hook_uuid = None
    def _11l11ll1l1_opy_(self, attrs):
        try:
            import traceback
            bstack1lll11l111_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l11l1lll_opy_ = bstack1lll11l111_opy_[-1] if bstack1lll11l111_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡶࡸࡴࡳࠠࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࠥ໘"))
            bstack11l11l1lll_opy_ = None
            exception = None
        return bstack11l11l1lll_opy_, exception