:orphan:

Date
====

.. toctree::

CIDOC based OpenAtlas shortcuts: OA8 (begins in) and OA9 (ends in)

Date input fields in forms are initially hidden and can be shown after
clicking on the **Show** button next to the **Date** label.

To manage uncertainty in time up to four dates can be used: a time span for the
beginning with start and end date as well as and a time span for the end,
also with a beginning and end date. Find detailed examples here:
:doc:`/examples/time_spans`

.. image:: date.png

**Exact date**

If you know the exact birth of an actor you could enter
**1356-12-23** in the first row of the date field.

**Time span**

If you are unsure when e.g. a Church was destroyed, you can use both end
dates to enter a timespan. Chose a wide enough range to make sure the event
lies in between those dates with 100% certainty. So, to record a date within
the fist decade of 1800, enter:
* **1800** into the first end row of the date field
* **1809** into the second end row of the date field

Days and months are filled in automatically if not stated by you. The result
will therefor be **1800-01-01** to **1809-12-31**.

**Autocomplete dates**

If a date but not an exact date was entered into the form, the system
automatically creates a **time span**. For example, if only a year is
entered in the first row, a timespan of this year will be saved.
For example:

* **800** will generate: **800-1-1** to **800-12-31**.
* **800-5** will generate **800-5-1** to **800-5-31**

**Input values**

* **Year**: -4713 to 9999 but not zero
* **Month**: 1 to 12
* **Day**: 1 to 31
* **Comment**: add additional information for begin or end

Additional fields for hour, minute and second appear if the time module is
activated in the :doc:`/tools/profile` or if that information was already
entered for that entity:

Possible values:

* **Hour**: 0 to 23
* **Minute**: 0 to 59
* **Second**: 0 to 59

**Background**

Dates will be validated so you can just try if you aren't sure about a leap
year or similar. Most limitations come from the database
`PostgreSQL <https://www.postgresql.org/>`_ which in turn uses the
`Proleptic Gregorian calendar <https://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar>`_.
So there is no year zero (one year before year 1 is the year 1 BC) and dates
before the year 4713 BC can not be recorded.
