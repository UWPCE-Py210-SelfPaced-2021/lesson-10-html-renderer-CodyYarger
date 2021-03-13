#!/usr/bin/env python3
# 03/08/2021
# Dev: Cody Yarger
# Exercise 10.0: HTML Renderer
"""
A class-based system for rendering html.
"""


class Element:
    """Base class for rendering HTML files """
    tag = "html"
    indent = "   "

    def __init__(self, content=None, **kwargs):
        """
        param content: results in nested list of tags and related content
        """
        if content is None:
            self.contents = []
        else:
            self.contents = [content]
        self.attributes = kwargs

    def append(self, new_content):
        """ append method """
        self.contents.append(new_content)

    def _open_tag(self):
        """ creates tag object to be written to file """
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
        # return "</{}>\n".format(self.tag)
        return "</{}>".format(self.tag)

    def render(self, out_file, cur_ind=""):
        """ render_page(page, "test_html_output8.html")renders an element with
         tag attributes and content """
        elem_ind = cur_ind + self.indent
        # open tag
        out_file.write(cur_ind + self._open_tag())
        out_file.write("\n")

        # for content in contents call render for tags or write content
        for content in self.contents:
            # try to see if content has render method (i.e is a tag)
            try:
                content.render(out_file, elem_ind)
            # except if no render method then its the tags content, write to file.
            except AttributeError:
                out_file.write(elem_ind + content)
            out_file.write("\n")

        # close tag
        out_file.write(cur_ind + self._close_tag())


class Html(Element):
    tag = "html"

    def render(self, out_file, cur_ind=""):
        out_file.write("<!DOCTYPE html>\n")
        super().render(out_file, cur_ind="")


class Body(Element):
    tag = "body"


class P(Element):
    tag = "p"


class Head(Element):
    tag = "head"


class Li(Element):
    tag = "li"


class Ul(Element):
    tag = "ul"


# ===============================================================================
# One Line Tag Class and Sub Classes
# ===============================================================================
class OneLineTag(Element):
    """ writes one line tag """

    def render(self, out_file, cur_ind=""):
        out_file.write(cur_ind)
        out_file.write(self._open_tag())
        out_file.write(self.contents[0])
        out_file.write(self._close_tag())

    def append(self, content):
        """ append method overwritten. One line tags don't have content """
        raise NotImplementedError


class Title(OneLineTag):
    tag = "title"


class A(OneLineTag):
    tag = 'a'

    def __init__(self, link, content=None, **kwargs):
        kwargs['href'] = link
        super().__init__(content, **kwargs)


class H(OneLineTag):
    """ One line tag class """

    def __init__(self, level, content=None, **kwargs):
        self.tag = "h" + str(level)
        if content is None:
            self.contents = []
        else:
            self.contents = [content]
        self.attributes = kwargs


# ==============================================================================
# Self Closing Tag Class and Sub Classes
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

    def render(self, outfile, cur_ind=""):
        tag = self._open_tag()[:-1] + " />"
        outfile.write(cur_ind + tag)


class Meta(SelfClosingTag):
    tag = "meta"


class Hr(SelfClosingTag):
    tag = "hr"


class Br(SelfClosingTag):
    tag = "br"
