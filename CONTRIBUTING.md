# How to contribute

Thank you for considering to contribute to OpenAtlas and reading this document.

We are happy about participation and there are multiple ways to contribute.

## Feedback, reporting bugs and feature requests

Feedback is always appreciated, preferable in a constructive way. E.g.


* Using our issue tracker [Redmine](https://redmine.openaltas.eu/wiki/uni) after
reading [How to report an issue](https://redmine.openatlas.eu/projects/uni/wiki/Issues_howto).
* Contacting us at <openatlas@oeaw.ac.at>

## Code contribution

We also welcome code contributions e.g. via a GitHub pull requests to the
develop branch.

Please be sure to read our
[Development Standards](https://redmine.openatlas.eu/projects/uni/wiki/Standards)
to avoid complications.

Submitting changes via a GitHub pull request:

Clone the repository and make a new branch from the develop branch:

    git checkout develop
    git checkout -b feature_example

Make changes, you can check this before committing with

    git status
    git diff --

Commit the changes and push it to your cloned repository on GitHub

    git add .
    git commit -m "A short message about the changes"
    git push

Make a pull request from your new branch to the develop branch of OpenAtlas.
See: [GitHub pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
