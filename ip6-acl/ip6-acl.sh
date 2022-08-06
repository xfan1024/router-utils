#!/bin/sh

lan=br-lan
allowed_file=/root/ip6_allowed_mac

ip6_allowed_mac(){
    grep -o '^[^#]*' "$allowed_file"
}

__ip6_acl_down(){
    ebtables -D INPUT  --logical-in  $lan -p IPv6 -j ip6_filter_input
    ebtables -D OUTPUT --logical-out $lan -p IPv6 -j ip6_filter_output
    ebtables -X ip6_filter_input
    ebtables -X ip6_filter_output
}

ip6_acl_down(){
    __ip6_acl_down 2>/dev/null
}

ip6_acl_up(){
    ip6_acl_down
    ebtables -N ip6_filter_input
    ebtables -N ip6_filter_output
    ebtables -P ip6_filter_input DROP
    ebtables -P ip6_filter_output DROP
    ebtables -A INPUT  --logical-in  $lan -p IPv6 -j ip6_filter_input
    ebtables -A OUTPUT --logical-out $lan -p IPv6 -j ip6_filter_output
    ebtables -A ip6_filter_output -d Multicast -j RETURN
    ip6_allowed_mac | while read mac
    do
        ebtables -A ip6_filter_input  -s "$mac" -j RETURN
        ebtables -A ip6_filter_output -d "$mac" -j RETURN
    done
}

case $1 in
    up|down)
        ip6_acl_$1
        ;;
    *)
        echo "usage $0 up|down"
        exit 1
esac

