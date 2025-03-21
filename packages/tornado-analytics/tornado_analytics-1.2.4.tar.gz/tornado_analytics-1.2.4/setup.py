from setuptools import setup

long_description = open("README.md").read()

setup(
    name="tornado-analytics",
    version="1.2.4",
    author="Tom Draper",
    author_email="tomjdraper1@gmail.com",
    license="MIT",
    description="Monitoring and analytics for Tornado applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tom-draper/api-analytics",
    key_words="analytics api dashboard tornado middleware",
    install_requires=["tornado", "requests"],
    packages=["api_analytics"],
    python_requires=">=3.6",
)
