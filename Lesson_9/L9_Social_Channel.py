from abc import ABC, abstractmethod
from time import time, sleep


class SocialChannel(ABC):
    def __init__(self, name: str, followers: int):
        self.name = name
        self.followers = followers

    @abstractmethod
    def post_message(self, message: str) -> None:
        pass


class YouTubeChannel(SocialChannel):
    def __init__(self, followers: int):
        super().__init__('YouTube', followers)

    def post_message(self, message: str):
        print(f"Posted to {self.name}: {message}")


class FacebookChannel(SocialChannel):
    def __init__(self, followers: int):
        super().__init__('Facebook', followers)

    def post_message(self, message: str):
        print(f"Posted to {self.name}: {message}")


class TwitterChannel(SocialChannel):
    def __init__(self, followers: int):
        super().__init__('Twitter', followers)

    def post_message(self, message: str):
        print(f"Posted to {self.name}: {message}")


class Post:
    def __init__(self, message: str, timestamp: int):
        self.message = message
        self.timestamp = timestamp


def process_schedule(posts: list[Post], channels: list[SocialChannel]):
    while posts:
        post_time = int(time())
        for post in posts[:]:
            if post.timestamp <= post_time:
                for channel in channels:
                    channel.post_message(post.message)
                posts.remove(post)
        sleep(1)


def main():
    twitter_channel = TwitterChannel(followers=4000)
    facebook_channel = FacebookChannel(followers=7000)
    youtube_channel = YouTubeChannel(followers=1000)

    post_1 = Post("Type your next message.", int(time()+3))
    post_2 = Post("Hi User!", int(time()))
    post_3 = Post("New video is available!", int(time() + 3))

    process_schedule([post_1, post_2], [twitter_channel, facebook_channel])
    process_schedule([post_3], [youtube_channel])


main()

