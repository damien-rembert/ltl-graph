#!/bin/bash

source .env.development

# Set the initial date
start_date=$(date --date "$GATSBY_RANGE_START_DATE" '+%Y-%m-%d')
end_date=$(date --date "$start_date +$GATSBY_STEP_SIZE_IN_DAYS days" '+%Y-%m-%d')

while [[ $(date --date "$end_date +$GATSBY_STEP_SIZE_IN_DAYS days" '+%s') -le $(date --date "$GATSBY_RANGE_END_DATE" '+%s') ]]
do
    echo "Starting, getting: $start_date"

    formatted_start_date=$(date --date "$start_date" '+%d/%m/%Y')
    formatted_end_date=$(date --date "$end_date" '+%d/%m/%Y')

    if [ ! -f "data/${AGGREGATE_ATTRIBUTE}/${start_date}_to_${end_date}.csv" ]; then

        curl --location "https://$API_URL/library/orgLoan/exportAggregateLoanReport" \
            --header "Host: $API_URL" \
            --header 'Accept: */*' \
            --header 'Accept-Language: en-GB,en;q=0.7,fr;q=0.3' \
            --header 'Accept-Encoding: gzip, deflate, br' \
            --header "Referer: https://$API_URL/" \
            --header 'User-Agent: curl for ltl-usage-graph' \
            --header 'Content-type: application/x-www-form-urlencoded' \
            --header "Origin: https://$API_URL" \
            --header 'DNT: 1' \
            --header 'Connection: keep-alive' \
            --header "Cookie: $COOKIE" \
            --header 'Sec-Fetch-Dest: empty' \
            --header 'Sec-Fetch-Mode: cors' \
            --header 'Sec-Fetch-Site: same-origin' \
            --header "host: $API_URL" \
            --data-urlencode "from_date=$formatted_start_date" \
            --data-urlencode 'from=struct' \
            --data-urlencode 'from_tz=Europe/London' \
            --data-urlencode 'from_time=00:00' \
            --data-urlencode "to_date=$formatted_end_date" \
            --data-urlencode 'to=struct' \
            --data-urlencode 'to_tz=Europe/London' \
            --data-urlencode 'to_time=23:59' \
            --data-urlencode "aggregateAttribute=$AGGREGATE_ATTRIBUTE" \
            --data-urlencode 'location.id=2806' \
            --data-urlencode 'format=csv' \
            --data-urlencode 'extension=csv' \
            --compressed \
            --output "data/${AGGREGATE_ATTRIBUTE}/${start_date}_to_${end_date}.csv"

        sleep 5
    else
        echo "data/${AGGREGATE_ATTRIBUTE}/${start_date}_to_${end_date}.csv already exists."
    fi

    # Increment the date for the next iteration
    start_date=$(date --date "$end_date +1 day" '+%Y-%m-%d')
    end_date=$(date --date "$start_date +$GATSBY_STEP_SIZE_IN_DAYS days" '+%Y-%m-%d')

done
    echo "Done."
