import requests
import json
import os


class Twitter:
    def __init__(self):
        self.session = requests.session()
        with open('./token.json', 'r') as f:
            self.session.headers = json.load(f)

    def update_profile(self, data):
        url = 'https://twitter.com/i/api/1.1/account/update_profile.json'
        res = self.session.post(url=url, data=data)

        return res.text

    def upload_image(self, file_path):
        file_len = os.path.getsize(file_path)
        media_type = "png"
        if ".jpg" in file_path:
            media_type = "jpg"

        # INIT
        url = f"https://upload.twitter.com/i/media/upload.json?command=INIT&total_bytes={file_len}&media_type=image%2F{media_type}&media_category=tweet_image"
        init_res = self.session.post(url=url)
        media_id = init_res.json()['media_id']

        # APPEND
        url = f"https://upload.twitter.com/i/media/upload.json?command=APPEND&media_id={media_id}&segment_index=0"
        append_res = self.session.post(url=url, files={'media': open(file_path, "rb")})

        # FINALIZE
        url = f"https://upload.twitter.com/i/media/upload.json?command=FINALIZE&media_id={media_id}"
        finalize_res = self.session.post(url=url)

        return media_id

    def tweet(self, text, image_list=[]):
        query_id = "rNfquQyDIcs2VnKnWa47jA"
        url = "https://twitter.com/i/api/graphql/rNfquQyDIcs2VnKnWa47jA/CreateTweet"
        data = {"tweet_text":text,"media":{"media_entities":[],"possibly_sensitive":False},"withDownvotePerspective":False,"withReactionsMetadata":False,"withReactionsPerspective":False,"withSuperFollowsTweetFields":True,"withSuperFollowsUserFields":True,"semantic_annotation_ids":[],"dark_request":False,"withBirdwatchPivots":False,"__fs_interactive_text": False,"__fs_dont_mention_me_view_api_enabled":False}
        media = {"possibly_sensitive":False}

        media_list = []
        for img_path in image_list:
            media_id = self.upload_image(img_path)
            pack = {'media_id':str(media_id),'tagged_users':[]}
            media_list.append(pack)

        media['media_entities'] = media_list
        data['media'] = media
        post_data = {'variables':json.dumps(data),"queryId":query_id}
        res = self.session.post(url=url, json=post_data)

        return json.dumps(res.json())

    def retweet(self, tweet_id):
        url = 'https://twitter.com/i/api/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet'
        variables = {"tweet_id":tweet_id,"dark_request":False}
        query_id = 'ojPdsZsimiJrUGLR1sjUtA'
        data = {"variables": json.dumps(variables), "queryId": query_id}
        res = self.session.post(url=url, json=data)

        return res.text

    def reply(self, tweet_id, text):
        url = 'https://twitter.com/i/api/graphql/hxq2o_BHpqLf0HGwKciGXA/CreateTweet'
        variables = {"tweet_text":text,"reply":{"in_reply_to_tweet_id":tweet_id,"exclude_reply_user_ids":[]},"media":{"media_entities":[],"possibly_sensitive":False},"withDownvotePerspective":False,"withReactionsMetadata":False,"withReactionsPerspective":False,"withSuperFollowsTweetFields":True,"withSuperFollowsUserFields":True,"semantic_annotation_ids":[],"dark_request":False,"__fs_interactive_text":False,"__fs_responsive_web_uc_gql_enabled":False,"__fs_dont_mention_me_view_api_enabled":False}
        query_id = 'hxq2o_BHpqLf0HGwKciGXA'
        data = {"variables": json.dumps(variables), "queryId": query_id}
        res = self.session.post(url=url, json=data)

        return res.text


if __name__ == "__main__":
    obj = Twitter()

    profile_data = {
        'birthdate_year': '2000',
        'birthdate_month': '1',
        'birthdate_day': '1',
        'birthdate_visibility': 'self',
        'birthdate_year_visibility': 'self',
        'displayNameMaxLength': 50,
        'url': 'https://twitter.com/vincent20763977',
        'name': 'vincentYu',
        'description': '123456789',
        'location': 'Taiwan'
    }

    # 編輯個人資料
    print(obj.update_profile(data=profile_data))

    # 發送推文
    print(obj.tweet(text='tweet test', image_list=['./Media/cat.png', './Media/dog.jpg']))

    # 轉貼推文
    print(obj.retweet(tweet_id='1486003812943163392'))

    # 回復推文
    print(obj.reply(tweet_id='1486003812943163392', text='marvelous!'))
