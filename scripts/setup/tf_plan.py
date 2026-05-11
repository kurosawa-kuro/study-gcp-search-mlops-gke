"""`terraform plan` wrapper that validates required vars + saves the plan to
infra/tfplan so the follow-up `terraform apply tfplan` is reproducible.

Defaults come from `env/config/setting.yaml` (`github_repo` / `oncall_email` /
`public_domain` / `dns_zone_name`) via `scripts._common`. The canonical
`-var=...` set is built by `terraform_var_args()` (single source of truth shared
with tf_apply / destroy_all / recover_wif / state_recovery) — adding a var name
to `CANONICAL_TF_VAR_NAMES` propagates here automatically. Override at the CLI
with env vars `GITHUB_REPO=...` / `ONCALL_EMAIL=...` for ad-hoc plans against
another repo / oncall address.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from scripts._common import DEFAULTS, _load_list_setting, fail, terraform_var_args
from scripts.domain.terraform.lock import run_terraform_streaming_with_lock_retry

INFRA = Path(__file__).resolve().parents[2] / "infra" / "terraform" / "environments" / "dev"


def main() -> int:
    github_repo = os.environ.get("GITHUB_REPO") or DEFAULTS.get("GITHUB_REPO", "")
    oncall_email = os.environ.get("ONCALL_EMAIL") or DEFAULTS.get("ONCALL_EMAIL", "")
    # `admin_user_emails:` は YAML block list なので専用 loader で読む。
    # 空 list は Terraform 側で binding 無しになる (default `[]`)。
    admin_user_emails = _load_list_setting("admin_user_emails")

    if not oncall_email or "@" not in oncall_email:
        return fail(
            "ONCALL_EMAIL must be a non-empty address containing '@' (terraform variables.tf "
            "validation rejects anything else).\n"
            "Source: env/config/setting.yaml::oncall_email or env var ONCALL_EMAIL.\n"
            f"Got: {oncall_email!r}"
        )

    if not github_repo or "/" not in github_repo or github_repo == "owner/name":
        return fail(
            "GITHUB_REPO must be a real `<owner>/<name>` (not the placeholder).\n"
            "Source: env/config/setting.yaml::github_repo or env var GITHUB_REPO.\n"
            f"Got: {github_repo!r}"
        )

    run_terraform_streaming_with_lock_retry(
        [
            "terraform",
            f"-chdir={INFRA}",
            "plan",
            *terraform_var_args(),
            f"-var=admin_user_emails={json.dumps(admin_user_emails)}",
            "-out=tfplan",
        ],
        chdir_infra=INFRA,
    )
    print("==> Plan saved to infra/tfplan. Apply with: terraform -chdir=infra apply tfplan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
