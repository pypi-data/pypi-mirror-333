# =============================================================================
# Minet Telegram Channel-Infos CLI Action
# =============================================================================
#
# Action retrieving the information of a Telegram channel.
#
from minet.cli.utils import with_enricher_and_loading_bar
from minet.telegram import TelegramScraper
from minet.telegram.types import TelegramChannelInfos
from minet.telegram.exceptions import TelegramInvalidTargetError


@with_enricher_and_loading_bar(
    headers=TelegramChannelInfos, title="Retrieving info", unit="channels"
)
def action(cli_args, enricher, loading_bar):
    scraper = TelegramScraper(throttle=cli_args.throttle)

    for i, row, channel in enricher.enumerate_cells(
        cli_args.column, with_rows=True, start=1
    ):
        with loading_bar.step():
            try:
                infos = scraper.channel_infos(channel)
                enricher.writerow(row, infos)
            except TelegramInvalidTargetError:
                loading_bar.print(
                    "%s (line %i) is not a telegram channel or url, or is not accessible."
                    % (channel, i)
                )
