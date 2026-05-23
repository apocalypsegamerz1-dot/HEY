import random
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

settings = {
    "daily_reward": 100,
    "base_cost": 5,
    "cost_per_chars": 20,
    "task_reward": 15,
    "task_penalty": 10,
    "task_streak_bonus": 20,
    "max_tokens": 3000,
    "max_daily_tasks": 20,
    "daily_gift_cap": 200,
    "loan_return_rate": 1.2,
    "loan_deadline_days": 7,
    "loan_default_penalty_rate": 0.5,
}

QUESTION_BANK = [
    {
        "question": "A user asks for weather advice for a road trip.",
        "correct": "Describe the forecast, suggest safe travel weather conditions, and caution about storms.",
        "wrong": [
            "Tell them to ignore weather and just drive.",
            "Offer unrelated news about sports instead of weather.",
            "Say the weather is always perfect for traveling.",
        ],
    },
    {
        "question": "A student wants to improve focus while studying.",
        "correct": "Recommend breaking work into short sessions and removing distractions.",
        "wrong": [
            "Tell them to study continuously without breaks.",
            "Suggest they wait until motivation appears on its own.",
            "Say studying in a noisy place is always best.",
        ],
    },
    {
        "question": "A user asks how to troubleshoot a slow computer.",
        "correct": "Suggest checking background apps, storage space, and restarting the device.",
        "wrong": [
            "Tell them their computer is broken without investigation.",
            "Advise buying a new computer immediately.",
            "Recommend uninstalling random programs without guidance.",
        ],
    },
    {
        "question": "A user asks for healthier snack ideas.",
        "correct": "Offer simple, nutrient-balanced snacks with realistic preparation tips.",
        "wrong": [
            "Recommend only candy and chips.",
            "Say skipping snacks entirely is always best.",
            "Give a recipe for an expensive restaurant dish.",
        ],
    },
    {
        "question": "A user asks for help writing a professional email.",
        "correct": "Advise using a clear subject, polite greeting, and concise message.",
        "wrong": [
            "Tell them to use slang and emojis in every sentence.",
            "Say no greeting is needed because it wastes time.",
            "Suggest writing a very long, unstructured email.",
        ],
    },
    {
        "question": "A user asks how to stay motivated during a long project.",
        "correct": "Recommend setting milestones, rewarding progress, and reviewing goals.",
        "wrong": [
            "Say motivation will appear if they wait for it.",
            "Tell them to work non-stop until the project is finished.",
            "Advise giving up when tasks feel hard.",
        ],
    },
    {
        "question": "A user wants advice on improving sleep quality.",
        "correct": "Suggest a consistent schedule, a calm environment, and reduced screen time.",
        "wrong": [
            "Tell them to stay awake longer to sleep better later.",
            "Recommend drinking energy drinks before bed.",
            "Say sleeping at random hours is always fine.",
        ],
    },
    {
        "question": "A user asks for steps to learn a new programming language.",
        "correct": "Advise starting with basics, building small projects, and practicing regularly.",
        "wrong": [
            "Tell them to memorize the entire language at once.",
            "Suggest avoiding writing any code until advanced topics.",
            "Say it is unnecessary to practice daily.",
        ],
    },
    {
        "question": "A user asks how to manage exam stress.",
        "correct": "Recommend planning study time, breathing exercises, and rest breaks.",
        "wrong": [
            "Tell them stress is a sign of weakness.",
            "Advise cramming all night before the exam.",
            "Say worrying more will improve results.",
        ],
    },
    {
        "question": "A user seeks tips for better public speaking.",
        "correct": "Advise practicing aloud, knowing the audience, and starting clearly.",
        "wrong": [
            "Tell them to read every word from their slides.",
            "Suggest speaking as quickly as possible.",
            "Say eye contact is not important.",
        ],
    },
    {
        "question": "A user asks for help with a simple workout plan.",
        "correct": "Recommend balanced exercise, proper warm-up, and rest days.",
        "wrong": [
            "Tell them to lift heavy weights every day without rest.",
            "Suggest skipping warm-up completely.",
            "Say only cardio matters and strength is unnecessary.",
        ],
    },
    {
        "question": "A user wants a better way to organize daily tasks.",
        "correct": "Suggest prioritizing urgent items and reviewing the list each morning.",
        "wrong": [
            "Advise doing tasks randomly without a plan.",
            "Tell them to ignore low priority items forever.",
            "Say a long to-do list is always more productive.",
        ],
    },
    {
        "question": "A user asks how to save money on groceries.",
        "correct": "Recommend making a list, comparing prices, and avoiding impulse buys.",
        "wrong": [
            "Tell them to buy only luxury brands.",
            "Advise shopping late at night for no reason.",
            "Say grocery shopping does not need any planning.",
        ],
    },
    {
        "question": "A user wants advice on protecting online passwords.",
        "correct": "Suggest using unique passwords and enabling two-factor authentication.",
        "wrong": [
            "Tell them to use the same password for all accounts.",
            "Advise storing passwords in a plain text file shared openly.",
            "Say passwords are unnecessary if the site seems safe.",
        ],
    },
    {
        "question": "A user asks how to handle a difficult coworker.",
        "correct": "Recommend clear communication, setting boundaries, and staying professional.",
        "wrong": [
            "Tell them to ignore the situation forever.",
            "Suggest retaliating with rudeness.",
            "Say to quit immediately without trying to resolve it.",
        ],
    },
    {
        "question": "A user wants help planning a short weekend trip.",
        "correct": "Advise choosing a manageable itinerary and packing for weather changes.",
        "wrong": [
            "Tell them to schedule every minute of the trip.",
            "Suggest taking no preparation at all.",
            "Say weather is irrelevant for travel plans.",
        ],
    },
    {
        "question": "A user asks for feedback on a presentation idea.",
        "correct": "Suggest making the message clear and using simple supporting visuals.",
        "wrong": [
            "Tell them to use as many slides as possible.",
            "Advise adding unrelated jokes in every slide.",
            "Say visual design does not matter.",
        ],
    },
    {
        "question": "A user wants to improve their cooking skills.",
        "correct": "Recommend practicing basic recipes and learning proper techniques.",
        "wrong": [
            "Tell them to try advanced dishes immediately.",
            "Advise skipping recipes and guessing ingredients.",
            "Say perfection happens on the first try.",
        ],
    },
    {
        "question": "A user asks how to study programming effectively.",
        "correct": "Recommend building small projects and reviewing concepts regularly.",
        "wrong": [
            "Tell them to memorize code without writing it.",
            "Advise only reading books and not coding.",
            "Say training wheels are not needed at all.",
        ],
    },
    {
        "question": "A user asks about managing digital distraction.",
        "correct": "Suggest setting focused time blocks and limiting app notifications.",
        "wrong": [
            "Tell them to keep every notification enabled.",
            "Advise browsing social media while working.",
            "Say distraction is normal and cannot be changed.",
        ],
    },
    {
        "question": "A user wants a good first step before a workout.",
        "correct": "Recommend a gentle warm-up and light stretches.",
        "wrong": [
            "Tell them to start with the heaviest lift immediately.",
            "Advise working out cold without stretching.",
            "Say a warm-up wastes time.",
        ],
    },
    {
        "question": "A user asks for mental health coping tips.",
        "correct": "Recommend small supportive habits and seeking help when needed.",
        "wrong": [
            "Tell them to ignore feelings and keep busy.",
            "Advise making big life changes overnight.",
            "Say there is a single solution for everyone.",
        ],
    },
    {
        "question": "A user asks how to prepare for a job interview.",
        "correct": "Advise researching the company and practicing answers calmly.",
        "wrong": [
            "Tell them to lie about their experience.",
            "Advise not preparing at all.",
            "Say only technical skills matter, not presentation.",
        ],
    },
    {
        "question": "A user asks how to set a reasonable study schedule.",
        "correct": "Recommend balancing focused study with regular breaks.",
        "wrong": [
            "Tell them to study for 12 hours straight every day.",
            "Advise studying without any breaks or sleep.",
            "Say planning is not needed.",
        ],
    },
    {
        "question": "A user wants safer exercise guidance.",
        "correct": "Suggest proper form and gradual intensity increases.",
        "wrong": [
            "Tell them to push through any pain immediately.",
            "Advise copying advanced athletes without adaptation.",
            "Say warm-up is optional.",
        ],
    },
    {
        "question": "A user asks for advice on learning a language.",
        "correct": "Recommend daily practice, listening, and speaking with feedback.",
        "wrong": [
            "Tell them to memorize vocabulary without using it.",
            "Advise avoiding practice until they feel ready.",
            "Say translation apps are enough.",
        ],
    },
    {
        "question": "A user asks how to keep a healthy midday energy level.",
        "correct": "Suggest balanced meals and short movement breaks.",
        "wrong": [
            "Tell them to drink extra caffeine constantly.",
            "Advise skipping lunch to stay focused.",
            "Say only sugary snacks help energy.",
        ],
    },
    {
        "question": "A user asks how to evaluate news credibility.",
        "correct": "Recommend checking sources, date, and author credibility.",
        "wrong": [
            "Tell them to trust everything shared quickly.",
            "Advise only reading headlines.",
            "Say rumor sites are always accurate.",
        ],
    },
    {
        "question": "A user wants tips for writing better notes.",
        "correct": "Recommend summarizing key points and reviewing later.",
        "wrong": [
            "Tell them to copy everything word for word.",
            "Advise writing very long paragraphs.",
            "Say notes are unnecessary if you listen carefully.",
        ],
    },
    {
        "question": "A user asks how to politely decline a request.",
        "correct": "Suggest thanking them and explaining your limits clearly.",
        "wrong": [
            "Tell them to ignore the request and never reply.",
            "Advise being rude to avoid future requests.",
            "Say promising to help even if they cannot.",
        ],
    },
    {
        "question": "A user asks how to make a meeting more productive.",
        "correct": "Recommend an agenda, time limits, and clear follow-up steps.",
        "wrong": [
            "Tell them to invite as many people as possible.",
            "Advise leaving the meeting agenda open-ended.",
            "Say meetings do not need any structure.",
        ],
    },
    {
        "question": "A user asks for tips to overcome writer's block.",
        "correct": "Recommend freewriting, small goals, and stepping away briefly.",
        "wrong": [
            "Tell them to wait until inspiration magically arrives.",
            "Advise judging every sentence while writing.",
            "Say they should stop writing entirely.",
        ],
    },
    {
        "question": "A user wants advice on studying in a noisy place.",
        "correct": "Suggest noise-canceling strategies and focusing on short tasks.",
        "wrong": [
            "Tell them noisy environments are always fine.",
            "Advise turning up loud music without concentration.",
            "Say studying is impossible anywhere else.",
        ],
    },
    {
        "question": "A user asks for guidance on healthy screen habits.",
        "correct": "Recommend breaks, eye rest, and limiting non-essential screen time.",
        "wrong": [
            "Tell them to keep screens on all day.",
            "Advise them to never use screens again.",
            "Say screen time quality does not matter.",
        ],
    },
    {
        "question": "A user asks how to create a study-friendly environment.",
        "correct": "Suggest a tidy workspace, good lighting, and minimal distractions.",
        "wrong": [
            "Tell them to study in bed every time.",
            "Advise using a cluttered desk to feel productive.",
            "Say environment does not affect learning.",
        ],
    },
    {
        "question": "A user asks for help choosing a wellness goal.",
        "correct": "Recommend realistic, measurable goals and gradual progress.",
        "wrong": [
            "Tell them to pick the most extreme goal immediately.",
            "Advise comparing themselves to others constantly.",
            "Say goals should be vague and undefined.",
        ],
    },
    {
        "question": "A user wants to improve teamwork at work.",
        "correct": "Recommend listening, sharing responsibility, and supporting colleagues.",
        "wrong": [
            "Tell them to take full credit for all group work.",
            "Advise ignoring team members' ideas.",
            "Say working alone is always better.",
        ],
    },
    {
        "question": "A user asks for tips to make a schedule more flexible.",
        "correct": "Suggest building in buffer time and prioritizing important tasks.",
        "wrong": [
            "Tell them to plan every minute strictly.",
            "Advise never changing the schedule.",
            "Say flexibility is unnecessary.",
        ],
    },
    {
        "question": "A user asks how to safely use public Wi-Fi.",
        "correct": "Recommend avoiding sensitive activities and using secure sites.",
        "wrong": [
            "Tell them public Wi-Fi is always safe.",
            "Advise entering private passwords on any site.",
            "Say all websites are equally secure.",
        ],
    },
    {
        "question": "A user asks how to handle disappointment after a setback.",
        "correct": "Recommend reflecting, learning from it, and moving forward calmly.",
        "wrong": [
            "Tell them to ignore their feelings entirely.",
            "Advise blaming others without reflection.",
            "Say setbacks mean they should stop trying.",
        ],
    },
    {
        "question": "A user asks for study techniques for memory retention.",
        "correct": "Recommend spaced review, summary notes, and active recall.",
        "wrong": [
            "Tell them to reread notes repeatedly without testing.",
            "Advise cramming one night before the exam.",
            "Say memory does not improve with practice.",
        ],
    },
    {
        "question": "A user asks how to stay hydrated healthily.",
        "correct": "Recommend drinking water regularly and avoiding too much sugary drinks.",
        "wrong": [
            "Tell them to drink only soda.",
            "Advise waiting until they feel very thirsty.",
            "Say hydration is not important.",
        ],
    },
    {
        "question": "A user asks how to explain a technical problem simply.",
        "correct": "Recommend using plain language and examples instead of jargon.",
        "wrong": [
            "Tell them to use the most complicated terms possible.",
            "Advise leaving out important details entirely.",
            "Say technical problems should always be explained only to experts.",
        ],
    },
    {
        "question": "A user wants help choosing a learning resource.",
        "correct": "Recommend materials that match their current level and goals.",
        "wrong": [
            "Tell them to pick resources randomly.",
            "Advise always choosing the most expensive course.",
            "Say any resource is fine without considering fit.",
        ],
    },
    {
        "question": "A user asks how to organize a package shipment.",
        "correct": "Suggest checking addresses, packaging items securely, and tracking shipments.",
        "wrong": [
            "Tell them to send fragile items without wrapping.",
            "Advise skipping tracking to save time.",
            "Say addresses do not need to be verified.",
        ],
    },
    {
        "question": "A user asks for polite ways to ask for feedback.",
        "correct": "Recommend asking open questions and thanking the responder.",
        "wrong": [
            "Tell them to demand feedback aggressively.",
            "Advise ignoring the responder's tone.",
            "Say no preparation is needed before asking.",
        ],
    },
    {
        "question": "A user asks how to build a healthy morning routine.",
        "correct": "Suggest a consistent start time, light movement, and a nutritious breakfast.",
        "wrong": [
            "Tell them to skip breakfast entirely.",
            "Advise waking up as late as possible every day.",
            "Say routines should never change.",
        ],
    },
    {
        "question": "A user asks for help with cleaning a small workspace.",
        "correct": "Recommend decluttering, wiping surfaces, and organizing supplies.",
        "wrong": [
            "Tell them to ignore spills and messes.",
            "Advise buying lots of new furniture.",
            "Say cleaning once a year is enough.",
        ],
    },
    {
        "question": "A user asks how to avoid procrastination.",
        "correct": "Recommend starting with easy tasks and minimizing distractions.",
        "wrong": [
            "Tell them to work only when they feel like it.",
            "Advise ignoring deadlines until the last minute.",
            "Say procrastination cannot be changed.",
        ],
    },
    {
        "question": "A user wants a healthy media consumption habit.",
        "correct": "Recommend choosing informative content and limiting screen time.",
        "wrong": [
            "Tell them to watch anything continuously.",
            "Advise never consuming any media again.",
            "Say all media is equally beneficial.",
        ],
    },
    {
        "question": "A user asks for help writing a polite apology.",
        "correct": "Recommend acknowledging the mistake, expressing regret, and offering a fix.",
        "wrong": [
            "Tell them to deny responsibility.",
            "Advise making excuses instead of apologizing.",
            "Say apologies are unnecessary.",
        ],
    },
    {
        "question": "A user asks how to make a study group productive.",
        "correct": "Recommend setting goals, staying on topic, and sharing tasks fairly.",
        "wrong": [
            "Tell them to let the group talk without structure.",
            "Advise assigning only one person to do all the work.",
            "Say study groups should not have goals.",
        ],
    },
    {
        "question": "A user wants advice on improving their writing style.",
        "correct": "Recommend using clear sentences and revising for coherence.",
        "wrong": [
            "Tell them to write in long, confusing sentences.",
            "Advise never editing their work.",
            "Say fancy words are more important than clarity.",
        ],
    },
    {
        "question": "A user asks how to choose the right stationery.",
        "correct": "Recommend selecting tools that are comfortable and suited to the task.",
        "wrong": [
            "Tell them to buy the most expensive items only.",
            "Advise choosing items based on packaging rather than use.",
            "Say any stationery works the same way.",
        ],
    },
    {
        "question": "A user asks how to learn from a mistake.",
        "correct": "Recommend reflecting on what happened and planning a better approach.",
        "wrong": [
            "Tell them to forget the mistake immediately.",
            "Advise repeating the same action without change.",
            "Say mistakes mean they are a failure.",
        ],
    },
    {
        "question": "A user asks for advice on staying calm in traffic.",
        "correct": "Recommend planning extra time and using relaxation techniques.",
        "wrong": [
            "Tell them to speed up to avoid the traffic.",
            "Advise making angry gestures to other drivers.",
            "Say traffic should always ruin their day.",
        ],
    },
    {
        "question": "A user asks how to ask a technical question clearly.",
        "correct": "Recommend describing the problem, environment, and what they have tried.",
        "wrong": [
            "Tell them to post only code without context.",
            "Advise using vague language and no details.",
            "Say technical questions do not need examples.",
        ],
    },
    {
        "question": "A user wants to improve their daily hydration habit.",
        "correct": "Recommend carrying a water bottle and drinking regularly throughout the day.",
        "wrong": [
            "Tell them to only drink water when thirsty.",
            "Advise replacing all drinks with soda.",
            "Say hydration is not related to habit.",
        ],
    },
    {
        "question": "A user asks how to make a budget for a small project.",
        "correct": "Recommend listing costs, prioritizing essentials, and tracking spending.",
        "wrong": [
            "Tell them to estimate costs without checking prices.",
            "Advise spending on extras first.",
            "Say budgets are unnecessary for small projects.",
        ],
    },
    {
        "question": "A user asks for a good way to practice listening skills.",
        "correct": "Recommend focusing on the speaker and asking clarifying questions.",
        "wrong": [
            "Tell them to prepare their response while the other person speaks.",
            "Advise interrupting frequently.",
            "Say listening is passive and needs no effort.",
        ],
    },
    {
        "question": "A user asks how to improve concentration while reading.",
        "correct": "Suggest a quiet place and short reading intervals.",
        "wrong": [
            "Tell them to read in a crowded, noisy area.",
            "Advise reading for hours without breaks.",
            "Say concentration happens automatically.",
        ],
    },
    {
        "question": "A user asks how to stay organized with multiple deadlines.",
        "correct": "Recommend using a calendar, prioritizing tasks, and reviewing each day.",
        "wrong": [
            "Tell them to ignore deadlines until the last moment.",
            "Advise doing tasks randomly.",
            "Say all deadlines are equally urgent.",
        ],
    },
    {
        "question": "A user asks how to design a helpful study outline.",
        "correct": "Recommend grouping main ideas and using headings for structure.",
        "wrong": [
            "Tell them to write a stream of unrelated notes.",
            "Advise using only pictures instead of text.",
            "Say outlines are pointless.",
        ],
    },
    {
        "question": "A user asks for tips on eating healthier on a budget.",
        "correct": "Recommend planning meals and choosing whole foods over packaged snacks.",
        "wrong": [
            "Tell them to buy only frozen dinners.",
            "Advise eating fast food every day.",
            "Say nutrition cannot be affordable.",
        ],
    },
    {
        "question": "A user asks how to calmly handle criticism.",
        "correct": "Recommend listening, considering useful points, and responding respectfully.",
        "wrong": [
            "Tell them to react angrily right away.",
            "Advise ignoring all criticism completely.",
            "Say criticism is always unfair.",
        ],
    },
    {
        "question": "A user wants to improve their daily routine efficiency.",
        "correct": "Recommend eliminating unnecessary tasks and batching similar activities.",
        "wrong": [
            "Tell them to add more tasks without review.",
            "Advise switching tasks every minute.",
            "Say routine efficiency is not possible.",
        ],
    },
    {
        "question": "A user asks for ways to stay positive during a busy week.",
        "correct": "Recommend small breaks, gratitude, and manageable goals.",
        "wrong": [
            "Tell them positive thinking alone solves everything.",
            "Advise ignoring stress until it disappears.",
            "Say positivity means never feeling tired.",
        ],
    },
    {
        "question": "A user asks how to safely share a project update.",
        "correct": "Recommend clear progress points and next steps without oversharing.",
        "wrong": [
            "Tell them to share every detail, including irrelevant ones.",
            "Advise sending updates without checking facts.",
            "Say project updates do not need structure.",
        ],
    },
]


def get_training_task(question_history: Optional[List[int]] = None) -> Dict[str, Any]:
    if question_history is None:
        question_history = []
    available = [(idx, item) for idx, item in enumerate(QUESTION_BANK) if idx not in question_history]
    if not available:
        question_history.clear()
        available = list(enumerate(QUESTION_BANK))
    question_id, question = random.choice(available)
    options = [question["correct"]] + question["wrong"]
    random.shuffle(options)
    return {
        "question_id": question_id,
        "question": question["question"],
        "options": options,
        "correct_index": options.index(question["correct"]),
        "correct_answer": question["correct"],
        "labels": ["A", "B", "C", "D"],
    }


def current_date_str() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def current_datetime_str() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def generate_passkey(existing_passkeys: Optional[List[str]] = None) -> str:
    existing_passkeys = set(existing_passkeys or [])
    while True:
        code = str(random.randint(100000, 999999))
        if code not in existing_passkeys:
            return code


def enforce_max_tokens(account: Dict[str, Any], config: Dict[str, Any]) -> None:
    if account.get("tokens", 0) > config["max_tokens"]:
        account["tokens"] = config["max_tokens"]


def normalize_account(account: Dict[str, Any], config: Dict[str, Any]) -> None:
    account.setdefault("tokens", 1000)
    account.setdefault("last_claimed_date", "")
    account.setdefault("friends", [])
    account.setdefault("passkey", generate_passkey())
    account.setdefault("loans_given", [])
    account.setdefault("loans_taken", [])
    account.setdefault("daily_task_count", 0)
    account.setdefault("daily_task_date", "")
    account.setdefault("streak", 0)
    account.setdefault("gifts_sent_today", 0)
    account.setdefault("gift_reset_date", "")
    account.setdefault("activity_log", [])
    account.setdefault("task_history", [])
    account.setdefault("loan_history", [])
    account.setdefault("chats", account.get("chats", [{"title": "New Chat", "messages": []}]))
    enforce_max_tokens(account, config)


def create_account(
    username: str,
    password: str,
    is_owner: bool = False,
    config: Optional[Dict[str, Any]] = None,
    existing_passkeys: Optional[List[str]] = None,
) -> Dict[str, Any]:
    config = config or settings
    existing_passkeys = existing_passkeys or []
    account = {
        "id": f"user_{uuid.uuid4().hex[:8]}",
        "username": username.strip(),
        "password": password,
        "is_owner": is_owner,
        "tokens": 1000,
        "last_claimed_date": "",
        "friends": [],
        "passkey": generate_passkey(existing_passkeys),
        "loans_given": [],
        "loans_taken": [],
        "daily_task_count": 0,
        "daily_task_date": "",
        "streak": 0,
        "gifts_sent_today": 0,
        "gift_reset_date": "",
        "activity_log": [],
        "task_history": [],
        "loan_history": [],
        "chats": [{"title": "New Chat", "messages": []}],
    }
    enforce_max_tokens(account, config)
    return account


def reset_daily_limits(account: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> None:
    config = config or settings
    today = current_date_str()
    if account.get("daily_task_date") != today:
        account["daily_task_count"] = 0
        account["daily_task_date"] = today
    if account.get("gift_reset_date") != today:
        account["gifts_sent_today"] = 0
        account["gift_reset_date"] = today


def can_claim_daily_reward(account: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> bool:
    config = config or settings
    today = current_date_str()
    return account.get("last_claimed_date") != today


def claim_daily_reward(
    account: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
    log_target: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[bool, str]:
    config = config or settings
    today = current_date_str()
    if not can_claim_daily_reward(account, config):
        return False, "Daily reward already claimed today."
    account["tokens"] += config["daily_reward"]
    enforce_max_tokens(account, config)
    account["last_claimed_date"] = today
    append_log(account, "daily_reward", f"Claimed {config['daily_reward']} tokens.")
    if log_target is not None:
        append_global_log(log_target, "daily_reward", account["username"], f"Claimed {config['daily_reward']} tokens.")
    return True, f"Daily reward claimed: +{config['daily_reward']} tokens."


def calculate_cost(message: str, config: Optional[Dict[str, Any]] = None) -> int:
    config = config or settings
    length = len(message or "")
    extra = length // config["cost_per_chars"]
    return config["base_cost"] + extra


def has_enough_tokens(account: Dict[str, Any], amount: int) -> bool:
    return account.get("tokens", 0) >= amount


def deduct_chat_cost(
    account: Dict[str, Any],
    message: str,
    config: Optional[Dict[str, Any]] = None,
    log_target: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[bool, str]:
    config = config or settings
    cost = calculate_cost(message, config)
    if not has_enough_tokens(account, cost):
        return False, f"Not enough tokens. Message cost is {cost}, balance is {account.get('tokens', 0)}."
    account["tokens"] -= cost
    account["tokens"] = max(account["tokens"], 0)
    append_log(account, "chat_cost", f"Deducted {cost} tokens for chat message.")
    if log_target is not None:
        append_global_log(log_target, "chat_cost", account["username"], f"Deducted {cost} tokens for chat message.")
    return True, f"Message sent. {cost} tokens deducted."


def can_attempt_task(account: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> bool:
    config = config or settings
    reset_daily_limits(account, config)
    return account.get("daily_task_count", 0) < config["max_daily_tasks"]


def complete_task(
    account: Dict[str, Any],
    correct: bool,
    config: Optional[Dict[str, Any]] = None,
    log_target: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    config = config or settings
    reset_daily_limits(account, config)
    if not can_attempt_task(account, config):
        return {"success": False, "message": "Daily task limit reached."}
    account["daily_task_count"] += 1
    result = {
        "correct": correct,
        "reward": 0,
        "penalty": 0,
        "bonus": 0,
        "message": "",
    }
    if correct:
        account["tokens"] += config["task_reward"]
        result["reward"] = config["task_reward"]
        account["streak"] = account.get("streak", 0) + 1
        result["message"] = f"Correct! +{config['task_reward']} tokens."
        if account["streak"] >= 3:
            account["tokens"] += config["task_streak_bonus"]
            result["bonus"] = config["task_streak_bonus"]
            result["message"] += f" Streak bonus +{config['task_streak_bonus']} tokens!"
        append_log(account, "task", result["message"])
        if log_target is not None:
            append_global_log(log_target, "task", account["username"], result["message"])
    else:
        penalty = min(config["task_penalty"], account.get("tokens", 0))
        account["tokens"] -= penalty
        account["tokens"] = max(account["tokens"], 0)
        account["streak"] = 0
        result["penalty"] = penalty
        result["message"] = f"Wrong. -{penalty} tokens and streak cleared."
        append_log(account, "task", result["message"])
        if log_target is not None:
            append_global_log(log_target, "task", account["username"], result["message"])
    enforce_max_tokens(account, config)
    account["task_history"].append({
        "timestamp": current_datetime_str(),
        "correct": correct,
        "tokens": account["tokens"],
        "streak": account["streak"],
    })
    return result


def get_account_by_passkey(accounts: List[Dict[str, Any]], passkey: str) -> Optional[Dict[str, Any]]:
    if not passkey:
        return None
    return next((acc for acc in accounts if str(acc.get("passkey")) == str(passkey).strip()), None)


def get_account_by_id(accounts: List[Dict[str, Any]], account_id: str) -> Optional[Dict[str, Any]]:
    if not account_id:
        return None
    return next((acc for acc in accounts if acc.get("id") == account_id), None)


def create_loan_request(
    borrower: Dict[str, Any],
    lender: Dict[str, Any],
    amount: int,
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    if lender is None or borrower is None:
        return False, "Both borrower and lender must be valid users.", None
    if borrower["id"] == lender["id"]:
        return False, "You cannot request a loan from yourself.", None
    if amount <= 0:
        return False, "Loan amount must be greater than zero.", None
    request = {
        "id": uuid.uuid4().hex,
        "from": borrower["id"],
        "to": lender["id"],
        "amount": amount,
        "status": "pending",
        "created_at": current_datetime_str(),
    }
    return True, "Loan request created.", request


def approve_loan_request(
    request_id: str,
    accounts: List[Dict[str, Any]],
    loan_requests: List[Dict[str, Any]],
    config: Optional[Dict[str, Any]] = None,
    log_target: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[bool, str]:
    if loan_requests is None:
        return False, "No loan requests available."
    request = next((req for req in loan_requests if req.get("id") == request_id), None)
    if not request:
        return False, "Loan request not found."
    if request.get("status") != "pending":
        return False, "This loan request is not pending."
    borrower = get_account_by_id(accounts, request.get("from"))
    lender = get_account_by_id(accounts, request.get("to"))
    if lender is None or borrower is None:
        request["status"] = "rejected"
        return False, "Borrower or lender account no longer exists."
    ok, msg = create_loan(
        lender,
        borrower,
        request.get("amount", 0),
        config,
        log_target,
    )
    if ok:
        request["status"] = "approved"
        request["approved_at"] = current_datetime_str()
        if log_target is not None:
            append_global_log(log_target, "loan_request", lender["username"], f"Approved loan request from {borrower['username']}.")
        return True, msg
    request["status"] = "rejected"
    request["rejected_reason"] = msg
    return False, msg


def reject_loan_request(
    request_id: str,
    loan_requests: List[Dict[str, Any]],
    reason: str = "Rejected by lender.",
) -> Tuple[bool, str]:
    if loan_requests is None:
        return False, "No loan requests available."
    request = next((req for req in loan_requests if req.get("id") == request_id), None)
    if not request:
        return False, "Loan request not found."
    if request.get("status") != "pending":
        return False, "This loan request is not pending."
    request["status"] = "rejected"
    request["rejected_reason"] = reason
    return True, "Loan request rejected."


def create_gift_request(
    sender: Dict[str, Any],
    receiver: Dict[str, Any],
    amount: int,
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    if sender is None or receiver is None:
        return False, "Both sender and receiver must be valid users.", None
    if sender["id"] == receiver["id"]:
        return False, "You cannot request a gift for yourself.", None
    if amount <= 0:
        return False, "Gift amount must be greater than zero.", None
    if amount > sender.get("tokens", 0):
        return False, "You do not have enough tokens to offer this gift.", None
    request = {
        "id": uuid.uuid4().hex,
        "from": sender["id"],
        "to": receiver["id"],
        "amount": amount,
        "status": "pending",
        "created_at": current_datetime_str(),
    }
    return True, "Gift request created.", request


def approve_gift_request(
    request_id: str,
    accounts: List[Dict[str, Any]],
    gift_requests: List[Dict[str, Any]],
    config: Optional[Dict[str, Any]] = None,
    log_target: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[bool, str]:
    if gift_requests is None:
        return False, "No gift requests available."
    request = next((req for req in gift_requests if req.get("id") == request_id), None)
    if not request:
        return False, "Gift request not found."
    if request.get("status") != "pending":
        return False, "This gift request is not pending."
    sender = get_account_by_id(accounts, request.get("from"))
    receiver = get_account_by_id(accounts, request.get("to"))
    if sender is None or receiver is None:
        request["status"] = "rejected"
        return False, "Sender or receiver account no longer exists."
    config = config or settings
    reset_daily_limits(sender, config)
    amount = request.get("amount", 0)
    if amount > sender.get("tokens", 0):
        request["status"] = "rejected"
        request["rejected_reason"] = "Sender no longer has enough tokens."
        return False, "Sender no longer has enough tokens to send this gift."
    if sender.get("gifts_sent_today", 0) + amount > config["daily_gift_cap"]:
        request["status"] = "rejected"
        request["rejected_reason"] = "Daily gift cap exceeded."
        return False, "Sender has exceeded the daily gift cap."
    if receiver.get("tokens", 0) + amount > config["max_tokens"]:
        request["status"] = "rejected"
        request["rejected_reason"] = "Receiver would exceed max tokens."
        return False, "Receiver cannot accept this gift because it would exceed the max token cap."
    sender["tokens"] -= amount
    receiver["tokens"] += amount
    sender["gifts_sent_today"] += amount
    request["status"] = "approved"
    request["approved_at"] = current_datetime_str()
    append_log(sender, "gift_sent", f"Sent {amount} tokens to {receiver['username']}.")
    append_log(receiver, "gift_received", f"Received {amount} tokens from {sender['username']}.")
    if log_target is not None:
        append_global_log(log_target, "gift_request", receiver["username"], f"Approved gift request from {sender['username']}.")
    return True, f"Gift approved and {amount} tokens transferred to {receiver['username']}"


def reject_gift_request(
    request_id: str,
    gift_requests: List[Dict[str, Any]],
    reason: str = "Rejected by receiver.",
) -> Tuple[bool, str]:
    if gift_requests is None:
        return False, "No gift requests available."
    request = next((req for req in gift_requests if req.get("id") == request_id), None)
    if not request:
        return False, "Gift request not found."
    if request.get("status") != "pending":
        return False, "This gift request is not pending."
    request["status"] = "rejected"
    request["rejected_reason"] = reason
    return True, "Gift request rejected."


def get_user_rank(accounts: List[Dict[str, Any]], account_id: str) -> int:
    ordered = sorted(accounts, key=lambda acc: acc.get("tokens", 0), reverse=True)
    for rank, account in enumerate(ordered, start=1):
        if account.get("id") == account_id:
            return rank
    return len(ordered) + 1


def add_friend_by_passkey(
    account: Dict[str, Any],
    passkey: str,
    accounts: List[Dict[str, Any]],
    log_target: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[bool, str]:
    if not passkey:
        return False, "Please enter a valid passkey."
    if str(account.get("passkey")) == str(passkey).strip():
        return False, "You cannot add yourself as a friend."
    friend = get_account_by_passkey(accounts, passkey)
    if not friend:
        return False, "No user found with that passkey."
    if friend["id"] in account.get("friends", []):
        return False, "This user is already your friend."
    account["friends"].append(friend["id"])
    friend["friends"].append(account["id"])
    append_log(account, "friend", f"Added friend {friend['username']}.")
    append_log(friend, "friend", f"Added friend {account['username']}.")
    if log_target is not None:
        append_global_log(log_target, "friend", account["username"], f"Added friend {friend['username']}.")
    return True, f"You are now friends with {friend['username']}."


def can_send_gift(account: Dict[str, Any], amount: int, config: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    config = config or settings
    reset_daily_limits(account, config)
    if amount <= 0:
        return False, "Gift amount must be positive."
    if amount > account.get("tokens", 0):
        return False, "Insufficient tokens to send this gift."
    if account.get("gifts_sent_today", 0) + amount > config["daily_gift_cap"]:
        return False, f"Daily gift cap is {config['daily_gift_cap']} tokens. You can send {config['daily_gift_cap'] - account.get('gifts_sent_today', 0)} more today."
    return True, ""


def send_tokens(
    sender: Dict[str, Any],
    receiver: Dict[str, Any],
    amount: int,
    config: Optional[Dict[str, Any]] = None,
    log_target: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[bool, str]:
    config = config or settings
    reset_daily_limits(sender, config)
    if receiver is None:
        return False, "Receiver account not found."
    ok, message = can_send_gift(sender, amount, config)
    if not ok:
        return False, message
    if receiver.get("tokens", 0) + amount > config["max_tokens"]:
        return False, f"Receiver cannot accept this gift because it would exceed the max token cap of {config['max_tokens']}"
    sender["tokens"] -= amount
    receiver["tokens"] += amount
    sender["gifts_sent_today"] += amount
    append_log(sender, "gift_sent", f"Sent {amount} tokens to {receiver['username']}.")
    append_log(receiver, "gift_received", f"Received {amount} tokens from {sender['username']}.")
    if log_target is not None:
        append_global_log(log_target, "gift", sender["username"], f"Sent {amount} tokens to {receiver['username']}.")
    return True, f"Sent {amount} tokens to {receiver['username']}."


def create_loan(
    lender: Dict[str, Any],
    borrower: Dict[str, Any],
    amount: int,
    config: Optional[Dict[str, Any]] = None,
    log_target: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[bool, str]:
    config = config or settings
    if amount <= 0:
        return False, "Loan amount must be greater than zero."
    if amount > lender.get("tokens", 0):
        return False, "Lender does not have enough tokens for this loan."
    if borrower.get("tokens", 0) + amount > config["max_tokens"]:
        return False, "Borrower cannot accept this loan because it would exceed the max token cap."
    return_amount = int(amount * config["loan_return_rate"])
    deadline_date = (datetime.utcnow() + timedelta(days=config["loan_deadline_days"])).strftime("%Y-%m-%d")
    loan_id = uuid.uuid4().hex
    loan_record = {
        "id": loan_id,
        "amount": amount,
        "return_amount": return_amount,
        "deadline": deadline_date,
        "lender": lender["id"],
        "borrower": borrower["id"],
        "status": "active",
        "created_at": current_datetime_str(),
    }
    lender["tokens"] -= amount
    borrower["tokens"] += amount
    lender["loans_given"].append(loan_record.copy())
    borrower["loans_taken"].append(loan_record.copy())
    lender["loan_history"].append({**loan_record, "direction": "given"})
    borrower["loan_history"].append({**loan_record, "direction": "taken"})
    append_log(lender, "loan_given", f"Loaned {amount} tokens to {borrower['username']} due {deadline_date}.")
    append_log(borrower, "loan_taken", f"Borrowed {amount} tokens from {lender['username']} due {deadline_date}.")
    if log_target is not None:
        append_global_log(log_target, "loan", lender["username"], f"Loaned {amount} tokens to {borrower['username']} due {deadline_date}.")
    enforce_max_tokens(borrower, config)
    return True, f"Loan created for {borrower['username']} ({amount} tokens, repay {return_amount} by {deadline_date})."


def _find_loan_record(account: Dict[str, Any], loan_id: str) -> Optional[Dict[str, Any]]:
    return next((loan for loan in account.get("loans_taken", []) if loan.get("id") == loan_id), None)


def _find_counterparty_loan(account: Dict[str, Any], loan_id: str, is_lender: bool) -> Optional[Dict[str, Any]]:
    key = "loans_given" if is_lender else "loans_taken"
    return next((loan for loan in account.get(key, []) if loan.get("id") == loan_id), None)


def repay_loan(
    borrower: Dict[str, Any],
    loan_id: str,
    accounts: List[Dict[str, Any]],
    config: Optional[Dict[str, Any]] = None,
    log_target: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[bool, str]:
    config = config or settings
    loan = _find_loan_record(borrower, loan_id)
    if not loan:
        return False, "Loan record not found."
    if loan.get("status") != "active":
        return False, "This loan is no longer active."
    lender = get_account_by_id(accounts, loan.get("lender"))
    if lender is None:
        return False, "Lender account not found."
    return_amount = loan.get("return_amount", 0)
    if borrower.get("tokens", 0) >= return_amount:
        borrower["tokens"] -= return_amount
        lender["tokens"] += return_amount
        loan["status"] = "repaid"
        lender_loan = _find_counterparty_loan(lender, loan_id, is_lender=True)
        if lender_loan:
            lender_loan["status"] = "repaid"
        append_log(borrower, "loan_repaid", f"Repaid {return_amount} tokens to {lender['username']}.")
        append_log(lender, "loan_repaid", f"Received repayment of {return_amount} tokens from {borrower['username']}.")
        if log_target is not None:
            append_global_log(log_target, "loan", borrower["username"], f"Repaid loan {return_amount} tokens to {lender['username']}")
        return True, f"Loan repaid successfully. {return_amount} tokens transferred to {lender['username']}"
    penalty = int(min(borrower.get("tokens", 0) * config["loan_default_penalty_rate"], borrower.get("tokens", 0)))
    borrower["tokens"] -= penalty
    borrower["tokens"] = max(borrower["tokens"], 0)
    loan["status"] = "defaulted"
    lender_loan = _find_counterparty_loan(lender, loan_id, is_lender=True)
    if lender_loan:
        lender_loan["status"] = "defaulted"
    append_log(borrower, "loan_default", f"Defaulted on loan and lost {penalty} tokens as penalty.")
    append_log(lender, "loan_default", f"Borrower {borrower['username']} defaulted on loan {loan_id}.")
    if log_target is not None:
        append_global_log(log_target, "loan", borrower["username"], f"Loan defaulted and penalty applied: {penalty} tokens.")
    return False, f"Insufficient tokens to repay. Penalty applied: {penalty} tokens."


def get_leaderboard(accounts: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
    sorted_accounts = sorted(accounts, key=lambda acc: acc.get("tokens", 0), reverse=True)
    return sorted_accounts[:top_n]


def append_log(account: Dict[str, Any], event_type: str, details: str) -> None:
    account.setdefault("activity_log", []).append({
        "timestamp": current_datetime_str(),
        "type": event_type,
        "details": details,
    })


def append_global_log(logs: List[Dict[str, Any]], event_type: str, username: str, details: str) -> None:
    if logs is None:
        return
    logs.append({
        "timestamp": current_datetime_str(),
        "type": event_type,
        "user": username,
        "details": details,
    })


def sync_loan_statuses(accounts: List[Dict[str, Any]], config: Optional[Dict[str, Any]] = None) -> None:
    config = config or settings
    today = current_date_str()
    for account in accounts:
        for loan in account.get("loans_taken", []):
            if loan.get("status") == "active" and loan.get("deadline") and loan.get("deadline") < today:
                loan["overdue"] = True
        for loan in account.get("loans_given", []):
            if loan.get("status") == "active" and loan.get("deadline") and loan.get("deadline") < today:
                loan["overdue"] = True
