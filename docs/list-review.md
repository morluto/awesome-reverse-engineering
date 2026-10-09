# Reverse-engineering list review

Snapshot: **9 October 2026 (UTC)**. This review covers **21 repositories**: eight general reverse-engineering lists, twelve specialist collections, and one broader discovery index.

## Findings

The largest general lists are useful historical references, but their popularity does not establish current maintenance. The default README histories of wtsxDev, alphaSeclab, and tylerha97 end in 2019, despite later repository push dates. The tables below link directly to the observed commits.

For current structure and maintenance practices, the strongest examples in this sample are **hexsecs** for curation and health checks, **VelocityRa** for organizing a growing catalog, and **DiscoverBox** for helping readers select tools. **TheQmaks** demonstrates a structured catalog with a working weekly verifier, but has a shorter public track record. The distinctions matter: a scheduled metadata update, a successful link check, and a considered resource addition are different evidence.

## Method

Discovery used GitHub repository search ordered by stars, web search, and related-list links. Queries included `awesome reverse engineering`, `awesome-reversing in:name fork:false`, `awesome android reverse engineering`, `awesome malware analysis`, `awesome firmware`, `awesome embedded security`, `awesome binary analysis`, and `topic:reverse-engineering topic:awesome-list fork:false`. Specialist candidates were added to find maintenance practices that the older high-star general lists lack.

For each repository, I inspected its README taxonomy and entry format, root/supporting files, repository metadata, and default-branch README commit history. I read selected topic pages and maintenance workflows from the recent candidates, and sampled their latest Actions runs. The linked [JSON snapshot](list-review-data.json) records dates, commit evidence, file names, and those runs.

This is a review of leading search results and relevant specialists, rather than an exhaustive census of GitHub or an audit of every linked resource. Stars are a discovery signal. “Last push” can reflect another branch or an automated change. A README commit can be cosmetic, and split catalogs can change without touching the root README. Imported history can predate repository creation, so it does not prove years of maintenance by the current owner. The gmh5225 `awesome-re-list` result was a fork; the tables use its original upstream, `extremecoders-re/re-list`, instead.

## General lists

| Repository | Stars | Last README commit | Last repository push | Structure and maintenance observation |
| --- | ---: | --- | --- | --- |
| [wtsxDev/reverse-engineering](https://github.com/wtsxDev/reverse-engineering) | 10,481 | [2019-03-07](https://github.com/wtsxDev/reverse-engineering/commit/b25498551c6d7110685896078afeb27097aa1e24) | 2023-07-29 | Single README: books, courses, practice, then tool categories. Large audience; README history is old. |
| [alphaSeclab/awesome-reverse-engineering](https://github.com/alphaSeclab/awesome-reverse-engineering) | 5,088 | [2019-12-31](https://github.com/alphaSeclab/awesome-reverse-engineering/commit/1a7445d2c7e3e42350a2556c70b469fb3429d49a) | 2021-09-01 | Very large bilingual catalog with deeply nested tool/platform sections and history files. Historical reference. |
| [tylerha97/awesome-reversing](https://github.com/tylerha97/awesome-reversing) | 4,527 | [2019-03-08](https://github.com/tylerha97/awesome-reversing/commit/0b7bb2b40797e996578d5175408efc7d6aac5dca) | 2023-08-19 | Single README mixing learning resources and tool categories. README history is old. |
| [HACKE-RC/awesome-reversing](https://github.com/HACKE-RC/awesome-reversing) | 1,523 | [2025-03-18](https://github.com/HACKE-RC/awesome-reversing/commit/f2c569eb293364a89e5e573319c25868f3f2fa4d) | 2025-03-18 | Learning sequence: assembly, OS internals, hands-on work, then advanced techniques. No README change in the past year. |
| [ReversingID/Awesome-Reversing](https://github.com/ReversingID/Awesome-Reversing) | 734 | [2026-05-27](https://github.com/ReversingID/Awesome-Reversing/commit/0229b0e16002d01ce08e61ecbf09a72d1a3f5b92) | 2026-05-27 | Small domain index linking software, hardware, format, and database pages. Reorganized in May; insufficient evidence of regular updates. |
| [extremecoders-re/re-list](https://github.com/extremecoders-re/re-list) | 259 | [2024-04-16](https://github.com/extremecoders-re/re-list/commit/539b60e6f4a17f42f07089b82c7cd909a1056f6f) | 2024-04-16 | Flat tool table rather than a learning path. Original upstream of the gmh5225 fork surfaced by web search. |
| [ZX41R/awesome-reverse-engineering-and-malware-analysis](https://github.com/ZX41R/awesome-reverse-engineering-and-malware-analysis) | 94 | [2026-08-04](https://github.com/ZX41R/awesome-reverse-engineering-and-malware-analysis/commit/dc993c0a52179350ffcd328ff5c91b9ad8c5a399) | 2026-10-02 | Track-oriented index plus topic directories and entry tags. Topic commits in September; short repository track record. |
| [cybersecurity-dev/awesome-reverse-engineering](https://github.com/cybersecurity-dev/awesome-reverse-engineering) | 5 | [2026-09-17](https://github.com/cybersecurity-dev/awesome-reverse-engineering/commit/bfdc3ffc9c704ceef7804f47ef9666740a3bc3c1) | 2026-09-17 | Compact OS/execution overview and tool categories. README edits across several months in the past year. |

## Specialist lists

| Repository | Stars | Last README commit | Last repository push | Structure and maintenance observation |
| --- | ---: | --- | --- | --- |
| [rshipp/awesome-malware-analysis](https://github.com/rshipp/awesome-malware-analysis) | 14,265 | [2024-05-30](https://github.com/rshipp/awesome-malware-analysis/commit/179887b9bfb04bb736348b2dc9d331bc860c6ef7) | 2024-06-07 | Workflow categories from collection and triage through debugging, networks, and memory. Broad historical reference. |
| [onethawt/idaplugins-list](https://github.com/onethawt/idaplugins-list) | 3,839 | [2023-05-02](https://github.com/onethawt/idaplugins-list/commit/decddd9fc3125eee900ec7d1cd3e557acffd26c1) | 2024-05-31 | Long plugin inventory with descriptions and a commercial section. Useful specialist index; README history is old. |
| [user1342/Awesome-Android-Reverse-Engineering](https://github.com/user1342/Awesome-Android-Reverse-Engineering) | 2,733 | [2025-07-08](https://github.com/user1342/Awesome-Android-Reverse-Engineering/commit/0ade43d6b46ff19675ca4d8b8f1cc098e1af73b8) | 2025-07-08 | Training, static/dynamic tools, documentation, practice, and advanced Android topics. No README change in the past year. |
| [AllsafeCyberSecurity/awesome-ghidra](https://github.com/AllsafeCyberSecurity/awesome-ghidra) | 1,435 | [2026-06-18](https://github.com/AllsafeCyberSecurity/awesome-ghidra/commit/9e786ded846e993ab3071cbb31b615cd0f69282d) | 2026-06-18 | Simple plugins/scripts, materials, and other links. May/June README history includes merges; regular curation not established. |
| [Cy-clon3/awesome-ios-security](https://github.com/Cy-clon3/awesome-ios-security) | 674 | [2022-05-30](https://github.com/Cy-clon3/awesome-ios-security/commit/a65370f368a740bbd256429990931dc0664ec782) | 2024-01-05 | Tools, tweaks, scripts, courses, articles, labs, and checklists. Has lint workflow; README history is old. |
| [PreOS-Security/awesome-firmware-security](https://github.com/PreOS-Security/awesome-firmware-security) | 618 | [2019-07-18](https://github.com/PreOS-Security/awesome-firmware-security/commit/c8daa78da2ec9d746bdbd496b67e28f188ec743b) | 2019-07-24 | Terminology and threats before open/closed-source tools and documentation. Historical reference. |
| [VelocityRa/awesome-game-file-format-reversing](https://github.com/VelocityRa/awesome-game-file-format-reversing) | 220 | [2026-10-01](https://github.com/VelocityRa/awesome-game-file-format-reversing/commit/abe77040e69b9e9dfb4357ba3dfd23bc4624802d) | 2026-10-03 | Thin index plus list pages by tools, engine, and game; documentation site and structure/link checks. Sustained recent additions. |
| [hexsecs/awesome-embedded-security](https://github.com/hexsecs/awesome-embedded-security) | 64 | [2026-09-30](https://github.com/hexsecs/awesome-embedded-security/commit/e0091c344e69a2b49858fb7e0edf190032f79e51) | 2026-10-07 | Software/hardware/training hierarchy, commercial/archive markers, contribution rules, and health workflows. Sustained recent curation. |
| [user1342/Awesome-Binary-Analysis-Automation](https://github.com/user1342/Awesome-Binary-Analysis-Automation) | 61 | [2024-04-21](https://github.com/user1342/Awesome-Binary-Analysis-Automation/commit/242a56129521b0bd693bbb792fb612ef299974c1) | 2024-04-21 | Training plus automated-analysis, emulation, extraction, and diffing categories. Historical reference. |
| [DiscoverBox/awesome-ai-reverse](https://github.com/DiscoverBox/awesome-ai-reverse) | 60 | [2026-10-09](https://github.com/DiscoverBox/awesome-ai-reverse/commit/4718e2b0e527267bd4ba767f9b41e1b2c9329f85) | 2026-10-09 | Quick-selection tables, tool types, ecosystem categories, bilingual pages, and daily metadata refresh. Recent editorial changes as well as automation. |
| [ram-elgov/awesome-llm-reverse-engineering](https://github.com/ram-elgov/awesome-llm-reverse-engineering) | 31 | [2025-07-28](https://github.com/ram-elgov/awesome-llm-reverse-engineering/commit/55366aa3d44526ed0a9d3cb7fa01d4d8227d4631) | 2025-07-28 | Tools, datasets, papers, tutorials, and benchmarks. README edits concentrated in July 2025. |
| [TheQmaks/awesome-web-reversing](https://github.com/TheQmaks/awesome-web-reversing) | 3 | [2026-09-01](https://github.com/TheQmaks/awesome-web-reversing/commit/e294f97fcd6560f6f7f7bde1ea7cc42b07b8e1f3) | 2026-10-05 | Workflow docs plus structured tool data and generated catalog. Weekly verifier recently ran successfully; repository created in August. |

## Broader discovery index

| Repository | Stars | Last README commit | Last repository push | Structure and maintenance observation |
| --- | ---: | --- | --- | --- |
| [Hack-with-Github/Awesome-Hacking](https://github.com/Hack-with-Github/Awesome-Hacking) | 122,002 | [2026-07-26](https://github.com/Hack-with-Github/Awesome-Hacking/commit/b2bb13aa69b4f568a1bab0cbb17b7a00a350dc36) | 2026-07-26 | Table of other security lists. Useful discovery index; broader than reverse engineering and recent changes include banner edits. |

## Structures worth adopting

### Clear selection before the catalog

[DiscoverBox's English README](https://github.com/DiscoverBox/awesome-ai-reverse/blob/main/README_EN.md) explains tool types and starts with a task-to-tool table before its ecosystem sections. That reduces the knowledge a reader needs before choosing a category. Its entries also surface dependencies on host tools and commercial software. For this repository, a short task table and explicit commercial labels provide that benefit without a wide metadata table for every entry.

DiscoverBox's [metadata workflow](https://github.com/DiscoverBox/awesome-ai-reverse/blob/main/.github/workflows/update-readme-metadata.yml) updates dates and stars daily and commits under the owner's name with a bot email. The sampled scheduled run on 9 October succeeded. Its history also contains editorial changes, including the 9 October catalog/selection revision. Treat the automated commits separately when assessing curation.

### Curation and link health as separate jobs

[hexsecs](https://github.com/hexsecs/awesome-embedded-security) groups resources into software, hardware, and learning, then refines by investigation task. Descriptions explain the purpose, and markers identify commercial or archived resources. Its [contribution guide](https://github.com/hexsecs/awesome-embedded-security/blob/main/contributing.md) sets concrete admission and formatting rules.

Its [entry-health workflow](https://github.com/hexsecs/awesome-embedded-security/blob/main/.github/workflows/entry-health.yml) checks repository decay that HTTP availability cannot detect; the sampled 8 October scheduled run succeeded. A separate web-health workflow reviews non-GitHub resources. This is a stronger maintenance model than assuming an HTTP 200 response means a recommendation remains useful.

### Split by domain when the catalog needs it

[Reversing.ID](https://github.com/ReversingID/Awesome-Reversing) separates software, hardware, formats, and databases into four pages. Within software, it separates learning, static analysis, dynamic analysis, automation, and protection-related tools. This is an effective domain map, although the May reorganization alone does not establish regular maintenance.

[VelocityRa](https://github.com/VelocityRa/awesome-game-file-format-reversing) recently split a large catalog into a root index and `list/` files, organized around engines and games. Its 1 October commit explicitly cites GitHub's README rendering limit. A [workflow](https://github.com/VelocityRa/awesome-game-file-format-reversing/blob/master/.github/workflows/continuous-integration.yml) checks structure and links, and a separate workflow builds a documentation site. The latest sampled CI run failed while the site build succeeded; configured automation should not be described as uniformly healthy.

For the initial version of this list, one browsable README is sufficient. Split a section when it becomes hard to navigate, retaining a short index and links between related tasks.

### Contextual descriptions and learning routes

[ZX41R](https://github.com/ZX41R/awesome-reverse-engineering-and-malware-analysis) provides investigation tracks and topic directories, with tags for resource type, level, and access restrictions. Its [reverse-engineering page](https://github.com/ZX41R/awesome-reverse-engineering-and-malware-analysis/tree/main/reverse-engineering) puts learning resources alongside analysis tools. The idea to adopt is describing whom an entry helps and what to do with it.

There are limits to the maintenance evidence: some tracks describe future sections, the current `.github` directory has no workflow, and the latest sampled link-check runs are failures from July. September topic commits show later content activity, but this review does not establish a currently successful automated link-check process.

### Structured data for a larger catalog

[TheQmaks](https://github.com/TheQmaks/awesome-web-reversing) separates workflow documentation from source data and a generated catalog. Its [weekly verification workflow](https://github.com/TheQmaks/awesome-web-reversing/blob/main/.github/workflows/verify.yml) refreshes GitHub metadata; sampled scheduled runs on 28 September and 5 October succeeded.

This is a useful pattern when filters, generated pages, or agent-readable queries become necessary. Its lifecycle labels are based largely on push age, which remains a proxy for usefulness. This repository starts with Markdown to avoid maintaining a generator before there is a need for one.

## Decisions for this repository

- Open with a task-based selection table and a short scope statement.
- Organize the initial catalog by work: learning, triage, native analysis, runtime analysis, managed code, web/protocols, firmware/hardware, formats, diffing/frameworks, and AI-assisted analysis.
- Use one-sentence descriptions with canonical links and disclose commercial dependencies or maintainer ownership.
- Keep deep specialist catalogs in related lists; write new descriptions rather than copying another list wholesale.
- Add contribution guidance, a pull-request template, CC0 licensing, and a weekly/PR link-check workflow.
- Keep this comparison dated. Review compatibility, archive status, and alternatives during editorial updates; automated availability checks cover only part of maintenance.

These choices also follow the [Awesome manifesto](https://github.com/sindresorhus/awesome/blob/main/awesome.md): a defined scope, useful descriptions, consistent categories, contribution guidance, and a suitable content license.
