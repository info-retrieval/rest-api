# Search Engine Rest API

## Requirements

To run this project you need to have installed:
* [Python 3.5](https://www.python.org/)
* [Python pip](https://pypi.python.org/pypi/pip)
* [Java 7+](http://www.oracle.com/technetwork/java/javase/downloads/index.html) - Just for Elasticsearch to run
* [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html#jvm-version)

### Installing Elasticsearch

To install this search engine, download it from the [official site](https://www.elastic.co/downloads/elasticsearch)
and unzip it to this project root folder.

### Installing Python dependencies

After installing pip, run on terminal
```bash
$ pip install -r requirements.txt
```
remember that you need to be `root` or run as `sudo`

## Populate database

You only have to do this part if you do not have an index populated. If you do, jump to the next step.

After running [./search-engine/index.sh](https://github.com/info-retrieval/search-engine) you will have a _parser.json_ file. Copy and paste it to this project folder (rest-api) and run 
```bash
$ python manage.py dummy_data
```

then, you have to populate your index from _elasticsearch_. To do this, run
```bash
$ python manage.py post-to-index
```

## Running

Start your _elasticsearch_ service with `./path/to/elasticsearch-version/bin/elasticsearch` 
and finally, run `python manage.py runserver` to run this service and then you can use this API on your frontend.
