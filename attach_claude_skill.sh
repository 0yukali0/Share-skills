#!/usr/bin/env bash
# Usage: ./attach_claude_skill.sh [skill_repo]
# No argument: copy all skills
# Example: ./attach_claude_skill.sh bbc_news

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

attach_skill() {
    local SKILL_REPO="$1"

    local SKILL_MD_SRC="${SCRIPT_DIR}/skills/${SKILL_REPO}/SKILL.md"
    local DIST_SKILL_DIR="${SCRIPT_DIR}/.claude/skills/${SKILL_REPO}"

    # Copy skills/<skill_repo>/SKILL.md -> dist/skills/<skill_repo>/SKILL.md
    mkdir -p "${DIST_SKILL_DIR}"
    cp "${SKILL_MD_SRC}" "${DIST_SKILL_DIR}/SKILL.md"
    echo "Copied: ${SKILL_MD_SRC} -> ${DIST_SKILL_DIR}/SKILL.md"
}

if [[ $# -eq 0 ]]; then
    # No argument: attach all skills found in skills/
    for skill_dir in "${SCRIPT_DIR}/skills"/*/; do
        skill_name="$(basename "${skill_dir}")"
        echo "=== ${skill_name} ==="
        attach_skill "${skill_name}"
    done
else
    attach_skill "$1"
fi
