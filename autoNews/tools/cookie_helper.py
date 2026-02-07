#!/usr/bin/env python3
"""
Cookie Helper - 辅助工具，帮助导入和验证Cookie
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.session_manager import SessionManager
from src.utils.logger import setup_logger, get_logger

setup_logger(level="INFO")
logger = get_logger()


def import_cookie_from_browser(source_name: str, cookie_json: str):
    """
    从浏览器导出的JSON导入Cookie

    Args:
        source_name: 源名称
        cookie_json: Cookie JSON字符串或文件路径
    """
    try:
        # 判断是文件路径还是JSON字符串
        if cookie_json.endswith('.json') and Path(cookie_json).exists():
            with open(cookie_json, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
        else:
            cookies = json.loads(cookie_json)

        # 保存到标准位置
        cookie_dir = Path("data/cookies")
        cookie_dir.mkdir(parents=True, exist_ok=True)

        cookie_file = cookie_dir / f"{source_name}.json"

        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)

        logger.info(f"✓ Cookie已保存到: {cookie_file}")
        logger.info(f"  共 {len(cookies)} 个Cookie项")

        return True

    except Exception as e:
        logger.error(f"✗ 导入Cookie失败: {e}")
        return False


def validate_cookie(source_name: str, test_url: str):
    """
    验证Cookie是否有效

    Args:
        source_name: 源名称
        test_url: 测试URL
    """
    try:
        session_manager = SessionManager()

        # 加载Cookie
        session = session_manager.get_session(
            source_name,
            {'cookies': 'auto'}
        )

        # 测试请求
        logger.info(f"测试URL: {test_url}")
        response = session.get(test_url, timeout=15)

        logger.info(f"状态码: {response.status_code}")

        if response.ok:
            logger.info("✓ Cookie有效！")
            return True
        else:
            logger.warning(f"✗ 请求失败: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"✗ 验证失败: {e}")
        return False


def list_cookies(source_name: str = None):
    """
    列出已保存的Cookie

    Args:
        source_name: 源名称（可选，None表示列出所有）
    """
    cookie_dir = Path("data/cookies")

    if not cookie_dir.exists():
        logger.info("没有保存的Cookie")
        return

    if source_name:
        cookie_file = cookie_dir / f"{source_name}.json"
        if cookie_file.exists():
            with open(cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)

            logger.info(f"\n=== {source_name} ===")
            logger.info(f"文件: {cookie_file}")
            logger.info(f"Cookie数量: {len(cookies)}")
            logger.info(f"\nCookie内容:")
            for key, value in cookies.items():
                masked_value = value[:20] + "..." if len(value) > 20 else value
                logger.info(f"  {key}: {masked_value}")
        else:
            logger.info(f"没有找到 {source_name} 的Cookie")
    else:
        # 列出所有
        cookie_files = list(cookie_dir.glob("*.json"))

        if not cookie_files:
            logger.info("没有保存的Cookie")
            return

        logger.info(f"\n找到 {len(cookie_files)} 个Cookie文件:\n")

        for cookie_file in cookie_files:
            with open(cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)

            source = cookie_file.stem
            logger.info(f"  • {source}: {len(cookies)} 个Cookie")


def delete_cookie(source_name: str):
    """
    删除指定源的Cookie

    Args:
        source_name: 源名称
    """
    cookie_file = Path(f"data/cookies/{source_name}.json")

    if cookie_file.exists():
        cookie_file.unlink()
        logger.info(f"✓ 已删除 {source_name} 的Cookie")
        return True
    else:
        logger.warning(f"✗ 没有找到 {source_name} 的Cookie")
        return False


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="AutoNews Cookie管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:

1. 从浏览器导出的JSON导入Cookie:
   python tools/cookie_helper.py import "36氪" cookies.json

2. 直接粘贴JSON字符串导入:
   python tools/cookie_helper.py import "36氪" '{"session_id":"abc123"}'

3. 验证Cookie是否有效:
   python tools/cookie_helper.py validate "36氪" https://www.36kr.com/

4. 列出所有已保存的Cookie:
   python tools/cookie_helper.py list

5. 查看特定源的Cookie:
   python tools/cookie_helper.py list "36氪"

6. 删除Cookie:
   python tools/cookie_helper.py delete "36氪"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='命令')

    # import命令
    import_parser = subparsers.add_parser('import', help='导入Cookie')
    import_parser.add_argument('source', help='源名称')
    import_parser.add_argument('cookie_json', help='Cookie JSON文件路径或JSON字符串')

    # validate命令
    validate_parser = subparsers.add_parser('validate', help='验证Cookie')
    validate_parser.add_argument('source', help='源名称')
    validate_parser.add_argument('url', help='测试URL')

    # list命令
    list_parser = subparsers.add_parser('list', help='列出Cookie')
    list_parser.add_argument('source', nargs='?', help='源名称（可选）')

    # delete命令
    delete_parser = subparsers.add_parser('delete', help='删除Cookie')
    delete_parser.add_argument('source', help='源名称')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'import':
        import_cookie_from_browser(args.source, args.cookie_json)

    elif args.command == 'validate':
        validate_cookie(args.source, args.url)

    elif args.command == 'list':
        list_cookies(args.source)

    elif args.command == 'delete':
        delete_cookie(args.source)


if __name__ == "__main__":
    main()
