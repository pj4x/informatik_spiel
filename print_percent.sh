git fame | awk '
/^Total loc:/ { total=$3; next }

/^\|/ {
    split($0, cols, "|")
    author=cols[2]
    loc=cols[3]

    gsub(/^[ \t]+|[ \t]+$/, "", author)
    gsub(/^[ \t]+|[ \t]+$/, "", loc)

    if (author != "Author" && author != "" && total > 0) {
        printf "%-15s %6d LOC  %6.2f%%\n", author, loc, (loc/total)*100
    }
}
'
