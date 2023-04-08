<p align="center">
  <h3 align="center">Army of AI Interns</h3>
</p>
<p align="center">
  pronounced <i><a href="https://www.youtube.com/watch?v=ge8lcPH-qMg">/aɪjɑ/</a></i>
</p>

This is my set of scripts, cronjobs, plugins and tools that allows me to command my own army of GPT powered AI interns.

Why? well.. well.. Why not?!
Let's see how far we can take this.

### Installation

```bash
 $ ./install
```

Then in your neovim `init.lua` add

```lua
{
    dir = "~/code/aiia/nvim/",
    config = function()
      require('aiia').setup()

      vim.keymap.set('v', '<C-g>r', require('aiia').replace, {
        silent = true,
        noremap = true,
        desc = "[G]pt [R]ewrite"
      })
      vim.keymap.set('v', '<C-g>p', require('aiia').visual_prompt, {
        silent = false,
        noremap = true,
        desc = "[G]pt [P]rompt"
      })
      vim.keymap.set('n', '<C-g>p', require('aiia').prompt, {
        silent = true,
        noremap = true,
        desc = "[G]pt [P]rompt"
      })
      vim.keymap.set('n', '<C-g>c', require('aiia').cancel, {
        silent = true,
        noremap = true,
        desc = "[G]pt [C]ancel"
      })
      vim.keymap.set('i', '<C-g>p', require('aiia').prompt, {
        silent = true,
        noremap = true,
        desc = "[G]pt [P]rompt"
      })
      vim.keymap.set('n', 'gsp', require("aiia").open_chatwindow, {
        silent = true,
        noremap = true,
        desc = '[G]oto [S]cratch [P]ad'
      })
    end
  }
```

### Usage

```bash
 $ aiia --help
```

