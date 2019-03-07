# coding=utf-8
"""Tools for analyses needed by the machine learning prediction algorithm."""
import multiprocessing
from typing import Dict, Mapping

from movie_recommender import exceptions
from movie_recommender.constants import GENRES
from movie_recommender.db import common, read
from movie_recommender.predict import ml


def analyze_users(user_ids, overwrite, jobs):
    """Analyze users, to find out which predictor works best for them.

    :param user_ids: An iterable of user IDs. The users for which analyses are
        being performed.
    :param overwrite: If a user has already been analyzed, should the analysis
        be overwritten?
    :param jobs: The number of processes to spawn. If none, spawn one per CPU.
    :returns: Nothing.
    """
    # The amount of time it takes to analyze a user depends on the number of
    # movies they've rated. If analysis of a user who has rated many movies
    # kicks off late in execution, then that one analysis will greatly lengthen
    # execution time. Anecdotally, this problem can be seen with data sets as
    # small as 64 users. An improvement would be to sort (user_id, overwrite)
    # tuples by the number of movies each user has rated.
    pfu_args = tuple((user_id, overwrite) for user_id in user_ids)
    with multiprocessing.Pool(jobs) as pool:
        pool.starmap(analyze_user, pfu_args)


def analyze_user(user_id, overwrite):
    """Analyze a user, to find out which predictor works best for them.

    :param user_id: A user ID. The user for which an analysis is being
        performed.
    :param overwrite: If a user has already been analyzed, should the analysis
        be overwritten?
    :returns: Nothing.
    """
    with common.get_db_conn() as conn:
        # What if a user already has a predictor?
        if not overwrite and conn.execute(
                'SELECT * FROM predictors WHERE userId=?',
                (user_id,)
        ).fetchall():
            return

        # Create a personalized predictor for this user. SQLite added
        # support for UPSERT in version 3.24.0, which was released on
        # 2018-06-24. See: https://www.sqlite.org/lang_UPSERT.html
        sses = calc_sse(user_id)
        predictor = min_sse(sses)
        with conn:
            conn.execute(
                """
                INSERT INTO predictors VALUES (?, ?)
                ON CONFLICT (userId) DO UPDATE SET predictor=?
                """,
                (user_id, predictor, predictor)
            )


def calc_sse(user_id) -> Mapping[str, float]:
    """Calculate the SSE for each type of predictor for the given user.

    .. WARNING:: This function may take a long time to execute.

    :param user_id: A user ID.
    :return: A dict in the form ``{predictor_name: sum_of_squared_errors}``.
    """
    # predictor name → sum of squared errors
    sses: Dict[str, float] = {}

    for movie_id in read.rated_movies((user_id,)):

        # Make a bunch of predictors, like year, genre:comedy, and
        # genre:horror. Let them be based on all movies the current user has
        # rated except the control.
        predictors = {'year': ml.make_year_predictor(user_id, movie_id)}
        for genre in GENRES:
            predictors[f'genre:{genre}'] = (
                ml.make_genre_predictor(genre, user_id, movie_id)
            )

        # See how well each predictor predicts the control. If we're using a
        # year-based predictor, then two errors can occur:
        #
        # * The movie for which a prediction is being made doesn't have a
        #   year.
        # * The movie for which a prediction is being made does have a
        #   year, but all of the _other_ movies the user has rated don't
        #   have a year.
        #
        # In either case, we respond by not calculating an SSE for the
        # predictor.
        #
        # It is possible to encounter this problem for every combination of
        # (control movie, other movies) for a user. In this case, we set the
        # SSE for that type of predictor to "infinite." Other areas of the code
        # base must be prepared to find out that a predictor has an infinite
        # SSE.
        for pred_name, pred in predictors.items():
            try:
                predicted_rating = pred(movie_id)
            except (exceptions.NoMovieYearError, exceptions.EmptyGraphError):
                continue
            actual_rating = read.rating(user_id, movie_id)
            sses.setdefault(pred_name, 0)
            sses[pred_name] += (predicted_rating - actual_rating) ** 2

    sses.setdefault('year', float('inf'))
    return sses


def min_sse(sses):
    """Select the best predictor from the given choices.

    :param sses: A dict in the form ``{predictor_name:
        sum_of_squared_errors}``.
    :return: A predictor name.
    """
    best_pred_name, best_sse = sses.popitem()
    while sses:
        pred_name, sse = sses.popitem()
        if sse < best_sse:
            best_pred_name, best_sse = pred_name, sse
    return best_pred_name
