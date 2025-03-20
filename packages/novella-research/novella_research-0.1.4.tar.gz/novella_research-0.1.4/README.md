# novella_research

This package contains all my custom Tensorflow work.

## Installation

You can install the package via pip:

```bash
pip install novella_research
```

## Usage

activations.flux

```python
from novella_research.activations import flux
import tensorflow as tf

...
tf.keras.layers.Dense(64, activation=flux('relu'))
```

## License

This package is licensed under the MIT License.
