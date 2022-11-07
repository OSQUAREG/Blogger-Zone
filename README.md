# **THE BLOGGER'S ZONE**

## **Table of Content**

1. Introduction
2. Packages Installed/Used
3. Design/Specifications
4. User Authentication
5. User Authorization
6. User's Dashboard (User Profile and User Articles)
7. Article Viewing & Commenting

## 1. Introduction

**Blogger's Zone** is an exam project created and designed by [Gregory Ogbemudia](https://github.com/OSQUAREG), a student of [AltSchool Africa School of Software Engineering](https://thealtschool.com/software-engineering/) in Backend (Python) Engineer, already creating magic using Flask framework!

This documentation sets to introduce and give you details of the design features of the Blogger's Zone.

The **Blooger's Zone** is a blog site where both authors and readers can explore the thoughts and minds of others, while getting inspired to write as well. In this Blog, you enjoy reading, enjoy writing and touch lives.

## 2. Design/Specifications

This Blog have the following pages:

### A) Main (General) Page/Menu

These comprises of Home Page (which lists only publised articles and authors), About Page, Contact Page and View Single Article Page, visible to everyone.

#### i) Home Page

* This page has button links to Sign-Up or Login (when not logged in) but has button links to " "create articles" and "view your dashboard".
* It has list of only published articles and authors.

#### ii) About Page

* This page tells about the creator and the blog.
* In addition, it has the list of authors and their email.

Contact Page

### B) Auth Pages/Menu

These are the Sign Up and Login Pages, only visible when you are not logged in.

### C) User Pages/Menu

These are pages and menus only logged users have access to. They include the Dashboard Page, Logout Menu, Create Article Page, Edit Article Page, Update Profile Page.

## 3. Packages Installed/Used

The main packages that were pip installed are:

* Flask
* Flask-CKEditor
* Flask-Login
* Flask-SQLAlchemy
* Flask-WTF

## 4. User Authentication

### A) Authentication Category

There are 2 main category of access to this Blog:

#### i) Contributors

These consists of **Authors** and **Commenters** are required to sign up and login with their account to be able to create, save or publish, edit and delete their articles.

#### ii) Viewers/Readers

However, **Viewers/Readers** can only view or read articles only published articles on the Home Page of this Blog. They can also view comments but cannot drop comments or write an article.

### B) Authentication Processes

#### i) Sign Up Process:

* Every user must have a first name, last name, username (unique), email (unique) and a password to sign up using the Sign-Up Page to become a contributor. Also, 'About Author' field is optional.

#### ii) Login Process:

* Every contributor can either log in using a unique "username" (or a unique "email") and password.

*NOTE: the passwords are hashed before they are saved on the database*

## 5) User Authorization

Below are various implemented authorizations level on this Blog:

### A) Articles

#### i) Creating, Saving and Publishing Articles

Only contributors can create and either "save as draft" or publish articles on this blog. Saved articles can only be accessed by their authors and then, can still edit or publish them.

#### ii) Viewing/Reading Articles

All contributors and viewers can view/read all publised articles on the Home Page.

#### iii) Editing and Deleting Articles

Only the author of an article can edit or delete the article, either saved or published.

#### iv) Viewing and Adding Comments

All can view comments by others but only contributors can add comments to an article.

### B) Users

#### i) User Dashboard

Only logged in users can see their own dashboard, which has 2 sections namely; Your Profile and Your Articles (published and saved as draft).

###### a. Your Profile section

Here, only logged-in users have button links to:

* update their profile
* delete their profile
* log out of their session

###### b. Your Article section

Logged-in users only see their articles, which are displayed under 2 separate tabs:

* Published
* Saved As Draft

Here, they also have buttons links to either create, view, edit, delete their articles.

## 8) Screenshots Samples

#### a) Home Page

![1667776361483](image/README/1667776361483.png)

#### b) Home Page (Logged in User)

![1667776487192](image/README/1667776487192.png)

#### c) Sign Up Page

![1667776537079](image/README/1667776537079.png)

#### d) Login Page

![1667776581548](image/README/1667776581548.png)

#### e) About Page

![1667776664064](image/README/1667776664064.png)

#### f) Contact Page

![1667776700613](image/README/1667776700613.png)

#### g) Single Article View Page (with Comments)

![1667776810435](image/README/1667776810435.png)

#### h) User Dashboard

![1667777051620](image/README/1667777051620.png)

#### i) User Article List on Dashboard

![1667777402378](image/README/1667777402378.png)

#### j) Creat Article Page

![1667777440625](image/README/1667777440625.png)

#### k) Update Profile

![1667777499545](image/README/1667777499545.png)
