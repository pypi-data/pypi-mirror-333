import aiohttp
import asyncio
from pyrogram import Client
import httpx
import http.client, json

async def verif_auido(KEY, video_id: str):
  conn = http.client.HTTPSConnection("api-to-download-songs-from-youtube-to-telegram.p.rapidapi.com")

  headers = {
    'x-rapidapi-key': f"{KEY}",
    'x-rapidapi-host': "api-to-download-songs-from-youtube-to-telegram.p.rapidapi.com"
  }
  conn.request("GET", f"/yt-download?video_id={video_id}&media_type=audio", headers=headers)
  res = conn.getresponse()
  data = res.read()
  response_json = json.loads(data.decode("utf-8"))
  download_link = response_json.get("download_link", "No link found")
  live_stream_link = response_json.get("link_live") 
  if live_stream_link:  
        return {"type": "live", "url": live_stream_link}     
  if download_link:
        return {"type": "download", "url": download_link}
 


async def verif_video(KEY, video_id: str):
  conn = http.client.HTTPSConnection("api-to-download-songs-from-youtube-to-telegram.p.rapidapi.com")

  headers = {
    'x-rapidapi-key': f"{KEY}",
    'x-rapidapi-host': "api-to-download-songs-from-youtube-to-telegram.p.rapidapi.com"
  }
  conn.request("GET", f"/yt-download?video_id={video_id}&media_type=video", headers=headers)
  res = conn.getresponse()
  data = res.read()
  response_json = json.loads(data.decode("utf-8"))
  download_link = response_json.get("download_link", "No link found")
  live_stream_link = response_json.get("link_live") 
  if live_stream_link:  
        return {"type": "live", "url": live_stream_link}     
  if download_link:
        return {"type": "download", "url": download_link}

class YTeva:
    def __init__(self, api_key: str, bot_app, max_retries=30, retry_delay=3000):
        self.api_key = api_key
        self.bot_app = bot_app
        self.channel = "Data_eva"
        self.session = httpx.AsyncClient(timeout=400)
        self.max_retries = max_retries
        self.retry_delay = retry_delay


    async def fetch_audio_link(self, video_id: str):
        return await verif_auido(self.api_key, video_id)
    
    async def fetch_video_link(self, video_id: str): 
        return await verif_video(self.api_key, video_id)
    
    async def play_audio(self, video_id: str):
        result = await self.fetch_audio_link(video_id)  
        if result["type"] == "live":
            return result["url"] 
        telegram_link = result["url"]
        message_id = int(telegram_link.split("/")[-1])
        msg = await self.bot_app.get_messages(self.channel, message_id)
        downloaded_file = await msg.download(file_name=f"downloads/{video_id}.m4a")
        return downloaded_file

    async def play_video(self, video_id: str):
        result = await self.fetch_video_link(video_id)  
        if result["type"] == "live":
            return result["url"]
        telegram_link = result["url"]
        message_id = int(telegram_link.split("/")[-1])
        msg = await self.bot_app.get_messages(self.channel, message_id)
        downloaded_file = await msg.download(file_name=f"downloads/{video_id}.mp4")
        return downloaded_file
    
    async def download_send_audio(self, video_id: str):
        result = await self.fetch_audio_link(video_id)  
        telegram_link = result["url"]
        return telegram_link
    
    async def download_send_video(self, video_id: str):
        result = await self.fetch_video_link(video_id)  
        telegram_link = result["url"]
        return telegram_link
        
    async def close(self):
        await self.session.close()
