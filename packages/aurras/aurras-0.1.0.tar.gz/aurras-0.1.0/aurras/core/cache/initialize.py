"""
Cache Initialization Module

This module provides a class for initializing the search history database.
"""

import sqlite3
from config.path import cache


class InitializeSearchHistoryDatabase:
    """
    Class for initializing the search history database.
    """

    def initialize_cache(self):
        """
        Initializes the cache database with the required tables.
        """
        with sqlite3.connect(cache) as db:
            cursor = db.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS cache (
                    id INTEGER PRIMARY KEY,
                    song_user_searched TEXT,
                    song_name_searched TEXT,
                    song_url_searched TEXT
                )"""
            )
