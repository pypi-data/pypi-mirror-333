import argparse
from ssl_analyzer.analyzer import SSLAnalyzer
from ssl_analyzer.utils import format_output

def main():
    parser = argparse.ArgumentParser(description="Analyze SSL Certificates")
    parser.add_argument("domain", help="Domain to check SSL details")
    parser.add_argument("-J", "--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    ssl_analyzer = SSLAnalyzer(args.domain)
    details = ssl_analyzer.analyze(output_json=args.json)
    
    print(details if args.json else format_output(details))

if __name__ == "__main__":
    main()
