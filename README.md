Interactions
============

Work sample for [Interact.io](http://www.interact.io) by [Victor Kristof](mailto:victor.kristof@epfl.ch).

Available online at [interactions-victor.herokuapp.com](http://interactions-victor.herokuapp.com).


## Setup

### MongoDB
The [MongoDB](http://www.mongodb.org) NoSQL database system will be used to store interactions data.

```
brew install mongodb
```

### PyMongo
The package [PyMongo](http://api.mongodb.org/python/current/) is an interface between MongoDB and Python.

```
pip install pymongo
```

### Flask
The [Flask](http://flask.pocoo.org) microframework must be installed to run the local website.

```
pip install Flask
```

## Use
Start by running the MongoDB database server:

```
mongod
```

Then run the web server in the `/webapp` folder using:

```
python2.7 interact.py
```

The web site is then available at [http://127.0.0.1:5000](http://127.0.0.1:5000).
