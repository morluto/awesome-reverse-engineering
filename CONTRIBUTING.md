# Contributing

Suggest tools, learning materials, references, and practice resources that help someone understand software, hardware, formats, or protocols. Fixes to descriptions and broken links are welcome.

## Adding a resource

1. Check that it is not already listed and choose the most relevant section.
2. Link to the canonical repository, documentation, or project homepage.
3. Explain the concrete task it helps with in one sentence, ending with a period.
4. Mention commercial licensing, required host tools, or important platform restrictions.
5. Describe your experience with the resource in the pull request, or provide a reproducible example showing its value.

Use this format and keep entries alphabetical within a section:

```markdown
- [Project name](https://example.com/) - What it does and when someone would use it.
```

Prefer a focused addition over a bulk import. Star counts alone do not establish quality. For a new or experimental tool, describe what works today and what remains limited.

## Updating or removing a resource

Report the broken link, outdated claim, incompatibility, or replacement that motivates the change. An old publication can remain useful, and an infrequently updated tool can be complete. Review its function and documentation before treating inactivity as abandonment.

Disclose your relationship to a project you recommend. Maintainer-owned projects follow the same criteria as other entries.

## Checks

Preview the Markdown and confirm that new links and table-of-contents anchors work. GitHub Actions runs the link check for pull requests. For the equivalent local check with [lychee](https://github.com/lycheeverse/lychee) installed:

```sh
lychee --no-progress README.md CONTRIBUTING.md 'docs/*.md'
```

## Maintenance

The weekly link-check workflow reports failures in its Actions run. When reviewing the list, also check whether linked repositories are archived, have moved, or require different versions of their host tools. Update descriptions and recommendations based on those findings.

The research in `docs/list-review.md` and `docs/list-review-data.json` is a dated snapshot. Refresh both together when repeating the comparison; do not interpret their dates or star counts as live metadata.
