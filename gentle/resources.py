"""Code was @generated by the upstream lowerquality/gentle project."""
import os

from . import metasentence
from .util.paths import ENV_VAR, get_resource


class Resources:
    def __init__(self):
        self.proto_langdir = get_resource("exp")
        self.nnet_gpu_path = get_resource("exp/tdnn_7b_chain_online/")

        # seems like the hclg is not built during install, so this is always None
        self.full_hclg_path = None

        def require_dir(path):
            if not os.path.isdir(path):
                raise RuntimeError(
                    "No resource directory %s.  Check %s environment variable?" % (path, ENV_VAR)
                )

        require_dir(self.proto_langdir)
        require_dir(self.nnet_gpu_path)

        with open(os.path.join(self.proto_langdir, "langdir", "words.txt")) as fh:
            self.vocab = metasentence.load_vocabulary(fh)
