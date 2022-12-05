#
#    Copyright (c) 2015 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""Upload the generated HTML files to a Firebase app
"""

import errno
import glob
import os.path
import re
import subprocess
import sys
import syslog
import threading
import time
import traceback

import configobj

from weeutil.weeutil import timestamp_to_string, option_as_list
# from weewx.reportengine import ReportGenerator
import weewx.manager

# Inherit from the base class ReportGenerator
class FirebaseUploadGenerator(weewx.reportengine.ReportGenerator):
    """Custom service to upload files to an Firebase instance"""

    def run(self):
        syslog.syslog(syslog.LOG_INFO, """reportengine: FirebaseUploadGenerator""")

        try:
            # Get the options from the configuration dictionary.
            # Raise an exception if a required option is missing.
            html_root = self.config_dict['StdReport']['HTML_ROOT']
            self.local_root = os.path.join(self.config_dict['WEEWX_ROOT'], html_root) + "/"
            syslog.syslog(syslog.LOG_INFO, "FirebaseUpload: deploying from '%s'" % (self.local_root)) 
        except KeyError as e:
            syslog.syslog(syslog.LOG_INFO, "FirebaseUpload: no upload configured. %s" % e)

        syslog.syslog(syslog.LOG_DEBUG, "FirebaseUpload: uploading")

        # Launch in a separate thread so it doesn't block the main LOOP thread:
        t  = threading.Thread(target=FirebaseUploadGenerator.uploadFiles, args=(self, ))
        t.start()
        syslog.syslog(syslog.LOG_DEBUG, "FirebaseUpload: finished upload thread")

    def uploadFiles(self):
        start_ts = time.time()
        t_str = timestamp_to_string(start_ts)
        syslog.syslog(syslog.LOG_INFO, "FirebaseUpload: start upload at %s" % t_str)
        cmd = ["firebase"]
        cmd.extend(["deploy"])
        syslog.syslog(syslog.LOG_DEBUG, "FirebaseUpload command: %s" % cmd)
        try:
            FirebaseUpload_cmd = subprocess.Popen(cmd, cwd= self.local_root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout = FirebaseUpload_cmd.communicate()[0]
            stroutput = stdout.strip()
        except OSError as e:
            if e.errno == errno.ENOENT:
                syslog.syslog(syslog.LOG_ERR, "FirebaseUpload: can't deploy. (errno %d, \"%s\")" % (e.errno, e.strerror))
            raise
        
        if weewx.debug == 1:
            syslog.syslog(syslog.LOG_DEBUG, "FirebaseUpload: deploy output: %s" % stroutput)

        if FirebaseUpload_cmd.returncode == 0:
            syslog.syslog(syslog.LOG_INFO, "FirebaseUpload: site was deployed")
        else:
            syslog.syslog(syslog.LOG_INFO, "FirebaseUpload: can't deploy")
            for line in iter(stroutput.splitlines()):
                syslog.syslog(syslog.LOG_INFO, "FirebaseUpload: error: %s" % line)
        
        stop_ts = time.time()
        syslog.syslog(syslog.LOG_INFO, "FirebaseUpload: executed in %0.2f seconds" % (stop_ts - start_ts))

        t_str = timestamp_to_string(stop_ts)
        syslog.syslog(syslog.LOG_INFO, "FirebaseUpload: end upload at %s" % t_str)

if __name__ == '__main__':
    """This section is used for testing the code. """
    # Note that this fails!
    import sys
    import configobj
    from optparse import OptionParser


    usage_string ="""Usage: 
    
    FirebaseUpload.py config_path 
    
    Arguments:
    
      config_path: Path to weewx.conf"""

    parser = OptionParser(usage=usage_string)
    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        sys.stderr.write("Missing argument(s).\n")
        sys.stderr.write(parser.parse_args(["--help"]))
        exit()
        
    config_path = args[0]
    
    weewx.debug = 1
    
    try :
        config_dict = configobj.ConfigObj(config_path, file_error=True)
    except IOError:
        print("Unable to open configuration file ", config_path)
        exit()
        
    if 'FirebaseUpload' not in config_dict:
        print >>sys.stderr, "No [FirebaseUpload] section in the configuration file %s" % config_path
        exit(1)
    
    engine = None
    FirebaseUpload = engine.uploadFiles(config_dict)
    
    rec = {'extraTemp1': 1.0,
           'outTemp'   : 38.2,
           'dateTime'  : int(time.time())}

    event = weewx.Event(weewx.NEW_ARCHIVE_RECORD, record=rec)
    FirebaseUpload.newArchiveRecord(event)
    
