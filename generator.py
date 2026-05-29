import os
import random
from datetime import datetime
from openai import OpenAI
import db

WEEKDAYS_CN = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

DEFAULT_TAGS = [
    "#早安", "#晚安", "#治愈", "#总有一句话戳心", "#生活感悟",
    "#把生活拍出电影感", "#街头随拍", "#人生感悟", "#温暖", "#正能量",
    "#每日一句", "#心灵鸡汤", "#情感", "#文案", "#短视频文案",
]

_client_cache = {}


def _get_client(api_key, api_base):
    cache_key = f"{api_key}:{api_base}"
    if cache_key not in _client_cache:
        _client_cache.clear()
        _client_cache[cache_key] = OpenAI(api_key=api_key, base_url=api_base, timeout=30.0)
    return _client_cache[cache_key]


def get_date_greeting(mode="morning"):
    now = datetime.now()
    date_str = f"{now.month}月{now.day}日"
    weekday = WEEKDAYS_CN[now.weekday()]
    greeting = "早安" if mode == "morning" else "晚安"
    return f"{greeting}，今天是{date_str}，{weekday}"


def get_date_key():
    return datetime.now().strftime("%Y-%m-%d")


STYLE_EXAMPLES_MORNING = [
    "早安，今天是5月28日，星期四\n山高一程，水远一程，风雨一程，晴暖一程\n所有低谷皆是铺垫，所有失去皆是馈赠\n来时全心奔赴，走时淡然回首\n煮雪烹茶，听雨眠云，不问归期，只问本心",
    "早安，今天是5月27日，星期三\n你走过的每一条弯路，都是必经之路\n不必追赶，不必慌张\n花开有期，你也有期\n心若不动，风又奈何",
    "早安，今天是5月26日，星期二\n有些路，走着走着就亮了\n有些人，遇着遇着就暖了\n别急，好戏还在后头\n愿你眼里有光，心中有海，脚下有路",
    "早安，今天是5月25日，星期一\n生活不会一直温柔，但你可以\n世界不会一直晴朗，但你可以\n做自己该做的事，走自己该走的路\n温柔且坚定，从容且清醒",
    "早安，今天是5月24日，星期日\n风会记得一朵花的香，时光会记得你努力的样子\n不必事事圆满，但求事事甘心\n慢慢来，比较快\n静水深流，厚积薄发",
]

STYLE_EXAMPLES_EVENING = [
    "晚安，今天是5月28日，星期四\n把白天的疲惫交给夜色\n把未完成的事交给明天\n你已经很努力了\n今夜，只管安心入眠",
    "晚安，今天是5月27日，星期三\n夜深了，世界安静了\n你的心事也该放下了\n明天又是新的一天\n愿你梦里有星辰，醒来有阳光",
    "晚安，今天是5月26日，星期二\n不是所有日子都闪闪发光\n但每个平凡的日子都值得温柔以待\n今天辛苦了\n好好休息，明天继续发光",
]


def build_prompt(mode="morning"):
    greeting = "早安" if mode == "morning" else "晚安"
    theme = "人生、遇见、成长、得失、释怀、活在当下" if mode == "morning" else "夜晚、宁静、放下、感恩、释怀、安眠"

    examples = STYLE_EXAMPLES_MORNING if mode == "morning" else STYLE_EXAMPLES_EVENING
    example_text = "\n\n---\n".join(examples)

    knowledge = db.get_knowledge_combined()
    knowledge_section = ""
    if knowledge.strip():
        knowledge_section = f"\n\n参考以下知识库的风格和意境：\n{knowledge}\n"

    existing = db.get_all_generated_texts()
    dedup_section = ""
    if existing:
        recent = existing[-20:]
        dedup_section = f"\n\n以下是最近生成过的文案，请不要重复或高度相似：\n" + "\n".join(
            f"- {t}" for t in recent
        )

    prompt = f"""生成一条抖音{greeting}治愈文案，今天是{{date}}，{{week}}。

要求：
- 文字温柔治愈，有画面感，有温度
- 主题围绕{theme}
- 30-60字，短句为主，适合短视频配音
- 风格自由发挥，可以排比、对仗、也可以散文诗、也可以一句话直击人心
- 格式不限，不要每次都用同样的结构
- 第一行写问候语（{greeting}，今天是X月X日，星期X），后面自由发挥

以下是几种不同风格的示例，仅供参考，请创造新的风格和表达：

{example_text}
{knowledge_section}{dedup_section}

请直接输出文案内容，不要任何解释。"""

    return prompt


def generate_copywriting(mode="morning"):
    api_key = db.get_config("api_key", "")
    api_base = db.get_config("api_base", "https://api.openai.com/v1")
    model = db.get_config("model", "gpt-4o-mini")

    if not api_key:
        return local_generate(mode), None

    try:
        client = _get_client(api_key, api_base)
        prompt = build_prompt(mode)

        now = datetime.now()
        date_info = f"{now.month}月{now.day}日"
        week_info = WEEKDAYS_CN[now.weekday()]
        prompt = prompt.replace("{date}", date_info).replace("{week}", week_info)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一位风格多变的抖音治愈文案创作者。你的文字时而温柔如水，时而锋利如刀，时而诗意盎然，时而朴实真挚。每次创作都追求不同的表达方式和结构，绝不重复自己。"},
                {"role": "user", "content": prompt},
            ],
            temperature=1.0,
            max_tokens=300,
            extra_body={"enable_thinking": False},
        )

        result = response.choices[0].message.content.strip()
        return result, None

    except Exception as e:
        _client_cache.clear()
        return None, str(e)


def parse_and_build(result_text, mode="morning"):
    lines = [l.strip() for l in result_text.strip().split("\n") if l.strip()]

    greeting_line = get_date_greeting(mode)

    body_lines = []
    for line in lines:
        if line.startswith("早安") or line.startswith("晚安"):
            continue
        body_lines.append(line)

    body = "\n".join(body_lines)

    import random
    tags_config = db.get_config("tags", "")
    if tags_config:
        tag_list = [t.strip() for t in tags_config.split(",") if t.strip()]
    else:
        tag_list = DEFAULT_TAGS

    mode_tag = "#早安" if mode == "morning" else "#晚安"
    other_tags = [t for t in tag_list if t != mode_tag]
    selected = random.sample(other_tags, min(4, len(other_tags)))
    tags_str = mode_tag + " " + " ".join(selected)

    full_text = f"{greeting_line}\n{body}\n{tags_str}"

    return {
        "greeting": greeting_line,
        "body": body,
        "tags": tags_str,
        "full_text": full_text,
    }


PARALLEL_A = [
    "人生", "岁月", "风雨", "山水", "时光", "悲欢", "春秋", "聚散",
    "行走", "跋涉", "寻觅", "等待", "相遇", "告别", "成长", "沉淀",
]
PARALLEL_B = [
    "得失", "起落", "冷暖", "悲喜", "阴晴", "进退", "取舍", "沉浮",
    "花开", "叶落", "潮起", "潮落", "云聚", "云散", "梦醒", "梦回",
]
INSIGHT_A = [
    "遇见", "陪伴", "经历", "付出", "等待", "坚持", "相遇", "选择",
    "失去", "遗憾", "错过", "离别", "伤痛", "挫折", "迷茫", "等待",
]
INSIGHT_B = [
    "缘分", "温暖", "馈赠", "勇气", "希望", "力量", "礼物", "成长",
    "释怀", "成长", "成全", "自由", "坚强", "智慧", "清醒", "答案",
]
ACTION_COME = [
    "满心欢喜", "好好珍惜", "心存感恩", "温柔以待", "坦然接受", "微笑面对",
    "张开双臂", "静静守候", "满怀期待", "用心感受",
]
ACTION_GO = [
    "从容挥手", "坦然相送", "不留遗憾", "微笑告别", "释然放手", "心怀感激",
    "优雅转身", "平静目送", "轻轻放下", "温暖道别",
]
ENDING = [
    "不恋过往", "不负当下", "不畏将来", "一路向前",
    "不念过去", "珍惜现在", "不惧未来", "向阳而行",
    "放下执念", "拥抱此刻", "心怀期待", "步履不停",
    "随遇而安", "顺其自然", "静待花开", "且行且歌",
    "心向阳光", "温柔坚定", "从容前行", "笑对人生",
]

LOCAL_STYLES = [
    lambda g, d, w: f"{g}，今天是{d}，{w}\n山高一程，水远一程，风雨一程，晴暖一程\n所有低谷皆是铺垫，所有失去皆是馈赠\n来时全心奔赴，走时淡然回首\n煮雪烹茶，听雨眠云，不问归期，只问本心",
    lambda g, d, w: f"{g}，今天是{d}，{w}\n你走过的每一条弯路，都是必经之路\n不必追赶，不必慌张\n花开有期，你也有期\n心若不动，风又奈何",
    lambda g, d, w: f"{g}，今天是{d}，{w}\n有些路，走着走着就亮了\n有些人，遇着遇着就暖了\n别急，好戏还在后头\n愿你眼里有光，心中有海，脚下有路",
    lambda g, d, w: f"{g}，今天是{d}，{w}\n生活不会一直温柔，但你可以\n世界不会一直晴朗，但你可以\n做自己该做的事，走自己该走的路\n温柔且坚定，从容且清醒",
    lambda g, d, w: f"{g}，今天是{d}，{w}\n风会记得一朵花的香，时光会记得你努力的样子\n不必事事圆满，但求事事甘心\n慢慢来，比较快\n静水深流，厚积薄发",
]


def local_generate(mode="morning"):
    now = datetime.now()
    date_str = f"{now.month}月{now.day}日"
    weekday = WEEKDAYS_CN[now.weekday()]
    greeting = "早安" if mode == "morning" else "晚安"

    style_idx = random.randint(0, len(LOCAL_STYLES) - 1)
    return LOCAL_STYLES[style_idx](greeting, date_str, weekday)
