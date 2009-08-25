#!/usr/bin/python

# Copyright (C) 2002,2003 Jonathan Middleton <jjm@ixtab.org.uk>

# This file is part of Logcheck

# Logcheck is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# Logcheck is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Logcheck; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import sys

class Logcheck:

    def __init__(self, conf, logfiles, rulefiles):
        self.conf = conf
        self.logfiles = logfiles
        self.rules = rulefiles

        self.command = "../src/logcheck -o -S ./state/ -c %s -l %s -r %s" % \
                       ( self.conf,
                         self.logfiles,
                         self.rules)

    def Run(self):

        run = os.popen(self.command)

        self.output = run.read()

        run.close()

    def Check(self, expected):
        if self.output == expected:
            return 1
        else:
            return 0

    def Result(self):
        return self.output

class Results:

    def __init__(self, dir):

        read = open(os.path.join(dir, "intro/disabled"))
        self.test1a = read.read()
        read.close()

        read = open(os.path.join(dir, "intro/enabled"))
        self.test1b = read.read()
        read.close()

        read = open(os.path.join(dir, "cracking-ignore/enabled"))
        self.test2a = read.read()
        read.close()

        read = open(os.path.join(dir, "cracking-ignore/disabled"))
        self.test2b = read.read()
        read.close()

        read = open(os.path.join(dir, "violations.ignore.d-local/test"))
        self.test3 = read.read()
        read.close()

        read = open(os.path.join(dir, "intro/disabled"))
        self.test4a = read.read()
        read.close()

        read = open(os.path.join(dir, "intro/yes"))
        self.test4b = read.read()
        read.close()


    def Test1a(self):
        return self.test1a

    def Test1b(self):
        return self.test1b

    def Test2a(self):
        return self.test2a

    def Test2b(self):
        return self.test2b

    def Test3(self):
        return self.test3

    def Test4a(self):
        return self.test4a

    def Test4b(self):
        return self.test4b

expected = Results("./results")

fail = 0

path = os.environ.get("PATH")
os.putenv("PATH", "../src:%s" % path)

# Test Intro (disabled)
print "Testing disabled intro...",

test1a = Logcheck("./conf/intro-disabled",
                  "./logs/intro/files",
                  "rulefiles")

if os.path.isfile("state/offsetlogs.intro.log"):
    os.remove("state/offsetlogs.intro.log")

test1a.Run()

if test1a.Check(expected.Test1a() ):
    print "success"
else:
    print "failed"
    print test1a.Result(),
    fail = 1

# Test 1b - Intro (enabled)
print "Testing enabled intro...",

test1b = Logcheck("../etc/logcheck.conf",
                "./logs/intro/files",
                "rulefiles")

if os.path.isfile("state/offsetlogs.intro.log"):
    os.remove("state/offsetlogs.intro.log")

test1b.Run()

if test1b.Check(expected.Test1b()):
    print "success"
else:
    print "failed"
    print test1b.Result(),
    fail = 1

# Test 2a and 2b still need to be finished.

# Test 2a - cracking ignore support: enabled
print "Testing enabled cracking ignore...",

test2a = Logcheck("./conf/cracking-ignore-enabled",
                "./logs/cracking-ignore/files",
                "rulefiles")

if os.path.isfile("state/offsetlogs.cracking-ignore.log"):
    os.remove("state/offsetlogs.cracking-ignore.log")

test2a.Run()

if test2a.Check(expected.Test2a()):
    print "success"
else:
    print "failed"
    print test2a.Result(),
    fail = 1

# Test 2b - cracking ignore support: disabled
print "Testing disabled cracking ignore...",

test2b = Logcheck("../etc/logcheck.conf",
                "./logs/cracking-ignore/files",
                "rulefiles")

if os.path.isfile("state/offsetlogs.cracking-ignore.log"):
    os.remove("state/offsetlogs.cracking-ignore.log")

test2b.Run()

if test2b.Check(expected.Test2b()):
    print "success"
else:
    print "failed"
    print test2b.Result(),
    fail = 1


# Test 3 - violations.ignore.d/local-*
print "Testing violations.ignore.d/local-*...",

test3 = Logcheck("../etc/logcheck.conf",
                "./logs/violations.ignore.d-local/files",
                "rulefiles")

if os.path.isfile("state/offsetlogs.violations.ignore.d-local.log"):
    os.remove("state/offsetlogs.violations.ignore.d-local.log")

test3.Run()

if test3.Check(expected.Test3()):
    print "success"
else:
    print "failed"
    print test3.Result(),
    fail = 1

# Test 4a - Intro "yes" (disabled)
print "Testing old style disabled intro...",

test4a = Logcheck("./conf/intro-no",
                  "./logs/intro/files",
                  "rulefiles")

if os.path.isfile("state/offsetlogs.intro.log"):
    os.remove("state/offsetlogs.intro.log")

test4a.Run()

if test4a.Check(expected.Test4a() ):
    print "success"
else:
    print "failed"
    print test4a.Result(),
    fail = 1

# Test 4b - Intro "no" (enabled)
print "Testing old style enabled intro...",

test4b = Logcheck("./conf/intro-yes",
                  "./logs/intro/files",
                  "rulefiles")

if os.path.isfile("state/offsetlogs.intro.log"):
    os.remove("state/offsetlogs.intro.log")

test4b.Run()

if test4b.Check(expected.Test4b()):
    print "success"
else:
    print "failed"
    print test4b.Result(),
    fail = 1

# Set the exit status

if fail:
    sys.exit(1)
else:
    sys.exit(0)
