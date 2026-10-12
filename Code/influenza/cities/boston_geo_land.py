"""Boston with edges derived from official (land) neighborhood polygons; see _boston_derived."""

from ._boston_derived import derived_boston

BOSTON_GEO_LAND = derived_boston("land")
