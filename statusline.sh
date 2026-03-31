#!/usr/bin/env bash
input=$(cat)

cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // ""')
model=$(echo "$input" | jq -r '.model.display_name // ""')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
five_h=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
week=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

dir_part=$(basename "$cwd")

parts=()
separator=" | "

[ -n "$dir_part" ] && parts+=("$dir_part")
[ -n "$model" ] && parts+=("$model")

if [ -n "$used" ]; then
  parts+=("context :$(printf '%.0f' "$used")% $separator ")
fi

rate_part=""
if [ -n "$five_h" ]; then
  rate_part="5h:$(printf '%.0f' "$five_h")% $separator "
fi
if [ -n "$week" ]; then
  [ -n "$rate_part" ] && rate_part="$rate_part "
  rate_part="${rate_part}7d:$(printf '%.0f' "$week")% $separator "
fi
[ -n "$rate_part" ] && parts+=("$rate_part")

printf '%s' "$(IFS=' | '; echo "${parts[*]}")"
