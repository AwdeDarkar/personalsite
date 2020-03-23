Ben Croisdale's Personal Website
================================

I have made many websites before, but strangely never the personal website that many web developers
create for their own use. Even my private metacortex site does not have my name anywhere on it and
it is not intended for public viewing aside (for the most part).

However, I have decided to transition to freelance software development. For this, a personal
homepage is not an idle curiosity but an active necessity. The code for this site and many of my
skill-focused personal projects will be available on my github.

General Design
--------------

I imagine this site to serve as a kind of fusion blog and technical showcase. I've seen many
developers simply display their work, but I've always been much more personally impressed by the
ones who can talk about it. Being able to see into the mind of a skilled developer at work is
enlightening, and also materially useful for those seeking to learn.

### Layout

The site will have the following sections

#### Home
For now, this will be pretty minimal, probably just a very short blurb about myself and my interest
in software development, and links to other stuff. At some point it could be fun to toss in some
sort of little javascript toy/game here. Also, it should have a picture of myself soon, so people
know I actually exist and am not a vague abstraction of code and words.

#### Skills
This will be a directory of what I'm going to call "skill feeds"; each skill feed will focus on an
individual skill I want to showcase professionally. That feed will be a mixture of project
showcases, blog posts, and other miscellania relevant to the skill in question. Internally, the
'skills' will be treated as tags that can be added to a 'project' or 'post' object.

#### Predictions
I want to keep a list of public predictions here, update them and score them regularly. This is a
habit I'm pushing hard and I think it will help me stand out in a crowd of smart developers who are
nonetheless confused about their own confusion.

#### About
This will be a more detailed personal description; it should go over some public facts about my
life, some of my personality, and bits of my philosophy.

#### Contact
I'll list various methods of getting into contact with me, including my professional email, social
media accounts, and a form for contacting me though the site itself (probably just dump sanitized
text input directly to my database for now).

Versions
--------

These are my plans for the website versions and a log of past changes:

0.1: Minimal State - done 2020-03-23 10:44

  + Displayed a simple HTML Webpage
  + Did initial planning

0.2: Sketched Out - done 2020-03-23 17:04

  + SQLite database created with the needed schema
  + Filler content made for all main webpages

0.3: Skills System

  + Be able to create and delete skills as needed.
  + Be able to create a plaintext blog post and 'tag' it with a skill so that the skill appears
    under the relevant skills feed.

0.4: Content Added

  + Replace filler content with real content (esp. Home, About, and Contact pages)

0.5: Styling

  + Simple (but decent-looking) SASS styling everywhere
  + Research frameworks for when better styling is implemented (probablly Material or Bootstrap)

1.0: Hosting and Public Release

  + Fix all the dumb little bugs and typos (yes, they are there, read closely)
  + Dockerize
  + Host on metis or frene for now, start planning for move to AWS
