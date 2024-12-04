Search
======

.. toctree::

To allow quick navigation even in big data sets, the global full-text search
can find entities containing the search term in their name or aliases. The
search is:

* Not case sensitive, so **aDa lovelacE** will find **Ada Lovelace**
* Full text, therefore **da Love** will find **Ada Lovelace**
* Unaccented, **Lovē** will find **Love** and vice-versa
* You can use *%* as a placeholder, so **Ada L%ce** will
  find **Ada Lovelace**

Additionally, an advanced search can be used to filter the results when more
than one option is available:

* **Only entities edited by me** - shows only entities which you have
  created or edited.
* **Also search in description** - searches in description and date comments
* **Classes** - searches only in selected classes, such as place or actor
* **Dates**

  * This filter is only active if at least the **from** or **to** year is
    filled out.
  * If only a year is provide the **from** date will be **YYYY-01-01**,
    the **to** date will be **YYYY-12-31**
  * If only a year and a month is provided it will show data from the first
    to the last day of the month
  * If the option **Include dateless entities** is checked, entities without
    dates will be displayed as well

Because entities can have up to 4 date values (time span for begin and time
span for end) they will be added to the result if at least one date meets the
criteria. Therefore, a person that lived from **1540 to 1590** will be found
when the **from year** value is **1550**.
