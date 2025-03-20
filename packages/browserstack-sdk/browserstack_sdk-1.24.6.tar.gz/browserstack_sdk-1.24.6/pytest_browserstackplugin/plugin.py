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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1l1ll1111_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1l1lll1l_opy_, bstack1ll1llll11_opy_, update, bstack1llll111l_opy_,
                                       bstack11l1l1l1l_opy_, bstack11l1lll111_opy_, bstack11ll1lll_opy_, bstack1l111ll11l_opy_,
                                       bstack11lllllll1_opy_, bstack1ll11lll1_opy_, bstack11ll1l1lll_opy_, bstack11lll1ll1l_opy_,
                                       bstack1llll11l1l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1111l1_opy_)
from browserstack_sdk.bstack1l1111lll1_opy_ import bstack11l11l1ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11l11l1l_opy_
from bstack_utils.capture import bstack11l1l111l1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l111111_opy_, bstack111l111l_opy_, bstack1l11111l11_opy_, \
    bstack1ll1llll_opy_
from bstack_utils.helper import bstack1llllll111_opy_, bstack11ll1l11lll_opy_, bstack11l111l1l1_opy_, bstack1ll11l11l1_opy_, bstack1ll1111l1l1_opy_, bstack1lllll11ll_opy_, \
    bstack11ll1l11l1l_opy_, \
    bstack11llllllll1_opy_, bstack111l111l1_opy_, bstack111l11ll1_opy_, bstack11lll1ll111_opy_, bstack11l1ll11ll_opy_, Notset, \
    bstack11111111_opy_, bstack11llll111ll_opy_, bstack11lll11l1l1_opy_, Result, bstack11llllll1ll_opy_, bstack11ll1ll1l11_opy_, bstack111lll1lll_opy_, \
    bstack1llll1lll_opy_, bstack11111ll1l_opy_, bstack11l1l1l11_opy_, bstack11lll1l111l_opy_
from bstack_utils.bstack11ll11l11ll_opy_ import bstack11ll11ll11l_opy_
from bstack_utils.messages import bstack1l11l11l1_opy_, bstack111ll11l1_opy_, bstack1lll11lll1_opy_, bstack111l1llll_opy_, bstack1llll111ll_opy_, \
    bstack11l1ll1l1_opy_, bstack11l1l11l1_opy_, bstack1l111l11l1_opy_, bstack11lll11l_opy_, bstack1111llll1_opy_, \
    bstack11l1llll1_opy_, bstack1lll1l1lll_opy_
from bstack_utils.proxy import bstack111111l11_opy_, bstack11l11llll_opy_
from bstack_utils.bstack1ll11ll11l_opy_ import bstack11l111ll1l1_opy_, bstack11l111llll1_opy_, bstack11l111l1ll1_opy_, bstack11l111ll1ll_opy_, \
    bstack11l11l111l1_opy_, bstack11l11l1111l_opy_, bstack11l111lll11_opy_, bstack11lll1llll_opy_, bstack11l111l1l1l_opy_
from bstack_utils.bstack1lllllll11_opy_ import bstack1lll1111ll_opy_
from bstack_utils.bstack1l111l11ll_opy_ import bstack1l1ll1llll_opy_, bstack11l1lll1l_opy_, bstack1l1l1ll1l_opy_, \
    bstack1l111l111_opy_, bstack1ll11ll1ll_opy_
from bstack_utils.bstack11l1l11l1l_opy_ import bstack11l11lll11_opy_
from bstack_utils.bstack11l11l1l1l_opy_ import bstack1ll11l1l1_opy_
import bstack_utils.accessibility as bstack1111l1111_opy_
from bstack_utils.bstack11l11l111l_opy_ import bstack111lllll1_opy_
from bstack_utils.bstack1l11l11l11_opy_ import bstack1l11l11l11_opy_
from browserstack_sdk.__init__ import bstack11l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1111l_opy_ import bstack1lllll111l1_opy_
from browserstack_sdk.sdk_cli.bstack11ll1l1ll1_opy_ import bstack11ll1l1ll1_opy_, bstack11lllll111_opy_, bstack1l1lll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l1l1l11l11_opy_, bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11ll1l1ll1_opy_ import bstack11ll1l1ll1_opy_, bstack11lllll111_opy_, bstack1l1lll1l1_opy_
bstack1lll111111_opy_ = None
bstack11ll1ll11l_opy_ = None
bstack1llll1l1l_opy_ = None
bstack1l1l1l1l_opy_ = None
bstack1lll1lll11_opy_ = None
bstack1ll11l1l_opy_ = None
bstack1ll1l1l1l1_opy_ = None
bstack1ll1l11l1l_opy_ = None
bstack1111ll1ll_opy_ = None
bstack1ll1ll111l_opy_ = None
bstack1l1lll1ll1_opy_ = None
bstack11l1ll11l1_opy_ = None
bstack1l1lll1l1l_opy_ = None
bstack1l1ll111ll_opy_ = bstack11_opy_ (u"ࠫࠬḘ")
CONFIG = {}
bstack1111ll1l_opy_ = False
bstack1ll111ll1_opy_ = bstack11_opy_ (u"ࠬ࠭ḙ")
bstack1l11l111_opy_ = bstack11_opy_ (u"࠭ࠧḚ")
bstack11llll11_opy_ = False
bstack1l1lll1ll_opy_ = []
bstack11l11ll11_opy_ = bstack1l111111_opy_
bstack111l1ll111l_opy_ = bstack11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧḛ")
bstack1l1lll111l_opy_ = {}
bstack1ll111lll1_opy_ = None
bstack11l1l11ll_opy_ = False
logger = bstack11l11l1l_opy_.get_logger(__name__, bstack11l11ll11_opy_)
store = {
    bstack11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬḜ"): []
}
bstack111l1lll11l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11l111l1ll_opy_ = {}
current_test_uuid = None
cli_context = bstack1l1l1l11l11_opy_(
    test_framework_name=bstack1ll1ll11ll_opy_[bstack11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ḝ")] if bstack11l1ll11ll_opy_() else bstack1ll1ll11ll_opy_[bstack11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࠪḞ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1l1l1l11l1_opy_(page, bstack1llll1l1l1_opy_):
    try:
        page.evaluate(bstack11_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧḟ"),
                      bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩḠ") + json.dumps(
                          bstack1llll1l1l1_opy_) + bstack11_opy_ (u"ࠨࡽࡾࠤḡ"))
    except Exception as e:
        print(bstack11_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧḢ"), e)
def bstack1l1lll11_opy_(page, message, level):
    try:
        page.evaluate(bstack11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤḣ"), bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧḤ") + json.dumps(
            message) + bstack11_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭ḥ") + json.dumps(level) + bstack11_opy_ (u"ࠫࢂࢃࠧḦ"))
    except Exception as e:
        print(bstack11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣḧ"), e)
def pytest_configure(config):
    global bstack1ll111ll1_opy_
    global CONFIG
    bstack1l1l1lll1_opy_ = Config.bstack11l111l11_opy_()
    config.args = bstack1ll11l1l1_opy_.bstack111ll111l11_opy_(config.args)
    bstack1l1l1lll1_opy_.bstack1lll1ll11l_opy_(bstack11l1l1l11_opy_(config.getoption(bstack11_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪḨ"))))
    try:
        bstack11l11l1l_opy_.bstack11ll1111l11_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11ll1l1ll1_opy_.invoke(bstack11lllll111_opy_.CONNECT, bstack1l1lll1l1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧḩ"), bstack11_opy_ (u"ࠨ࠲ࠪḪ")))
        config = json.loads(os.environ.get(bstack11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠣḫ"), bstack11_opy_ (u"ࠥࡿࢂࠨḬ")))
        cli.bstack1llll11l1l1_opy_(bstack111l11ll1_opy_(bstack1ll111ll1_opy_, CONFIG), cli_context.platform_index, bstack1llll111l_opy_)
    if cli.bstack1llllll1lll_opy_(bstack1lllll111l1_opy_):
        cli.bstack1llllll11l1_opy_()
        logger.debug(bstack11_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥḭ") + str(cli_context.platform_index) + bstack11_opy_ (u"ࠧࠨḮ"))
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.BEFORE_ALL, bstack111111l1ll_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11_opy_ (u"ࠨࡷࡩࡧࡱࠦḯ"), None)
    if cli.is_running() and when == bstack11_opy_ (u"ࠢࡤࡣ࡯ࡰࠧḰ"):
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.LOG_REPORT, bstack111111l1ll_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack11_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢḱ"):
            cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.BEFORE_EACH, bstack111111l1ll_opy_.POST, item, call, outcome)
        elif when == bstack11_opy_ (u"ࠤࡦࡥࡱࡲࠢḲ"):
            cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.LOG_REPORT, bstack111111l1ll_opy_.POST, item, call, outcome)
        elif when == bstack11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧḳ"):
            cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.AFTER_EACH, bstack111111l1ll_opy_.POST, item, call, outcome)
        return # skip all existing bstack111l1llllll_opy_
    bstack111l1l1l11l_opy_ = item.config.getoption(bstack11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ḵ"))
    plugins = item.config.getoption(bstack11_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨḵ"))
    report = outcome.get_result()
    bstack111l1lll1ll_opy_(item, call, report)
    if bstack11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦḶ") not in plugins or bstack11l1ll11ll_opy_():
        return
    summary = []
    driver = getattr(item, bstack11_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣḷ"), None)
    page = getattr(item, bstack11_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢḸ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack111l1l1llll_opy_(item, report, summary, bstack111l1l1l11l_opy_)
    if (page is not None):
        bstack111l1l11l1l_opy_(item, report, summary, bstack111l1l1l11l_opy_)
def bstack111l1l1llll_opy_(item, report, summary, bstack111l1l1l11l_opy_):
    if report.when == bstack11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨḹ") and report.skipped:
        bstack11l111l1l1l_opy_(report)
    if report.when in [bstack11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤḺ"), bstack11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨḻ")]:
        return
    if not bstack1ll1111l1l1_opy_():
        return
    try:
        if (str(bstack111l1l1l11l_opy_).lower() != bstack11_opy_ (u"ࠬࡺࡲࡶࡧࠪḼ") and not cli.is_running()):
            item._driver.execute_script(
                bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫḽ") + json.dumps(
                    report.nodeid) + bstack11_opy_ (u"ࠧࡾࡿࠪḾ"))
        os.environ[bstack11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫḿ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤṀ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧṁ")))
    bstack1l1l111ll_opy_ = bstack11_opy_ (u"ࠦࠧṂ")
    bstack11l111l1l1l_opy_(report)
    if not passed:
        try:
            bstack1l1l111ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧṃ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l111ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣṄ")))
        bstack1l1l111ll_opy_ = bstack11_opy_ (u"ࠢࠣṅ")
        if not passed:
            try:
                bstack1l1l111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣṆ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l111ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ṇ")
                    + json.dumps(bstack11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦṈ"))
                    + bstack11_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢṉ")
                )
            else:
                item._driver.execute_script(
                    bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪṊ")
                    + json.dumps(str(bstack1l1l111ll_opy_))
                    + bstack11_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤṋ")
                )
        except Exception as e:
            summary.append(bstack11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧṌ").format(e))
def bstack111ll11111l_opy_(test_name, error_message):
    try:
        bstack111l1ll1lll_opy_ = []
        bstack1l1l1111ll_opy_ = os.environ.get(bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨṍ"), bstack11_opy_ (u"ࠩ࠳ࠫṎ"))
        bstack1lllll1111_opy_ = {bstack11_opy_ (u"ࠪࡲࡦࡳࡥࠨṏ"): test_name, bstack11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪṐ"): error_message, bstack11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫṑ"): bstack1l1l1111ll_opy_}
        bstack111ll111111_opy_ = os.path.join(tempfile.gettempdir(), bstack11_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫṒ"))
        if os.path.exists(bstack111ll111111_opy_):
            with open(bstack111ll111111_opy_) as f:
                bstack111l1ll1lll_opy_ = json.load(f)
        bstack111l1ll1lll_opy_.append(bstack1lllll1111_opy_)
        with open(bstack111ll111111_opy_, bstack11_opy_ (u"ࠧࡸࠩṓ")) as f:
            json.dump(bstack111l1ll1lll_opy_, f)
    except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭Ṕ") + str(e))
def bstack111l1l11l1l_opy_(item, report, summary, bstack111l1l1l11l_opy_):
    if report.when in [bstack11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣṕ"), bstack11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧṖ")]:
        return
    if (str(bstack111l1l1l11l_opy_).lower() != bstack11_opy_ (u"ࠫࡹࡸࡵࡦࠩṗ")):
        bstack1l1l1l11l1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢṘ")))
    bstack1l1l111ll_opy_ = bstack11_opy_ (u"ࠨࠢṙ")
    bstack11l111l1l1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1l111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢṚ").format(e)
                )
        try:
            if passed:
                bstack1ll11ll1ll_opy_(getattr(item, bstack11_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧṛ"), None), bstack11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤṜ"))
            else:
                error_message = bstack11_opy_ (u"ࠪࠫṝ")
                if bstack1l1l111ll_opy_:
                    bstack1l1lll11_opy_(item._page, str(bstack1l1l111ll_opy_), bstack11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥṞ"))
                    bstack1ll11ll1ll_opy_(getattr(item, bstack11_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫṟ"), None), bstack11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨṠ"), str(bstack1l1l111ll_opy_))
                    error_message = str(bstack1l1l111ll_opy_)
                else:
                    bstack1ll11ll1ll_opy_(getattr(item, bstack11_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ṡ"), None), bstack11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣṢ"))
                bstack111ll11111l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨṣ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢṤ"), default=bstack11_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥṥ"), help=bstack11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦṦ"))
    parser.addoption(bstack11_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧṧ"), default=bstack11_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨṨ"), help=bstack11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢṩ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦṪ"), action=bstack11_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤṫ"), default=bstack11_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦṬ"),
                         help=bstack11_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦṭ"))
def bstack11l11lllll_opy_(log):
    if not (log[bstack11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧṮ")] and log[bstack11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨṯ")].strip()):
        return
    active = bstack11l11llll1_opy_()
    log = {
        bstack11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧṰ"): log[bstack11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨṱ")],
        bstack11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭Ṳ"): bstack11l111l1l1_opy_().isoformat() + bstack11_opy_ (u"ࠫ࡟࠭ṳ"),
        bstack11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ṵ"): log[bstack11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧṵ")],
    }
    if active:
        if active[bstack11_opy_ (u"ࠧࡵࡻࡳࡩࠬṶ")] == bstack11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ṷ"):
            log[bstack11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩṸ")] = active[bstack11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪṹ")]
        elif active[bstack11_opy_ (u"ࠫࡹࡿࡰࡦࠩṺ")] == bstack11_opy_ (u"ࠬࡺࡥࡴࡶࠪṻ"):
            log[bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ṽ")] = active[bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧṽ")]
    bstack111lllll1_opy_.bstack1l1l11ll11_opy_([log])
def bstack11l11llll1_opy_():
    if len(store[bstack11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬṾ")]) > 0 and store[bstack11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ṿ")][-1]:
        return {
            bstack11_opy_ (u"ࠪࡸࡾࡶࡥࠨẀ"): bstack11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩẁ"),
            bstack11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẂ"): store[bstack11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪẃ")][-1]
        }
    if store.get(bstack11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫẄ"), None):
        return {
            bstack11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ẅ"): bstack11_opy_ (u"ࠩࡷࡩࡸࡺࠧẆ"),
            bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪẇ"): store[bstack11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨẈ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.INIT_TEST, bstack111111l1ll_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.INIT_TEST, bstack111111l1ll_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.TEST, bstack111111l1ll_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._111l1ll1111_opy_ = True
        bstack11l1lllll1_opy_ = bstack1111l1111_opy_.bstack11ll1lllll_opy_(bstack11llllllll1_opy_(item.own_markers))
        if not cli.bstack1llllll1lll_opy_(bstack1lllll111l1_opy_):
            item._a11y_test_case = bstack11l1lllll1_opy_
            if bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫẉ"), None):
                driver = getattr(item, bstack11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧẊ"), None)
                item._a11y_started = bstack1111l1111_opy_.bstack1111ll111_opy_(driver, bstack11l1lllll1_opy_)
        if not bstack111lllll1_opy_.on() or bstack111l1ll111l_opy_ != bstack11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧẋ"):
            return
        global current_test_uuid #, bstack11l11l11ll_opy_
        bstack111llll1l1_opy_ = {
            bstack11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ẍ"): uuid4().__str__(),
            bstack11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ẍ"): bstack11l111l1l1_opy_().isoformat() + bstack11_opy_ (u"ࠪ࡞ࠬẎ")
        }
        current_test_uuid = bstack111llll1l1_opy_[bstack11_opy_ (u"ࠫࡺࡻࡩࡥࠩẏ")]
        store[bstack11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩẐ")] = bstack111llll1l1_opy_[bstack11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫẑ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11l111l1ll_opy_[item.nodeid] = {**_11l111l1ll_opy_[item.nodeid], **bstack111llll1l1_opy_}
        bstack111l1lll111_opy_(item, _11l111l1ll_opy_[item.nodeid], bstack11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨẒ"))
    except Exception as err:
        print(bstack11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪẓ"), str(err))
def pytest_runtest_setup(item):
    store[bstack11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭Ẕ")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.BEFORE_EACH, bstack111111l1ll_opy_.PRE, item, bstack11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩẕ"))
        return # skip all existing bstack111l1llllll_opy_
    global bstack111l1lll11l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11lll1ll111_opy_():
        atexit.register(bstack11lll1l1l1_opy_)
        if not bstack111l1lll11l_opy_:
            try:
                bstack111l1l11lll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11lll1l111l_opy_():
                    bstack111l1l11lll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack111l1l11lll_opy_:
                    signal.signal(s, bstack111l1l1l1ll_opy_)
                bstack111l1lll11l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡩ࡬ࡷࡹ࡫ࡲࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡪࡤࡲࡩࡲࡥࡳࡵ࠽ࠤࠧẖ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11l111ll1l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬẗ")
    try:
        if not bstack111lllll1_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111llll1l1_opy_ = {
            bstack11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫẘ"): uuid,
            bstack11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫẙ"): bstack11l111l1l1_opy_().isoformat() + bstack11_opy_ (u"ࠨ࡜ࠪẚ"),
            bstack11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧẛ"): bstack11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨẜ"),
            bstack11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧẝ"): bstack11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪẞ"),
            bstack11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩẟ"): bstack11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭Ạ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬạ")] = item
        store[bstack11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭Ả")] = [uuid]
        if not _11l111l1ll_opy_.get(item.nodeid, None):
            _11l111l1ll_opy_[item.nodeid] = {bstack11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩả"): [], bstack11_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭Ấ"): []}
        _11l111l1ll_opy_[item.nodeid][bstack11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫấ")].append(bstack111llll1l1_opy_[bstack11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫẦ")])
        _11l111l1ll_opy_[item.nodeid + bstack11_opy_ (u"ࠧ࠮ࡵࡨࡸࡺࡶࠧầ")] = bstack111llll1l1_opy_
        bstack111l1l1l1l1_opy_(item, bstack111llll1l1_opy_, bstack11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩẨ"))
    except Exception as err:
        print(bstack11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬẩ"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.TEST, bstack111111l1ll_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.AFTER_EACH, bstack111111l1ll_opy_.PRE, item, bstack11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬẪ"))
        return # skip all existing bstack111l1llllll_opy_
    try:
        global bstack1l1lll111l_opy_
        bstack1l1l1111ll_opy_ = 0
        if bstack11llll11_opy_ is True:
            bstack1l1l1111ll_opy_ = int(os.environ.get(bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫẫ")))
        if bstack111ll1l1l_opy_.bstack111ll11l_opy_() == bstack11_opy_ (u"ࠧࡺࡲࡶࡧࠥẬ"):
            if bstack111ll1l1l_opy_.bstack1l1lll11l_opy_() == bstack11_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣậ"):
                bstack111l1llll1l_opy_ = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪẮ"), None)
                bstack1111l111l_opy_ = bstack111l1llll1l_opy_ + bstack11_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦắ")
                driver = getattr(item, bstack11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪẰ"), None)
                bstack1l11111ll_opy_ = getattr(item, bstack11_opy_ (u"ࠪࡲࡦࡳࡥࠨằ"), None)
                bstack1ll1111l11_opy_ = getattr(item, bstack11_opy_ (u"ࠫࡺࡻࡩࡥࠩẲ"), None)
                PercySDK.screenshot(driver, bstack1111l111l_opy_, bstack1l11111ll_opy_=bstack1l11111ll_opy_, bstack1ll1111l11_opy_=bstack1ll1111l11_opy_, bstack1ll1ll1ll_opy_=bstack1l1l1111ll_opy_)
        if not cli.bstack1llllll1lll_opy_(bstack1lllll111l1_opy_):
            if getattr(item, bstack11_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬẳ"), False):
                bstack11l11l1ll_opy_.bstack1lll111l_opy_(getattr(item, bstack11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧẴ"), None), bstack1l1lll111l_opy_, logger, item)
        if not bstack111lllll1_opy_.on():
            return
        bstack111llll1l1_opy_ = {
            bstack11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬẵ"): uuid4().__str__(),
            bstack11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬẶ"): bstack11l111l1l1_opy_().isoformat() + bstack11_opy_ (u"ࠩ࡝ࠫặ"),
            bstack11_opy_ (u"ࠪࡸࡾࡶࡥࠨẸ"): bstack11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩẹ"),
            bstack11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨẺ"): bstack11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪẻ"),
            bstack11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪẼ"): bstack11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪẽ")
        }
        _11l111l1ll_opy_[item.nodeid + bstack11_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬẾ")] = bstack111llll1l1_opy_
        bstack111l1l1l1l1_opy_(item, bstack111llll1l1_opy_, bstack11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫế"))
    except Exception as err:
        print(bstack11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪỀ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack11l111ll1ll_opy_(fixturedef.argname):
        store[bstack11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫề")] = request.node
    elif bstack11l11l111l1_opy_(fixturedef.argname):
        store[bstack11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫỂ")] = request.node
    if not bstack111lllll1_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.SETUP_FIXTURE, bstack111111l1ll_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.SETUP_FIXTURE, bstack111111l1ll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack111l1llllll_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.SETUP_FIXTURE, bstack111111l1ll_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.SETUP_FIXTURE, bstack111111l1ll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack111l1llllll_opy_
    try:
        fixture = {
            bstack11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬể"): fixturedef.argname,
            bstack11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨỄ"): bstack11ll1l11l1l_opy_(outcome),
            bstack11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫễ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧỆ")]
        if not _11l111l1ll_opy_.get(current_test_item.nodeid, None):
            _11l111l1ll_opy_[current_test_item.nodeid] = {bstack11_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ệ"): []}
        _11l111l1ll_opy_[current_test_item.nodeid][bstack11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧỈ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩỉ"), str(err))
if bstack11l1ll11ll_opy_() and bstack111lllll1_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.STEP, bstack111111l1ll_opy_.PRE, request, step)
            return
        try:
            _11l111l1ll_opy_[request.node.nodeid][bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪỊ")].bstack1lllll11l_opy_(id(step))
        except Exception as err:
            print(bstack11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ị"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.STEP, bstack111111l1ll_opy_.POST, request, step, exception)
            return
        try:
            _11l111l1ll_opy_[request.node.nodeid][bstack11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬỌ")].bstack11l11ll111_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧọ"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.STEP, bstack111111l1ll_opy_.POST, request, step)
            return
        try:
            bstack11l1l11l1l_opy_: bstack11l11lll11_opy_ = _11l111l1ll_opy_[request.node.nodeid][bstack11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧỎ")]
            bstack11l1l11l1l_opy_.bstack11l11ll111_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩỏ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack111l1ll111l_opy_
        try:
            if not bstack111lllll1_opy_.on() or bstack111l1ll111l_opy_ != bstack11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪỐ"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.TEST, bstack111111l1ll_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ố"), None)
            if not _11l111l1ll_opy_.get(request.node.nodeid, None):
                _11l111l1ll_opy_[request.node.nodeid] = {}
            bstack11l1l11l1l_opy_ = bstack11l11lll11_opy_.bstack111llll1ll1_opy_(
                scenario, feature, request.node,
                name=bstack11l11l1111l_opy_(request.node, scenario),
                started_at=bstack1lllll11ll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪỒ"),
                tags=bstack11l111lll11_opy_(feature, scenario),
                bstack11l1l11111_opy_=bstack111lllll1_opy_.bstack11l1l11lll_opy_(driver) if driver and driver.session_id else {}
            )
            _11l111l1ll_opy_[request.node.nodeid][bstack11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬồ")] = bstack11l1l11l1l_opy_
            bstack111l1lllll1_opy_(bstack11l1l11l1l_opy_.uuid)
            bstack111lllll1_opy_.bstack11l1l1111l_opy_(bstack11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫỔ"), bstack11l1l11l1l_opy_)
        except Exception as err:
            print(bstack11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ổ"), str(err))
def bstack111l1ll1ll1_opy_(bstack11l11lll1l_opy_):
    if bstack11l11lll1l_opy_ in store[bstack11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩỖ")]:
        store[bstack11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪỗ")].remove(bstack11l11lll1l_opy_)
def bstack111l1lllll1_opy_(test_uuid):
    store[bstack11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫỘ")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack111lllll1_opy_.bstack111lll11lll_opy_
def bstack111l1lll1ll_opy_(item, call, report):
    logger.debug(bstack11_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡳࡶࠪộ"))
    global bstack111l1ll111l_opy_
    bstack1ll1l11111_opy_ = bstack1lllll11ll_opy_()
    if hasattr(report, bstack11_opy_ (u"ࠩࡶࡸࡴࡶࠧỚ")):
        bstack1ll1l11111_opy_ = bstack11llllll1ll_opy_(report.stop)
    elif hasattr(report, bstack11_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩớ")):
        bstack1ll1l11111_opy_ = bstack11llllll1ll_opy_(report.start)
    try:
        if getattr(report, bstack11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩỜ"), bstack11_opy_ (u"ࠬ࠭ờ")) == bstack11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫỞ"):
            logger.debug(bstack11_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩở").format(getattr(report, bstack11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭Ỡ"), bstack11_opy_ (u"ࠩࠪỡ")).__str__(), bstack111l1ll111l_opy_))
            if bstack111l1ll111l_opy_ == bstack11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪỢ"):
                _11l111l1ll_opy_[item.nodeid][bstack11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩợ")] = bstack1ll1l11111_opy_
                bstack111l1lll111_opy_(item, _11l111l1ll_opy_[item.nodeid], bstack11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧỤ"), report, call)
                store[bstack11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪụ")] = None
            elif bstack111l1ll111l_opy_ == bstack11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦỦ"):
                bstack11l1l11l1l_opy_ = _11l111l1ll_opy_[item.nodeid][bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫủ")]
                bstack11l1l11l1l_opy_.set(hooks=_11l111l1ll_opy_[item.nodeid].get(bstack11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨỨ"), []))
                exception, bstack11l11l1l11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l11l1l11_opy_ = [call.excinfo.exconly(), getattr(report, bstack11_opy_ (u"ࠪࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠩứ"), bstack11_opy_ (u"ࠫࠬỪ"))]
                bstack11l1l11l1l_opy_.stop(time=bstack1ll1l11111_opy_, result=Result(result=getattr(report, bstack11_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭ừ"), bstack11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ử")), exception=exception, bstack11l11l1l11_opy_=bstack11l11l1l11_opy_))
                bstack111lllll1_opy_.bstack11l1l1111l_opy_(bstack11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩử"), _11l111l1ll_opy_[item.nodeid][bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫỮ")])
        elif getattr(report, bstack11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧữ"), bstack11_opy_ (u"ࠪࠫỰ")) in [bstack11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪự"), bstack11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧỲ")]:
            logger.debug(bstack11_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨỳ").format(getattr(report, bstack11_opy_ (u"ࠧࡸࡪࡨࡲࠬỴ"), bstack11_opy_ (u"ࠨࠩỵ")).__str__(), bstack111l1ll111l_opy_))
            bstack11l11l11l1_opy_ = item.nodeid + bstack11_opy_ (u"ࠩ࠰ࠫỶ") + getattr(report, bstack11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨỷ"), bstack11_opy_ (u"ࠫࠬỸ"))
            if getattr(report, bstack11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ỹ"), False):
                hook_type = bstack11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫỺ") if getattr(report, bstack11_opy_ (u"ࠧࡸࡪࡨࡲࠬỻ"), bstack11_opy_ (u"ࠨࠩỼ")) == bstack11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨỽ") else bstack11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧỾ")
                _11l111l1ll_opy_[bstack11l11l11l1_opy_] = {
                    bstack11_opy_ (u"ࠫࡺࡻࡩࡥࠩỿ"): uuid4().__str__(),
                    bstack11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩἀ"): bstack1ll1l11111_opy_,
                    bstack11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩἁ"): hook_type
                }
            _11l111l1ll_opy_[bstack11l11l11l1_opy_][bstack11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬἂ")] = bstack1ll1l11111_opy_
            bstack111l1ll1ll1_opy_(_11l111l1ll_opy_[bstack11l11l11l1_opy_][bstack11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ἃ")])
            bstack111l1l1l1l1_opy_(item, _11l111l1ll_opy_[bstack11l11l11l1_opy_], bstack11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫἄ"), report, call)
            if getattr(report, bstack11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨἅ"), bstack11_opy_ (u"ࠫࠬἆ")) == bstack11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫἇ"):
                if getattr(report, bstack11_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧἈ"), bstack11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧἉ")) == bstack11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨἊ"):
                    bstack111llll1l1_opy_ = {
                        bstack11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧἋ"): uuid4().__str__(),
                        bstack11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧἌ"): bstack1lllll11ll_opy_(),
                        bstack11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩἍ"): bstack1lllll11ll_opy_()
                    }
                    _11l111l1ll_opy_[item.nodeid] = {**_11l111l1ll_opy_[item.nodeid], **bstack111llll1l1_opy_}
                    bstack111l1lll111_opy_(item, _11l111l1ll_opy_[item.nodeid], bstack11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ἆ"))
                    bstack111l1lll111_opy_(item, _11l111l1ll_opy_[item.nodeid], bstack11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨἏ"), report, call)
    except Exception as err:
        print(bstack11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬἐ"), str(err))
def bstack111l1l1ll11_opy_(test, bstack111llll1l1_opy_, result=None, call=None, bstack11llll111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l1l11l1l_opy_ = {
        bstack11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ἑ"): bstack111llll1l1_opy_[bstack11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧἒ")],
        bstack11_opy_ (u"ࠪࡸࡾࡶࡥࠨἓ"): bstack11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩἔ"),
        bstack11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪἕ"): test.name,
        bstack11_opy_ (u"࠭ࡢࡰࡦࡼࠫ἖"): {
            bstack11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ἗"): bstack11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨἘ"),
            bstack11_opy_ (u"ࠩࡦࡳࡩ࡫ࠧἙ"): inspect.getsource(test.obj)
        },
        bstack11_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧἚ"): test.name,
        bstack11_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪἛ"): test.name,
        bstack11_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬἜ"): bstack1ll11l1l1_opy_.bstack11l11111l1_opy_(test),
        bstack11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩἝ"): file_path,
        bstack11_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ἞"): file_path,
        bstack11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ἟"): bstack11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪἠ"),
        bstack11_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨἡ"): file_path,
        bstack11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨἢ"): bstack111llll1l1_opy_[bstack11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩἣ")],
        bstack11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩἤ"): bstack11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧἥ"),
        bstack11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫἦ"): {
            bstack11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ἧ"): test.nodeid
        },
        bstack11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨἨ"): bstack11llllllll1_opy_(test.own_markers)
    }
    if bstack11llll111_opy_ in [bstack11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬἩ"), bstack11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧἪ")]:
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"࠭࡭ࡦࡶࡤࠫἫ")] = {
            bstack11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩἬ"): bstack111llll1l1_opy_.get(bstack11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪἭ"), [])
        }
    if bstack11llll111_opy_ == bstack11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪἮ"):
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪἯ")] = bstack11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬἰ")
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫἱ")] = bstack111llll1l1_opy_[bstack11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬἲ")]
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬἳ")] = bstack111llll1l1_opy_[bstack11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ἴ")]
    if result:
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩἵ")] = result.outcome
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫἶ")] = result.duration * 1000
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩἷ")] = bstack111llll1l1_opy_[bstack11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪἸ")]
        if result.failed:
            bstack11l1l11l1l_opy_[bstack11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬἹ")] = bstack111lllll1_opy_.bstack111l11ll1l_opy_(call.excinfo.typename)
            bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨἺ")] = bstack111lllll1_opy_.bstack111lll1111l_opy_(call.excinfo, result)
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧἻ")] = bstack111llll1l1_opy_[bstack11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨἼ")]
    if outcome:
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪἽ")] = bstack11ll1l11l1l_opy_(outcome)
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬἾ")] = 0
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪἿ")] = bstack111llll1l1_opy_[bstack11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫὀ")]
        if bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧὁ")] == bstack11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨὂ"):
            bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨὃ")] = bstack11_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫὄ")  # bstack111l1l1lll1_opy_
            bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬὅ")] = [{bstack11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ὆"): [bstack11_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ὇")]}]
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭Ὀ")] = bstack111llll1l1_opy_[bstack11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧὉ")]
    return bstack11l1l11l1l_opy_
def bstack111l1l1ll1l_opy_(test, bstack111llll1ll_opy_, bstack11llll111_opy_, result, call, outcome, bstack111l1ll11ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111llll1ll_opy_[bstack11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬὊ")]
    hook_name = bstack111llll1ll_opy_[bstack11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭Ὃ")]
    hook_data = {
        bstack11_opy_ (u"ࠫࡺࡻࡩࡥࠩὌ"): bstack111llll1ll_opy_[bstack11_opy_ (u"ࠬࡻࡵࡪࡦࠪὍ")],
        bstack11_opy_ (u"࠭ࡴࡺࡲࡨࠫ὎"): bstack11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ὏"),
        bstack11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ὐ"): bstack11_opy_ (u"ࠩࡾࢁࠬὑ").format(bstack11l111llll1_opy_(hook_name)),
        bstack11_opy_ (u"ࠪࡦࡴࡪࡹࠨὒ"): {
            bstack11_opy_ (u"ࠫࡱࡧ࡮ࡨࠩὓ"): bstack11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬὔ"),
            bstack11_opy_ (u"࠭ࡣࡰࡦࡨࠫὕ"): None
        },
        bstack11_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ὖ"): test.name,
        bstack11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨὗ"): bstack1ll11l1l1_opy_.bstack11l11111l1_opy_(test, hook_name),
        bstack11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ὘"): file_path,
        bstack11_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬὙ"): file_path,
        bstack11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ὚"): bstack11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭Ὓ"),
        bstack11_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ὜"): file_path,
        bstack11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫὝ"): bstack111llll1ll_opy_[bstack11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ὞")],
        bstack11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬὟ"): bstack11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬὠ") if bstack111l1ll111l_opy_ == bstack11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨὡ") else bstack11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬὢ"),
        bstack11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩὣ"): hook_type
    }
    bstack111llll11l1_opy_ = bstack11l111ll1l_opy_(_11l111l1ll_opy_.get(test.nodeid, None))
    if bstack111llll11l1_opy_:
        hook_data[bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬὤ")] = bstack111llll11l1_opy_
    if result:
        hook_data[bstack11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨὥ")] = result.outcome
        hook_data[bstack11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪὦ")] = result.duration * 1000
        hook_data[bstack11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨὧ")] = bstack111llll1ll_opy_[bstack11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩὨ")]
        if result.failed:
            hook_data[bstack11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫὩ")] = bstack111lllll1_opy_.bstack111l11ll1l_opy_(call.excinfo.typename)
            hook_data[bstack11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧὪ")] = bstack111lllll1_opy_.bstack111lll1111l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧὫ")] = bstack11ll1l11l1l_opy_(outcome)
        hook_data[bstack11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩὬ")] = 100
        hook_data[bstack11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧὭ")] = bstack111llll1ll_opy_[bstack11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨὮ")]
        if hook_data[bstack11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫὯ")] == bstack11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬὰ"):
            hook_data[bstack11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬά")] = bstack11_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨὲ")  # bstack111l1l1lll1_opy_
            hook_data[bstack11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩέ")] = [{bstack11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬὴ"): [bstack11_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧή")]}]
    if bstack111l1ll11ll_opy_:
        hook_data[bstack11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫὶ")] = bstack111l1ll11ll_opy_.result
        hook_data[bstack11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ί")] = bstack11llll111ll_opy_(bstack111llll1ll_opy_[bstack11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪὸ")], bstack111llll1ll_opy_[bstack11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬό")])
        hook_data[bstack11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ὺ")] = bstack111llll1ll_opy_[bstack11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧύ")]
        if hook_data[bstack11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪὼ")] == bstack11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫώ"):
            hook_data[bstack11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ὾")] = bstack111lllll1_opy_.bstack111l11ll1l_opy_(bstack111l1ll11ll_opy_.exception_type)
            hook_data[bstack11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ὿")] = [{bstack11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᾀ"): bstack11lll11l1l1_opy_(bstack111l1ll11ll_opy_.exception)}]
    return hook_data
def bstack111l1lll111_opy_(test, bstack111llll1l1_opy_, bstack11llll111_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11_opy_ (u"ࠨࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬᾁ").format(bstack11llll111_opy_))
    bstack11l1l11l1l_opy_ = bstack111l1l1ll11_opy_(test, bstack111llll1l1_opy_, result, call, bstack11llll111_opy_, outcome)
    driver = getattr(test, bstack11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᾂ"), None)
    if bstack11llll111_opy_ == bstack11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᾃ") and driver:
        bstack11l1l11l1l_opy_[bstack11_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᾄ")] = bstack111lllll1_opy_.bstack11l1l11lll_opy_(driver)
    if bstack11llll111_opy_ == bstack11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᾅ"):
        bstack11llll111_opy_ = bstack11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᾆ")
    bstack111llll111_opy_ = {
        bstack11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᾇ"): bstack11llll111_opy_,
        bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᾈ"): bstack11l1l11l1l_opy_
    }
    bstack111lllll1_opy_.bstack111111111_opy_(bstack111llll111_opy_)
    if bstack11llll111_opy_ == bstack11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᾉ"):
        threading.current_thread().bstackTestMeta = {bstack11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᾊ"): bstack11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᾋ")}
    elif bstack11llll111_opy_ == bstack11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᾌ"):
        threading.current_thread().bstackTestMeta = {bstack11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᾍ"): getattr(result, bstack11_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨᾎ"), bstack11_opy_ (u"ࠨࠩᾏ"))}
def bstack111l1l1l1l1_opy_(test, bstack111llll1l1_opy_, bstack11llll111_opy_, result=None, call=None, outcome=None, bstack111l1ll11ll_opy_=None):
    logger.debug(bstack11_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤ࡭ࡵ࡯࡬ࠢࡧࡥࡹࡧࠬࠡࡧࡹࡩࡳࡺࡔࡺࡲࡨࠤ࠲ࠦࡻࡾࠩᾐ").format(bstack11llll111_opy_))
    hook_data = bstack111l1l1ll1l_opy_(test, bstack111llll1l1_opy_, bstack11llll111_opy_, result, call, outcome, bstack111l1ll11ll_opy_)
    bstack111llll111_opy_ = {
        bstack11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᾑ"): bstack11llll111_opy_,
        bstack11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ᾒ"): hook_data
    }
    bstack111lllll1_opy_.bstack111111111_opy_(bstack111llll111_opy_)
def bstack11l111ll1l_opy_(bstack111llll1l1_opy_):
    if not bstack111llll1l1_opy_:
        return None
    if bstack111llll1l1_opy_.get(bstack11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᾓ"), None):
        return getattr(bstack111llll1l1_opy_[bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᾔ")], bstack11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᾕ"), None)
    return bstack111llll1l1_opy_.get(bstack11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᾖ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.LOG, bstack111111l1ll_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_.LOG, bstack111111l1ll_opy_.POST, request, caplog)
        return # skip all existing bstack111l1llllll_opy_
    try:
        if not bstack111lllll1_opy_.on():
            return
        places = [bstack11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᾗ"), bstack11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᾘ"), bstack11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᾙ")]
        logs = []
        for bstack111l1l11ll1_opy_ in places:
            records = caplog.get_records(bstack111l1l11ll1_opy_)
            bstack111l1l1l111_opy_ = bstack11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᾚ") if bstack111l1l11ll1_opy_ == bstack11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᾛ") else bstack11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᾜ")
            bstack111l1lll1l1_opy_ = request.node.nodeid + (bstack11_opy_ (u"ࠨࠩᾝ") if bstack111l1l11ll1_opy_ == bstack11_opy_ (u"ࠩࡦࡥࡱࡲࠧᾞ") else bstack11_opy_ (u"ࠪ࠱ࠬᾟ") + bstack111l1l11ll1_opy_)
            test_uuid = bstack11l111ll1l_opy_(_11l111l1ll_opy_.get(bstack111l1lll1l1_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11ll1ll1l11_opy_(record.message):
                    continue
                logs.append({
                    bstack11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᾠ"): bstack11ll1l11lll_opy_(record.created).isoformat() + bstack11_opy_ (u"ࠬࡠࠧᾡ"),
                    bstack11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᾢ"): record.levelname,
                    bstack11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᾣ"): record.message,
                    bstack111l1l1l111_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack111lllll1_opy_.bstack1l1l11ll11_opy_(logs)
    except Exception as err:
        print(bstack11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬᾤ"), str(err))
def bstack111lll11_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11l1l11ll_opy_
    bstack1lll1ll11_opy_ = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᾥ"), None) and bstack1llllll111_opy_(
            threading.current_thread(), bstack11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᾦ"), None)
    bstack1ll11111ll_opy_ = getattr(driver, bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᾧ"), None) != None and getattr(driver, bstack11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᾨ"), None) == True
    if sequence == bstack11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᾩ") and driver != None:
      if not bstack11l1l11ll_opy_ and bstack1ll1111l1l1_opy_() and bstack11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᾪ") in CONFIG and CONFIG[bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᾫ")] == True and bstack1l11l11l11_opy_.bstack1ll11111l1_opy_(driver_command) and (bstack1ll11111ll_opy_ or bstack1lll1ll11_opy_) and not bstack1l1111l1_opy_(args):
        try:
          bstack11l1l11ll_opy_ = True
          logger.debug(bstack11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫᾬ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨᾭ").format(str(err)))
        bstack11l1l11ll_opy_ = False
    if sequence == bstack11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᾮ"):
        if driver_command == bstack11_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩᾯ"):
            bstack111lllll1_opy_.bstack1l11ll11l1_opy_({
                bstack11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᾰ"): response[bstack11_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ᾱ")],
                bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᾲ"): store[bstack11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᾳ")]
            })
def bstack11lll1l1l1_opy_():
    global bstack1l1lll1ll_opy_
    bstack11l11l1l_opy_.bstack1l1ll111l1_opy_()
    logging.shutdown()
    bstack111lllll1_opy_.bstack111ll11l1l_opy_()
    for driver in bstack1l1lll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack111l1l1l1ll_opy_(*args):
    global bstack1l1lll1ll_opy_
    bstack111lllll1_opy_.bstack111ll11l1l_opy_()
    for driver in bstack1l1lll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1l1ll1_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1ll1l1ll_opy_(self, *args, **kwargs):
    bstack11l11l11_opy_ = bstack1lll111111_opy_(self, *args, **kwargs)
    bstack1l1llll1l1_opy_ = getattr(threading.current_thread(), bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫᾴ"), None)
    if bstack1l1llll1l1_opy_ and bstack1l1llll1l1_opy_.get(bstack11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ᾵"), bstack11_opy_ (u"ࠬ࠭ᾶ")) == bstack11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᾷ"):
        bstack111lllll1_opy_.bstack11ll1ll1ll_opy_(self)
    return bstack11l11l11_opy_
@measure(event_name=EVENTS.bstack1ll1ll1l1_opy_, stage=STAGE.bstack1l11l1lll1_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1l1ll1ll1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1l1lll1_opy_ = Config.bstack11l111l11_opy_()
    if bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫᾸ")):
        return
    bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬᾹ"), True)
    global bstack1l1ll111ll_opy_
    global bstack1l11111l1l_opy_
    bstack1l1ll111ll_opy_ = framework_name
    logger.info(bstack1lll1l1lll_opy_.format(bstack1l1ll111ll_opy_.split(bstack11_opy_ (u"ࠩ࠰ࠫᾺ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll1111l1l1_opy_():
            Service.start = bstack11ll1lll_opy_
            Service.stop = bstack1l111ll11l_opy_
            webdriver.Remote.get = bstack1l1l1ll11l_opy_
            webdriver.Remote.__init__ = bstack1ll1l111l1_opy_
            if not isinstance(os.getenv(bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫΆ")), str):
                return
            WebDriver.close = bstack11lllllll1_opy_
            WebDriver.quit = bstack1l11l1111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack111lllll1_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1l1ll_opy_
        bstack1l11111l1l_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩᾼ")):
        bstack1l11111l1l_opy_ = eval(os.environ.get(bstack11_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ᾽")))
    if not bstack1l11111l1l_opy_:
        bstack11ll1l1lll_opy_(bstack11_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣι"), bstack11l1llll1_opy_)
    if bstack1l11ll111_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._11llll1lll_opy_ = bstack11ll11l1l1_opy_
        except Exception as e:
            logger.error(bstack11l1ll1l1_opy_.format(str(e)))
    if bstack11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᾿") in str(framework_name).lower():
        if not bstack1ll1111l1l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l1l1l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11l1lll111_opy_
            Config.getoption = bstack1ll11lllll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11ll11ll1l_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1lll1l1_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1l11l1111_opy_(self):
    global bstack1l1ll111ll_opy_
    global bstack11l111l1_opy_
    global bstack11ll1ll11l_opy_
    try:
        if bstack11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ῀") in bstack1l1ll111ll_opy_ and self.session_id != None and bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭῁"), bstack11_opy_ (u"ࠪࠫῂ")) != bstack11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬῃ"):
            bstack11111l11_opy_ = bstack11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬῄ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭῅")
            bstack11111ll1l_opy_(logger, True)
            if self != None:
                bstack1l111l111_opy_(self, bstack11111l11_opy_, bstack11_opy_ (u"ࠧ࠭ࠢࠪῆ").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llllll1lll_opy_(bstack1lllll111l1_opy_):
            item = store.get(bstack11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬῇ"), None)
            if item is not None and bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨῈ"), None):
                bstack11l11l1ll_opy_.bstack1lll111l_opy_(self, bstack1l1lll111l_opy_, logger, item)
        threading.current_thread().testStatus = bstack11_opy_ (u"ࠪࠫΈ")
    except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧῊ") + str(e))
    bstack11ll1ll11l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11l1111ll_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1ll1l111l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11l111l1_opy_
    global bstack1ll111lll1_opy_
    global bstack11llll11_opy_
    global bstack1l1ll111ll_opy_
    global bstack1lll111111_opy_
    global bstack1l1lll1ll_opy_
    global bstack1ll111ll1_opy_
    global bstack1l11l111_opy_
    global bstack1l1lll111l_opy_
    CONFIG[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧΉ")] = str(bstack1l1ll111ll_opy_) + str(__version__)
    command_executor = bstack111l11ll1_opy_(bstack1ll111ll1_opy_, CONFIG)
    logger.debug(bstack111l1llll_opy_.format(command_executor))
    proxy = bstack1llll11l1l_opy_(CONFIG, proxy)
    bstack1l1l1111ll_opy_ = 0
    try:
        if bstack11llll11_opy_ is True:
            bstack1l1l1111ll_opy_ = int(os.environ.get(bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ῌ")))
    except:
        bstack1l1l1111ll_opy_ = 0
    bstack1llll1l11l_opy_ = bstack1l1l1lll1l_opy_(CONFIG, bstack1l1l1111ll_opy_)
    logger.debug(bstack1l111l11l1_opy_.format(str(bstack1llll1l11l_opy_)))
    bstack1l1lll111l_opy_ = CONFIG.get(bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ῍"))[bstack1l1l1111ll_opy_]
    if bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ῎") in CONFIG and CONFIG[bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭῏")]:
        bstack1l1l1ll1l_opy_(bstack1llll1l11l_opy_, bstack1l11l111_opy_)
    if bstack1111l1111_opy_.bstack11ll1l1l11_opy_(CONFIG, bstack1l1l1111ll_opy_) and bstack1111l1111_opy_.bstack1111l11ll_opy_(bstack1llll1l11l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llllll1lll_opy_(bstack1lllll111l1_opy_):
            bstack1111l1111_opy_.set_capabilities(bstack1llll1l11l_opy_, CONFIG)
    if desired_capabilities:
        bstack1lll1ll1ll_opy_ = bstack1ll1llll11_opy_(desired_capabilities)
        bstack1lll1ll1ll_opy_[bstack11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪῐ")] = bstack11111111_opy_(CONFIG)
        bstack1l1l1l111_opy_ = bstack1l1l1lll1l_opy_(bstack1lll1ll1ll_opy_)
        if bstack1l1l1l111_opy_:
            bstack1llll1l11l_opy_ = update(bstack1l1l1l111_opy_, bstack1llll1l11l_opy_)
        desired_capabilities = None
    if options:
        bstack1ll11lll1_opy_(options, bstack1llll1l11l_opy_)
    if not options:
        options = bstack1llll111l_opy_(bstack1llll1l11l_opy_)
    if proxy and bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫῑ")):
        options.proxy(proxy)
    if options and bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫῒ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111l111l1_opy_() < version.parse(bstack11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬΐ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1llll1l11l_opy_)
    logger.info(bstack1lll11lll1_opy_)
    bstack1l1ll1111_opy_.end(EVENTS.bstack1ll1ll1l1_opy_.value, EVENTS.bstack1ll1ll1l1_opy_.value + bstack11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ῔"),
                               EVENTS.bstack1ll1ll1l1_opy_.value + bstack11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ῕"), True, None)
    if bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩῖ")):
        bstack1lll111111_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩῗ")):
        bstack1lll111111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫῘ")):
        bstack1lll111111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lll111111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack111lll11l_opy_ = bstack11_opy_ (u"ࠬ࠭Ῑ")
        if bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧῚ")):
            bstack111lll11l_opy_ = self.caps.get(bstack11_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢΊ"))
        else:
            bstack111lll11l_opy_ = self.capabilities.get(bstack11_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ῜"))
        if bstack111lll11l_opy_:
            bstack1llll1lll_opy_(bstack111lll11l_opy_)
            if bstack111l111l1_opy_() <= version.parse(bstack11_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ῝")):
                self.command_executor._url = bstack11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ῞") + bstack1ll111ll1_opy_ + bstack11_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ῟")
            else:
                self.command_executor._url = bstack11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢῠ") + bstack111lll11l_opy_ + bstack11_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢῡ")
            logger.debug(bstack111ll11l1_opy_.format(bstack111lll11l_opy_))
        else:
            logger.debug(bstack1l11l11l1_opy_.format(bstack11_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣῢ")))
    except Exception as e:
        logger.debug(bstack1l11l11l1_opy_.format(e))
    bstack11l111l1_opy_ = self.session_id
    if bstack11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨΰ") in bstack1l1ll111ll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ῤ"), None)
        if item:
            bstack111l1ll1l1l_opy_ = getattr(item, bstack11_opy_ (u"ࠪࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨῥ"), False)
            if not getattr(item, bstack11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬῦ"), None) and bstack111l1ll1l1l_opy_:
                setattr(store[bstack11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩῧ")], bstack11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧῨ"), self)
        bstack1l1llll1l1_opy_ = getattr(threading.current_thread(), bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨῩ"), None)
        if bstack1l1llll1l1_opy_ and bstack1l1llll1l1_opy_.get(bstack11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨῪ"), bstack11_opy_ (u"ࠩࠪΎ")) == bstack11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫῬ"):
            bstack111lllll1_opy_.bstack11ll1ll1ll_opy_(self)
    bstack1l1lll1ll_opy_.append(self)
    if bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ῭") in CONFIG and bstack11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ΅") in CONFIG[bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ`")][bstack1l1l1111ll_opy_]:
        bstack1ll111lll1_opy_ = CONFIG[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ῰")][bstack1l1l1111ll_opy_][bstack11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭῱")]
    logger.debug(bstack1111llll1_opy_.format(bstack11l111l1_opy_))
@measure(event_name=EVENTS.bstack1l1l111l11_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1l1l1ll11l_opy_(self, url):
    global bstack1111ll1ll_opy_
    global CONFIG
    try:
        bstack11l1lll1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11lll11l_opy_.format(str(err)))
    try:
        bstack1111ll1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack11111ll1_opy_ = str(e)
            if any(err_msg in bstack11111ll1_opy_ for err_msg in bstack1l11111l11_opy_):
                bstack11l1lll1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11lll11l_opy_.format(str(err)))
        raise e
def bstack1l1l1l1ll_opy_(item, when):
    global bstack11l1ll11l1_opy_
    try:
        bstack11l1ll11l1_opy_(item, when)
    except Exception as e:
        pass
def bstack11ll11ll1l_opy_(item, call, rep):
    global bstack1l1lll1l1l_opy_
    global bstack1l1lll1ll_opy_
    name = bstack11_opy_ (u"ࠩࠪῲ")
    try:
        if rep.when == bstack11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨῳ"):
            bstack11l111l1_opy_ = threading.current_thread().bstackSessionId
            bstack111l1l1l11l_opy_ = item.config.getoption(bstack11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ῴ"))
            try:
                if (str(bstack111l1l1l11l_opy_).lower() != bstack11_opy_ (u"ࠬࡺࡲࡶࡧࠪ῵")):
                    name = str(rep.nodeid)
                    bstack1lll11l1_opy_ = bstack1l1ll1llll_opy_(bstack11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧῶ"), name, bstack11_opy_ (u"ࠧࠨῷ"), bstack11_opy_ (u"ࠨࠩῸ"), bstack11_opy_ (u"ࠩࠪΌ"), bstack11_opy_ (u"ࠪࠫῺ"))
                    os.environ[bstack11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧΏ")] = name
                    for driver in bstack1l1lll1ll_opy_:
                        if bstack11l111l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll11l1_opy_)
            except Exception as e:
                logger.debug(bstack11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬῼ").format(str(e)))
            try:
                bstack11lll1llll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ´"):
                    status = bstack11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ῾") if rep.outcome.lower() == bstack11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ῿") else bstack11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ ")
                    reason = bstack11_opy_ (u"ࠪࠫ ")
                    if status == bstack11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ "):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ ") if status == bstack11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ ") else bstack11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ ")
                    data = name + bstack11_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ ") if status == bstack11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ ") else name + bstack11_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ ") + reason
                    bstack1lll11ll11_opy_ = bstack1l1ll1llll_opy_(bstack11_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ "), bstack11_opy_ (u"ࠬ࠭ "), bstack11_opy_ (u"࠭ࠧ​"), bstack11_opy_ (u"ࠧࠨ‌"), level, data)
                    for driver in bstack1l1lll1ll_opy_:
                        if bstack11l111l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll11ll11_opy_)
            except Exception as e:
                logger.debug(bstack11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ‍").format(str(e)))
    except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭‎").format(str(e)))
    bstack1l1lll1l1l_opy_(item, call, rep)
notset = Notset()
def bstack1ll11lllll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1lll1ll1_opy_
    if str(name).lower() == bstack11_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪ‏"):
        return bstack11_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ‐")
    else:
        return bstack1l1lll1ll1_opy_(self, name, default, skip)
def bstack11ll11l1l1_opy_(self):
    global CONFIG
    global bstack1ll1l1l1l1_opy_
    try:
        proxy = bstack111111l11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ‑")):
                proxies = bstack11l11llll_opy_(proxy, bstack111l11ll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1ll11l1l_opy_ = proxies.popitem()
                    if bstack11_opy_ (u"ࠨ࠺࠰࠱ࠥ‒") in bstack1l1ll11l1l_opy_:
                        return bstack1l1ll11l1l_opy_
                    else:
                        return bstack11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ–") + bstack1l1ll11l1l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧ—").format(str(e)))
    return bstack1ll1l1l1l1_opy_(self)
def bstack1l11ll111_opy_():
    return (bstack11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ―") in CONFIG or bstack11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ‖") in CONFIG) and bstack1ll11l11l1_opy_() and bstack111l111l1_opy_() >= version.parse(
        bstack111l111l_opy_)
def bstack11lll1lll1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll111lll1_opy_
    global bstack11llll11_opy_
    global bstack1l1ll111ll_opy_
    CONFIG[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭‗")] = str(bstack1l1ll111ll_opy_) + str(__version__)
    bstack1l1l1111ll_opy_ = 0
    try:
        if bstack11llll11_opy_ is True:
            bstack1l1l1111ll_opy_ = int(os.environ.get(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ‘")))
    except:
        bstack1l1l1111ll_opy_ = 0
    CONFIG[bstack11_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ’")] = True
    bstack1llll1l11l_opy_ = bstack1l1l1lll1l_opy_(CONFIG, bstack1l1l1111ll_opy_)
    logger.debug(bstack1l111l11l1_opy_.format(str(bstack1llll1l11l_opy_)))
    if CONFIG.get(bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ‚")):
        bstack1l1l1ll1l_opy_(bstack1llll1l11l_opy_, bstack1l11l111_opy_)
    if bstack11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ‛") in CONFIG and bstack11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ“") in CONFIG[bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭”")][bstack1l1l1111ll_opy_]:
        bstack1ll111lll1_opy_ = CONFIG[bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ„")][bstack1l1l1111ll_opy_][bstack11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ‟")]
    import urllib
    import json
    if bstack11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ†") in CONFIG and str(CONFIG[bstack11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ‡")]).lower() != bstack11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ•"):
        bstack11ll1111l1_opy_ = bstack11l1111l_opy_()
        bstack1l1llllll_opy_ = bstack11ll1111l1_opy_ + urllib.parse.quote(json.dumps(bstack1llll1l11l_opy_))
    else:
        bstack1l1llllll_opy_ = bstack11_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ‣") + urllib.parse.quote(json.dumps(bstack1llll1l11l_opy_))
    browser = self.connect(bstack1l1llllll_opy_)
    return browser
def bstack1l1lllll1_opy_():
    global bstack1l11111l1l_opy_
    global bstack1l1ll111ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11111ll1_opy_
        if not bstack1ll1111l1l1_opy_():
            global bstack1l11ll11ll_opy_
            if not bstack1l11ll11ll_opy_:
                from bstack_utils.helper import bstack11lll11l11_opy_, bstack1llll1lll1_opy_
                bstack1l11ll11ll_opy_ = bstack11lll11l11_opy_()
                bstack1llll1lll1_opy_(bstack1l1ll111ll_opy_)
            BrowserType.connect = bstack1l11111ll1_opy_
            return
        BrowserType.launch = bstack11lll1lll1_opy_
        bstack1l11111l1l_opy_ = True
    except Exception as e:
        pass
def bstack111ll1111ll_opy_():
    global CONFIG
    global bstack1111ll1l_opy_
    global bstack1ll111ll1_opy_
    global bstack1l11l111_opy_
    global bstack11llll11_opy_
    global bstack11l11ll11_opy_
    CONFIG = json.loads(os.environ.get(bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ․")))
    bstack1111ll1l_opy_ = eval(os.environ.get(bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ‥")))
    bstack1ll111ll1_opy_ = os.environ.get(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ…"))
    bstack11lll1ll1l_opy_(CONFIG, bstack1111ll1l_opy_)
    bstack11l11ll11_opy_ = bstack11l11l1l_opy_.bstack1lll11ll1l_opy_(CONFIG, bstack11l11ll11_opy_)
    if cli.bstack1ll111ll1l_opy_():
        bstack11ll1l1ll1_opy_.invoke(bstack11lllll111_opy_.CONNECT, bstack1l1lll1l1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭‧"), bstack11_opy_ (u"ࠧ࠱ࠩ ")))
        cli.bstack1lllll1ll11_opy_(cli_context.platform_index)
        cli.bstack1llll11l1l1_opy_(bstack111l11ll1_opy_(bstack1ll111ll1_opy_, CONFIG), cli_context.platform_index, bstack1llll111l_opy_)
        cli.bstack1llllll11l1_opy_()
        logger.debug(bstack11_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ ") + str(cli_context.platform_index) + bstack11_opy_ (u"ࠤࠥ‪"))
        return # skip all existing bstack111l1llllll_opy_
    global bstack1lll111111_opy_
    global bstack11ll1ll11l_opy_
    global bstack1llll1l1l_opy_
    global bstack1l1l1l1l_opy_
    global bstack1lll1lll11_opy_
    global bstack1ll11l1l_opy_
    global bstack1ll1l11l1l_opy_
    global bstack1111ll1ll_opy_
    global bstack1ll1l1l1l1_opy_
    global bstack1l1lll1ll1_opy_
    global bstack11l1ll11l1_opy_
    global bstack1l1lll1l1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll111111_opy_ = webdriver.Remote.__init__
        bstack11ll1ll11l_opy_ = WebDriver.quit
        bstack1ll1l11l1l_opy_ = WebDriver.close
        bstack1111ll1ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭‫") in CONFIG or bstack11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ‬") in CONFIG) and bstack1ll11l11l1_opy_():
        if bstack111l111l1_opy_() < version.parse(bstack111l111l_opy_):
            logger.error(bstack11l1l11l1_opy_.format(bstack111l111l1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1ll1l1l1l1_opy_ = RemoteConnection._11llll1lll_opy_
            except Exception as e:
                logger.error(bstack11l1ll1l1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1lll1ll1_opy_ = Config.getoption
        from _pytest import runner
        bstack11l1ll11l1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1llll111ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1lll1l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭‭"))
    bstack1l11l111_opy_ = CONFIG.get(bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ‮"), {}).get(bstack11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ "))
    bstack11llll11_opy_ = True
    bstack1l1ll1ll1_opy_(bstack1ll1llll_opy_)
if (bstack11lll1ll111_opy_()):
    bstack111ll1111ll_opy_()
@bstack111lll1lll_opy_(class_method=False)
def bstack111ll1111l1_opy_(hook_name, event, bstack1l1l111l11l_opy_=None):
    if hook_name not in [bstack11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ‰"), bstack11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭‱"), bstack11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ′"), bstack11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭″"), bstack11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ‴"), bstack11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ‵"), bstack11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭‶"), bstack11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ‷")]:
        return
    node = store[bstack11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭‸")]
    if hook_name in [bstack11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ‹"), bstack11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭›")]:
        node = store[bstack11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ※")]
    elif hook_name in [bstack11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ‼"), bstack11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ‽")]:
        node = store[bstack11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭‾")]
    hook_type = bstack11l111l1ll1_opy_(hook_name)
    if event == bstack11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ‿"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_[hook_type], bstack111111l1ll_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111llll1ll_opy_ = {
            bstack11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⁀"): uuid,
            bstack11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⁁"): bstack1lllll11ll_opy_(),
            bstack11_opy_ (u"ࠬࡺࡹࡱࡧࠪ⁂"): bstack11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⁃"),
            bstack11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⁄"): hook_type,
            bstack11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ⁅"): hook_name
        }
        store[bstack11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⁆")].append(uuid)
        bstack111l1llll11_opy_ = node.nodeid
        if hook_type == bstack11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⁇"):
            if not _11l111l1ll_opy_.get(bstack111l1llll11_opy_, None):
                _11l111l1ll_opy_[bstack111l1llll11_opy_] = {bstack11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⁈"): []}
            _11l111l1ll_opy_[bstack111l1llll11_opy_][bstack11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⁉")].append(bstack111llll1ll_opy_[bstack11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⁊")])
        _11l111l1ll_opy_[bstack111l1llll11_opy_ + bstack11_opy_ (u"ࠧ࠮ࠩ⁋") + hook_name] = bstack111llll1ll_opy_
        bstack111l1l1l1l1_opy_(node, bstack111llll1ll_opy_, bstack11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⁌"))
    elif event == bstack11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⁍"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11ll1_opy_[hook_type], bstack111111l1ll_opy_.POST, node, None, bstack1l1l111l11l_opy_)
            return
        bstack11l11l11l1_opy_ = node.nodeid + bstack11_opy_ (u"ࠪ࠱ࠬ⁎") + hook_name
        _11l111l1ll_opy_[bstack11l11l11l1_opy_][bstack11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁏")] = bstack1lllll11ll_opy_()
        bstack111l1ll1ll1_opy_(_11l111l1ll_opy_[bstack11l11l11l1_opy_][bstack11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁐")])
        bstack111l1l1l1l1_opy_(node, _11l111l1ll_opy_[bstack11l11l11l1_opy_], bstack11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⁑"), bstack111l1ll11ll_opy_=bstack1l1l111l11l_opy_)
def bstack111l1ll1l11_opy_():
    global bstack111l1ll111l_opy_
    if bstack11l1ll11ll_opy_():
        bstack111l1ll111l_opy_ = bstack11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ⁒")
    else:
        bstack111l1ll111l_opy_ = bstack11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⁓")
@bstack111lllll1_opy_.bstack111lll11lll_opy_
def bstack111l1ll11l1_opy_():
    bstack111l1ll1l11_opy_()
    if cli.is_running():
        try:
            bstack11ll11ll11l_opy_(bstack111ll1111l1_opy_)
        except Exception as e:
            logger.debug(bstack11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⁔").format(e))
        return
    if bstack1ll11l11l1_opy_():
        bstack1l1l1lll1_opy_ = Config.bstack11l111l11_opy_()
        bstack11_opy_ (u"ࠪࠫࠬࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡃࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡩࡨࡸࡸࠦࡵࡴࡧࡧࠤ࡫ࡵࡲࠡࡣ࠴࠵ࡾࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠮ࡹࡵࡥࡵࡶࡩ࡯ࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡳࡷࡱࠤࡧ࡫ࡣࡢࡷࡶࡩࠥ࡯ࡴࠡ࡫ࡶࠤࡵࡧࡴࡤࡪࡨࡨࠥ࡯࡮ࠡࡣࠣࡨ࡮࡬ࡦࡦࡴࡨࡲࡹࠦࡰࡳࡱࡦࡩࡸࡹࠠࡪࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡹࡸࠦࡷࡦࠢࡱࡩࡪࡪࠠࡵࡱࠣࡹࡸ࡫ࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࡒࡤࡸࡨ࡮ࠨࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡫ࡥࡳࡪ࡬ࡦࡴࠬࠤ࡫ࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠫࠬ࠭⁕")
        if bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⁖")):
            if CONFIG.get(bstack11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⁗")) is not None and int(CONFIG[bstack11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⁘")]) > 1:
                bstack1lll1111ll_opy_(bstack111lll11_opy_)
            return
        bstack1lll1111ll_opy_(bstack111lll11_opy_)
    try:
        bstack11ll11ll11l_opy_(bstack111ll1111l1_opy_)
    except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ⁙").format(e))
bstack111l1ll11l1_opy_()