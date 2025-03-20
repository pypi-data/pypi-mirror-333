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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1lll1ll1_opy_
bstack1l1l1lll1_opy_ = Config.bstack11l111l11_opy_()
def bstack11l11l111ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11l11l11l1l_opy_(bstack11l11l11l11_opy_, bstack11l11l11lll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11l11l11l11_opy_):
        with open(bstack11l11l11l11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11l11l111ll_opy_(bstack11l11l11l11_opy_):
        pac = get_pac(url=bstack11l11l11l11_opy_)
    else:
        raise Exception(bstack11_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧᯫ").format(bstack11l11l11l11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤᯬ"), 80))
        bstack11l11l1l111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11l11l1l111_opy_ = bstack11_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪᯭ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11l11l11lll_opy_, bstack11l11l1l111_opy_)
    return proxy_url
def bstack1l111lll1_opy_(config):
    return bstack11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᯮ") in config or bstack11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᯯ") in config
def bstack111111l11_opy_(config):
    if not bstack1l111lll1_opy_(config):
        return
    if config.get(bstack11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᯰ")):
        return config.get(bstack11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᯱ"))
    if config.get(bstack11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼ᯲ࠫ")):
        return config.get(bstack11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽ᯳ࠬ"))
def bstack11l1ll11_opy_(config, bstack11l11l11lll_opy_):
    proxy = bstack111111l11_opy_(config)
    proxies = {}
    if config.get(bstack11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᯴")) or config.get(bstack11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᯵")):
        if proxy.endswith(bstack11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ᯶")):
            proxies = bstack11l11llll_opy_(proxy, bstack11l11l11lll_opy_)
        else:
            proxies = {
                bstack11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ᯷"): proxy
            }
    bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭᯸"), proxies)
    return proxies
def bstack11l11llll_opy_(bstack11l11l11l11_opy_, bstack11l11l11lll_opy_):
    proxies = {}
    global bstack11l11l11ll1_opy_
    if bstack11_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪ᯹") in globals():
        return bstack11l11l11ll1_opy_
    try:
        proxy = bstack11l11l11l1l_opy_(bstack11l11l11l11_opy_, bstack11l11l11lll_opy_)
        if bstack11_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣ᯺") in proxy:
            proxies = {}
        elif bstack11_opy_ (u"ࠤࡋࡘ࡙ࡖࠢ᯻") in proxy or bstack11_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤ᯼") in proxy or bstack11_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥ᯽") in proxy:
            bstack11l11l1l11l_opy_ = proxy.split(bstack11_opy_ (u"ࠧࠦࠢ᯾"))
            if bstack11_opy_ (u"ࠨ࠺࠰࠱ࠥ᯿") in bstack11_opy_ (u"ࠢࠣᰀ").join(bstack11l11l1l11l_opy_[1:]):
                proxies = {
                    bstack11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᰁ"): bstack11_opy_ (u"ࠤࠥᰂ").join(bstack11l11l1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᰃ"): str(bstack11l11l1l11l_opy_[0]).lower() + bstack11_opy_ (u"ࠦ࠿࠵࠯ࠣᰄ") + bstack11_opy_ (u"ࠧࠨᰅ").join(bstack11l11l1l11l_opy_[1:])
                }
        elif bstack11_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧᰆ") in proxy:
            bstack11l11l1l11l_opy_ = proxy.split(bstack11_opy_ (u"ࠢࠡࠤᰇ"))
            if bstack11_opy_ (u"ࠣ࠼࠲࠳ࠧᰈ") in bstack11_opy_ (u"ࠤࠥᰉ").join(bstack11l11l1l11l_opy_[1:]):
                proxies = {
                    bstack11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᰊ"): bstack11_opy_ (u"ࠦࠧᰋ").join(bstack11l11l1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᰌ"): bstack11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᰍ") + bstack11_opy_ (u"ࠢࠣᰎ").join(bstack11l11l1l11l_opy_[1:])
                }
        else:
            proxies = {
                bstack11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᰏ"): proxy
            }
    except Exception as e:
        print(bstack11_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᰐ"), bstack11l1lll1ll1_opy_.format(bstack11l11l11l11_opy_, str(e)))
    bstack11l11l11ll1_opy_ = proxies
    return proxies