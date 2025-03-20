# gdpnum

[![CI](https://github.com/Felipe-Gomez/gdp-numeric/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Felipe-Gomez/gdp-numeric/actions/workflows/ci.yml)

Repository for numerically computing the privacy parameter in Gaussian Differential Privacy.

## Quickstart

You can install the library with pip:
```
pip install gdpnum
```


### DP-SGD
To analyze DP-SGD, we have:

```python
import gdpnum

mu, regret = gdpnum.dpsgd.get_mu_and_regret_for_dpsgd(
    noise_multiplier=9.4,
    sample_rate=0.328,
    num_steps=2000
)
# (1.5685621993129137, 0.0010208130697719753)
```

We get the numerically computed GDP mu parameter, and regret which
shows the goodness-of-fit of the GDP.

The library also includes an [Opacus-compatible](https://opacus.ai/api/accounting/iaccountant.html) accountant interface:
```
import gdpnum

acct = gdpnum.dpsgd.CTDAccountant()
acct.step(noise_multiplier=9.4, sample_rate=0.328)
acct.get_mu_and_regret()
```

### General mechanisms
For general mechanisms, the library relies on the privacy loss distribution
objects from the `dp_accounting` package:

```python
import gdpnum

pld = ...

converter = gdpnum.PLDConverter(pld)
mu, regret = converter.get_mu_and_regret()
```

See an example for the US Census TopDown mechanism in the notebooks folder.
