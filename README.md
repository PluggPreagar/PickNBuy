# PickNBuy


Implement a tool in python. It contains 5 parts. Part 1 is a crawler for web sides.  Part 2 is a Cache it stores the recieved pages.  Create a method for cache that calls checks if cache file exists. if no cache file for page is available reads crawl and stores the result in caching file. Part 3 is the extractor it extracts items from HTML DOM-Structure by DIV-Elements into assoziative array. Part 3 is a web interface. It offers Input-Elements for Page to crawl and filters to apply. As result it will list the items from the assoziative array.  It uses grid layout and lightweight style. Content is retrieved via lazyloading. Scrolling down retrieves further content.  Define a HTML with javascript to handle that. Part 4 is the coordinator it is started by the web interface and uses Part 1 to recieve pages and follows the next-page link.


