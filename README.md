# [Pulse Check](https://pulsecheckclassifier.herokuapp.com/)

Tweet sentiment analyser

## What is this?

Pulse Check is a web app that predicts the sentiment (positive or negative) of tweets that are related to a user-submitted topic.

## How does it work?

Under the hood, Pulse Check uses a [Naive Bayes classifier](https://en.wikipedia.org/wiki/Naive_Bayes_classifier), trained on over 1 million tweets, to predict sentiment. The Naive Bayes classifier is one of a multitude of machine learning text classifiers that exist. 

The web app is built using a [Python 3](https://www.python.org/download/releases/3.0/) backend and the [Flask](https://flask.palletsprojects.com/en/1.1.x/) framework. You'll need these installed on your machine to build it locally.

## How can I contribute?

Contributions are welcome! In particular, contributions of additional machine learning text classifiers would be very useful. For example, a Naive Bayes classifier predicts sentiment with reasonable accuracy (this classifier achieved an accuracy of 73%). However, as the [canonical Stanford paper on Tweet sentiment analysis](https://www-cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf) shows, support vector machines do better. 

Another useful addition would be a sentiment analyser trained to predict neutral sentiment, as well as positive and negative sentiment.

To contribute, please follow the process below:

* Create a personal fork of this GitHub repo.
* In your fork, create a branch off the **master** branch.
* Make your changes on your branch, keeping the following in mind:
    * Follow the current coding style.
    * Include tests when adding a new feature.
* Build the repo with your changes, and ensure that the tests pass.
* Commit your changes to your branch.
* Create a pull request (PR) against the repo's **master** branch:
    * Add a title that summarises the changes.
    * In the description, list the main changes.
* Wait for feedback or approval of your changes.
* When your changes have been approved, the PR will be merged.

# License

The project is licensed under the [MIT license](LICENSE.txt).