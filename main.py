# import uvicorn
# from functools import lru_cache
# from pydantic import BaseModel
# import config
# import boto3
# import base64
# from fastapi import FastAPI

# app=FastAPI()

# @lru_cache()
# def get_settings():
#     return config.Settings()

# class Text(BaseModel):
#     content: str
#     output_format: str

# @app.post("/")
# async def get_audio(text:Text):
#     client = boto3.client('polly', aws_access_key_id=get_settings().AWS_AK, aws_secret_access_key=get_settings().AWS_SAK, region_name='ap-south-1')
#     result = client.synthesize_speech(Text=text.content, OutputFormat=text.output_format, VoiceId='Aditi')
#     audio = result['AudioStream'].read()
    
#     # with open('audio.mp3','wb') as file:
#     #     file.write(audio)
    
#     # return {"message":text.content}
#     encoded_audio = base64.b64encode(audio).decode('utf-8')
#     return {"message": "Audio convertion complete", "data" : {
#         "text": text.content,
#         "output_format": text.output_format,
#         "audio": encoded_audio
#     }} 

# if __name__=="__main__":
#     uvicorn.run("main:app",host="0.0.0.0",port=8080,reload=True)

# import uvicorn
# from functools import lru_cache
# from pydantic import BaseModel
# import config
# import boto3
# from fastapi import FastAPI, HTTPException, Response

# app = FastAPI()

# @lru_cache()
# def get_settings():
#     return config.Settings()

# class Text(BaseModel):
#     content: str
#     output_format: str

# @app.post("/")
# async def get_audio(text: Text):
#     client = boto3.client(
#         'polly',
#         aws_access_key_id=get_settings().AWS_AK,
#         aws_secret_access_key=get_settings().AWS_SAK,
#         region_name='ap-south-1'
#     )
    
#     result = client.synthesize_speech(
#         Text=text.content,
#         OutputFormat=text.output_format,
#         VoiceId='Aditi'
#     )
    
#     if 'AudioStream' not in result:
#         raise HTTPException(status_code=500, detail="Failed to generate audio")

#     audio = result['AudioStream'].read()
    
#     response = Response(content=audio, media_type='audio/mpeg')
#     response.headers["Content-Disposition"] = f"attachment; filename=audio.mp3"
#     return response

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
import os
import time
import uvicorn
from functools import lru_cache
from pydantic import BaseModel
import config
import boto3
from fastapi import FastAPI, HTTPException, Response

app = FastAPI()

@lru_cache()
def get_settings():
    return config.Settings()

class Text(BaseModel):
    content: str
    output_format: str

def save_audio_file(audio_content):
    folder_path = "audio_files"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    timestamp = int(time.time())  # Use timestamp as a unique identifier
    file_name = f"audio_{timestamp}.mp3"
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_content)

    return file_path

@app.post("/")
async def get_audio(text: Text):
    client = boto3.client(
        'polly',
        aws_access_key_id=get_settings().AWS_AK,
        aws_secret_access_key=get_settings().AWS_SAK,
        region_name='ap-south-1'
    )
    
    result = client.synthesize_speech(
        Text=text.content,
        OutputFormat=text.output_format,
        VoiceId='Aditi'
    )
    
    if 'AudioStream' not in result:
        raise HTTPException(status_code=500, detail="Failed to generate audio")

    audio = result['AudioStream'].read()
    
    file_path = save_audio_file(audio)
    
    response = Response(content=audio, media_type='audio/mpeg')
    response.headers["Content-Disposition"] = f"attachment; filename=audio.mp3"
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
