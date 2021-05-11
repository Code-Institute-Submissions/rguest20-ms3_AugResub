# **Project FREElance - MS3**

# **Pre-development**

**Functional specifications - Given by Code Institute**
- LO1	Design, develop and implement a back-end for a web application using Python and a micro-framework
- LO2	Demonstrate competence in modeling and managing non-relational data
- LO3	Demonstrate competence in querying and manipulating non-relational data
- LO4	Deploy a full stack web application to a Cloud platform
- LO5	Identify and apply security features

**What this means**
- Build a web application that is powering a non-relational database.
- Ensure UX design is considered throughout, producing a site that is functional and easily navigable
- Create a website using the principles of MVCs using Python as a back end language.
- Deploy correctly and without error to the Heroku platform
- Ensure that secret keys are hidden within the GitHub platform, so that the site is less vulnerable to attack.
- Ensure the website is standard in terms of style.
- Ensure that there is accessibility even for those people who use assistive technology
- Make sure the website responds to different devices.  No point in a website that breaks when viewed on mobile.
- Static website produced using HTML (passing quality check)
- Styled using CSS and bootstrap (passing quality check)
- JavaScript not required, but can be implemented. For example, bootstrap will use JQuery.
- No Lorem ipsum text.
- Ensure this is fully documented and commented to be clear to any developer reading through.

**User stories**

**First Time Users**

- As a first time user (developer), I want to be able to sign up quickly and easily, creating an account that can be seen by agencies.
- As a first time user (developer), I want to be able to search through companies that closely match my profile and see if they have jobs available.
- As a first time user (company), I want to be able to search through the available developers based on several different criteria.
- As a first time user (company/developer), I want assurances that my personal email will not be spammed by unscrupulous users.
- As a first time user sending a message, I want the system to be simple and similar to email, that I am familiar with.

**Hitting these targets**
- Upon entry to the webpage, you are greeted with a call to action to either login or register. This makes it easy to see where to go to sign up.
- The site does not require an email as all messaging can be done through the site itself.  This secures users data and reduces and risk of a GDPR violation.
- The search function quickly allows the user to search the database for Companies, Freelancers or available jobs.  This can be done either by title/name or by programming language/technology stack. This quickly allows the user to find what s/he is looking for.
- In design, the system was built to look similar to email to ensure that users are not presented an interface that looks alien.

**Returning User**
- As a user, I want to be able to check on the progress of my applications sent or received.
- As a user, I want to be able to contact the site admin if there is a problem, or to report suspicious activity.
- As a user, I want to be able to follow up any messages that have been sent to me.
- (extension: As a user, I may want to create coding groups so that I can share hints and tips with my fellow coders)
- (extension: As a user, I may want to view coding groups so that I can wee who is active and may be worth approaching with a job)

**Hitting these targets**
- Upon login, relevant posts are offered to the users based on their chosen languages/tech stack.  This streamlines the search that the user may have to do.  
- There is a contact page that allows users to quickly ask questions of the administration of the site.  This would usually be protected by a ReCaptcha to ensure that the site admin email is not spammed.
- Responses and replies to messages have been built into the messaging system making returning to a previously sent message a breeze.
- There is a visible change for companies when developers respond to a job listing.  This allows them to quickly identify when a response has been made and see if they are interested in the developer.

**Entity Relationships**

There are many interconnected parts of the database.  These have been kept non-relational to abide by the coursework criteria:

![Entity Relationship](static/images/entityrelationship.png "Flowchart")

**Preliminary Designs**
These can be found [here](wireframes.zip "Project Freelance Wireframes")

**Features**

- Responsive on all device sizes
- Database functionality driven
- HTML/CSS/Javascript
- Built in Python (Flask)

# **Post-Development**

To access the page go to your favourite browser and type &quot;[https://ms3-rguest.herokuapp.com/](https://ms3-rguest.herokuapp.com/)&quot; into the search bar. The code is hosted at &quot;[https://github.com/rguest20/MS3](https://github.com/rguest20/MS3)&quot;.

**Dependencies**

**HTML**

I am using HTML 5 and this is shown by the use of the <html> tag used at the start of the document. This comes with all of the semantic markup that I need to ensure that the code is easy to read and debug if necessary.

**CSS/CSS Grid**

To style the page, a mixture of CSS and the newer library CSS Grid was used to keep the site looking neat.  Checks were performed to ensure that, in the event of a browser that did not support grid, the site would look ok.  
Other libraries brought in include:

- Bootstrap CSS (activated via the flask-bootstrap python module)
- Selectize CSS

**JavaScript**

To help with the smooth running and operation of the site, several libraries were used that I have acknowledged in my acknowledgment page.  These are:

- JQuery
- select2.js
- selectize js

**Python**

Python was used as the fundamental language in which the site was built and the following modules were utilized and would be required if rebuilt:

Core flask modules
- flask
- flask-bootstrap
- flask-wtf
- flask-mongoengine
- pymongo
- Flask-Login
- Flask-Admin
- Flask-Redis

Extension modules
- datetime
- dnspython
- python-dotenv (for storing secrets)

- (flask_sqlalchemy and flask_migrate are included in the requirements but is deprecated)

**How to use**

**Home Page**
![Home Page](static/images/home.png "Home Page")
This page is a hub allowing you access to the features of the site.  A basic description is given below along with some taster CTA boxes showing jobs that are available.  Upon login, this page will alter depending on the type of user that is present.  At the head of the page are several links that allow the user to navigate the site.

**Search page**
![Search Page](static/images/search.png "Search Page")
By selecting the tab and the dropdown, you can search either companies, freelancers or job posts.  If searching companies or job posts, a helpful box will give you a list of available names once 3 letters have been typed in.

**Message page**
![Message Page](static/images/messages.png "Message Page")
By selecting the correct tab, you can filter by your sent or recieved messages.  Clicking the buttons on any of these will allow you to continue the conversation or delete the message.

**Account page**
![Account Page](static/images/account.png "Account Page")
These options will help personalise your experience of the site.  Based on the jobs selected and type of user, different content will be presented.
The hourly rate is so users and companies can best match each other and create a competitive market.

**Job page**
![Job Post Page](static/images/jobpost.png "Job Post Page")
![Job Response Page](static/images/jobresponse.png "Job Response Page")
Both of these pages show how jobs are dealt with by the system.  Posts allow companies to show what they are looking for and what they are offering.  The response allows counter offers to be made and allows the freelancer to undercut their competition by offering their services at a lower rate.  

**Profile page**
![Profile Page](static/images/profile.png "Profile Page")
If companies or freelancers wish to know more about each other then they can visit each others profile pages and get a feel for who they may be going into business with.  At a later date, I am looking to add the ability for freelancers to have links to their work so that they can showcase for companies what they are capable of.

**UX design**

To make the design more user friendly I have done the following:

- To ensure that accessibility is not an issue for colorblind people, I have tested the website using the toptal.com colorblind site checker in achromatopsia setting that renders the page in greyscale.  All links and CTAs were still visible.
![Toptal Check](static/images/toptal.png "Toptal Check")
- CTAs and links are made obvious by keeping them in the blue that people expect a link to be in.  Generally, where it looked right, I have also made the text bold to show that it is clickable.
- Colour contrast was checked to ensure readibility
- All buttons are clickable and take you to the expected area of the site.
- Any required form sections will flag if not filled in.

# **Testing**

**W3C Validator**

- HTML
![Screenshot of html test](static/images/html_check.png "HTML Check")
Only one warning shown that cannot be amended as it is set by flask_bootstrap.

- CSS
![Screenshot of css test](static/images/css_check.png "CSS Check")
One error detected in bootstrap module.  No errors in my CSS

**Unit Testing - Database**

![Screenshot of unit test](static/images/unittest.png "Unit Test")
The database was tested to ensure that required functionality was present. All tests pass.

# **Deployment**

**Do Not Deploy To GitHub Pages – Python does not work on GitHub Pages**

**Forking the GitHub Repository**

By forking the GitHub Repository we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original repository by using the following steps...

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/)
2. At the top of the Repository (not top of page) just above the &quot;Settings&quot; Button on the menu, locate the &quot;Fork&quot; Button.
3. You should now have a copy of the original repository in your GitHub account.

**Making a Local Clone**

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/)
2. Under the repository name, click &quot;Clone or download&quot;.
3. To clone the repository using HTTPS, under &quot;Clone with HTTPS&quot;, copy the link.
4. Open Git Bash
5. Change the current working directory to the location where you want the cloned directory to be made.
6. Type git clone, and then paste the URL you copied in Step 3.

$ git clone https://github.com/rguest20/ms2

1. Press Enter. Your local clone will be created.

$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY

\> Cloning into `CI-Clone`...

\> remote: Counting objects: 10, done.

\> remote: Compressing objects: 100% (8/8), done.

\> remove: Total 10 (delta 1), reused 10 (delta 1)

\> Unpacking objects: 100% (10/10), done.

**Heroku Hosted App**

The project was deployed to Heroku using the following steps...

1. Log in to Heroku and create a new app - use the python buildpack
2. Click the deploy bar and check the GitHub Deployment Method
3. locate the [GitHub Repository](https://github.com/)and copy the address of that page into the bar asking for origin
4. This will link to your GitHub account and deploy to the site when changes are detected.
5. Click the Settings bar and add the following Config Vars:
- SECRET_KEY: (this should be a difficult to guess string)
- MONGO_LOGIN: (this should be the url of the mongodb database that you intend to use with the app)
- FLASK_APP: app.py
- FLASK_CONIFG: heroku
6. Check that the build has occurred as expected.
7. Enjoy your shiny new app.

**Credits**

**Code**

- [Bootstrap4](https://getbootstrap.com/docs/4.4/getting-started/introduction/): Bootstrap Library used throughout the project mainly to make site responsive using the Bootstrap Grid System.

- [Flask](https://flask.palletsprojects.com/en/1.1.x/): Lite Framework in which the app was built.

- [Select2](https://select2.org/): Jquery Replacement for select boxes.

- [Jquery](https://jquery.com/): Library to make javascript more readable/funtional.

**Content**

- All content was written by the developer, except for icons taken from FontAwesome

**Media**

- There are media files available in the assets folder that are freely available from google image search (with the option to only show images that are correctly licenced)

**Known issues/extensions to be added**

- Admin area to be added at a later date, allowing refreshing of passwords and removal of troublesome users.
- Links for companies/freelancer on profile page to be added
- Avatars on profile page to be added
