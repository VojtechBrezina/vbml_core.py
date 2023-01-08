NAME := $(shell basename `realpath .`)

install: .install_path
	@if [ -e `cat .install_path`/$(NAME) ]; then echo "Replacing."; rm `cat .install_path`/$(NAME); fi
	ln -sT `realpath src` `cat .install_path`/$(NAME)

uninstall:
	@if [ -f .install_path ]; then  rm `cat .install_path`/$(NAME); echo "Uninstalled. (You can remove .install_path if you want.)"; else echo "Cannot find the install path."; fi

autodetect:
	@echo "Picking first nonempty entry from "'$$PYTHONPATH'"."
	echo $$PYTHONPATH | tr ':' '\n' | tr -s '\n' | awk '{if($$0 != "") print($$0);}' | head -n 1 > .install_path
	@echo "Found `cat .install_path`."

.install_path:
	@echo -n "Please specify the install path: "; read install_path; echo $$install_path > .install_path

.PHONY: install uninstall
