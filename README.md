# <img height="36" src="https://raw.githubusercontent.com/source-foundry/Slice/main/src/resources/img/slice-icon.svg"/>  Slice

### An open-source application to create custom font design spaces from variable fonts

<img src="https://d33wubrfki0l68.cloudfront.net/faa7cb26d3ad28e0fced37690d416503081be711/10796/images/slice-hero-crunch.png">

## About

Slice is an open-source, cross-platform GUI app that generates fonts with custom design sub-spaces from variable font inputs.

## Install

* macOS: [Slice.0.7.1.dmg](https://github.com/source-foundry/Slice/releases/download/v0.7.1/Slice.0.7.1.dmg)
* Windows: [Slice-0.7.1-Installer.exe](https://github.com/source-foundry/Slice/releases/download/v0.7.1/Slice-0.7.1-Installer.exe)

Please see the [Installation docs](https://slice-gui.netlify.app/docs/install/) for additional details, including available package manager installation/upgrade approaches.

## User documentation

User docs are available at https://slice-gui.netlify.app/docs/

- [Installation](https://slice-gui.netlify.app/docs/install/)
- [Usage](https://slice-gui.netlify.app/docs/usage/)

## Axis definitions

Slice currently supports combinations of the following axis definition types in output fonts:

- Fixed instance locations
- Level 3 restricted axis ranges (must include original axis default value in the new, smaller axis range)<sup>[[1](#footnote1)]</sup>
- Full, original variable axis ranges

Define your font axes with the syntax in the table below.

|Axis definition | Axis Editor Syntax  | Example |
| --- | --- | --- |
| Fixed axis location| Integer or float value | `400.0` |
| Restricted axis range | Colon-delimited min:max integer or float range | `200:700` |
| Full axis range | Leave editor row blank | n/a |

## Issues

Please file issues on the [project tracker](https://github.com/source-foundry/Slice/issues).

## Contributing

Source contributions are welcome.  Please see the [Slice application developer documentation](https://slice-gui.netlify.app/docs/developer/#slice-source-code-contributions) for instructions on how to set up a local development environment and test your source changes.  Submit a pull request with any changes that you would like to share upstream.

The Slice documentation is maintained in a separate GitHub repository.  Please see the [Slice documentation developer docs](https://slice-gui.netlify.app/docs/developer/#slice-documentation-contributions) for additional details about how to modify documentation content and set up a local testing environment.

Contributions to this project are accepted under the licenses specified in the [Licenses](#Licenses) section below.

## Licenses

The Slice project is licensed under the GNU General Public License version 3. Please see the [LICENSE](LICENSE) document for details.

Please see the [thirdparty directory](https://github.com/source-foundry/Slice/tree/main/thirdparty) for additional details about third-party licenses.

## Acknowledgments

❤️ Slice slices with the fantastic [fonttools Python library](https://github.com/fonttools/fonttools).

❤️ Slice uses the wonderful [Recursive](https://github.com/arrowtype/recursive) (sliced with Slice!) and [IBM Plex](https://github.com/IBM/plex) typefaces in the UI.

⚡ [Slice docs](https://slice-gui.netlify.app/) are powered by Netlify ([doc sources](https://github.com/source-foundry/Slice-docs)).

  <a href="https://www.netlify.com">
    <img src="https://www.netlify.com/img/global/badges/netlify-light.svg" alt="Deploys by Netlify" />
  </a>


---

<small><a id="footnote1">1</a>: Default axis locations are required to compile valid variable font format files.  The default axis value defined in the original font must be included in the restricted axis range due to the lack of compiler support for default axis location moves during the slicing process. We intend to support default axis location moves when it is possible to do so. [This issue is being tracked on our GitHub tracker](https://github.com/source-foundry/Slice/issues/32).</small>
