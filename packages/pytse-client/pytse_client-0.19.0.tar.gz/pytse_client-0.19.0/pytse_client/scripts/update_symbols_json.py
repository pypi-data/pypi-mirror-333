import asyncio
import json
import locale
from pathlib import Path
from typing import List

from pytse_client import config
from pytse_client.scraper.symbol_scraper import (
    MarketSymbol,
    add_old_indexes_to_market_symbols,
    get_market_symbols_from_market_watch_page,
    get_market_symbols_from_symbols_list_page,
)

locale.setlocale(locale.LC_COLLATE, "fa_IR.UTF-8")


def write_symbols_to_json(
    market_symbols: List[MarketSymbol], filename: str, path: str
) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(f"{path}/{filename}", "w", encoding="utf8") as file:
        data = {
            obj.symbol: {
                "index": obj.index,
                "code": obj.code,
                "name": obj.name,
                "old": obj.old,
            }
            for obj in market_symbols
        }
        json.dump(data, file, ensure_ascii=False, indent=2)


async def main():
    # the sum order is important
    # https://github.com/Glyphack/pytse-client/issues/123
    market_symbols = (
        get_market_symbols_from_market_watch_page()
        + get_market_symbols_from_symbols_list_page()
    )
    print("finished fetching symbols")
    print(f"Total symbols: {len(market_symbols)}")
    deduplicated_market_symbols = list(set(market_symbols))
    print(f"Total deduplicated symbols: {len(deduplicated_market_symbols)}")
    # fetch old indexes of symbols
    deduplicated_market_symbols = await add_old_indexes_to_market_symbols(
        deduplicated_market_symbols
    )
    print("finished fetching old indexes")
    # sort by sybmol
    sorted_market_symbols = sorted(deduplicated_market_symbols)
    write_symbols_to_json(
        sorted_market_symbols, "symbols_name.json", f"{config.pytse_dir}/data"
    )


if __name__ == "__main__":
    asyncio.run(main())
