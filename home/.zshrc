# Enable mise - polyglot runtime manager
eval "$(/Users/sanhehu/.local/bin/mise activate zsh)"

# Enable starship - cross-platform shell prompt
eval "$(starship init zsh)"

# Enable zsh-autosuggestions
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh

# Enable zsh-syntax-highlighting
source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# Enable zsh-completions
fpath=(~/.zsh/zsh-completions/src $fpath)

# Alias
alias ccc="claude"
alias ggg="gemini"
