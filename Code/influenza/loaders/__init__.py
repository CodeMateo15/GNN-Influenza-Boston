"""Per-city data loaders.

Every city exposes the same function names -- `load_rates`, `load_weather`,
`load_static_demographics` and so on -- so `samples.load_dataset` can stay
demand-driven and city-agnostic. The Boston loaders are the originals, kept
byte-identical when they moved here; the Columbus loaders reproduce the same
contracts from a very different set of source files.
"""
