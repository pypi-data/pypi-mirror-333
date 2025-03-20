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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l1111ll111_opy_, bstack11ll11llll_opy_, bstack1ll11lll1_opy_, bstack1l1ll1l1_opy_,
                                    bstack1l1111lllll_opy_, bstack1l111l1l111_opy_, bstack1l11111ll1l_opy_, bstack1l1111l11l1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1l1llll_opy_, bstack111ll1ll1_opy_
from bstack_utils.proxy import bstack1l11ll11l_opy_, bstack11lll11lll_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1lll111ll_opy_
from browserstack_sdk._version import __version__
bstack1ll11111ll_opy_ = Config.bstack111lll11_opy_()
logger = bstack1lll111ll_opy_.get_logger(__name__, bstack1lll111ll_opy_.bstack1llll1l1ll1_opy_())
def bstack1l11l111l11_opy_(config):
    return config[bstack1l11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᢖ")]
def bstack1l111lll1ll_opy_(config):
    return config[bstack1l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᢗ")]
def bstack1111l111l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11lll11111l_opy_(obj):
    values = []
    bstack11lll1l111l_opy_ = re.compile(bstack1l11l_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢᢘ"), re.I)
    for key in obj.keys():
        if bstack11lll1l111l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11ll1l1l11l_opy_(config):
    tags = []
    tags.extend(bstack11lll11111l_opy_(os.environ))
    tags.extend(bstack11lll11111l_opy_(config))
    return tags
def bstack11lllll1111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11lll1l1ll1_opy_(bstack11lllll11ll_opy_):
    if not bstack11lllll11ll_opy_:
        return bstack1l11l_opy_ (u"ࠫࠬᢙ")
    return bstack1l11l_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨᢚ").format(bstack11lllll11ll_opy_.name, bstack11lllll11ll_opy_.email)
def bstack1l11l111lll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11lll11ll1l_opy_ = repo.common_dir
        info = {
            bstack1l11l_opy_ (u"ࠨࡳࡩࡣࠥᢛ"): repo.head.commit.hexsha,
            bstack1l11l_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥᢜ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l11l_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣᢝ"): repo.active_branch.name,
            bstack1l11l_opy_ (u"ࠤࡷࡥ࡬ࠨᢞ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨᢟ"): bstack11lll1l1ll1_opy_(repo.head.commit.committer),
            bstack1l11l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧᢠ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l11l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧᢡ"): bstack11lll1l1ll1_opy_(repo.head.commit.author),
            bstack1l11l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦᢢ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l11l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᢣ"): repo.head.commit.message,
            bstack1l11l_opy_ (u"ࠣࡴࡲࡳࡹࠨᢤ"): repo.git.rev_parse(bstack1l11l_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦᢥ")),
            bstack1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᢦ"): bstack11lll11ll1l_opy_,
            bstack1l11l_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᢧ"): subprocess.check_output([bstack1l11l_opy_ (u"ࠧ࡭ࡩࡵࠤᢨ"), bstack1l11l_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤᢩ"), bstack1l11l_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥᢪ")]).strip().decode(
                bstack1l11l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᢫")),
            bstack1l11l_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦ᢬"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ᢭"): repo.git.rev_list(
                bstack1l11l_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦ᢮").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11lll1l1lll_opy_ = []
        for remote in remotes:
            bstack11lll1l1111_opy_ = {
                bstack1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᢯"): remote.name,
                bstack1l11l_opy_ (u"ࠨࡵࡳ࡮ࠥᢰ"): remote.url,
            }
            bstack11lll1l1lll_opy_.append(bstack11lll1l1111_opy_)
        bstack11ll1l1lll1_opy_ = {
            bstack1l11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᢱ"): bstack1l11l_opy_ (u"ࠣࡩ࡬ࡸࠧᢲ"),
            **info,
            bstack1l11l_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥᢳ"): bstack11lll1l1lll_opy_
        }
        bstack11ll1l1lll1_opy_ = bstack11ll1l111l1_opy_(bstack11ll1l1lll1_opy_)
        return bstack11ll1l1lll1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᢴ").format(err))
        return {}
def bstack11ll1l111l1_opy_(bstack11ll1l1lll1_opy_):
    bstack11lllll1l11_opy_ = bstack11llllllll1_opy_(bstack11ll1l1lll1_opy_)
    if bstack11lllll1l11_opy_ and bstack11lllll1l11_opy_ > bstack1l1111lllll_opy_:
        bstack11lll11l1ll_opy_ = bstack11lllll1l11_opy_ - bstack1l1111lllll_opy_
        bstack11lll111ll1_opy_ = bstack11lllll11l1_opy_(bstack11ll1l1lll1_opy_[bstack1l11l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᢵ")], bstack11lll11l1ll_opy_)
        bstack11ll1l1lll1_opy_[bstack1l11l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᢶ")] = bstack11lll111ll1_opy_
        logger.info(bstack1l11l_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣᢷ")
                    .format(bstack11llllllll1_opy_(bstack11ll1l1lll1_opy_) / 1024))
    return bstack11ll1l1lll1_opy_
def bstack11llllllll1_opy_(bstack11ll1111ll_opy_):
    try:
        if bstack11ll1111ll_opy_:
            bstack11lll1l11l1_opy_ = json.dumps(bstack11ll1111ll_opy_)
            bstack11llll1l111_opy_ = sys.getsizeof(bstack11lll1l11l1_opy_)
            return bstack11llll1l111_opy_
    except Exception as e:
        logger.debug(bstack1l11l_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢᢸ").format(e))
    return -1
def bstack11lllll11l1_opy_(field, bstack1l1111111l1_opy_):
    try:
        bstack11llll1l1ll_opy_ = len(bytes(bstack1l111l1l111_opy_, bstack1l11l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᢹ")))
        bstack11lll111lll_opy_ = bytes(field, bstack1l11l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᢺ"))
        bstack11llllll1ll_opy_ = len(bstack11lll111lll_opy_)
        bstack11lllllllll_opy_ = ceil(bstack11llllll1ll_opy_ - bstack1l1111111l1_opy_ - bstack11llll1l1ll_opy_)
        if bstack11lllllllll_opy_ > 0:
            bstack11ll1lll1ll_opy_ = bstack11lll111lll_opy_[:bstack11lllllllll_opy_].decode(bstack1l11l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᢻ"), errors=bstack1l11l_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫᢼ")) + bstack1l111l1l111_opy_
            return bstack11ll1lll1ll_opy_
    except Exception as e:
        logger.debug(bstack1l11l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥᢽ").format(e))
    return field
def bstack1l11111l1_opy_():
    env = os.environ
    if (bstack1l11l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦᢾ") in env and len(env[bstack1l11l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᢿ")]) > 0) or (
            bstack1l11l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢᣀ") in env and len(env[bstack1l11l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᣁ")]) > 0):
        return {
            bstack1l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᣂ"): bstack1l11l_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧᣃ"),
            bstack1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᣄ"): env.get(bstack1l11l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᣅ")),
            bstack1l11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᣆ"): env.get(bstack1l11l_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥᣇ")),
            bstack1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᣈ"): env.get(bstack1l11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᣉ"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠦࡈࡏࠢᣊ")) == bstack1l11l_opy_ (u"ࠧࡺࡲࡶࡧࠥᣋ") and bstack11llllllll_opy_(env.get(bstack1l11l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣᣌ"))):
        return {
            bstack1l11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᣍ"): bstack1l11l_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥᣎ"),
            bstack1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᣏ"): env.get(bstack1l11l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᣐ")),
            bstack1l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᣑ"): env.get(bstack1l11l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤᣒ")),
            bstack1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᣓ"): env.get(bstack1l11l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥᣔ"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠣࡅࡌࠦᣕ")) == bstack1l11l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᣖ") and bstack11llllllll_opy_(env.get(bstack1l11l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥᣗ"))):
        return {
            bstack1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᣘ"): bstack1l11l_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣᣙ"),
            bstack1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᣚ"): env.get(bstack1l11l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢᣛ")),
            bstack1l11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᣜ"): env.get(bstack1l11l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᣝ")),
            bstack1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᣞ"): env.get(bstack1l11l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᣟ"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠧࡉࡉࠣᣠ")) == bstack1l11l_opy_ (u"ࠨࡴࡳࡷࡨࠦᣡ") and env.get(bstack1l11l_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣᣢ")) == bstack1l11l_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥᣣ"):
        return {
            bstack1l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᣤ"): bstack1l11l_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧᣥ"),
            bstack1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᣦ"): None,
            bstack1l11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᣧ"): None,
            bstack1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᣨ"): None
        }
    if env.get(bstack1l11l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥᣩ")) and env.get(bstack1l11l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦᣪ")):
        return {
            bstack1l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᣫ"): bstack1l11l_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨᣬ"),
            bstack1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᣭ"): env.get(bstack1l11l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥᣮ")),
            bstack1l11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᣯ"): None,
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᣰ"): env.get(bstack1l11l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᣱ"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠤࡆࡍࠧᣲ")) == bstack1l11l_opy_ (u"ࠥࡸࡷࡻࡥࠣᣳ") and bstack11llllllll_opy_(env.get(bstack1l11l_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥᣴ"))):
        return {
            bstack1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᣵ"): bstack1l11l_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧ᣶"),
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᣷"): env.get(bstack1l11l_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦ᣸")),
            bstack1l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᣹"): None,
            bstack1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᣺"): env.get(bstack1l11l_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᣻"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠧࡉࡉࠣ᣼")) == bstack1l11l_opy_ (u"ࠨࡴࡳࡷࡨࠦ᣽") and bstack11llllllll_opy_(env.get(bstack1l11l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥ᣾"))):
        return {
            bstack1l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᣿"): bstack1l11l_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧᤀ"),
            bstack1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᤁ"): env.get(bstack1l11l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥᤂ")),
            bstack1l11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᤃ"): env.get(bstack1l11l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᤄ")),
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᤅ"): env.get(bstack1l11l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦᤆ"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠤࡆࡍࠧᤇ")) == bstack1l11l_opy_ (u"ࠥࡸࡷࡻࡥࠣᤈ") and bstack11llllllll_opy_(env.get(bstack1l11l_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢᤉ"))):
        return {
            bstack1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᤊ"): bstack1l11l_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨᤋ"),
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᤌ"): env.get(bstack1l11l_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧᤍ")),
            bstack1l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᤎ"): env.get(bstack1l11l_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᤏ")),
            bstack1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᤐ"): env.get(bstack1l11l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣᤑ"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠨࡃࡊࠤᤒ")) == bstack1l11l_opy_ (u"ࠢࡵࡴࡸࡩࠧᤓ") and bstack11llllllll_opy_(env.get(bstack1l11l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦᤔ"))):
        return {
            bstack1l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᤕ"): bstack1l11l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨᤖ"),
            bstack1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᤗ"): env.get(bstack1l11l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᤘ")),
            bstack1l11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᤙ"): env.get(bstack1l11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤᤚ")) or env.get(bstack1l11l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᤛ")),
            bstack1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᤜ"): env.get(bstack1l11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᤝ"))
        }
    if bstack11llllllll_opy_(env.get(bstack1l11l_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᤞ"))):
        return {
            bstack1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᤟"): bstack1l11l_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨᤠ"),
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᤡ"): bstack1l11l_opy_ (u"ࠣࡽࢀࡿࢂࠨᤢ").format(env.get(bstack1l11l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᤣ")), env.get(bstack1l11l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪᤤ"))),
            bstack1l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᤥ"): env.get(bstack1l11l_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦᤦ")),
            bstack1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᤧ"): env.get(bstack1l11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᤨ"))
        }
    if bstack11llllllll_opy_(env.get(bstack1l11l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥᤩ"))):
        return {
            bstack1l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᤪ"): bstack1l11l_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧᤫ"),
            bstack1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᤬"): bstack1l11l_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦ᤭").format(env.get(bstack1l11l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬ᤮")), env.get(bstack1l11l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨ᤯")), env.get(bstack1l11l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᤰ")), env.get(bstack1l11l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᤱ"))),
            bstack1l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᤲ"): env.get(bstack1l11l_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᤳ")),
            bstack1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᤴ"): env.get(bstack1l11l_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᤵ"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣᤶ")) and env.get(bstack1l11l_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᤷ")):
        return {
            bstack1l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᤸ"): bstack1l11l_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍ᤹ࠧ"),
            bstack1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᤺"): bstack1l11l_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽ᤻ࠣ").format(env.get(bstack1l11l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩ᤼")), env.get(bstack1l11l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬ᤽")), env.get(bstack1l11l_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨ᤾"))),
            bstack1l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᤿"): env.get(bstack1l11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ᥀")),
            bstack1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᥁"): env.get(bstack1l11l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ᥂"))
        }
    if any([env.get(bstack1l11l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᥃")), env.get(bstack1l11l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᥄")), env.get(bstack1l11l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ᥅"))]):
        return {
            bstack1l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᥆"): bstack1l11l_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥ᥇"),
            bstack1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᥈"): env.get(bstack1l11l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᥉")),
            bstack1l11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᥊"): env.get(bstack1l11l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᥋")),
            bstack1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᥌"): env.get(bstack1l11l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ᥍"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ᥎")):
        return {
            bstack1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᥏"): bstack1l11l_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧᥐ"),
            bstack1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᥑ"): env.get(bstack1l11l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤᥒ")),
            bstack1l11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᥓ"): env.get(bstack1l11l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣᥔ")),
            bstack1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᥕ"): env.get(bstack1l11l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᥖ"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨᥗ")) or env.get(bstack1l11l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᥘ")):
        return {
            bstack1l11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᥙ"): bstack1l11l_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤᥚ"),
            bstack1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᥛ"): env.get(bstack1l11l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᥜ")),
            bstack1l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᥝ"): bstack1l11l_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧᥞ") if env.get(bstack1l11l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᥟ")) else None,
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᥠ"): env.get(bstack1l11l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᥡ"))
        }
    if any([env.get(bstack1l11l_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᥢ")), env.get(bstack1l11l_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᥣ")), env.get(bstack1l11l_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᥤ"))]):
        return {
            bstack1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᥥ"): bstack1l11l_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧᥦ"),
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᥧ"): None,
            bstack1l11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᥨ"): env.get(bstack1l11l_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨᥩ")),
            bstack1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᥪ"): env.get(bstack1l11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᥫ"))
        }
    if env.get(bstack1l11l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣᥬ")):
        return {
            bstack1l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᥭ"): bstack1l11l_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥ᥮"),
            bstack1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᥯"): env.get(bstack1l11l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᥰ")),
            bstack1l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᥱ"): bstack1l11l_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧᥲ").format(env.get(bstack1l11l_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨᥳ"))) if env.get(bstack1l11l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤᥴ")) else None,
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᥵"): env.get(bstack1l11l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᥶"))
        }
    if bstack11llllllll_opy_(env.get(bstack1l11l_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥ᥷"))):
        return {
            bstack1l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᥸"): bstack1l11l_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧ᥹"),
            bstack1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᥺"): env.get(bstack1l11l_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥ᥻")),
            bstack1l11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᥼"): env.get(bstack1l11l_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦ᥽")),
            bstack1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᥾"): env.get(bstack1l11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᥿"))
        }
    if bstack11llllllll_opy_(env.get(bstack1l11l_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧᦀ"))):
        return {
            bstack1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᦁ"): bstack1l11l_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢᦂ"),
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᦃ"): bstack1l11l_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤᦄ").format(env.get(bstack1l11l_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭ᦅ")), env.get(bstack1l11l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧᦆ")), env.get(bstack1l11l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫᦇ"))),
            bstack1l11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᦈ"): env.get(bstack1l11l_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣᦉ")),
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᦊ"): env.get(bstack1l11l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣᦋ"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠤࡆࡍࠧᦌ")) == bstack1l11l_opy_ (u"ࠥࡸࡷࡻࡥࠣᦍ") and env.get(bstack1l11l_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦᦎ")) == bstack1l11l_opy_ (u"ࠧ࠷ࠢᦏ"):
        return {
            bstack1l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᦐ"): bstack1l11l_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢᦑ"),
            bstack1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᦒ"): bstack1l11l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧᦓ").format(env.get(bstack1l11l_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧᦔ"))),
            bstack1l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᦕ"): None,
            bstack1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᦖ"): None,
        }
    if env.get(bstack1l11l_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤᦗ")):
        return {
            bstack1l11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᦘ"): bstack1l11l_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥᦙ"),
            bstack1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᦚ"): None,
            bstack1l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᦛ"): env.get(bstack1l11l_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧᦜ")),
            bstack1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᦝ"): env.get(bstack1l11l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᦞ"))
        }
    if any([env.get(bstack1l11l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥᦟ")), env.get(bstack1l11l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣᦠ")), env.get(bstack1l11l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢᦡ")), env.get(bstack1l11l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦᦢ"))]):
        return {
            bstack1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᦣ"): bstack1l11l_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣᦤ"),
            bstack1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᦥ"): None,
            bstack1l11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᦦ"): env.get(bstack1l11l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᦧ")) or None,
            bstack1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᦨ"): env.get(bstack1l11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᦩ"), 0)
        }
    if env.get(bstack1l11l_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᦪ")):
        return {
            bstack1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᦫ"): bstack1l11l_opy_ (u"ࠨࡇࡰࡅࡇࠦ᦬"),
            bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᦭"): None,
            bstack1l11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᦮"): env.get(bstack1l11l_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᦯")),
            bstack1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᦰ"): env.get(bstack1l11l_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥᦱ"))
        }
    if env.get(bstack1l11l_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᦲ")):
        return {
            bstack1l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᦳ"): bstack1l11l_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥᦴ"),
            bstack1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᦵ"): env.get(bstack1l11l_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᦶ")),
            bstack1l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᦷ"): env.get(bstack1l11l_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢᦸ")),
            bstack1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᦹ"): env.get(bstack1l11l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᦺ"))
        }
    return {bstack1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᦻ"): None}
def get_host_info():
    return {
        bstack1l11l_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥᦼ"): platform.node(),
        bstack1l11l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦᦽ"): platform.system(),
        bstack1l11l_opy_ (u"ࠥࡸࡾࡶࡥࠣᦾ"): platform.machine(),
        bstack1l11l_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧᦿ"): platform.version(),
        bstack1l11l_opy_ (u"ࠧࡧࡲࡤࡪࠥᧀ"): platform.architecture()[0]
    }
def bstack1l11111l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11lll1ll11l_opy_():
    if bstack1ll11111ll_opy_.get_property(bstack1l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᧁ")):
        return bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᧂ")
    return bstack1l11l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧᧃ")
def bstack11llll111ll_opy_(driver):
    info = {
        bstack1l11l_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᧄ"): driver.capabilities,
        bstack1l11l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧᧅ"): driver.session_id,
        bstack1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᧆ"): driver.capabilities.get(bstack1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᧇ"), None),
        bstack1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᧈ"): driver.capabilities.get(bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᧉ"), None),
        bstack1l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᧊"): driver.capabilities.get(bstack1l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᧋"), None),
    }
    if bstack11lll1ll11l_opy_() == bstack1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ᧌"):
        if bstack111l1l11l_opy_():
            info[bstack1l11l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ᧍")] = bstack1l11l_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᧎")
        elif driver.capabilities.get(bstack1l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᧏"), {}).get(bstack1l11l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ᧐"), False):
            info[bstack1l11l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ᧑")] = bstack1l11l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭᧒")
        else:
            info[bstack1l11l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ᧓")] = bstack1l11l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᧔")
    return info
def bstack111l1l11l_opy_():
    if bstack1ll11111ll_opy_.get_property(bstack1l11l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᧕")):
        return True
    if bstack11llllllll_opy_(os.environ.get(bstack1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ᧖"), None)):
        return True
    return False
def bstack11lllll1l_opy_(bstack11ll1l1llll_opy_, url, data, config):
    headers = config.get(bstack1l11l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ᧗"), None)
    proxies = bstack1l11ll11l_opy_(config, url)
    auth = config.get(bstack1l11l_opy_ (u"ࠨࡣࡸࡸ࡭࠭᧘"), None)
    response = requests.request(
            bstack11ll1l1llll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l11l11l1_opy_(bstack1lllllll1l_opy_, size):
    bstack1l11lll11l_opy_ = []
    while len(bstack1lllllll1l_opy_) > size:
        bstack1l1ll111_opy_ = bstack1lllllll1l_opy_[:size]
        bstack1l11lll11l_opy_.append(bstack1l1ll111_opy_)
        bstack1lllllll1l_opy_ = bstack1lllllll1l_opy_[size:]
    bstack1l11lll11l_opy_.append(bstack1lllllll1l_opy_)
    return bstack1l11lll11l_opy_
def bstack11lllll111l_opy_(message, bstack11lllll1ll1_opy_=False):
    os.write(1, bytes(message, bstack1l11l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᧙")))
    os.write(1, bytes(bstack1l11l_opy_ (u"ࠪࡠࡳ࠭᧚"), bstack1l11l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᧛")))
    if bstack11lllll1ll1_opy_:
        with open(bstack1l11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫ᧜") + os.environ[bstack1l11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ᧝")] + bstack1l11l_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬ᧞"), bstack1l11l_opy_ (u"ࠨࡣࠪ᧟")) as f:
            f.write(message + bstack1l11l_opy_ (u"ࠩ࡟ࡲࠬ᧠"))
def bstack1ll1111ll1l_opy_():
    return os.environ[bstack1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭᧡")].lower() == bstack1l11l_opy_ (u"ࠫࡹࡸࡵࡦࠩ᧢")
def bstack111l11l1l_opy_(bstack1l111111l1l_opy_):
    return bstack1l11l_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫ᧣").format(bstack1l1111ll111_opy_, bstack1l111111l1l_opy_)
def bstack111ll1l1l_opy_():
    return bstack11l111l1l1_opy_().replace(tzinfo=None).isoformat() + bstack1l11l_opy_ (u"࡚࠭ࠨ᧤")
def bstack11llll11ll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l11l_opy_ (u"࡛ࠧࠩ᧥"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l11l_opy_ (u"ࠨ࡜ࠪ᧦")))).total_seconds() * 1000
def bstack11lll1lll1l_opy_(timestamp):
    return bstack11lll11l111_opy_(timestamp).isoformat() + bstack1l11l_opy_ (u"ࠩ࡝ࠫ᧧")
def bstack11lll1llll1_opy_(bstack11ll1ll111l_opy_):
    date_format = bstack1l11l_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨ᧨")
    bstack11llll1111l_opy_ = datetime.datetime.strptime(bstack11ll1ll111l_opy_, date_format)
    return bstack11llll1111l_opy_.isoformat() + bstack1l11l_opy_ (u"ࠫ࡟࠭᧩")
def bstack11lllllll11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᧪")
    else:
        return bstack1l11l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᧫")
def bstack11llllllll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l11l_opy_ (u"ࠧࡵࡴࡸࡩࠬ᧬")
def bstack11lll11llll_opy_(val):
    return val.__str__().lower() == bstack1l11l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ᧭")
def bstack111llll1l1_opy_(bstack1l11111111l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1l11111111l_opy_ as e:
                print(bstack1l11l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤ᧮").format(func.__name__, bstack1l11111111l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11lll111l1l_opy_(bstack11llllll11l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11llllll11l_opy_(cls, *args, **kwargs)
            except bstack1l11111111l_opy_ as e:
                print(bstack1l11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥ᧯").format(bstack11llllll11l_opy_.__name__, bstack1l11111111l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11lll111l1l_opy_
    else:
        return decorator
def bstack1l111111ll_opy_(bstack111ll11111_opy_):
    if os.getenv(bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ᧰")) is not None:
        return bstack11llllllll_opy_(os.getenv(bstack1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᧱")))
    if bstack1l11l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᧲") in bstack111ll11111_opy_ and bstack11lll11llll_opy_(bstack111ll11111_opy_[bstack1l11l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᧳")]):
        return False
    if bstack1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᧴") in bstack111ll11111_opy_ and bstack11lll11llll_opy_(bstack111ll11111_opy_[bstack1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᧵")]):
        return False
    return True
def bstack1lll1lll1l_opy_():
    try:
        from pytest_bdd import reporting
        bstack11lll1111l1_opy_ = os.environ.get(bstack1l11l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥ᧶"), None)
        return bstack11lll1111l1_opy_ is None or bstack11lll1111l1_opy_ == bstack1l11l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ᧷")
    except Exception as e:
        return False
def bstack11l1l1l1_opy_(hub_url, CONFIG):
    if bstack11l1ll1ll_opy_() <= version.parse(bstack1l11l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ᧸")):
        if hub_url:
            return bstack1l11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ᧹") + hub_url + bstack1l11l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ᧺")
        return bstack1ll11lll1_opy_
    if hub_url:
        return bstack1l11l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ᧻") + hub_url + bstack1l11l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ᧼")
    return bstack1l1ll1l1_opy_
def bstack11ll1ll1111_opy_():
    return isinstance(os.getenv(bstack1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩ᧽")), str)
def bstack1l1ll1ll_opy_(url):
    return urlparse(url).hostname
def bstack1ll111ll1l_opy_(hostname):
    for bstack1llll1ll11_opy_ in bstack11ll11llll_opy_:
        regex = re.compile(bstack1llll1ll11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11llll1lll1_opy_(bstack11ll1llllll_opy_, file_name, logger):
    bstack11lll1l1_opy_ = os.path.join(os.path.expanduser(bstack1l11l_opy_ (u"ࠫࢃ࠭᧾")), bstack11ll1llllll_opy_)
    try:
        if not os.path.exists(bstack11lll1l1_opy_):
            os.makedirs(bstack11lll1l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l11l_opy_ (u"ࠬࢄࠧ᧿")), bstack11ll1llllll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l11l_opy_ (u"࠭ࡷࠨᨀ")):
                pass
            with open(file_path, bstack1l11l_opy_ (u"ࠢࡸ࠭ࠥᨁ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1l1llll_opy_.format(str(e)))
def bstack11ll1lll111_opy_(file_name, key, value, logger):
    file_path = bstack11llll1lll1_opy_(bstack1l11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᨂ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1lll1ll_opy_ = json.load(open(file_path, bstack1l11l_opy_ (u"ࠩࡵࡦࠬᨃ")))
        else:
            bstack1ll1lll1ll_opy_ = {}
        bstack1ll1lll1ll_opy_[key] = value
        with open(file_path, bstack1l11l_opy_ (u"ࠥࡻ࠰ࠨᨄ")) as outfile:
            json.dump(bstack1ll1lll1ll_opy_, outfile)
def bstack1l1l1lll1_opy_(file_name, logger):
    file_path = bstack11llll1lll1_opy_(bstack1l11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᨅ"), file_name, logger)
    bstack1ll1lll1ll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l11l_opy_ (u"ࠬࡸࠧᨆ")) as bstack1l11l1111l_opy_:
            bstack1ll1lll1ll_opy_ = json.load(bstack1l11l1111l_opy_)
    return bstack1ll1lll1ll_opy_
def bstack1ll1llll1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l11l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪᨇ") + file_path + bstack1l11l_opy_ (u"ࠧࠡࠩᨈ") + str(e))
def bstack11l1ll1ll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l11l_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥᨉ")
def bstack111lll11l_opy_(config):
    if bstack1l11l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᨊ") in config:
        del (config[bstack1l11l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᨋ")])
        return False
    if bstack11l1ll1ll_opy_() < version.parse(bstack1l11l_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪᨌ")):
        return False
    if bstack11l1ll1ll_opy_() >= version.parse(bstack1l11l_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫᨍ")):
        return True
    if bstack1l11l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᨎ") in config and config[bstack1l11l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᨏ")] is False:
        return False
    else:
        return True
def bstack111111111_opy_(args_list, bstack11llllll111_opy_):
    index = -1
    for value in bstack11llllll111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l11ll11l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l11ll11l_opy_ = bstack11l11ll11l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᨐ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᨑ"), exception=exception)
    def bstack111l11ll11_opy_(self):
        if self.result != bstack1l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᨒ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l11l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᨓ") in self.exception_type:
            return bstack1l11l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᨔ")
        return bstack1l11l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᨕ")
    def bstack11ll1lllll1_opy_(self):
        if self.result != bstack1l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᨖ"):
            return None
        if self.bstack11l11ll11l_opy_:
            return self.bstack11l11ll11l_opy_
        return bstack11ll1llll11_opy_(self.exception)
def bstack11ll1llll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll1l1ll1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1llll1llll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11lll111_opy_(config, logger):
    try:
        import playwright
        bstack11lll11ll11_opy_ = playwright.__file__
        bstack11ll1l1l111_opy_ = os.path.split(bstack11lll11ll11_opy_)
        bstack11lll1ll1l1_opy_ = bstack11ll1l1l111_opy_[0] + bstack1l11l_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫᨗ")
        os.environ[bstack1l11l_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ᨘࠬ")] = bstack11lll11lll_opy_(config)
        with open(bstack11lll1ll1l1_opy_, bstack1l11l_opy_ (u"ࠪࡶࠬᨙ")) as f:
            bstack1l1l1l111_opy_ = f.read()
            bstack11llll11lll_opy_ = bstack1l11l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪᨚ")
            bstack11lll11l11l_opy_ = bstack1l1l1l111_opy_.find(bstack11llll11lll_opy_)
            if bstack11lll11l11l_opy_ == -1:
              process = subprocess.Popen(bstack1l11l_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤᨛ"), shell=True, cwd=bstack11ll1l1l111_opy_[0])
              process.wait()
              bstack11lll111l11_opy_ = bstack1l11l_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭᨜")
              bstack11lll1111ll_opy_ = bstack1l11l_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦ᨝")
              bstack11ll1l1l1l1_opy_ = bstack1l1l1l111_opy_.replace(bstack11lll111l11_opy_, bstack11lll1111ll_opy_)
              with open(bstack11lll1ll1l1_opy_, bstack1l11l_opy_ (u"ࠨࡹࠪ᨞")) as f:
                f.write(bstack11ll1l1l1l1_opy_)
    except Exception as e:
        logger.error(bstack111ll1ll1_opy_.format(str(e)))
def bstack1llll111l1_opy_():
  try:
    bstack11lll11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩ᨟"))
    bstack11ll1ll1l11_opy_ = []
    if os.path.exists(bstack11lll11l1l1_opy_):
      with open(bstack11lll11l1l1_opy_) as f:
        bstack11ll1ll1l11_opy_ = json.load(f)
      os.remove(bstack11lll11l1l1_opy_)
    return bstack11ll1ll1l11_opy_
  except:
    pass
  return []
def bstack11lll1ll_opy_(bstack1l1l11ll_opy_):
  try:
    bstack11ll1ll1l11_opy_ = []
    bstack11lll11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪᨠ"))
    if os.path.exists(bstack11lll11l1l1_opy_):
      with open(bstack11lll11l1l1_opy_) as f:
        bstack11ll1ll1l11_opy_ = json.load(f)
    bstack11ll1ll1l11_opy_.append(bstack1l1l11ll_opy_)
    with open(bstack11lll11l1l1_opy_, bstack1l11l_opy_ (u"ࠫࡼ࠭ᨡ")) as f:
        json.dump(bstack11ll1ll1l11_opy_, f)
  except:
    pass
def bstack11l1llll1l_opy_(logger, bstack11llllll1l1_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l11l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᨢ"), bstack1l11l_opy_ (u"࠭ࠧᨣ"))
    if test_name == bstack1l11l_opy_ (u"ࠧࠨᨤ"):
        test_name = threading.current_thread().__dict__.get(bstack1l11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧᨥ"), bstack1l11l_opy_ (u"ࠩࠪᨦ"))
    bstack11llll111l1_opy_ = bstack1l11l_opy_ (u"ࠪ࠰ࠥ࠭ᨧ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11llllll1l1_opy_:
        bstack111ll111l_opy_ = os.environ.get(bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᨨ"), bstack1l11l_opy_ (u"ࠬ࠶ࠧᨩ"))
        bstack1ll11l1ll1_opy_ = {bstack1l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᨪ"): test_name, bstack1l11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᨫ"): bstack11llll111l1_opy_, bstack1l11l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᨬ"): bstack111ll111l_opy_}
        bstack11lll1l1l1l_opy_ = []
        bstack11llll11l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᨭ"))
        if os.path.exists(bstack11llll11l1l_opy_):
            with open(bstack11llll11l1l_opy_) as f:
                bstack11lll1l1l1l_opy_ = json.load(f)
        bstack11lll1l1l1l_opy_.append(bstack1ll11l1ll1_opy_)
        with open(bstack11llll11l1l_opy_, bstack1l11l_opy_ (u"ࠪࡻࠬᨮ")) as f:
            json.dump(bstack11lll1l1l1l_opy_, f)
    else:
        bstack1ll11l1ll1_opy_ = {bstack1l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᨯ"): test_name, bstack1l11l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᨰ"): bstack11llll111l1_opy_, bstack1l11l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᨱ"): str(multiprocessing.current_process().name)}
        if bstack1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫᨲ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll11l1ll1_opy_)
  except Exception as e:
      logger.warn(bstack1l11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᨳ").format(e))
def bstack11ll1llll_opy_(error_message, test_name, index, logger):
  try:
    bstack11lll111111_opy_ = []
    bstack1ll11l1ll1_opy_ = {bstack1l11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᨴ"): test_name, bstack1l11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᨵ"): error_message, bstack1l11l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᨶ"): index}
    bstack11ll1lll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ᨷ"))
    if os.path.exists(bstack11ll1lll11l_opy_):
        with open(bstack11ll1lll11l_opy_) as f:
            bstack11lll111111_opy_ = json.load(f)
    bstack11lll111111_opy_.append(bstack1ll11l1ll1_opy_)
    with open(bstack11ll1lll11l_opy_, bstack1l11l_opy_ (u"࠭ࡷࠨᨸ")) as f:
        json.dump(bstack11lll111111_opy_, f)
  except Exception as e:
    logger.warn(bstack1l11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᨹ").format(e))
def bstack1l11llll_opy_(bstack1l111l11l1_opy_, name, logger):
  try:
    bstack1ll11l1ll1_opy_ = {bstack1l11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᨺ"): name, bstack1l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᨻ"): bstack1l111l11l1_opy_, bstack1l11l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᨼ"): str(threading.current_thread()._name)}
    return bstack1ll11l1ll1_opy_
  except Exception as e:
    logger.warn(bstack1l11l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣᨽ").format(e))
  return
def bstack11ll1l111ll_opy_():
    return platform.system() == bstack1l11l_opy_ (u"ࠬ࡝ࡩ࡯ࡦࡲࡻࡸ࠭ᨾ")
def bstack1ll11llll1_opy_(bstack11lllllll1l_opy_, config, logger):
    bstack11ll1ll11ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11lllllll1l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡱࡺࡥࡳࠢࡦࡳࡳ࡬ࡩࡨࠢ࡮ࡩࡾࡹࠠࡣࡻࠣࡶࡪ࡭ࡥࡹࠢࡰࡥࡹࡩࡨ࠻ࠢࡾࢁࠧᨿ").format(e))
    return bstack11ll1ll11ll_opy_
def bstack11ll1l1ll11_opy_(bstack1l1111111ll_opy_, bstack11ll1l1l1ll_opy_):
    bstack11lll1lllll_opy_ = version.parse(bstack1l1111111ll_opy_)
    bstack1l111111l11_opy_ = version.parse(bstack11ll1l1l1ll_opy_)
    if bstack11lll1lllll_opy_ > bstack1l111111l11_opy_:
        return 1
    elif bstack11lll1lllll_opy_ < bstack1l111111l11_opy_:
        return -1
    else:
        return 0
def bstack11l111l1l1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11lll11l111_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11lll1ll1ll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lllllll1_opy_(options, framework, bstack1111l1lll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l11l_opy_ (u"ࠧࡨࡧࡷࠫᩀ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1111ll1l_opy_ = caps.get(bstack1l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᩁ"))
    bstack11ll1l11lll_opy_ = True
    bstack11ll11l1l1_opy_ = os.environ[bstack1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᩂ")]
    if bstack11lll11llll_opy_(caps.get(bstack1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪ࡝࠳ࡄࠩᩃ"))) or bstack11lll11llll_opy_(caps.get(bstack1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫᩄ"))):
        bstack11ll1l11lll_opy_ = False
    if bstack111lll11l_opy_({bstack1l11l_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧᩅ"): bstack11ll1l11lll_opy_}):
        bstack1l1111ll1l_opy_ = bstack1l1111ll1l_opy_ or {}
        bstack1l1111ll1l_opy_[bstack1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᩆ")] = bstack11lll1ll1ll_opy_(framework)
        bstack1l1111ll1l_opy_[bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᩇ")] = bstack1ll1111ll1l_opy_()
        bstack1l1111ll1l_opy_[bstack1l11l_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᩈ")] = bstack11ll11l1l1_opy_
        bstack1l1111ll1l_opy_[bstack1l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᩉ")] = bstack1111l1lll_opy_
        if getattr(options, bstack1l11l_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫᩊ"), None):
            options.set_capability(bstack1l11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᩋ"), bstack1l1111ll1l_opy_)
        else:
            options[bstack1l11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᩌ")] = bstack1l1111ll1l_opy_
    else:
        if getattr(options, bstack1l11l_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧᩍ"), None):
            options.set_capability(bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᩎ"), bstack11lll1ll1ll_opy_(framework))
            options.set_capability(bstack1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᩏ"), bstack1ll1111ll1l_opy_())
            options.set_capability(bstack1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᩐ"), bstack11ll11l1l1_opy_)
            options.set_capability(bstack1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᩑ"), bstack1111l1lll_opy_)
        else:
            options[bstack1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᩒ")] = bstack11lll1ll1ll_opy_(framework)
            options[bstack1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᩓ")] = bstack1ll1111ll1l_opy_()
            options[bstack1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᩔ")] = bstack11ll11l1l1_opy_
            options[bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᩕ")] = bstack1111l1lll_opy_
    return options
def bstack11llll1l1l1_opy_(bstack11llll11111_opy_, framework):
    bstack1111l1lll_opy_ = bstack1ll11111ll_opy_.get_property(bstack1l11l_opy_ (u"ࠣࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡖࡒࡐࡆࡘࡇ࡙ࡥࡍࡂࡒࠥᩖ"))
    if bstack11llll11111_opy_ and len(bstack11llll11111_opy_.split(bstack1l11l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᩗ"))) > 1:
        ws_url = bstack11llll11111_opy_.split(bstack1l11l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᩘ"))[0]
        if bstack1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᩙ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11ll1ll1lll_opy_ = json.loads(urllib.parse.unquote(bstack11llll11111_opy_.split(bstack1l11l_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᩚ"))[1]))
            bstack11ll1ll1lll_opy_ = bstack11ll1ll1lll_opy_ or {}
            bstack11ll11l1l1_opy_ = os.environ[bstack1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᩛ")]
            bstack11ll1ll1lll_opy_[bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᩜ")] = str(framework) + str(__version__)
            bstack11ll1ll1lll_opy_[bstack1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᩝ")] = bstack1ll1111ll1l_opy_()
            bstack11ll1ll1lll_opy_[bstack1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᩞ")] = bstack11ll11l1l1_opy_
            bstack11ll1ll1lll_opy_[bstack1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ᩟")] = bstack1111l1lll_opy_
            bstack11llll11111_opy_ = bstack11llll11111_opy_.split(bstack1l11l_opy_ (u"ࠫࡨࡧࡰࡴ࠿᩠ࠪ"))[0] + bstack1l11l_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᩡ") + urllib.parse.quote(json.dumps(bstack11ll1ll1lll_opy_))
    return bstack11llll11111_opy_
def bstack11ll1l1l1_opy_():
    global bstack11llll11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11llll11_opy_ = BrowserType.connect
    return bstack11llll11_opy_
def bstack1llll111l_opy_(framework_name):
    global bstack1l1l1111_opy_
    bstack1l1l1111_opy_ = framework_name
    return framework_name
def bstack1l1ll1l11l_opy_(self, *args, **kwargs):
    global bstack11llll11_opy_
    try:
        global bstack1l1l1111_opy_
        if bstack1l11l_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᩢ") in kwargs:
            kwargs[bstack1l11l_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᩣ")] = bstack11llll1l1l1_opy_(
                kwargs.get(bstack1l11l_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᩤ"), None),
                bstack1l1l1111_opy_
            )
    except Exception as e:
        logger.error(bstack1l11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤᩥ").format(str(e)))
    return bstack11llll11_opy_(self, *args, **kwargs)
def bstack11lll1l1l11_opy_(bstack11ll1ll11l1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l11ll11l_opy_(bstack11ll1ll11l1_opy_, bstack1l11l_opy_ (u"ࠥࠦᩦ"))
        if proxies and proxies.get(bstack1l11l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᩧ")):
            parsed_url = urlparse(proxies.get(bstack1l11l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᩨ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l11l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩᩩ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l11l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᩪ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᩫ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᩬ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1lll1l11ll_opy_(bstack11ll1ll11l1_opy_):
    bstack11ll1ll1l1l_opy_ = {
        bstack1l1111l11l1_opy_[bstack11lll1lll11_opy_]: bstack11ll1ll11l1_opy_[bstack11lll1lll11_opy_]
        for bstack11lll1lll11_opy_ in bstack11ll1ll11l1_opy_
        if bstack11lll1lll11_opy_ in bstack1l1111l11l1_opy_
    }
    bstack11ll1ll1l1l_opy_[bstack1l11l_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥᩭ")] = bstack11lll1l1l11_opy_(bstack11ll1ll11l1_opy_, bstack1ll11111ll_opy_.get_property(bstack1l11l_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᩮ")))
    bstack11llll11l11_opy_ = [element.lower() for element in bstack1l11111ll1l_opy_]
    bstack1l111111111_opy_(bstack11ll1ll1l1l_opy_, bstack11llll11l11_opy_)
    return bstack11ll1ll1l1l_opy_
def bstack1l111111111_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l11l_opy_ (u"ࠧ࠰ࠪࠫࠬࠥᩯ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1l111111111_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1l111111111_opy_(item, keys)
def bstack11llll1ll11_opy_():
    bstack11ll1l11l11_opy_ = [os.environ.get(bstack1l11l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡉࡍࡇࡖࡣࡉࡏࡒࠣᩰ")), os.path.join(os.path.expanduser(bstack1l11l_opy_ (u"ࠢࡿࠤᩱ")), bstack1l11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᩲ")), os.path.join(bstack1l11l_opy_ (u"ࠩ࠲ࡸࡲࡶࠧᩳ"), bstack1l11l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᩴ"))]
    for path in bstack11ll1l11l11_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l11l_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦ᩵") + str(path) + bstack1l11l_opy_ (u"ࠧ࠭ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣ᩶"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l11l_opy_ (u"ࠨࡇࡪࡸ࡬ࡲ࡬ࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠤ࡫ࡵࡲࠡࠩࠥ᩷") + str(path) + bstack1l11l_opy_ (u"ࠢࠨࠤ᩸"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l11l_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣ᩹") + str(path) + bstack1l11l_opy_ (u"ࠤࠪࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡮ࡡࡴࠢࡷ࡬ࡪࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠴ࠢ᩺"))
            else:
                logger.debug(bstack1l11l_opy_ (u"ࠥࡇࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࠫࠧ᩻") + str(path) + bstack1l11l_opy_ (u"ࠦࠬࠦࡷࡪࡶ࡫ࠤࡼࡸࡩࡵࡧࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴ࠮ࠣ᩼"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l11l_opy_ (u"ࠧࡕࡰࡦࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠤ࡫ࡵࡲࠡࠩࠥ᩽") + str(path) + bstack1l11l_opy_ (u"ࠨࠧ࠯ࠤ᩾"))
            return path
        except Exception as e:
            logger.debug(bstack1l11l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡶࡲࠣࡪ࡮ࡲࡥࠡࠩࡾࡴࡦࡺࡨࡾࠩ࠽ࠤ᩿ࠧ") + str(e) + bstack1l11l_opy_ (u"ࠣࠤ᪀"))
    logger.debug(bstack1l11l_opy_ (u"ࠤࡄࡰࡱࠦࡰࡢࡶ࡫ࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠨ᪁"))
    return None
@measure(event_name=EVENTS.bstack1l1111l1111_opy_, stage=STAGE.bstack1111111l_opy_)
def bstack1lll11ll111_opy_(binary_path, bstack1lll1ll1ll1_opy_, bs_config):
    logger.debug(bstack1l11l_opy_ (u"ࠥࡇࡺࡸࡲࡦࡰࡷࠤࡈࡒࡉࠡࡒࡤࡸ࡭ࠦࡦࡰࡷࡱࡨ࠿ࠦࡻࡾࠤ᪂").format(binary_path))
    bstack11ll1llll1l_opy_ = bstack1l11l_opy_ (u"ࠫࠬ᪃")
    bstack11llll1l11l_opy_ = {
        bstack1l11l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ᪄"): __version__,
        bstack1l11l_opy_ (u"ࠨ࡯ࡴࠤ᪅"): platform.system(),
        bstack1l11l_opy_ (u"ࠢࡰࡵࡢࡥࡷࡩࡨࠣ᪆"): platform.machine(),
        bstack1l11l_opy_ (u"ࠣࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ᪇"): bstack1l11l_opy_ (u"ࠩ࠳ࠫ᪈"),
        bstack1l11l_opy_ (u"ࠥࡷࡩࡱ࡟࡭ࡣࡱ࡫ࡺࡧࡧࡦࠤ᪉"): bstack1l11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ᪊")
    }
    try:
        if binary_path:
            bstack11llll1l11l_opy_[bstack1l11l_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ᪋")] = subprocess.check_output([binary_path, bstack1l11l_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ᪌")]).strip().decode(bstack1l11l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭᪍"))
        response = requests.request(
            bstack1l11l_opy_ (u"ࠨࡉࡈࡘࠬ᪎"),
            url=bstack111l11l1l_opy_(bstack1l1111l1l1l_opy_),
            headers=None,
            auth=(bs_config[bstack1l11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ᪏")], bs_config[bstack1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭᪐")]),
            json=None,
            params=bstack11llll1l11l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l11l_opy_ (u"ࠫࡺࡸ࡬ࠨ᪑") in data.keys() and bstack1l11l_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩࡥࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᪒") in data.keys():
            logger.debug(bstack1l11l_opy_ (u"ࠨࡎࡦࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡣ࡫ࡱࡥࡷࡿࠬࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰ࠽ࠤࢀࢃࠢ᪓").format(bstack11llll1l11l_opy_[bstack1l11l_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᪔")]))
            bstack11lllll1lll_opy_ = bstack11lll11lll1_opy_(data[bstack1l11l_opy_ (u"ࠨࡷࡵࡰࠬ᪕")], bstack1lll1ll1ll1_opy_)
            bstack11ll1llll1l_opy_ = os.path.join(bstack1lll1ll1ll1_opy_, bstack11lllll1lll_opy_)
            os.chmod(bstack11ll1llll1l_opy_, 0o777) # bstack11llll1llll_opy_ permission
            return bstack11ll1llll1l_opy_
    except Exception as e:
        logger.debug(bstack1l11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡖࡈࡐࠦࡻࡾࠤ᪖").format(e))
    return binary_path
@measure(event_name=EVENTS.bstack1l111l11l1l_opy_, stage=STAGE.bstack1111111l_opy_)
def bstack11lll11lll1_opy_(bstack11ll1l11l1l_opy_, bstack11llll1ll1l_opy_):
    logger.debug(bstack1l11l_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯࠽ࠤࠧ᪗") + str(bstack11ll1l11l1l_opy_) + bstack1l11l_opy_ (u"ࠦࠧ᪘"))
    zip_path = os.path.join(bstack11llll1ll1l_opy_, bstack1l11l_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡡࡩ࡭ࡱ࡫࠮ࡻ࡫ࡳࠦ᪙"))
    bstack11lllll1lll_opy_ = bstack1l11l_opy_ (u"࠭ࠧ᪚")
    with requests.get(bstack11ll1l11l1l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l11l_opy_ (u"ࠢࡸࡤࠥ᪛")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l11l_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠥ᪜"))
    with zipfile.ZipFile(zip_path, bstack1l11l_opy_ (u"ࠩࡵࠫ᪝")) as zip_ref:
        bstack11lllll1l1l_opy_ = zip_ref.namelist()
        if len(bstack11lllll1l1l_opy_) > 0:
            bstack11lllll1lll_opy_ = bstack11lllll1l1l_opy_[0] # bstack11lll1l11ll_opy_ bstack1l111l11lll_opy_ will be bstack11ll1l11ll1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11llll1ll1l_opy_)
        logger.debug(bstack1l11l_opy_ (u"ࠥࡊ࡮ࡲࡥࡴࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡧࡻࡸࡷࡧࡣࡵࡧࡧࠤࡹࡵࠠࠨࠤ᪞") + str(bstack11llll1ll1l_opy_) + bstack1l11l_opy_ (u"ࠦࠬࠨ᪟"))
    os.remove(zip_path)
    return bstack11lllll1lll_opy_
def get_cli_dir():
    bstack11ll1ll1ll1_opy_ = bstack11llll1ll11_opy_()
    if bstack11ll1ll1ll1_opy_:
        bstack1lll1ll1ll1_opy_ = os.path.join(bstack11ll1ll1ll1_opy_, bstack1l11l_opy_ (u"ࠧࡩ࡬ࡪࠤ᪠"))
        if not os.path.exists(bstack1lll1ll1ll1_opy_):
            os.makedirs(bstack1lll1ll1ll1_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1ll1ll1_opy_
    else:
        raise FileNotFoundError(bstack1l11l_opy_ (u"ࠨࡎࡰࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠤ᪡"))
def bstack1llll11l1ll_opy_(bstack1lll1ll1ll1_opy_):
    bstack1l11l_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯࡮ࠡࡣࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠤࠥࠦ᪢")
    bstack11ll1lll1l1_opy_ = [
        os.path.join(bstack1lll1ll1ll1_opy_, f)
        for f in os.listdir(bstack1lll1ll1ll1_opy_)
        if os.path.isfile(os.path.join(bstack1lll1ll1ll1_opy_, f)) and f.startswith(bstack1l11l_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹ࠮ࠤ᪣"))
    ]
    if len(bstack11ll1lll1l1_opy_) > 0:
        return max(bstack11ll1lll1l1_opy_, key=os.path.getmtime) # get bstack11lll1ll111_opy_ binary
    return bstack1l11l_opy_ (u"ࠤࠥ᪤")