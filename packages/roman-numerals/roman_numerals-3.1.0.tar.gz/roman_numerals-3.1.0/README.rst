===============
 roman-numerals
===============

A library for manipulating well-formed Roman numerals.

Integers between 1 and 3,999 (inclusive) are supported.
Numbers beyond this range will return an ``OutOfRangeError``.

The classical system of roman numerals requires that
the same character may not appear more than thrice consecutively,
meaning that 'MMMCMXCIX' (3,999) is the largest well-formed Roman numeral.
The smallest is 'I' (1), as there is no symbol for zero in Roman numerals.

Both upper- and lower-case formatting of roman numerals are supported,
and likewise for parsing strings,
although the entire string must be of the same case.
Numerals that do not adhere to the classical form are rejected
with an ``InvalidRomanNumeralError``.

Example usage
=============

Creating a roman numeral
------------------------

.. code-block:: python

   from roman_numerals import RomanNumeral

   num = RomanNumeral(16)
   assert str(num) == 'XVI'

   num = RomanNumeral.from_string("XVI")
   assert int(num) == 16


Convert a roman numeral to a string
-----------------------------------

.. code-block:: python

   from roman_numerals import RomanNumeral

   num = RomanNumeral(16)
   assert str(num) == 'XVI'
   assert num.to_uppercase() == 'XVI'
   assert num.to_lowercase() == 'xvi'
   assert repr(num) == 'RomanNumeral(16)'


Extract the decimal value of a roman numeral
--------------------------------------------

.. code-block:: python

   from roman_numerals import RomanNumeral

   num = RomanNumeral(42)
   assert int(num) == 42


Invalid input
-------------

.. code-block:: python

   from roman_numerals import RomanNumeral, InvalidRomanNumeralError

   num = RomanNumeral.from_string("Spam!")  # raises InvalidRomanNumeralError
   num = RomanNumeral.from_string("CLL")  # raises InvalidRomanNumeralError
   num = RomanNumeral(0)  # raises OutOfRangeError
   num = RomanNumeral(4_000)  # raises OutOfRangeError


Licence
=======

This project is licenced under the terms of either the Zero-Clause BSD licence
or the CC0 1.0 Universal licence.
See `LICENCE.rst`__ for the full text of both licences.

__ ./LICENCE.rst
