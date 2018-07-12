# Encyclopedia Dramatica Scraper
Scraper realized for the DMI summer School 2018. It contains all the scripts to get all the links among pages hosted on [encyclopediadramatica.rs](https://encyclopediadramatica.rs/Main_Page).

Links are extracted directly from wikitext to exclude transcluded links (e.g. all the links cotained in pages templates).

It is composed by a series aof scripts.

### 1-encyclopediadramatica-getallpages

Collects all the pages contained on the wiki.

### 2-encyclopediadramatica-getlinks-from-text

Starting from the output of the previous script, collect all the links coteined in the page.

### 3-encyclopediadramatica-target-redirects-resolver

Check redirects for list of pages. if not existing, the APIs are called to check wether there is a redirect, a normalization, or if the target poage doesn't exists.

### 4-encyclopediadramatica-consolidator

Merges the output of #2 and #3.

## Other scripts

### encyclopediadramatica-categories

Get all the categories from a wiki, and all the pages contained

### encyclopediadramatica-getlinks

Collect all the links contained in a page using the wikimedia API. Can be used in place of "2-encyclopediadramatica-getlinks-from-text".

### get-orphan-links

Can be used in place of "3-encyclopediadramatica-target-redirects-resolver". Honestly, i don't remember the difference between the two.

### links-deduplicator

convert a bipartite network to a monopartite one, keeping only reciprocal links among nodes.

