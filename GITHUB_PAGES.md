# Publish the public teaching website

## 1. Public-release boundary

The website identifies Sayara Beg as course author and Heat Cascade research lead. It publishes general teaching examples and synthetic data. Detailed proposal architecture and work-package plans are withheld from the current release.

Each release should be reviewed against the intended public scope, including repository versions and student forks. Attribution identifies authorship; the detailed research proposal remains outside this teaching release.

## 2. Activate GitHub Pages

The generated website is in `docs`. In the repository, open **Settings > Pages**, then select **Deploy from a branch**, then branch **main** and folder **/docs**, and choose **Save**.

The connected GitHub tools can write repository files but cannot change the Pages setting. GitHub confirms the live address after deployment. The course website is https://uclse.github.io/data-analytics/. Its source repository is UCLse/data-analytics. Keep the source Markdown and generated `docs` files together in each update.

Pages is available for public repositories on GitHub Free. Hosting from a private repository requires a supporting plan. Pages content is normally public even when its source repository is private.

## 3. Update the rendered teaching material

Edit the source Markdown in `heat-cascade`. From the repository root, install the website dependency and rebuild:

```bash
npm install
npm run build:site
```

Node.js 20 or later is required for this instructor build. The builder renders the course pages, adds attribution, links students to the GitHub fork workflow. Commit the updated source and generated `docs` together. Students only need the VS Code or Codespaces route in Workshop 00.

## 4. Verification boundary

The website build and internal paths are checked before upload. A live GitHub Pages deployment and a fresh Codespaces session require verification in the selected GitHub environment. The course's analytical reference checks remain documented separately.

Official guidance: [publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) and [GitHub Pages availability](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).
