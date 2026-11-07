# -*- coding: utf-8 -*-
"""
传奇发布网 · 静态站点生成器
运行：python3 _build.py
输出：当前目录下全部 .html / style.css / app.js / sitemap.xml / robots.txt 等
所有文件平铺在根目录，可直接部署到 cqfbz.github.io
"""

import os
import re
import json

from _content_gonglue import G1
from _content_gonglue2 import G2
from _content_gonglue3 import G3
from _content_zixun import Z1
from _content_xinfu import X1

OUT = os.path.dirname(os.path.abspath(__file__))

SITE = "传奇发布网"
DOMAIN = "https://cqfbz.github.io"
TAGLINE = "每日新开传奇发布站"
TODAY = "2026-11-07"

CATS = {
    "gonglue": {
        "name": "传奇攻略",
        "file": "gonglue",
        "kw": "传奇攻略,传奇玩法,传奇技巧,传奇新手攻略,传奇进阶",
        "seo_title": "传奇攻略_职业选择与升级打宝技巧_传奇发布网",
        "desc": "传奇攻略栏目收录职业选择、升级路线、装备出处、打宝 PK、攻沙组织等实战内容，按版本差异给出可执行的做法，帮助玩家少走弯路。",
        "intro": "这里的内容都来自实际玩法场景：开区第一天该做什么、装备去哪打、PK 怎么站位、攻沙怎么分工。每一篇都尽量给出可执行的步骤，而不是空泛的结论。",
    },
    "zixun": {
        "name": "传奇资讯",
        "file": "zixun",
        "kw": "传奇资讯,传奇行业,传奇版本,传奇市场,传奇动态",
        "seo_title": "传奇资讯_版本演变与市场观察_传奇发布网",
        "desc": "传奇资讯栏目关注版本演变、玩家结构、内容生态与版权环境，用可核查的观察解释这个品类正在发生什么，帮助玩家理解版本设计背后的逻辑。",
        "intro": "资讯栏目不做标题党。我们更关心「为什么」：为什么复古会回潮、为什么开区周期变短、为什么三端互通成了标配。把这些讲清楚，选版本时才有判断依据。",
    },
    "xinfu": {
        "name": "新服动态",
        "file": "xinfu",
        "kw": "新服动态,传奇开区,开服预告,新区汇总,传奇新服",
        "seo_title": "新服动态_每日新开传奇区服_传奇发布网",
        "desc": "新服动态栏目按天汇总新开区信息，包含开区时间、版本类型、节奏特点与适合人群，方便玩家对照自己的在线时段安排进场。",
        "intro": "新区每天都在开，但不是每个都适合你。这里按时间和版本整理开盘节奏，说明每个区的定位和窗口期，帮你在对的时间进对的区。",
    },
}

ICON_PALETTE = [
    ("#7d1f16", "#c0561f"),
    ("#1d3f6b", "#3f7fb5"),
    ("#4a2d6b", "#7b53a8"),
    ("#155b52", "#2c9184"),
    ("#6b4a13", "#b7852a"),
    ("#5c1f33", "#9c3a58"),
]

VER_MAP = {
    "1.76 复古": "banben-176.html",
    "1.80 合击": "banben-180.html",
    "单职业": "banben-danzhiye.html",
    "冰雪": "banben-bingxue.html",
    "微变": "banben-weibian.html",
    "合击打金": "banben-dajin.html",
    "打金": "banben-dajin.html",
}

SERVERS = [
    {"t": "10:00", "d": "11-07", "name": "龙渊一区", "ver": "1.76 复古", "type": "三端互通", "status": "已开", "hot": 1, "icon": "龙渊", "ci": 0},
    {"t": "11:00", "d": "11-07", "name": "烈焰二区", "ver": "1.80 合击", "type": "双端", "status": "火爆", "hot": 1, "icon": "烈焰", "ci": 1},
    {"t": "12:00", "d": "11-07", "name": "苍月三区", "ver": "单职业", "type": "三端互通", "status": "火爆", "hot": 1, "icon": "苍月", "ci": 2},
    {"t": "13:00", "d": "11-07", "name": "冰封四区", "ver": "冰雪", "type": "手游", "status": "已开", "hot": 0, "icon": "冰封", "ci": 3},
    {"t": "14:00", "d": "11-07", "name": "沙城五区", "ver": "1.76 复古", "type": "三端互通", "status": "已开", "hot": 0, "icon": "沙城", "ci": 4},
    {"t": "15:00", "d": "11-07", "name": "龙腾六区", "ver": "微变", "type": "三端互通", "status": "今日", "hot": 0, "icon": "龙腾", "ci": 5},
    {"t": "16:00", "d": "11-07", "name": "战神七区", "ver": "合击打金", "type": "双端", "status": "今日", "hot": 1, "icon": "战神", "ci": 0},
    {"t": "18:00", "d": "11-07", "name": "赤月八区", "ver": "1.80 合击", "type": "三端互通", "status": "预告", "hot": 0, "icon": "赤月", "ci": 1},
    {"t": "19:00", "d": "11-07", "name": "幽兰九区", "ver": "单职业", "type": "手游", "status": "预告", "hot": 0, "icon": "幽兰", "ci": 2},
    {"t": "20:00", "d": "11-07", "name": "星火十区", "ver": "打金", "type": "三端互通", "status": "预告", "hot": 1, "icon": "星火", "ci": 4},
    {"t": "10:00", "d": "11-08", "name": "破晓十一区", "ver": "1.76 复古", "type": "三端互通", "status": "预告", "hot": 0, "icon": "破晓", "ci": 5},
    {"t": "11:00", "d": "11-08", "name": "惊雷十二区", "ver": "1.80 合击", "type": "双端", "status": "预告", "hot": 0, "icon": "惊雷", "ci": 1},
    {"t": "13:00", "d": "11-08", "name": "霜月十三区", "ver": "冰雪", "type": "手游", "status": "预告", "hot": 0, "icon": "霜月", "ci": 3},
    {"t": "15:00", "d": "11-08", "name": "龙吟十四区", "ver": "微变", "type": "三端互通", "status": "预告", "hot": 0, "icon": "龙吟", "ci": 4},
    {"t": "17:00", "d": "11-08", "name": "流火十五区", "ver": "单职业", "type": "三端互通", "status": "预告", "hot": 1, "icon": "流火", "ci": 0},
    {"t": "19:00", "d": "11-08", "name": "沙城十六区", "ver": "合击打金", "type": "双端", "status": "预告", "hot": 0, "icon": "沙城", "ci": 2},
    {"t": "20:00", "d": "11-08", "name": "长夜十七区", "ver": "打金", "type": "三端互通", "status": "预告", "hot": 0, "icon": "长夜", "ci": 5},
    {"t": "21:00", "d": "11-08", "name": "归墟十八区", "ver": "1.76 复古", "type": "三端互通", "status": "预告", "hot": 0, "icon": "归墟", "ci": 3},
]

VERSIONS = [
    {
        "slug": "banben-176.html",
        "name": "1.76 复古传奇",
        "icon": "复古",
        "tag": "经典",
        "ci": 0,
        "kw": "1.76复古,176传奇,复古传奇版本,1.76传奇开服,复古传奇",
        "desc": "1.76 复古传奇版本介绍：保留三职业、原味属性与掉落式装备体系，节奏慢、门槛低、上限高，附该版本今日开区与相关攻略。",
        "sub": "三职业 · 原味属性 · 掉落式装备",
        "intro": [
            "1.76 复古是传奇类版本里最经典的一支。它保留了最初的三职业结构、原始的属性数值和以掉落为主的装备体系，节奏慢、门槛低、上限高。",
            "这个版本的核心体验是「积累」。等级要一级一级升，装备要一件一件打，任何捷径都不存在。也正因为如此，每一件装备都有明确的记忆点，每一次提升都能被感知。",
            "本站收录的 1.76 区以三端互通为主，开区时间集中在上午和下午，适合作息规律、愿意长期经营的玩家。",
        ],
        "points": [("经验倍率", "1—3 倍，升级偏慢"), ("装备来源", "以怪物掉落为主"), ("职业结构", "战士 / 法师 / 道士三职业"), ("合击技能", "无"), ("攻沙节奏", "开区第 3—4 天"), ("单区周期", "约 3—6 周")],
        "articles": ["176-zhuangbei-chuchu", "yuanshi-zhuangbei", "shengji-luxian", "jinni-176-fugu"],
    },
    {
        "slug": "banben-180.html",
        "name": "1.80 合击传奇",
        "icon": "合击",
        "tag": "组合技",
        "ci": 1,
        "kw": "1.80合击,合击传奇,合击版本,1.80传奇,合击技能",
        "desc": "1.80 合击传奇版本介绍：在复古基础上加入双职业合击，说明战战、道道、法法、战道四种组合的伤害结构与适用场景，附今日开区。",
        "sub": "双职业 · 合击技能 · 爆发对抗",
        "intro": [
            "1.80 是在 1.76 基础上加入合击技能的版本。两个职业组合可以释放组合技，改变了单职业的对抗逻辑，也让队伍配置变得更重要。",
            "合击的伤害由双方属性和组合系数共同决定，因此这个版本的核心不是「一个号堆多高」，而是「两个号配得多好」。",
            "本站收录的 1.80 区多开在下午和晚上，人气集中，适合有固定队友、喜欢团战和攻沙的玩家。",
        ],
        "points": [("经验倍率", "3—8 倍，节奏中等"), ("装备来源", "掉落 + 部分兑换"), ("职业结构", "三职业，支持双号合击"), ("核心玩法", "组合技与攻沙团战"), ("攻沙节奏", "开区第 2—3 天"), ("单区周期", "约 2—4 周")],
        "articles": ["heji-jineng-dapei", "pk-zouwei", "shabake-gongcheng", "heji-dajin-anpai"],
    },
    {
        "slug": "banben-danzhiye.html",
        "name": "单职业传奇",
        "icon": "单职",
        "tag": "快节奏",
        "ci": 2,
        "kw": "单职业传奇,单职业版本,单职业打金,单职业流派,传奇单职业",
        "desc": "单职业传奇版本介绍：三职业合并为一个角色，靠装备词条区分攻速流、暴击流、肉盾流，节奏快、成型快、适合打金，附今日开区与流派攻略。",
        "sub": "单角色 · 词条流派 · 快节奏",
        "intro": [
            "单职业版本把战士、法师、道士的能力合并到一个角色身上，既能近战也能远程，还能召唤。看起来更强，实际意味着所有属性都要自己堆。",
            "流派靠装备词条区分：攻速流前期成型快，暴击流后期爆发高，肉盾流单干打宝最稳。选哪个方向，取决于你的在线时长和目标。",
            "这个版本的节奏明显快于复古，前三天是关键的窗口期。本站收录的单职业区多开在晚上，适合时间集中、追求效率的玩家。",
        ],
        "points": [("经验倍率", "10—30 倍，升级极快"), ("装备来源", "掉落 + 升阶"), ("职业结构", "单角色，词条分流派"), ("核心玩法", "流派搭配与打金"), ("攻沙节奏", "开区第 2—3 天"), ("单区周期", "约 1—3 周")],
        "articles": ["danzhiye-wanfa", "dajin-banzhuan", "yuanbao-huafa", "danzhiye-yugao"],
    },
    {
        "slug": "banben-bingxue.html",
        "name": "冰雪传奇",
        "icon": "冰雪",
        "tag": "高爆",
        "ci": 3,
        "kw": "冰雪传奇,冰雪版本,高爆传奇,冰雪打金,冰雪传奇开服",
        "desc": "冰雪传奇版本介绍：高爆率、快节奏、装备升阶，开区前三天是收益窗口，说明装备体系、打金特点与常见节奏误判，附本周新区。",
        "sub": "高爆率 · 装备升阶 · 短周期",
        "intro": [
            "冰雪版本以高爆率和快节奏著称。普通怪也能出不错的装备，开区第一天就能体验到中期的内容。",
            "它的装备体系通常采用升阶模式：同一件装备通过材料升级，而不是不断更换。理解这一点，能避免大量无效的找装备时间。",
            "冰雪区的生命周期较短，前三天的收益占整区的七成。想打金就要抢窗口，想慢慢玩则不太适合这个版本。",
        ],
        "points": [("经验倍率", "20—50 倍，节奏很快"), ("装备来源", "高爆掉落 + 升阶"), ("职业结构", "多为三职业或单职业"), ("核心玩法", "升阶与短周期冲榜"), ("攻沙节奏", "开区第 2—3 天"), ("单区周期", "约 1—2 周")],
        "articles": ["bingxue-wanfa", "bingxue-xinfu", "weibian-qingbian", "dajin-banzhuan"],
    },
    {
        "slug": "banben-weibian.html",
        "name": "微变传奇",
        "icon": "微变",
        "tag": "均衡",
        "ci": 4,
        "kw": "微变传奇,微变版本,轻变传奇,微变开服,传奇微变",
        "desc": "微变传奇版本介绍：经验与爆率居中，装备以升阶为主兼顾掉落，节奏不快不慢，适合上班族与普通玩家，附本周微变新区。",
        "sub": "中等倍率 · 升阶兼顾掉落 · 节奏居中",
        "intro": [
            "微变是介于复古和高爆之间的选择。经验倍率中等、爆率中等，装备体系以升阶为主，同时保留掉落。",
            "这个版本的平衡点在于「既不拖，也不飘」：每天两三个小时能跟上主流进度，又不会三天就毕业。",
            "微变区的竞争相对温和，不必抢开区第一分钟进场，第二天进场也能追上。适合大多数普通玩家。",
        ],
        "points": [("经验倍率", "5—15 倍，节奏适中"), ("装备来源", "升阶为主，兼顾掉落"), ("职业结构", "三职业或单职业"), ("核心玩法", "稳定成长与攻沙"), ("攻沙节奏", "开区第 3 天"), ("单区周期", "约 2—4 周")],
        "articles": ["weibian-qingbian", "weibian-xinqu", "zhuansheng-neigong", "zhuangbei-jianming"],
    },
    {
        "slug": "banben-dajin.html",
        "name": "合击打金服",
        "icon": "打金",
        "tag": "产出",
        "ci": 5,
        "kw": "传奇打金,打金版本,合击打金,传奇搬砖,打金开服",
        "desc": "合击打金服版本介绍：以产出和变现为导向，双角色组合提升刷怪效率，说明物价窗口、成本核算与出货时机，附今日打金区。",
        "sub": "产出导向 · 双角色 · 物价窗口",
        "intro": [
            "打金向的版本设计目标很明确：让产出稳定、让交易活跃。常见做法是高爆率配合双角色组合，提升单位时间的刷怪效率。",
            "这类版本的生命周期短，物价下跌快。开区前 48 小时是最佳窗口，之后收益会明显收窄。",
            "打金不是稳赚。药钱、修理费、时间成本都要算进去，连续两天的净收益为负，就应该换区。",
        ],
        "points": [("经验倍率", "10—40 倍，成型快"), ("装备来源", "高爆掉落为主"), ("职业结构", "双角色合击为主"), ("核心玩法", "刷产出与交易变现"), ("攻沙节奏", "开区第 2 天"), ("单区周期", "约 1—2 周")],
        "articles": ["dajin-banzhuan", "heji-dajin-anpai", "xinqu-wujia", "yuanbao-huafa"],
    },
]

ARTICLES = G1 + G2 + G3 + Z1 + X1
for a in ARTICLES:
    a.setdefault("views", 1000)
ARTICLES.sort(key=lambda x: (x["date"], x["views"]), reverse=True)
BY_SLUG = {a["slug"]: a for a in ARTICLES}

PER_PAGE = 9


# --------------------------------------------------------------------------
# 基础工具
# --------------------------------------------------------------------------

def esc(t):
    return (
        str(t or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def md_html(text):
    out, buf, ul = [], [], []

    def flush_p():
        if buf:
            out.append("<p>%s</p>" % esc("".join(buf)))
            buf.clear()

    def flush_ul():
        if ul:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % esc(x) for x in ul))
            ul.clear()

    for line in text.strip().split("\n"):
        s = line.strip()
        if not s:
            flush_p()
            flush_ul()
            continue
        if s.startswith("## "):
            flush_p()
            flush_ul()
            out.append("<h2>%s</h2>" % esc(s[3:].strip()))
        elif s.startswith("### "):
            flush_p()
            flush_ul()
            out.append("<h3>%s</h3>" % esc(s[4:].strip()))
        elif s.startswith("- "):
            flush_p()
            ul.append(s[2:].strip())
        else:
            flush_ul()
            buf.append(s)
    flush_p()
    flush_ul()
    return "\n".join(out)


def cat_of(a):
    return CATS[a["cat"]]


def icon_html(chars, ci, cls="gicon"):
    c1, c2 = ICON_PALETTE[ci % len(ICON_PALETTE)]
    return '<span class="%s" style="--c1:%s;--c2:%s">%s</span>' % (cls, c1, c2, esc(chars))


def short_date(d):
    return d[5:]


def canon(path):
    return DOMAIN + "/" + ("" if path == "index.html" else path)


# --------------------------------------------------------------------------
# 页面骨架
# --------------------------------------------------------------------------

NAV_ITEMS = [
    ("index.html", "首页", "home"),
    ("kaifu.html", "开服表", "kaifu"),
    ("banben.html", "版本大全", "banben"),
    ("gonglue.html", "传奇攻略", "gonglue"),
    ("zixun.html", "传奇资讯", "zixun"),
    ("xinfu.html", "新服动态", "xinfu"),
]


def head_html(title, desc, kw, path, jsonld=None, noindex=False):
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1"
    parts = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        '<title>%s</title>' % esc(title),
        '<meta name="keywords" content="%s">' % esc(kw),
        '<meta name="description" content="%s">' % esc(desc),
        '<meta name="robots" content="%s">' % robots,
        '<meta name="googlebot" content="%s">' % robots,
        '<meta name="author" content="传奇发布网">',
        '<meta name="applicable-device" content="pc,mobile">',
        '<meta name="format-detection" content="telephone=no">',
        '<link rel="canonical" href="%s">' % canon(path),
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="传奇发布网">',
        '<meta property="og:title" content="%s">' % esc(title),
        '<meta property="og:description" content="%s">' % esc(desc),
        '<meta property="og:url" content="%s">' % canon(path),
        '<link rel="icon" href="favicon.svg" type="image/svg+xml">',
        '<link rel="stylesheet" href="style.css">',
    ]
    if jsonld:
        parts.append('<script type="application/ld+json">%s</script>' % json.dumps(jsonld, ensure_ascii=False))
    return "\n".join(parts)


def header_html(active):
    nav = []
    for url, label, key in NAV_ITEMS:
        cls = " class=\"on\"" if key == active else ""
        nav.append('<a href="%s"%s>%s</a>' % (url, cls, label))
    return """<div class="topbar"><div class="wrap">
  <div class="notice"><b>公告</b> 本站为传奇类游戏资讯与开服信息展示站，不提供游戏下载、充值代付与账号交易服务。</div>
  <div class="tb-links"><a href="kaifu.html">今日开服表</a><a href="banben.html">版本大全</a><a href="about.html">关于本站</a></div>
</div></div>
<header class="header"><div class="wrap">
  <a class="logo" href="index.html" title="传奇发布网首页">
    <span class="logo-mark">传</span>
    <span class="logo-txt"><span class="logo-name">传奇发布网</span><span class="logo-sub">cqfbz.github.io · 每日新开传奇发布站</span></span>
  </a>
  <nav class="nav">%s</nav>
  <button class="nav-toggle" type="button">导航菜单</button>
  <div class="search"><form action="search.html" method="get">
    <input type="search" name="q" placeholder="搜索版本 / 攻略 / 开区" aria-label="站内搜索">
    <button type="submit">搜索</button>
  </form></div>
</div></header>
<div class="chipbar"><div class="wrap">%s</div></div>""" % (
        "".join(nav),
        "".join(
            '<a class="chip" href="%s">%s<span class="chip-txt"><span class="chip-name">%s</span><span class="chip-sub">%s %s</span></span></a>'
            % (
                VER_MAP.get(s["ver"], "kaifu.html"),
                icon_html(s["icon"], s["ci"]),
                s["name"],
                s["d"],
                s["t"],
            )
            for s in SERVERS[:10]
        ),
    )


def footer_html():
    return """<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <h4>传奇发布网 · cqfbz.github.io</h4>
        <p>每日汇总新开传奇发布信息，按版本整理开区节奏，提供职业选择、升级路线、打宝 PK、攻沙组织等实战攻略。内容持续更新，坚持写清楚、写准确。</p>
      </div>
      <div><h4>站点导航</h4><ul class="footer-links">
        <li><a href="index.html">网站首页</a></li>
        <li><a href="kaifu.html">今日开服表</a></li>
        <li><a href="banben.html">版本大全</a></li>
        <li><a href="about.html">关于本站</a></li>
      </ul></div>
      <div><h4>版本入口</h4><ul class="footer-links">
        <li><a href="banben-176.html">1.76 复古传奇</a></li>
        <li><a href="banben-180.html">1.80 合击传奇</a></li>
        <li><a href="banben-danzhiye.html">单职业传奇</a></li>
        <li><a href="banben-bingxue.html">冰雪传奇</a></li>
        <li><a href="banben-weibian.html">微变传奇</a></li>
        <li><a href="banben-dajin.html">合击打金服</a></li>
      </ul></div>
      <div><h4>内容栏目</h4><ul class="footer-links">
        <li><a href="gonglue.html">传奇攻略</a></li>
        <li><a href="zixun.html">传奇资讯</a></li>
        <li><a href="xinfu.html">新服动态</a></li>
        <li><a href="search.html">站内搜索</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <div class="disclaim">免责声明：本站为静态资讯站点，仅展示传奇类游戏的版本信息、开服时间与玩法攻略，不提供任何客户端下载、充值服务或账号交易。站内出现的区服名称、时间为信息整理示例，具体以游戏内公告为准。请理性游戏，注意休息。</div>
      <div style="display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap">
        <span>© 2026 传奇发布网 cqfbz.github.io</span>
        <span>内容仅供交流参考 · 每日更新开服信息</span>
      </div>
    </div>
  </div>
</footer>"""


def page_html(title, desc, kw, path, content, active, jsonld=None, noindex=False, extra_scripts=""):
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
%s
</head>
<body>
%s
<main class="main"><div class="wrap">
%s
</div></main>
%s
%s<script src="app.js" defer></script>
</body>
</html>""" % (head_html(title, desc, kw, path, jsonld, noindex), header_html(active), content, footer_html(), extra_scripts)


def breadcrumb(items):
    parts = []
    for i, (name, url) in enumerate(items):
        if i:
            parts.append('<span class="sep">›</span>')
        if url:
            parts.append('<a href="%s">%s</a>' % (url, name))
        else:
            parts.append("<span>%s</span>" % name)
    return '<nav class="crumb" aria-label="面包屑">%s</nav>' % "".join(parts)


def breadcrumb_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": canon(u) if u else canon("index.html")}
            for i, (n, u) in enumerate(items)
        ],
    }


# --------------------------------------------------------------------------
# 侧栏 / 通用模块
# --------------------------------------------------------------------------

def sidebar(with_tags=True):
    top = sorted(ARTICLES, key=lambda x: -x["views"])[:10]
    rank = "".join(
        '<li><a href="%s.html"><span class="no">%d</span><span class="tt">%s</span><span class="vi">%d</span></a></li>'
        % (a["slug"], i + 1, esc(a["title"]), a["views"])
        for i, a in enumerate(top)
    )
    recent = "".join(
        '<li><span class="cat">%s</span><a href="%s.html">%s</a></li>'
        % (cat_of(a)["name"][:2], a["slug"], esc(a["title"]))
        for a in ARTICLES[:7]
    )
    mini = "".join(
        '<li><span class="tm">%s</span><span class="nm">%s</span><span class="vtag">%s</span></li>'
        % (s["t"], esc(s["name"]), esc(s["ver"]))
        for s in SERVERS[:5]
    )
    tags = [
        "传奇发布网", "新开传奇", "1.76复古", "合击传奇", "单职业", "冰雪版本",
        "微变传奇", "打金搬砖", "开服表", "攻沙", "职业选择", "装备出处",
        "升级路线", "三端互通", "公益服", "复古回潮",
    ]
    tag_html = "".join('<a href="search.html?q=%s" rel="nofollow">%s</a>' % (esc(t), esc(t)) for t in tags)
    return """<aside class="col side">
  <section class="card"><div class="card-hd"><h3>热门排行</h3><a class="more" href="gonglue.html">更多</a></div>
    <div class="card-bd" style="padding-top:4px"><ul class="side-rank">%s</ul></div></section>
  <section class="card"><div class="card-hd"><h3>最近发表</h3></div>
    <div class="card-bd" style="padding-top:6px"><ul class="side-list">%s</ul></div></section>
  <section class="card"><div class="card-hd"><h3>今日开区快讯</h3><a class="more" href="kaifu.html">全部</a></div>
    <div class="card-bd" style="padding-top:4px"><ul class="mini-srv">%s</ul></div></section>
  <section class="card"><div class="card-hd"><h3>站点说明</h3></div>
    <div class="card-bd"><p class="note">本站只做信息整理与玩法科普，<b>不提供下载、不代充、不参与交易</b>。开区时间以游戏内公告为准，进区前建议先试玩半小时。</p></div></section>
  %s
</aside>""" % (rank, recent, mini,
        ('<section class="card"><div class="card-hd"><h3>热门标签</h3></div>'
         '<div class="card-bd"><div class="tags">' + tag_html + '</div></div></section>') if with_tags else "")


def srv_table(rows, show_date=False):
    head = "<th>开区时间</th>" + ("<th>日期</th>" if show_date else "") + "<th>区服名称</th><th>版本</th><th>类型</th><th>状态</th><th>查看</th>"
    body = []
    for s in rows:
        c1, c2 = ICON_PALETTE[s["ci"] % len(ICON_PALETTE)]
        badge = "hot" if s["status"] in ("火爆", "已开") else ("new" if s["status"] == "今日" else "")
        body.append(
            '<tr><td class="c-time">%s</td>%s<td class="c-name"><a href="%s">%s</a></td><td>%s</td><td>%s</td>'
            '<td><span class="badge %s">%s</span></td><td class="c-go"><a href="%s">查看开区 →</a></td></tr>'
            % (
                s["t"],
                ('<td>%s</td>' % s["d"]) if show_date else "",
                VER_MAP.get(s["ver"], "kaifu.html"),
                esc(s["name"]),
                esc(s["ver"]),
                esc(s["type"]),
                badge,
                esc(s["status"]),
                VER_MAP.get(s["ver"], "kaifu.html"),
            )
        )
    return '<div class="table-wrap"><table class="srv-table"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (head, "".join(body))


def link_list(articles, show_date=True):
    items = []
    for a in articles:
        d = '<span class="date">%s</span>' % short_date(a["date"]) if show_date else ""
        items.append('<li><a href="%s.html">%s</a>%s</li>' % (a["slug"], esc(a["title"]), d))
    return '<ul class="linklist">%s</ul>' % "".join(items)


def srv_cards(rows):
    out = []
    for s in rows:
        badge = "hot" if s["status"] in ("火爆", "已开") else ("new" if s["status"] == "今日" else "")
        out.append(
            '<div class="srv">%s<div class="srv-body"><div class="srv-name"><a href="%s">%s</a></div>'
            '<div class="srv-meta"><span class="t">%s %s</span><span>%s</span><span class="badge %s">%s</span></div></div></div>'
            % (
                icon_html(s["icon"], s["ci"]),
                VER_MAP.get(s["ver"], "kaifu.html"),
                esc(s["name"]),
                s["d"],
                s["t"],
                esc(s["ver"]),
                badge,
                esc(s["status"]),
            )
        )
    return '<div class="grid-2">%s</div>' % "".join(out)


# --------------------------------------------------------------------------
# 首页
# --------------------------------------------------------------------------

HOME_TITLE = "传奇发布网_新开传奇发布站_每日传奇开服表_版本大全"
HOME_DESC = (
    "传奇发布网是每日更新的新开传奇发布站，汇总1.76复古、1.80合击、单职业、冰雪、微变、打金等版本的"
    "传奇开服表与开区时间，并提供职业选择、升级路线、打宝PK、攻沙组织等传奇攻略，找传奇版本就上传奇发布网。"
)
HOME_KW = (
    "传奇发布网,新开传奇,传奇发布站,传奇开服表,传奇私服发布网,传奇版本,1.76复古传奇,"
    "合击传奇,单职业传奇,冰雪传奇,传奇攻略"
)


def home_content():
    n_gong = len([a for a in ARTICLES if a["cat"] == "gonglue"])
    feat = BY_SLUG["kaiqu-diyitian"]
    today_rows = [s for s in SERVERS if s["d"] == "11-07"]

    hero = """<section class="hero"><div class="hero-in">
  <span class="hero-kicker">每日更新 · 开服表 / 版本 / 攻略</span>
  <h1>传奇发布网<small>每日新开传奇发布站 · 开服表与版本大全</small></h1>
  <p class="lead-txt">汇总今天与明天的传奇开区信息，按 1.76 复古、1.80 合击、单职业、冰雪、微变、打金六条版本线整理节奏；配套 %d 篇实战攻略，从职业选择到攻沙分工，帮你在对的时间进对的区。</p>
  <div class="hero-stats">
    <span class="stat"><b>%d</b>组今日开区</span>
    <span class="stat"><b>6</b>类主流版本</span>
    <span class="stat"><b>%d</b>篇攻略资讯</span>
    <span class="stat"><b>每日</b>更新</span>
  </div>
  <div class="hero-cta">
    <a class="btn btn-gold" href="kaifu.html">查看今日开服表</a>
    <a class="btn btn-ghost" href="banben.html">按版本选新区</a>
  </div>
</div></section>""" % (len(ARTICLES), len(today_rows), len(ARTICLES))

    left = """<div class="col col-left">
  <section class="card"><div class="card-hd"><h3>每日一荐</h3></div>
    <div class="card-bd">
      <div style="display:flex;gap:12px;align-items:center">
        <span class="gicon lg" style="--c1:#7d1f16;--c2:#c0561f">荐</span>
        <div style="min-width:0">
          <a href="%s.html" style="font-size:15px;font-weight:700;line-height:1.5;display:block">%s</a>
          <span class="note">传奇攻略 · %s</span>
        </div>
      </div>
      <p class="note" style="margin-top:11px">开区第一天做的事，决定了后面一周的节奏。从抢名字、备补给到占刷点，十二件事按时间顺序排好，照着走就行。</p>
      <a class="btn btn-gold" style="width:100%%;justify-content:center;margin-top:12px" href="%s.html">阅读全文</a>
    </div></section>
  <section class="card"><div class="card-hd"><h3>新服动态</h3><a class="more" href="xinfu.html">更多</a></div>
    <div class="card-bd" style="padding-top:6px"><ul class="side-list">%s</ul></div></section>
  <section class="card"><div class="card-hd"><h3>热门标签</h3></div>
    <div class="card-bd"><div class="tags">%s</div></div></section>
</div>""" % (
        feat["slug"], esc(feat["title"]), feat["date"], feat["slug"],
        "".join('<li><span class="cat">新服</span><a href="%s.html">%s</a></li>' % (a["slug"], esc(a["title"])) for a in [x for x in ARTICLES if x["cat"] == "xinfu"][:6]),
        "".join('<a href="search.html?q=%s" rel="nofollow">%s</a>' % (esc(t), esc(t)) for t in ["传奇发布网", "开服表", "1.76复古", "合击", "单职业", "冰雪", "打金", "攻沙", "转生"]),
    )

    center = """<div class="col col-main">
  %s
  <section class="card"><div class="card-hd"><h2>今日新开区</h2><a class="more" href="kaifu.html">完整开服表</a></div>
    <div class="card-bd">%s
      <p class="note" style="margin-top:12px">以上为 11 月 7 日当天开放的部分区服，按开区时间排序。状态「已开」表示已过开区时刻，可正常进入；「预告」表示尚未开区。</p>
    </div></section>
  <section class="card"><div class="card-hd"><h2>今日开服表</h2><a class="more" href="kaifu.html">查看更多</a></div>
    <div class="card-bd" style="padding:0 0 6px">%s</div></section>
  <section class="card"><div class="card-hd"><h2>热门版本</h2><a class="more" href="banben.html">版本大全</a></div>
    <div class="card-bd"><div class="grid-2">%s</div></div></section>
  <section class="card"><div class="card-hd"><h2>传奇攻略</h2><a class="more" href="gonglue.html">全部攻略</a></div>
    <div class="card-bd">%s</div></section>
  <section class="card"><div class="card-hd"><h2>传奇资讯</h2><a class="more" href="zixun.html">更多资讯</a></div>
    <div class="card-bd" style="padding-top:6px"><ul class="side-list">%s</ul></div></section>
  <section class="card"><div class="card-hd"><h2>新服动态</h2><a class="more" href="xinfu.html">全部动态</a></div>
    <div class="card-bd">%s</div></section>
</div>""" % (
        hero,
        srv_cards(today_rows[:8]),
        srv_table(today_rows, show_date=False),
        "".join(
            '<a class="ver" href="%s"><h3>%s<span class="tag">%s</span></h3><p>%s</p></a>'
            % (v["slug"], esc(v["name"]), esc(v["tag"]), esc(v["sub"]))
            for v in VERSIONS
        ),
        link_list([a for a in ARTICLES if a["cat"] == "gonglue"][:12]).replace('class="linklist"', 'class="linklist one"'),
        "".join(
            '<li><span class="cat">资讯</span><a href="%s.html">%s</a></li>' % (a["slug"], esc(a["title"]))
            for a in [x for x in ARTICLES if x["cat"] == "zixun"][:8]
        ),
        link_list([a for a in ARTICLES if a["cat"] == "xinfu"][:6]),
    )

    content = '<div class="layout home">%s%s%s</div>' % (left, center, sidebar(False))
    jsonld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "传奇发布网",
        "alternateName": "cqfbz.github.io 传奇发布站",
        "url": DOMAIN + "/",
        "description": HOME_DESC,
        "inLanguage": "zh-CN",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {"@type": "EntryPoint", "urlTemplate": DOMAIN + "/search.html?q={search_term_string}"},
            "query-input": "required name=search_term_string",
        },
    }
    return content, jsonld


def build_home():
    content, jsonld = home_content()
    write("index.html", page_html(HOME_TITLE, HOME_DESC, HOME_KW, "index.html", content, "home", jsonld))


# --------------------------------------------------------------------------
# 文章页
# --------------------------------------------------------------------------

def related_for(a, n=4):
    pool = [x for x in ARTICLES if x["cat"] == a["cat"] and x["slug"] != a["slug"]]
    tags = set(a.get("tags", []))
    scored = sorted(
        pool,
        key=lambda x: (-len(tags & set(x.get("tags", []))), x["date"]),
    )
    picked = scored[:n]
    if len(picked) < n:
        others = [x for x in ARTICLES if x["cat"] != a["cat"] and x["slug"] != a["slug"]]
        picked += others[: n - len(picked)]
    return picked[:n]


def article_content(a):
    cat = cat_of(a)
    idx = [x for x in ARTICLES if x["cat"] == a["cat"]]
    pos = idx.index(a)
    prev_a = idx[pos - 1] if pos > 0 else None
    next_a = idx[pos + 1] if pos + 1 < len(idx) else None

    words = len(re.sub(r"\s", "", a["body"]))
    mins = max(2, words // 380)

    tags = "".join('<a href="search.html?q=%s" rel="nofollow">%s</a>' % (esc(t), esc(t)) for t in a.get("tags", []))

    pager = '<div class="pager">'
    if prev_a:
        pager += '<a href="%s.html"><span class="lb">上一篇</span>%s</a>' % (prev_a["slug"], esc(prev_a["title"]))
    else:
        pager += '<span></span>'
    if next_a:
        pager += '<a class="next" href="%s.html"><span class="lb">下一篇</span>%s</a>' % (next_a["slug"], esc(next_a["title"]))
    pager += "</div>"

    rel = related_for(a)
    rel_html = '<div class="rel"><h3>相关阅读</h3>%s</div>' % link_list(rel)

    article = """<article class="card">
  <header class="post-head">
    <h1>%s</h1>
    <div class="post-meta"><span class="c">%s</span><span>%s</span><span>约 %d 分钟读完</span><span>%d 次阅读</span><span>来源：传奇发布网</span></div>
  </header>
  <div class="post-body">%s</div>
  <div class="post-tags"><span>标签：</span>%s</div>
  <div class="cta"><p>今日开区已更新，<b>共 %d 组</b>。想按版本挑区，可以看完整开服表。</p><a class="btn btn-gold" href="kaifu.html">查看开服表</a></div>
  %s
  %s
</article>""" % (
        esc(a["title"]),
        cat["name"],
        a["date"],
        mins,
        a["views"],
        md_html(a["body"]),
        tags,
        len([s for s in SERVERS if s["d"] == "11-07"]),
        pager,
        rel_html,
    )

    crumb_items = [("首页", "index.html"), (cat["name"], cat["file"] + ".html"), (a["title"], None)]
    content = breadcrumb(crumb_items) + '<div class="layout">%s%s</div>' % (article, sidebar())

    title = "%s_%s_传奇发布网" % (a["title"], cat["name"])
    if len(title) > 40:
        title = "%s_传奇发布网" % a["title"]
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": a["title"],
                "description": a["desc"],
                "datePublished": a["date"] + "T08:00:00+08:00",
                "dateModified": a["date"] + "T08:00:00+08:00",
                "author": {"@type": "Organization", "name": "传奇发布网"},
                "publisher": {"@type": "Organization", "name": "传奇发布网", "url": DOMAIN + "/"},
                "mainEntityOfPage": {"@type": "WebPage", "@id": canon(a["slug"] + ".html")},
                "articleSection": cat["name"],
                "keywords": a["kw"],
                "inLanguage": "zh-CN",
                "url": canon(a["slug"] + ".html"),
            },
            breadcrumb_ld(crumb_items),
        ],
    }
    return content, title, jsonld


def build_articles():
    for a in ARTICLES:
        content, title, jsonld = article_content(a)
        write(a["slug"] + ".html", page_html(title, a["desc"], a["kw"], a["slug"] + ".html", content, a["cat"], jsonld))


# --------------------------------------------------------------------------
# 栏目列表页
# --------------------------------------------------------------------------

def build_lists():
    for key, cat in CATS.items():
        items = [a for a in ARTICLES if a["cat"] == key]
        pages = (len(items) + PER_PAGE - 1) // PER_PAGE
        for p in range(1, pages + 1):
            chunk = items[(p - 1) * PER_PAGE: p * PER_PAGE]
            path = cat["file"] + ".html" if p == 1 else "%s-%d.html" % (cat["file"], p)
            h1 = cat["name"] if p == 1 else "%s（第 %d 页）" % (cat["name"], p)
            page_title = (cat["seo_title"] if p == 1 else "%s_第%d页_传奇发布网" % (cat["name"], p))

            posts = []
            for a in chunk:
                c1, c2 = ICON_PALETTE[(len(a["slug"]) + a["views"]) % len(ICON_PALETTE)]
                posts.append(
                    """<article class="post-item">
  <a class="thumb" href="%s.html" style="--c1:%s;--c2:%s" aria-hidden="true">%s</a>
  <div class="pi-body">
    <h2><a href="%s.html">%s</a></h2>
    <div class="pi-meta"><span class="c">%s</span><span>%s</span><span>%d 次阅读</span></div>
    <p class="pi-desc">%s</p>
    <a class="rm" href="%s.html">阅读全文 →</a>
  </div>
</article>""" % (
                        a["slug"], c1, c2, "攻略" if a["cat"] == "gonglue" else ("资讯" if a["cat"] == "zixun" else "新服"),
                        a["slug"], esc(a["title"]), cat["name"], a["date"], a["views"], esc(a["desc"]), a["slug"],
                    )
                )

            pag = ['<div class="pagination">']
            if p > 1:
                prev_url = cat["file"] + ".html" if p == 2 else "%s-%d.html" % (cat["file"], p - 1)
                pag.append('<a href="%s">上一页</a>' % prev_url)
            else:
                pag.append('<span class="dis">上一页</span>')
            for i in range(1, pages + 1):
                u = cat["file"] + ".html" if i == 1 else "%s-%d.html" % (cat["file"], i)
                if i == p:
                    pag.append('<span class="cur">%d</span>' % i)
                else:
                    pag.append('<a href="%s">%d</a>' % (u, i))
            if p < pages:
                pag.append('<a href="%s-%d.html">下一页</a>' % (cat["file"], p + 1))
            else:
                pag.append('<span class="dis">下一页</span>')
            pag.append("</div>")

            card = """<section class="card">
  <div class="list-head">
    <h1>%s</h1>
    <p class="desc">%s</p>
    <p class="desc" style="margin-top:8px;color:#8a7455">%s</p>
    <div class="list-count">共 %d 篇 · 第 %d / %d 页 · 按发布时间排序</div>
  </div>
  %s
  %s
</section>""" % (
                h1, cat["desc"], cat["intro"], len(items), p, pages, "".join(posts), "".join(pag),
            )

            content = breadcrumb([("首页", "index.html"), (cat["name"], cat["file"] + ".html")]) + \
                '<div class="layout">%s%s</div>' % (card, sidebar())
            jsonld = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "CollectionPage",
                        "name": h1,
                        "description": cat["desc"],
                        "url": canon(path),
                        "inLanguage": "zh-CN",
                        "isPartOf": {"@type": "WebSite", "name": "传奇发布网", "url": DOMAIN + "/"},
                    },
                    breadcrumb_ld([("首页", "index.html"), (cat["name"], cat["file"] + ".html")]),
                ],
            }
            desc_p = cat["desc"] if p == 1 else "%s第 %d 页：继续列出更早发布的文章，按发布时间倒序排列，便于逐页查阅。" % (cat["name"], p)
            kw_p = cat["kw"] if p == 1 else cat["kw"] + ",第%d页" % p
            write(path, page_html(page_title, desc_p, kw_p, path, content, key, jsonld))


# --------------------------------------------------------------------------
# 版本页
# --------------------------------------------------------------------------

def ver_rows2(v):
    key = v["name"].replace("传奇", "").strip()
    rows = []
    for s in SERVERS:
        sv = s["ver"]
        if key.startswith("1.76") and sv.startswith("1.76"):
            rows.append(s)
        elif key.startswith("1.80") and sv.startswith("1.80"):
            rows.append(s)
        elif key == "单职业" and sv == "单职业":
            rows.append(s)
        elif key == "冰雪" and sv == "冰雪":
            rows.append(s)
        elif key == "微变" and sv == "微变":
            rows.append(s)
        elif key.startswith("合击打金") and sv in ("合击打金", "打金"):
            rows.append(s)
    return rows


def build_versions():
    # 版本大全
    hub_cards = "".join(
        '<a class="ver" href="%s"><h3>%s<span class="tag">%s</span></h3><p>%s</p></a>'
        % (v["slug"], esc(v["name"]), esc(v["tag"]), esc(v["sub"]))
        for v in VERSIONS
    )
    hub = """<section class="card">
  <div class="list-head">
    <h1>传奇版本大全：六类主流版本的节奏与选择</h1>
    <p class="desc">同一个「传奇」，不同版本的玩法能差出十万八千里。这里按六条主线拆开讲：复古、合击、单职业、冰雪、微变、打金，各自的倍率、装备体系、开区节奏和适合人群，看完再选，少走弯路。</p>
  </div>
  <div class="card-bd"><div class="grid-3">%s</div>
    <p class="note" style="margin-top:16px">版本名称没有统一标准，同样的「微变」在不同区可能差很多。判断一个区适不适合自己，最直接的办法是看倍率、装备体系和开区时间这三项，而不是只看宣传词。</p>
  </div>
</section>
<section class="card"><div class="card-hd"><h2>今日各版本开区分布</h2><a class="more" href="kaifu.html">开服表</a></div>
  <div class="card-bd" style="padding:0 0 6px">%s</div></section>""" % (hub_cards, srv_table([s for s in SERVERS if s["d"] == "11-07"], show_date=False))

    content = breadcrumb([("首页", "index.html"), ("版本大全", None)]) + '<div class="layout"><div class="col">%s</div>%s</div>' % (hub, sidebar())
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "name": "传奇版本大全", "url": canon("banben.html"),
             "description": "六类主流传奇版本介绍与选择指南", "inLanguage": "zh-CN"},
            breadcrumb_ld([("首页", "index.html"), ("版本大全", "banben.html")]),
        ],
    }
    write("banben.html", page_html(
        "传奇版本大全_1.76复古_合击_单职业_冰雪_微变_打金_传奇发布网",
        "传奇版本大全：介绍1.76复古、1.80合击、单职业、冰雪、微变、合击打金六类主流版本的倍率、装备体系与开区节奏，帮助玩家按时间投入选版本。",
        "传奇版本,版本大全,1.76复古,1.80合击,单职业,冰雪版本,微变版本,打金版本",
        "banben.html", content, "banben", jsonld))

    for v in VERSIONS:
        rows = ver_rows2(v)
        points = "".join("<li><b>%s</b>：%s</li>" % (esc(k), esc(val)) for k, val in v["points"])
        arts = [BY_SLUG[x] for x in v["articles"] if x in BY_SLUG]
        table = srv_table(rows, show_date=True) if rows else '<p class="note">该版本今日暂无收录开区，可查看完整开服表或明日预告。</p>'
        body = """<section class="card">
  <div class="ver-hero">
    %s
    <div><h1>%s</h1><div class="sub">%s</div></div>
  </div>
  <div class="ver-body post-body">
    %s
    <h2>版本要点</h2>
    <ul class="ver-points">%s</ul>
    <h2>今日与明日开区</h2>
    %s
    <h2>相关攻略与动态</h2>
    %s
    <p class="note">版本信息会随开区调整变化，具体设定以区内公告为准。选版本之前，建议先进区试玩半小时，确认节奏是否能接受。</p>
  </div>
</section>""" % (
            icon_html(v["icon"], v["ci"], "gicon"),
            esc(v["name"]),
            esc(v["sub"]),
            "".join("<p>%s</p>" % esc(p) for p in v["intro"]),
            points,
            table,
            link_list(arts),
        )
        content = breadcrumb([("首页", "index.html"), ("版本大全", "banben.html"), (v["name"], None)]) + \
            '<div class="layout">%s%s</div>' % (body, sidebar())
        jsonld = {
            "@context": "https://schema.org",
            "@graph": [
                {"@type": "WebPage", "name": v["name"], "description": v["desc"],
                 "url": canon(v["slug"]), "inLanguage": "zh-CN"},
                breadcrumb_ld([("首页", "index.html"), ("版本大全", "banben.html"), (v["name"], v["slug"])]),
            ],
        }
        write(v["slug"], page_html("%s_版本介绍与开服表_传奇发布网" % v["name"], v["desc"], v["kw"], v["slug"], content, "banben", jsonld))


# --------------------------------------------------------------------------
# 开服表
# --------------------------------------------------------------------------

def build_kaifu():
    today = [s for s in SERVERS if s["d"] == "11-07"]
    tomorrow = [s for s in SERVERS if s["d"] == "11-08"]
    body = """<section class="card">
  <div class="list-head">
    <h1>传奇开服表：今日与明日新开区一览</h1>
    <p class="desc">下面这张表按开区时间列出今天（11 月 7 日）和明天（11 月 8 日）的全部收录区服，包含版本、端类型与当前状态。开区时刻以区内公告为准，本站只做信息整理。</p>
    <div class="list-count">更新时间：2026-11-07 08:00 · 今日 %d 组 / 明日 %d 组</div>
  </div>
  <div class="card-bd" style="padding:0 0 4px">%s</div>
  <div class="card-bd" style="padding-top:0">
    <p class="note"><b>状态说明：</b>「已开」表示已过开区时刻，可正常进入；「火爆」表示当前在线人数较多，好点较难抢；「今日」表示今日内开放；「预告」表示尚未到开区时间。</p>
  </div>
</section>
<section class="card"><div class="card-hd"><h2>明日开区预告</h2></div>
  <div class="card-bd" style="padding:0 0 6px">%s</div></section>
<section class="card"><div class="card-hd"><h2>怎么用这张表</h2></div>
  <div class="card-bd post-body" style="padding-top:14px">
    <p>先按版本筛一遍。只看自己熟悉的版本，能过滤掉大部分不合适的区。</p>
    <p>再按时间筛。你几点能上线，就选那个时段前后开的区。开区后两小时内进场最划算，晚了进度会落后一截。</p>
    <p>最后看状态。「火爆」的区人多、组队容易，但抢点难；「预告」的区适合提前做计划，占点压力小。</p>
    <p>如果你还没想好进哪个版本，可以先看 <a href="banben.html" style="color:#a2261c">版本大全</a>，了解六类版本的节奏差异，再回来挑区。</p>
  </div></section>""" % (len(today), len(tomorrow), srv_table(today, show_date=True), srv_table(tomorrow, show_date=True))

    content = breadcrumb([("首页", "index.html"), ("开服表", None)]) + '<div class="layout"><div class="col">%s</div>%s</div>' % (body, sidebar())
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "name": "传奇开服表", "url": canon("kaifu.html"),
             "description": "今日与明日新开传奇区服一览，含版本、端类型与状态", "inLanguage": "zh-CN"},
            breadcrumb_ld([("首页", "index.html"), ("开服表", "kaifu.html")]),
        ],
    }
    write("kaifu.html", page_html(
        "传奇开服表_今日新开传奇区服_明日开区预告_传奇发布网",
        "传奇开服表：按开区时间列出今日与明日的新开传奇区服，标注版本、端类型与状态，附状态说明与选服方法，帮助玩家安排进场时间。",
        "传奇开服表,今日开服,新开传奇,开区时间,明日开区,传奇发布网",
        "kaifu.html", content, "kaifu", jsonld))


# --------------------------------------------------------------------------
# 关于 / 搜索 / 404
# --------------------------------------------------------------------------

def build_about():
    body = """<section class="card"><div class="list-head"><h1>关于本站：传奇发布网在做什么</h1>
  <p class="desc">一个把开服信息、版本说明和实战攻略放在一起的静态站点。</p></div>
  <div class="about-body">
    <h2>站点定位</h2>
    <p>传奇发布网（cqfbz.github.io）是一个纯静态的传奇类游戏资讯站。核心工作只有三件：整理开区信息、说明版本差异、写清玩法细节。不做下载、不做充值、不做账号交易，也不替任何区服做质量担保。</p>
    <h2>内容范围</h2>
    <ul>
      <li>开服表：按天整理今日与明日的新开区，标注版本、端类型与状态。</li>
      <li>版本大全：1.76 复古、1.80 合击、单职业、冰雪、微变、合击打金六条主线。</li>
      <li>传奇攻略：职业选择、升级路线、装备出处、打宝 PK、攻沙组织。</li>
      <li>传奇资讯：版本演变、玩家结构、内容生态与版权环境。</li>
      <li>新服动态：按周汇总开区节奏、物价窗口与备战要点。</li>
    </ul>
    <h2>更新方式</h2>
    <p>站点为静态页面，开服表与文章按天/按周更新。所有页面都由统一的内容源生成，标题、关键词、描述与内链保持一致，方便搜索引擎抓取与收录。</p>
    <h2>写内容的原则</h2>
    <ul>
      <li>结论先行：先说怎么做，再说为什么。</li>
      <li>给数字：倍率、时间、成本，能写具体就不写「适当」。</li>
      <li>讲差异：不同版本的做法不一样，不混着讲。</li>
      <li>不夸大：不写「一刀999」「上线送神装」这类话术。</li>
    </ul>
    <h2>免责声明</h2>
    <p>本站为信息展示与玩法科普站点，不提供任何游戏客户端、下载链接、充值入口或账号交易服务。站内出现的区服名称、开区时间为信息整理示例，具体以游戏内公告为准。游戏内容版权归相应权利人所有。请理性游戏，注意休息，未成年人请在监护人陪同下了解相关内容。</p>
    <h2>反馈与建议</h2>
    <p>如果发现信息错误、链接失效，或希望补充某个版本的说明，可以在站点仓库提交 issue，或通过站内搜索找到对应栏目后留言反馈。我们会按优先级处理，开服表的信息纠错优先。</p>
  </div>
</section>"""
    content = breadcrumb([("首页", "index.html"), ("关于本站", None)]) + '<div class="layout">%s%s</div>' % (body, sidebar())
    jsonld = {
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": "关于传奇发布网",
        "url": canon("about.html"),
        "inLanguage": "zh-CN",
    }
    write("about.html", page_html(
        "关于本站_传奇发布网_新开传奇发布站",
        "传奇发布网是纯静态的传奇类游戏资讯站，整理开服信息、说明版本差异、提供实战攻略，不提供下载与充值服务。",
        "关于传奇发布网,传奇发布站介绍,传奇资讯站",
        "about.html", content, "about", jsonld))


def build_search():
    hot = ["开服表", "1.76复古", "合击", "单职业", "冰雪", "微变", "打金", "攻沙", "转生", "装备"]
    body = """<section class="card">
  <div class="list-head" style="padding-bottom:18px"><h1>站内搜索</h1>
    <p class="desc">输入版本名、玩法关键词或区服名，检索全站攻略、资讯与开服信息。</p></div>
  <div class="searchbox">
    <form action="search.html" method="get">
      <input id="kw" type="search" name="q" placeholder="例如：合击、打金、冰雪、攻沙、装备出处" aria-label="搜索关键词">
      <button type="submit">搜索</button>
    </form>
    <div class="hotkw"><span>热门：</span>%s</div>
  </div>
  <div class="search-res" id="search-res"><p class="empty">输入关键词开始检索。</p></div>
</section>""" % "".join('<a href="search.html?q=%s">%s</a>' % (esc(t), esc(t)) for t in hot)
    content = breadcrumb([("首页", "index.html"), ("站内搜索", None)]) + '<div class="layout">%s%s</div>' % (body, sidebar())
    write("search.html", page_html(
        "站内搜索_传奇发布网",
        "传奇发布网站内搜索：按版本名、玩法关键词或区服名检索攻略、资讯与开服信息。",
        "站内搜索,传奇搜索,传奇攻略搜索",
        "search.html", content, "search", None, noindex=True,
        extra_scripts='<script src="search-data.js"></script>\n'))


def build_404():
    body = """<section class="card"><div class="list-head"><h1>页面走丢了</h1>
  <p class="desc">这个地址没有对应的内容，可能是链接写错了，也可能是页面已经调整。可以试试下面几个入口。</p></div>
  <div class="about-body">
    <p><a class="btn btn-gold" href="index.html">返回首页</a> <a class="btn btn-ghost" href="kaifu.html" style="color:#7a6132;border-color:#d9c08a">查看今日开服表</a></p>
    <h2>常用入口</h2>
    <ul>
      <li><a href="kaifu.html">今日开服表</a>：今天与明天的新开区一览。</li>
      <li><a href="banben.html">版本大全</a>：六类主流版本的节奏与选择。</li>
      <li><a href="gonglue.html">传奇攻略</a>：职业、升级、装备、PK、攻沙。</li>
      <li><a href="search.html">站内搜索</a>：用关键词找具体内容。</li>
    </ul>
  </div></section>"""
    content = breadcrumb([("首页", "index.html"), ("页面未找到", None)]) + '<div class="layout">%s%s</div>' % (body, sidebar())
    write("404.html", page_html("页面未找到_传奇发布网", "页面未找到，可通过首页、开服表或站内搜索继续浏览。",
                                "传奇发布网", "404.html", content, "404", None, noindex=True))


# --------------------------------------------------------------------------
# 静态资源与 SEO 辅助文件
# --------------------------------------------------------------------------

def build_search_data():
    rows = []
    for a in ARTICLES:
        rows.append({"t": a["title"], "u": a["slug"] + ".html", "c": cat_of(a)["name"],
                     "d": a["date"], "desc": a["desc"], "k": a["kw"]})
    for v in VERSIONS:
        rows.append({"t": v["name"], "u": v["slug"], "c": "版本大全", "d": TODAY,
                     "desc": v["desc"], "k": v["kw"]})
    rows.append({"t": "今日开服表", "u": "kaifu.html", "c": "开服表", "d": TODAY,
                 "desc": "今日与明日新开传奇区服一览，含版本、端类型与状态。", "k": "开服表,开区时间,新开传奇"})
    rows.append({"t": "传奇版本大全", "u": "banben.html", "c": "版本大全", "d": TODAY,
                 "desc": "六类主流传奇版本的介绍与选择指南。", "k": "传奇版本,版本大全"})
    rows.append({"t": "关于本站", "u": "about.html", "c": "关于", "d": TODAY,
                 "desc": "传奇发布网的定位、内容范围与免责声明。", "k": "关于本站"})
    js = "window.SEARCH_DATA = " + json.dumps(rows, ensure_ascii=False, indent=0) + ";\n"
    write("search-data.js", js)


def build_seo_files():
    urls = []

    def add(path, lastmod, pri, freq="weekly"):
        urls.append((path, lastmod, pri, freq))

    add("index.html", TODAY, "1.0", "daily")
    add("kaifu.html", TODAY, "0.9", "daily")
    add("banben.html", TODAY, "0.8")
    for v in VERSIONS:
        add(v["slug"], TODAY, "0.8")
    for key, cat in CATS.items():
        items = [a for a in ARTICLES if a["cat"] == key]
        pages = (len(items) + PER_PAGE - 1) // PER_PAGE
        add(cat["file"] + ".html", TODAY, "0.8")
        for p in range(2, pages + 1):
            add("%s-%d.html" % (cat["file"], p), TODAY, "0.6")
    for a in ARTICLES:
        add(a["slug"] + ".html", a["date"], "0.7")
    add("about.html", TODAY, "0.3", "monthly")

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, lastmod, pri, freq in urls:
        xml.append("  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>"
                   % (canon(path), lastmod, freq, pri))
    xml.append("</urlset>")
    write("sitemap.xml", "\n".join(xml))

    write("robots.txt", """User-agent: *
Allow: /
Disallow: /search.html
Disallow: /404.html

User-agent: Baiduspider
Allow: /
Disallow: /search.html

User-agent: Googlebot
Allow: /

Sitemap: https://cqfbz.github.io/sitemap.xml
""")

    write("favicon.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#7d1f16"/><stop offset="100%" stop-color="#2a0f0a"/>
  </linearGradient></defs>
  <rect x="2" y="2" width="60" height="60" rx="12" fill="url(#g)" stroke="#c8a02b" stroke-width="2"/>
  <text x="32" y="45" font-size="34" font-family="KaiTi,STKaiti,serif" font-weight="bold" fill="#e9c65f" text-anchor="middle">传</text>
</svg>
""")

    write(".nojekyll", "")


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# --------------------------------------------------------------------------

def main():
    build_home()
    build_lists()
    build_versions()
    build_articles()
    build_kaifu()
    build_about()
    build_search()
    build_404()
    build_search_data()
    build_seo_files()
    files = sorted(x for x in os.listdir(OUT) if x.endswith((".html", ".xml", ".txt", ".svg", ".js", ".css")))
    print("已生成页面 %d 个" % len([x for x in files if x.endswith(".html")]))
    print("文章 %d 篇（攻略 %d / 资讯 %d / 新服 %d）" % (
        len(ARTICLES),
        len([a for a in ARTICLES if a["cat"] == "gonglue"]),
        len([a for a in ARTICLES if a["cat"] == "zixun"]),
        len([a for a in ARTICLES if a["cat"] == "xinfu"]),
    ))


if __name__ == "__main__":
    main()
