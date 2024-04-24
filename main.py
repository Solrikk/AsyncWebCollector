
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote
import asyncio
import os
import time

app = FastAPI()


def extract_image_url(html_content):
  soup = BeautifulSoup(html_content, 'html.parser')
  image_meta = soup.find('meta', property='og:image')
  if image_meta:
    return image_meta['content']
  return None


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def process_url(session, url):
  try:
    html_content = await fetch(url, session)
    image_url = extract_image_url(html_content)
    if image_url:
      return {"URL": url, "ImageURL": image_url}
    else:
      return {"URL": url, "Error": "Image URL not found"}
  except aiohttp.ClientError as err:
    return {"URL": url, "Error": "ClientError", "ErrorMessage": str(err)}
  except Exception as e:
    return {"URL": url, "Error": "Unhandled exception", "ErrorMessage": str(e)}


async def process_batch(urls):
  async with aiohttp.ClientSession() as session:
    tasks = [process_url(session, url) for url in urls]
    return await asyncio.gather(*tasks)


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

  batch_size = 10  # Adjust the batch size as needed
  batches = [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]
  total_urls = len(urls)

  start_time = time.time()
  processed_count = 0

  print("Starting to process the uploaded file...")

  images_info = []
  for batch in batches:
    batch_result = await process_batch(batch)
    images_info.extend(batch_result)
    processed_count += len(batch)
    elapsed_time = time.time() - start_time
    remaining_urls = total_urls - processed_count
    est_total_time = (elapsed_time / processed_count) * total_urls
    remaining_time = est_total_time - elapsed_time
    print(
        f"Processed: {processed_count}/{total_urls} URLs. Estimated remaining time: {remaining_time:.2f} seconds."
    )

  print(f"Processing completed. Total URLs processed: {total_urls}")

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
