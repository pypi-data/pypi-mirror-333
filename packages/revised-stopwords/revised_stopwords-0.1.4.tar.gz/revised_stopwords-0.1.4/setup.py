from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="revised-stopwords",
    version="0.1.4",
    packages=find_packages(),
    install_requires=["nltk"],
    author="Priyaa Gopal Shankar",
    author_email="priyaashankar9498@gmail.com",
    description="An optimized stopwords list for sentiment analysis that retains key negations like 'not', 'won't', and 'wouldn't', along with intensity modifiers like 'very' and 'most' to preserve sentiment accuracy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/priyaa279/revised_stopwords",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
