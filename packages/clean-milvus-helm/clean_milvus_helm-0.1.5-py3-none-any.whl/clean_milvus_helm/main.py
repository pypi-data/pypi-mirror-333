#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime, timedelta
import sys
import click


def parse_time(time_str):
    """Parse time string, handle different timezone formats"""
    # Remove timezone info before parsing
    time_str = time_str.split()[0]  # Only take the date time part
    return datetime.strptime(time_str, '%Y-%m-%d')


def get_releases_to_delete(dry_run=True, days=3, chart_types=None, exclude_releases=None, exclude_prefixes=None):
    """
    Get a list of helm releases that should be deleted based on criteria
    
    Args:
        dry_run (bool): If True, only show what would be deleted
        days (int): Delete releases older than this many days
        chart_types (list): List of chart types to process
        exclude_releases (list): List of release names to exclude from deletion
        exclude_prefixes (list): List of release name prefixes to exclude from deletion
    """
    if chart_types is None:
        chart_types = ['milvus', 'etcd', 'minio', 'kafka', 'pulsar']
        
    if exclude_releases is None:
        exclude_releases = []
        
    if exclude_prefixes is None:
        exclude_prefixes = []

    try:
        # Execute helm ls command and get JSON output
        result = subprocess.run(
            ['helm', 'ls', '-o', 'json'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error executing helm ls: {result.stderr}")
            return

        # Parse JSON output
        releases = json.loads(result.stdout)
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(days=days)

        releases_to_delete = []

        for release in releases:
            # Get base chart name (e.g., get 'milvus' from 'milvus-4.2.0')
            base_chart = release['chart'].split('-')[0].lower()

            if base_chart not in chart_types:
                continue
                
            # Skip releases that are in the exclude list
            if release['name'] in exclude_releases:
                continue
                
            # Skip releases that start with any of the excluded prefixes
            if any(release['name'].startswith(prefix) for prefix in exclude_prefixes):
                continue

            update_time = parse_time(release['updated'])

            if update_time < cutoff_time:
                releases_to_delete.append({
                    'name': release['name'],
                    'namespace': release['namespace'],
                    'chart': release['chart'],
                    'update_time': update_time,
                    'app_version': release.get('app_version', 'N/A')
                })

        if releases_to_delete:
            print(f"\n找到 {len(releases_to_delete)} 个需要删除的releases:")
            print("-" * 80)

            # Sort by update time, oldest first
            releases_to_delete.sort(key=lambda x: x['update_time'])

            for release in releases_to_delete:
                print(f"名称: {release['name']}")
                print(f"命名空间: {release['namespace']}")
                print(f"Chart: {release['chart']} (应用版本: {release['app_version']})")
                print(f"更新时间: {release['update_time']}")
                print(f"删除命令: helm uninstall {release['name']} -n {release['namespace']}")
                print("-" * 80)

            if not dry_run:
                response = input("\n是否确认删除这些releases? (yes/no): ")
                if response.lower() == 'yes':
                    for release in releases_to_delete:
                        cmd = f"helm uninstall {release['name']} -n {release['namespace']}"
                        print(f"\n执行命令: {cmd}")
                        try:
                            subprocess.run(cmd, shell=True, check=True)
                            print(f"成功删除 {release['name']}")
                        except subprocess.CalledProcessError as e:
                            print(f"删除 {release['name']} 时出错: {e}")
                else:
                    print("取消删除操作。")
            else:
                print("\n试运行模式：不会实际删除任何releases")
                print("要实际删除releases，请使用 --execute 参数运行脚本")
        else:
            print(f"没有找到符合条件的releases (早于 {days} 天且chart类型在 {chart_types} 中)")

    except json.JSONDecodeError as e:
        print(f"解析helm命令输出为JSON时出错: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


@click.command(help='清理旧的Helm releases')
@click.option(
    '--execute/--dry-run', 
    default=False, 
    help='执行删除操作（默认为试运行模式）'
)
@click.option(
    '--days', 
    type=int, 
    default=3, 
    help='删除指定天数之前的releases'
)
@click.option(
    '--charts', 
    type=str, 
    default='milvus,etcd,minio,kafka,pulsar', 
    help='要处理的chart类型列表，用逗号分隔'
)
@click.option(
    '--exclude', 
    type=str, 
    default='', 
    help='要排除的release名称列表，用逗号分隔'
)
@click.option(
    '--exclude-prefix', 
    type=str, 
    default='', 
    help='要排除的release名称前缀列表，用逗号分隔，例如：long-run-'
)
def main(execute, days, charts, exclude, exclude_prefix):
    """Main entry point for the script"""
    chart_types = [c.strip().lower() for c in charts.split(',')]
    exclude_releases = [r.strip() for r in exclude.split(',') if r.strip()]
    exclude_prefixes = [p.strip() for p in exclude_prefix.split(',') if p.strip()]

    get_releases_to_delete(
        dry_run=not execute,
        days=days,
        chart_types=chart_types,
        exclude_releases=exclude_releases,
        exclude_prefixes=exclude_prefixes
    )


if __name__ == "__main__":
    main()
