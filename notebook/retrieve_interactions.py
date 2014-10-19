import argparse
from pymongo import MongoClient


def retrieve_interactions(user):

    client = MongoClient('localhost', 27017)
    db = client['interact-io']

    interaction_collection = db['interaction']
    interaction = interaction_collection.find_one({'_id': user['id']})
    interactions = interaction['interactions']

    print "Retrieved %s interactions for %s." % (len(interactions), user['username'])

    client.close()

    return interactions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--user', default=None)
    args = parser.parse_args()

    retrieve_interactions(args.user)
