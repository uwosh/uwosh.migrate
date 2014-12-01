scripts
-------
Contains some misc. scripts that I created when transitioning the COLS site.

uwosh.migrate
-------------
Now available as a product. Yay!!

These scripts should grab the html from the pages and create new Plone documentsfrom it. It will create the necessary folders too.

The whole thing is kind of a big hack. I plan to improve it.

There is now a little bit of security. You will need cmf.ManagePortal privilages to run the script.

To access the script the url is: /migrate-pages
So.....something like: http://localhost:8080/Plone/migrate-pages


Sitemapper
----------
Sitemapper is an opensource sitemapping script written in perl.
I didn't write it. I just modified it.
I modified it to summarize its results and create plain text list of urls. And I added support for .pdf .doc and .php.
