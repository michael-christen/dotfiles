-- Changing the default f keyword
-- XXX: Consider enabling / remapping
-- vim.api.nvim_set_keymap('', 'f', "<cmd>lua require'hop'.hint_char1()<cr>", {})
return {
  "phaazon/hop.nvim",
  opts = {
    keys = 'etovxqpdygfblzhckisuran',
	term_seq_bias = 0.5,
  }
}
