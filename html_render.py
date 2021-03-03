#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""


# This is the framework for the base class
class Element:
    tag = "html"

    def __init__(self, content=None, **kwargs):
        """
        param content: """
        if content is None:
            self.contents = []
        else:
            self.contents = [content]
        self.attributes = kwargs

    def append(self, new_content):
        """ append method """
        self.contents.append(new_content)

    def _open_tag(self):
        # begin element < tag:
        tagl = ["<{}".format(self.tag)]

        # for name and style in **kwargs-attributes apppend attributes to tag
        for name, style in self.attributes.items():
            tagl.append(' {}="{}"'.format(name, style))

        # close tag with >
        tagl.append(">")

        # join "< - tag - attributes - >"
        return "".join(tagl)

    def _close_tag(self):
        return "</{}>\n".format(self.tag)

    def render(self, out_file):
        """ renders an element with tag and attributes """

        # open tag
        out_file.write(self._open_tag())
        out_file.write("\n")

        # write contents of contents list to file.
        for content in self.contents:
            try:
                content.render(out_file)
            except AttributeError:
                out_file.write(content)
            out_file.write("\n")

        # close tag
        out_file.write(self._close_tag())
        out_file.write("\n")


class Html(Element):
    tag = "html"


class Body(Element):
    tag = "body"


class P(Element):
    tag = "p"


class Head(Element):
    tag = "head"


# ===============================================================================
# ===============================================================================

class OneLineTag(Element):
    """ writes one line tag """

    def render(self, out_file):
        out_file.write("<{}>".format(self.tag))
        out_file.write(self.contents[0])
        out_file.write("</{}>\n".format(self.tag))

    def append(self, content):
        raise NotImplementedError


class Title(OneLineTag):
    tag = "title"


# ==============================================================================
# ==============================================================================
class SelfClosingTag(Element):

    def __init__(self, content=None, **kwargs):
        """
        Override the __init__, test if content is passed in,
        if True, raise error. If False call Element __init__
        """
        if content is not None:
            raise TypeError("SelfClosingTag can not contain any content")
        super().__init__(content=content, **kwargs)

    def append(self, *args):
        """ if append is called a type error is raised...self closing tags contain
         no content """
        raise TypeError("You can not add content to a SelfClosingTag")

    def render(self, outfile):
        tag = self._open_tag()[:-1] + " />\n"
        outfile.write(tag)


class Hr(SelfClosingTag):
    tag = "hr"


class Br(SelfClosingTag):
    tag = "br"
