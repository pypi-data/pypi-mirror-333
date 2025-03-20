parserOpts = {
  headerPattern: /^(?:(\w*)(?:\((.*)\))?!?: )?(.*)$/,
  mergePattern: /^Merge branch '(.*)' into '(.*)'$/,
  mergeCorrespondence: ['source', 'destination'],
}

module.exports = {
  "branches": [
    "main",
  ],

  "plugins": [
    [
      "@semantic-release/commit-analyzer",
      {
        "preset": 'conventionalcommits',
        "parserOpts": parserOpts,
        "releaseRules": [
          {breaking: true, release: 'major'},
          {revert: true, release: 'patch'},
          // {type: "build", release: "no-release"},
          {type: "chore", release: "patch"},
          // {type: "ci", release: "no-release"},
          // {type: "docs", release: "no-release"},
          {type: 'feat', release: 'minor'},
          {type: 'fix', release: 'patch'},
          {type: "perf", release: "minor"},
          // {type: "refactor", release: "no-release"},
          {type: "revert", release: "patch"},
          // {type: "style", release: "no-release"},
          // {type: "test", release: "no-release"},
          ]
      }
    ],

    [
      "@semantic-release/release-notes-generator",
      {
        "preset": "conventionalcommits",
        "parserOpts": parserOpts,
        "presetConfig": {
          "types": [
            {type:"feat", section:":sparkles: Features", hidden:false},
            {type:"fix",section:":bug: Fixes"},
            {type:"docs", section:":memo: Documentation"},
            {type:"style", section:":barber: Code-style"},
            {type:"refactor", section:":zap: Refactor"},
            {type:"perf", section:":fast_forward: Performance"},
            {type:"test", section:":white_check_mark: Tests"},
            {type:"ci", section:":repeat: CI"},
            {type:"chore", section:":repeat: Chore"},
            { type:"", section:":question: Unclassified"},
          ],
        },
      },
    ],

    [
      "@semantic-release/changelog",
      {
        "changelogFile": "CHANGELOG.md",
        "changelogTitle": "# Change Log"
      }
    ],

    [
      "@google/semantic-release-replace-plugin",
      {
        "replacements": [
          {
            "files": ["src/gitlabracadabra/__init__.py"],
            "from": "__version__ = \".*\"",
            "to": "__version__ = \"${nextRelease.version}\"",
            "results": [
              {
                "file": "src/gitlabracadabra/__init__.py",
                "hasChanged": true,
                "numMatches": 1,
                "numReplacements": 1
              }
            ],
            "countMatches": true
          },
          {
            "files": ["README.md"],
            "from": "'registry.gitlab.com/gitlabracadabra/gitlabracadabra:.*'",
            "to": "'registry.gitlab.com/gitlabracadabra/gitlabracadabra:v${nextRelease.version}'",
            "results": [
              {
                "file": "README.md",
                "hasChanged": true,
                "numMatches": 2,
                "numReplacements": 2
              }
            ],
            "countMatches": true
          }
        ]
      }
    ],

    [
      "@semantic-release/exec",
      {
        "prepareCmd": "dch -v '${nextRelease.version}' -D unstable 'New release'"
      }
    ],

    [
      "@semantic-release/git",
      {
        "assets": [
          "CHANGELOG.md",
          "README.md",
          "debian/changelog",
          "src/gitlabracadabra/__init__.py"
        ],
        "message": "chore(release): ${nextRelease.version}\n\n${nextRelease.notes}"
      }
    ],
  ],
}
