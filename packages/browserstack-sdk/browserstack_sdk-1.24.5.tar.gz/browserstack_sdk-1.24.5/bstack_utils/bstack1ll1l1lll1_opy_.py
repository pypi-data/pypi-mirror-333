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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1lll111ll_opy_ import get_logger
logger = get_logger(__name__)
bstack11l11l1llll_opy_: Dict[str, float] = {}
bstack11l11l1lll1_opy_: List = []
bstack11l11l1l1l1_opy_ = 5
bstack1lll1l1l11_opy_ = os.path.join(os.getcwd(), bstack1l11l_opy_ (u"ࠩ࡯ࡳ࡬࠭ᯑ"), bstack1l11l_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ᯒ"))
logging.getLogger(bstack1l11l_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰ࠭ᯓ")).setLevel(logging.WARNING)
lock = FileLock(bstack1lll1l1l11_opy_+bstack1l11l_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦᯔ"))
class bstack11l11l1ll1l_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack11l11ll11l1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack11l11ll11l1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l11l_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫ࠢᯕ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1ll1l11_opy_:
    global bstack11l11l1llll_opy_
    @staticmethod
    def bstack1lll111l1ll_opy_(key: str):
        bstack1ll1ll11111_opy_ = bstack1lll1ll1l11_opy_.bstack1l111lll1l1_opy_(key)
        bstack1lll1ll1l11_opy_.mark(bstack1ll1ll11111_opy_+bstack1l11l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᯖ"))
        return bstack1ll1ll11111_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack11l11l1llll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l11l_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᯗ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1ll1l11_opy_.mark(end)
            bstack1lll1ll1l11_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨᯘ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack11l11l1llll_opy_ or end not in bstack11l11l1llll_opy_:
                logger.debug(bstack1l11l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠡࡱࡵࠤࡪࡴࡤࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠧᯙ").format(start,end))
                return
            duration: float = bstack11l11l1llll_opy_[end] - bstack11l11l1llll_opy_[start]
            bstack11l11ll1111_opy_ = os.environ.get(bstack1l11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢᯚ"), bstack1l11l_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦᯛ")).lower() == bstack1l11l_opy_ (u"ࠨࡴࡳࡷࡨࠦᯜ")
            bstack11l11ll111l_opy_: bstack11l11l1ll1l_opy_ = bstack11l11l1ll1l_opy_(duration, label, bstack11l11l1llll_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l11l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᯝ"), 0), command, test_name, hook_type, bstack11l11ll1111_opy_)
            del bstack11l11l1llll_opy_[start]
            del bstack11l11l1llll_opy_[end]
            bstack1lll1ll1l11_opy_.bstack11l11ll11ll_opy_(bstack11l11ll111l_opy_)
        except Exception as e:
            logger.debug(bstack1l11l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡦࡣࡶࡹࡷ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦᯞ").format(e))
    @staticmethod
    def bstack11l11ll11ll_opy_(bstack11l11ll111l_opy_):
        os.makedirs(os.path.dirname(bstack1lll1l1l11_opy_)) if not os.path.exists(os.path.dirname(bstack1lll1l1l11_opy_)) else None
        bstack1lll1ll1l11_opy_.bstack11l11l1l1ll_opy_()
        try:
            with lock:
                with open(bstack1lll1l1l11_opy_, bstack1l11l_opy_ (u"ࠤࡵ࠯ࠧᯟ"), encoding=bstack1l11l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᯠ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11l11ll111l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack11l11l1ll11_opy_:
            logger.debug(bstack1l11l_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠥࢁࡽࠣᯡ").format(bstack11l11l1ll11_opy_))
            with lock:
                with open(bstack1lll1l1l11_opy_, bstack1l11l_opy_ (u"ࠧࡽࠢᯢ"), encoding=bstack1l11l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᯣ")) as file:
                    data = [bstack11l11ll111l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡢࡲࡳࡩࡳࡪࠠࡼࡿࠥᯤ").format(str(e)))
        finally:
            if os.path.exists(bstack1lll1l1l11_opy_+bstack1l11l_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢᯥ")):
                os.remove(bstack1lll1l1l11_opy_+bstack1l11l_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫᯦ࠣ"))
    @staticmethod
    def bstack11l11l1l1ll_opy_():
        attempt = 0
        while (attempt < bstack11l11l1l1l1_opy_):
            attempt += 1
            if os.path.exists(bstack1lll1l1l11_opy_+bstack1l11l_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤᯧ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack1l111lll1l1_opy_(label: str) -> str:
        try:
            return bstack1l11l_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥᯨ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l11l_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᯩ").format(e))