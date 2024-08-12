import os
import random
from secret import YOUTUBE_API

import googleapiclient.discovery

unique_users = []


def get_unique_users(response, owner_id):
    comments = response['items']
    
    for comment in comments:
        handle_name = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
        if handle_name not in unique_users and handle_name != owner_id:
            unique_users.append(handle_name)


def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = YOUTUBE_API
    # to make sure the channel owner isn't qualified
    owner_id = input("Owner's Handle ID:")
    myVideoId = input("Video ID:")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=myVideoId,
        maxResults="100"
    )
    
    response = request.execute()
    get_unique_users(response,owner_id)
    
    # If more than 100 comments
    while 'nextPageToken' in response:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=myVideoId,
            maxResults="100",
            pageToken=response["nextPageToken"]
        )
        response = request.execute()
        get_unique_users(response,owner_id)

    print("Number of Unique Users:",len(unique_users))
    pick_num = int(input("Enter number of users to pick:"))

    print("Congratulations:")
    random_numbers = []
    for i in range(0,pick_num):
        random_number = random.randint(0,len(unique_users)-1)
        while random_number in random_numbers:
            random_number = random.randint(0,len(unique_users)-1)
        print(unique_users[random_number])
        random_numbers.append(random_number)

if __name__ == "__main__":
    main()
