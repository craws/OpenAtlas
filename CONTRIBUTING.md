# How to contribute

Thank you for considering to contribute to OpenAtlas and reading this document.

## Feedback, reporting bugs and feature requests

Feedback is always appreciated and can be done by

* using our issue tracker
  [Redmine](https://redmine.openaltas.eu/wiki/uni) after reading
  [how to report an issue](https://redmine.openatlas.eu/projects/uni/wiki/Issues_howto)
* contacting us at <openatlas@oeaw.ac.at>

## Code contribution

We also welcome code contributions via GitHub pull requests to the develop
branch after reading about our
[development standards](https://redmine.openatlas.eu/projects/uni/wiki/Standards).

### Submitting changes via GitHub pull requests

Clone the repository and make a new branch from the develop branch.

    git checkout develop
    git checkout -b feature_example

Make changes, you can check these before committing with

    git status
    git diff --

Commit the changes and push it to your cloned repository on GitHub

    git add .
    git commit -m "A short message about the changes"
    git push

Make a pull request from your new branch to the develop branch of OpenAtlas,
see: [GitHub pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
