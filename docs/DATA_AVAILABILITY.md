# Data availability and privacy

## Recommended manuscript statement

> The individual-level dataset used in this case study is not publicly available because it contains sensitive personal data concerning participation and roles in a religious organization, together with residential geolocation information. Public disclosure could create a material risk of re-identification. The repository therefore provides the full analysis code, a synthetic dataset with the same computational schema, and aggregate results sufficient to inspect the analytical workflow. Any future restricted access to the confidential data would be subject to applicable ethical, institutional, and legal requirements.

## Public-release rules

Do not upload:

1. names or aliases of participants;
2. street addresses or neighborhood-level address strings;
3. exact residential latitude/longitude;
4. interactive Folium/Leaflet HTML maps created from confidential coordinates;
5. screenshots that show street geometry around participant homes;
6. lookup tables that map public IDs back to names;
7. Git history containing files that were later deleted but had identifying information.

## Safer publication choices

- Use synthetic coordinates in the public repository.
- In the article, replace coordinate tables with a data dictionary or non-geographic normalized coordinates.
- For figures, use privacy-preserving schematic/normalized plots rather than a recognizable street basemap.
- If exact replication is required by a journal, use a restricted-access research-data repository or controlled data-use process rather than public GitHub.
