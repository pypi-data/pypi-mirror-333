"""
Utilities to load configuration of experiments
"""

import shutil
from pathlib import Path
from typing import List, Optional, Union

import yaml
from omegaconf import DictConfig, OmegaConf
from pipe import map

from .resolvers import extra_resolvers as _extra_resolvers


def load_config(
    conf_dir: Union[str, Path],
    from_cli: Optional[List[str]] = None,
    dump_conf: Optional[Union[str, Path]] = None,
    extra_resolvers: bool = True,
) -> DictConfig:
    """
    Takes the path of a config.yaml file and loads the configuration, moreover it
    resolve all the configurations under extend_config to other files and merge the
    whole configuration. It's also possible to override any config through cli args
    """
    # register solvers
    if extra_resolvers:
        for name, fn in _extra_resolvers().items():
            try:
                OmegaConf.register_new_resolver(name, fn)
            except ValueError:
                pass  # already registered

    # resolve base configuration
    conf_path = Path(conf_dir) / "config.yaml"
    base_conf = OmegaConf.load(conf_path)

    # load cli configuration, substitute extended configs
    # if required and then merge those extensions
    cli_conf = dict(
        (from_cli if from_cli else [])
        | map(lambda x: x.split("="))
        | map(lambda x: (x[0].strip(), _parse(x[1].strip())))
    )

    # merge all the configurations together, in order we fuse
    # 1. the $override_from listed files
    # 2. the $extend_config listed files
    # 3. the $override_config listed files
    for override_dir in base_conf.pop("$override_from", []):
        for sub_conf_path in sorted(
            Path(conf_path.parent / override_dir).glob("*.yaml"),
            key=lambda x: x.stem,
        ):
            sub_conf_data = OmegaConf.load(sub_conf_path)
            base_conf = OmegaConf.merge(base_conf, sub_conf_data)

    other_confs = base_conf.get("$extend_config", OmegaConf.create())
    for sub_conf in other_confs.keys():
        if sub_conf in cli_conf:
            other_confs[sub_conf] = cli_conf.pop(sub_conf)
    for dirname in other_confs.keys():
        conf_name = base_conf["$extend_config"][dirname]
        sub_conf_path = conf_path.parent / dirname / (conf_name + ".yaml")
        sub_conf_data = OmegaConf.load(sub_conf_path)
        override_config = sub_conf_data.pop("$override_config", OmegaConf.create())
        base_conf = OmegaConf.merge(
            base_conf, {dirname: sub_conf_data}, override_config
        )
    base_conf.pop("$extend_config", OmegaConf.create())
    for key, value in cli_conf.items():
        OmegaConf.update(base_conf, key, value)

    # dump modified files in the provided path, this can be logged and contains
    # all the config plus the modified part, unluckily without the usage of external
    # dependencies it does not maintain comments so far
    if dump_conf is not None:

        def repr_str(dumper, data):
            if "\n" in data:
                return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
            return dumper.org_represent_str(data)

        _DumpWithLineBreak.org_represent_str = _DumpWithLineBreak.represent_str
        yaml.add_representer(str, repr_str, Dumper=_DumpWithLineBreak)

        dump_conf = Path(dump_conf)
        shutil.copytree(conf_dir, dump_conf)
        cfg_all = OmegaConf.to_container(base_conf)
        # sub_confs = [(k, v, cfg_all.pop(k)) for k, v in other_confs.items()]
        # cfg_all["$extend_config"] = OmegaConf.to_container(other_confs)
        _dump_cfg(dump_conf / "config.yaml", cfg_all)
        # for dirname, fname, content in sub_confs:
        #     _dump_cfg(dump_conf / dirname / (fname + ".yaml"), content)

    # return final configuration
    return base_conf


# yaml utilities


def _dump_cfg(path, cfg):
    with open(path, "wt") as f:
        f.write(
            yaml.dump(
                cfg,
                default_flow_style=False,
                sort_keys=False,
                Dumper=_DumpWithLineBreak,
            )
        )


class _DumpWithLineBreak(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


# type cast utility


def _parse_bool(v: str):
    if v.lower() == "true":
        return True
    elif v.lower() == "false":
        return False
    else:
        raise ValueError(f"{v} not a bool")


def _parse_float_int(v: str):
    if "." in v:
        return float(v)
    else:
        return int(v)


def _parse_omega(v: str):
    if v.startswith(("[", "{")):
        return OmegaConf.to_container(OmegaConf.create(v))
    else:
        raise ValueError(f"{v} not a container")


def _parse(v: str):
    for parser in [_parse_bool, _parse_float_int, _parse_omega]:
        try:
            return parser(v)
        except ValueError:
            pass
    return v
