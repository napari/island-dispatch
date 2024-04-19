# The Island Dispatch

A blog for napari-related news and announcements.

To contribute a post, please submit a pull request to this repository with your post written in markdown format.

## How to submit a post

If you are familiar with the GitHub workflow, you can submit a post directly via pull request. If you prefer using the GitHub web interface, follow the steps below:

1. Fork this repository

![GitHub interface, showing the "Fork" button](images/00_fork.png)

1. On your fork, navigate to [`source/blog`](source/blog) and create a new markdown file.

![GitHub interface, showing the source/blog directory](images/01_source.png)

![GitHub interface, showing the "Create new file" button](images/02_create_new_file.png)

2. Your post must have the following front-matter (with date, author, location, category, and language fields filled in according to your post):

```markdown
---
blogpost: true
date: Apr 18, 2024
author: The napari community
location: World
category: Manual
language: English
---

# Title to your post

Contents of your post.
```

3. Name your file and commit your changes.

![GitHub interface, showing the "Commit changes" button](images/03_commit.png)

4. Submit your changes as a Pull Request.

> [!IMPORTANT]
> Make sure you select "Create a new branch for this commit and start a pull request".

![GitHub interface, showing the "Propose changes" dialog](images/04_create_branch.png)

5. You will have the option to add more context or information to your Pull Request proposal, and submit it. If you are still working on your post, you can create a "Draft Pull Request" to save your progress. Once you are ready, you can  mark it as "Ready for review" to notify the maintainers.

![GitHub interface, showing the "Open a pull request" page](images/05_create_pr.png)

6. Wait for a review 🎉

Once your post is approved, it will be published on the blog.

## Review process

When your pull request is submitted, a few checks will run automatically to validate the post syntax and metadata. You can see a preview of your post by clicking on the "Blog preview" link in the Checks section of the Pull Request page.
