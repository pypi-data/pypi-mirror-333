# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"

import os
import shutil
import datetime
import tempfile
import subprocess
import xml.etree.ElementTree as ET

from pyogctest.logger import Logger
from pyogctest.report.format import Format

COLOR_PASSED="#006600"
COLOR_FAILED="#e60000"


class Test(object):
    def __init__(self):
        self.name = ""
        self.message = ""
        self.result = ""
        self.exception = ""
        self.method = ""

    def toc(self):
        href = ('<a href="#{}">{}</a><b style="font-family: Verdana, '
                'sans-serif; color: {};"> {}</b>'
               ).format(self.method, self.method, self.color, self.status)

        toc = ('<ul>\n'
           '  <li>\n'
           '    {0}\n'
           '  </li>\n'
           '</ul>').format(href)

        return toc

    def body(self):
        result = ('<b style="font-family: Verdana, sans-serif; '
                  'color: {};"> {}</b>'
        ).format(self.color, self.status)

        description = "Test {}.{} method.".format(self.name, self.method)

        reporter = "There is nothing to report."
        if self.status != "Passed":
            reporter = "{}: {}".format(self.exception, self.message)

        body = ('<div class="test">\n'
        '<h2><a name="{}">test: {}.{}</a></h2>'
        '<p><h4>Assertion</h4>{}</p>'
        '<p><h4>Test result</h4>{}</p>'
        '<p><h4>Message</h4>{}</p>'
        '</div>\n'
        ).format("id", self.name, self.method, description, result, reporter)

        return body

    @property
    def color(self):
        color = COLOR_FAILED
        if self.status == "Passed":
            color = COLOR_PASSED
        return color

    @property
    def status(self):
        status = "Failed"
        if self.result == "PASS":
            status = "Passed"
        return status


class Html(object):
    def __init__(self, tests):
        self.tests = tests

    @property
    def color(self):
        for test in self.tests:
            if test.result != "PASS":
                return COLOR_FAILED
        return COLOR_PASSED

    @property
    def status(self):
        for test in self.tests:
            if test.result != "PASS":
                return "Failed"
        return "Passed"

    def toc(self):
        toc = ''

        classes = {}
        for test in self.tests:
            if test.classe not in classes:
                classes[test.classe] = True
                continue

            if test.result == "PASS":
                classes[test.classe] &= True
            else:
                classes[test.classe] = False

        for classe in classes:
            status = "Failed"
            color = COLOR_FAILED

            if classes[classe]:
                status = "Passed"
                color = COLOR_PASSED

            href = ('<a href="#{}">{}</a><b style="font-family: Verdana, '
            'sans-serif; color: {};"> {}</b>'
           ).format(classe, classe, color, status)

            t = ''
            for test in self.tests:
                if test.classe != classe:
                    continue

                t += test.toc()

            toc += ('<ul>\n'
           '  <li>\n'
           '    {0}\n'
           '    {1}\n'
           '  </li>\n'
           '</ul>').format(href, t)

        return toc

    def body(self):
        classes = {}
        for test in self.tests:
            if test.classe not in classes:
                classes[test.classe] = True
                continue

            if test.result == "PASS":
                classes[test.classe] &= True
            else:
                classes[test.classe] = False

        body = ""
        for classe in classes:
            status = "Failed"
            color = COLOR_FAILED

            if classes[classe]:
                status = "Passed"
                color = COLOR_PASSED

            subtests = ('<p><h4>Executed tests</h4>'
                        '<ul>\n')
            for test in self.tests:
                if classe != test.classe:
                    continue

                subtests += ('<li>'
                             '<a name="{}">{}</a><b style="font-family: '
                             'Verdana, sans-serif; color: {};"> {}</b>'
                             '</li>').format(test.method, test.method, test.color, test.status)
            subtests += "</ul>"

            body += ('<div class="test">\n'
            '<h2><a name="{}">test: {}</a></h2>'
            '<p><h4>Test result</h4>{}</p>'
            '{}'
            '</div>\n'
            ).format(classe, classe, status, subtests)

            for test in self.tests:
                if classe != test.classe:
                    continue

                body += test.body()

        return body



class ParserOGCAPIF(object):
    def __init__(self, xml, duration):
        self.xml = xml
        self.duration = duration
        self.error = 0

    def dump_html(self, outdir, commit, branch):
        tests = self._parse()
        html = Html(tests)

        # generate html
        outpath = os.path.join(outdir, 'pyogctest_ogcapif.html')

        moddir = os.path.dirname(os.path.realpath(__file__))
        template = os.path.join(moddir, 'template.html')
        with open(template, 'r') as infile:
            with open(outpath, 'w') as outfile:
                for line in infile:
                    # date
                    date_tag = '{{TEMPLATE_DATE}}'
                    if date_tag in line:
                        format = '%Y-%m-%d %H:%M:%S'
                        date = datetime.datetime.now().strftime(format)
                        line = date

                    # overall result
                    color_tag = '{{TEMPLATE_RESULT_COLOR}}'
                    status_tag = '{{TEMPLATE_RESULT_STATUS}}'
                    if color_tag in line:
                        line = line.replace(color_tag, html.color)
                        line = line.replace(status_tag, html.status)

                    # version
                    version_tag = '{{TEMPLATE_VERSION}}'
                    if version_tag in line:
                        line = line.replace(version_tag, branch)

                    # commit
                    commit_tag = '{{TEMPLATE_COMMIT}}'
                    if commit_tag in line:
                        line = line.replace(commit_tag, commit)

                    # toc
                    toc_tag = '{{TEMPLATE_TOC}}'
                    if toc_tag in line:
                        line = html.toc()

                    # body
                    body_tag = '{{TEMPLATE_BODY}}'
                    if body_tag in line:
                        line = html.body()

                    outfile.write(line)

        style = os.path.join(moddir, "style.css")
        shutil.copy(style, outdir)

        logo = os.path.join(moddir, "logo.png")
        shutil.copy(logo, outdir)

    def dump_prompt(self, verbose, regex):
        tests = self._parse()
        Logger.log("collected {} items".format(len(tests)), bold=True)
        Logger.log("")

        ok = "PASSED" if verbose else "."
        ko = "FAIL" if verbose else "F"

        for test in tests:
            if regex not in test.name and regex not in test.method:
                continue

            results = ""
            if test.result == "PASS":
                results = results + Logger.Symbol.OK + ok + Logger.Symbol.ENDC
            else:
                results = results + Logger.Symbol.FAIL + ko + Logger.Symbol.ENDC

            print("{}::{} {}".format(test.name, test.method, results))

        self._print_summary(tests)

    def _print_summary(self, tests):
        failures = []
        successes = []
        for test in tests:
            if test.result == "PASS":
                successes.append(test)
            else:
                failures.append(test)

        Logger.log("")
        if not failures:
            msg = " {} passed in {} seconds ".format(len(successes), self.duration)
            Logger.log(msg, color=Logger.Symbol.OK, center=True, symbol="=")
        else:
            Logger.log(" FAILURES ", center=True, symbol="=")

            for failure in failures:
                name = " {}::{} ".format(failure.name, failure.method)
                Logger.log(name, color=Logger.Symbol.FAIL, center=True, symbol="_")
                Logger.log("")

                if failure.exception:
                    Logger.log("Error: {}".format(failure.exception))
                    Logger.log("")

                if failure.message:
                    msg = failure.message.strip().replace("\n", "")
                    Logger.log("Message: {}".format(msg))
                    Logger.log("")

                if failure.method:
                    Logger.log("Method: {}".format(failure.method))
                    Logger.log("")

            msg = " {} passed, {} failed in {} seconds ".format(
                len(successes), len(failures), self.duration
            )
            self.error = 1
            Logger.log(msg, color=Logger.Symbol.WARNING, center=True, symbol="=")

    def _parse(self):
        root = ET.fromstring(self.xml)

        tests = []
        for test in root.find("suite").findall("test"):
            for cls in test.findall("class"):
                for meth in cls.findall("test-method"):
                    if meth.attrib["status"] == "SKIP":
                        continue

                    msg = ""
                    exc = ""
                    if meth.attrib["status"] != "PASS":
                        msg = meth.find("exception").find("message").text.strip()
                        exc = meth.find("exception").attrib["class"]

                    t = Test()
                    t.classe = cls.attrib["name"].split(".")[-1]
                    t.name = "::".join(cls.attrib["name"].split(".")[-2:])
                    t.method = meth.attrib["name"]
                    t.result = meth.attrib["status"]
                    t.exception = exc
                    t.message = msg
                    tests.append(t)

        return tests
