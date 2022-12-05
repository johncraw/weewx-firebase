# weewx-firebase

This is a weewx extension to upload web files to a Firebase instance.

Uploads the weewx files to a static site hosted on Firebase. Inspired
by Bill Madill's S3upload extension.

This has been tested against weewx 4.9.1 and Firebase 11.16.1

## Setup

For Ubuntu 22.04.1

Install a current version of nodejs from deb.nodesource, not the
default package manager repository

Get a Firebase static site, install the Firebase CLI and init the html root: /var/www/html/

```
cd /var/www/html/
firebase init
```

Clone this repo; e.g. to your home directory

## Installation instructions

1. run the installer

  ```
  wee_extension --install ~/weewx-firebase/
  ```

2. (re)start weewx:

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

2. add the following to weewx.conf

  ```
  [StdReport]
      ...
      [[firebase]]
          skin = firebase
          enable = true
  ```

4. (re)start weewx:

  ```
  systemctl stop weewx
  systemctl start weewx
  ```
