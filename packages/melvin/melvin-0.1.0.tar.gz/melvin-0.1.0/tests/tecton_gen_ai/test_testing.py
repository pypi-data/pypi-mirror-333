from src.tecton_gen_ai.testing import make_local_realtime_feature_view
import pandas as pd
import pytest


def test_mock_rtfv(tecton_unit_test):
    fv = make_local_realtime_feature_view(
        "fv", {"user_id": "user1", "age": 30}, ["user_id"]
    )

    events = pd.DataFrame([{"user_id": "user1"}])

    odf = fv.get_features_for_events(events).to_pandas()
    assert odf["fv__age"].iloc[0] == 30

    events = pd.DataFrame([{"user_id": "user2"}])

    with pytest.raises(Exception):
        odf = fv.get_features_for_events(events).to_pandas()
