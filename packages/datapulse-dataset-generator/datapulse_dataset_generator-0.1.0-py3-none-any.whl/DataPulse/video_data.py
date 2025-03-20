from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_video_id():
    return fake.uuid4()

def generate_title():
    return fake.sentence(nb_words=6)

def generate_duration():
    return fake.random_int(min=10, max=14400)  # Duration in seconds (10 secs to 4 hours)

def generate_resolution():
    return fake.random_element(elements=["480p", "720p", "1080p", "4K", "8K"])

def generate_format():
    return fake.random_element(elements=["MP4", "AVI", "MKV", "MOV", "WMV"])

def generate_codec():
    return fake.random_element(elements=["H.264", "H.265", "VP9", "AV1"])

def generate_bitrate():
    return fake.random_int(min=500, max=50000)  # Bitrate in kbps

def generate_framerate():
    return fake.random_element(elements=[24, 30, 60, 120])

def generate_aspect_ratio():
    return fake.random_element(elements=["16:9", "4:3", "21:9", "1:1"])

def generate_file_size():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)  # Size in MB

def generate_category():
    return fake.random_element(elements=["Education", "Entertainment", "Sports", "Documentary", "Music", "Gaming"])

def generate_language():
    return fake.random_element(elements=["English", "Spanish", "French", "Chinese", "Hindi", "Arabic"])

def generate_uploaded_by():
    return fake.name()

def generate_upload_date():
    return fake.date_between(start_date='-5y', end_date='today')

def generate_license_type():
    return fake.random_element(elements=["Creative Commons", "Public Domain", "Standard", "Royalty-Free"])

def generate_audio_codec():
    return fake.random_element(elements=["AAC", "MP3", "Opus", "FLAC"])

def generate_subtitles():
    return fake.random_element(elements=["Yes", "No"])

def generate_views():
    return fake.random_int(min=0, max=10000000)

def generate_likes():
    return fake.random_int(min=0, max=500000)

def generate_dislikes():
    return fake.random_int(min=0, max=50000)

def generate_video_data(num_records=100):
    data = [
        {
            "video_id": generate_video_id(),
            "title": generate_title(),
            "duration": generate_duration(),
            "resolution": generate_resolution(),
            "format": generate_format(),
            "codec": generate_codec(),
            "bitrate": generate_bitrate(),
            "framerate": generate_framerate(),
            "aspect_ratio": generate_aspect_ratio(),
            "file_size": generate_file_size(),
            "category": generate_category(),
            "language": generate_language(),
            "uploaded_by": generate_uploaded_by(),
            "upload_date": generate_upload_date(),
            "license_type": generate_license_type(),
            "audio_codec": generate_audio_codec(),
            "subtitles": generate_subtitles(),
            "views": generate_views(),
            "likes": generate_likes(),
            "dislikes": generate_dislikes(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_video_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_video_data')
# def download_video_data():
#     df = generate_video_data(500000)
#     file_path = "video_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
