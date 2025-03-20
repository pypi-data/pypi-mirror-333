from .conftest import use_real_keys
from pten.keys import Keys
import pytest


pytestmark = pytest.mark.skipif(use_real_keys, reason="Skipping when using real keys")


def test_key_path_not_exist():
    keys = Keys("not_exist.ini")
    with pytest.raises(FileNotFoundError):
        keys.get_bot_weebhook_key()


@pytest.mark.parametrize(
    "section,option,expected",
    [
        ("ww", "app_aes_key", "9z1Cj9cSd7WtEV3hOWo5iMQlFkSP9Td1ejzsV9WhCmO"),
        ("ww", "app_agentid", "1000005"),
        ("ww", "app_secret", "jVJF_EBWCVA_KVi_89YnY1T1bPD8-0PdqQ2rXc_Pgmj5"),
        ("ww", "app_token", "zJdPmXg8E4J1mMdnzP8d"),
        ("ww", "contact_sync_secret", "G4PC19fIwfsykabdv_drNVlOIe_crBvay3sUX8DhGss"),
        ("ww", "corpid", "wwdb63ff5ae01cd4b4"),
        ("ww", "webhook_key", "7ande764-52a4-43d7-a252-05e8abcdb863"),
        ("notice", "deepseek_api_key", "sk-0a6e5b4e8b4c0e1a5b6b8e0e4d5aefb"),
        ("notice", "seniverse_api_key", "v5bFw3o1pSmbGvuEN"),
    ],
)
def test_get_key(key_filepath_example, section, option, expected):
    keys = Keys(key_filepath_example)
    assert keys.get_key(section, option) == expected


@pytest.mark.parametrize(
    "section,options,expected",
    [
        (
            "proxies",
            ["http", "https"],
            {
                "http": "http://xxx:xxx@xxx.xxx.xxx.xxx:8888",
                "https": "http://xxx:xxx@xxx.xxx.xxx.xxx:8888",
            },
        )
    ],
)
def test_get_keys(key_filepath_example, section, options, expected):
    keys = Keys(key_filepath_example)
    assert keys.get_keys(section, options) == expected


def test_get_debug_mode(key_filepath_example):
    keys = Keys(key_filepath_example)
    assert keys.get_debug_mode() is False

    keys_no_debug_mode = Keys("pten_keys_example_min.ini")
    assert keys_no_debug_mode.get_debug_mode() is False


def test_proxies(key_filepath_example):
    keys = Keys(key_filepath_example)
    proxies_expected = {
        "http": "http://xxx:xxx@xxx.xxx.xxx.xxx:8888",
        "https": "http://xxx:xxx@xxx.xxx.xxx.xxx:8888",
    }
    assert keys.get_proxies() == proxies_expected

    keys_no_proxies = Keys("pten_keys_example_min.ini")
    assert keys_no_proxies.get_proxies() is None


def test_bot_weebhook_key(key_filepath_example):
    keys = Keys(key_filepath_example)
    assert keys.get_bot_weebhook_key() == "7ande764-52a4-43d7-a252-05e8abcdb863"
