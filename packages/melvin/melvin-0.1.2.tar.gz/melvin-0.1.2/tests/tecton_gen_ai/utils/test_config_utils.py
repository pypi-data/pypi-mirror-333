from melvin.tecton_gen_ai.api import Configs


def test_configs():
    with Configs(
        llm="gpt",
        fv_base_config={"x": 1},
        bfv_config={"y": 2},
        rtfv_config={"z": 3},
        sfv_config={"a": 4},
        feature_service_config={"b": 5},
    ).update_default():
        conf = Configs.get_default()
        assert conf.llm == "gpt"
        assert conf.get_bfv_config() == {"x": 1, "y": 2}
        assert conf.get_rtfv_config() == {"x": 1, "z": 3}
        assert conf.get_sfv_config() == {"x": 1, "a": 4}
        assert conf.feature_service_config == {"b": 5}

        with Configs(
            fv_base_config={"x": 2},
            bfv_config={"y": 3},
            feature_service_config={"b": 6},
        ).update_default():
            conf = Configs.get_default()
            assert conf.llm == "gpt"
            assert conf.get_bfv_config() == {"x": 2, "y": 3}
            assert conf.get_rtfv_config() == {"x": 2, "z": 3}
            assert conf.get_sfv_config() == {"x": 2, "a": 4}
            assert conf.feature_service_config == {"b": 6}

        conf = Configs.get_default()
        assert conf.llm == "gpt"
        assert conf.get_bfv_config() == {"x": 1, "y": 2}
        assert conf.get_rtfv_config() == {"x": 1, "z": 3}
        assert conf.get_sfv_config() == {"x": 1, "a": 4}
        assert conf.feature_service_config == {"b": 5}
