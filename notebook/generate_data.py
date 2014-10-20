import argparse
from datetime import datetime, timedelta
from math import floor
from retrieve_interactions import retrieve_interactions


def interactions_for_period(user, period):

    today = datetime.today()
    last_N_days = today - timedelta(days=period)

    interactions = retrieve_interactions(user)

    filtered = [i for i in interactions if datetime.fromtimestamp(int(i['time']/1000)) > last_N_days]

    return filtered


def sample_interactions(interactions, frequency, period):

    today = datetime.today()

    start = today.replace(hour=0, minute=0, second=0)
    end = today.replace(hour=23, minute=59, second=59)

    start -= timedelta(days=frequency-1)

    samples = []
    current_interval = []

    # Generate list of bins (list of interactions)
    for interaction in interactions:
        time = datetime.fromtimestamp(int(interaction['time']/1000))
        if start < time < end:
            current_interval.append(interaction)
        else:
            samples.append(current_interval)
            current_interval = []
            start -= timedelta(days=frequency)
            end -= timedelta(days=frequency)

    # Add empty list to complete if there is no data at the end of the period
    expected_length = int(floor(period / frequency))
    if len(samples) != expected_length:
        to_add = expected_length - len(samples)
        for i in xrange(to_add):
            samples.append([])

    # Reverse list of number of interactions to have it from most ancient to most recent
    num_interactions = [len(x) for x in reversed(samples)]

    return samples, num_interactions


def generate_data(user, frequency, period):
    """
    Generate the sampled interactions and the number of interactions to be displayed.

    :param user: the user whose interactions are fetched
    :param frequency: the frequency of sampling in day (1, 7, 12)
    :param period: the time period to be reported (7, 30, 90, 365)
    :return: a tuple (samples, num_interactions) with samples a list of list of interactions and
    num_interactions a list of list of number of interactions in reversed order
    (from most ancient to most recent).
    """

    if not user:
        print "Invalid user."
        return

    interactions_filtered = interactions_for_period(user, period)
    samples, num_interactions = sample_interactions(interactions_filtered, frequency, period)

    print "Generated data over %s days sampled every %s day for user %s." %\
          (period, frequency, user['username'])

    return samples, num_interactions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--user', default=None)
    parser.add_argument('-f', '--frequency', default=1)
    parser.add_argument('-p', '--period', default=7)
    args = parser.parse_args()

    generate_data(args.user, args.frequency, args.period)
