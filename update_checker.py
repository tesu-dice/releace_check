"""
githubのパブリックリポジトリに対して最新バージョンを取得、現在のものと比較する。
リポジトリの設定がプライベートの場合は認証情報が必要になる。
"""

import requests
import sys

"""
現在のリリースバージョンの定義、
githubのリリースを作成するときにおけるtagの部分。
"""
CURRENT_APP_VERSION = "v0.0.0"#現在のバージョンの値、ここが最新と異なるかどうかをチェックする。
def get_latest_github_release_version(owner, repo):
    """
    指定されたGitHubリポジトリの最新リリースバージョンを取得します。
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTPエラーが発生した場合に例外を発生させる

        release_info = response.json()
        latest_version = release_info.get("tag_name")
        return latest_version

    except requests.exceptions.RequestException as e:
        print(f"GitHub APIへのリクエスト中にエラーが発生しました: {e}", file=sys.stderr)
        return None

def check_for_updates(github_owner, github_repo):
    """
    GitHubの最新リリースと現在のアプリケーションバージョンを比較し、更新の有無をチェックします。
    """
    print("更新を確認しています...")
    latest_version = get_latest_github_release_version(github_owner, github_repo)

    if latest_version:
        print(f"現在のバージョン: {CURRENT_APP_VERSION}")
        print(f"GitHub上の最新バージョン: {latest_version}")

        # バージョン比較ロジック（簡易版）
        # より厳密なバージョン比較には、packaging.versionなどのライブラリを使用することを推奨します。
        if latest_version > CURRENT_APP_VERSION:
            print("新しいバージョンが利用可能です！")
            print(f"最新版をダウンロードしてください: https://github.com/{github_owner}/{github_repo}/releases/latest")
            return True
        else:
            print("お使いのバージョンは最新です。")
            return False
    else:
        print("最新のバージョン情報を取得できませんでした。")
        return False

if __name__ == "__main__":
    # このスクリプトを直接実行した場合のテスト用
    # 例: github_owner='your-github-username', github_repo='your-repo-name'
    test_owner = "tesu-dice"  # ここをあなたのGitHubユーザー名に置き換える
    test_repo = "releace_check"      # ここをあなたのリポジトリ名に置き換える

    # requestsライブラリがインストールされているか確認
    try:
        import requests
    except ImportError:
        print("requestsライブラリがインストールされていません。", file=sys.stderr)
        print("pip install requests を実行してインストールしてください。", file=sys.stderr)
        sys.exit(1)

    check_for_updates(test_owner, test_repo)
