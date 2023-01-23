# Flask_Y - Hacker News v2.0

Redesigned Hacker News
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/hacker_new_redesign.PNG)

Original Hacker News
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/hacker_news_original.PNG)

## Inspiration
Y Combinator is an awesome venture capital and I love their investment in start-ups that solve real world problems. Their infamous Hacker News is a centralize hub for students to get insight about the start-up world and even find jobs! However, their Hacker News site is not very well design and eye-pleasing, thus I want to use my skill to solve this mini problem.

Flask-Y means that the app is the redesigning version of Y Combinator's Hacker News using Flask.

## Accomplished app features
Flask-Y is designed to be user friendly, similar to how Reddit design their user-friendly page. Here are the list of features from the client and admin side:

Client (User) can:
- [Sign Up / Logout / Sign Out / Delete (their) account](https://drive.google.com/file/d/1VZXQNsctVqs6bY6i7bWxUSaZcMfhzpe-/view?usp=sharing).
- [View / Upvote / Downvote / Create posts](https://drive.google.com/file/d/1lnuhxXBFmIAwjqAM2rtAZOQy9Vp4M5Wa/view?usp=sharing).
- [View other user's profile](https://drive.google.com/file/d/1MtNb7Q6Y5EgdMOj0MW2Y2XZmridyNTok/view?usp=sharing).
- [Comment on / Delete (their) comments or comments on their posts](https://drive.google.com/file/d/1ZR0bhqZOrHnKppoVQrykOgrKFSMssJdr/view?usp=sharing).
- [Edit Personal dashboard including personal info and images](https://drive.google.com/file/d/1y9CmBSpNHAZE_lHqPTdrAepxGAXZAQHT/view?usp=sharing).
- [Search for posts](https://drive.google.com/file/d/13f7mXUEFZgme9CMEzK5SSCrLsKh1C-AX/view?usp=sharing).
- [Delete user will delete all info related to that user](https://drive.google.com/file/d/1ev3YW5h_r_8ym2flTFPyNzbRcW7q_bW2/view?usp=sharing).

Admin can:
- Do all Client's abilities.
- [Can Delete users / comments](https://drive.google.com/file/d/1mu3d4rR9z9k-2zKVbEZGiz8R1nuTIlRL/view?usp=sharing).
- [Can Delete / Edit posts](https://drive.google.com/file/d/1jNX7R922HVAohdix9zytc9r86Sx3cSCE/view?usp=sharing).

## How I built it

![](https://github.com/mnguyen0226/flask_y/blob/main/docs/MVC_model.png)

This project has been built with a lot of consideration for better user experience and Python, using:
- Flask API.
- Bootstrap Component.
- CkEditor API (rich text).
- Werkzeug API (password hashed).
- MySQL.

## Challenges
Implement one-to-many relationship in database.

Posts voting and ranking features.

Upload avatar from local feature and save to database.

Follow the 4 principles in web design: Contrast, Repetition, Alignment, Proximity from ["The Non-Designer's Design Book"](https://www.amazon.com/Williams-Non-Designers-Design-Bk_p3-Designers/dp/0321534042).

## Getting start
1. Install MySQL and create a MySQL Connection to local root. Unlike SQLite, You won't have access to my database.

2. Environmental Setup
```bash
python3 -m pip install -r requirements.txt
```

3. Connect and create database
```bash
python ./src/create_db.py
```

4. Run
```bash
flask app.py
```

## Pages

Home Page
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/home_page.PNG)

News Page
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/new_page.PNG)

Sign Up Page
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/sign_up_page.PNG)

Login Page
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/login_page.PNG)

User Dashboard
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/dashboard_page.PNG)

Create New Post Page
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/create_post_page.PNG)

View Post Page
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/view_post_page.PNG)

Search Page
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/search_page.PNG)

View User Page
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/view_user_page.PNG)

Admin Page
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/admin_page.PNG)

Customize Error Page
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/customized_error_page.PNG)
