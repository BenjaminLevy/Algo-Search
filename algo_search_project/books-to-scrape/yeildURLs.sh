#!/usr/bin/env bash

set -e

# Allows case match on number
shopt -s extglob
end=$((${1} + 10))
main() {
	case $1 in
		+([0-9]))
			urlArr=`head --lines=${end} book-urls.txt | tail`
			echo "current URLs:"
			echo $urlArr
			# Redirect stderr to circumvent Chrome error message 
			for item in "${urlArr[@]}"; do google-chrome $item 2>/dev/null; done
			;;
		*)
			echo "Argument not recognized."
			displayHelp
			exit 1
			;;
	esac
exit 0
}
function displayHelp()
{
	echo "Usage:"
	echo "yeildURLs {line number to start on}"
}
main "$@"; 
