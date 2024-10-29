Execute SQL
=====================

.. toctree::

Admins can execute SQL direct to the database.

**Warning**: direct database manipulation can result in data loss and an
unusable application!

Preparation
-----------
* Backup the database (:doc:`export`) and download it in case you lose data
  or crash the application
* Create a local database with the backup and test the SQL on the local
  version first
* **Note**: If no recent backup is available (max. one day old), the SQL
  function is not available either.

Keep in mind
------------
* This is a simple but powerful feature; unlike the rest of the
  application there are no safeguards to prevent total data loss and/or
  making the application unusable.
* If data is lost and/or the application crashes it can **only** be fixed
  by a person with server and database access. So depending on the situation
  this might take some time and effort.
* A transaction (BEGIN, COMMIT) is automatically build around your statement.
* Don't refresh the page (e.g pressing F5) as this will execute the
  statement again.
* You can use multiple statements (every statement has to be terminated with
  ";") but only the result of the last one will be displayed.

Result
------
After clicking on **Execute** the result of the last query is shown below
depending on the statement:

* **SELECT** - the row count and the (not very readable) query result
* **INSERT, UPDATE, DELETE** - the affected row count
* **Error** - there is nothing to worry about because the transaction
  executes the statement(s) only if there is no error
