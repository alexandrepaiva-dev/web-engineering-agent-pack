transactional_replace_dir() {
  local staged="$1"
  local target="$2"
  local old="${target}.weap-old-$$"

  rm -rf "$old"
  if [[ -e "$target" ]]; then
    mv "$target" "$old"
  fi

  if ! mv "$staged" "$target"; then
    rm -rf "$target"
    if [[ -e "$old" ]]; then mv "$old" "$target"; fi
    return 1
  fi

  rm -rf "$old"
}

transactional_replace_file() {
  local staged="$1"
  local target="$2"
  local old="${target}.weap-old-$$"

  rm -f "$old"
  if [[ -e "$target" ]]; then
    mv "$target" "$old"
  fi

  if ! mv "$staged" "$target"; then
    rm -f "$target"
    if [[ -e "$old" ]]; then mv "$old" "$target"; fi
    return 1
  fi

  rm -f "$old"
}

validate_skill_stage() {
  local stage="$1"
  local expected="$2"
  local count=0

  for d in "$stage"/*; do
    [[ -d "$d" ]] || continue
    [[ -f "$d/SKILL.md" ]] || { echo "Missing SKILL.md in $d" >&2; return 1; }
    count=$((count+1))
  done

  [[ "$count" -eq "$expected" ]] || {
    echo "Skill stage count mismatch: expected $expected, got $count" >&2
    return 1
  }
}
