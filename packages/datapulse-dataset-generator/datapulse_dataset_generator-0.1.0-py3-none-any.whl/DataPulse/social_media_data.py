from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_user_id():
    return fake.uuid4()

def generate_username():
    return fake.user_name()

def generate_email():
    return fake.email()

def generate_platform():
    return fake.random_element(elements=["Facebook", "Twitter", "Instagram", "LinkedIn", "TikTok", "Snapchat"])

def generate_post_id():
    return fake.uuid4()

def generate_post_content():
    return fake.sentence(nb_words=20)

def generate_post_date():
    return fake.date_time_this_year()

def generate_like_count():
    return fake.random_int(min=0, max=10000)

def generate_comment_count():
    return fake.random_int(min=0, max=5000)

def generate_share_count():
    return fake.random_int(min=0, max=3000)

def generate_followers_count():
    return fake.random_int(min=0, max=1000000)

def generate_following_count():
    return fake.random_int(min=0, max=5000)

def generate_profile_creation_date():
    return fake.date_this_decade()

def generate_account_status():
    return fake.random_element(elements=["Active", "Inactive", "Suspended"])

def generate_hashtags():
    return ", ".join(fake.words(nb=5))

def generate_location():
    return fake.city()

def generate_device_type():
    return fake.random_element(elements=["Mobile", "Desktop", "Tablet"])

def generate_engagement_rate():
    return round(fake.pyfloat(left_digits=1, right_digits=4, positive=True), 4)

def generate_content_type():
    return fake.random_element(elements=["Text", "Image", "Video", "Link"])

def generate_ad_impressions():
    return fake.random_int(min=0, max=100000)

def generate_social_media_data(num_records=100):
    data = []
    for _ in range(num_records):
        data.append({
            "user_id": generate_user_id(),
            "username": generate_username(),
            "email": generate_email(),
            "platform": generate_platform(),
            "post_id": generate_post_id(),
            "post_content": generate_post_content(),
            "post_date": generate_post_date(),
            "like_count": generate_like_count(),
            "comment_count": generate_comment_count(),
            "share_count": generate_share_count(),
            "followers_count": generate_followers_count(),
            "following_count": generate_following_count(),
            "profile_creation_date": generate_profile_creation_date(),
            "account_status": generate_account_status(),
            "hashtags": generate_hashtags(),
            "location": generate_location(),
            "device_type": generate_device_type(),
            "engagement_rate": generate_engagement_rate(),
            "content_type": generate_content_type(),
            "ad_impressions": generate_ad_impressions(),
        })

    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_social_media_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_social_media_data')
# def download_social_media_data():
#     df = generate_social_media_data(500000)
#     file_path = "social_media_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
