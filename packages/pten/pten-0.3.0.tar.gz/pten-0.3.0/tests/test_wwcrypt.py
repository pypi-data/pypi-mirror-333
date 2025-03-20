from .conftest import use_real_keys
from pten.wwcrypt import WXBizMsgCrypt
from pten.keys import Keys
import pytest


@pytest.fixture()
def wwcpt(key_filepath_example):
    keys = Keys(key_filepath_example)
    CORP_ID = keys.get_key("ww", "corpid")
    API_TOKEN = keys.get_key("ww", "app_token")
    API_AES_KEY = keys.get_key("ww", "app_aes_key")

    wwcpt = WXBizMsgCrypt(API_TOKEN, API_AES_KEY, CORP_ID)
    return wwcpt


def test_VerifyURL(wwcpt):
    if not use_real_keys:
        pytest.skip("use_real_keys is False")

    msg_signature = "fa256ca984aa648c058fe106d9fb766cb5271299"
    timestamp = "1740712860"
    nonce = "1741290221"
    echostr = "ZiukUpbK6YHaHAQ2FFKciqqehcgztxpA0qd4PHf4jCS/xZ4Yw0IF+utac04PF4HqB7bKNF+7h1qsaZRKUjoZWA=="
    echo_str_expected = b"7805676074021366686"
    ret, echo_str_decrypted = wwcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
    assert ret == 0
    assert echo_str_decrypted == echo_str_expected


def test_DecryptMsg(wwcpt):
    if not use_real_keys:
        pytest.skip("use_real_keys is False")

    sPostData = "<xml><ToUserName><![CDATA[wwdb36ffe501dc44ba]]></ToUserName><Encrypt><![CDATA[Lc2M6ZsoQ08Us9UdegINhn4NOAj64Rtecn8onJ544OsSgkLX5O16XqtnO0xkc0cE3fzgy5vXZd/CZPtmAJlXaR1qfIINKm+w3J8LP17WnuD98MvkwHO5Vje1n69GouXU+fYujCtsd2TM8L7exzuooJXJao1mqpvUqHMUArvRvo+XVcyXSbBhWB+rzj8zcVSwu4JSzPxwdqVk2Q3GNVVxaDw8DfH0nhivjEeLdlD0IaDCw2pNn62lLpHZvZ52T+AV1HvIj+OZ4QvQ6cw3Ntr9gtpAuaA/HQbqXNT7pYCUss4KqmFAGjkVAH88ceF5iL7DrI4oPTTTzZ43DD3YK07bRdJU7w5j/H+b2oRFru8Q+RQFnh+jsTQIGR39gWHRr1qYJZr8ixeKuA2OZYLe84yRkhZA8EFUdUwIgW9lPyDK4Ew=]]></Encrypt><AgentID><![CDATA[1000005]]></AgentID></xml>"
    msg_signature = "89ab6f020ae9cf2792f04e6b535f92806dcaee14"
    timestamp = "1740718337"
    nonce = "1741092583"
    ret, sMsg = wwcpt.DecryptMsg(sPostData, msg_signature, timestamp, nonce)
    sMsg_expected = b"<xml><ToUserName><![CDATA[wwdb36ffe501dc44ba]]></ToUserName><FromUserName><![CDATA[PengYong]]></FromUserName><CreateTime>1740718337</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[hello]]></Content><MsgId>7476328330859679818</MsgId><AgentID>1000005</AgentID></xml>"

    assert ret == 0
    assert sMsg == sMsg_expected


def test_EncryptMsg(wwcpt):
    sReplyMsg = "hello"
    nonce = "1741290221"
    ret, send_msg = wwcpt.EncryptMsg(sReplyMsg=sReplyMsg, sNonce=nonce)
    assert ret == 0
