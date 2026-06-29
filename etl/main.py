from constants import Franchise
import argparse
import sys
import etl as etl

def parse_franchise(name: str) -> Franchise:
    """
    Parse a franchise short code string to a Franchise enum member.

    Args:
        name: Franchise short code (e.g. 'US', 'UK'). Case-insensitive.

    Returns:
        Matching Franchise enum member.

    Raises:
        ValueError: If no franchise matches the given short code.
    """

    name = name.upper()
    for franchise in Franchise:
        if franchise.name == name:
            return franchise
    raise ValueError(f"No franchise found for : '{name}'")


def main():
    parser = argparse.ArgumentParser(description="Collect lip sync data from Drag Race wiki")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--all", help="Collect all uncollected seasons that have not been collected yet", action="store_true")
    group.add_argument("-f", "--franchise", type=str, help="Franchise short code (e.g. US, UK)")
    group.add_argument("-l", "--list-franchises", action="store_true", help="List all franchises")

    parser.add_argument("-s", "--season", type=int, help="Season number (optional, requires --franchise)")

    args = parser.parse_args()

    # Validate input

    if args.season is not None and args.all:
        parser.error("--season cannot be used with --all")

    if args.season is not None and not args.franchise:
        parser.error ("--season requires --franchise to be specified")
    
    # Input is valid, dispatch to the correct handler
    if args.list_franchises:
        list_franchises()
    elif args.all:
        collect_all()

    # --season cannot be used without --franchise
    elif args.season and not args.franchise:
        parser.error("--season requires --franchise to be specified")
    elif args.franchise:
        try:
            franchise = parse_franchise(args.franchise)
        except ValueError as e:
            parser.error(str(e))  # prints clean error and exits
        collect_franchise(franchise, season_number=args.season)
    else:
        parser.print_help()
        sys.exit(0)


def list_franchises():
    """Print all supported franchise codes and titles"""
    #print("Code","\t|\t", "Franchise Title")
    print(f"{'Code':<8} Title")
    print("-"*40)
    for f in Franchise:
        #print(f.name,"\t|\t", f.title)
        print(f"{f.name:<8} {f.title}")

def collect_all():
    """Collect all uncollected seasons across every franchise."""
    print("Collecting all seasons...")
    for franchise in Franchise:
        collect_franchise(franchise)

def collect_franchise(franchise: Franchise, season_number: int = None):
    """
    Collect one specific season or all seasons of a franchise.
    Args:
        franchise: The franchise enum memeber to collect.
        season_number: Specific season number, or NONE to collect all seasons
    """

    if season_number is None:
        print(f"Collecting all {franchise.number_of_season} seasons of {franchise.title}...")
        seasons = range(1,franchise.number_of_season+1)
    else:
        print(f"Collecting season {season_number} of {franchise.title}...")
        seasons = [season_number]

    for s in seasons:

        print(f"Processing season {s}")
        etl.run_etl(franchise,s)

# Extract : Initial run for collecting data from previously aired season for all franchise
# In the future, a run can be done during or after a season of a franchise has finished airing.



if __name__ == "__main__":
    main()

