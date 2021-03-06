# Maintainer Documentation

## Create Draft GitHub Release

The GitHub release is automatically generated by GitHub Actions when a version formatted git tag is pushed to the remote.  This is configured to push a release in draft format so that installers can be uploaded and the release text can be updated with SHA hashes, VirusTotal scan links.

## Release Process

The application release version is updated in the following source files:

- `src/build/settings/base.json`
- `src/slice/__main__.py`

### macOS Release

#### References

- https://developer.apple.com/developer-id/
- https://help.apple.com/xcode/mac/current/#/dev033e997ca
- https://stackoverflow.com/a/53121755/2848172
- https://successfulsoftware.net/2018/11/16/how-to-notarize-your-software-on-macos/
- https://help.apple.com/xcode/mac/current/#/dev1cc22a95c

#### macOS Release Prep Process

In Python venv with project dev-requirements.txt dependencies installed:

##### Build the code signed app bundle and installer

```sh
make build-macos
make codesign-macos
make verify-codesign-macos
make build-macos-installer
make codesign-macos-installer
```

##### Push the installer to Apple for notarization

```sh
xcrun altool --notarize-app --type osx --primary-bundle-id "org.sourcefoundry.slice" --username [USERNAME] --password [APP-SPECIFIC PASSWORD] --file dist/*.dmg
```

##### Check the status of the notarization

```sh
xcrun altool --notarization-info [NOTARIZATION UUID] --username [USERNAME] --password [APP-SPECIFIC PASSWORD]
```

##### Staple the installer after notarization passes

After the notarization passes, enter:

```sh
xcrun stapler staple -v dist/*.dmg
```

Note that this does not require entry of data from the previous steps.  The notary data stapling is automated when you run this command after the notarization step passes.

The installer file is located on the path `dist/Slice[VERSION].dmg`.  This must be the dmg installer file that is released.  If any edits are made, start back at step 1 of the code signing and notarization process and begin again...

##### Push to VirusTotal

Upload installer to [VirusTotal](https://www.virustotal.com/gui/)

Copy VirusTotal URL and installer SHA256 hash to the GitHub release.

##### Upload installer to the GitHub release

Upload installer to the release.

##### Update the source-foundry/taproom Homebrew tap

Update the source-foundry/homebrew-taproom `Casks/sourcefoundry-slice` cask version number and SHA256 hash.  Commit and push to the repository to trigger user updates when they run `brew update && brew upgrade`.

### Windows Release

Powershell 7 on Win 10

In a Python venv with project dev-requirements.txt dependencies installed:

Activate venv on Windows:

```sh
.\venv\Scripts\activate
```

PyInstaller build of the application binary:

```sh
pyinstaller --noconfirm .\target\PyInstaller-Windows\Slice-Windows.spec
```

Generate the Windows Inno Setup installer:

- Launch Inno Setup
- Open the `target\InnoSetup-Windows\Slice-Installer.iss` ISS configuration file in the application
- Edit the Slice version string in the .iss configuration file
- Build the installer

The installer file is located on the path `dist\Windows-Installer\Slice-[VERSION]-Installer.exe`.

Upload installer to [VirusTotal](https://www.virustotal.com/gui/).

Copy VirusTotal URL and installer SHA256 hash to the GitHub release.

Upload installer to the GitHub release.

## Assets

### Fonts

The Recursive typeface is used for the application GUI title.  The v1.077 variable font was sliced @ MONO=0, CASL=0.5, wght=800, slnt=0, CRSV=1 settings to produce this instance.  It was subsequently subset with the pyftsubset executable to the character set "Slice". 
