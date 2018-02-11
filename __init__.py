# -*- coding: utf-8 -*-
"""Supporting functions for Date and Time

Date and Time Formats
=====================
VSR time tuples
---------------
The are of the form::
  (YYYY,DDD,sssss)
where the latter is seconds since midnight.
  
VSR filename time strings
-------------------------
Used in the output files, these are text strings of the form::
  'YYYY DDD ssssss'
where the latter is seconds since midnight.
  
VSR script time stamps
----------------------
used in filenames are of the form::
  DDD/HH:MM:SS
  
ISO timestamps
--------------
These are of the form::
  YYYYMMDDTHHMMSS or 
  YYYY-MM-DDTHH:MM:SS.
We've extended this to include::
  YYYY-DDDTHH:MM(:SS) and 
  YYYYDDDTHHMM.

Python times
------------
take these forms::
  datetime.datetime object
     datetime.datetime(2015, 12, 19, 10, 29, 29, 198776)
  time.time (float)
     1450729528.987735
  time.struct_time
     time.struct_time(tm_year=2015, tm_mon=12, tm_mday=21,
                      tm_hour=20, m_min=23, tm_sec=18, 
                      tm_wday=0, tm_yday=355, tm_isdst=0)
  datetime ordinal (int)
     735951
  matplotlib datetime (float)
     735953.5172106482

UNIX (System) Time
------------------
Number of seconds since 1970/01/01 00:00:00 UT. Example::
 In [10]: time.gmtime(0)
 Out[10]: time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1,
                          tm_hour=0, tm_min=0, tm_sec=0,
                          tm_wday=3, tm_yday=1, tm_isdst=0)

Julian Date and Modified Julian Date
------------------------------------
Julian Date is number of days since -4713:11:24 12:00:00 UT
Example::
 In [11]: julian_date(-4713,328.5)
 Out[11]: 0.0
 In [12]: calendar_date(-4713,328)
 Out[12]: (-4713, 11, 24)

Modified Julian Date is::
 - Julian date - 2400000.5
 - number of days since 1858/11/17 00:00:00 UT.
 - 40587 + unixtime/(24*60*60)
 
Example::
 In [13]: julian_date(1858,day_of_year(1858,11,17))
 Out[13]: 2400000.5
 In [14]: MJD(1858,11,17)
 Out[14]: 0
 In [15]: MJD(1970,1,1)
 Out[15]: 40587

IAU position based names
========================
These take the forms::
  Jhhmm+ddmm, Bhhmm+ddmm and Gddd.d+dd.d

Methods
=======
ISO times
---------
Methods to convert to and from ISO times::
  format_ISO_time(year,doy,timestr)
  ISOtime2datetime(ISOtime):

VSR Times
---------
To and from various VSR time formats::
  incr_VSR_timestamp(timestr)  incr_VSR_timestring(timestr)
  make_VSR_timestring()
  VSR_to_datetime(VSR_time_tuple)
  VSR_to_timetuple(VSR_tuple)
  VSR_timestring_to_ISOtime(timestr)  
  VSR_script_time(doy,h,m,s)  
  VSR_script_time_to_timestamp(year,string)  
  VSR_tuple_to_MPL(year,doy,seconds)  
  VSR_tuple_to_datetime(year,doy,start_sec)  
  VSR_tuple_to_timestamp(year,doy,start_sec)
  VSR_timestamp()

Time strings
------------
Various functions to convert to and from time strings::
  DDDMM_to_dec_deg(DDDMM)
  HHMM_to_timetuple(time_string)
  HHMM_to_dec_deg(HHMM)
  HHMMSS_to_seconds(string)
  make_date_string(date_tuple)
  timetuple_to_HHMM(time)
  YYYYDDD_datecode(year, midfix, doy)

Miscellaneous
-------------
Various useful functions::
  datetime_to_UnixTime(t)
  deg_to_IAU_str(position,format="h")
  format_now()
  get_current_week()
  get_date()
  logtime_to_timetuple(time_string)
  macro_log_time_to_UnixTime(year,timestr)
  mpldate2doy(mpldate)
  MPLtime_to_UnixTime(MPLtime)
  now_string()
  parse_date(ses_date)
  seconds(timedelta)
  time_int_to_decimal(time)
  timestamp_to_str_with_ms(TS)
  timetuple_to_datetime(timetuple)
  UnixTime_to_datetime(UnixTimeStamp)
  UnixTime_to_MPL(UnixTimeStamp)
  week_number(year,doy)
  MJD_to_UnixTime(MJD)
"""
import calendar
import datetime as DT
from math import pi
import re
from sys import argv
import time as T

from pylab import date2num, num2date, ndarray

import logging

logger = logging.getLogger(__name__)

sec_per_day = 24.*60*60
hr_to_rad = pi/12.
deg_to_rad = pi/180.

# ------------------------ time zone classes -----------------------------

class UTC(DT.tzinfo):
  """
  This subclass of tzinfo defines UTC
  """
  def utcoffset(self,dt):
    return DT.timedelta(hours=0,minutes=0)

  def tzname(self,dt):
    return "UTC"

  def dst(self,dt):
    return DT.timedelta(0)

class ST(DT.tzinfo):
  """This subclass of tzinfo defines standard time in the current timezone"""
  def tzname(self,dt):
    return "ST"

  def dst(self,dt):
    return DT.timedelta(0)

utc = UTC()

# general conversions

def calendar_date(year, doy):
  """Calendar date from day of year

  @param year : int

  @param doy : int
    day of year

  @return: tuple of ints
    (year, month, day)
  """
  if doy < 32:
    month = 1
    day = doy
  elif doy < 60 + leap_year(year):
    month = 2
    day = doy - 31
  else:
    if leap_year(year) == 0:
      doy += 1
    month = int((doy+31.39)/30.61)
    day = doy + 2 - (month-1)*30-int((month+1)*0.61)
  return year,month,day

def day_of_week (doy, year):
  """
  Numeric value for the day of week

  @param doy : int
    Day of year

  @param year : int

  @return: int
  1 - sunday,
  2 - monday,
  3 - tuesday,
  4 - wednesday,
  5 - thursday,
  6 - friday,
  7 - saturday,
  """
  day = julian_date( year, (doy + 0.5) ) + 2
  return int((day - 7 * (int(day - 1) / 7)))

def julian_date (year, doy):
  """
  Julian date

  Notes
  =====
  On the Julian calendar; Julian Days are used by astromoners to
  avoid the complexities of the various calendars.

  @param year : int

  @param doy : int
    Day of year

  @return: float
    Julian Day (J.D) = number of days since noon on Jan. 1, 4713 BC
  """
  prev_year = year - 1
  century = prev_year / 100
  num_leaps = int(prev_year / 4) - century + int(century / 4)
  jd = 1721425. + 365. * prev_year + num_leaps - 0.5 + doy
  return (jd)

def day_of_year (year, month, day):
  """
  Day of year

  @param year : int

  @param month : int

  @param day : int

  @return: int
    the day of the year where Jan. 1 is DOY 1
  """
  day = day + (month -1) * 30. + (int)((month + 1) * 0.61) - 2
  if (month <= 2):
    day = day + month
  else:
    if (leap_year(year) != 1):
      day = day - 1
  return (int(day))

def leap_year (year):
  """
  Leap year

  @param year : int

  @return: int
    1 if year is leap year, otherwise 0
  """
  if (year % 100 == 0 ): # Gregorian fix
    if (year % 400 == 0 ):
      return (1)
    else:
      return (0)
  else:
    if (year % 4 == 0 ):
      return (1)
    else:
      return (0)

# --------------- conversion between Python representations -----------------------

def ISOtime2datetime(ISOtime):
    """
    Converts an ISO string to a datetime object
    
    Acceptable input formats are::
      YYYY-MM-DDTHH:MM:SS,
      YYYY-DDDTHH:MM(:SS),
      YYYYMMDDTHHMMSS,
      YYYYDDDTHHMM and
      YYYY-MM-DD HH:MM:SS

    @param ISOtime : time in one of the above formats
    @type  ISOtime : str

    @return: datetime object
    """
    if re.search("T",ISOtime):
      if re.search(":",ISOtime):
        if re.search("-",ISOtime):
          if ISOtime.index('T') == 10:
            if len(ISOtime) == 19:
              # case YYYY-MM-DDTHH:MM:SS
              return DT.datetime.strptime(ISOtime,'%Y-%m-%dT%H:%M:%S')
            elif len(ISOtime) == 16:
              # case YYYY-MM-DDTHH:MM
              return DT.datetime.strptime(ISOtime,'%Y-%m-%dT%H:%M')
          elif ISOtime.index('T') == 8:
            # case YYYY-DDDTHH:MM(:SS)
            if len(ISOtime) == 14:
              return DT.datetime.strptime(ISOtime,'%Y-%jT%H:%M')
            elif len(ISOtime) == 17:
              return DT.datetime.strptime(ISOtime,'%Y-%jT%H:%M:%S')
            else:
              return None
      elif ISOtime.index('T') == 8:
        # case YYYYMMDDTHHMMSS
        return DT.datetime.strptime(ISOtime,'%Y%m%dT%H%M%S')
      elif ISOtime.index('T') == 7:
        # case YYYYDDDTHHMM(SS)
        if len(ISOtime) == 12:
          return DT.datetime.strptime(ISOtime,'%Y%jT%H%M')
        elif len(ISOtime) == 14:
          return DT.datetime.strptime(ISOtime,'%Y%jT%H%M%S')          
        else:
          return DT.datetime.strptime(ISOtime,'%Y%jT%H%M%S.%f')
      else:
        return None
    else:
      if re.search('\.',ISOtime):
        # YYYY-MM-DD HH:MM:SS.sss
        return DT.datetime.strptime(ISOtime, "%Y-%m-%d %H:%M:%S.%f")
      else:
        # YYYY-MM-DD HH:MM:SS
        return DT.datetime.strptime(ISOtime, "%Y-%m-%d %H:%M:%S")

def timestamp_to_str_with_ms(TS):
  """Converts a UNIX time.time float to a date time string with
  milliseconds."""
  string = str(DT.datetime.fromtimestamp(TS))
  if string.find('.') != -1:
    return string[:-3]
  else:
    return string + ".000"

def UnixTime_to_datetime(UnixTimeStamp):
  """Converts a UNIX time stamp to a Python datetime object"""
  return DT.datetime.fromtimestamp(UnixTimeStamp, tz=UTC())

def datetime_to_UnixTime(t):
  """
  Converts a Python datetime object to a UNIX timestamp.
  
  Since t is a datetime object considered to be in the timezone of the
  user, the dst flag is changed to prevent dst conversion.
  """
  return calendar.timegm(t.utctimetuple())

def timetuple_to_datetime(timetuple):
  """
  Converts a timetuple (y,mo,d,h,mi,s) to a datetime object.
  
  To convert a datetime object to a timetuple, simply invoke the object's
  timetuple() method.
  """
  if len(timetuple) < 6:
    return DT.datetime(*timetuple)
  else:
    return DT.datetime(*timetuple[:6])

def UnixTime_to_MPL(UnixTime):
  """
  Converts a UNIX time stamp (seconds since the epoch) to matplotlib date/time.
  """
  # date2num works on datetime objects
  if type(UnixTime) == list or type(UnixTime) == ndarray:
    response = []
    for item in UnixTime:
      response.append(date2num(DT.datetime.fromtimestamp(item, tz=UTC())))
    return response
  else:
    return date2num(DT.datetime.fromtimestamp(UnixTime, tz=UTC()))

def MPLtime_to_UnixTime(MPLtime):
  """
  Converts an MPL time to a UNIX time stamp
  """
  # num2date returns a datetime object
  logger.debug("MPLtime_to_UnixTime entered with %s", MPLtime)
  if type(MPLtime) == list or type(MPLtime) == ndarray:
    response = []
    for item in MPLtime:
      response.append(datetime_to_UnixTime(num2date(item), tz=UTC()))
  else:
    response = datetime_to_UnixTime(num2date(MPLtime, tz=UTC()))
  logger.debug("MPLtime_to_UnixTime returned\n%s", response)
  return response
 
# conversions to and from VSR representations

def make_VSR_timestring():
  """
  Creates a time string for the current time in the format that
  the VSR uses: 'YYYY DDD SSSSS'.
  """
  T = DT.datetime.utcnow()
  secs = T.hour*3600 + T.minute*60 + T.second - 1
  return T.strftime("%Y %j ")+("%5d" % secs)
  
def incr_VSR_timestring(timestr):
  """
  Increments a VSR timestamp.  It does not handle
  the midnight transition.
  """
  year,day,sec = timestr.split()
  newsec = int(sec)+1
  return year +' '+ day + (" %5d" % newsec)

def VSR_to_datetime(VSR_time_tuple):
  """
  Converts a VSR time tuple to a datetime object. Example::
  >>> DateTime.VSR_to_datetime((2010,15,16212))
  >>> datetime.datetime(2010, 1, 15, 4, 30, 12)
  To create a VSR time tuple from a string use VSR_to_timetuple
  """
  (year,doy,seconds) = VSR_time_tuple
  hrs = int(seconds)/3600
  mins = (int(seconds)-3600*hrs)/60
  secs = int(seconds) -3600*hrs - 60*mins
  t = calendar_date(year,doy)+(hrs,)+(mins,)+(secs,)
  return DT.datetime(*t)

def VSR_to_timetuple(VSR_tuple):
  """Converts a VSR time tuple to a Python time tuple.  Example
  In [1]: VSR_to_timetuple((2010,101,12345))
  Out[1]: (2010, 4, 11, 3, 25, 45, 6, 101, -1)"""
  t = VSR_to_datetime(VSR_tuple)
  return t.timetuple()
  
def VSR_timestring_to_ISOtime(timestr):
  """Formats a VSR time string as YYYYMMDDTHHMMSS. Example:
  In [2]: VSR_tuple_to_ISOtime((2010,101,12345))
  Out[2]: '20100411T032545'"""
  t = VSR_to_datetime(timestr)
  return t.strftime("%Y%m%dT%H%M%S")

def VSR_script_time(doy,h,m,s):
  """This creates a timestamp such as VSR script files use. Example:
  In [3]: VSR_script_time(101,3,25,45)
  Out[3]: '101/03:25:45'"""
  return ("%03d" % doy)+'/'+("%02d" % h)+':'+("%02d" % m)+':'+("%02d" % s)

def VSR_script_time_to_timestamp(year,string):
  """
  Converts a VSR time string like 123/12:34:45 to a UNIX time stamp.
  
  Note that 'mktime' returns a local time from a UT timetuple
  """
  doystr,timestr = string.split('/')
  h,m,s = timestr.split(':')
  y,mn,d = calendar_date(year,int(doystr))
  t = DT.datetime(y,mn,d,int(h),int(m),int(s))
  return calendar.timegm(t.timetuple())

def WVSR_script_time_to_timestamp(yrdoystr,timestr):
  """
  Converts a VSR time string like 16/237 08:45:01 to a UNIX time stamp.
  
  Note that 'mktime' returns a local time (not UT) from a UT timetuple
  """
  yr, doy = yrdoystr.split('/')
  year = 2000 + int(yr)
  DOY = int(doy)
  h,m,s = timestr.split(':')
  y,mn,d = calendar_date(year, DOY)
  t = DT.datetime(y, mn, d, int(h), int(m), int(s))
  return calendar.timegm(t.timetuple())

def macro_log_time_to_UnixTime(year,timestr):
  """
  Given a time string DDD_HH:MM:SS it returns the UNIX timestamp
  """
  vsr_str = timestr.replace("_","/")
  UnixTime = VSR_script_time_to_timestamp(year,vsr_str)
  return UnixTime

def VSR_tuple_to_MPL(year,doy,seconds):
  """Converts a VSR time tuple to a matplotlib date/time float."""
  yr,mn,dy = calendar_date(year,doy)
  # UT at midnight in matplotlib format
  UT0 = date2num(DT.datetime(yr,mn,dy))
  time = UT0 + seconds/sec_per_day
  return time

def VSR_tuple_to_datetime(year,doy,start_sec):
  """
  Converts VSR time specification toa datetime object.
  """
  mpl_time = VSR_tuple_to_MPL(year,doy,start_sec)
  return num2date(mpl_time)

def VSR_tuple_to_timestamp(year,doy,start_sec):
  """
  Converts a VSR time specification to a UNIX time stamp.
  """
  yr,mn,dy = calendar_date(year,doy)
  # UT at midnight as a UNIX timestamp
  DT0 = DT.datetime(yr,mn,dy)
  UT0 = T.mktime(DT0.timetuple())
  return UT0 + start_sec

def VSR_timestamp():
  """
  Alias for make_VSR_timestring, for backwards compatibility
  """
  return make_VSR_timestring()
  
def incr_VSR_timestamp(timestr):
  """Alias for inc_VSR_timestring for backwards compatibility"""
  return incr_VSR_timestring(timestr)

# conversion to anf from other DSN formats

def HHMM_to_timetuple(time_string):
  """This converts a time string of the form used in DSN schedules (HHMM) to
  a time tuple (h,m)."""
  t = T.strptime(time_string,"%H%M")
  return t.tm_hour, t.tm_min

def logtime_to_timetuple(time_string):
  """This converts a time string of the form used in EAC and RAC logs
  (HH:MM:SS) to a time tuple (h,m,s)."""
  t = T.strptime(time_string,"%H:%M:%S")
  return t.tm_hour, t.tm_min, t.tm_sec

def timetuple_to_HHMM(time):
  """Converts a time in time() format, seconds since the epoch, to an
  HHMM string."""
  h,m = T.localtime(time)[3:5]
  return "%02d%02d" % (h,m)

def YYYYDDD_datecode(year, midfix, doy):
  """
  Format the datecode pattern used in many log files.
  
  The results consists of a year and doy separated by a string. 'year' is
  assumed to be a four digit integer but a two digit one should work.
  'doy' does NOT have leading zeros, that is, it's a normal integer.
  
  @param year : four digit year
  @type  year : int

  @param midfix :
  @type  midfix : str
  
  @param doy : day of year without leading zero(s)
  @type  doy : int

  @return: str
"""
  return str(year)+midfix+("%03d" % doy)

# other utilities

def week_number(year,doy):
  """
  Computes the week number given the year and day of year.

  This assumes the week begins on Sunday (weekday 1).

  @param year :
  @type  year : int

  @param doy :
  @type  doy : int

  @return: int
  """
  # This is the week day on which the year starts.  This week belongs to the
  # previous year
  weekday1 = day_of_week(1,year)
  #print "Day of week for DOY 001 =",weekday1
  if doy <= weekday1:
    # This day belongs to the previous year
    return 52
  else:
    first_doy_of_week_2 =  8 - (weekday1-1) % 7
    #print "First DOY of week 2 =",first_doy_of_week_2
    weeks_to_doy = 1 + (doy - first_doy_of_week_2)/7
    #print "Weeks to current DOY =",weeks_to_doy
    return weeks_to_doy

def make_date_string(date_tuple):
  """Accepts a date tuple (year,month,day) and returns a formatted
  string of the form YYYY-MM-DD."""
  year,month,day = date_tuple
  return "%4d-%02d-%02d" % (year,month,day)

def parse_date(ses_date):
  """This parses a date string of the form YYYY-MM-DD and returns
  the string, year, month, day and day of year."""
  [yr,mn,dy] = ses_date.split('-')
  year = int(yr)
  month = int(mn)
  day = int(dy[:2]) # strip of any a or b
  DOY = day_of_year(year,month,day)
  return ses_date,year,month,day,DOY

def get_date():
  """This gets a date string of the form YYY-MM-DD from the command line or
  requests it from the user.  It returns the string, and the year, month,
  day and day of year."""
  L = len(argv)
  if L > 1 and argv[0] == 'python':
    ses_date = argv[1]
  elif L == 2 and argv[0][-3:] == '.py':
    ses_date = argv[1]
  elif L > 2 and argv[1] == '-pylab':
    ses_date = argv[2]
  else:
    ses_date = raw_input("Enter session date (YYYY-MM-DD): ")
  ses_date,year,month,day,DOY = parse_date(ses_date)
  return ses_date,year,month,day,DOY

def HHMM_to_dec_deg(HHMM):
  """Converts a string HHMM to decimal hours."""
  return 15*(int(HHMM[0:2])+float(HHMM[2:4])/60.)

def DDDMM_to_dec_deg(DDDMM):
  """Converts a strin DDDMM to decimal degrees."""
  sign = int(self.DDDMM[0]+'1')
  return sign * (int(self.DDDMM[1:3]) + float(self.DDDMM[3:5])/60.)

def deg_to_IAU_str(position,format="h"):
  """The position is a longitude-like, latitude-like tuple.  The first
  coordinate and be in hours or degrees but it must be > 0.  The second
  coordinate can be negative.  The output will be of thhe form
  hhmm+ddmm if format= 'h' (default), dddmm+ddmm if format='d', or
  ddd.d+dd.d if format='g'."""
  if format.lower() == "g":
    ra_str = "%05.1f" % position[0]
    dec_str = "%+05.1f" % position[1]
  else:
    longitude = position[0]
    latitude = position[1]
    ra_hh  = int(longitude)
    # The IAU convention is to truncate, not to round
    ra_mm  = int(60*(longitude-ra_hh))
    if format.lower() == "d":
      ra_str = "%03d%02d" % (ra_hh,ra_mm)
    else:
      ra_str = "%02d%02d" % (ra_hh,ra_mm)
    sign = int(latitude/abs(latitude))
    dec_dd = int(abs(latitude))
    dec_mm = int(60*(abs(latitude)-dec_dd))
    dec_str = "%+03d%02d" % (sign*dec_dd,dec_mm)
  return ra_str+dec_str

def HHMMSS_to_seconds(string):
  """Converts a colon-separated time string (HH:MM:SS) to seconds since
  midnight"""
  (hhs,mms,sss) = string.split(':')
  return (int(hhs)*60 + int(mms))*60 + int(sss)

def time_int_to_decimal(time):
  """Takes a number of the form HHMMSS or +/-DDMMSS and converts it
  to a decimal."""
  if time[0] == "-":
    sign = -1
    timestr = time[1:]
  elif time[0] == "+":
    sign = 1
    timestr = time[1:]
  else:
    sign = 1
    timestr = time
  index = timestr.find('.')
  if index > -1:
    seconds_fraction = timestr[index:]
    timestr = timestr[:index]
  else:
    seconds_fraction = ".0"
  # We expect six digits but it could be less so work from the back
  hh = int(timestr[-6:-4])
  mm = int(timestr[-4:-2])
  ss = float(timestr[-2:]+seconds_fraction)
  return sign*hh+mm/60.+ss/3600.

def now_string():
  """
  Current minute formatted as YYYY/DDD-HHMM
  """
  now = T.gmtime(T.time())
  return "%40d/%03d-%02d%02d" % (now[0],now[7],now[3],now[4])

def format_now():
  """
  Return the current time as a formatted string:
  """
  return T.ctime(T.time())

def format_ISO_time(year,doy,timestr):
  """
  Format an ISO-like time string: YYYY-DDDTHH:MM

  @param year : 4-digit year
  @type  year : str

  @param doy : 3-digit day of year
  @type  doy : str

  @param timestr : HHMM
  @type  timestr : str

  @return: str
  """
  return year + '-' + doy + 'T' + timestr[0:2] + ':' + timestr[2:4]
  
def get_current_week():
  year,daytime = now_string().strip().split('/')
  doy,timestr = daytime.split('-')
  return week_number(int(year),int(doy)),int(year)

def mpldate2doy(mpldate):
  """
  get day of year from matplotlib date number

  @param mpldate : date and time
  @type  mpldate : matplotlib datenum

  @return: int
  """
  dt = num2date(mpldate, tz=UTC())
  return day_of_year(dt.year, dt.month, dt.day)

def MJD_to_UnixTime(MJD):
  """
  Converts MJD time to UNIX time

  @param MJD : modified Julian date with fractional day
  @type  MJD : float

  @return: float
  """
  return (MJD-40587)*sec_per_day

def UnixTime_to_MJD(UnixTime):
  """
  Convert UnixTime to fractional MJD

  @param UnixTime : seconds since 1970/01/01 00:00:00 UT
  @type  UnixTime : float

  @return: float
  """
  return 40587+UnixTime/sec_per_day

def MJD(*args):
  """
  Returns modified Julian date from UNIX time or (year,doy) or (year,month,day)
  """
  if len(args) == 1:
    # assume UNIX time stamp
    unixtime = args[0]
    return 40587 + unixtime/(24*60*60)
  elif len(args) == 2:
    # assume year and day-of-year
    year, doy = args
    return julian_date(year,doy) - 2400000.5
  elif len(args) == 3:
    # assume calendar date
    year, month, day = args
    doy = day_of_year(year, month, day)
    return julian_date(year,doy) - 2400000.5
  else:
    raise RuntimeError, "MJD requires 1, 2, or 3 arguments"

def seconds(timedelta, unit="sec"):
  """
  Computes the length of a datetime interval to specified units
  
  @param timedelta : difference between two datetime values
  @type  timedelta : datetime.timedelta instance
  
  @param unit : "sec" or "min" or "day"
  @type  unit : str
  
  @return: float
  """
  days = timedelta.days
  secs = timedelta.seconds
  if unit == "sec":
    return days*24*3600 + secs
  elif unit == "min":
    return days*24*60 + secs/60.
  else:
    return days*24 + secs/3600.

