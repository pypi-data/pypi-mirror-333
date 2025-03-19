from tinyprint.job import Job
from tinyprint.jobconfig import JobConfig


def test_markdown_preprocessor(tmpdir):
    md_file_path = f"{tmpdir}/test.md"
    with open(md_file_path, "w") as f:
        f.write(md)

    config = JobConfig([[md_file_path, 0]])
    job = Job(config)
    page_tuple = job._generate_page_tuple()
    for p in page_tuple:
        p(job.printer)


md = r"""

# hello world

this is a test.

this is still a *test*.

[abc](https://codeberg.org)

"""
