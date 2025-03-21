# [1.7.7](https://github.com/thesadru/genshin.py/compare/v1.7.6..v1.7.7) - 2025-03-12

## Bug Fixes

- Remove pydantic.computed_field decorator - ([57f4f7c](https://github.com/thesadru/genshin.py/commit/57f4f7c08c4f9de3cea35e1ecf22ddc6b44883e9))
- Update field validator to handle None values and improve servant detail access - ([b38bdd4](https://github.com/thesadru/genshin.py/commit/b38bdd4e15a2fd18adf9227a41994f14e0c23666))
- Correct timezone assignment in add_timezone function - ([d8cfbe7](https://github.com/thesadru/genshin.py/commit/d8cfbe77e55f1e85f7d2d8674db158bb3e7cdce3))

## Documentation

- Update authkey section - ([53b4205](https://github.com/thesadru/genshin.py/commit/53b420562c5c6e1754943018a9420ff0e55e49f7))

## Features

- **(errors)** Add error message for max usage limit on redemption codes - ([9636fb5](https://github.com/thesadru/genshin.py/commit/9636fb5448260734cda189f44b6026b2a7328e05))
- Add is_wearing_outfit property to StarRailDetailCharacter - ([c00a0d4](https://github.com/thesadru/genshin.py/commit/c00a0d47613f557681b86ac33891ced51ef79199))
- Support memosprite - ([6f83be5](https://github.com/thesadru/genshin.py/commit/6f83be57932898ddabede4a876953d0baed6f42a))

## Improvements

- Use cookie manager's session instead of creating a new one - ([b8ada9c](https://github.com/thesadru/genshin.py/commit/b8ada9cd1585368955f760a501e6e2ffb1f429bb))
- Handle ProxyError in retry deco - ([67c32ae](https://github.com/thesadru/genshin.py/commit/67c32aecadd6a20004d9cd5824e4a2ff93eb78f0))

## Miscellaneous Chores

- **(deps)** Update lock file - ([2c4e4ad](https://github.com/thesadru/genshin.py/commit/2c4e4ad1a54ba3b37b04b9580c4212da3bffd593))
- **(deps)** update paambaati/codeclimate-action action to v3.2.0 - ([28d1bff](https://github.com/thesadru/genshin.py/commit/28d1bff5638f95c8a3e934d4960dff233e63200c))
- **(deps)** Update paambaati/codeclimate-action action to v9 ([#240](https://github.com/thesadru/genshin.py/issues/240)) - ([ac8e7da](https://github.com/thesadru/genshin.py/commit/ac8e7daa0cda0a2263b84fcee75951ad17b615ad))
- **(deps)** Update astral-sh/setup-uv action to v5 ([#239](https://github.com/thesadru/genshin.py/issues/239)) - ([bd43210](https://github.com/thesadru/genshin.py/commit/bd4321018187b5cd3138891b21199a415d8dcd4b))
- **(deps)** Update actions/setup-python action to v5 ([#238](https://github.com/thesadru/genshin.py/issues/238)) - ([58a8194](https://github.com/thesadru/genshin.py/commit/58a81946980581c85956a013348615a527d3ee30))
- **(deps)** Update actions/download-artifact action to v4 ([#237](https://github.com/thesadru/genshin.py/issues/237)) - ([5756349](https://github.com/thesadru/genshin.py/commit/575634905996660a4cbde646fae058dead7d53c7))
- **(deps)** lock file maintenance ([#241](https://github.com/thesadru/genshin.py/issues/241)) - ([b9531e1](https://github.com/thesadru/genshin.py/commit/b9531e1ab5f1c9310962273b93b812b1ee3d9897))
- **(deps)** lock file maintenance ([#242](https://github.com/thesadru/genshin.py/issues/242)) - ([546068b](https://github.com/thesadru/genshin.py/commit/546068bdcf21c03d657c392f41a0f06ab86a9e3e))
- **(deps)** update dependency python to 3.13 - ([273659f](https://github.com/thesadru/genshin.py/commit/273659f331fdbec26e6384e05d694c44eced8a41))
- **(ruff)** Ignore A005 - ([fc60490](https://github.com/thesadru/genshin.py/commit/fc604903b88c193be863397847cebd03ea7a0b72))

