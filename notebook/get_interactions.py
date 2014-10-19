import argparse
import urllib2
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def clear_interactions(interaction_id=None):

    client = MongoClient('localhost', 27017)
    db = client['interact-io']

    interaction_collection = db['interaction']

    if interaction_id:
        interactions = interaction_collection.find_one({'_id': interaction_id})
        count = len(interactions['interactions'])
        interaction_collection.remove({'_id': interaction_id})

    else:
        interactions = interaction_collection.find()
        count = interactions.count()

        for interaction in interactions:
            interaction_collection.remove({'_id': interaction['_id']})

    client.close()

    return count


def fetch_interactions(user, base_url, get_interactions_url):

    if not user:
        print "Invalid user."
        return

    url_interactions = base_url + get_interactions_url

    token = user['token']

    request = urllib2.Request(url_interactions)
    request.add_header('Content-Type', 'application/json')
    request.add_header('authToken', token)

    print "Fetching interactions for user %s..." % user['username']

    json_url = urllib2.urlopen(request)
    interactions = json.loads(json_url.read())

    print "Fetched %s interactions." % len(interactions)

    return interactions


def get_interactions(user, base_url, get_interactions_url, store=True):

    if not user:
        print "Invalid user."
        return

    interactions = fetch_interactions(user, base_url, get_interactions_url)

    if store:

        client = MongoClient('localhost', 27017)
        db = client['interact-io']
        interaction_collection = db['interaction']

        new_interaction = {'_id': user['id'],
                           'username': user['username'],
                           'interactions': interactions}
        count = len(interactions)

        try:
            interaction_collection.insert(new_interaction)
            print "Stored %s interactions for %s" % (count, user['username'])
        except DuplicateKeyError:
            print "Interactions already stored."
            print "Updating..."
            clear_interactions(user['id'])
            interaction_collection.insert(new_interaction)
            print "Interactions updated."

        client.close()

    return interactions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--user', default=None)
    parser.add_argument('-b', '--base_url', default="https://api.interact.io/v2")
    parser.add_argument('-i', '--get_interactions_url', default="/interactions")
    parser.add_argument('-s', '--store', default=True)
    args = parser.parse_args()

    get_interactions(args.user, args.base_url, args.get_interactions_url, args.store)