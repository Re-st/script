#!/bin/bash

# 파일 경로 확인
if [ $# -eq 0 ]; then
    echo "사용법: $0 <텍스트 파일 경로>"
    exit 1
fi

# 대문자 3개 이상 이어지거나 대문자 괄호로 시작하는 경우 줄 바꾸기
awk '{
    for (i=1; i<=NF; i++) {
        if (match($i, "\\[INAUDIBLE\\]") || match($i, "\\[LAUGHTER\\]") || (i > 1 && match($(i-1), /^[A-Z]{3,}$/))) {
            printf "%s ", $i
        } else if (match($i, /^[A-Z]{3,}$/) || (substr($i, 1, 1) == "[" && match($i, /\[[A-Z]{3,}\]/)) || (substr($i, length($i), 1) == "]" && match($i, /[A-Z]{3,}\]/))) {
            printf "\n%s ", $i
        } else {
            printf "%s ", $i
        }
    }
    print ""
}' "$1"
