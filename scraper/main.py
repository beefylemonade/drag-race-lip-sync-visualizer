import collection
import constants
from constants import Franchise
import argparse
import sys

def parse_franchise(name: str) -> Franchise:
    name = name.upper()
    for franchise in Franchise:
        if franchise.name == name:
            return franchise
    raise ValueError(f"No franchise found for : '{name}'")

franchise_to_be_scraped = []


parser = argparse.ArgumentParser(description="Collect data from wiki page of one or all franchises of Drag Race")
group = parser.add_mutually_exclusive_group()
group.add_argument("-a", "--all", help="Collect all seasons that have not been collected yet", action="store_true")
group.add_argument("-f", "--franchise", type=str, help="Franchise code (e.g. US, UK)")
group.add_argument("-l", "--list-franchises", action="store_true", help="List all franchises")

parser.add_argument("-s", "--season", type=int, help="Season number (optional, requires --franchise)")

args = parser.parse_args()

if args.list_franchises:
    print("Code","\t|\t", "Franchise Title")
    print("--------------------------------------")
    for f in Franchise:
        print(f.abbr,"\t|\t", f.title)
elif args.all:
    print("Collecting all seasons")
    for f in Franchise:
        franchise_to_be_scraped.append(f)

# --season cannot be used without --franchise
elif args.season and not args.franchise:
    parser.error("--season requires --franchise to be specified")
elif args.season and args.franchise:
    print(f"Collecting season {args.season} of ", args.franchise)
elif args.franchise:
    try:
        franchise = parse_franchise(args.franchise)
    except ValueError as e:
        parser.error(str(e))  # prints clean error and exits
    print("Collecting all seasons of ", franchise.title)
    franchise_to_be_scraped.append(franchise)
else:
    parser.print_help()
    sys.exit(0)


# Extract : Initial run for collecting data from previously aired season for all franchise
# In the future, a run can be done during or after a season of a franchise has finished airing.
for f in franchise_to_be_scraped:
    print("Processing", f.title)


# Transform

# Load


