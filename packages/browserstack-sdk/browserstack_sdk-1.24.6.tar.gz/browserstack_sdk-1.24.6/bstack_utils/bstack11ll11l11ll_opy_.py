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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11llll111l1_opy_
from browserstack_sdk.bstack1l1111lll1_opy_ import bstack11l11l1ll_opy_
def _11ll11lllll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11ll11ll11l_opy_:
    def __init__(self, handler):
        self._11ll11lll1l_opy_ = {}
        self._11ll1l1111l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11l11l1ll_opy_.version()
        if bstack11llll111l1_opy_(pytest_version, bstack11_opy_ (u"ࠦ࠽࠴࠱࠯࠳ࠥ᪦")) >= 0:
            self._11ll11lll1l_opy_[bstack11_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᪧ")] = Module._register_setup_function_fixture
            self._11ll11lll1l_opy_[bstack11_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᪨")] = Module._register_setup_module_fixture
            self._11ll11lll1l_opy_[bstack11_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᪩")] = Class._register_setup_class_fixture
            self._11ll11lll1l_opy_[bstack11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᪪")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11ll11l1l1l_opy_(bstack11_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᪫"))
            Module._register_setup_module_fixture = self.bstack11ll11l1l1l_opy_(bstack11_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᪬"))
            Class._register_setup_class_fixture = self.bstack11ll11l1l1l_opy_(bstack11_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᪭"))
            Class._register_setup_method_fixture = self.bstack11ll11l1l1l_opy_(bstack11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᪮"))
        else:
            self._11ll11lll1l_opy_[bstack11_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᪯")] = Module._inject_setup_function_fixture
            self._11ll11lll1l_opy_[bstack11_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᪰")] = Module._inject_setup_module_fixture
            self._11ll11lll1l_opy_[bstack11_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᪱")] = Class._inject_setup_class_fixture
            self._11ll11lll1l_opy_[bstack11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᪲")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11ll11l1l1l_opy_(bstack11_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᪳"))
            Module._inject_setup_module_fixture = self.bstack11ll11l1l1l_opy_(bstack11_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᪴"))
            Class._inject_setup_class_fixture = self.bstack11ll11l1l1l_opy_(bstack11_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩ᪵ࠬ"))
            Class._inject_setup_method_fixture = self.bstack11ll11l1l1l_opy_(bstack11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫᪶ࠧ"))
    def bstack11ll11ll1ll_opy_(self, bstack11ll11l11l1_opy_, hook_type):
        bstack11ll11lll11_opy_ = id(bstack11ll11l11l1_opy_.__class__)
        if (bstack11ll11lll11_opy_, hook_type) in self._11ll1l1111l_opy_:
            return
        meth = getattr(bstack11ll11l11l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11ll1l1111l_opy_[(bstack11ll11lll11_opy_, hook_type)] = meth
            setattr(bstack11ll11l11l1_opy_, hook_type, self.bstack11ll11l1ll1_opy_(hook_type, bstack11ll11lll11_opy_))
    def bstack11ll11ll1l1_opy_(self, instance, bstack11ll11ll111_opy_):
        if bstack11ll11ll111_opy_ == bstack11_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧ᪷ࠥ"):
            self.bstack11ll11ll1ll_opy_(instance.obj, bstack11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤ᪸"))
            self.bstack11ll11ll1ll_opy_(instance.obj, bstack11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨ᪹"))
        if bstack11ll11ll111_opy_ == bstack11_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨ᪺ࠦ"):
            self.bstack11ll11ll1ll_opy_(instance.obj, bstack11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥ᪻"))
            self.bstack11ll11ll1ll_opy_(instance.obj, bstack11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢ᪼"))
        if bstack11ll11ll111_opy_ == bstack11_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨ᪽"):
            self.bstack11ll11ll1ll_opy_(instance.obj, bstack11_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧ᪾"))
            self.bstack11ll11ll1ll_opy_(instance.obj, bstack11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤᪿ"))
        if bstack11ll11ll111_opy_ == bstack11_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧᫀࠥ"):
            self.bstack11ll11ll1ll_opy_(instance.obj, bstack11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤ᫁"))
            self.bstack11ll11ll1ll_opy_(instance.obj, bstack11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨ᫂"))
    @staticmethod
    def bstack11ll1l11111_opy_(hook_type, func, args):
        if hook_type in [bstack11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧ᫃ࠫ"), bstack11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨ᫄")]:
            _11ll11lllll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11ll11l1ll1_opy_(self, hook_type, bstack11ll11lll11_opy_):
        def bstack11ll11l1lll_opy_(arg=None):
            self.handler(hook_type, bstack11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ᫅"))
            result = None
            try:
                bstack111l1111l1_opy_ = self._11ll1l1111l_opy_[(bstack11ll11lll11_opy_, hook_type)]
                self.bstack11ll1l11111_opy_(hook_type, bstack111l1111l1_opy_, (arg,))
                result = Result(result=bstack11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᫆"))
            except Exception as e:
                result = Result(result=bstack11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᫇"), exception=e)
                self.handler(hook_type, bstack11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ᫈"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ᫉"), result)
        def bstack11ll11llll1_opy_(this, arg=None):
            self.handler(hook_type, bstack11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩ᫊ࠬ"))
            result = None
            exception = None
            try:
                self.bstack11ll1l11111_opy_(hook_type, self._11ll1l1111l_opy_[hook_type], (this, arg))
                result = Result(result=bstack11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᫋"))
            except Exception as e:
                result = Result(result=bstack11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᫌ"), exception=e)
                self.handler(hook_type, bstack11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᫍ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᫎ"), result)
        if hook_type in [bstack11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ᫏"), bstack11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭᫐")]:
            return bstack11ll11llll1_opy_
        return bstack11ll11l1lll_opy_
    def bstack11ll11l1l1l_opy_(self, bstack11ll11ll111_opy_):
        def bstack11ll11l1l11_opy_(this, *args, **kwargs):
            self.bstack11ll11ll1l1_opy_(this, bstack11ll11ll111_opy_)
            self._11ll11lll1l_opy_[bstack11ll11ll111_opy_](this, *args, **kwargs)
        return bstack11ll11l1l11_opy_