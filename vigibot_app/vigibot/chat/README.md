# Chat Engine for Vigibot
We are using [Chatterbot](https://github.com/gunthercox/chatterbot) for the conversational engine of vigibot.com/

Here we will keep the Epidemiology specific corpora needed to train chatterbot.

## Getting started

Before starting to use chatterbot we need to setup spacy, the nlp engine it uses.

```bash
sudo python -m spacy download en
sudo python -m spacy download pt
```

Then open this [notebook](Testing.ipynb) to train and test the chat engine with the latest version of the corpus.
