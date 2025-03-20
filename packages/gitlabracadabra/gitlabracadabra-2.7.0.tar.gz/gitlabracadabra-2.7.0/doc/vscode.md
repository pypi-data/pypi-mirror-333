# Visual Studio Code configuration

Configure `<WORKSPACE>/.vscode/launch.json`:

```json
{
    "configurations": [
        {
            "name": "Docker: Python - General",
            "type": "docker",
            "request": "launch",
            "preLaunchTask": "docker-run: debug",
            "python": {
                "pathMappings": [
                    {
                        "localRoot": "${workspaceFolder}",
                        "remoteRoot": "/app"
                    }
                ],
                "projectType": "general"
            }
        }
    ]
}
```

Configure `<WORKSPACE>/.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "docker-build",
      "label": "docker-build",
      "platform": "python",
      "dockerBuild": {
        "tag": "gitlabracadabra:latest",
        "dockerfile": "${workspaceFolder}/Dockerfile",
        "context": "${workspaceFolder}",
        "pull": true
      }
    },
    {
      "type": "docker-run",
      "label": "docker-run: debug",
      "dependsOn": [
        "docker-build"
      ],
      "dockerRun": {
        "network": "host"
      },
      "python": {
        "module": "gitlabracadabra.cli",
        "args": [ "-c <CONF_PATH>/.python-gitlab.cfg", "--dry-run",  "-g gitlab", "--debug", "--verbose","<CONF_PATH>/<ACTION_FILE>.yml"]
      }
    }
  ]
}
```

NOTE: Docker Network `host` is important if you want to apply to a local gitlab.
