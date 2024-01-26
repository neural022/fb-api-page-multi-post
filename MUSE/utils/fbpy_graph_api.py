# -*- coding: utf-8 -*-

"""
@author: george chen(neural022)

"""
from facepy import GraphAPI, FacebookError
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FacebookUserAPI():
    def __init__(self, access_token, api_version="18.0"):
        self.graph_api = GraphAPI(access_token, version=api_version)

    def get_managed_pages(self):
        """
        Get the list of pages managed by the user.

        Returns:
            list: List of dictionaries containing page details.
        """
        fan_pages = self.graph_api.get('me/accounts')['data']
        return fan_pages
            

class FacebookPageAPI():
    def __init__(self, access_token, api_version="18.0"):
        self.graph_api = GraphAPI(access_token, version=api_version)

    def upload_image(self, image_path, publish=False):
        """
        Upload an image to Facebook without necessarily publishing it.
        
        Args:
            image_path (str): Path to the image file.
            publish (bool): Whether to publish the image immediately.

        Returns:
            list: List containing dictionary with media id.
        """
        with open(image_path, 'rb') as image:
                    image_data = self.graph_api.post(
                        path = 'me/photos', 
                        source = image, 
                        published = publish
                    )
    
        return [{'media_fbid': image_data['id']}]
    
    def post(self, message=None, attached_media=None):
        """
        Post a message and/or media to Facebook page.

        Args:
            message (str): The text message to post.
            attached_media (list): List containing media data to post.

        Returns:
            dict: Response data from the post request.
        """
        # create post data
        post_data = dict()
        if message:
            post_data['message'] = message
        if attached_media:
            post_data['attached_media'] = attached_media

        response = self.graph_api.post(path='me/feed', **post_data)
        return response

def determine_post_type(post_text, post_image):
    """Determine the type of post based on provided text and image."""
    has_text = bool(post_text.strip())  
    has_image = bool(post_image.strip())
    return has_text, has_image

def get_long_lived_token(app_id, app_secret, short_lived_token, api_version="18.0"):
    graph = GraphAPI(oauth_token=short_lived_token, version=api_version)
    path = f"oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={short_lived_token}"
    response = graph.get(path)
    return response.get('access_token')


if __name__ == '__main__':
    # example
    APP_ID = '<YOUR_APP_ID>'
    APP_SECRET = '<YOUR_APP_SECRET>'
    USER_ACCESS_TOKEN = '<USER_ACCESS_TOKEN>'

    user = FacebookUserAPI(USER_ACCESS_TOKEN)

    target_page_ids = list()
    post_text = "fbpy API Test！"
    post_image = "../img/example.jpg"

    has_text, has_image = determine_post_type(post_text, post_image)

    try:
        for page_data in user.get_managed_pages():
            if page_data['id'] in target_page_ids:
                page = FacebookPageAPI(page_data['access_token'])

                if has_text and not has_image:
                    # 純發文字
                    page.post(message=post_text)

                elif not has_text and has_image:
                    # 純發圖片
                    page.upload_image(post_image, publish=True)

                elif has_text and has_image:
                    # 圖片加文字
                    attached_media = page.upload_image(post_image, publish=False)
                    page.post(message=post_text, attached_media=attached_media)

                logger.info(f"Posted to page {page_data['id']}:{page_data['name']} successfully!")

    except FacebookError as e:
        logger.error(f"Error occurred while interacting with Facebook: {e}")
    except FileNotFoundError:
        logger.error(f"Error: Specified image path not found.")