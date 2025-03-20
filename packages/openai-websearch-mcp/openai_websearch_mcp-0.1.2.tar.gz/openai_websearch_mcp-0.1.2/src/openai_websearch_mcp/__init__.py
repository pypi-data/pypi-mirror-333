from .server import mcp


def main():
    """OpenAI WebSearch MCP Server"""
    import argparse

    parser = argparse.ArgumentParser(
        description="give a model the ability to handle time queries and timezone conversions"
    )
    parser.add_argument("--transport", type=str, help="Transport to use", default="stdio")

    args = parser.parse_args()
    mcp.run(args.transport)


if __name__ == "__main__":
    main()