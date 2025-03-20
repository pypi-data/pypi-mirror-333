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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack11l11l1l_opy_ import get_logger
logger = get_logger(__name__)
bstack11l11l1l1l1_opy_: Dict[str, float] = {}
bstack11l11ll11l1_opy_: List = []
bstack11l11ll11ll_opy_ = 5
bstack11lll1l1_opy_ = os.path.join(os.getcwd(), bstack11_opy_ (u"ࠪࡰࡴ࡭ࠧᯒ"), bstack11_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧᯓ"))
logging.getLogger(bstack11_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠧᯔ")).setLevel(logging.WARNING)
lock = FileLock(bstack11lll1l1_opy_+bstack11_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧᯕ"))
class bstack11l11ll111l_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack11l11l1ll11_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack11l11l1ll11_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11_opy_ (u"ࠢ࡮ࡧࡤࡷࡺࡸࡥࠣᯖ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack11111111l1_opy_:
    global bstack11l11l1l1l1_opy_
    @staticmethod
    def bstack1ll1ll11111_opy_(key: str):
        bstack1ll1l1llll1_opy_ = bstack11111111l1_opy_.bstack1l11l111111_opy_(key)
        bstack11111111l1_opy_.mark(bstack1ll1l1llll1_opy_+bstack11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᯗ"))
        return bstack1ll1l1llll1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack11l11l1l1l1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᯘ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack11111111l1_opy_.mark(end)
            bstack11111111l1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢᯙ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack11l11l1l1l1_opy_ or end not in bstack11l11l1l1l1_opy_:
                logger.debug(bstack11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠢࡲࡶࠥ࡫࡮ࡥࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠨᯚ").format(start,end))
                return
            duration: float = bstack11l11l1l1l1_opy_[end] - bstack11l11l1l1l1_opy_[start]
            bstack11l11l1llll_opy_ = os.environ.get(bstack11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡎ࡙࡟ࡓࡗࡑࡒࡎࡔࡇࠣᯛ"), bstack11_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧᯜ")).lower() == bstack11_opy_ (u"ࠢࡵࡴࡸࡩࠧᯝ")
            bstack11l11l1l1ll_opy_: bstack11l11ll111l_opy_ = bstack11l11ll111l_opy_(duration, label, bstack11l11l1l1l1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᯞ"), 0), command, test_name, hook_type, bstack11l11l1llll_opy_)
            del bstack11l11l1l1l1_opy_[start]
            del bstack11l11l1l1l1_opy_[end]
            bstack11111111l1_opy_.bstack11l11l1lll1_opy_(bstack11l11l1l1ll_opy_)
        except Exception as e:
            logger.debug(bstack11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡧࡤࡷࡺࡸࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧᯟ").format(e))
    @staticmethod
    def bstack11l11l1lll1_opy_(bstack11l11l1l1ll_opy_):
        os.makedirs(os.path.dirname(bstack11lll1l1_opy_)) if not os.path.exists(os.path.dirname(bstack11lll1l1_opy_)) else None
        bstack11111111l1_opy_.bstack11l11l1ll1l_opy_()
        try:
            with lock:
                with open(bstack11lll1l1_opy_, bstack11_opy_ (u"ࠥࡶ࠰ࠨᯠ"), encoding=bstack11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᯡ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11l11l1l1ll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack11l11ll1111_opy_:
            logger.debug(bstack11_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠦࡻࡾࠤᯢ").format(bstack11l11ll1111_opy_))
            with lock:
                with open(bstack11lll1l1_opy_, bstack11_opy_ (u"ࠨࡷࠣᯣ"), encoding=bstack11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᯤ")) as file:
                    data = [bstack11l11l1l1ll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡣࡳࡴࡪࡴࡤࠡࡽࢀࠦᯥ").format(str(e)))
        finally:
            if os.path.exists(bstack11lll1l1_opy_+bstack11_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫᯦ࠣ")):
                os.remove(bstack11lll1l1_opy_+bstack11_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤᯧ"))
    @staticmethod
    def bstack11l11l1ll1l_opy_():
        attempt = 0
        while (attempt < bstack11l11ll11ll_opy_):
            attempt += 1
            if os.path.exists(bstack11lll1l1_opy_+bstack11_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥᯨ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack1l11l111111_opy_(label: str) -> str:
        try:
            return bstack11_opy_ (u"ࠧࢁࡽ࠻ࡽࢀࠦᯩ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᯪ").format(e))