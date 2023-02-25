from enum import Enum
import os
import sys
from omegaconf import DictConfig, OmegaConf
import logging

from torch_points3d.utils.model_building_utils.model_definition_resolver import resolve

log = logging.getLogger(__name__)

CUR_FILE = os.path.realpath(__file__)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class ModelArchitectures(Enum):
    UNET = "unet"
    ENCODER = "encoder"
    DECODER = "decoder"


class ModelFactory:
    MODEL_ARCHITECTURES = [e.value for e in ModelArchitectures]

    @staticmethod
    def raise_enum_error(arg_name, arg_value, options):
        raise Exception("The provided argument {} with value {} isn't within {}".format(arg_name, arg_value, options))

    def __init__(
        self,
        architecture: str = None,
        input_nc: int = None,
        num_layers: int = None,
        config: DictConfig = None,
        **kwargs
    ):
        if not architecture:
            raise ValueError()
        self._architecture = architecture.lower()
        assert self._architecture in self.MODEL_ARCHITECTURES, ModelFactory.raise_enum_error(
            "model_architecture", self._architecture, self.MODEL_ARCHITECTURES
        )

        self._input_nc = input_nc
        self._num_layers = num_layers
        self._config = config
        self._kwargs = kwargs

        if self._config:
            log.info("The config will be used to build the model")

    @property
    def modules_lib(self):
        raise NotImplementedError

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def num_layers(self):
        return self._num_layers

    @property
    def num_features(self):
        return self._input_nc

    def _build_unet(self):
        raise NotImplementedError

    def _build_unet_base(self, unet_class, config_dir, module_name, config_file=None):
        PATH_TO_CONFIG = os.path.join(DIR_PATH, config_dir)
        if self._config:
            model_config = self._config
        else:
            if config_file is None:
                config_file = "unet_{}.yaml".format(self.num_layers)
            path_to_model = os.path.join(PATH_TO_CONFIG, config_file)
            model_config = OmegaConf.load(path_to_model)
        ModelFactory.resolve_model(model_config, self.num_features, self._kwargs)
        modules_lib = sys.modules[module_name]
        return unet_class(model_config, None, None, modules_lib, **self.kwargs)

    def _build_encoder(self):
        raise NotImplementedError

    def _build_encoder_base(self, encoder_class, config_dir, module_name, config_file=None):
        PATH_TO_CONFIG = os.path.join(DIR_PATH, config_dir)
        if self._config:
            model_config = self._config
        else:
            if config_file is None:
                config_file = "encoder_{}.yaml".format(self.num_layers)
            path_to_model = os.path.join(PATH_TO_CONFIG, config_file)
            model_config = OmegaConf.load(path_to_model)
        ModelFactory.resolve_model(model_config, self.num_features, self._kwargs)
        modules_lib = sys.modules[module_name]
        return encoder_class(model_config, None, None, modules_lib, **self.kwargs)

    def _build_decoder(self):
        raise NotImplementedError

    def build(self):
        if self._architecture == ModelArchitectures.UNET.value:
            return self._build_unet()
        elif self._architecture == ModelArchitectures.ENCODER.value:
            return self._build_encoder()
        elif self._architecture == ModelArchitectures.DECODER.value:
            return self._build_decoder()
        else:
            raise NotImplementedError

    @staticmethod
    def resolve_model(model_config, num_features, kwargs):
        """Parses the model config and evaluates any expression that may contain constants
        Overrides any argument in the `define_constants` with keywords wrgument to the constructor
        """
        # placeholders to subsitute
        constants = {
            "FEAT": max(num_features, 0),
        }

        # user defined contants to subsitute
        if "define_constants" in model_config.keys():
            constants.update(dict(model_config.define_constants))
            define_constants = model_config.define_constants
            for key in define_constants.keys():
                value = kwargs.get(key)
                if value:
                    constants[key] = value
        resolve(model_config, constants)
