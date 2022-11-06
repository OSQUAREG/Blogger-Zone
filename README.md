# **THE BLOGGER'S ZONE**

## **Table of Content**

1. Introduction
2. Packages Installed/Used
3. Design/Specifications
4. User Authentication
5. User Authorization
6. User's Dashboard (User Profile and User Articles)
7. 

## 1. Introduction

**Blogger's Zone** is an exam project created and designed by Gregory Ogbemudia, a student of [AltSchool Africa School of Software Engineering](https://thealtschool.com/software-engineering/) in Backend (Python) Engineer, already creating magic using Flask framework!

This documentation sets to introduce and give you details of the design features of the Blogger's Zone.

The **Blooger's Zone** is a blog site where both authors and readers can explore the thoughts and minds of others, while getting inspired to write as well. In this Blog, you enjoy reading, enjoy writing and touch lives.

## 2. Design/Specifications

This Blog have the following pages:

### a) Main (General) Page/Menu

These comprises of Home Page (which lists only publised articles and authors), About Page, Contact Page and View Single Article Page, visible to everyone.

### b) Auth Pages/Menu

These are the Sign Up and Login Pages, only visible when you are not logged in.

### c) User Pages/Menu

These are Dashboard Page, Logout Menu, Create Article Page, Edit Article Page, Update Profile Page, only visible to logged-in users.

## 3. Packages Installed/Used

The main packages that were pip installed are:

* Flask
* Flask-CKEditor
* Flask-Login
* Flask-SQLAlchemy
* Flask-WTF

## 4. User Authentication

Contributors (Authors and Commenters) are required to sign up and login with their account to be able to create, save or publish, edit and delete their articles.

However, Viewers (Readers) can access and view or read articles published on the home page of this Blog, but cannot drop comments or write an article.

**Sign Up Process:**

* Every user must have a first name, last name, username (unique), email (unique) and a password. About Author is optional.

**Login Process:**

* Contributors can either log in using a unique "username" (or a unique "email") and password.

*NOTE: the passwords are hashed before they are saved on the database*

## 5) User Authorization

Below are the authorizations checks put in place

* Only logged users can create, save or publish, edit and delete only their own articles.
* A logged-in user cannot edit or delete other authors publiched articles
* A logged-in user cannot view other authors articles "saved as draft".
* Logged-in users can only edit their user profile.

## 6) User's Dashboard

Logged in users are able to see their dashboard, which comprises of their User Profile and their Articles (published and saved as draft).

On the **User Profile Section**, users have button links to:

* update their profile
* delete their profile

On the User's Article Section, users see only their articles under 2 tabs:

* Published
* Saved As Drafts

## 7) Article Viewing & Commenting

Logged in users are able to view/read and also add comments on a published article.

However, not signed up or logged in viewers can only view comments but cannot add comments.

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
