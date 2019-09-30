# pygoa_gemini
A simple python library for working with the [Gemini Observatory Archive (GOA) APIs](https://archive.gemini.edu/help/api.html)

## Installation
The scripts require a standard python distribution that includes 
the requests package. This is compatible with both Python 2.7 and Python 3.6+.

Then install the library by downloading and unpacking the zip
file or use git,

    git clone https://github.com/bryanmiller/pygoa_gemini.git

or pip

    pip install pygoa-gemini

## Authentication

In order to download prioprietary data you must provide the GOA authentication
cookie from a web browser.  Updated instructions for how to find the cookie are
given below.

First login to https://archive.gemini.edu with your archive account. Associate your account
to programs with proprietary data using the program key provided to the PI. See the GOA
[help page](https://archive.gemini.edu/help/index.html) for more details.

Safari
1) Go to Preferences - Advanced and turn on "Show Develop menu in menu bar".
2) Click "Show Web Inspector" in the Develop menu.
3) Select Cookies in the Storage tab. The cookie you need is called gemini_archive_session.

Firefox
1) Select Tools->Web Developer->Storage Inspector.
2) Click on "Cookies" and select "https://archive.gemini.edu".
   The cookie you need is called gemini_archive_session.

Chrome
1) Select View->Developer->Developer Tools.
2) Click on "Cookies" and select "https://archive.gemini.edu".
   The cookie you need is called gemini_archive_session.

Copy the value of the cookie and store it in a hidden file called <path>/.goa_auth.
By default get_goa_authority assumes that this is in the home directory, but the path (keydir)
can be specified.
