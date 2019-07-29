#Kindle weather page
This project consists of two distinct parts:
1) a python script which retrieves weather report and forecast pages from the National Weather Service, parses those pages to extract specific content, and builds an HTML page with the desired content.
2) A NodeJS web server which hosts a REST service to serve the HTML page.

A CRON job is set up to generate a new web page every hour, several minutes after the page is normally updated.

The Node REST service can also refresh the web page on demand.



