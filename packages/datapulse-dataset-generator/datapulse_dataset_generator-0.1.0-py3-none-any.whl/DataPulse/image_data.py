from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_image_id():
    return fake.uuid4()

def generate_image_url():
    return fake.image_url()

def generate_image_format():
    return fake.random_element(elements=["JPEG", "PNG", "BMP", "GIF", "TIFF"])

def generate_resolution():
    return f"{fake.random_int(min=640, max=3840)}x{fake.random_int(min=480, max=2160)}"

def generate_file_size():
    return f"{fake.random_int(min=100, max=5000)} KB"

def generate_color_mode():
    return fake.random_element(elements=["RGB", "CMYK", "Grayscale", "RGBA"])

def generate_capture_device():
    return fake.random_element(elements=["DSLR", "Smartphone", "Drone", "Webcam", "Security Camera"])

def generate_location():
    return fake.city()

def generate_capture_date():
    return fake.date_between(start_date='-5y', end_date='today')

def generate_license_type():
    return fake.random_element(elements=["Public Domain", "Creative Commons", "Royalty-Free", "Editorial Use Only"])

def generate_alt_text():
    return fake.sentence()

def generate_image_category():
    return fake.random_element(elements=["Nature", "Urban", "Portrait", "Abstract", "Food", "Sports", "Technology"])

def generate_aspect_ratio():
    return fake.random_element(elements=["16:9", "4:3", "1:1", "3:2", "21:9"])

def generate_metadata():
    return {"ISO": fake.random_int(min=100, max=3200), "Aperture": f"f/{fake.random_int(min=1, max=22)}", "Shutter Speed": f"1/{fake.random_int(min=30, max=8000)}s"}

def generate_photographer():
    return fake.name()

def generate_watermark():
    return fake.boolean(chance_of_getting_true=20)

def generate_image_tags():
    return [fake.word() for _ in range(5)]

def generate_image_source():
    return fake.random_element(elements=["Stock Library", "User Upload", "Generated", "Archived"])

def generate_focal_length():
    return f"{fake.random_int(min=18, max=200)}mm"

def generate_image_orientation():
    return fake.random_element(elements=["Landscape", "Portrait", "Square"])

def generate_image_data(num_records=100):
    data = [
        {
            "image_id": generate_image_id(),
            "image_url": generate_image_url(),
            "image_format": generate_image_format(),
            "resolution": generate_resolution(),
            "file_size": generate_file_size(),
            "color_mode": generate_color_mode(),
            "capture_device": generate_capture_device(),
            "location": generate_location(),
            "capture_date": generate_capture_date(),
            "license_type": generate_license_type(),
            "alt_text": generate_alt_text(),
            "image_category": generate_image_category(),
            "aspect_ratio": generate_aspect_ratio(),
            "metadata": generate_metadata(),
            "photographer": generate_photographer(),
            "watermark": generate_watermark(),
            "image_tags": generate_image_tags(),
            "image_source": generate_image_source(),
            "focal_length": generate_focal_length(),
            "image_orientation": generate_image_orientation(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_image_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_image_data')
# def download_image_data():
#     df = generate_image_data(500000)
#     file_path = "image_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
