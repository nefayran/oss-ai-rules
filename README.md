# AI contribution rules in 30 open-source repositories

What 30 open-source repositories say about AI-assisted contributions, read on 2 October 2026: 106 quotes from
their contributing guides, pull request and issue templates, AGENTS.md and CLAUDE.md files and the guides
those files link to. Every quote links to its line at the commit that was read, so the link keeps showing
what the file said that day.

[table.md](table.md) has the quotes, the counts, the date each rule first appeared and a few side notes.
[verify.py](verify.py) checks every quote against the file it links to.

## Counts

19 of the 30 have a rule about AI in contributions. Two are borderline and not counted, and nine have none.

| what the rule asks | repositories |
|---|---|
| say that you used AI | 15 |
| the person who submits is responsible and must understand the change | 12 |
| a person writes the description, the comments or the commit messages | 10 |
| a rule about commit trailers: required, allowed or banned | 9 |
| no bulk or automated pull requests | 7 |
| an issue or a maintainer's approval before the pull request | 6 |

A rule often asks for several things, so the rows add up to more than 19. 14 of the 19 rules appeared in 2026.

## Check the quotes

```sh
python3 verify.py
```

Python 3.9 or newer, no packages. Each linked file is downloaded once into `.cache/`; the Deskflow wiki,
which has no line anchors, is cloned with git and read at the linked revision. The script prints every
quote it cannot find and exits with status 1 if there is one.

## Method

- Files read: CONTRIBUTING, pull request and issue templates, AGENTS.md, CLAUDE.md, the code of conduct, and
  the guides or wiki pages these files link to, at the default branch on 2 October 2026.
- "First appeared" is the first commit that contains the rule, found by searching the history of its file.
- The kinds (disclose, a person writes the text, and so on) are my labels, and one rule can fit several.

## Limits

The 30 repositories are not a random sample. Nine are projects I sent contributions to that week, and the
rest lean towards AI tooling and developer tools, where rules are more likely. Rules change often: in 16 of
the 19, a file holding the rule was edited in the month before it was read.

## License

The table and the script are MIT-licensed. The quoted lines belong to their projects and are quoted for
reference; follow the links for the full text and its license.
