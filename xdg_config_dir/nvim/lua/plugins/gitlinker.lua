-- XXX: Not working, but could link
-- https://github.com/vincent178/nvim-github-linker
return {
  "ruifm/gitlinker.nvim",
  -- lazy = true,
  opts = {
    -- opts = {
    --   remote = nil, -- force the use of a specific remote
    --   -- adds current line nr in the url for normal mode
    --   add_current_line_on_normal_mode = true,
    --   -- callback for what to do with the url
    --   action_callback = require"gitlinker.actions".copy_to_clipboard,
    --   -- print the url after performing the action
    --   print_url = true,
    -- },
    -- callbacks = {
    -- 	  -- XXX: Revisit
    --       ["github.com"] = require"gitlinker.hosts".get_github_type_url,
    --       ["git.kernel.org"] = require"gitlinker.hosts".get_cgit_type_url,
    -- },
    --   default mapping to call url generation with action_callback
    mappings = "<leader>gh"
  }
}
