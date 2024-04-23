from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote
import asyncio
import os

app = FastAPI()


def extract_image_url(html_content):
  soup = BeautifulSoup(html_content, 'html.parser')
  image_meta = soup.find('meta', property='og:image')
  if image_meta:
    print(f"Found image URL: {image_meta['content']}")
    return image_meta['content']
  print("Image URL not found")
  return None


async def process_url(url, index, total):
  try:
    print(f"Processing URL {index+1}/{total}: {url}")
    response = requests.get(url)
    response.raise_for_status()
    image_url = extract_image_url(response.content.decode('utf-8'))
    if image_url:
      return {"URL": url, "ImageURL": image_url}
    else:
      return {"URL": url, "Error": "Image URL not found"}
  except requests.exceptions.HTTPError as err:
    print(f"HTTP error encountered while processing {url}: {err}")
    return {"URL": url, "Error": "HTTPError", "ErrorMessage": str(err)}
  except requests.exceptions.RequestException as e:
    print(f"Request exception encountered while processing {url}: {e}")
    return {"URL": url, "Error": "RequestException", "ErrorMessage": str(e)}


@app.get("/", response_class=HTMLResponse)
async def read_root():
  return """
    <html>
        <head>
            <title>Upload URLs File</title>
        </head>
        <body>
            <h2>Upload File</h2>
            <form action="/upload-file/" enctype="multipart/form-data" method="post">
            <input name="file" type="file" accept=".txt">
            <input type="submit">
            </form>
        </body>
    </html>
    """


@app.post("/upload-file/")
async def create_upload_file(file: UploadFile = File(...)):
  content = await file.read()
  urls = content.decode('utf-8').splitlines()

  print("Starting to process the uploaded file...")

  tasks = [
      process_url(url, index, len(urls)) for index, url in enumerate(urls)
  ]
  images_info = await asyncio.gather(*tasks)

  print(f"Processing completed. Total URLs processed: {len(urls)}")

  if images_info:
    df = pd.DataFrame(images_info)
  else:
    df = pd.DataFrame({"Message": ["No image URLs extracted"]})

  file_path = 'image_urls.csv'
  df.to_csv(file_path, index=False, encoding='utf-8-sig', sep=';')

  return FileResponse(path=file_path,
                      filename=file_path,
                      media_type='text/csv')


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
