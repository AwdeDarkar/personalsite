Gears-Level Description of the Site
===================================

This is my attempt at conferring a [gears-level
understanding](https://www.lesswrong.com/posts/B7P97C27rvHPz3s9B/gears-in-understanding) in written
text. This is, of course, impossible. The only way to actually get that level of understanding is by
reading and comprehending the code itself (not only the code in _this_ repo, mind, but also the code
for every dependency, and probably also the code for every tool being used in the environment and
maybe the underlying hardware as well...). But hopefully this can be a helpful reference anyway
(especially to myself in a few months time).

Production Environment
----------------------

Web development is a game of boxes inside boxes, and my current deployment environment is no
exception. Going from the inside-out, the relevant things are

  0. Website code, written in [Flask](https://flask.palletsprojects.com/en/1.1.x/)
  1. [Gunicorn](https://gunicorn.org/), serving the flask code through the <wsgi.py> file.
  2. [Nginx](https://www.nginx.com/), routing outside traffic to gunicorn and
     serving the static files (both `/static` and `/node`)
  3. [Docker](https://www.docker.com/), containing everything above this.
  4. Another Nginx, which reverse-proxies outside traffic to the docker container where the nginx
     _inside_ that container can handle it. This nginx also handles my SSL cert, which is signed by
     [letsencrypt](https://letsencrypt.org/).
  5. [EC2 t2.micro instance](https://aws.amazon.com/ec2/instance-types/) which hosts the whole
     thing.
  6. [Elastic IP Address](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) to
     keep things with the DNS simple.
  7. [Google Domains](https://domains.google/) to get the DNS to resolve my URL to the right IP
     address.

Obviously the networking process continues on from there, but that's everything I have access to.
Also, inside the EC2 instance I have [another docker container](https://hub.docker.com/_/postgres)
which runs my [PostgreSQL](https://www.postgresql.org/) database. I plan to move this either to its
own instance or to an AWS or other third-party managed instance soon.

Deployment Process
------------------

TODO
