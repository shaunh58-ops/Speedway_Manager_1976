"""
Speedway Game Engine

News Manager Module

Version: 1.0

Creates news stories from game events.

Features
--------
- Breaking news
- Match reports
- Transfer news
- Injury reports
- Retirement articles
- Championship summaries
- Searchable archive

"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class NewsCategory(str, Enum):

    MATCH = "Match"

    TRANSFER = "Transfer"

    INJURY = "Injury"

    RETIREMENT = "Retirement"

    CHAMPIONSHIP = "Championship"

    CLUB = "Club"

    AWARD = "Award"

    GENERAL = "General"


@dataclass(slots=True)
class NewsArticle:

    id: int

    season: int

    week: int

    category: NewsCategory

    headline: str

    body: str

    created: datetime = field(default_factory=datetime.utcnow)


class NewsManager:

    """
    Stores and generates in-game news.
    """

    def __init__(self):

        self._next_id = 1

        self.archive: List[NewsArticle] = []

    # ======================================================
    # INTERNAL
    # ======================================================

    def _publish(
        self,
        season: int,
        week: int,
        category: NewsCategory,
        headline: str,
        body: str
    ) -> NewsArticle:

        article = NewsArticle(

            id=self._next_id,

            season=season,

            week=week,

            category=category,

            headline=headline.strip(),

            body=body.strip()

        )

        self.archive.append(article)

        self._next_id += 1

        return article

    # ======================================================
    # MATCH REPORTS
    # ======================================================

    def publish_match_report(
        self,
        season: int,
        week: int,
        home_team: str,
        away_team: str,
        home_score: int,
        away_score: int
    ) -> NewsArticle:

        headline = (
            f"{home_team} {home_score} - "
            f"{away_score} {away_team}"
        )

        if home_score > away_score:

            result = f"{home_team} secured an important home victory."

        elif away_score > home_score:

            result = f"{away_team} produced an excellent away performance."

        else:

            result = "Neither side could be separated."

        body = (
            f"{result}\n\n"
            f"Final Score: "
            f"{home_team} {home_score} "
            f"{away_score} {away_team}."
        )

        return self._publish(

            season,

            week,

            NewsCategory.MATCH,

            headline,

            body

        )

    # ======================================================
    # TRANSFERS
    # ======================================================

    def publish_transfer(
        self,
        season: int,
        week: int,
        rider_name: str,
        old_club: str,
        new_club: str
    ) -> NewsArticle:

        headline = f"{rider_name} joins {new_club}"

        body = (
            f"{new_club} have completed the signing of "
            f"{rider_name} from {old_club}."
        )

        return self._publish(

            season,

            week,

            NewsCategory.TRANSFER,

            headline,

            body

        )

    # ======================================================
    # INJURIES
    # ======================================================

    def publish_injury(
        self,
        season: int,
        week: int,
        rider_name: str,
        severity: str,
        weeks: int
    ) -> NewsArticle:

        headline = f"{rider_name} suffers injury"

        body = (
            f"{rider_name} has suffered a "
            f"{severity.lower()} injury and "
            f"is expected to miss approximately "
            f"{weeks} week(s)."
        )

        return self._publish(

            season,

            week,

            NewsCategory.INJURY,

            headline,

            body

        )

    # ======================================================
    # RETIREMENT
    # ======================================================

    def publish_retirement(
        self,
        season: int,
        week: int,
        rider_name: str,
        age: int
    ) -> NewsArticle:

        headline = f"{rider_name} announces retirement"

        body = (
            f"After a distinguished Speedway career "
            f"{rider_name} has retired at the age of "
            f"{age}."
        )

        return self._publish(

            season,

            week,

            NewsCategory.RETIREMENT,

            headline,

            body

        )

    # ======================================================
    # CHAMPIONSHIP
    # ======================================================

    def publish_champions(
        self,
        season: int,
        champion: str
    ) -> NewsArticle:

        headline = f"{champion} crowned champions"

        body = (
            f"{champion} have secured the league title "
            f"after an outstanding season."
        )

        return self._publish(

            season,

            0,

            NewsCategory.CHAMPIONSHIP,

            headline,

            body

        )

    # ======================================================
    # SEARCH
    # ======================================================

    def by_category(
        self,
        category: NewsCategory
    ) -> List[NewsArticle]:

        return [

            article

            for article

            in self.archive

            if article.category == category

        ]

    def season_archive(
        self,
        season: int
    ) -> List[NewsArticle]:

        return [

            article

            for article

            in self.archive

            if article.season == season

        ]

    def latest(
        self,
        limit: int = 10
    ) -> List[NewsArticle]:

        return self.archive[-limit:]

    # ======================================================
    # SUMMARY
    # ======================================================

    def summary(self) -> Dict[str, int]:

        counts: Dict[str, int] = {}

        for article in self.archive:

            key = article.category.value

            counts[key] = counts.get(key, 0) + 1

        return counts


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    news = NewsManager()

    news.publish_transfer(

        1976,

        3,

        "Peter Collins",

        "Belle Vue",

        "Ipswich"

    )

    for article in news.latest():

        print(article.headline)
