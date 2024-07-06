return {
  {"folke/which-key.nvim", lazy = true },
  { "folke/neoconf.nvim", cmd = "Neoconf" },
  "folke/neodev.nvim",
  -- XXX: I want solarized back
  { "ellisonleao/gruvbox.nvim", priority = 1000 , config = true},
  {
    "ThePrimeagen/refactoring.nvim",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "nvim-treesitter/nvim-treesitter",
    },
    config = function()
      require("refactoring").setup()
    end,
  },
}
