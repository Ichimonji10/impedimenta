# coding=utf-8

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  help               to show this message"
	@echo "  lint               to run all linters"
	@echo "  lint-ansible-lint  to run ansible-lint"
	@echo "  lint-pylint        to run pylint"
	@echo "  lint-shellcheck    to run shellcheck"
	@echo "  lint-syntax-check  to run ansible-playbook --syntax-check"
	@echo "  lint-yamllint      to run yamllint"

lint: lint-syntax-check lint-ansible-lint lint-pylint lint-shellcheck lint-yamllint

# Execute `ansible-lint -L` to view all codes.
#
# 405: Remote package tasks should have a retry
#     I'm not going to do something as offensively stupid as put an infinite
#     retry loop in my code, as suggested by ansible-lint. Also, pacman already
#     offers basic retry logic when fetching packages. No need to waste time by
#     adding yet more retries here in Ansible.
#
# 501: become_user requires become to work as expected
#     ansible-lint doesn't know how to deal with the case where `become_user: …`
#     is applied directly to a task and `become: true` is applied to a task via
#     a block statement.
#
# 701: meta/main.yml should contain relevant info
#     These modules aren't being distributed on Ansible Galaxy.
lint-ansible-lint:
	ansible-lint -x 405,501,701 site.yml

lint-pylint:
	find . -type f -name '*.py' -print0 | xargs -0 pylint

lint-shellcheck:
	find . -type d -name templates -prune -o -type f -name '*.sh' -print0 | xargs -0 shellcheck

lint-syntax-check:
	ansible-playbook site.yml --syntax-check

lint-yamllint:
	yamllint --strict .

.PHONY: help lint lint-ansible-lint lint-pylint lint-shellcheck lint-syntax-check lint-yamllint
