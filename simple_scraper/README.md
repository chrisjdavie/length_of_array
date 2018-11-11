# Run

Requires `Python 3.7`, and requires `aiohttp` to be installed.

Needs `simple_scraper` to be importable (in linux, in the parent folder, `export 
From the parent folder,  `export PYTHONPATH=$PYTHONPATH:$PWD` will achieve this).

To run, run

`python3.7 simple_scraper/run_scraper.py <output json path>`

The scraper will the take urls from stdin and scrape them. For instance

`python3.7 simple_scraper/run_scraper.py test.json < simple_scraper/tests/data/list_of_urls.txt`

will take the list of urls from `simple_scraper/tests/data/list_of_urls.txt` and output it to `test.json`.

An empty line will terminate the scraper.

# Tests

In addition to the above requirements, the tests require `parameterized` and `asynctest`. The tests are implemented using `unittest` and can be run using

` python3.7 -m unittest discover -v simple_scraper/`
 
# Sites tested on

The scraper seems to work on the sky sports website, the guardian and bbc sports. It doesn't work well on bbc news, seems to be due to image load being delayed through javascript.

For a production scraper, the tests would need to be much more extensive.

# Stability

- on invalid urls, it logs an error and records the traceback
- if it hits connectivity issues, it logs an error and records the traceback
 
# Comments on the scraper

- it doesn't typically resolve images imported from twitter
- it sometimes finds valid pictures and captions that aren't rendered on the screen
- if there are issues with the connection, it logs an error and returns empty strings. It does not try to recover
- it doesn't test that the image urls are valid, but that would be a valuable addition (but increase the run time)
- there is a good chance I've missed a bunch of different erros, in terms of connectivity issues and websites this can't handle


# Additonal tests

The scraper seems to work for some sites and not others. A specific problem seems to be with BBC news and some javascript image loading.

All examined on 11/11/2018

## Additional websites it works for

https://www.theguardian.com/football/blog/2018/nov/10/united-way-jose-mourinho-manchester-city-derby

https://www.bbc.co.uk/sport/mixed-martial-arts/46168948

## Additional websites it doesn't work for

https://www.bbc.co.uk/news/world-us-canada-46145777 - fails to capture image

https://www.bbc.co.uk/news/world-us-canada-46168107 - captures 3/4 images, fails
to load the following javascript
`<div class="js-delayed-image-load" data-alt="A house on fire in Malibu, 9 November 2018" data-src="https://ichef.bbci.co.uk/news/320/cpsprodpb/129CC/production/_104263267_221cb814-e45c-49e0-ada7-c36b607a1c92.jpg" data-width="976" data-height="549"></div>`

