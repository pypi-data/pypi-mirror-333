def format_output(cert_details):
    """Format output for console display."""
    output = "SSL CERTIFICATE ANALYZER\n============================\n"
    for key, value in cert_details.items():
        output += f"\n{key.upper()}\n--------------------------\n"
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                output += f"{subkey}: {subvalue}\n"
        else:
            output += f"{value}\n"
    return output
