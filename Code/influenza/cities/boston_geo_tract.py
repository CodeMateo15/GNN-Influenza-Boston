"""Boston with edges derived from Census-tract neighborhood polygons; see _boston_derived."""

from ._boston_derived import derived_boston

BOSTON_GEO_TRACT = derived_boston("tract")
