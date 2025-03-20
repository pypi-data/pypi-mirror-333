# Revised Stopwords for NLP

## Overview
This package provides an optimized stopwords list for sentiment analysis by preserving sentiment-related words that NLTK’s default list would typically remove. By retaining key negations and intensity modifiers, this package ensures that sentiment expressions remain intact, leading to more accurate sentiment classification.

## Features
- Retains crucial negations (`not`, `won't`, `wouldn't`, `shouldn't`, etc.)
- Keeps intensity modifiers (`very`, `most`, `more`, etc.) for better sentiment retention
- Removes only words that do not impact sentiment analysis

---

## Installation

### **Install via [pip](https://pip.pypa.io/en/stable/)**
```bash
pip install revised-stopwords
```


### Import and Use in Your NLP Pipeline

```python
from revised_stopwords import get_revised_stopwords

# Get the optimized stopwords list
stopwords_list = get_revised_stopwords()

print(stopwords_list)  # Output: A set of refined stopwords
```
### Example: Removing Stopwords from Text

```python
from revised_stopwords import get_revised_stopwords

text = "I don't think this is a very good idea"
tokens = text.lower().split()  # Basic word split

filtered_tokens = [word for word in tokens if word not in get_revised_stopwords()]

print(filtered_tokens)
# Output: ["don't", 'think', 'very', 'good', 'idea']
```
## Troubleshooting
LookupError: Resource stopwords not found?

Please use the NLTK Downloader to obtain the resource. Run this command once to manually download stopwords

```python
import nltk
nltk.download('stopwords')
```

ModuleNotFoundError: No module named 'nltk'?  

This error means that the `nltk` library is not installed in your environment.  
Ensure NLTK is installed:

```bash
pip install nltk
```

## Contributing  
Want to improve this package? Feel free to **fork the repo, submit PRs, or suggest enhancements!**  

### How to Contribute:

1. **Fork this repository** to your GitHub account.  
2. **Clone your forked repo**:  

    ```bash
    git clone https://github.com/priyaa279/revised_stopwords.git
    ```
3. Create a new branch for your changes:

    ```bash
    git checkout -b feature-branch-name
    ```

4. Make your changes and commit them:

    ```bash
    git commit -m "Describe your change"
    ```
5. Push your branch to GitHub:

    ```bash
    git push origin feature-branch-name
    ```
Submit a Pull Request (PR) for review.
For major changes, please open an issue first to discuss what you'd like to modify. 

## License

This project is open-source and licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.
