return {
  "linrongbin16/gitlinker.nvim",
  config = function()
    require"gitlinker".setup({
      cmd = "GitLink",
      opts = {},
      keys = {
        { "<leader>ty", "<cmd>GitLink remote=origin<cr>", mode = { "n", "v" }, desc = "Yank git link" },
        { "<leader>tY", "<cmd>GitLink! remote=origin<cr>", mode = { "n", "v" }, desc = "Open git link" },
      },
      router = {
        browse = {
          ["^github%.corp%.astranis%.space"] = "https://github.corp.astranis.space/"
            .. "{_A.ORG}/"
            .. "{_A.REPO}/blob/"
            .. "{_A.REV}/"
            .. "{_A.FILE}"
            .. "#L{_A.LSTART}"
            .. "{_A.LEND > _A.LSTART and ('-L' .. _A.LEND) or ''}",
        },
      },
    })
  end
}
