#!/bin/bash
# Claude Code status line - displays session usage in VSCode interface

input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name // "Claude"')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
TOKENS_IN=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')
TOKENS_OUT=$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | awk '{printf "%d", $1}')
DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

# Format cost
COST_FMT=$(printf "%.4f" "$COST")

# Format duration
MINS=$(( DURATION_MS / 60000 ))
SECS=$(( (DURATION_MS % 60000) / 1000 ))

# Build context progress bar (10 chars)
FILLED=$(( PCT * 10 / 100 ))
EMPTY=$(( 10 - FILLED ))
BAR=$(printf '%0.s█' $(seq 1 $FILLED 2>/dev/null) 2>/dev/null)$(printf '%0.s░' $(seq 1 $EMPTY 2>/dev/null) 2>/dev/null)

echo "[$MODEL] | ctx: $BAR ${PCT}% | in: ${TOKENS_IN} / out: ${TOKENS_OUT} | cost: \$${COST_FMT} | time: ${MINS}m${SECS}s"