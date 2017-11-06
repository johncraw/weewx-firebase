# weewx-firebase

This is a weewx extension to upload web files to a Firebase instance.

Uploads the weewx files to a static site hosted on Firebase. Inspired
by Bill Madill's S3upload extension.

This has been tested against weewx 3.7.1 and Firebase 3.14.0

## Setup

For Debian 8 running on a BeagleBone

Install a current version of nodejs from deb.nodesource, not the
default package manager repository

```
curl -sL https://deb.nodesource.com/setup_8.x | bash
apt-get install nodejs
apt-get install build-essential
```

Get a Firebase static site, install the Firebase CLI and init the local app

```
npm install -g firebase-tools --unsafe-perms
mkdir -p /srv/weewx/build
cd /srv/weewx
firebase init
```

Clone this repo; e.g. to your home directory

```
cd ~
git clone https://github.com/johncraw/weewx-firebase.git
```

## Installation instructions

1. run the installer

  ```
  wee_extension --install ~/weewx-firebase/
  ```

2. copy to the deployment directory:

  ```
  cp -p deploy.js /srv/weewx
  ```

3. (re)start weewx:

  ```
  systemctl stop weewx
  systemctl start weewx
  ```

## Manual installation instructions:

1. copy to the weewx user directory:

  ```
  cp -rp skins/firebase /etc/weewx/skins
  cp -rp bin/user/firebase /usr/share/weewx/user
  ```

2. copy to the deployment directory:

  ```
  cp -p deploy.js /srv/weewx
  ```

3. add the following to weewx.conf

  ```
  [StdReport]
      ...
      [[firebase]]
          skin = firebase
  ```

4. (re)start weewx:

  ```
  systemctl stop weewx
  systemctl start weewx
  ```
