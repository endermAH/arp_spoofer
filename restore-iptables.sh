#!/bin/bash

iptables -F
iptables -t nat -F

# Accept from loopback
iptables -A INPUT -i lo -j ACCEPT

# Accept established connctions
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# DNS
iptables -A INPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p udp --sport 53 --dport 1024:65535 -j ACCEPT

# DHCP
iptables -I INPUT -p udp -i enp0s8 --dport 67 -j ACCEPT

#ICMP
iptables -A INPUT -p icmp -i enp0s8 -j ACCEPT

#Forwarding
iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -p icmp -j ACCEPT
iptables -A FORWARD -i enp0s8 -o enp0s3 -j ACCEPT
iptables -P FORWARD DROP

# Block requests from outside
iptables -A INPUT -m state --state NEW -i enp0s3 -j DROP
iptables -P INPUT DROP

# Enable NAT
iptables -t nat -A POSTROUTING -s 192.168.56.0/24 -j MASQUERADE
