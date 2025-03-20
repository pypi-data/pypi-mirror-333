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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11l1l1l1l1_opy_ import bstack11l1l11lll_opy_, bstack11l11lll11_opy_
from bstack_utils.bstack11l11l1ll1_opy_ import bstack11l1llllll_opy_
from bstack_utils.helper import bstack1llll1llll_opy_, bstack111ll1l1l_opy_, Result
from bstack_utils.bstack11l1l111ll_opy_ import bstack1ll1lll11_opy_
from bstack_utils.capture import bstack11l11l1l11_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1ll1l1111l_opy_:
    def __init__(self):
        self.bstack11l1l111l1_opy_ = bstack11l11l1l11_opy_(self.bstack11l11l11ll_opy_)
        self.tests = {}
    @staticmethod
    def bstack11l11l11ll_opy_(log):
        if not (log[bstack1l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ຋")] and log[bstack1l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຌ")].strip()):
            return
        active = bstack11l1llllll_opy_.bstack11l1l1l111_opy_()
        log = {
            bstack1l11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧຍ"): log[bstack1l11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨຎ")],
            bstack1l11l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ຏ"): bstack111ll1l1l_opy_(),
            bstack1l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬຐ"): log[bstack1l11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຑ")],
        }
        if active:
            if active[bstack1l11l_opy_ (u"࠭ࡴࡺࡲࡨࠫຒ")] == bstack1l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬຓ"):
                log[bstack1l11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨດ")] = active[bstack1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩຕ")]
            elif active[bstack1l11l_opy_ (u"ࠪࡸࡾࡶࡥࠨຖ")] == bstack1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩທ"):
                log[bstack1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬຘ")] = active[bstack1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ນ")]
        bstack1ll1lll11_opy_.bstack1111lll1l_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack11l1l111l1_opy_.start()
        driver = bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ບ"), None)
        bstack11l1l1l1l1_opy_ = bstack11l11lll11_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack111ll1l1l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l11l_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤປ"),
            framework=bstack1l11l_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩຜ"),
            scope=[attrs.feature.name],
            bstack11l1l11111_opy_=bstack1ll1lll11_opy_.bstack11l11l1lll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ຝ")] = bstack11l1l1l1l1_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack1ll1lll11_opy_.bstack11l11l11l1_opy_(bstack1l11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬພ"), bstack11l1l1l1l1_opy_)
    def end_test(self, attrs):
        bstack11l11ll111_opy_ = {
            bstack1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥຟ"): attrs.feature.name,
            bstack1l11l_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦຠ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11l1l1l1l1_opy_ = self.tests[current_test_uuid][bstack1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪມ")]
        meta = {
            bstack1l11l_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤຢ"): bstack11l11ll111_opy_,
            bstack1l11l_opy_ (u"ࠤࡶࡸࡪࡶࡳࠣຣ"): bstack11l1l1l1l1_opy_.meta.get(bstack1l11l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ຤"), []),
            bstack1l11l_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨລ"): {
                bstack1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ຦"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11l1l1l1l1_opy_.bstack11l11ll1l1_opy_(meta)
        bstack11l1l1l1l1_opy_.bstack11l11l1l1l_opy_(bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫວ"), []))
        bstack11l1l1l11l_opy_, exception = self._11l11lllll_opy_(attrs)
        bstack11l11lll1l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l11ll11l_opy_=[bstack11l1l1l11l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪຨ")].stop(time=bstack111ll1l1l_opy_(), duration=int(attrs.duration)*1000, result=bstack11l11lll1l_opy_)
        bstack1ll1lll11_opy_.bstack11l11l11l1_opy_(bstack1l11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪຩ"), self.tests[threading.current_thread().current_test_uuid][bstack1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬສ")])
    def bstack11ll11l1_opy_(self, attrs):
        bstack11l1l11ll1_opy_ = {
            bstack1l11l_opy_ (u"ࠪ࡭ࡩ࠭ຫ"): uuid4().__str__(),
            bstack1l11l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬຬ"): attrs.keyword,
            bstack1l11l_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬອ"): [],
            bstack1l11l_opy_ (u"࠭ࡴࡦࡺࡷࠫຮ"): attrs.name,
            bstack1l11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫຯ"): bstack111ll1l1l_opy_(),
            bstack1l11l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨະ"): bstack1l11l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪັ"),
            bstack1l11l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨາ"): bstack1l11l_opy_ (u"ࠫࠬຳ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨິ")].add_step(bstack11l1l11ll1_opy_)
        threading.current_thread().current_step_uuid = bstack11l1l11ll1_opy_[bstack1l11l_opy_ (u"࠭ࡩࡥࠩີ")]
    def bstack1l1l11111l_opy_(self, attrs):
        current_test_id = bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫຶ"), None)
        current_step_uuid = bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬື"), None)
        bstack11l1l1l11l_opy_, exception = self._11l11lllll_opy_(attrs)
        bstack11l11lll1l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l11ll11l_opy_=[bstack11l1l1l11l_opy_])
        self.tests[current_test_id][bstack1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥຸࠬ")].bstack11l11ll1ll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11l11lll1l_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11ll1l11ll_opy_(self, name, attrs):
        try:
            bstack11l11llll1_opy_ = uuid4().__str__()
            self.tests[bstack11l11llll1_opy_] = {}
            self.bstack11l1l111l1_opy_.start()
            scopes = []
            driver = bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳູࠩ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴ຺ࠩ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l11llll1_opy_)
            if name in [bstack1l11l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤົ"), bstack1l11l_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤຼ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l11l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣຽ"), bstack1l11l_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣ຾")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l11l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ຿")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11l1l11lll_opy_(
                name=name,
                uuid=bstack11l11llll1_opy_,
                started_at=bstack111ll1l1l_opy_(),
                file_path=file_path,
                framework=bstack1l11l_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥເ"),
                bstack11l1l11111_opy_=bstack1ll1lll11_opy_.bstack11l11l1lll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l11l_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧແ"),
                hook_type=name
            )
            self.tests[bstack11l11llll1_opy_][bstack1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣໂ")] = hook_data
            current_test_id = bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥໃ"), None)
            if current_test_id:
                hook_data.bstack11l1l11l1l_opy_(current_test_id)
            if name == bstack1l11l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦໄ"):
                threading.current_thread().before_all_hook_uuid = bstack11l11llll1_opy_
            threading.current_thread().current_hook_uuid = bstack11l11llll1_opy_
            bstack1ll1lll11_opy_.bstack11l11l11l1_opy_(bstack1l11l_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤ໅"), hook_data)
        except Exception as e:
            logger.debug(bstack1l11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳࠣໆ"), name, e)
    def bstack1l1l111111_opy_(self, attrs):
        bstack11l1l11l11_opy_ = bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ໇"), None)
        hook_data = self.tests[bstack11l1l11l11_opy_][bstack1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧ່ࠧ")]
        status = bstack1l11l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨ້ࠧ")
        exception = None
        bstack11l1l1l11l_opy_ = None
        if hook_data.name == bstack1l11l_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ໊"):
            self.bstack11l1l111l1_opy_.reset()
            bstack11l11l111l_opy_ = self.tests[bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪ໋ࠧ"), None)][bstack1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ໌")].result.result
            if bstack11l11l111l_opy_ == bstack1l11l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤໍ"):
                if attrs.hook_failures == 1:
                    status = bstack1l11l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ໎")
                elif attrs.hook_failures == 2:
                    status = bstack1l11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ໏")
            elif attrs.bstack11l1l1111l_opy_:
                status = bstack1l11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ໐")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l11l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ໑") and attrs.hook_failures == 1:
                status = bstack1l11l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ໒")
            elif hasattr(attrs, bstack1l11l_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ໓")) and attrs.error_message:
                status = bstack1l11l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ໔")
            bstack11l1l1l11l_opy_, exception = self._11l11lllll_opy_(attrs)
        bstack11l11lll1l_opy_ = Result(result=status, exception=exception, bstack11l11ll11l_opy_=[bstack11l1l1l11l_opy_])
        hook_data.stop(time=bstack111ll1l1l_opy_(), duration=0, result=bstack11l11lll1l_opy_)
        bstack1ll1lll11_opy_.bstack11l11l11l1_opy_(bstack1l11l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ໕"), self.tests[bstack11l1l11l11_opy_][bstack1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ໖")])
        threading.current_thread().current_hook_uuid = None
    def _11l11lllll_opy_(self, attrs):
        try:
            import traceback
            bstack11ll1lllll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l1l1l11l_opy_ = bstack11ll1lllll_opy_[-1] if bstack11ll1lllll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l11l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡵࡷࡳࡲࠦࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠤ໗"))
            bstack11l1l1l11l_opy_ = None
            exception = None
        return bstack11l1l1l11l_opy_, exception