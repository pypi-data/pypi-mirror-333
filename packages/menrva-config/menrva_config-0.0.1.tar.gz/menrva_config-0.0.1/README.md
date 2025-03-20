# Menrva

Menrva is a small yet effective library to manage everything you need about configuration! It enables
<u>modular, composable and scriptable yaml configuration files</u>. This allows to move the complexity of
configuration management directly in the configuration itself and narrows the code logic that deals with it,
leading to readable configuration and code.

## Basic Usage

The most simple way to use Menrva is to load configuration from a .yaml file. Configuration is a folder containing
a config file in yaml

```yaml
# config/ folder contaning this file: config.yaml

# our configuration for a model
model:
  name: unetmodel
  args:
    in_channels: 3
    out_channels: 1
    encoder: resnet18

# the training configuration
train:
    n_epochs: 20
```

From code it can be loaded as follows

```python
>>> from menrva.config import load_config
>>> cfg = load_config("config")
>>> print(cfg.model.args)
{'in_channels': 3, 'out_channels': 1, 'encoder': 'resnet18'}
```

Configuration can be overwritten by command line passing to the `load_config` function
the updates that can be easily obtained from the command line

```python
>>> cfg = load_config(
    "config",
    from_cli=[
        "model.args.encoder=resnet34",
        "model.args.in_channels=1",
    ]
)
>>> print(cfg.model.args)
{'in_channels': 1, 'out_channels': 1, 'encoder': 'resnet34'}
```

## Variable Interpolation

Yaml configuration allows for variables interpolation: dynamic variables whose value is
evaluated when at runtime that specific parameter is retrieved. This allows to define in
the config dependencies between variables that are automatically resolved. As an example
let's say that we need to configure the preprocessing steps of a model depending from the
currently executed step

```yaml
step: train

model:
  name: unetmodel
  args:
    in_channels: 3
    out_channels: 1
    encoder: resnet18
  preprocessing: ${ _preprocess.${step} }

# the two different preprocessing steps
_preprocess:
  train:
    - resize
    - random_crop
    - noise
  test:
    - resize
```

```python
>>> cfg = load_config("config")
>>> cfg.model.preprocessing
['resize', 'random_crop', 'noise']
>>> cfg.step = "test"
>>> cfg.model.preprocessing
['resize']
```

This approach simplifies the code that uses the configuration since it does not have to
actively modify the configuration file that is always completely readable and not hidden
in the code logic. In our example it allows to seamlessly switch between train and test
configuration (note that you can set step=train or step=test from command line) In our example it allows to seamlessly switch between train and test configuration (note that you can set step=train or step=test from command line).

## Modular Configuration

However, having the configuration in an unique file is not handy. Menrva allows to split the
configuration in multiple files and to freely compose them. Suppose that we have a model, and
we support testing on different scenes of different datasets. Each dataset however has its own set of required preprocessing operations. We can divide the the configuration as follows: a
root `config.yaml` file, a folder containing specific `overrides` for each supported dataset
and a folder `scenes` containing the specific scenes we want to test.

```
config/
  config.yaml
  overrides/
    replica.yaml
    tum.yaml
  scenes/
    tum/
      xyz.yaml
    replica/
      room0.yaml
```

```yaml
#### config.yaml
model:
  name: unetmodel
  args:
    in_channels: 3
    out_channels: 1
    encoder: resnet18

dataset:
  _root: datasets

# (searches for the configuration file under <key>/<value_path>
# and adds the founc config under the scope <key>). Fields are
# evaluated in order, thus `dataset.name` must be set by the 
# chosen scene
$extend_config:
  scene: tum/xyz
  overrides: ${ dataset.name }
####

#### scene/tum/xyz.yaml

# this field will be in the cfg.scene scope
name: tum-xyz

# everything in in $override_config overrides fields starting
# from the root scope, thus cfg.dataset
$override_config:
  dataset:
    name: tum
    seq_name: xyz
####

#### overrides/tum.yaml
$override_config:
  dataset:
  basedir: ${ dataset.root }/tum
  args:
    undistort: true
```

Following the example, dividing the configuration this way allows to factorize the configuration of all the scenes of the same dataset.

```python
>>> cfg = menrva.config.load_config("config")
>>> cfg.scene.name
"tum-xyz"
>>> cfg.dataset.basedir, cfg.dataset.args.undistort
('datasets/tum', True)
```

Note that overrides are evaluated when the config is loaded, thus you can not change
`cfg.scene` to another scene directly from code. However you can do that when you
load it.

```python
>>> cfg = menrva.config.load_config("config", from_cli=["scene=replica/room0"])
>>> cfg.scene.name
"replica-room0"
>>> cfg.dataset.basedir, cfg.dataset.args.undistort
('datasets/replica', False)
```

## Save Configuration

Since the configuration can be changed at runtime or when loaded, for logging purposes Menrva allows to dump the loaded config on disk.

```python
# save the config overwritten by the cli in the new replica-config folder
# (if loaded back it will be the same config, but without variable interpolation available, use it only for logging purposes)
>>> cfg = menrva.config.load_config("config", from_cli=["scene=replica/room0"], dump_cfg="replica-config")
>>> cfg.scene.name
"replica-room0"
>>> cfg.dataset.basedir, cfg.dataset.args.undistort
('datasets/replica', False)
```