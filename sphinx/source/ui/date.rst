:orphan:

Date
====

.. toctree::

CIDOC based OpenAtlas shortcuts: OA8 (begins in) and OA9 (ends in)

Date input fields in forms are initially hidden and can be shown after
clicking on the **Show** button next to the **Date** label.

To manage uncertainty in time up to four dates can be used: a time span for the
beginning with start and end date as well as a time span for the end,
also with a beginning and end date. To capture specific historical contexts,
you are also allowed to enter standalone **to/end** dates (the second or
fourth row) without the corresponding **from/start** dates. Find detailed
examples here: :doc:`/examples/time_spans`

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

If a date is not entered as an exact date (e.g., only a year or a year and
month is entered), the system autocompletes the missing parts for that specific
date:

* For **start dates** (first and third row), the earliest possible date is used:
  * **800** in a start row will generate: **800-01-01**
  * **800-05** in a start row will generate: **800-05-01**
* For **end dates** (second and fourth row), the latest possible date is used:
  * **800** in an end row will generate: **800-12-31**
  * **800-05** in an end row will generate: **800-05-31**

Entering a partial date in a start row no longer
automatically creates a timespan across both fields. For instance, entering
**800** in the first row only generates a single start date of **800-01-01**,
leaving the second row empty unless it is explicitly filled out.

**Standalone End/To Dates and Historical Semantics**

Often, historical sources provide information about the latest possible time an
event occurred or was initiated, but leave the earliest limit completely
unknown. OpenAtlas allows entering standalone **end/to** dates (the second or
fourth row) without specifying the corresponding **start/from** dates.

This is particularly useful to capture specific historical contexts accurately:

* **Begin To (without Begin From):** If a historical charter mentions that a
  church was already consecrated on a specific date, we know with
  certainty that the church existed *by* this date at the latest. It most likely
  existed before, but we don't know how long before. In this case, we only
  enter the **Begin To** date (the second row).
* **End To (without End From):** If a traveler's itinerary mentions that a
  church did not exist anymore when they visited, we know that its end
  (destruction or abandonment) occurred *by* this date at the latest. However,
  we do not know when the process of its destruction or abandonment started. In
  this case, we only enter the **End To** date (the fourth row).

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
