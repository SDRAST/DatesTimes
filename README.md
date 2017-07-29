# DatesTimes

Conversions between various date and time formats

## Date and Time Formats

### VSR time tuples

The are of the form
  `(YYYY,DDD,sssss)`
where the latter is seconds since midnight.

### VSR filename time strings

Used in the output files, these are text strings of the form
  `YYYY DDD ssssss`
where the latter is seconds since midnight.

### VSR script time stamps

used in filenames are of the form
  `DDD/HH:MM:SS`

### ISO timestamps

These are of the form
  `YYYYMMDDTHHMMSS` or `YYYY-MM-DDTHH:MM:SS`.

### Python times

take these forms
*  **time.time** float
```
   In [29]: time.time()
   Out[29]: 1501361397.04814
```
*  **time.struct_time**
```
   In [15]: time.gmtime(0)
   Out[15]: time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1,
                               tm_hour=0,    tm_min=0, tm_sec=0,
                               tm_wday=3,    tm_yday=1, tm_isdst=0)
```
*  **datetime.datetime** object
```
   In [16]: datetime.datetime.now()
   Out[16]: datetime.datetime(2017, 7, 29, 13, 31, 54, 963632)
```
*  **datetime** timetuple
```
   In [32]: datetime.datetime(2, 1, 1, 0, 0, 0, 0).timetuple()
   Out[32]: time.struct_time(tm_year=2, tm_mon=1, tm_mday=1,
                               tm_hour=0, tm_min=0, tm_sec=0,
                               tm_wday=1, tm_yday=1, tm_isdst=-1)
```
*  **datetime** ordinal
```
   In [24]: datetime.datetime.toordinal(datetime.datetime(1, 1, 31, 0, 0, 0, 0))
   Out[24]: 31
```
*  **matplotlib datenum** float
```
   In [36]: matplotlib.dates.num2date(1)
   Out[36]: datetime.datetime(1, 1, 1, 0, 0,
                        tzinfo=<matplotlib.dates._UTC object at 0x7f66371f6550>)
```
In converting strings, this module converts a 2-digit year as nearest 4-digit
year.
```
   In [55]: num2date(matplotlib.dates.datestr2num("Jan 1 99 00:00:00"))
   Out[55]: datetime.datetime(1999, 1, 1, 0, 0,
                        tzinfo=<matplotlib.dates._UTC object at 0x7f66371f6550>)
```

### UNIX (System) Time

Number of seconds since `1970/01/01 00:00:00 UT`. Example
```
 In [10]: time.gmtime(0)
 Out[10]: time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1,
                          tm_hour=0, tm_min=0, tm_sec=0,
                          tm_wday=3, tm_yday=1, tm_isdst=0)
```

### Julian Date and Modified Julian Date

Julian Date is number of days since `-4713:11:24 12:00:00 UT`.
```
 In [11]: julian_date(-4713,328.5)
 Out[11]: 0.0
 In [12]: calendar_date(-4713,328)
 Out[12]: (-4713, 11, 24)
 ```

Modified Julian Date is

 - Julian date - 2400000.5
 - number of days since 1858/11/17 00:00:00 UT.
 - 40587 + unixtime/(24*60*60)

```
Example::
 In [13]: julian_date(1858,day_of_year(1858,11,17))
 Out[13]: 2400000.5
 In [14]: MJD(1858,11,17)
 Out[14]: 0
 In [15]: MJD(1970,1,1)
 Out[15]: 40587
```

## IAU position based names

These take the forms::
  `Jhhmm+ddmm`, `Bhhmm+ddmm` and `Gddd.d+dd.d`

## Classes

Subclass `UTC(datetime.tzinfo)` defines UTC.

## Functions

### ISO times

Methods to convert to and from ISO times
```
  format_ISO_time(year,doy,timestr)
  ISOtime2datetime(ISOtime)
```

### UNIX Timestamp

```
  datetime_to_UnixTime(t)
  macro_log_time_to_UnixTime(year,timestr)
  UnixTime_to_datetime(UnixTimeStamp)
  UnixTime_to_MPL(UnixTimeStamp)
  MPLtime_to_UnixTime(MPLtime)
  timestamp_to_str_with_ms(TS)
```
### VSR Times

To and from various VSR time formats
```
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
```

### Time strings

Various functions to convert to and from time strings
```
  DDDMM_to_dec_deg(DDDMM)
  HHMM_to_timetuple(time_string)
  HHMM_to_dec_deg(HHMM)
  HHMMSS_to_seconds(string)
  make_date_string(date_tuple)
  timetuple_to_HHMM(time)
  YYYYDDD_datecode(year, midfix, doy)
```

### Date Conversions
```
  calendar_date(year, doy)
  julian_date (year, doy)
  MJD_to_UnixTime(MJD)
  day_of_year (year, month, day)
```

### Miscellaneous

Various useful functions
```
  day_of_week(doy, year)
  leap_year (year)
  deg_to_IAU_str(position,format="h")
  week_number(year,doy)
  format_now()
  now_string()
  get_current_week()
  get_date()
  
  logtime_to_timetuple(time_string)
  mpldate2doy(mpldate)
  parse_date(ses_date)
  time_int_to_decimal(time)
  timetuple_to_datetime(timetuple)
```