<div align="center">
  <img src="assets/searching.png" width="30%"/>
</div>

<div align="center">
  <h3> <a href="https://github.com/Solrikk/AsyncWebCollector/blob/main/README.md"> English | <a href="https://github.com/Solrikk/AsyncWebCollector/blob/main/README_RU.md">Русский</a> | <a href="https://github.com/Solrikk/AsyncWebCollector/blob/main/README_GE.md"> Deutsch </a> | <a href="https://github.com/Solrikk/AsyncWebCollector/blob/main/README_JP.md"> 日本語 </a> | <a href="README_KR.md">한국어</a> | <a href="README_CN.md">中文</a> </h3>
</div>

-----------------

# AsyncWebCollector ⚡️

AsyncWebCollector is an asynchronous web application built with FastAPI, designed for the asynchronous extraction and downloading of images from URLs provided in an uploaded file. The application scans the HTML content of web pages for images, extracts the image URLs, and exports the data in CSV format.

## Features
Asynchronous processing: Utilizing asynchronous libraries for efficient handling of multiple requests.
Batch URL processing: Capability to upload and process a list of URLs from a file.
Image extraction: Scans HTML for meta-tags indicating images and extracts the image URLs.
Results export: Compiles the processing results (image URLs or error messages) into a CSV file.
How It Works
Users upload a file (.txt) containing a list of URLs via the web interface. AsyncWebCollector asynchronously processes each URL, extracting image links from the HTML code. The processing outcomes (image URL or error message) are compiled into a CSV file that can then be downloaded from the server.

## Technologies
FastAPI: For creating the web application and managing asynchronous tasks.
BeautifulSoup: For parsing HTML and extracting data.
aiohttp: For asynchronous HTTP requests.
pandas: For convenient data handling and creating the CSV file.

Installation and Running
Clone the repository:
- `git clone https://github.com/yourusername/AsyncWebCollector.git`

Navigate to the project directory:
- `cd AsyncWebCollector`

Install dependencies:
- `pip install -r requirements.txt`

Run the application:
- `uvicorn main:app --reload`

Usage
After starting the application, navigate to http://localhost:8000 in your browser. Use the file upload form to submit your list of URLs. Once processing is complete, the application will provide a CSV file with the results for download.
