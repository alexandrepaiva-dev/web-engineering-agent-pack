choose_profile_interactive() {
  local default="${1:-core}"
  echo "Select global skill profile:"
  echo "1) core       - recommended globally"
  echo "2) nextjs     - CORE + Next.js stack"
  echo "3) symfony    - CORE + Symfony stack"
  echo "4) full       - both stacks"
  echo "5) nextjs-mysql"
  echo "6) symfony-postgresql"
  read -r -p "Choice [1]: " choice
  case "${choice:-1}" in
    1) echo "core" ;;
    2) echo "nextjs" ;;
    3) echo "symfony" ;;
    4) echo "full" ;;
    5) echo "nextjs-mysql" ;;
    6) echo "symfony-postgresql" ;;
    *) echo "Invalid profile choice" >&2; return 2 ;;
  esac
}

resolve_profile_skills() {
  local root="$1" profile="$2"
  shift 2
  local py="python3"
  command -v python3 >/dev/null 2>&1 || py="python"
  "$py" "$root/scripts/profile_manager.py" resolve --profile "$profile" "$@"
}
