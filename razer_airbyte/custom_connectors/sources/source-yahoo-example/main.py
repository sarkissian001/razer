import sys

from airbyte_cdk.entrypoint import launch
from source_yahoo_example import SourceYahooFinancePrice

if __name__ == "__main__":
    source = SourceYahooFinancePrice()
    launch(source, sys.argv[1:])
