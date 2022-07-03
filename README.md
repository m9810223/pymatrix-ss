# pymatrix

[![pypi](https://img.shields.io/pypi/v/pymatrix-ss?color=%2334D058)](https://pypi.org/project/pymatrix-ss/)

## Screensaver with zsh-morpho

![demo](./demo.svg)

1. Install

   ```shell
   pip install pymatrix-ss
   ```

    [![Typing SVG](https://readme-typing-svg.herokuapp.com/?lines=pip+install+pymatrix-ss)](https://pypi.org/project/pymatrix-ss/)

1. Open `~/.zshrc`
   1. add `zsh-morpho` to `plugins`
   1. config zsh-morpho

      ```shell
      zstyle ":morpho" screen-saver "pymatrix"
      zstyle ":morpho" delay "290"             # 5 minutes  before screen saver starts
      zstyle ":morpho" check-interval "60"     # check every 1 minute if to run screen saver
      ```
