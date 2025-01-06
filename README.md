# LeetCode Scraper and MongoDB Collector

## Overview

This Python application uses Selenium to scrape user statistics from the LeetCode website and stores the data in MongoDB in a structured JSON format. It is designed to provide an efficient way to collect and manage LeetCode performance data for analysis or sharing.

## Features

Automates browser interaction using Selenium to scrape data from LeetCode.
Collects data in JSON format, including details like:
Username
Problem-solving status (easy, medium, hard)
Total problems solved and total problems available
Programming languages used and the count of problems solved in each language.
Inserts the data into a MongoDB collection for further use or analysis.
Requirements

## Sample Data
Here is an example of the JSON data collected by the scraper:
```json
{
    "username": "pingruchou1125tw",
    "easy_status": "363/846",
    "medium_status": "440/1775",
    "hard_status": "31/785",
    "total_solved": "834",
    "total_problem": "3406",
    "languages_info": {
        "Python3": 797,
        "C++": 87,
        "C": 38,
        "Go": 15,
        "JavaScript": 10,
        "Java": 9,
        "Python": 7,
        "Kotlin": 2
    }
}
```

## Environment
Python 3.6+
### Python Libraries
selenium: For automating browser interactions. <br>
pymongo: For interacting with MongoDB. <br>
json: For handling JSON data.

### Setup

1. Clone the Repository
```cd leetcode-scraper```
2. Install Dependencies with 
```pip install -r requirements.txt```

## Notes:
Make sure the browser driver (e.g., ChromeDriver) is installed and in your system's PATH.
You may need additional dependencies depending on how you handle specific scenarios in your scraper. Let me know if you need further customization!