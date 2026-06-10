# updating vsCode with the help of apt

- we want to make sure that we had added the given bellow repos to the apt so that we can confirms apt successfully reached out to Microsoft's official servers to check for updates.

```bash
Get:2 https://packages.microsoft.com/repos/code stable InRelease [3,590 B]         
Get:3 https://packages.microsoft.com/repos/code stable/main amd64 Packages [25.2 kB]
```

*After making sure that is is added, then we can run the following comments to update the vscode*

```bash
sudo apt update
sudo apt --only-upgrade install code
```

When updating if it says "code is already the newest version" and the vsCode is showing the update notification it means Microsoft just pushed the update to their update server, triggering the in-app notification. However, it usually takes anywhere from a few hours to a day for them to sync and build the Linux .deb packages in their apt repository.