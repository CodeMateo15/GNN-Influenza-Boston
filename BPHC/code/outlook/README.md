# outlook/ (generated)

The Boston Flu Outlook site's layout, charts and offline exporter, copied from the
`boston-flu-outlook` repository by its `vendor_bphc.py`. `../make_site.py` uses them
to write the whole site as one HTML file; you don't run anything in here directly.

- `boston/geo.json`, `boston/edges.csv`: neighborhood boundaries (City of Boston
  official neighborhoods, grouped into BPHC's 14 areas) and which areas border each
  other. They don't change from week to week.
- Everything else is a copy: edit it upstream, not here.
