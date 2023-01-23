# Flask_Y - Hacker News v2.0

Redesigned Hacker News
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/hacker_new_redesign.PNG)

Original Hacker News
![](https://github.com/mnguyen0226/flask_y/blob/main/docs/hacker_news_original.PNG)

## Inspiration
Y Combinator is an awesome venture capital and I love their investment in start-ups that solve real world problems. Their infamous Hacker News is a centralize hub for students to get insight about the start-up world and even find jobs! However, their Hacker News site is not very well design and eye-pleasing, thus I want to use my skill to solve this mini problem.

Flask-Y means that the app is the redesigning version of Y Combinator's Hacker News using Flask.

## What it does
Flask-Y is designed to be user friendly, similar to how Reddit design their user-friendly page. Here are the list of features from the client and admin side:

Client (User) can:
- Sign Up / Logout / Sign Out / Delete (their) account.
- View / Upvote / Downvote / Create posts.
- View other user's profile.
- Comment on / Delete (their) comments or comments on their posts.
- Edit Personal Page including personal info and images.
- Search for posts.

Admin can:
- Do all Client's abilities.
- Can Delete users / comments.
- Can Delete / Edit posts.

## How I built it

![](https://github.com/mnguyen0226/flask_y/blob/main/docs/MVC_model.png)

This project has been built with a lot of consideration for better user experience and Python, using:
- Flask.
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

## Accomplished App Features




