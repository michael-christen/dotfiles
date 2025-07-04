return {
  "epwalsh/obsidian.nvim",
  enabled = false, -- XXX: Makes ediiting large files, like logs, very annoying
  version = "*",  -- recommended, use latest release instead of latest commit
  lazy = true,
  ft = "markdown",
  -- Replace the above line with this if you only want to load obsidian.nvim for markdown files in your vault:
  -- event = {
  --   -- If you want to use the home shortcut '~' here you need to call 'vim.fn.expand'.
  --   -- E.g. "BufReadPre " .. vim.fn.expand "~" .. "/my-vault/**.md"
  --   "BufReadPre path/to/my-vault/**.md",
  --   "BufNewFile path/to/my-vault/**.md",
  -- },
  dependencies = {
    -- Required.
    "nvim-lua/plenary.nvim",
    -- for completion of note references
    "hrsh7th/nvim-cmp",
    -- for search and quick-switch functionality
    "nvim-telescope/telescope.nvim",
    -- for markdown syntax highlighting
    "nvim-treesitter/nvim-treesitter",
  },
  opts = {
    workspaces = {
      {
        name = "main",
        path = "~/notes",
      },
    },
    attachments = {
      img_folder = "media",
    },
  },
}
