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
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111lllllll_opy_ import RobotHandler
from bstack_utils.capture import bstack11l1l111l1_opy_
from bstack_utils.bstack11l1l11l1l_opy_ import bstack11l111l11l_opy_, bstack11l1l1l1l1_opy_, bstack11l11lll11_opy_
from bstack_utils.bstack11l11l1l1l_opy_ import bstack1ll11l1l1_opy_
from bstack_utils.bstack11l11l111l_opy_ import bstack111lllll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1llllll111_opy_, bstack1lllll11ll_opy_, Result, \
    bstack111lll1lll_opy_, bstack11l111l1l1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ໙"): [],
        bstack11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ໚"): [],
        bstack11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭໛"): []
    }
    bstack11l1111lll_opy_ = []
    bstack11l111ll11_opy_ = []
    @staticmethod
    def bstack11l11lllll_opy_(log):
        if not ((isinstance(log[bstack11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫໜ")], list) or (isinstance(log[bstack11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬໝ")], dict)) and len(log[bstack11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ໞ")])>0) or (isinstance(log[bstack11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧໟ")], str) and log[bstack11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໠")].strip())):
            return
        active = bstack1ll11l1l1_opy_.bstack11l11llll1_opy_()
        log = {
            bstack11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ໡"): log[bstack11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ໢")],
            bstack11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭໣"): bstack11l111l1l1_opy_().isoformat() + bstack11_opy_ (u"ࠫ࡟࠭໤"),
            bstack11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໥"): log[bstack11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໦")],
        }
        if active:
            if active[bstack11_opy_ (u"ࠧࡵࡻࡳࡩࠬ໧")] == bstack11_opy_ (u"ࠨࡪࡲࡳࡰ࠭໨"):
                log[bstack11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ໩")] = active[bstack11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ໪")]
            elif active[bstack11_opy_ (u"ࠫࡹࡿࡰࡦࠩ໫")] == bstack11_opy_ (u"ࠬࡺࡥࡴࡶࠪ໬"):
                log[bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭໭")] = active[bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ໮")]
        bstack111lllll1_opy_.bstack1l1l11ll11_opy_([log])
    def __init__(self):
        self.messages = bstack111lll11ll_opy_()
        self._111lll1111_opy_ = None
        self._111ll11l11_opy_ = None
        self._11l111l1ll_opy_ = OrderedDict()
        self.bstack11l11l11ll_opy_ = bstack11l1l111l1_opy_(self.bstack11l11lllll_opy_)
    @bstack111lll1lll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111ll1ll11_opy_()
        if not self._11l111l1ll_opy_.get(attrs.get(bstack11_opy_ (u"ࠨ࡫ࡧࠫ໯")), None):
            self._11l111l1ll_opy_[attrs.get(bstack11_opy_ (u"ࠩ࡬ࡨࠬ໰"))] = {}
        bstack11l111llll_opy_ = bstack11l11lll11_opy_(
                bstack111ll111ll_opy_=attrs.get(bstack11_opy_ (u"ࠪ࡭ࡩ࠭໱")),
                name=name,
                started_at=bstack1lllll11ll_opy_(),
                file_path=os.path.relpath(attrs[bstack11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ໲")], start=os.getcwd()) if attrs.get(bstack11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ໳")) != bstack11_opy_ (u"࠭ࠧ໴") else bstack11_opy_ (u"ࠧࠨ໵"),
                framework=bstack11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ໶")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11_opy_ (u"ࠩ࡬ࡨࠬ໷"), None)
        self._11l111l1ll_opy_[attrs.get(bstack11_opy_ (u"ࠪ࡭ࡩ࠭໸"))][bstack11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ໹")] = bstack11l111llll_opy_
    @bstack111lll1lll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111ll1l1ll_opy_()
        self._111ll1l11l_opy_(messages)
        for bstack11l1111ll1_opy_ in self.bstack11l1111lll_opy_:
            bstack11l1111ll1_opy_[bstack11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ໺")][bstack11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ໻")].extend(self.store[bstack11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭໼")])
            bstack111lllll1_opy_.bstack111111111_opy_(bstack11l1111ll1_opy_)
        self.bstack11l1111lll_opy_ = []
        self.store[bstack11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ໽")] = []
    @bstack111lll1lll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l11l11ll_opy_.start()
        if not self._11l111l1ll_opy_.get(attrs.get(bstack11_opy_ (u"ࠩ࡬ࡨࠬ໾")), None):
            self._11l111l1ll_opy_[attrs.get(bstack11_opy_ (u"ࠪ࡭ࡩ࠭໿"))] = {}
        driver = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪༀ"), None)
        bstack11l1l11l1l_opy_ = bstack11l11lll11_opy_(
            bstack111ll111ll_opy_=attrs.get(bstack11_opy_ (u"ࠬ࡯ࡤࠨ༁")),
            name=name,
            started_at=bstack1lllll11ll_opy_(),
            file_path=os.path.relpath(attrs[bstack11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭༂")], start=os.getcwd()),
            scope=RobotHandler.bstack11l11111l1_opy_(attrs.get(bstack11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ༃"), None)),
            framework=bstack11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ༄"),
            tags=attrs[bstack11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ༅")],
            hooks=self.store[bstack11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩ༆")],
            bstack11l1l11111_opy_=bstack111lllll1_opy_.bstack11l1l11lll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨ༇").format(bstack11_opy_ (u"ࠧࠦࠢ༈").join(attrs[bstack11_opy_ (u"࠭ࡴࡢࡩࡶࠫ༉")]), name) if attrs[bstack11_opy_ (u"ࠧࡵࡣࡪࡷࠬ༊")] else name
        )
        self._11l111l1ll_opy_[attrs.get(bstack11_opy_ (u"ࠨ࡫ࡧࠫ་"))][bstack11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༌")] = bstack11l1l11l1l_opy_
        threading.current_thread().current_test_uuid = bstack11l1l11l1l_opy_.bstack111ll11lll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11_opy_ (u"ࠪ࡭ࡩ࠭།"), None)
        self.bstack11l1l1111l_opy_(bstack11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ༎"), bstack11l1l11l1l_opy_)
    @bstack111lll1lll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l11l11ll_opy_.reset()
        bstack111llllll1_opy_ = bstack11l1111l11_opy_.get(attrs.get(bstack11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ༏")), bstack11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ༐"))
        self._11l111l1ll_opy_[attrs.get(bstack11_opy_ (u"ࠧࡪࡦࠪ༑"))][bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ༒")].stop(time=bstack1lllll11ll_opy_(), duration=int(attrs.get(bstack11_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧ༓"), bstack11_opy_ (u"ࠪ࠴ࠬ༔"))), result=Result(result=bstack111llllll1_opy_, exception=attrs.get(bstack11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༕")), bstack11l11l1l11_opy_=[attrs.get(bstack11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭༖"))]))
        self.bstack11l1l1111l_opy_(bstack11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ༗"), self._11l111l1ll_opy_[attrs.get(bstack11_opy_ (u"ࠧࡪࡦ༘ࠪ"))][bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤ༙ࠫ")], True)
        self.store[bstack11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭༚")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111lll1lll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111ll1ll11_opy_()
        current_test_id = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬ༛"), None)
        bstack111ll111l1_opy_ = current_test_id if bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭༜"), None) else bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ༝"), None)
        if attrs.get(bstack11_opy_ (u"࠭ࡴࡺࡲࡨࠫ༞"), bstack11_opy_ (u"ࠧࠨ༟")).lower() in [bstack11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ༠"), bstack11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ༡")]:
            hook_type = bstack111lllll1l_opy_(attrs.get(bstack11_opy_ (u"ࠪࡸࡾࡶࡥࠨ༢")), bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ༣"), None))
            hook_name = bstack11_opy_ (u"ࠬࢁࡽࠨ༤").format(attrs.get(bstack11_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭༥"), bstack11_opy_ (u"ࠧࠨ༦")))
            if hook_type in [bstack11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ༧"), bstack11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ༨")]:
                hook_name = bstack11_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫ༩").format(bstack11l111lll1_opy_.get(hook_type), attrs.get(bstack11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ༪"), bstack11_opy_ (u"ࠬ࠭༫")))
            bstack111llll1ll_opy_ = bstack11l1l1l1l1_opy_(
                bstack111ll111ll_opy_=bstack111ll111l1_opy_ + bstack11_opy_ (u"࠭࠭ࠨ༬") + attrs.get(bstack11_opy_ (u"ࠧࡵࡻࡳࡩࠬ༭"), bstack11_opy_ (u"ࠨࠩ༮")).lower(),
                name=hook_name,
                started_at=bstack1lllll11ll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ༯")), start=os.getcwd()),
                framework=bstack11_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ༰"),
                tags=attrs[bstack11_opy_ (u"ࠫࡹࡧࡧࡴࠩ༱")],
                scope=RobotHandler.bstack11l11111l1_opy_(attrs.get(bstack11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ༲"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111llll1ll_opy_.bstack111ll11lll_opy_()
            threading.current_thread().current_hook_id = bstack111ll111l1_opy_ + bstack11_opy_ (u"࠭࠭ࠨ༳") + attrs.get(bstack11_opy_ (u"ࠧࡵࡻࡳࡩࠬ༴"), bstack11_opy_ (u"ࠨ༵ࠩ")).lower()
            self.store[bstack11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭༶")] = [bstack111llll1ll_opy_.bstack111ll11lll_opy_()]
            if bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪ༷ࠧ"), None):
                self.store[bstack11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ༸")].append(bstack111llll1ll_opy_.bstack111ll11lll_opy_())
            else:
                self.store[bstack11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶ༹ࠫ")].append(bstack111llll1ll_opy_.bstack111ll11lll_opy_())
            if bstack111ll111l1_opy_:
                self._11l111l1ll_opy_[bstack111ll111l1_opy_ + bstack11_opy_ (u"࠭࠭ࠨ༺") + attrs.get(bstack11_opy_ (u"ࠧࡵࡻࡳࡩࠬ༻"), bstack11_opy_ (u"ࠨࠩ༼")).lower()] = { bstack11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༽"): bstack111llll1ll_opy_ }
            bstack111lllll1_opy_.bstack11l1l1111l_opy_(bstack11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ༾"), bstack111llll1ll_opy_)
        else:
            bstack11l1l111ll_opy_ = {
                bstack11_opy_ (u"ࠫ࡮ࡪࠧ༿"): uuid4().__str__(),
                bstack11_opy_ (u"ࠬࡺࡥࡹࡶࠪཀ"): bstack11_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬཁ").format(attrs.get(bstack11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧག")), attrs.get(bstack11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭གྷ"), bstack11_opy_ (u"ࠩࠪང"))) if attrs.get(bstack11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨཅ"), []) else attrs.get(bstack11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫཆ")),
                bstack11_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬཇ"): attrs.get(bstack11_opy_ (u"࠭ࡡࡳࡩࡶࠫ཈"), []),
                bstack11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫཉ"): bstack1lllll11ll_opy_(),
                bstack11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨཊ"): bstack11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪཋ"),
                bstack11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨཌ"): attrs.get(bstack11_opy_ (u"ࠫࡩࡵࡣࠨཌྷ"), bstack11_opy_ (u"ࠬ࠭ཎ"))
            }
            if attrs.get(bstack11_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧཏ"), bstack11_opy_ (u"ࠧࠨཐ")) != bstack11_opy_ (u"ࠨࠩད"):
                bstack11l1l111ll_opy_[bstack11_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪདྷ")] = attrs.get(bstack11_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫན"))
            if not self.bstack11l111ll11_opy_:
                self._11l111l1ll_opy_[self._111lll111l_opy_()][bstack11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཔ")].add_step(bstack11l1l111ll_opy_)
                threading.current_thread().current_step_uuid = bstack11l1l111ll_opy_[bstack11_opy_ (u"ࠬ࡯ࡤࠨཕ")]
            self.bstack11l111ll11_opy_.append(bstack11l1l111ll_opy_)
    @bstack111lll1lll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111ll1l1ll_opy_()
        self._111ll1l11l_opy_(messages)
        current_test_id = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨབ"), None)
        bstack111ll111l1_opy_ = current_test_id if current_test_id else bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪབྷ"), None)
        bstack11l11111ll_opy_ = bstack11l1111l11_opy_.get(attrs.get(bstack11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨམ")), bstack11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪཙ"))
        bstack11l1111l1l_opy_ = attrs.get(bstack11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཚ"))
        if bstack11l11111ll_opy_ != bstack11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬཛ") and not attrs.get(bstack11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཛྷ")) and self._111lll1111_opy_:
            bstack11l1111l1l_opy_ = self._111lll1111_opy_
        bstack11l1l1l11l_opy_ = Result(result=bstack11l11111ll_opy_, exception=bstack11l1111l1l_opy_, bstack11l11l1l11_opy_=[bstack11l1111l1l_opy_])
        if attrs.get(bstack11_opy_ (u"࠭ࡴࡺࡲࡨࠫཝ"), bstack11_opy_ (u"ࠧࠨཞ")).lower() in [bstack11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧཟ"), bstack11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫའ")]:
            bstack111ll111l1_opy_ = current_test_id if current_test_id else bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ཡ"), None)
            if bstack111ll111l1_opy_:
                bstack11l11l11l1_opy_ = bstack111ll111l1_opy_ + bstack11_opy_ (u"ࠦ࠲ࠨར") + attrs.get(bstack11_opy_ (u"ࠬࡺࡹࡱࡧࠪལ"), bstack11_opy_ (u"࠭ࠧཤ")).lower()
                self._11l111l1ll_opy_[bstack11l11l11l1_opy_][bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཥ")].stop(time=bstack1lllll11ll_opy_(), duration=int(attrs.get(bstack11_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ས"), bstack11_opy_ (u"ࠩ࠳ࠫཧ"))), result=bstack11l1l1l11l_opy_)
                bstack111lllll1_opy_.bstack11l1l1111l_opy_(bstack11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬཨ"), self._11l111l1ll_opy_[bstack11l11l11l1_opy_][bstack11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཀྵ")])
        else:
            bstack111ll111l1_opy_ = current_test_id if current_test_id else bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧཪ"), None)
            if bstack111ll111l1_opy_ and len(self.bstack11l111ll11_opy_) == 1:
                current_step_uuid = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪཫ"), None)
                self._11l111l1ll_opy_[bstack111ll111l1_opy_][bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཬ")].bstack11l11ll111_opy_(current_step_uuid, duration=int(attrs.get(bstack11_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭཭"), bstack11_opy_ (u"ࠩ࠳ࠫ཮"))), result=bstack11l1l1l11l_opy_)
            else:
                self.bstack111lllll11_opy_(attrs)
            self.bstack11l111ll11_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨ཯"), bstack11_opy_ (u"ࠫࡳࡵࠧ཰")) == bstack11_opy_ (u"ࠬࡿࡥࡴཱࠩ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1ll11l1l1_opy_.bstack11l11llll1_opy_():
                logs.append({
                    bstack11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱིࠩ"): bstack1lllll11ll_opy_(),
                    bstack11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཱི"): message.get(bstack11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦུࠩ")),
                    bstack11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨཱུ"): message.get(bstack11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩྲྀ")),
                    **bstack1ll11l1l1_opy_.bstack11l11llll1_opy_()
                })
                if len(logs) > 0:
                    bstack111lllll1_opy_.bstack1l1l11ll11_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack111lllll1_opy_.bstack111ll11l1l_opy_()
    def bstack111lllll11_opy_(self, bstack111ll1llll_opy_):
        if not bstack1ll11l1l1_opy_.bstack11l11llll1_opy_():
            return
        kwname = bstack11_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪཷ").format(bstack111ll1llll_opy_.get(bstack11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬླྀ")), bstack111ll1llll_opy_.get(bstack11_opy_ (u"࠭ࡡࡳࡩࡶࠫཹ"), bstack11_opy_ (u"ࠧࠨེ"))) if bstack111ll1llll_opy_.get(bstack11_opy_ (u"ࠨࡣࡵ࡫ࡸཻ࠭"), []) else bstack111ll1llll_opy_.get(bstack11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦོࠩ"))
        error_message = bstack11_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤཽ").format(kwname, bstack111ll1llll_opy_.get(bstack11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫཾ")), str(bstack111ll1llll_opy_.get(bstack11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཿ"))))
        bstack111ll1ll1l_opy_ = bstack11_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ྀࠦࠧ").format(kwname, bstack111ll1llll_opy_.get(bstack11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹཱྀࠧ")))
        bstack111lll11l1_opy_ = error_message if bstack111ll1llll_opy_.get(bstack11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྂ")) else bstack111ll1ll1l_opy_
        bstack111ll1111l_opy_ = {
            bstack11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬྃ"): self.bstack11l111ll11_opy_[-1].get(bstack11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺ྄ࠧ"), bstack1lllll11ll_opy_()),
            bstack11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ྅"): bstack111lll11l1_opy_,
            bstack11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ྆"): bstack11_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ྇") if bstack111ll1llll_opy_.get(bstack11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧྈ")) == bstack11_opy_ (u"ࠨࡈࡄࡍࡑ࠭ྉ") else bstack11_opy_ (u"ࠩࡌࡒࡋࡕࠧྊ"),
            **bstack1ll11l1l1_opy_.bstack11l11llll1_opy_()
        }
        bstack111lllll1_opy_.bstack1l1l11ll11_opy_([bstack111ll1111l_opy_])
    def _111lll111l_opy_(self):
        for bstack111ll111ll_opy_ in reversed(self._11l111l1ll_opy_):
            bstack111lll1ll1_opy_ = bstack111ll111ll_opy_
            data = self._11l111l1ll_opy_[bstack111ll111ll_opy_][bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྋ")]
            if isinstance(data, bstack11l1l1l1l1_opy_):
                if not bstack11_opy_ (u"ࠫࡊࡇࡃࡉࠩྌ") in data.bstack111ll1lll1_opy_():
                    return bstack111lll1ll1_opy_
            else:
                return bstack111lll1ll1_opy_
    def _111ll1l11l_opy_(self, messages):
        try:
            bstack111ll11ll1_opy_ = BuiltIn().get_variable_value(bstack11_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦྍ")) in (bstack111ll1l111_opy_.DEBUG, bstack111ll1l111_opy_.TRACE)
            for message, bstack111lll1l11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྎ"))
                level = message.get(bstack11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ྏ"))
                if level == bstack111ll1l111_opy_.FAIL:
                    self._111lll1111_opy_ = name or self._111lll1111_opy_
                    self._111ll11l11_opy_ = bstack111lll1l11_opy_.get(bstack11_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤྐ")) if bstack111ll11ll1_opy_ and bstack111lll1l11_opy_ else self._111ll11l11_opy_
        except:
            pass
    @classmethod
    def bstack11l1l1111l_opy_(self, event: str, bstack111lll1l1l_opy_: bstack11l111l11l_opy_, bstack11l111111l_opy_=False):
        if event == bstack11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫྑ"):
            bstack111lll1l1l_opy_.set(hooks=self.store[bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧྒ")])
        if event == bstack11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬྒྷ"):
            event = bstack11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧྔ")
        if bstack11l111111l_opy_:
            bstack111llll111_opy_ = {
                bstack11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪྕ"): event,
                bstack111lll1l1l_opy_.bstack111llll11l_opy_(): bstack111lll1l1l_opy_.bstack111ll1l1l1_opy_(event)
            }
            self.bstack11l1111lll_opy_.append(bstack111llll111_opy_)
        else:
            bstack111lllll1_opy_.bstack11l1l1111l_opy_(event, bstack111lll1l1l_opy_)
class bstack111lll11ll_opy_:
    def __init__(self):
        self._11l1111111_opy_ = []
    def bstack111ll1ll11_opy_(self):
        self._11l1111111_opy_.append([])
    def bstack111ll1l1ll_opy_(self):
        return self._11l1111111_opy_.pop() if self._11l1111111_opy_ else list()
    def push(self, message):
        self._11l1111111_opy_[-1].append(message) if self._11l1111111_opy_ else self._11l1111111_opy_.append([message])
class bstack111ll1l111_opy_:
    FAIL = bstack11_opy_ (u"ࠧࡇࡃࡌࡐࠬྖ")
    ERROR = bstack11_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧྗ")
    WARNING = bstack11_opy_ (u"࡚ࠩࡅࡗࡔࠧ྘")
    bstack11l111l111_opy_ = bstack11_opy_ (u"ࠪࡍࡓࡌࡏࠨྙ")
    DEBUG = bstack11_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪྚ")
    TRACE = bstack11_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫྛ")
    bstack11l11l1111_opy_ = [FAIL, ERROR]
def bstack11l111ll1l_opy_(bstack111llll1l1_opy_):
    if not bstack111llll1l1_opy_:
        return None
    if bstack111llll1l1_opy_.get(bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྜ"), None):
        return getattr(bstack111llll1l1_opy_[bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྜྷ")], bstack11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ྞ"), None)
    return bstack111llll1l1_opy_.get(bstack11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧྟ"), None)
def bstack111lllll1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩྠ"), bstack11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ྡ")]:
        return
    if hook_type.lower() == bstack11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫྡྷ"):
        if current_test_uuid is None:
            return bstack11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪྣ")
        else:
            return bstack11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬྤ")
    elif hook_type.lower() == bstack11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪྥ"):
        if current_test_uuid is None:
            return bstack11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬྦ")
        else:
            return bstack11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧྦྷ")