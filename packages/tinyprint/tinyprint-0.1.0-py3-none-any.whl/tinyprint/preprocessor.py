from __future__ import annotations

import abc
from typing import Callable, TypeAlias

from escpos.escpos import Escpos  # type: ignore
import marko  # type: ignore
from PIL import Image  # type: ignore

from tinyprint.jobconfig import Resource
from tinyprint.job import Job


Page: TypeAlias = Callable[[Escpos], None]


class Preprocessor(abc.ABC):
    def __init__(self, job: Job):
        self.job = job

    @abc.abstractmethod
    def __call__(self, resource: Resource) -> Page: ...


class ImagePreprocessor(Preprocessor):
    def __call__(self, resource: Resource):
        profile = self.job.printer.profile

        def _(printer):

            with Image.open(resource[0]) as im:
                max_width = profile.profile_data["media"]["width"]["pixels"]
                assert max_width != "Unknown", "max_width of printer unknown!"
                max_width = int(max_width * profile.img_scale_factor)
                width = im.width
                heigth = im.height
                factor = max_width / width
                im = im.resize(
                    (
                        int(width * factor * profile.img_x_scale_factor),
                        int(heigth * factor * profile.img_y_scale_factor),
                    )
                )

                # Add extra space between to make spaces between cuts even
                # XXX Does number '10' need to change depending on printer?
                if self.job.config.cut:
                    printer.line_spacing(10)
                    printer.ln()
                    printer.line_spacing()

                img_kwargs = dict(self.job.printer.profile.img_kwargs)
                if fragment_height := resource[1]:
                    img_kwargs["fragment_height"] = fragment_height

                printer.image(
                    im,
                    **img_kwargs,
                )

        return _


# https://github.com/Belval/pdf2image
# but then we depend on 1 more external program: poppler
class PdfPreprocessor(Preprocessor): ...


class MarkdownPreprocessor(Preprocessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.markdown = marko.Markdown(renderer=_EscposRenderer)
        self.markdown._setup_extensions()

    def __call__(self, resource: Resource):
        with open(resource[0], "r") as f:
            md = f.read()

        def _(printer):
            self.markdown.renderer.set_printer(printer)
            self.markdown(md)

        return _


class _EscposRenderer(marko.renderer.Renderer):
    # Ref: https://github.com/frostming/marko/blob/master/marko/html_renderer.py

    # TODO Allow images
    # TODO Add auto line breaks
    # TODO Add auto page breaks

    def render_raw_text(self, element) -> str:
        self._printer.text(element.children)
        return ""

    def render_emphasis(self, element) -> str:
        self._set(bold=True)
        self.render_children(element)
        self._set(bold=False)
        return ""

    def render_strong_emphasis(self, element) -> str:
        return self.render_emphasis(element)

    def render_line_break(self, element) -> str:
        self._printer.ln(2)
        return ""

    def render_paragraph(self, element) -> str:
        self.render_children(element)
        self._printer.ln(2)
        return ""

    def render_heading(self, element) -> str:
        self._set(double_height=True, double_width=True)
        self.render_children(element)
        self._set(double_height=False, double_width=False, normal_textsize=True)
        self._printer.ln(3)
        return ""

    def set_printer(self, printer):
        self._printer = printer

    def set_job(self, job):
        self._job = job

    def _set(self, *args, **kwargs):
        if self._printer:
            self._printer.set(*args, **kwargs)
        else:
            raise RuntimeError("printer not yet set")
