import os
from multiprocessing import cpu_count
#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.

bind = '127.0.0.1:5000'

#
# Worker processes
#
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#
#       A positive integer generally in the 1+2 x $(NUM_CORES)
#       range for prod and 2 for dev.
#
#   worker_class - The type of workers to use. The default
#       sync class should handle most 'normal' types of work
#       loads.
#
#   keepalive - The number of seconds to wait for the next request
#       on a Keep-Alive HTTP connection.
#
#       A positive integer. Generally set in the 1-5 seconds range.

if os.getenv("FLASK_ENV") == "DEV":
    workers = 2
else:
    workers = cpu_count() * 2 + 1

worker_class = 'sync'

keepalive = 2

#
#   Logging
#
#   logfile - The path to a log file to write to.
#
#       A path string. "-" means log to stdout.
#
#   loglevel - The granularity of log output
#
#       A string of "debug", "info", "warning", "error", "critical"
#

errorlog = '/home/deploy/logs/error.log'

# Log level set to debug for dev deployment and warning for prod
if os.getenv("FLASK_ENV") == "DEV":
    loglevel = 'debug'
else:
    loglevel = 'warning'

accesslog = '/home/deploy/logs/access.log'

access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" "%({X-WWW-USER-TOKEN}i)s"  %(s)s %(b)s "%(f)s" "%(a)s"'
