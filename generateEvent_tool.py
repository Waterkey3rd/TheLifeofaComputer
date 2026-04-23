import os
import json
import re
import time
import argparse
from openai import OpenAI

# ================= 配置区 =================
# 请替换为你的第三方大模型 API 配置
API_KEY = os.getenv("OPENAI_API_KEY", "your-third-party-api-key")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.your-third-party.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini") # 推荐使用便宜且听话的模型

# 存储路径
DRAFT_DIR = "./backend/data/events/drafts"
APPROVED_DIR = "./backend/data/events/approved"

# 确保目录存在
os.makedirs(DRAFT_DIR, exist_ok=True)
os.makedirs(APPROVED_DIR, exist_ok=True)

# 错误处理：如果没有配置 KEY，给出明确提示
if API_KEY == "your-third-party-api-key":
    print("\n[警告] 您似乎还没有配置 OPENAI_API_KEY 环境变量！")
    print("这可能导致生成失败。请确保配置了正确的第三方 API 信息。\n")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ================= Prompt 模板 =================

SYSTEM_PROMPT = """你是一个大学模拟经营游戏《赛博校园生存指南》的资深游戏策划与数值设计师。
你的任务是根据给定的主题和类型，生成一个符合 JSON 规范的随机事件。

【事件类型说明】
1. routine (一般事件): 发生在大一新生的日常生活中，不涉及大修。重点是考察和提升电脑知识。必须包含选择，根据选择有不同的结果。
2. crisis (紧急事件): 电脑出现严重故障（如蓝屏、异响、黑屏）。选项必须包含“找网协(免费靠谱)”、“找学服(昂贵坑人)”、“找外头/自己修”等。
3. random (随机事件): 侧重于金钱的增减、校园生活，特别是【防诈骗】、【网络安全】。

【JSON 严格输出格式】
你必须且只能输出一个合法的 JSON 对象，不要输出任何 Markdown 标记（如 ```json ），格式如下：
{
  "event_id": "自动生成一个英文唯一ID",
  "event_type": "routine 或 crisis 或 random",
  "tags": ["标签1", "标签2"],
  "is_unique": false,
  "weight": 100,
  "prerequisites": {},
  "title": "事件中文标题",
  "description": "事件的生动描述，带点幽默或无厘头的大学生活气息",
  "technical_context": "硬核的电脑科普知识或防诈骗科普",
  "options": [
    {
      "option_id": "opt_1",
      "text": "选项文字",
      "required_cyber_sense": 0,
      "outcomes": [
        {
          "probability": 1.0,
          "result_text": "结果描述",
          "stat_changes": {"health_hardware": 0, "health_system": 0, "health_storage": 0, "health_software": 0, "mental_state": 0, "wealth": 0, "cyber_sense": 0}
        }
      ]
    }
  ]
}
注：stat_changes 中的数值可以是正数也可以是负数。缺失的属性默认不改变。
"""

def clean_json_string(raw_string):
    """清理大模型可能返回的 Markdown 标记"""
    cleaned = re.sub(r'^```json\n?', '', raw_string)
    cleaned = re.sub(r'\n?```$', '', cleaned)
    return cleaned.strip()

def generate_event(theme, event_type):
    """调用大模型生成单个事件"""
    print(f"[*] 正在呼叫 AI 生成事件... 主题: [{theme}] | 类型: [{event_type}]")
    
    user_prompt = f"请生成一个类型为 '{event_type}'，主题关于 '{theme}' 的游戏事件。请确保科普知识严谨，校园气息浓厚。"
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=1500
        )
        
        raw_content = response.choices[0].message.content
        clean_content = clean_json_string(raw_content)
        
        # 尝试解析 JSON 以验证合法性
        event_data = json.loads(clean_content)
        return event_data
        
    except json.JSONDecodeError as e:
        print(f"[!] AI 返回的 JSON 格式有误: {e}")
        print(f"原始内容:\n{raw_content}")
        return None
    except Exception as e:
        print(f"[!] API 请求失败: {e}")
        return None

def interactive_review(event_data):
    """人工审查交互系统"""
    print("\n" + "="*60)
    print(f"🎮 标题: {event_data.get('title')}")
    print(f"🏷️  类型: {event_data.get('event_type')} | 标签: {event_data.get('tags')}")
    print(f"📖 描述: {event_data.get('description')}")
    print(f"💡 科普: {event_data.get('technical_context')}")
    print("-" * 60)
    for i, opt in enumerate(event_data.get('options', [])):
        print(f"🔘 选项 {i+1}: {opt.get('text')} (门槛: 常识>{opt.get('required_cyber_sense', 0)})")
        for out in opt.get('outcomes', []):
            print(f"   ↳ [{(out.get('probability', 1)*100):.0f}%] {out.get('result_text')}")
            print(f"      数值变化: {out.get('stat_changes')}")
    print("="*60)
    
    while True:
        choice = input("\n请选择操作 [A]通过保存 / [R]拒绝丢弃 / [E]存入草稿箱: ").strip().lower()
        
        event_id = event_data.get("event_id", f"evt_{int(time.time())}")
        
        if choice == 'a':
            filepath = os.path.join(APPROVED_DIR, f"{event_id}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(event_data, f, ensure_ascii=False, indent=2)
            print(f"[+] 已保存至生产环境目录: {filepath}")
            return True
        elif choice == 'r':
            print("[-] 已丢弃该事件。")
            return False
        elif choice == 'e':
            filepath = os.path.join(DRAFT_DIR, f"{event_id}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(event_data, f, ensure_ascii=False, indent=2)
            print(f"[*] 已保存至草稿箱，后续可人工修改: {filepath}")
            return True
        else:
            print("输入无效，请重新输入 A, R 或 E。")

def interactive_mode():
    """纯交互式引导模式"""
    print("\n" + "*"*40)
    print(" 欢迎使用 网协游戏 - 事件生成终端 ")
    print("*"*40 + "\n")
    
    # 选择事件类型
    print("请选择要生成的事件类型：")
    print("  1. routine (一般事件 - 考察电脑知识的日常)")
    print("  2. crisis  (紧急事件 - 电脑大病，需选择维修机构)")
    print("  3. random  (随机事件 - 校园防诈骗、金钱增减等)")
    
    type_map = {"1": "routine", "2": "crisis", "3": "random"}
    while True:
        type_choice = input("请输入序号 (1/2/3): ").strip()
        if type_choice in type_map:
            event_type = type_map[type_choice]
            break
        print("输入有误，请重新输入。")

    # 输入主题
    theme = input("\n请输入事件的具体主题或灵感 (例如: 室友把泡面汤洒键盘上了): ").strip()
    if not theme:
        theme = "大学生活日常"
        print("未输入主题，使用默认主题: 大学生活日常")

    # 输入数量
    while True:
        count_str = input("\n需要生成多少个此主题的事件？(默认 1): ").strip()
        if not count_str:
            count = 1
            break
        if count_str.isdigit() and int(count_str) > 0:
            count = int(count_str)
            break
        print("请输入一个大于 0 的正整数。")

    # 是否自动跳过审查
    auto_str = input("\n是否开启自动模式？(跳过人工审查，直接全部存入草稿箱) [y/N]: ").strip().lower()
    auto_mode = auto_str == 'y'

    print("\n配置完成，开始生成...\n" + "-"*40)
    run_generation(theme, event_type, count, auto_mode)


def run_generation(theme, event_type, count, auto_mode):
    """执行生成循环"""
    success_count = 0
    for i in range(count):
        print(f"\n>>> 开始生成进度: {i+1} / {count}")
        event = generate_event(theme, event_type)
        
        if not event:
            print("[!] 生成失败，跳过此次。")
            continue
            
        if auto_mode:
            # 自动模式直接丢进草稿箱
            event_id = event.get("event_id", f"evt_{int(time.time())}")
            filepath = os.path.join(DRAFT_DIR, f"{event_id}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(event, f, ensure_ascii=False, indent=2)
            print(f"[*] [自动模式] 已保存至: {filepath}")
            success_count += 1
        else:
            # 人工审查模式
            saved = interactive_review(event)
            if saved:
                success_count += 1
                
        # 如果不是最后一个，稍微停顿防限流
        if i < count - 1:
            time.sleep(1) 
        
    print(f"\n[完成] 计划生成: {count} | 实际保存: {success_count}")


def main():
    parser = argparse.ArgumentParser(description="网协游戏 - 事件批量生成与审查工具")
    parser.add_argument("--theme", type=str, help="生成事件的主题 (如: 宿舍断电, 防诈骗)")
    parser.add_argument("--type", type=str, choices=['routine', 'crisis', 'random'], help="事件大类")
    parser.add_argument("--count", type=int, default=1, help="需要生成的事件数量")
    parser.add_argument("--auto", action="store_true", help="跳过人工审查，直接存入草稿箱")
    
    args = parser.parse_args()
    
    # 逻辑判断：如果用户提供了核心参数(--theme 或 --type)，则走命令行静默模式
    # 如果没有提供任何参数，则进入交互式问答模式
    if args.theme or args.type:
        if not args.theme or not args.type:
            print("错误: 命令行模式下，必须同时提供 --theme 和 --type 参数！")
            parser.print_help()
            return
        run_generation(args.theme, args.type, args.count, args.auto)
    else:
        interactive_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] 收到退出指令，程序已终止。")