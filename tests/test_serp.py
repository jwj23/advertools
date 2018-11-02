import logging
import os
from itertools import product

import pandas as pd
import pytest

from advertools.serp import (serp_goog, serp_youtube, SERP_GOOG_VALID_VALS,
                             SERP_YTUBE_VALID_VALS, youtube_channel_details,
                             youtube_video_details, YOUTUBE_VID_CATEGORY_IDS,
                             YOUTUBE_TOPIC_IDS, _dict_product, set_logging_level)

goog_cse_cx = os.environ.get('GOOG_CSE_CX')
goog_cse_key = os.environ.get('GOOG_CSE_KEY')
youtube_key = os.environ.get('YOUTUBE_KEY')


def test_dict_product_produces_correct_result():
    d = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [10, 20]}
    dp = _dict_product(d)
    assert (sorted(list(product(*d.values()))) ==
            sorted([tuple(x.values()) for x in dp]))
    assert (sorted([tuple(x.keys()) for x in dp]) ==
            sorted([tuple(d.keys()) for x in range(len(dp))]))


def test_dict_product_return_correct_types():
    d = {'a': [1], 'b': [10, 20, 30], 'c': (4, 5, 6)}
    dp = _dict_product(d)
    assert isinstance(dp, list)
    assert [isinstance(x, dict) for x in dp]
    assert len(dp) == len(list(product(*d.values())))


# Google search tests:
def test_serp_goog_raises_error_on_invalid_args():
    with pytest.raises(ValueError):
        for val in SERP_GOOG_VALID_VALS:
            params = {val: 'WRONG VALUE'}
            serp_goog(q='q', cx='cx', key='key', **params)


def test_serp_goog_return_correct_result():
    result = serp_goog(q='testing hotels', cx=goog_cse_cx,
                       key=goog_cse_key, searchType=['image', None])
    assert isinstance(result, pd.core.frame.DataFrame)
    assert 'title' in result
    assert 'image' in result
    assert len(result) == 20


def test_serp_goog_handles_no_search_results():
    q = 'aquerythatdoesntgetrezultssss'
    result = serp_goog(q=q, cx=goog_cse_cx, key=goog_cse_key,
                       cr='countryRU', hl='zh-TW', gl='nf')
    assert len(result) == 1
    assert result['searchTerms'].values[0] == q


# YouTube search tests:
def test_serp_youtube_raises_error_on_invalid_args():
    with pytest.raises(ValueError):
        for val in SERP_YTUBE_VALID_VALS:
            params = {val: 'WRONG VALUE'}
            serp_youtube(q='q', key='key', **params)


def test_serp_youtube_return_correct_result():
    result = serp_youtube(q='testing hotels', key=youtube_key,
                          order='date')
    assert isinstance(result, pd.core.frame.DataFrame)
    assert 'title' in result
    assert 'rank' in result
    assert len(result) == 5


def test_serp_youtube_handles_no_search_results():
    q = 'aquerythatdoesntgetrezultssss'
    result = serp_youtube(q=q, key=youtube_key,
                          relevanceLanguage='ar')
    assert len(result) == 1
    assert result['searchTerms'].values[0] == q


def test_correctly_changing_log_levels():
    lvl_names_values = [0, 10, 20, 30, 40, 50]
    for level in lvl_names_values:
        set_logging_level(level)
        assert logging.getLogger().level == level
    with pytest.raises(ValueError):
        set_logging_level('WRONG VALUE')
