#!/usr/bin/env bash

set -e

# Allows case match on number
shopt -s extglob
end=$((${1} + 10))
main() {
	case $1 in
		+([0-9]))
			while true; do
				urlArr=`head --lines=${end} good-urls.txt | tail`
				echo "current URLs:"
				echo $urlArr
				for item in "${urlArr[@]}"; do processLink item 
				done
				end=$((${end} + 10))
				read -p "press any key to open 10 more" -n1 -s
			done
			;;
		*)
			echo "Argument not recognized."
			displayHelp
			exit 1
			;;
	esac
exit 0
}

function processLink(){
	echo $1
	# Redirect stderr to circumvent Chrome error message 
	# google-chrome $1 2>/dev/null
}
function displayHelp()
{
	echo "Usage:"
	echo "yeildURLs {line number to start on}"
}

main "$@"; 
