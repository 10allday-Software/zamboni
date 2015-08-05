import datetime

import elasticsearch_dsl.filter as es_filter
from elasticsearch_dsl import aggs, query, SF
from rest_framework.filters import BaseFilterBackend

from mkt.games.constants import GAME_CATEGORIES


class DailyGamesFilter(BaseFilterBackend):
    """
    Randomly chooses 4 games, one from each featured game category, based off
    of the current date such that the games are shuffled daily.

    The query:
        - Selects only games that match the featured game category tags.
        - Scores randomly using random_score using date as seed.
        - Buckets by tag, using Top Hits with size=1 to select only one game
          from each category.
        - elastic.co/guide/en/elasticsearch/guide/current/top-hits.html
    """
    def filter_queryset(self, request, queryset, view):
        daily_seed = int(datetime.datetime.now().strftime('%Y%m%d'))

        # Map over the game categories to create a function score query for one
        # and dump it into a Bool should.
        game_query = query.Q(
            'function_score',
            filter=es_filter.Bool(should=[es_filter.Term(tags=cat)
                                          for cat in GAME_CATEGORIES]),
            # Consistently random based on the day.
            functions=[SF('random_score', seed=daily_seed)],
        )

        # Run a size=1 TopHits aggregation to only select one game from each
        # tag. Results will have to be pulled out of S.execute().aggregations
        # rather than S.execute().hits.
        top_hits = aggs.TopHits(size=1)
        a = aggs.A('terms', field='tags', size=4,
                   aggs={'first_game': top_hits})

        queryset = queryset.query(game_query)[0:4]
        queryset.aggs.bucket('top_hits', a)  # Not chainable.
        return queryset
