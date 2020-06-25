DatesTimes
==========

Conversions between various date and time formats
-------------------------------------------------

This module originally contained the time conversion and formatting routines from the 
FORTRAN program `DOPSET <https://library.nrao.edu/public/memos/comp/CDIR_8.pdf>`_ of Dick 
Manchester and Mark Gordon, subsequently augmented with some from program 
`coco <http://www.starlink.ac.uk/docs/starlinksummary.html>`_ from the Starlink 
software collection. Time formats used by DSN Science data files were also added, as
well as convenience routines.  The time formats converted include

  * UNIX time
  * ``matplotlib`` date numbers
  * Python ``datetime`` objects
  * Julian date and modified Julian date
  * formats used by the DSN VLBI Science Recorder series data file
  * miscellaneous other time strings
  
.. image:: python-times.png

The project `website <https://github.com/SDRAST/DatesTimes/>`_ 
contains the  Git repository from which the package can be cloned.

Software `documentation <https://sdrast.github.io/DatesTimes/>`_
is generated with Sphinx.

