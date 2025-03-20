# flake8: noqa
from .mocks import (
    make_local_batch_feature_view,
    make_local_realtime_feature_view,
    make_local_source,
    make_local_stream_feature_view,
)
from .utils import make_local_vector_db_config, print_md, set_dev_mode

try:
    from .examples.copilot import assist
except ImportError:
    pass
