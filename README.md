
# Facebook API Page Multi-Post

This project provides a streamlined way to post content to multiple Facebook Pages using the Facebook API. Below are the setup instructions and a demonstration of the user interface.

## Setup

### Convert PyQt UI File to Python
To convert the PyQt UI file to a Python file, use the following command:
```bash
pyuic5 -x [FILENAME].ui -o [FILENAME].py
```

### Create Executable Using PyInstaller
To create an executable, run PyInstaller with the following command:
```bash
pyinstaller --windowed Muse_FB-Page_Multi-Post.py --paths ./utils
```

## Demo

### Step 1: Home Page
This is the home page of the application:
<img src="https://github.com/neural022/Facebook-API-Page-Multi-Post/blob/main/demo_img/home_page.png" width="632" height="521">

### Step 2: API Token Setting
Set up your API token to start using the application:
<img src="https://github.com/neural022/Facebook-API-Page-Multi-Post/blob/main/demo_img/api_token_setting.png" width="632" height="521">

### Step 3: Post Object Setting
Configure the post object settings for your content:
<img src="https://github.com/neural022/Facebook-API-Page-Multi-Post/blob/main/demo_img/post_object_setting.png" width="632" height="521">

### Step 4: Send Post
Send your post to the selected Facebook Pages:
<img src="https://github.com/neural022/Facebook-API-Page-Multi-Post/blob/main/demo_img/send_post.png" width="632" height="521">

### Step 5: Demo Result
Here’s the result of posting to two different Facebook Pages:
<img src="https://github.com/neural022/Facebook-API-Page-Multi-Post/blob/main/demo_img/post_result1.png" width="600" height="433">
<img src="https://github.com/neural022/Facebook-API-Page-Multi-Post/blob/main/demo_img/post_result2.png" width="570" height="512">
