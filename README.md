# Read-me
## By Arafat Arman, Kangming Deng, Andy Li
### (Everything our Team Accomplished)

## Important
In order to run this system, your computer must have the following requirements:
	- Django 2.1.2 or later installed
	- Python 3.6 or later installed
If you meet the above requirements follow these steps to run the system:
	- open terminal
	- activate a Python environment with Django installed
	- change directory to DSS folder
	- run the following command
```$ python manage.py runserver```
	- Click the URL that shows up after the server is running (http://127.0.0.1:8000/)
	- To exit and quit the server, press CONTROL-C

# Document Sharing System (DSS)
The DSS is a system that allows users to create, edit, and share documents. To use the DSS, one must sign up for an account. Once logged in, the user has many available functionalities, depending on their user status.

The main functionalities of the DSS are as follows:
 - Document creation and maintenance
 - Message system
 - Account/User management

### Document Creation and Maintenance
The core functionality of the DSS, the document managing is as follows:
 - Only Ordinary Users (OU) and Super Users (SU) can create documents and put a public, private, shared, or restricted privacy level.
 - **Public**: everyone can see
 - **Private**: only creator of document can see and edit
 - **Shared**: only OUs and SUs can edit, if they are invited to by the creator of the document. Contributing users can be kicked off the document by the creator of the document given valid reasons. Furthermore, shared documents can be locked and updated by a contributing OU and get an assigned version number. Once unlocked, old versions of the document can be retrieved and viewed.
 - **Restricted**: can only be viewed as read-only by Guest Users (GU) and edited by OUs
 - The document itself supports multiple words per line, word formatting, and even images (provided a link). Every document displays the creator and the number of times someone viewed the document.
 - Any word that belongs to the **Taboo List** (list of banned words) will be censored.
 - Users that insert taboo words into a document and save it, will be locked out of their account until they revert their changes. When their account is locked out, all features and functionalities of the DSS is blocked exclusively for them.

### Message System
In order to improve communication between users, the DSS provides a message system. The message system can be used to:
 - send taboo word suggestions to an SU
 - file any kind of complaint
 - invite users to work on a shared document
A user can keep track of his or her sent messages, and messages in his or her inbox.

### Account/User Management
 - Users have the ability to manage their account by clicking the ‘Home’ tab.
 - Users can add a profile picture and list their interests by updating their account settings
 - Depending on their status, more functionalities are available: If a user is a GU, they have the ability to fill out an application to get their user status promoted to an OU, and send it to an SU. If a user is an SU, they can manage all membership applications, and manage the taboo list.
 - All user pages show the 3 most recent documents they worked on. If they are a GU, it shows the 3 most popular documents currently on the site (based on view count)
 - Users can also search other registered DSS users by clicking the ‘Users’ tab
 - Viewing other users’ page shows their stats and 3 most recent documents
 - If an SU is viewing another user’s page, he or she can manage their user status, i.e promote/demote users based on valid reasons.

⚠️ Disclaimer: The DSS was developed and released with no apparent bugs (to our knowledge). If you happen to encounter a bug or a functionality that does not work properly, please report it and we will fix it to the best of our abilities.
