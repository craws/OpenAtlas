FAQ
===

.. toctree::

Here you can find answers to some frequently asked questions.

**Why is it not possible to add custom types with a free text entry field
the same way it is possible with numbers for value types?**

Tag: design decision

A free text entry field would lead to lots of unstructured data.
Unstructured data can not be processed automatically and would result in it
not being presented nor searchable in the OpenAtlas system as well as in a
frontend that presents your data. Therefore, we made the decision, not to
include free text types into the OpenAtlas system. Solutions to this problem
are very case specific, but you could:

* use the already provided description fields to enter any type of free text
  (keep in mind that this also comes with restrictions on how to present this
  data in a frontend)
* create a new tree of project specific types for as many cases as possible
  and structure your data with them – for a step by step tutorial how to
  create new types, click :doc:`here</examples/types>`.

We are more than happy to help you find a solution tailored to your
project’s specific needs, so please don’t hesitate to reach out to us if you
have any additional questions on this topic.

**How can I enter professions into the OpenAtlas system?**

Tag: model

A profession is not entered via a type as a lot of other information you
will put into the database. You can enter a person’s profession by linking
them to a group.
This group consists of people with the same profession. Say you want to
enter our lead developer Alex into the database: create a group named
‘OpenAtlas’ and connect him to that group in the respective form. Here you
can also pick the role he has in that group from a list of types. For a more
detailed tutorial on how to enter professions, have a look
:doc:`here</examples/profession>`.

**Why can't longer texts be formatted?**

Tag: design decision

For formatting longer texts, e.g. entity descriptions, only linebreaks can
be used. The main reason for not implementing formatting systems like HTML or
Markdown for e.g. bold font, underline, lists and similar is that data may
be used by other systems via the :doc:`/technical/api`, and these systems are
not necessarily able to handle these formats.

Another reason is that these formats might change over time. All in all it is
more important for us that acquired data is as interoperable, as long as
possible.

Of course the situation is different for e.g. presentation sites for OpenAtlas
data. There it would be possible to e.g. add manual formatted texts where
needed.
