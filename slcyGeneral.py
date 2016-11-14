from twython import Twython
import time

APP_KEY='zmmlyAJzMDIntLpDYmSH98gbw'
APP_SECRET='ksfSVa2hxvTQKYy4UR9tjpb57CAynMJDsygz9qOyzlH24NVwpW'
OAUTH_TOKEN='794094183841566720-BagrHW91yH8C3Mdh9SOlBfpL6wrSVRW'
OAUTH_TOKEN_SECRET='d0Uucq2dkSHrFHZGLM1X8Hw05d80ajKYGl1zTRxZQSKTm'
applepislcy = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

### GENERAL ###

def Cleanup():
    GPIO.cleanup()

def Sleep(seconds) -> None:
    """Puts the program to sleep"""
    time.sleep(seconds)

def Alert(channel) -> None:
    """Simple alert function for testing event interrupts"""
    print('Alert on channel',channel)


### TWITTER ###

def Tweet(twit,statustext) -> None:
    """Tweets a message
    twit <Twython>, create with Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    statustext <str>, must be <= 140 characters
    """
    if len(statustext) > 140:
        print('ERROR: Character limit 140 exceeded:',len(statustext))
    else:
        twit.update_status(status=statustext)

def TweetPicture(twit,file,statustext) -> None:
    """Tweets a message with a picture
    twit <Twython>, create with Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    file <str>, path and filename to picture
    statustext <str>, must be <= 140 characters
    """
    photo = open(file, 'rb')
    response = twitter.upload_media(media=photo)
    twit.update_status(status=statustext, media_ids=[response['media_id']])

def TweetVideo(twit,file,statustext) -> None:
    """Tweets a message with a video
    twit <Twython>, create with Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    file <str>, path and filename to video
    statustext <str>, must be <= 140 characters
    """
    video = open(file, 'rb')
    response = twitter.upload_video(media=video, media_type='video/mp4')
    twit.update_status(status=statustext, media_ids=[response['media_id']])
