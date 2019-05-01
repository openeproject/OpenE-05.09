# OpenE
OpenE was designed for performing various scientific, mathematical and engineering based calculations and function.

## License
Here's the boring license information
~~~
Copyright 2019 Anthony

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
~~~

## Credits
I just briefly wanted to add some credits here, even though most people won't even bother to look over them.
* Anthony Provenza - (That's me) - So far I've done everything. I'll add others when they contribute  


## Usage
OpenE files are simple to run. If using the non compiled Python code then just use
~~~bash
python opene.py -f file.opene
~~~
If you are using the compiled code (which should be released eventually) then simply use
~~~bash
opene -f file.opene
~~~
If you would like to run OpenE as a command line interface, then use
~~~bash
# Non compiled
python opene.py

# Compiled
opene
~~~

---

## Basics
### Variables
All values that are stored in OpenE are stored as a _variable_.
This is an item that can be referred to later and its value can be retrieved or changed.

There are a few built in variable types. These are explained below:

* `Empty` - An empty variable with no value
* `string` - Contains a value between two double quotes (") (Single quotes are not currently supported)
* `sum` - This is how any numbers or calculations are stored by default.
It is strongly recommended not to use this type when writing a program, but instead use either an `integer` or `float`
* `integer` - This is a whole number, with no decimal point
* `float` - This is a floating point number and contains a decimal. Any integers will end in .0. For example, 1 become 1.0
* `list` - Contains multiple values of any type. Can be any size and it can change later
* `matrix` - Contains rows and columns, similar to a table. Can be any size however the size cannot change later 


_Note:_ There is currently no way to specify new variable types. This is something I plan to add in the future.
### Errors
There are some built in errors in OpenE. They are raised automatically in the code. Below are explanations of them
* `DeveloperError` - This should not be raised in most programs, as (I like to think) that OpenE is rather well tested.
    This is raised when something in the Python code raises in error.
    Don't worry. It's not your fault, but there's also nothing you can do about it
* `ImportError` - This is raised when `@external` or `@require` is used in your code and the file can't be found.
* `SyntaxError` - As the name suggests, this one is raised when the syntax of your program is incorrect,
    such as a character or variable in an incorrect location
* `NameError` - This is raised when a value, such as a function or variable,
    is being referenced but an item with that name can't be found

All the errors are located in the `errors.json` file and can be easily be changed.

### External Modules
There are currently only a few external modules written. These are written in Python.
Documentation on how to write these will be released in the future.

The currently available external modules are
* `core` - Some core functions of the language

To import an external module, such as `core` just use
~~~
@external "~core";
~~~

This will allow you to use functions such as `HelloWorld()` and `test()` in your code.

_Note:_ The tilde _(~)_ at the beginning of the external name states that it is located in the default external directory.
You can also state a location to import from, such as `C:\Users\Me\Desktop\MyModule`.

You can, alternatively, specify an external module to be imported and referenced explicitly only,
such as `core.HelloWorld()` by writing
~~~
@require    explicit    "~core";
~~~ 

By default, all modules are imported implicitly, meaning you can call `HelloWorld()` with the need for the preceding `core.`.
If you would like to make it clear that a module is being imported implicitly,
then you can replace the `explicit` in the previous example with `implicit`
~~~
@require    implicit    "~core";
~~~

_Note:_ The values don't have to be inline, but simply look better, particularly when using multiple
imports/externals and on larger programs

---

## External Modules

### core
This is the core module. It contains some core functions for the language, such as basic input and output.

This is also the first module to be implemented, and contains some testing functions, such as `HelloWorld()` and `test()`
#### Import
~~~
@external   "~core";
~~~
#### Dependencies
~~~
None
~~~

#### HelloWorld
Simply returns the string `"Hello World! - From OpenE"`

_Note:_ This function is primarily for testing and serves no purpose in code
~~~
string x = HelloWorld();
~~~

#### print
Outputs the values given
~~~
print("Hello World! This is a test");
~~~
Multiple values can also be given to be outputted
~~~
string hello = HelloWorld();
print(hello, "This is added to the other string);
~~~

#### input
Gets the user to input a value with a prompt
~~~
string name = input("What is your name? ");
~~~
Multiple values can also be given as a prompt
~~~
string name = input("What is your name? ");
string age = input("How old are you ", name, "? ");
~~~

#### range
Creates a list up to a certain number
~~~
range(start, [stop], [step])
~~~

#### to_matrix
Takes a list and converts it to a matrix, by taking each item in a list and putting it in a matrix

The function takes an existing matrix so that it knows the correct dimension to use.
~~~
to_matrix(existing_matrix, list_of_values) 
~~~

#### to_column
Takes a list and converts it to a column in a matrix
~~~
to_column(existing_matrix, list_of_values, column_number) 
~~~

### stringlib
This module is designed for manipulating strings

#### Import
~~~
@external   "~stringlib";
~~~

#### Dependencies
~~~
None
~~~

#### join
Joins multiple strings together
~~~
join(item_one, item_two, [...])
~~~

#### string_length
Returns an integer with the length of a string
~~~
string_length("Hello World!");
~~~

#### split_string
Splits a string into smaller strings in a list.

Can be split by specific delimiters, otherwise the default values are used
~~~
split_string("This string will be nine items in a list", [delimiters]);
~~~

#### replace_string
Replaces a part of a string with another value

~~~
replace_string(old_string, value_to_replace, value_to_replace_with)
~~~

