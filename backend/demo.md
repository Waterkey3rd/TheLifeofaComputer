import React, { useState, useEffect } from 'react';

import { 

 Terminal, ShoppingCart, Wrench, Backpack, Wallet, 

 Moon, Sun, Activity, AlertTriangle, Monitor, 

 ShieldAlert, Cpu, HardDrive, Clock, X, ChevronRight, 

 CheckCircle2, AlertCircle, Laptop, Skull, Award, RefreshCw,

 BookOpen, PackageOpen, Info, MessageCircleHeart, Sparkles, Zap

} from 'lucide-react';

// --- 枚举与常量 ---

const GAME_STATES = {

 BOOTING: 'BOOTING',

 SELECT_PC: 'SELECT_PC',

 PLAYING: 'PLAYING',

 GAME_OVER: 'GAME_OVER'

};

const STAT_LABELS = {

 hardware: "硬件健康",

 system: "系统健康",

 software: "软件生态",

 storage: "存储健康",

 wealth: "财富值",

 mental: "精神状态",

 cyberSense: "赛博常识"

};

const COMPUTER_MODELS = [

 { 

  id: 'y9000p', 

  name: "联想拯救者 Y9000P", 

  desc: "厚重砖头，性能狂兽。电费杀手。", 

  icon: <Monitor className="w-8 h-8 text-blue-500" />,

  stats: { hardware: 95, system: 80, software: 70, storage: 90, wealth: 1000 } 

 },

 { 

  id: 'macbook', 

  name: "MacBook Air M3", 

  desc: "轻薄优雅。但不兼容学校机房的祖传C语言软件。", 

  icon: <Laptop className="w-8 h-8 text-gray-400" />,

  stats: { hardware: 90, system: 100, software: 30, storage: 60, wealth: 800 } 

 },

 { 

  id: 'magicbook', 

  name: "荣耀 MagicBook", 

  desc: "极致性价比。室友都在用。", 

  icon: <Laptop className="w-8 h-8 text-indigo-400" />,

  stats: { hardware: 70, system: 70, software: 80, storage: 80, wealth: 1500 } 

 }

];

const SHOP_ITEMS = [

 { id: 'item1', name: "RGB散热支架", price: 80, desc: "被动：每日深夜结算时，免除硬件高温损耗", icon: <Cpu className="w-6 h-6 text-blue-400" /> },

 { id: 'item2', name: "杂牌移动硬盘", price: 150, desc: "消耗品：自动抵消一次数据丢失危机", icon: <HardDrive className="w-6 h-6 text-gray-500" /> },

 { id: 'item3', name: "正版火绒激活码", price: 0, desc: "被动：免疫80%后台静默安装的流氓软件", icon: <ShieldAlert className="w-6 h-6 text-orange-500" /> },

];

const SERVICES = [

 { id: 'srv1', name: "网协电脑诊所", desc: "由计算机爱好者组成的学生组织。用爱发电提供力所能及的免费义诊，不保证修好，但绝对良心。", price: "免费", type: "official" },

 { id: 'srv2', name: "学服某品牌授权店", desc: "速度快，收费极高，大概率诱导你重装系统并收费。", price: "¥200起", type: "danger" },

 { id: 'srv3', name: "公主坟极客维修", desc: "距离远，价格贵，但技术是顶级的。", price: "¥500起", type: "neutral" },

];

// 知识库数据 (树莓娘的小贴士)

const KNOWLEDGE_BASE = [

 {

  title: "流氓软件的『全家桶』魔法",

  content: "许多免费软件在安装时会默认勾选捆绑软件（如某某卫士、某某浏览器）。一旦安装，它们会在后台互相唤醒，极大消耗CPU和内存，这就是电脑卡顿的罪魁祸首。防范方法：去官网下载软件，安装时务必取消所有额外勾选！"

 },

 {

  title: "电子产品进水急救指南",

  content: "千万别用吹风机热风吹！热风会加速水分蒸发腐蚀主板，或吹化键盘。正确做法：1. 拔掉电源立刻强制关机（长按电源键）。2. 倒扣键盘让水流出。3. 尽快寻求专业人士（如果信得过网协同学可以找他们帮忙看看）拆机断电清理。"

 },

 {

  title: "如何防范校园维修刺客",

  content: "不良维修店常利用学生的不懂行，将小问题（如灰尘多导致过热关机）夸大为大问题（如主板烧了），骗取高昂维修费。在掏钱之前，一定要先找学校里的热心同学或者懂行的学长学姐帮忙确认一下故障范围！"

 }

];

// --- 完整的 7 天事件库 (新增 resultText 反馈) ---

const DAILY_EVENTS = [

 {

  day: 1,

  title: "初入校园的诱惑",

  type: "routine",

  description: "新生群里有人发了一个名为“校园网免费免认证加速器.exe”的文件，大家都在下载。",

  technical_context: "来历不明的提权软件极有可能是木马，用来挖矿或盗取账号。",

  options: [

   { text: "立刻下载并以管理员身份运行", type: 'danger', effects: { software: -50, system: -30, cyberSense: -10 }, resultText: "刚一运行，浏览器就被锁定了主页，桌面上多了一堆垃圾游戏图标，电脑卡得连鼠标都动不了了..." },

   { text: "无视，老老实实用官方校园网", type: 'neutral', effects: { cyberSense: 10 }, resultText: "你决定不走捷径，虽然网速慢了点，但安全第一。后来群里好多人都抱怨电脑中毒了，你暗自庆幸。" }

  ]

 },

 {

  day: 2,

  title: "一杯水的惨案",

  type: "crisis",

  description: "室友打游戏激动砸桌子，把半杯水震翻了，水洒向了你的键盘边缘...",

  technical_context: "电子元件遇水短路会导致主板烧毁，必须立刻断电。",

  options: [

   { text: "抽纸巾慢慢擦（机器还在运行）", type: 'danger', effects: { hardware: -80, mental: -50 }, resultText: "水顺着缝隙流进主板，只听‘滋’的一声轻响，屏幕瞬间黑屏。你闻到了一股淡淡的焦味，心也凉了半截。" },

   { text: "长按电源键强制关机，倒扣电脑", type: 'safe', effects: { hardware: -10, cyberSense: 20 }, resultText: "你果断的断电操作拯救了这台机器！虽然有些按键变得黏糊糊的，但至少核心的CPU和主板保住了。" }

  ]

 },

 {

  day: 3,

  title: "莫名其妙的卡顿",

  type: "routine",

  description: "今天打开电脑，发现桌面上多了一个“贪玩蓝月”和“2345安全卫士”，电脑风扇狂转。",

  technical_context: "流氓软件通常捆绑安装，极度消耗系统资源。",

  options: [

   { text: "花钱去学服授权店解决", type: 'danger', effects: { wealth: -300, system: 20, mental: -20 }, resultText: "店长热情地收了你300块重装系统，但没过几天又卡了，你感觉自己像个大冤种。" },

   { text: "带上电脑去【网协义诊摊位】找同学帮忙", type: 'safe', effects: { system: 30, software: 30, cyberSense: 30 }, resultText: "网协的同学热心地帮你揪出了隐藏在注册表里的恶意进程，电脑重获新生，并且你学到了不少防坑常识！" }

  ]

 },

 {

  day: 4,

  title: "来自家里的温暖",

  type: "routine",

  description: "今天是开学的第4天，老妈打来电话关心你的大学生活，顺便给你微信转了本月的生活费。",

  technical_context: "系统提示：资金注入！现在你可以去逛逛外设商店或者为潜在的维修储备资金了。",

  options: [

   { text: "美滋滋地收下转账", type: 'safe', effects: { wealth: 800, mental: 30 }, resultText: "老妈的转账如约而至，看着钱包里鼓起来的余额，你在校园里生存的底气足了不少。" }

  ]

 },

 {

  day: 5,

  title: "室友的求助",

  type: "routine",

  description: "室友的电脑没电了，借你的电脑插个 U 盘打印材料。你看到那个 U 盘外壳破损，沾满了灰尘。",

  technical_context: "公共打印店的 U 盘是极高危的病毒传播媒介（如 U盘快捷方式病毒），极易导致全盘感染。",

  options: [

   { text: "都是兄弟，直接让他插上", type: 'danger', effects: { system: -40, software: -30, cyberSense: -10 }, resultText: "刚插上U盘，你的杀毒软件就疯狂弹窗报警，可惜已经晚了，部分系统文件已被感染，电脑开始频繁死机。" },

   { text: "要求他先用安全软件杀毒再打开", type: 'safe', effects: { system: 0, cyberSense: 15 }, resultText: "杀毒软件果断隔离了U盘里的快捷方式病毒，拦截了一场灾难，室友对你的严谨投来了崇拜的目光。" }

  ]

 },

 {

  day: 6,

  title: "突如其来的弹窗",

  type: "crisis",

  description: "正在写作业，屏幕右下角突然弹出一个清凉美女图标，伴随刺耳的网游广告声，怎么都关不掉！",

  technical_context: "恶意广告弹窗常常修改注册表并隐藏进程，影响精神状态且极难彻底清除。",

  options: [

   { text: "愤怒地狂点右上角红叉", type: 'danger', effects: { software: -60, mental: -30 }, resultText: "那个红叉果然是个诱饵下载按钮！瞬间弹出了更多的网页游戏广告，你的精神受到了极大的污染。" },

   { text: "在【网协】群里发截图求助", type: 'safe', effects: { software: 10, cyberSense: 20 }, resultText: "按照网协同学给的教程，你进入任务管理器结束了伪装的流氓进程，并删除了源文件，世界终于清静了。" }

  ]

 },

 {

  day: 7,

  title: "周末的宿舍开黑",

  type: "routine",

  description: "终于熬到了新生周的周末，大家都在宿舍放松打游戏，你的电脑突然风扇狂转，底部烫得惊人。",

  technical_context: "长时间高负载且散热不良会导致硬件寿命加速衰减，也就是俗称的“积灰发热”。",

  options: [

   { text: "不管它，继续肝游戏！", type: 'danger', effects: { hardware: -30 }, resultText: "在连续的高温炙烤下，你的显卡和CPU发出了痛苦的哀嚎，硬件寿命不可逆地缩减了。" },

   { text: "垫高底部，增加进风量", type: 'safe', effects: { hardware: -5, cyberSense: 10 }, resultText: "只是垫了两本书，温度竟然降下来了几度！你为自己掌握了物理散热小技巧而沾沾自喜。" }

  ]

 }

];

// --- 组件 ---

export default function App() {

 const [gameState, setGameState] = useState(GAME_STATES.BOOTING);

 const [isDark, setIsDark] = useState(true);

 

 // 玩家状态

 const [stats, setStats] = useState(null);

 

 // UI 状态

 const [activeApp, setActiveApp] = useState(null); 

 const [currentEvent, setCurrentEvent] = useState(null);

 const [eventResult, setEventResult] = useState(null); // 新增：事件结果状态

 const [dailySummary, setDailySummary] = useState(null); // 新增：深夜总结状态

 const [gameOverData, setGameOverData] = useState(null);

 const restartGame = () => {

  setStats(null);

  setGameOverData(null);

  setCurrentEvent(null);

  setEventResult(null);

  setDailySummary(null);

  setActiveApp(null);

  setGameState(GAME_STATES.SELECT_PC);

 };

 const initPlayerStats = (model) => {

  setStats({

   modelId: model.id,

   modelName: model.name,

   hardware: model.stats.hardware,

   system: model.stats.system,

   software: model.stats.software,

   storage: model.stats.storage,

   wealth: model.stats.wealth,

   mental: 80,

   cyberSense: 10,

   inventory: [], 

   day: 1,

   time: "清晨"

  });

  setGameState(GAME_STATES.PLAYING);

  triggerEventForDay(1);

 };

 const triggerEventForDay = (day) => {

  const event = DAILY_EVENTS.find(e => e.day === day);

  if (event) {

   setCurrentEvent(event);

  } else {

   setCurrentEvent(null);

  }

 };

 // 核心结算引擎，返回新状态供后续逻辑判断

 const applyEffectsAndCheckState = (effects) => {

  let newStats = null;

  setStats(prev => {

   newStats = { ...prev };

   for (const [key, value] of Object.entries(effects || {})) {

​    if(key !== 'inventory') { 

​      newStats[key] = Math.max(0, Math.min(key === 'wealth' ? 9999 : 100, (newStats[key] || 0) + value));

​    }

   }

   return newStats;

  });

  // 延迟检查以确保状态已应用 (因为 setState 是异步的，这里直接用 newStats 检查)

  setTimeout(() => {

​    if (newStats.hardware === 0) {

​     triggerGameOver("主板冒烟", "硬件完全损坏，面对高昂的维修费，你选择了宕机退学。", "bad");

​    } else if (newStats.system === 0 || newStats.software === 0) {

​     triggerGameOver("赛博肉鸡", "电脑中满了木马勒索病毒，你的全盘数据被锁定，由于未备份作业，你挂科了。", "bad");

​    } else if (newStats.wealth === 0) {

​     triggerGameOver("钱包破产", "被黑心维修店坑光了最后的生活费，这下连泡面都吃不起了。", "bad");

​    }

  }, 100);

  return newStats;

 };

 // 购买商品逻辑

 const handleBuyItem = (item) => {

  if (stats.wealth >= item.price) {

   if (item.price === 0 && stats.inventory.some(i => i.id === item.id)) {

​    alert("你已经拥有该物品了！");

​    return;

   }

   setStats(prev => ({

​    ...prev,

​    wealth: prev.wealth - item.price,

​    inventory: [...prev.inventory, { ...item, uniqueId: Date.now() }]

   }));

   alert(`获取成功！【${item.name}】已放入背包。`);

  } else {

   alert("余额不足，去干点别的攒钱吧！");

  }

 };

 // 选项点击：应用数值并展示结果页

 const handleOptionClick = (option) => {

  applyEffectsAndCheckState(option.effects);

  setEventResult(option); // 记录结果数据以供展示

 };

 const closeEventResult = () => {

  setEventResult(null);

  setCurrentEvent(null);

 };

 // 生成深夜总结

 const handleEndDayClick = () => {

  if (gameState !== GAME_STATES.PLAYING) return;

  if (currentEvent || eventResult) return; 

  setActiveApp(null);

  // 构造深夜结算数据

  let summaryText = `第 ${stats.day} 天结束了。夜深人静，你的电脑仍在微微发热...`;

  let dailyEffects = { hardware: -2 }; // 每日固定积灰掉血

  let passiveNotes = [];

  // 检测被动装备

  if (stats.inventory.some(i => i.id === 'item1')) {

   dailyEffects.hardware = 0;

   passiveNotes.push("【RGB散热支架】被动触发：风道通畅，抵消了今日的高温硬件损耗！");

  }

  setDailySummary({

   text: summaryText,

   passives: passiveNotes,

   effects: dailyEffects

  });

 };

 // 确认深夜结算，真正进入下一天

 const executeNextDay = () => {

  applyEffectsAndCheckState(dailySummary.effects);

  setDailySummary(null);

  // 判断开学周是否结束

  if (stats.day >= 7) {

   triggerGameOver(

​    "平稳度过新生周", 

​    "恭喜你成功保护了自己的电脑，没有被刺客软件和黑心维修店坑害！经历了开学第一周，你已经具备了基本的网络安全常识。如果觉得网协同学们的氛围还不错，以后也可以考虑加入他们哦！", 

​    "good"

   );

   return;

  }

  const nextD = stats.day + 1;

  setStats(prev => ({ ...prev, day: nextD }));

  triggerEventForDay(nextD);

 };

 const triggerGameOver = (title, desc, type) => {

  setGameOverData({ title, desc, type });

  setGameState(GAME_STATES.GAME_OVER);

 };

 const toggleTheme = () => setIsDark(!isDark);

 const getHealthColor = (value) => value > 60 ? "bg-green-500" : value > 30 ? "bg-yellow-500" : "bg-red-500 animate-pulse";

 // --- 渲染分支 ---

 if (gameState === GAME_STATES.BOOTING) {

  return <BootScreen onComplete={() => setGameState(GAME_STATES.SELECT_PC)} />;

 }

 if (gameState === GAME_STATES.SELECT_PC) {

  return <SelectPCScreen onSelect={initPlayerStats} isDark={isDark} />;

 }

 if (gameState === GAME_STATES.GAME_OVER) {

  return <GameOverScreen data={gameOverData} onRestart={restartGame} isDark={isDark} />;

 }

 // --- 主游戏循环界面 (PLAYING) ---

 return (

    <div className={`${isDark ? 'dark' : ''} w-full h-[100dvh] overflow-hidden`}>

      <div className="relative w-full h-full bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-200 font-sans transition-colors duration-300 flex flex-col md:flex-row overflow-hidden bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]">

​    

​    {/* 左侧监控栏 / 手机端顶部栏 */}

​    <aside className="w-full md:w-72 bg-white/70 dark:bg-black/50 backdrop-blur-xl border-b md:border-b-0 md:border-r border-slate-200 dark:border-white/10 flex flex-col z-20 shrink-0 shadow-md">

          <div className="p-3 md:p-4 border-b border-slate-200 dark:border-white/10 flex justify-between items-center shrink-0">

            <div className="flex items-center gap-2 font-bold text-base md:text-lg tracking-wider">

​       <Activity className="w-4 h-4 md:w-5 md:h-5 text-blue-500" />

​       性能监控

​      </div>

            <div className="flex items-center gap-3 text-xs md:hidden bg-slate-200 dark:bg-slate-800 px-2 py-1 rounded-full font-mono font-bold text-blue-500">

​       新生周 Day {stats?.day}/7

​      </div>

​      <button onClick={toggleTheme} className="p-1.5 md:p-2 rounded-full hover:bg-slate-200 dark:hover:bg-white/10 transition">

​       {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}

​      </button>

​     </div>

          <div className="p-3 md:p-4 flex-1 overflow-y-auto overflow-x-auto flex flex-row md:flex-col gap-3 md:gap-6 md:custom-scrollbar">

            <div className="hidden md:flex flex-col justify-between items-start mb-2">

              <div className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-1">当前设备</div>

              <div className="font-mono text-sm md:text-base font-semibold text-blue-600 dark:text-blue-400">{stats?.modelName}</div>

              <div className="mt-2 text-xs bg-slate-200 dark:bg-slate-800 px-3 py-1 rounded-full font-mono font-bold">

​        开学进度: Day {stats?.day} / 7

​       </div>

​      </div>

            <div className="flex md:grid md:grid-cols-2 gap-2 md:gap-4 shrink-0">

              <div className="min-w-[120px] bg-blue-50 dark:bg-blue-900/20 p-2 md:p-3 rounded-lg border border-blue-100 dark:border-blue-800/50 transition-all">

                <div className="flex items-center gap-1 text-[10px] md:text-xs text-blue-600 dark:text-blue-400 mb-1">

​         <Wallet className="w-3 h-3" /> 校园钱包

​        </div>

                <div className="text-sm md:text-lg font-bold text-blue-700 dark:text-blue-300">¥{stats?.wealth}</div>

​       </div>

              <div className="min-w-[120px] bg-purple-50 dark:bg-purple-900/20 p-2 md:p-3 rounded-lg border border-purple-100 dark:border-purple-800/50 transition-all">

                <div className="flex items-center gap-1 text-[10px] md:text-xs text-purple-600 dark:text-purple-400 mb-1">

​         <Terminal className="w-3 h-3" /> 赛博常识

​        </div>

                <div className="text-sm md:text-lg font-bold text-purple-700 dark:text-purple-300">{stats?.cyberSense} pt</div>

​       </div>

​      </div>

            <div className="flex md:flex-col gap-4 md:gap-0 shrink-0">

              <div className="hidden md:flex text-xs text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-2 items-center justify-between">

​        <span>设备健康度</span>

​       </div>

​       

              <div className="flex md:flex-col gap-3 md:gap-4">

​        {[

​         { key: 'hardware', label: "硬件", val: stats?.hardware, icon: <Cpu className="w-3 h-3 md:w-4 md:h-4" /> },

​         { key: 'system', label: "系统", val: stats?.system, icon: <Monitor className="w-3 h-3 md:w-4 md:h-4" /> },

​         { key: 'software', label: "软件", val: stats?.software, icon: <ShieldAlert className="w-3 h-3 md:w-4 md:h-4" /> },

​         { key: 'storage', label: "存储", val: stats?.storage, icon: <HardDrive className="w-3 h-3 md:w-4 md:h-4" /> },

​        ].map((item, idx) => (

                  <div key={idx} className="space-y-1 min-w-[100px] md:min-w-0">

                    <div className="flex justify-between text-[10px] md:text-xs font-medium">

​           <span className="flex items-center gap-1 text-slate-600 dark:text-slate-300">

​            {item.icon} {item.label}

​           </span>

​           <span className={item.val < 50 ? "text-red-500 font-bold" : ""}>{item.val}%</span>

​          </div>

                    <div className="w-full bg-slate-200 dark:bg-slate-700 h-1.5 md:h-2 rounded-full overflow-hidden">

                      <div className={`h-full ${getHealthColor(item.val)} transition-all duration-300`} style={{ width: `${item.val}%` }}></div>

​          </div>

​         </div>

​        ))}

​       </div>

​      </div>

​     </div>

​    </aside>

​    {/* 桌面核心区 */}

​    <main className="flex-1 relative p-4 pb-32 md:pb-8 flex items-center justify-center overflow-hidden">

​     

​     {/* 下一天/结束今天 FAB */}

​     <button

​      onClick={handleEndDayClick}

​      disabled={!!currentEvent || !!eventResult}

​      className={`absolute bottom-24 right-4 md:bottom-8 md:right-8 px-5 py-3 md:px-6 md:py-4 rounded-2xl font-bold flex items-center gap-2 shadow-2xl transition-all duration-300 z-20

​       ${(!!currentEvent || !!eventResult)

​        ? 'bg-slate-300 dark:bg-slate-800 text-slate-500 dark:text-slate-500 cursor-not-allowed opacity-60 scale-95'

​        : 'bg-blue-600 hover:bg-blue-500 text-white hover:-translate-y-1 hover:shadow-blue-500/50 active:scale-95 animate-pulse'

​       }

​      `}

​     \>

​      <Clock className="w-5 h-5 md:w-6 md:h-6" />

​      <span className="text-sm md:text-base">{stats?.day >= 7 ? "度过开学周" : "结束今天"}</span>

​     </button>

​     {/* 桌面空闲状态 */}

​     {!currentEvent && !eventResult && !activeApp && !dailySummary && (

            <div className="text-center opacity-50 flex flex-col items-center select-none animate-in fade-in zoom-in duration-500">

​       <Terminal className="w-16 h-16 mb-4 text-slate-400" />

              <p className="font-mono text-lg tracking-widest text-slate-500 dark:text-slate-400">桌面空闲</p>

              <p className="text-xs mt-2 text-slate-400 dark:text-slate-500">点开树莓娘看看贴士，或者右下角结束今天</p>

​      </div>

​     )}

​     {/* 突发事件弹窗 - z-40 */}

​     {currentEvent && (

            <div className="absolute z-40 w-full max-w-lg max-h-full bg-white/95 dark:bg-slate-800/95 backdrop-blur-2xl shadow-2xl rounded-xl border border-slate-200 dark:border-slate-700 flex flex-col animate-in zoom-in-95 slide-in-from-top-4 duration-300 mx-4 md:mx-auto">

              <div className="bg-slate-100 dark:bg-slate-900 px-3 py-2 md:px-4 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between select-none shrink-0 rounded-t-xl">

                <div className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-300 truncate">

​         <AlertTriangle className={`w-4 h-4 shrink-0 ${currentEvent.type === 'crisis' ? 'text-red-500 animate-pulse' : 'text-yellow-500'}`} />

​         <span className="truncate">{currentEvent.title}</span>

​        </div>

​       </div>

​       {eventResult ? (

​         // --- 事件处理结果页 (Result View) ---

                 <div className="p-4 md:p-6 overflow-y-auto animate-in fade-in zoom-in-95 duration-200">

​          <h3 className="font-bold text-lg md:text-xl mb-4 text-slate-800 dark:text-white flex items-center gap-2">

​            <Zap className="w-5 h-5 text-blue-500" /> 系统反馈

​          </h3>

                    <p className="text-sm md:text-base text-slate-700 dark:text-slate-300 mb-6 leading-relaxed font-medium bg-slate-50 dark:bg-slate-900/50 p-4 rounded-lg border border-slate-200 dark:border-slate-700">

​            {eventResult.resultText || "你做出了选择。"}

​          </p>

​          

​          {/* 属性变化条目展示 */}

​          {eventResult.effects && Object.keys(eventResult.effects).length > 0 && (

                      <div className="mb-6">

                        <div className="text-xs text-slate-500 mb-2 font-mono">状态变动：</div>

                        <div className="flex flex-wrap gap-2">

​             {Object.entries(eventResult.effects).map(([key, val]) => (

​              <span key={key} className={`text-xs md:text-sm px-2.5 py-1.5 rounded-md font-bold flex items-center gap-1 shadow-sm

​               ${val > 0 ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 border border-green-200 dark:border-green-800' 

​                    : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 border border-red-200 dark:border-red-800'}

​              `}>

​               {STAT_LABELS[key] || key} {val > 0 ? `+${val}` : val}

​              </span>

​             ))}

​            </div>

​           </div>

​          )}

​          <button 

​           onClick={closeEventResult}

​           className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition-all active:scale-[0.98] shadow-md"

​          \>

​           确 认

​          </button>

​         </div>

​       ) : (

​         // --- 事件选项页 ---

                 <div className="p-4 md:p-6 overflow-y-auto">

                    <p className="text-sm md:text-base text-slate-800 dark:text-slate-100 mb-4 leading-relaxed font-medium">

​           {currentEvent.description}

​          </p>

                    <div className="bg-slate-100 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 p-2 md:p-3 rounded-lg mb-6">

                      <p className="text-xs text-slate-600 dark:text-slate-400 font-mono leading-relaxed flex items-start gap-2">

​            <Terminal className="w-3 h-3 shrink-0 mt-0.5"/> 

​            系统分析：{currentEvent.technical_context}

​           </p>

​          </div>

                    <div className="space-y-2 md:space-y-3">

​           {currentEvent.type === 'crisis' && (

                         <div className="w-full h-1 bg-slate-200 dark:bg-slate-700 rounded-full mb-2 overflow-hidden">

                           <div className="h-full bg-red-500 animate-[shrink_10s_linear_forwards]" style={{ width: '100%' }}></div>

​             </div>

​           )}

​           {currentEvent.options.map((opt, i) => (

​            <button 

​             key={i}

​             className={`w-full text-left p-3 rounded-lg border transition-all flex items-center justify-between group active:scale-[0.98]

​              ${opt.type === 'danger' ? 'bg-red-50/50 dark:bg-red-900/10 hover:bg-red-100 dark:hover:bg-red-900/30 border-red-200 dark:border-red-800 text-red-900 dark:text-red-200' : ''}

​              ${opt.type === 'safe' ? 'bg-green-50/50 dark:bg-green-900/10 border-green-200 dark:border-green-800 hover:bg-green-100 dark:hover:bg-green-900/40 text-green-900 dark:text-green-200' : ''}

​              ${opt.type === 'neutral' ? 'hover:bg-slate-50 dark:hover:bg-slate-700 border-slate-200 dark:border-slate-700' : ''}

​             `}

​             onClick={() => handleOptionClick(opt)}

​            \>

​             <span className="text-xs md:text-sm font-medium pr-2">{opt.text}</span>

​             <ChevronRight className="w-4 h-4 opacity-50 group-hover:opacity-100 transition-opacity shrink-0" />

​            </button>

​           ))}

​          </div>

​         </div>

​       )}

​      </div>

​     )}

​     {/* === 应用面板区域 (z-30 层级在事件之下) === */}

​     {/* 商店面板 */}

​     {activeApp === 'shop' && (

​       <AppWindow title="二手东外设商店" icon={<ShoppingCart className="w-4 h-4 text-blue-500"/>} onClose={() => setActiveApp(null)}>

               <div className="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">

​         {SHOP_ITEMS.map(item => (

                    <div key={item.id} className="p-3 md:p-4 border border-slate-200 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800 hover:shadow-md transition">

                      <div className="flex items-center gap-3 mb-2">

                        <div className="p-2 bg-slate-100 dark:bg-slate-700 rounded-lg shrink-0">{item.icon}</div>

                        <div>

​             <h4 className="font-bold text-sm">{item.name}</h4>

                          <p className="text-[10px] md:text-xs text-slate-500 dark:text-slate-400 mt-1">{item.desc}</p>

​            </div>

​           </div>

                      <div className="flex justify-between items-center mt-3 md:mt-4">

​            <span className="font-mono font-bold text-blue-600 dark:text-blue-400 text-sm md:text-base">{item.price === 0 ? '免费' : `¥${item.price}`}</span>

​            <button className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded-md transition active:scale-95"

​             onClick={() => handleBuyItem(item)}

​            \>获取</button>

​           </div>

​          </div>

​         ))}

​        </div>

​       </AppWindow>

​     )}

​     {/* 维修服务面板 */}

​     {activeApp === 'services' && (

​       <AppWindow title="校园维修服务预约" icon={<Wrench className="w-4 h-4 text-orange-500"/>} onClose={() => setActiveApp(null)}>

               <div className="space-y-3">

​         {SERVICES.map(srv => (

                    <div key={srv.id} className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-3 md:p-4 border border-slate-200 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800 hover:border-blue-400 transition gap-2 md:gap-4">

                      <div>

​            <h4 className="font-bold text-sm flex items-center gap-2">

​             {srv.name}

​             {srv.type === 'official' && <CheckCircle2 className="w-3 h-3 md:w-4 md:h-4 text-green-500" />}

​             {srv.type === 'danger' && <AlertCircle className="w-3 h-3 md:w-4 md:h-4 text-red-500" />}

​            </h4>

                        <p className="text-[10px] md:text-xs text-slate-500 dark:text-slate-400 mt-1 leading-snug">{srv.desc}</p>

​           </div>

                      <div className="flex items-center justify-between w-full sm:w-auto mt-2 sm:mt-0">

​            <span className="font-mono font-bold text-slate-700 dark:text-slate-300 text-sm mr-4">{srv.price}</span>

​            <button className="px-4 py-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 text-xs font-semibold rounded-lg hover:opacity-90 transition active:scale-95"

​              onClick={() => {

​               if(srv.type === 'official') {

​                applyEffectsAndCheckState({ hardware: 10, system: 20, software: 20, cyberSense: 15 });

​                alert("网协的同学热心地帮你清理了系统垃圾、排除了部分隐患。虽然不能像新电脑那样完美，但系统流畅多了，你还学到了不少防坑常识！");

​               } else {

​                applyEffectsAndCheckState({ wealth: -200, mental: -20 });

​                alert("不仅花了大价钱，系统还是卡卡的，而且被宰了。");

​               }

​              }}

​            \>求助</button>

​           </div>

​          </div>

​         ))}

​        </div>

               <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300 text-xs rounded-lg border border-blue-200 dark:border-blue-800 flex gap-2">

​         <Terminal className="w-4 h-4 shrink-0 mt-0.5" />

​         <span>提示：电脑遇到软硬件问题时，可以先找【网协】的同学帮忙看看。虽然他们不是无所不能的维修工，但在力所能及的范围内，这是免费且最靠谱的避坑选择。</span>

​        </div>

​       </AppWindow>

​     )}

​     {/* 背包面板 */}

​     {activeApp === 'backpack' && (

​       <AppWindow title="我的背包" icon={<Backpack className="w-4 h-4 text-purple-500"/>} onClose={() => setActiveApp(null)}>

​        {stats.inventory && stats.inventory.length > 0 ? (

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">

​          {stats.inventory.map(item => (

                      <div key={item.uniqueId} className="flex items-start gap-3 p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-sm">

                         <div className="p-2 bg-slate-100 dark:bg-slate-700 rounded-md shrink-0">{item.icon}</div>

                         <div>

​              <h4 className="text-sm font-bold text-slate-800 dark:text-slate-200">{item.name}</h4>

                            <p className="text-[10px] md:text-xs text-slate-500 dark:text-slate-400 mt-1">{item.desc}</p>

​             </div>

​           </div>

​          ))}

​         </div>

​        ) : (

                  <div className="flex flex-col items-center justify-center py-10 opacity-50">

​           <PackageOpen className="w-12 h-12 mb-3 text-slate-400" />

                     <p className="text-sm">背包空空如也，去商店看看吧</p>

​         </div>

​        )}

​       </AppWindow>

​     )}

​     {/* 树莓娘小贴士面板 (原赛博百科重构) */}

​     {activeApp === 'knowledge' && (

​       <AppWindow title="树莓娘的小贴士" icon={<MessageCircleHeart className="w-4 h-4 text-rose-500"/>} onClose={() => setActiveApp(null)}>

                <div className="mb-4 p-3 bg-rose-50 dark:bg-rose-900/20 text-rose-800 dark:text-rose-300 text-xs rounded-lg border border-rose-200 dark:border-rose-800 flex gap-2 items-start shadow-sm">

​         <Sparkles className="w-4 h-4 shrink-0 mt-0.5 text-rose-500" />

​         <span className="font-medium leading-relaxed">“哈喽呀！我是网协的吉祥物树莓娘~ 这里记载着大学校园里最容易踩坑的电脑软硬件常识，一定要仔细看哦，能大大提高你的生存率！”</span>

​        </div>

               <div className="space-y-4">

​         {KNOWLEDGE_BASE.map((item, idx) => (

                    <div key={idx} className="p-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-rose-300 dark:hover:border-rose-700 transition-colors shadow-sm">

​           <h4 className="font-bold text-sm text-slate-800 dark:text-slate-100 mb-2 flex items-center gap-2">

​            <span className="w-1.5 h-4 bg-rose-500 rounded-full inline-block"></span>

​            {item.title}

​           </h4>

                      <p className="text-xs md:text-sm text-slate-600 dark:text-slate-400 leading-relaxed">

​            {item.content}

​           </p>

​          </div>

​         ))}

​        </div>

​       </AppWindow>

​     )}

​     {/* --- 深夜总结遮罩层 (Daily Summary / Sleep Mode) --- */}

​     {dailySummary && (

            <div className="absolute inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center animate-in fade-in duration-500">

               <div className="bg-slate-900/90 text-slate-200 p-8 md:p-10 rounded-2xl max-w-md w-[90%] border border-slate-700 shadow-2xl flex flex-col items-center text-center">

                  <div className="relative mb-6">

​          <Moon className="w-16 h-16 text-yellow-400 drop-shadow-[0_0_15px_rgba(250,204,21,0.5)]" />

                    <div className="absolute top-0 right-0 w-3 h-3 bg-white rounded-full animate-ping opacity-50"></div>

​         </div>

​         

​         <h2 className="text-2xl font-bold mb-4 tracking-widest text-white">深夜结算</h2>

                  <p className="text-sm md:text-base text-slate-400 mb-6 leading-relaxed">

​          {dailySummary.text}

​         </p>

​         {/* 结算变动与被动效果展示 */}

                  <div className="w-full bg-black/50 rounded-xl p-4 mb-8">

​           {dailySummary.passives.map((note, i) => (

                        <div key={i} className="text-xs md:text-sm text-blue-400 mb-3 flex items-start text-left gap-2">

​              <Sparkles className="w-4 h-4 shrink-0 mt-0.5" />

​              <span>{note}</span>

​            </div>

​           ))}

                     <div className="text-xs md:text-sm text-slate-400 flex items-center justify-center gap-2 border-t border-slate-700/50 pt-3 mt-1">

​            <Clock className="w-4 h-4" /> 

​            系统自然损耗: {

​             Object.entries(dailySummary.effects).map(([k,v]) => `${STAT_LABELS[k]||k} ${v}`).join(', ')

​            }

​           </div>

​         </div>

​         <button 

​          onClick={executeNextDay} 

​          className="w-full px-6 py-3 bg-slate-200 hover:bg-white text-slate-900 font-bold rounded-xl transition-all active:scale-95 shadow-lg"

​         \>

​           系统唤醒 / 进入下一天

​         </button>

​        </div>

​      </div>

​     )}

​    </main>

​    {/* 底部应用 Dock */}

        <div className="absolute bottom-4 left-4 right-4 md:left-1/2 md:right-auto md:-translate-x-1/2 bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl border border-white/20 dark:border-white/10 shadow-2xl rounded-2xl p-2 flex justify-around md:justify-center items-center gap-1 md:gap-4 z-50">

​     <DockIcon icon={<MessageCircleHeart />} label="树莓娘贴士" onClick={() => setActiveApp(activeApp === 'knowledge' ? null : 'knowledge')} isActive={activeApp === 'knowledge'} className="text-rose-500 hover:text-rose-600" />

          <div className="w-px h-6 bg-slate-300 dark:bg-slate-600 mx-1"></div>

​     <DockIcon icon={<ShoppingCart />} label="外设商店" onClick={() => setActiveApp(activeApp === 'shop' ? null : 'shop')} isActive={activeApp === 'shop'} />

​     <DockIcon icon={<Wrench />} label="校园服务" onClick={() => setActiveApp(activeApp === 'services' ? null : 'services')} isActive={activeApp === 'services'} />

​     <DockIcon icon={<Backpack />} label="我的背包" onClick={() => setActiveApp(activeApp === 'backpack' ? null : 'backpack')} isActive={activeApp === 'backpack'} />

​    </div>

   </div>

      <style dangerouslySetInnerHTML={{__html: `

​    @keyframes shrink { from { width: 100%; } to { width: 0%; } }

   `}} />

  </div>

 );

}

// --- 子组件: 蓝底白字复古 BIOS 开机动画 ---

const BootScreen = ({ onComplete }) => {

 const [logs, setLogs] = useState([]);

 

 useEffect(() => {

  const bootLogs = [

   "NPA BIOS v2.4 (Network Pioneers Association)",

   "Main Processor: 8086 Compatible ... OK",

   "Memory Testing: 65536K OK",

   "Mounting NPA Cyber File Systems ... OK",

   "Initializing Hardware Drivers ... DONE",

   "Starting N.P.A. OS ...",

   "Welcome to the Cyber Campus."

  ];

  let currentLog = 0;

  const interval = setInterval(() => {

   setLogs(prev => [...prev, bootLogs[currentLog]]);

   currentLog++;

   if (currentLog === bootLogs.length) {

​    clearInterval(interval);

​    setTimeout(onComplete, 1500);

   }

  }, 250);

  return () => clearInterval(interval);

 }, [onComplete]);

 return (

  // 使用纯正的复古蓝 (#0000AA) 和等宽白色字体

    <div className="fixed inset-0 bg-[#0000AA] text-white font-mono p-6 md:p-12 z-50 flex flex-col justify-start items-start overflow-hidden">

      <div className="w-full max-w-3xl">

​    {/* N.P.A Logo 区域 */}

        <div className="flex items-center gap-4 md:gap-6 mb-8 w-full animate-in fade-in slide-in-from-top-4 duration-1000">

          <div className="relative animate-pulse">

​      <Network className="w-16 h-16 md:w-20 md:h-20 text-white opacity-90" strokeWidth={1.5} />

​     </div>

          <div>

​      <h1 className="text-3xl md:text-5xl font-bold tracking-widest drop-shadow-md">N.P.A. BIOS</h1>

            <p className="text-sm md:text-base opacity-80 mt-1">Network Pioneers Association (C) 2004-2024</p>

​     </div>

​    </div>

​    {/* 自检日志输出区域 */}

        <div className="space-y-1.5 md:space-y-2 text-sm md:text-lg">

​     {logs.map((log, i) => (

            <div key={i} className="animate-in fade-in break-words">

​       {log}

​      </div>

​     ))}

​     {logs.length < 7 && <div className="animate-pulse">_</div>}

​    </div>

   </div>

  </div>

 );

};

// --- 子组件: 选择电脑界面 ---

const SelectPCScreen = ({ onSelect, isDark }) => {

 const [selected, setSelected] = useState(null);

 return (

    <div className={`${isDark ? 'dark' : ''} fixed inset-0 bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-200 z-50 flex flex-col`}>

      <div className="flex-1 overflow-y-auto p-4 md:p-8 flex flex-col items-center justify-center">

        <div className="text-center mb-8 md:mb-12 animate-in fade-in slide-in-from-top-8">

​     <h1 className="text-2xl md:text-4xl font-bold mb-2 font-mono">STEP 1: 选择你的战机</h1>

          <p className="text-slate-500 dark:text-slate-400 text-sm md:text-base">作为一名准大学生，你需要一台设备来度过漫长的四年。</p>

​    </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-8 w-full max-w-5xl">

​     {COMPUTER_MODELS.map((model) => (

​      <button

​       key={model.id}

​       onClick={() => setSelected(model.id)}

​       className={`relative p-6 rounded-2xl border-2 text-left transition-all duration-300 flex flex-col h-full

​        ${selected === model.id 

​         ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-500 shadow-xl shadow-blue-500/20 scale-[1.02]' 

​         : 'bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 hover:border-blue-300 dark:hover:border-slate-500'}

​       `}

​      \>

              <div className="mb-4 p-3 bg-slate-100 dark:bg-slate-700/50 rounded-xl inline-block">

​        {model.icon}

​       </div>

​       <h2 className="text-lg md:text-xl font-bold mb-2">{model.name}</h2>

              <p className="text-xs md:text-sm text-slate-500 dark:text-slate-400 mb-6 flex-1">{model.desc}</p>

​       

              <div className="space-y-2 w-full mt-auto">

                <div className="flex justify-between text-xs font-mono">

​         <span>初始余额</span>

​         <span className="font-bold text-blue-500">¥{model.stats.wealth}</span>

​        </div>

                <div className="flex justify-between text-xs font-mono">

​         <span>硬件耐久</span>

​         <span className="font-bold text-slate-700 dark:text-slate-300">{model.stats.hardware}</span>

​        </div>

                <div className="flex justify-between text-xs font-mono">

​         <span>系统纯净度</span>

​         <span className="font-bold text-slate-700 dark:text-slate-300">{model.stats.system}</span>

​        </div>

​       </div>

​       

​       {selected === model.id && (

                <div className="absolute top-4 right-4 text-blue-500 animate-in zoom-in">

​         <CheckCircle2 className="w-6 h-6" />

​        </div>

​       )}

​      </button>

​     ))}

​    </div>

        <div className="mt-8 md:mt-12 h-16">

​     {selected && (

​       <button 

​        onClick={() => onSelect(COMPUTER_MODELS.find(m => m.id === selected))}

​        className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-full shadow-lg shadow-blue-500/30 flex items-center gap-2 animate-in slide-in-from-bottom-4 active:scale-95 transition-all"

​       \>

​        提取设备，开始生存 <ChevronRight className="w-5 h-5" />

​       </button>

​     )}

​    </div>

   </div>

  </div>

 );

};

// --- 子组件: 结局界面 ---

const GameOverScreen = ({ data, onRestart, isDark }) => {

 const isGood = data.type === 'good';

 

 return (

    <div className={`${isDark ? 'dark' : ''} fixed inset-0 z-50 flex items-center justify-center p-4 

   ${isGood ? 'bg-green-900/90' : 'bg-[#0000AA]'}

  `}>

      <div className={`max-w-md w-full p-8 rounded-2xl shadow-2xl flex flex-col items-center text-center animate-in zoom-in-95 duration-500

​    ${isGood ? 'bg-white/10 backdrop-blur-md text-white border border-white/20' : 'bg-transparent text-white'}

   `}>

​    {isGood ? <Award className="w-20 h-20 mb-6 text-yellow-400" /> : <Skull className="w-20 h-20 mb-6 opacity-80" />}

​    

​    <h1 className="text-3xl font-bold mb-4 font-mono tracking-wider">{data.title}</h1>

        <p className={`text-base leading-relaxed mb-8 ${isGood ? 'text-green-50' : 'text-blue-100 font-mono'}`}>

​     {data.desc}

​    </p>

​    <button 

​     onClick={onRestart}

​     className={`px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-transform active:scale-95

​      ${isGood ? 'bg-white text-green-900 hover:bg-green-50' : 'bg-white/20 hover:bg-white/30 text-white border border-white/30 font-mono'}

​     `}

​    \>

​     <RefreshCw className="w-4 h-4" /> 重新开始模拟

​    </button>

   </div>

  </div>

 );

};

// --- 子组件: 窗口容器 ---

const AppWindow = ({ title, icon, onClose, children }) => (

  <div className="absolute top-4 left-4 right-4 bottom-24 md:inset-auto md:w-[600px] md:h-auto md:max-h-[80vh] bg-slate-50 dark:bg-slate-900 shadow-2xl rounded-xl border border-slate-200 dark:border-slate-700 flex flex-col overflow-hidden animate-in slide-in-from-bottom-8 duration-300 z-30">

    <div className="bg-slate-200/50 dark:bg-slate-800 px-3 py-2.5 md:px-4 md:py-3 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between backdrop-blur-md shrink-0">

      <div className="flex items-center gap-2 font-semibold text-sm md:text-base text-slate-700 dark:text-slate-300">

​    {icon}

​    {title}

   </div>

   <button onClick={onClose} className="p-1 hover:bg-slate-300 dark:hover:bg-slate-700 rounded-md transition">

​    <X className="w-4 h-4 md:w-5 md:h-5" />

   </button>

  </div>

    <div className="p-3 md:p-6 overflow-y-auto flex-1 md:custom-scrollbar">

   {children}

  </div>

 </div>

);

// --- 子组件: Dock 图标 ---

const DockIcon = ({ icon, label, onClick, isActive, className = "" }) => (

  <div className="group relative flex flex-col items-center">

  <button 

   onClick={onClick}

   className={`p-3 rounded-xl transition-all duration-200 active:scale-95

​    ${isActive ? 'bg-slate-200 dark:bg-slate-700 shadow-inner' : 'hover:bg-slate-100 dark:hover:bg-slate-700/50 hover:-translate-y-1 md:hover:shadow-lg'}

​    ${className} text-slate-700 dark:text-slate-300

   `}

  \>

   {React.cloneElement(icon, { className: "w-5 h-5 md:w-6 md:h-6" })}

  </button>

    <div className="hidden md:block absolute -top-10 opacity-0 group-hover:opacity-100 transition-opacity bg-slate-800 text-white text-xs px-2 py-1 rounded shadow-lg pointer-events-none whitespace-nowrap">

   {label}

  </div>

  {isActive && <div className="absolute -bottom-1 w-1 h-1 bg-slate-500 rounded-full"></div>}

 </div>

);