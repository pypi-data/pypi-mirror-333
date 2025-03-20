import os
import webview
import json

default_config = {
    "问小白": "https://www.wenxiaobai.com/chat/200006",
    "百度AI": "https://chat.baidu.com/",
    "纳米AI": "https://bot.n.cn/",
    "豆包": "https://www.doubao.com/chat/",
    "腾讯元宝": "https://yuanbao.tencent.com/chat",
    "KIMI": "https://kimi.moonshot.cn/",
    "知乎直答": "https://zhida.zhihu.com/",
    "DeepSeek": "https://chat.deepseek.com/",
}

webview.settings["OPEN_EXTERNAL_LINKS_IN_BROWSER"] = False
filedir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(filedir, "config.json")
if not os.path.exists(config_path):
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(default_config, f, indent=4, ensure_ascii=False)


def main():
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            if not config:
                raise Exception("config is empty")
    except Exception:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        config = default_config
    window = webview.create_window("AI百宝箱", list(config.values())[0])
    menu_items = [
        webview.menu.MenuAction(name, lambda name=name: window.load_url(config[name]))
        for name in config
    ] + [
        webview.menu.MenuAction(
            "配置",
            lambda: os.system(f"start {config_path}"),
        ),
        webview.menu.MenuAction(
            "关于",
            lambda: window.load_html(
                '<center><h1>AI百宝箱</h1><img src="https://random.imagecdn.app/500/300"></center>'
            ),
        ),
    ]
    webview.start(menu=menu_items)


if __name__ == "__main__":
    main()
