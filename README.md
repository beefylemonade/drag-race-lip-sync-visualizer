# drag-race-lip-sync-visualizer
A data visualization of Rupaul's Drag Race's lip sync across all seasons and franchises.

## Scraper Usage
- python report-generator.py --all
- python report-generator.py --franchise US
- python report-generator.py --franchise US --season 19

## Arguments

| Argument        | Description                                    |
|-----------------|------------------------------------------------|
| -a, --all       | Collect all franchises and seasons             |
| -f, --franchise | Franchise code (e.g. US, UK)                   |
| -s, --season    | Season number (optional, requires --franchise) |

## Franchises

| Code         | Franchise Title             |
|--------------|-----------------------------|
| US           | RuPaul's Drag Race          |
| UK           | Rupaul's Drag Race UK       |
| ...          | ...                         |
