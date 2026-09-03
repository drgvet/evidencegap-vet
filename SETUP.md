# Publishing setup, once

Two things to do, both in a browser. About ten minutes.

## 1. Put the repo on GitHub

The folder is already a git repository with two commits in it, so there is
nothing to initialise — you only need to point it at GitHub.

1. Go to https://github.com/new
2. Repository name: `evidencegap-vet`. Private is fine — Cloudflare can still
   read it once you authorise it.
3. Do **not** tick "add a README" — this folder already has one.
4. On the next screen GitHub shows a block headed
   "…or push an existing repository from the command line". Copy those two
   `git remote add` and `git push` lines.
5. Open Terminal on your Mac and run:

   ```
   cd ~/Claude/evidencegap-site
   ```

   then paste the lines you copied.

If Terminal asks for a password, use a personal access token rather than your
GitHub password — GitHub stopped accepting passwords here. Settings →
Developer settings → Personal access tokens → Fine-grained tokens.

## 2. Point Cloudflare Pages at it

In the Cloudflare dashboard, on the existing evidencegap.vet Pages project:

- Settings → Builds & deployments → Configure Git integration, and pick the
  repository you just created.

Or, if it is easier to start a fresh project: Workers & Pages → Create → Pages
→ Connect to Git.

Then set:

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | `python3 build.py` |
| Build output directory | `_site` |
| Production branch | `main` |

Save and deploy. The first build takes a minute or two.

If the build fails saying python3 is not found, add an environment variable
`PYTHON_VERSION` set to `3.11` under Settings → Environment variables.

## One tidy-up

The `.html` files sitting in the top of the folder are the old manually
uploaded copies of the site. They are deliberately not tracked by git, and
once Cloudflare is building from the repository they serve no purpose. Delete
them whenever you like — along with the `_to_delete` folder, which holds two
stale git lock files.

## After that

Editing is: open the file on github.com, click the pencil, change the words,
click "Commit changes". The site rebuilds on its own within a minute or two.

You never need to touch the old manual upload again.
