# Scraping News Paper

<head>
    <title>Code Descriptions</title>
</head>
<body>

    <h1>About This GitHub Repository:</h1>
    <p>This GitHub repository is part of my work as a Research Assistant. It hosts various code and scripts employed in the research.</p>

    <h2>Data Availability:</h2>
    <p>Please note that the data itself is not provided in this repository.</p>

    <h2>Prerequisites:</h2>
    <ul>
        <li>A <code>.env</code> file needs to be created to host passwords and user credentials.</li>
        <li>A folder named <code>article_titles_json</code> should be created if you wish to additionally save article titles in JSON format.</li>
    </ul>

    <hr>

    <h1>crawl.py:</h1>
    <p>The code performs web scraping of articles from the Wall Street Journal (WSJ) for a specific year. It extracts the article details and stores them in an SQLite database and also saves the information in JSON files. It uses libraries such as <code>requests</code>, <code>BeautifulSoup</code>, <code>json</code>, and <code>sqlite3</code>. The code is organized into distinct classes and methods:</p>
    
    <ul>
        <li><code>ManagementDB</code> class: Handles SQLite database operations, such as inserting article details and tracking page explorations.</li>
        <li><code>WebScrap</code> class: Manages the web scraping logic, extracting article details like headlines, timestamps, and links.</li>
        <li>Uses the <code>requests</code> library to make HTTP requests and fetch web pages.</li>
        <li>Stores the scraped article information both in an SQLite database and JSON files.</li>
        <li>Supports pagination by incrementing the page number until no more articles are found.</li>
    </ul>
    
    <p>The script also includes rate-limiting measures by incorporating sleep timings. It is capable of printing debugging information like page status codes and the URLs being explored.</p>


    <hr>

    <h1>createDB.py:</h1>
    <p>This script is responsible for initializing the SQLite database that will store the scraped articles and related information. It creates three tables: <code>articles_index</code>, <code>article</code>, and <code>exploration</code>. Each table is designed to hold specific types of data that are crucial for the web scraping and data analysis process.</p>

    <p>The <code>articles_index</code> table contains metadata about the articles such as the headline, publication time, and link.</p>

    <p>The <code>article</code> table stores detailed information about each article, including any associated images and the text corpus.</p>

    <p>The <code>exploration</code> table logs details about the web scraping process itself, including the URLs that have been checked, the number of articles found on each page, and whether or not values were extracted from that page.</p>
    
    <hr>

    <h1>delete_duplicates.py:</h1>
    <p>This script is designed to eliminate duplicate records from the <code>articles_index</code> table in the SQLite database. It does so by identifying articles with the same link and retaining only one instance of each while deleting the others. The number of deleted elements is displayed at the end.</p>

    <hr>

    <h1>delete_jumplines.py:</h1>
    <p>This script is aimed at cleaning the <code>headline</code> field in the <code>articles_index</code> table of the SQLite database. Specifically, it removes newline characters ('\n') that may have been inadvertently inserted during the scraping process. Modified headlines are updated in the database, and a log is printed to indicate the IDs of the updated records.</p>

    <h1>web_scrap.py:</h1>
    <p>This script performs automated web scraping of Wall Street Journal articles. It uses Selenium for browser automation and navigation. The script is divided into different classes and functions for better modularity:</p>
    
    <ul>
        <li><code>Scraper</code> class initializes a web driver and prepares the browser for scraping.</li>
        <li><code>Search4Articles</code> class inherits from <code>Scraper</code> and provides specific functionalities for WSJ such as signing in and scraping articles.</li>
        <li>The script leverages the <code>.env</code> file to securely manage sensitive information like login credentials.</li>
        <li>It fetches unscanned article links from an SQLite database, scrapes their content, and then updates the database.</li>
        <li>Logs are generated using Python's built-in logging module.</li>
        <li>Scraped articles, along with their metadata, are inserted back into the SQLite database.</li>
    </ul>

    <p>For performance and rate-limiting, the script includes various sleep timings. It also prints out debugging and state information during execution.</p>

</body>
