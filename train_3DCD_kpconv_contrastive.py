import hydra
from hydra.core.global_hydra import GlobalHydra
from omegaconf import OmegaConf
from torch_points3d.trainer_3DCD_kpconv_contrastive import Trainer


# @hydra.main(config_path="conf/configUrb3D.yaml")
@hydra.main(config_path="conf", config_name="config3DCD_self_sup")
def main(cfg):
    OmegaConf.set_struct(cfg, False)  # This allows getattr and hasattr methods to function correctly
    if cfg.pretty_print:
        print(cfg.pretty())
    trainer = Trainer(cfg)
    trainer.train()
    # trainer.eval()
    # https://github.com/facebookresearch/hydra/issues/440
    GlobalHydra.get_state().clear()
    return 0


if __name__ == "__main__":
    main()
