Versions
--------

This doubles as a changelog and a planning document; past versions have key changes and the date and
time of the version release listed, future versions have my plans for what I want to get done. Those
are just plans, though, and can change at any time.

0.1: Minimal State - done 2020-03-23 10:44

  + Displayed a simple HTML Webpage
  + Did initial planning

0.2: Sketched Out - done 2020-03-23 17:04

  + SQLite database created with the needed schema
  + Filler content made for all main webpages

0.3: Skills System - done 2020-03-23 19:50

  + Be able to create skills as needed.
  + Be able to create a plaintext blog post and 'tag' it with a skill so that the skill appears
    under the relevant skills feed.

0.4: Content Added - done 2020-03-27 09:24

  + Replaced filler content with real (minimal) content (esp. Home, About, and Contact pages)

0.5: Styling - done 2020-03-27 18:51

  + Simple (but decent-looking) SASS styling everywhere
  + Research frameworks for when better styling is implemented (probablly Material or Bootstrap)
    + We've got a winner! [Foundation](https://get.foundation/) is like Bootsrap but faster and more
      versatile

0.6.0: Build CLI Tool and use Alchemy - done 2020-04-01 10:30

  + Create django-style manage.py
  + Switch over to SQLAlchemy

0.6.1: Refactor - done 2020-04-01 11:20

  + Break each page into its own file
  + Break templates into separate subdirectories
  + Reorganize 'blueprints' and urls
  + Clean up testing code

0.6.2: Auth and Controls - done 2020-04-02 09:52

  + Build a user authentication system
  + Lock the skills setup behind that system
  + Make the skill management less evil
  + Add basic contact form

0.7.0: Basic Frameworks - done 2020-04-03 09:24

  + Setup NPM to work with flask
  + Use webpack to deliver script ("bundle.js")

0.7.1: Missed???

0.7.2: Javascript - done 2020-04-03 19:06

  + Setup typescript to work with flask
  + Setup react.js to work with flask

0.7.3: Style Framework - done 2020-04-07 11:06

  + Setup foundation to work with flask

0.8.0: More Database - done 2020-04-07 17:02

  + Add migrations support

0.9.0: Prehosting - done 2020-04-08 12:19

  + Dockerize

0.9.1: Security - done 2020-04-08 17:33

  + Extract private information into environment vars
  + Careful security check, go through a checklist

0.9.2: Documentation - done 2020-04-09 16:35

  + Document everything carefully

0.9.3: Production Setup - done 2020-04-13 18:39

  + Create production-ready dockerfile
    + With nginx and gunicorn

0.9.4: Production Database - done 2020-04-16 09:39

  + Add support for postgresql backend (and generally, for modular db backends)

0.9.5: Deploy Production

  + Deploy to AWS
  + Fix a bunch of errors
  + Reorganize some documentation

1.0: Hosting and Public Release

  + Fix all the dumb little bugs and typos (yes, they are there, read closely)
