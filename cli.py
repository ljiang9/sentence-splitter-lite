"""命令行：python3 cli.py "待分句文本" """
import argparse
import json
import sys

from splitter import split_sentences


def main(argv=None):
    p = argparse.ArgumentParser(description="sentence-splitter-lite 中英文分句")
    p.add_argument("text", nargs="?", help="待分句文本")
    p.add_argument("--json", action="store_true", help="以 JSON 数组输出")
    args = p.parse_args(argv)

    text = args.text or sys.stdin.read()
    sents = split_sentences(text)
    if args.json:
        print(json.dumps(sents, ensure_ascii=False, indent=2))
    else:
        for idx, s in enumerate(sents, 1):
            print(f"{idx}. {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
