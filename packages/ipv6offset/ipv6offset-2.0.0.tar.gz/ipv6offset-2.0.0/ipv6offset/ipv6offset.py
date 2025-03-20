import sys
from netaddr import IPAddress

def main():
    if len(sys.argv) != 4:
        print("Usage: ipv6offset <IPv6_Address> <+|-> <Number>")
        sys.exit(1)

    ip = IPAddress(sys.argv[1])
    operator = sys.argv[2]
    num = int(sys.argv[3])

    if operator == '+':
        result_ip = ip + num
    elif operator == '-':
        result_ip = ip - num
    else:
        print("Operator Must Be '+' Or '-'")
        sys.exit(1)

    print(result_ip)

#if __name__ == "__main__":
#    main()
