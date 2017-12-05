# UCD PS Python Crash Course

This GitHub repository contains materials for a short Python crash course prepared for UC Davis Political Science graduate students. It is designed to be as accessible as possible to students who are familiar with object-oriented programming in R, but not with programming more generally.

Basic familiarity with the command line is assumed.

# Early warning

Google will be your best friend. If you encounter any problems while programming, someone else probably has too. There are many online resources to help you troubleshoot. This is how _all_ programmers (from beginners to pros) solve their problems.

# More training

If you want to pursue programming in more detail, I am always happy to help guide you to the appropriate resources. There are also many great tutorials and online courses. For example, the D-Lab at UC Berkeley has a great bootcamp on Python: [https://github.com/dlab-berkeley/python-fundamentals](https://github.com/dlab-berkeley/python-fundamentals)

I am partial to [Learn Python The Hard Way](https://learnpythonthehardway.org), although it's no longer free...

# Advice

Whether we like it or not, computers are essential to our lives. They are also increasingly essential for our profession. You will be at a comparative advantage if you invest some energy in learning some programming. As you get started, there are some good habits to begin developing:

**Learn more about how computers work.** This is a _great_ little intro to the fundamentals of computing: [https://web.stanford.edu/class/cs101/](https://web.stanford.edu/class/cs101/)

**Get comfortable with the command line.** It may seem weird, but working in the command line can end up being _easier_ than pointing and clicking.

**Always write in plain text.** Get a good text editor (I recommend [Atom](https://atom.io) or [Sublime Text](https://www.sublimetext.com/)), and learn some basic [markdown](https://guides.github.com/features/mastering-markdown/). Use LaTeX for writing papers. [ShareLatex](https://www.sharelatex.com/) is a great collaborative LaTeX environment---it's the Google Drive of LaTeX.

**Keep your files organized and well-named.** Do not use spaces or punctuation in file names, except for underscores and hyphens.

**Always back up.** Use Box, Dropbox or Google Drive to sync your files to the cloud and keep files off your desktop. Familiarize yourself with your obligations to secure data appropriately: [https://cloud.ucdavis.edu/data-guide](https://cloud.ucdavis.edu/data-guide).

**Take security seriously.** I recommend using a password manager, such as OnePass or Dashlane. Always use two-factor authentication if available. At the very least, enable TFA for your primary email address and your main cloud service(s).

**Learn how to use [GitHub](https://github.com).** This is a (somewhat clunky) version management system that is ubiquitous among programmers and data scientists. The earlier you learn it, the better (I speak from experience). It is also a good way to advertise your work to the wider world.

**Be transparent.** If your data is not restricted, then you should _always make your code and your data available for others to replicate without having to ask you_. If your data is restricted, then you should at least make your code available.

**Comment your code.** Always leave helfpul comments in your code and try to follow style guides (such as [this one for Python](https://www.python.org/dev/peps/pep-0008/)).

**Learn about text encoding.** If you plan to work with text in any way, you should learn a little about how text is encoded because it will cause you headaches. First, read [this](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/). Then, read [this](http://farmdev.com/talks/unicode/) and [this](https://docs.python.org/3/howto/unicode.html). Note: on this front, one of the major differences between Python 2 and Python 3 is that strings are now unicode by default Python 3.

# Set up

These instructions work for "typical" macOS installations, but there is no guarantee they'll work on every machine or every OS.

## Python

I recommend you install the Python 3.X version of the [Anaconda python distribution](https://www.anaconda.com/download/).

If you have a Windows machine, be sure to check the option for **Make Anaconda the default Python**.

If you have another installation of Python on your machine and you are comfortable with that, you do not need to install Anaconda. For example, Python comes pre-installed on macOS machines.

I strongly recommend that you install Python 3, although, there is some debate about this.

We will use several Python modules. (These are like libraries in R.) If you are using the Anaconda distribution, you should always try to install these modules via `conda install MODULENAME`.

If you get an error message saying that the package cannot be found, then do this instead: `pip install MODULENAME`.

## Selenium

We will use `selenium` to perform some basic webscraping in a Firefox browser. If you have not installed Firefox, please do so [here](https://www.mozilla.org/en-US/firefox/).

Selenium also requires something called `geckodriver`. You can download it [here](https://github.com/mozilla/geckodriver/releases).

Place the `geckodriver` file in your PATH. If you have installed Anaconda and you are using macOS, you _should_ be able to place the file in `/anaconda/bin` with no trouble. If you encounter problems with the `geckodriver`, this [StackOverflow thread](https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path) may help.

Finally, at your command line, execute `pip install selenium` to install the `selenium` Python module.

## Box SDK

Box offers a set of tools that enable you to interact with your account from within Python. This is called the Box SDK. I will demonstrate how this works.

In order to use the Box SDK, you will need to do the following:

1. Go to [http://developers.box.com](http://developers.box.com).
2. Log in using your UC Davis credentials.
3. Create a new app.
4. Select a custom app, then under "Authentication Method," select **Standard OAuth 2.0**.
5. Open a new plain text file and save it as `boxapp.cfg` in your working directory.
6. On the Box developers site, navigate to your app, go to **Configuration** and copy/paste the **Client ID**, the **Client Secret** on the first two lines of your `boxapp.cfg` file.
7. Select **Generate Developer Token** and paste it into the third line of your `boxapp.cfg` file.

At your command line, execute `pip install boxsdk` to install the `boxsdk` Python module.

For the full instructions, see [Box's Tutorial](http://opensource.box.com/box-python-sdk/tutorials/intro.html).

# Working With Python

Python code is usually saved in a `.py` file, which can be executed in Python from the command line.

You may also use an integrated development environment (IDE) to edit and execute your script. Anaconda comes with an IDE called Spyder, which you can open by typing `spyder` at the command line.

Some people prefer to use a notebook to do their Python scripting. Notebooks contain chunks of code in specific "cells," as well as markdown. When you execute a cell, the output appears in line, below the cell. For Python, the standard is the Jupyter Notebook, which comes with the Anaconda distribution. You can access your notebook menu by typing `jupyter notebook` at the command line. (You will edit notebooks in your default web browser.)

If you are familiar with R and RStudio, Jupyter Notebooks are the Python equivalent of R Notebooks.

For what ever reason, I don't like working with notebooks. I do all my Python scripting in `.py` documents either in an IDE or a text editor.
