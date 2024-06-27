import shodan
import socket
import ipaddress
import os

# Shodan API key (replace with your own key)
SHODAN_API_KEY = os.getenv('SHODAN_API_KEY')

# Initialize the Shodan API client
api = shodan.Shodan(SHODAN_API_KEY)

def get_ip_list(input_str):
    def is_valid_ip(address):
        try:
            ipaddress.ip_address(address)
            return True
        except ValueError:
            return False

    def is_valid_cidr(address):
        try:
            ipaddress.ip_network(address, strict=False)
            return True
        except ValueError:
            return False

    def get_ip(domain):
        try:
            ip = socket.gethostbyname(domain)
            return [ip]
        except socket.gaierror as e:
            print(f'Error: {e}')
            return []

    if is_valid_ip(input_str):
        return [input_str]
    elif is_valid_cidr(input_str):
        network = ipaddress.ip_network(input_str, strict=False)
        return [str(ip) for ip in network]
    else:
        return get_ip(input_str)

def query_shodan_for_host(ip, output_file):

    # import ipdb
    # ipdb.set_trace()


    ip_list = get_ip_list(ip)
    
    web_ips = dict()

    web = 0

    try:
        # Perform the Shodan host search

        for ip in ip_list:

            host = api.host(ip)

            # Append the results to the output file
            with open(output_file, 'a') as file:
                file.write(f"IP: {host['ip_str']}\n")
                file.write(f"Organization: {host.get('org', 'n/a')}\n")
                file.write("Ports:\n")
                for item in host['data']:
                    file.write(f"  Port: {item['port']}\n")
                    if item['port'] == 80:
                        web += 1
                    elif item['port'] == 443:
                        web += 2
                    file.write(f"    Service: {item.get('product', 'n/a')}\n")
                    file.write(f"    Version: {item.get('version', 'n/a')}\n")
                    cves = item.get('vulns', [])
                    if cves:
                        file.write("    CVEs:\n")
                        for cve in cves.items():
                            file.write(f"      {cve[0]}\n")
                        # for cve, info in cves.items():
                            # file.write(f"      {cve}: {info.get('summary', 'n/a')}\n")
                file.write("\n")

            print(f"Results for {ip} written to {output_file}")

            web_ips[ip] = web
        
    
    except Exception as e:
        print(f"Error: {e}")

    return web_ips

    

def main():
    pass

if __name__ == '__main__':
    main()