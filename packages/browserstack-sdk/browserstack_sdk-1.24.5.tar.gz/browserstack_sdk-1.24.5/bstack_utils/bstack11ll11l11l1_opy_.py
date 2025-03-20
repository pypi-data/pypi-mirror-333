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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11ll1l1ll11_opy_
from browserstack_sdk.bstack1l1lllll11_opy_ import bstack1ll111ll_opy_
def _11ll11lllll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11ll11lll11_opy_:
    def __init__(self, handler):
        self._11ll11ll1ll_opy_ = {}
        self._11ll11l11ll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1ll111ll_opy_.version()
        if bstack11ll1l1ll11_opy_(pytest_version, bstack1l11l_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤ᪥")) >= 0:
            self._11ll11ll1ll_opy_[bstack1l11l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᪦")] = Module._register_setup_function_fixture
            self._11ll11ll1ll_opy_[bstack1l11l_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᪧ")] = Module._register_setup_module_fixture
            self._11ll11ll1ll_opy_[bstack1l11l_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᪨")] = Class._register_setup_class_fixture
            self._11ll11ll1ll_opy_[bstack1l11l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᪩")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11ll11l1lll_opy_(bstack1l11l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᪪"))
            Module._register_setup_module_fixture = self.bstack11ll11l1lll_opy_(bstack1l11l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᪫"))
            Class._register_setup_class_fixture = self.bstack11ll11l1lll_opy_(bstack1l11l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᪬"))
            Class._register_setup_method_fixture = self.bstack11ll11l1lll_opy_(bstack1l11l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᪭"))
        else:
            self._11ll11ll1ll_opy_[bstack1l11l_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᪮")] = Module._inject_setup_function_fixture
            self._11ll11ll1ll_opy_[bstack1l11l_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᪯")] = Module._inject_setup_module_fixture
            self._11ll11ll1ll_opy_[bstack1l11l_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᪰")] = Class._inject_setup_class_fixture
            self._11ll11ll1ll_opy_[bstack1l11l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᪱")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11ll11l1lll_opy_(bstack1l11l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᪲"))
            Module._inject_setup_module_fixture = self.bstack11ll11l1lll_opy_(bstack1l11l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᪳"))
            Class._inject_setup_class_fixture = self.bstack11ll11l1lll_opy_(bstack1l11l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᪴"))
            Class._inject_setup_method_fixture = self.bstack11ll11l1lll_opy_(bstack1l11l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ᪵࠭"))
    def bstack11ll1l11111_opy_(self, bstack11ll11ll1l1_opy_, hook_type):
        bstack11ll11l1l1l_opy_ = id(bstack11ll11ll1l1_opy_.__class__)
        if (bstack11ll11l1l1l_opy_, hook_type) in self._11ll11l11ll_opy_:
            return
        meth = getattr(bstack11ll11ll1l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11ll11l11ll_opy_[(bstack11ll11l1l1l_opy_, hook_type)] = meth
            setattr(bstack11ll11ll1l1_opy_, hook_type, self.bstack11ll11ll111_opy_(hook_type, bstack11ll11l1l1l_opy_))
    def bstack11ll11llll1_opy_(self, instance, bstack11ll11l1ll1_opy_):
        if bstack11ll11l1ll1_opy_ == bstack1l11l_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ᪶"):
            self.bstack11ll1l11111_opy_(instance.obj, bstack1l11l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮᪷ࠣ"))
            self.bstack11ll1l11111_opy_(instance.obj, bstack1l11l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲ᪸ࠧ"))
        if bstack11ll11l1ll1_opy_ == bstack1l11l_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧ᪹ࠥ"):
            self.bstack11ll1l11111_opy_(instance.obj, bstack1l11l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤ᪺"))
            self.bstack11ll1l11111_opy_(instance.obj, bstack1l11l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨ᪻"))
        if bstack11ll11l1ll1_opy_ == bstack1l11l_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧ᪼"):
            self.bstack11ll1l11111_opy_(instance.obj, bstack1l11l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶ᪽ࠦ"))
            self.bstack11ll1l11111_opy_(instance.obj, bstack1l11l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣ᪾"))
        if bstack11ll11l1ll1_opy_ == bstack1l11l_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᪿ"):
            self.bstack11ll1l11111_opy_(instance.obj, bstack1l11l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤᫀࠣ"))
            self.bstack11ll1l11111_opy_(instance.obj, bstack1l11l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧ᫁"))
    @staticmethod
    def bstack11ll1l1111l_opy_(hook_type, func, args):
        if hook_type in [bstack1l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ᫂"), bstack1l11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪ᫃ࠧ")]:
            _11ll11lllll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11ll11ll111_opy_(self, hook_type, bstack11ll11l1l1l_opy_):
        def bstack11ll11ll11l_opy_(arg=None):
            self.handler(hook_type, bstack1l11l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ᫄࠭"))
            result = None
            try:
                bstack1111ll1l1l_opy_ = self._11ll11l11ll_opy_[(bstack11ll11l1l1l_opy_, hook_type)]
                self.bstack11ll1l1111l_opy_(hook_type, bstack1111ll1l1l_opy_, (arg,))
                result = Result(result=bstack1l11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᫅"))
            except Exception as e:
                result = Result(result=bstack1l11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᫆"), exception=e)
                self.handler(hook_type, bstack1l11l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ᫇"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l11l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ᫈"), result)
        def bstack11ll11l1l11_opy_(this, arg=None):
            self.handler(hook_type, bstack1l11l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ᫉"))
            result = None
            exception = None
            try:
                self.bstack11ll1l1111l_opy_(hook_type, self._11ll11l11ll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨ᫊ࠬ"))
            except Exception as e:
                result = Result(result=bstack1l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᫋"), exception=e)
                self.handler(hook_type, bstack1l11l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᫌ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l11l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᫍ"), result)
        if hook_type in [bstack1l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᫎ"), bstack1l11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ᫏")]:
            return bstack11ll11l1l11_opy_
        return bstack11ll11ll11l_opy_
    def bstack11ll11l1lll_opy_(self, bstack11ll11l1ll1_opy_):
        def bstack11ll11lll1l_opy_(this, *args, **kwargs):
            self.bstack11ll11llll1_opy_(this, bstack11ll11l1ll1_opy_)
            self._11ll11ll1ll_opy_[bstack11ll11l1ll1_opy_](this, *args, **kwargs)
        return bstack11ll11lll1l_opy_