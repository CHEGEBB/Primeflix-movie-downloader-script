#!/bin/bash

function download_file {
    local url="$1"
    local output_path="$2"

    if command -v wget &>/dev/null; then
        wget -O "$output_path" "$url"
    elif command -v curl &>/dev/null; then
        curl -o "$output_path" "$url"
    else
        echo "Error: Neither 'wget' nor 'curl' is installed. Please install one of them."
        exit 1
    fi

    echo "File downloaded successfully to $output_path"
}

function search_content {
    local content_type="$1"

    while true; do
        read -p "Enter the $content_type name: " content_name
        if [ -n "$content_name" ]; then
            break
        fi
        echo "Invalid input. Please enter a valid name."
    done

    name_query=$(echo "$content_name" | tr ' ' '+')
    result=$(curl -s "https://mycima.cloud/search/$name_query")

    content_info=$(echo "$result" | grep -o '<div class="Thumb--GridItem">.*</div>' | sed 's/<[^>]*>//g')

    if [ -z "$content_info" ]; then
        echo "No matching $content_type found. Please try again."
        return 1
    fi

    if [ "$(echo "$content_info" | wc -l)" -gt 1 ]; then
        echo "$content_info" | nl -w2 -s": " -b a
        while true; do
            read -p "Choose a $content_type by entering its index: " choice
            if [ "$choice" -ge 0 ] && [ "$choice" -lt "$(echo "$content_info" | wc -l)" ]; then
                content_link=$(echo "$result" | grep -o '<div class="Thumb--GridItem">.*</div>' | sed -n "${choice + 1}s/.*<a href=\"\([^\"]*\)\".*/\1/p")
                echo "$content_link"
                return 0
            else
                echo "Invalid choice. Please enter a valid index."
            fi
        done
    else
        content_link=$(echo "$result" | grep -o '<div class="Thumb--GridItem">.*</div>' | sed -n 's/.*<a href=\"\([^\"]*\)\".*/\1/p')
        echo "$content_link"
        return 0
    fi
}

function main {
    clear
    cat << "EOF"
 ________        .__                        ___________.__  .__        
 \______   \_______|__| _____   ____          \_   _____/|  | |__|__  ___
  |     ___/\_  __ \  |/     \_/ __ \   ______ |    __)  |  | |  \  \/  /
  |    |     |  | \/  |  Y Y  \  ___/  /_____/ |     \   |  |_|  |>    < 
  |____|     |__|  |__|__|_|  /\___  >         \___  /   |____/__/__/\_ \
                            \/     \/              \/                  \/
EOF
    echo "Written by CHEGEBB"
    echo -e "\nWelcome to Primeflix"

    while true; do
        echo -e "\nChoose what to download:"
        echo "1. Movie"
        echo "2. TV Series"
        echo "3. Links to other download sites (Coming Soon)"
        echo "4. Exit"

        read -p "Enter your choice: " choice

        case $choice in
            1)
                movie_link=$(search_content "movie")
                if [ -n "$movie_link" ]; then
                    output_path="$HOME/Downloads/movie_file.mp4"
                    download_file "$movie_link" "$output_path"
                else
                    echo "No valid download links found for the selected movie."
                fi
                ;;
            2)
                series_link=$(search_content "TV series")
                if [ -n "$series_link" ]; then
                    output_path="$HOME/Downloads/series_file.mp4"
                    download_file "$series_link" "$output_path"
                else
                    echo "No valid download links found for the selected TV series."
                fi
                ;;
            3)
                echo "Links to other download sites functionality coming soon!"
                ;;
            4)
                echo "Thank you for using Primeflix. Goodbye!"
                exit 0
                ;;
            *)
                echo "Invalid choice. Please enter a valid option."
                ;;
        esac
    done
}

main
