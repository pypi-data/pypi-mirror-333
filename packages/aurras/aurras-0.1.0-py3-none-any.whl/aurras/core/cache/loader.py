"""
Cache Loading Module

This module provides a class for loading data from the cache database.
"""

import sqlite3
from config.path import cache
from aurras.core.cache.initialize import InitializeSearchHistoryDatabase


class LoadSongHistoryData:
    """
    Class for loading song history data from the cache database.
    """

    def __init__(self) -> None:
        """Initialize the cache if needed."""
        InitializeSearchHistoryDatabase().initialize_cache()

    def load_song_metadata_from_db(self):
        """
        Loads song metadata from the cache database.

        Returns:
            list: A list of tuples containing the song metadata.
        """
        with sqlite3.connect(cache) as cache_db:
            cursor = cache_db.cursor()
            cursor.execute(
                "SELECT song_user_searched, song_name_searched, song_url_searched FROM cache"
            )
            return cursor.fetchall()
