const DEFAULT_STORY = `0|你从极夜线三号车厢醒来，车窗外没有城市灯光，只有贴着地面的黑雾。|1
0|腕表终端弹出故障提示：主列车已偏离公开轨道，剩余氧气无法估算。|2
1|前往驾驶台;先查看乘客舱;探出车门观察外部|3;77;79
0|你沿着倾斜的过道走向驾驶台，脚下的地毯被冷凝水泡得发沉。|4
0|驾驶台的玻璃碎了一半，控制屏只剩一条蓝色进度线还在缓慢闪烁。|5
1|读取控制屏;扫描无线电频道;直接检查主控台下方|6;81;6
0|控制屏显示列车仍在自动返程，但返程终点被标记成一串乱码。|7
0|你在主控台下找到一张维修卡，卡面写着：只允许单人进入核心车厢。|8
1|收好维修卡继续前进;打开座椅下的保险盒;尝试唤醒驾驶系统|9;83;9
0|你离开驾驶台，车厢灯忽明忽暗，每一次熄灭都像有人从身后靠近。|10
0|第一节连接门没有锁死，门缝里传来温热的风，和整列车的寒意不相称。|11
0|腕表开始记录你的步数，数字每走十步就自动回退一步。|12
1|穿过连接门;停下监听广播;检查车窗反光|13;85;13
0|连接门后是餐车，桌面摆着没喝完的咖啡，杯沿却结着白霜。|14
0|餐车尽头的服务屏还亮着，上面滚动显示：请不要向终点站透露姓名。|15
0|你把这句话记下来，腕表立刻把它归类为安全提示。|16
1|继续沿餐车前进;读取服务屏日志;关闭服务屏|17;87;17
0|服务屏熄灭后，餐车恢复安静，你听见远处有机械锁连续复位。|18
0|你抵达二号车厢，所有座椅都被安全带绑住，像曾经有人试图固定什么。|19
1|走主通道;查看通风格栅;从座椅间绕行|20;89;20
0|主通道尽头有一台备用发电机，外壳上贴着矿区检修站的旧标签。|21
0|发电机无法启动，旁边留着三个空插槽，其中一个尺寸正好适合维修卡。|22
0|你把维修卡贴上去，机器吐出一张临时通行条。|23
1|拿走通行条;检查通行条背面;把通行条留在原处|24;91;24
0|通行条打开了二号车厢侧门，侧门后是一段狭窄的检修廊。|25
0|检修廊墙壁上排列着细密管线，每根管线上都贴着相同日期。|26
0|日期是明天，时间是你醒来后的第七分钟。|27
1|继续前进;查看急救箱;把日期拍进腕表|28;93;28
0|你没有停太久，检修廊尽头的安全门已经开始倒计时。|29
0|倒计时不是关门，而是开门，它像是在等你走到正确的位置。|30
0|门后出现一截露天月台，月台悬在黑雾上方，没有任何支撑柱。|31
0|站牌写着临时避难点，但站名被人为刮掉，只剩一个空圆环。|32
0|腕表定位忽然恢复一秒，给出坐标后又立刻离线。|33
0|坐标指向轨道尽头的核心车厢，那里应该是列车的独立控制中心。|34
1|按坐标前进;检查月台工具箱;尝试呼叫避难点|35;95;35
0|你沿月台边缘前进，黑雾在脚下翻滚，却始终没有越过黄色安全线。|36
0|前方传来列车自动报站声：下一站，返程点，请确认记忆完整。|37
0|你第一次意识到，这趟列车的问题可能不是脱轨，而是循环。|38
0|月台尽头的门需要通行条，门禁识别后显示：临时乘员权限通过。|39
0|你进入核心连接桥，桥下没有轨道，只有一排还在发热的黑色电缆。|40
0|电缆从所有车厢汇到前方，像把整列车的心跳都拉到同一个地方。|41
0|连接桥中段出现气压波动，你不得不扶住扶手继续往前挪。|42
0|扶手上刻着一行小字：别急着逃出去，先让它停下来。|43
0|你把这句话和服务屏提示放在一起，终于看出两者来自同一个人。|44
0|那个人很可能不是幸存者，而是上一轮还记得事情的人。|45
0|核心车厢门口有三盏灯，蓝灯代表电源，白灯代表制动，红灯代表循环。|46
0|现在只有红灯亮着，而且亮得异常稳定。|47
0|你刷入维修卡，核心门缓慢打开，里面的空气比外面暖得多。|48
0|核心车厢像一间小型机房，中央发电机被透明罩封住。|49
0|罩子上显示：要关闭循环，必须先恢复一次完整供电。|50
1|直接走向发电机;查看核心日志;检查逃生舱|51;97;51
0|你走到中央发电机前，发现三个空插槽分别标着启动、稳定、脱离。|52
0|维修卡只能临时充当启动钥匙，稳定电源还需要从车厢系统借电。|53
0|你把通行条插入稳定槽，机器响起低沉的预热声。|54
0|脱离槽旁边还有一枚手动按钮，按钮上贴着很旧的胶带。|55
0|胶带下面写着：按下前确认广播已经发送。|56
0|你明白逃生不是唯一目标，必须让下一轮的人知道该怎么走到这里。|57
0|核心广播台就在发电机旁，话筒线被人打了一个死结。|58
0|你解开死结，广播台自动接入全列车频道。|59
0|腕表提示：广播内容将保留到下一次系统重启。|60
1|录制路线提示;检查广播台备份;直接跳过广播|61;99;61
0|你用最短的话录下路线：醒来后去驾驶台，拿维修卡，穿过餐车，找到核心。|62
0|广播台确认保存，红灯第一次出现明显闪烁。|63
0|中央发电机完成预热，透明罩自动升起一掌宽。|64
0|你把维修卡和通行条同时推到底，整列车的灯从尾端一节节亮起。|65
0|车窗外的黑雾被灯光压低，露出下面荒废多年的旧轨道。|66
0|系统提示完整供电已恢复，循环锁进入人工确认阶段。|67
0|你按下脱离槽旁的按钮，红灯熄灭，白灯亮起。|68
0|列车开始真正减速，过去那些像幽灵一样的报站声全部断开。|69
0|应急逃生舱从地板下升起，舱门内侧贴着一张手写纸条。|70
0|纸条写着：如果你看见这行字，说明主线终于走通了。|71
0|你坐进逃生舱，把腕表终端接到舱内接口，备份所有路线记录。|72
0|核心屏幕弹出最后一个问题：是否保留支线记录。|73
1|保留支线记录;只保留主线记录|74;74
0|你选择让后来者知道所有岔路都能回来，因为恐惧最怕没有路标。|75
0|逃生舱脱离列车时，极夜线终于报出一个正常站名：黎明站。|76
3|你没有成为另一条世界线的幸存者，你只是把一条主线走到了尽头。|-1
0|乘客舱里空无一人，座椅背后却夹着几张写到一半的求救纸条。|78
0|纸条都指向同一句话：先去驾驶台，别在这里浪费太久。|3
0|你探出车门，外部轨道被黑雾包住，远处有蓝色信标一闪一灭。|80
0|信标方向和驾驶台坐标一致，你退回车内，决定先拿到正式线索。|3
0|无线电频道里只有短促噪声，但噪声间隔正好对应三号车厢编号。|82
0|你记下频率，确认有人曾用无线电留下过路径标记。|6
0|保险盒里有备用熔断片，可惜规格不对，只能作为照明电源。|84
0|你把它插进随身灯，光线稳定下来，足够支撑你继续走主线。|9
0|广播里重复着终点站三个字，语气却像在劝你不要过去。|86
0|你关掉扬声器，只保留关键词，重新回到连接门前。|13
0|服务屏日志显示同一名乘员反复经过餐车，每次都比上一次多留一句提示。|88
0|最后一句提示是：不要在餐车做决定，真正的开关在核心。|17
0|通风格栅里传来敲击声，但节奏很规律，更像维修机器人卡在里面。|90
0|你没有拆开格栅，只把敲击节奏记成检修廊的方向提示。|20
0|通行条背面有一串小字：它不是车票，是临时权限。|92
0|你确认它必须带走，随后回到侧门前继续推进。|24
0|急救箱里只剩一支冷光笔和一卷绷带。|94
0|你用冷光笔标记墙面，给自己留下一条能回到主路的线。|28
0|月台工具箱里有扳手、旧手套和一块写着黎明站的金属牌。|96
0|金属牌证明终点不是骗局，只是必须先关闭循环才能抵达。|35
0|核心日志显示所有支线信息都会被广播系统缓存，不会改变主线目标。|98
0|你把日志保存到腕表，确认最终任务仍是恢复供电并关闭循环。|51
0|广播台备份里有上一轮的半句话：支线别贪，拿到线索就回主路。|61`;

const NODE_W = 250;
const NODE_H = 112;
const WORLD_W = 5000;
const WORLD_H = 5000;
const STORAGE_KEY = "lifeline-story-board-state-v2";
const DEFAULT_CHARACTER_MAP = {
  1: "抄录员",
  2: "无名诗人",
  3: "温迪-风之精灵",
  4: "阿莫斯",
  5: "莱艮芬德",
  6: "高塔孤王",
  7: "古恩希尔德家族族长的女儿"
};

const app = {
  nodes: [],
  edges: [],
  groups: [],
  selectedNodeId: null,
  selectedEdgeId: null,
  selectedGroupId: null,
  groupSelectMode: false,
  camera: { x: 180, y: 24, scale: 1 },
  characterMap: { ...DEFAULT_CHARACTER_MAP },
  minimap: null,
  drag: null,
  issues: []
};

const els = {};

function boot() {
  collectElements();
  const saved = loadSavedState();
  if (saved) {
    app.nodes = saved.nodes;
    app.edges = saved.edges;
    app.groups = saved.groups || [];
    app.camera = saved.camera || app.camera;
    app.characterMap = normalizeCharacterMap(saved.characterMap || DEFAULT_CHARACTER_MAP);
  } else {
    app.characterMap = normalizeCharacterMap(DEFAULT_CHARACTER_MAP);
    loadFromStory(DEFAULT_STORY);
    autoLayout(false);
  }
  renderCharacterMap();
  bindEvents();
  refresh();
}

function collectElements() {
  [
    "storyFile", "layoutFile", "exportStory", "exportLayout", "autoLayout",
    "addStoryNode", "addEndNode", "groupSelect", "collapseGroup", "expandGroup",
    "ungroup", "centerSelected", "resetView", "canvas",
    "world", "edgesSvg", "dragSvg", "nodesLayer", "selectionBox",
    "minimap", "minimapNodes", "minimapViewport", "sourcePreview",
    "applySource", "nodeCount", "edgeCount", "branchCount", "issueCount",
    "issues", "nodeId", "nodeKind", "nodeRole", "characterMap",
    "nodeText", "saveNode", "deleteNode", "edgeEditor", "edgeLabel",
    "saveEdge", "deleteEdge", "search"
  ].forEach((id) => {
    els[id] = document.getElementById(id);
  });
}

function bindEvents() {
  els.canvas.addEventListener("pointerdown", onCanvasPointerDown);
  els.canvas.addEventListener("wheel", onWheel, { passive: false });
  els.minimap.addEventListener("pointerdown", onMinimapPointerDown);
  window.addEventListener("pointermove", onPointerMove);
  window.addEventListener("pointerup", onPointerUp);

  els.exportStory.addEventListener("click", () => download("story.txt", exportStory()));
  els.exportLayout.addEventListener("click", () => download("story_layout.txt", exportLayoutText()));
  els.autoLayout.addEventListener("click", () => autoLayout(true));
  els.addStoryNode.addEventListener("click", () => addNode("story"));
  els.addEndNode.addEventListener("click", () => addNode("end"));
  els.groupSelect.addEventListener("click", toggleGroupSelectMode);
  els.collapseGroup.addEventListener("click", collapseSelectedGroup);
  els.expandGroup.addEventListener("click", expandSelectedGroup);
  els.ungroup.addEventListener("click", ungroupSelected);
  els.centerSelected.addEventListener("click", centerSelected);
  els.resetView.addEventListener("click", resetView);
  els.applySource.addEventListener("click", () => {
    loadFromStory(els.sourcePreview.value);
    autoLayout(false);
    refresh();
  });
  els.saveNode.addEventListener("click", saveSelectedNode);
  els.nodeText.addEventListener("input", syncSelectedNodeText);
  els.nodeKind.addEventListener("change", syncSelectedNodeMeta);
  els.nodeRole.addEventListener("change", syncSelectedNodeMeta);
  els.characterMap.addEventListener("change", onCharacterMapChange);
  els.characterMap.addEventListener("click", onCharacterMapClick);
  els.deleteNode.addEventListener("click", deleteSelectedNode);
  els.saveEdge.addEventListener("click", saveSelectedEdge);
  els.deleteEdge.addEventListener("click", deleteSelectedEdge);
  els.search.addEventListener("input", renderNodes);

  els.storyFile.addEventListener("change", async (event) => {
    const file = event.target.files && event.target.files[0];
    if (!file) return;
    loadFromStory(await file.text());
    autoLayout(false);
    refresh();
  });

  els.layoutFile.addEventListener("change", async (event) => {
    const file = event.target.files && event.target.files[0];
    if (!file) return;
    applyLayoutText(await file.text());
    refresh();
  });
}

function loadFromStory(source) {
  app.nodes = [];
  app.edges = [];
  app.groups = [];
  app.selectedNodeId = null;
  app.selectedEdgeId = null;
  app.selectedGroupId = null;

  const rows = source.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const parsedRows = rows.map((line, index) => {
    const parts = line.split("|");
    const status = parseStatusField(parts[0] || "0");
    return {
      index,
      state: status.state,
      characterId: status.characterId,
      meta: parts[1] || "",
      next: parts[2] || "-1"
    };
  });

  parsedRows.forEach(({ index, state, characterId, meta }) => {
    const kind = state === "3" ? "end" : "story";
  app.nodes.push({
      id: index,
      text: state === "1" ? `选择节点 #${index}` : isAudioState(state) ? parsedRows[index].next : meta,
      kind,
      role: roleFromStatus(state, characterId),
      x: 360,
      y: 80 + index * 150
    });
  });

  parsedRows.forEach(({ index, state, meta, next }) => {
    if (state === "1") {
      const labels = splitList(meta);
      splitList(next).forEach((target, branchIndex) => {
        addEdge(index, Number(target), labels[branchIndex] || `分支 ${branchIndex + 1}`, false);
      });
      return;
    }

    if (isAudioState(state)) {
      if (index + 1 < parsedRows.length) {
        addEdge(index, index + 1, "", false);
      }
      return;
    }

    addEdge(index, Number(next), "", false);
  });
}

function exportStory() {
  const { orderedNodes, nodeIndex } = buildExportModel();
  const lines = orderedNodes
    .map((node) => {
      const outs = outgoing(node.id);
      if (node.kind === "end") {
        const target = outs.length >= 1 ? nodeIndex.get(outs[0].to) : -1;
        return `3|${cleanText(node.text)}|${target ?? -1}`;
      }
      if (isAudioRole(node.role)) {
        return `${stateFromRole(node.role)}|0|${cleanText(node.text) || "0"}`;
      }
      if (outs.length > 1) {
        return `1|${outs.map((edge) => cleanText(edge.label || "继续")).join(";")}|${outs.map((edge) => nodeIndex.get(edge.to) ?? -1).join(";")}`;
      }
      if (outs.length === 1) {
        return `${statusFromNode(node)}|${cleanText(node.text)}|${nodeIndex.get(outs[0].to) ?? -1}`;
      }
      return `3|${cleanText(node.text)}|-1`;
    });

  return lines.join("\n") + "\n";
}

function buildExportModel() {
  const orderedNodes = [];
  const seen = new Set();
  const start = app.nodes[0] ? app.nodes[0].id : null;

  const visit = (nodeId) => {
    if (seen.has(nodeId)) return;
    const node = findNode(nodeId);
    if (!node) return;
    seen.add(nodeId);
    orderedNodes.push(node);
    outgoing(nodeId).forEach((edge) => visit(edge.to));
  };

  visit(start);

  app.nodes
    .filter((node) => !seen.has(node.id))
    .slice()
    .sort((a, b) => {
      const y = (a.y || 0) - (b.y || 0);
      if (Math.abs(y) > 1) return y;
      const x = (a.x || 0) - (b.x || 0);
      if (Math.abs(x) > 1) return x;
      return a.id - b.id;
    })
    .forEach((node) => {
      seen.add(node.id);
      orderedNodes.push(node);
    });

  return {
    orderedNodes,
    nodeIndex: new Map(orderedNodes.map((node, index) => [node.id, index]))
  };
}

function displayNodeId(nodeId, nodeIndex = buildExportModel().nodeIndex) {
  return nodeIndex.has(nodeId) ? nodeIndex.get(nodeId) : "?";
}

function addNode(kind) {
  const id = nextNodeId();
  const point = screenToWorld(els.canvas.clientWidth / 2, els.canvas.clientHeight / 2);
  app.nodes.push({
    id,
    kind,
    text: kind === "end" ? "新的结局节点" : "新的剧情节点",
    role: "narrator",
    x: point.x - NODE_W / 2,
    y: point.y - NODE_H / 2
  });
  app.selectedNodeId = id;
  app.selectedEdgeId = null;
  refresh();
}

function addEdge(from, to, label, save = true) {
  if (!Number.isInteger(to) || !findNode(to) || from === to) {
    return null;
  }
  const edge = {
    id: nextEdgeId(),
    from,
    to,
    label: label || defaultEdgeLabel(from),
    labelX: null,
    labelY: null
  };
  app.edges.push(edge);
  if (save) {
    app.selectedEdgeId = edge.id;
    app.selectedNodeId = from;
    refresh();
  }
  return edge;
}

function defaultEdgeLabel(from) {
  const count = outgoing(from).length + 1;
  return count === 1 ? "继续" : `分支 ${count}`;
}

function refresh() {
  normalizeIds();
  validate();
  updateWorldSize();
  renderStats();
  renderIssues();
  renderSourcePreview();
  renderInspector();
  renderNodes();
  renderEdges();
  renderMinimap();
  applyCamera();
  saveState();
}

function normalizeIds() {
  app.nodes.forEach((node) => {
    if (!node.role) {
      node.role = "narrator";
    }
    if (node.characterId && !isCharacterRole(node.role)) {
      node.role = roleFromStatus(stateFromRole(node.role), node.characterId);
    }
    delete node.characterId;
  });
}

function validate() {
  app.issues = [];
  const ids = new Set(app.nodes.map((node) => node.id));
  const nodeIndex = buildExportModel().nodeIndex;
  app.edges.forEach((edge) => {
    if (!ids.has(edge.from)) {
      app.issues.push(`通路 ${edge.id} 起点不存在：#${displayNodeId(edge.from, nodeIndex)}`);
    }
    if (!ids.has(edge.to)) {
      app.issues.push(`通路 ${edge.id} 终点不存在：#${displayNodeId(edge.to, nodeIndex)}`);
    }
  });
  app.nodes.forEach((node) => {
    if (node.kind !== "end" && outgoing(node.id).length === 0) {
      app.issues.push(`节点 #${displayNodeId(node.id, nodeIndex)} 没有输出通路，导出时会变成结局`);
    }
    if (node.kind === "end" && outgoing(node.id).length > 1) {
      app.issues.push(`结局节点 #${displayNodeId(node.id, nodeIndex)} 只能导出一个下一节点，目前只会使用第一条输出通路`);
    }
  });
}

function renderStats() {
  els.nodeCount.textContent = app.nodes.length;
  els.edgeCount.textContent = app.edges.length;
  els.branchCount.textContent = app.nodes.filter((node) => outgoing(node.id).length > 1).length;
  els.issueCount.textContent = app.issues.length;
}

function renderIssues() {
  if (!app.issues.length) {
    els.issues.className = "list empty";
    els.issues.textContent = "暂无问题";
    return;
  }
  els.issues.className = "list";
  els.issues.innerHTML = app.issues.map((issue) => `<div class="issue">${escapeHtml(issue)}</div>`).join("");
}

function renderSourcePreview() {
  els.sourcePreview.value = exportStory();
}

function renderInspector() {
  const node = findNode(app.selectedNodeId);
  const nodeIndex = buildExportModel().nodeIndex;
  if (!node) {
    els.nodeId.value = "";
    els.nodeKind.value = "story";
    els.nodeRole.value = "narrator";
    els.nodeRole.disabled = false;
    els.nodeText.value = "";
    els.edgeEditor.className = "edge-editor empty";
    els.edgeEditor.textContent = "选中节点后显示通路";
  } else {
    els.nodeId.value = `#${displayNodeId(node.id, nodeIndex)} / 内部 ${node.id}`;
    els.nodeKind.value = node.kind;
    els.nodeRole.value = node.role || "narrator";
    els.nodeRole.disabled = node.kind === "end";
    els.nodeText.value = node.text;
    renderEdgeEditor(node.id, nodeIndex);
  }

  const edge = findEdge(app.selectedEdgeId);
  els.edgeLabel.value = edge ? edge.label : "";
}

function renderEdgeEditor(nodeId, nodeIndex = buildExportModel().nodeIndex) {
  const edges = outgoing(nodeId);
  if (!edges.length) {
    els.edgeEditor.className = "edge-editor empty";
    els.edgeEditor.textContent = "暂无输出通路，从节点底部圆点拖拽创建";
    return;
  }

  els.edgeEditor.className = "edge-editor";
  els.edgeEditor.innerHTML = "";
  edges.forEach((edge, index) => {
    const item = document.createElement("div");
    item.className = "edge-item";
    item.innerHTML = `
      <div class="edge-top">
        <span>${index === 0 ? "主线" : "分支"} -> #${displayNodeId(edge.to, nodeIndex)}</span>
        <button class="button danger" type="button" data-delete-edge="${edge.id}">删除</button>
      </div>
      <input type="text" value="${escapeHtml(edge.label)}" data-edge-input="${edge.id}" placeholder="这条通路的分支文本">
    `;
    els.edgeEditor.appendChild(item);
  });

  els.edgeEditor.querySelectorAll("[data-edge-input]").forEach((input) => {
    input.addEventListener("input", () => {
      const edge = findEdge(Number(input.dataset.edgeInput));
      if (!edge) return;
      edge.label = input.value;
      app.selectedEdgeId = edge.id;
      renderEdges();
      renderSourcePreview();
      saveState();
    });
  });

  els.edgeEditor.querySelectorAll("[data-delete-edge]").forEach((button) => {
    button.addEventListener("click", () => {
      app.selectedEdgeId = Number(button.dataset.deleteEdge);
      deleteSelectedEdge();
    });
  });
}

function renderNodes() {
  const query = els.search.value.trim();
  els.nodesLayer.innerHTML = "";
  const collapsedIds = collapsedNodeIds();
  const nodeIndex = buildExportModel().nodeIndex;

  renderGroups(query);

  app.nodes.forEach((node) => {
    if (collapsedIds.has(node.id)) {
      return;
    }
    const displayId = displayNodeId(node.id, nodeIndex);
    const characterId = characterIdFromRole(node.role);
    const characterName = characterLabel(characterId);
    const text = `${displayId} ${node.id} ${node.text} ${characterId || ""} ${characterName}`.toLowerCase();
    if (query && !text.includes(query.toLowerCase())) {
      return;
    }

    const div = document.createElement("div");
    const outs = outgoing(node.id);
    const selected = node.id === app.selectedNodeId ? " selected" : "";
    const issue = (node.kind !== "end" && outs.length === 0) || (node.kind === "end" && outs.length > 1) ? " issue" : "";
    const role = node.role || "narrator";
    const headerKind = node.kind === "end" ? "end" : isAudioRole(role) ? audioHeaderKind(role) : role === "func" ? "func" : outs.length > 1 ? "choice" : "story";
    const headerLabel = node.kind === "end" ? "结局" : isAudioRole(role) ? roleLabel(role) : outs.length > 1 ? "选择" : characterName || roleLabel(role);
    const characterMeta = characterName ? `<div class="node-character">${escapeHtml(characterId)} · ${escapeHtml(characterName)}</div>` : "";
    div.className = `node ${node.kind}${selected}${issue}`;
    div.dataset.nodeId = node.id;
    div.style.left = `${node.x}px`;
    div.style.top = `${node.y}px`;
    div.innerHTML = `
      <div class="node-header ${headerKind}">
        <span>#${displayId}</span>
        <span>${headerLabel}</span>
      </div>
      ${characterMeta}
      <div class="node-body">${escapeHtml(node.text)}</div>
      <div class="port" data-port="${node.id}" title="拖拽创建通路"></div>
    `;
    div.addEventListener("pointerdown", (event) => onNodePointerDown(event, node.id));
    div.querySelector(".port").addEventListener("pointerdown", (event) => onPortPointerDown(event, node.id));
    els.nodesLayer.appendChild(div);
  });
}

function renderGroups(query) {
  app.groups.forEach((group) => {
    const box = group.collapsed ? collapsedGroupBox(group) : expandedGroupBox(group);
    if (!box) return;

    const searchable = `${group.name} ${group.nodeIds.join(" ")}`.toLowerCase();
    if (query && !searchable.includes(query.toLowerCase())) {
      return;
    }

    if (group.collapsed) {
      const node = document.createElement("div");
      node.className = `group-node${group.id === app.selectedGroupId ? " selected" : ""}`;
      node.dataset.groupId = group.id;
      node.style.left = `${box.x}px`;
      node.style.top = `${box.y}px`;
      node.innerHTML = `
        <div class="node-header">
          <span>${escapeHtml(group.name)}</span>
          <span>${group.nodeIds.length} 节点</span>
        </div>
        <div class="node-body">${escapeHtml(groupSummary(group))}</div>
      `;
      node.addEventListener("pointerdown", (event) => onGroupPointerDown(event, group.id));
      els.nodesLayer.appendChild(node);
      return;
    }

    const rect = document.createElement("div");
    rect.className = `group-box${group.id === app.selectedGroupId ? " selected" : ""}`;
    rect.dataset.groupId = group.id;
    rect.style.left = `${box.x}px`;
    rect.style.top = `${box.y}px`;
    rect.style.width = `${box.w}px`;
    rect.style.height = `${box.h}px`;
    rect.innerHTML = `<div class="group-title">${escapeHtml(group.name)} / ${group.nodeIds.length} 节点</div>`;
    rect.addEventListener("pointerdown", (event) => onGroupPointerDown(event, group.id));
    els.nodesLayer.appendChild(rect);
  });
}

function renderEdges() {
  els.edgesSvg.innerHTML = `
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"></path>
      </marker>
    </defs>
  `;
  removeEdgeLabels();

  app.edges.forEach((edge) => {
    const from = endpointFor(edge.from);
    const to = endpointFor(edge.to);
    if (!from || !to) return;
    if (from.groupId && from.groupId === to.groupId) return;

    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("class", edgeClass(edge));
    path.setAttribute("d", edgePath(from, to));
    path.dataset.edgePath = edge.id;
    path.addEventListener("pointerdown", (event) => onEdgePathPointerDown(event, edge.id));
    els.edgesSvg.appendChild(path);
    renderEdgeLabel(edge, from, to);
  });
}

function renderEdgeLabel(edge, from, to) {
  const label = document.createElement("div");
  label.className = `edge-label${edge.id === app.selectedEdgeId ? " selected" : ""}`;
  label.dataset.edgeLabel = edge.id;
  const fallback = edge.label || "继续";
  label.textContent = fallback;
  const point = getEdgeLabelPosition(edge, from, to);
  label.style.left = `${point.x}px`;
  label.style.top = `${point.y}px`;
  label.addEventListener("pointerdown", (event) => onEdgeLabelPointerDown(event, edge.id));
  els.nodesLayer.appendChild(label);
}

function removeEdgeLabels() {
  Array.from(els.nodesLayer.querySelectorAll(".edge-label")).forEach((item) => item.remove());
}

function edgeClass(edge) {
  const first = outgoing(edge.from)[0];
  const type = first && first.id === edge.id ? "main" : "branch";
  const selected = edge.id === app.selectedEdgeId ? " selected" : "";
  return `edge-path ${type}${selected}`;
}

function edgePath(from, to) {
  const start = nodeBottom(from);
  const end = nodeTop(to);
  const dy = Math.max(70, Math.abs(end.y - start.y) / 2);
  return `M ${start.x} ${start.y} C ${start.x} ${start.y + dy}, ${end.x} ${end.y - dy}, ${end.x} ${end.y}`;
}

function getEdgeLabelPosition(edge, from, to) {
  if (Number.isFinite(edge.labelX) && Number.isFinite(edge.labelY)) {
    return { x: edge.labelX, y: edge.labelY };
  }
  const start = nodeBottom(from);
  const end = nodeTop(to);
  return {
    x: (start.x + end.x) / 2 - 55,
    y: (start.y + end.y) / 2 - 15
  };
}

function onCanvasPointerDown(event) {
  if (event.button !== 0 || isInteractiveTarget(event.target)) {
    return;
  }
  if (app.groupSelectMode) {
    startMarquee(event);
    return;
  }
  app.selectedEdgeId = null;
  app.selectedNodeId = null;
  app.selectedGroupId = null;
  app.drag = {
    type: "pan",
    startX: event.clientX,
    startY: event.clientY,
    cameraX: app.camera.x,
    cameraY: app.camera.y
  };
  els.canvas.classList.add("dragging");
}

function onMinimapPointerDown(event) {
  if (event.button !== 0) {
    return;
  }
  event.preventDefault();
  event.stopPropagation();
  app.drag = { type: "minimap" };
  els.minimap.classList.add("dragging");
  moveCameraFromMinimap(event);
}

function isInteractiveTarget(target) {
  if (!target || !target.closest) {
    return false;
  }
  return Boolean(target.closest(".node, .group-node, .group-box, .edge-label, [data-edge-path]"));
}

function onNodePointerDown(event, nodeId) {
  if (event.target.classList.contains("port")) {
    return;
  }
  if (app.groupSelectMode) {
    event.stopPropagation();
    startMarquee(event);
    return;
  }
  event.stopPropagation();
  const node = findNode(nodeId);
  app.selectedNodeId = nodeId;
  app.selectedEdgeId = null;
  app.selectedGroupId = groupContainingNode(nodeId)?.id ?? null;
  app.drag = {
    type: "node",
    nodeId,
    startX: event.clientX,
    startY: event.clientY,
    nodeX: node.x,
    nodeY: node.y
  };
  refresh();
}

function onGroupPointerDown(event, groupId) {
  event.stopPropagation();
  if (app.groupSelectMode) {
    startMarquee(event);
    return;
  }
  const group = findGroup(groupId);
  if (!group) return;
  app.selectedGroupId = groupId;
  app.selectedNodeId = null;
  app.selectedEdgeId = null;

  if (!group.collapsed) {
    refresh();
    return;
  }

  app.drag = {
    type: "group",
    groupId,
    startX: event.clientX,
    startY: event.clientY,
    groupX: group.x,
    groupY: group.y,
    nodePositions: group.nodeIds
      .map((id) => findNode(id))
      .filter(Boolean)
      .map((node) => ({ id: node.id, x: node.x, y: node.y }))
  };
  refresh();
}

function onPortPointerDown(event, nodeId) {
  event.stopPropagation();
  if (app.groupSelectMode) {
    startMarquee(event);
    return;
  }
  const node = findNode(nodeId);
  if (!node) {
    return;
  }
  const start = nodeBottom(node);
  app.selectedNodeId = nodeId;
  app.selectedEdgeId = null;
  app.drag = {
    type: "connect",
    from: nodeId,
    start,
    end: screenToWorld(event.clientX, event.clientY)
  };
  drawTempEdge();
}

function onEdgeLabelPointerDown(event, edgeId) {
  event.stopPropagation();
  if (app.groupSelectMode) {
    startMarquee(event);
    return;
  }
  const edge = findEdge(edgeId);
  if (!edge) return;
  const from = endpointFor(edge.from);
  const to = endpointFor(edge.to);
  if (!from || !to) return;
  const point = getEdgeLabelPosition(edge, from, to);
  app.selectedEdgeId = edgeId;
  app.selectedNodeId = edge.from;
  app.selectedGroupId = null;
  app.drag = {
    type: "edge-label",
    edgeId,
    startX: event.clientX,
    startY: event.clientY,
    labelX: point.x,
    labelY: point.y
  };
  refresh();
}

function onEdgePathPointerDown(event, edgeId) {
  event.stopPropagation();
  if (app.groupSelectMode) {
    startMarquee(event);
    return;
  }
  const edge = findEdge(edgeId);
  if (!edge) return;
  const from = endpointFor(edge.from);
  const to = endpointFor(edge.to);
  if (!from || !to) return;
  app.selectedEdgeId = edgeId;
  app.selectedNodeId = edge.from;
  app.selectedGroupId = null;
  app.drag = {
    type: "edge-reconnect",
    edgeId,
    from: edge.from,
    start: nodeBottom(from),
    end: screenToWorld(event.clientX, event.clientY)
  };
  refresh();
  drawTempEdge();
}

function onPointerMove(event) {
  if (!app.drag) return;

  if (app.drag.type === "minimap") {
    moveCameraFromMinimap(event);
    return;
  }

  if (app.drag.type === "pan") {
    app.camera.x = app.drag.cameraX + event.clientX - app.drag.startX;
    app.camera.y = app.drag.cameraY + event.clientY - app.drag.startY;
    applyCamera();
    return;
  }

  if (app.drag.type === "node") {
    const node = findNode(app.drag.nodeId);
    node.x = app.drag.nodeX + (event.clientX - app.drag.startX) / app.camera.scale;
    node.y = app.drag.nodeY + (event.clientY - app.drag.startY) / app.camera.scale;
    renderNodes();
    renderEdges();
    renderMinimap();
    return;
  }

  if (app.drag.type === "group") {
    const group = findGroup(app.drag.groupId);
    const dx = (event.clientX - app.drag.startX) / app.camera.scale;
    const dy = (event.clientY - app.drag.startY) / app.camera.scale;
    group.x = app.drag.groupX + dx;
    group.y = app.drag.groupY + dy;
    app.drag.nodePositions.forEach((position) => {
      const node = findNode(position.id);
      if (!node) return;
      node.x = position.x + dx;
      node.y = position.y + dy;
    });
    renderNodes();
    renderEdges();
    renderMinimap();
    return;
  }

  if (app.drag.type === "connect") {
    app.drag.end = screenToWorld(event.clientX, event.clientY);
    drawTempEdge();
    return;
  }

  if (app.drag.type === "edge-reconnect") {
    app.drag.end = screenToWorld(event.clientX, event.clientY);
    drawTempEdge();
    return;
  }

  if (app.drag.type === "edge-label") {
    const edge = findEdge(app.drag.edgeId);
    edge.labelX = app.drag.labelX + (event.clientX - app.drag.startX) / app.camera.scale;
    edge.labelY = app.drag.labelY + (event.clientY - app.drag.startY) / app.camera.scale;
    renderEdges();
    renderMinimap();
    return;
  }

  if (app.drag.type === "marquee") {
    app.drag.end = screenToWorld(event.clientX, event.clientY);
    showSelectionBox(app.drag.start, app.drag.end);
  }
}

function onPointerUp(event) {
  if (!app.drag) return;

  if (app.drag.type === "connect") {
    const target = hitNode(event.clientX, event.clientY);
    let newEdge = null;
    if (target && target.id !== app.drag.from) {
      newEdge = addEdge(app.drag.from, target.id, defaultEdgeLabel(app.drag.from), false);
      app.selectedNodeId = app.drag.from;
      app.selectedEdgeId = newEdge ? newEdge.id : null;
    }
    clearTempEdge();
    refresh();
    if (newEdge) {
      focusEdgeInput(newEdge.id);
    }
  } else if (app.drag.type === "edge-reconnect") {
    const edge = findEdge(app.drag.edgeId);
    const target = hitNode(event.clientX, event.clientY);
    if (edge && target && target.id !== edge.from) {
      edge.to = target.id;
      edge.labelX = null;
      edge.labelY = null;
    } else {
      deleteEdge(app.drag.edgeId);
    }
    clearTempEdge();
    refresh();
  } else if (app.drag.type === "edge-label") {
    const target = hitNode(event.clientX, event.clientY);
    if (!target && isOutsideCanvas(event.clientX, event.clientY)) {
      deleteEdge(app.drag.edgeId);
    }
    refresh();
  } else if (app.drag.type === "node" || app.drag.type === "group") {
    refresh();
  } else if (app.drag.type === "marquee") {
    const ids = nodesInRect(rectFromPoints(app.drag.start, app.drag.end));
    hideSelectionBox();
    if (ids.length >= 2) {
      createGroup(ids);
      app.groupSelectMode = false;
      els.groupSelect.classList.remove("primary");
    } else if (ids.length === 1) {
      app.selectedNodeId = ids[0];
      app.selectedGroupId = null;
    }
    refresh();
  } else if (app.drag.type === "pan") {
    els.canvas.classList.remove("dragging");
    saveState();
  } else if (app.drag.type === "minimap") {
    els.minimap.classList.remove("dragging");
    saveState();
  }

  app.drag = null;
}

function focusEdgeInput(edgeId) {
  const input = document.querySelector(`[data-edge-input="${edgeId}"]`);
  if (input) {
    input.focus();
    input.select();
    return;
  }
  els.edgeLabel.focus();
  els.edgeLabel.select();
}

function onWheel(event) {
  event.preventDefault();
  if (!event.ctrlKey && !event.altKey) {
    app.camera.x -= event.deltaX;
    app.camera.y -= event.deltaY;
    applyCamera();
    saveState();
    return;
  }
  const direction = event.deltaY > 0 ? -1 : 1;
  const nextScale = clamp(app.camera.scale + direction * 0.08, 0.45, 1.6);
  const before = screenToWorld(event.clientX, event.clientY);
  app.camera.scale = nextScale;
  const after = screenToWorld(event.clientX, event.clientY);
  app.camera.x += (after.x - before.x) * nextScale;
  app.camera.y += (after.y - before.y) * nextScale;
  applyCamera();
  saveState();
}

function drawTempEdge() {
  const drag = app.drag;
  if (!drag || (drag.type !== "connect" && drag.type !== "edge-reconnect")) return;
  els.dragSvg.innerHTML = "";
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  const dy = Math.max(70, Math.abs(drag.end.y - drag.start.y) / 2);
  path.setAttribute("d", `M ${drag.start.x} ${drag.start.y} C ${drag.start.x} ${drag.start.y + dy}, ${drag.end.x} ${drag.end.y - dy}, ${drag.end.x} ${drag.end.y}`);
  path.setAttribute("class", "edge-path selected");
  els.dragSvg.appendChild(path);
}

function clearTempEdge() {
  els.dragSvg.innerHTML = "";
}

function saveSelectedNode() {
  const node = findNode(app.selectedNodeId);
  if (!node) return;
  node.kind = els.nodeKind.value;
  node.role = node.kind === "end" ? "narrator" : els.nodeRole.value;
  node.text = els.nodeText.value.trim() || "空节点";
  refresh();
}

function syncSelectedNodeText() {
  const node = findNode(app.selectedNodeId);
  if (!node) return;
  node.text = els.nodeText.value;
  renderNodes();
  renderSourcePreview();
  saveState();
}

function syncSelectedNodeMeta() {
  const node = findNode(app.selectedNodeId);
  if (!node) return;
  node.kind = els.nodeKind.value;
  node.role = node.kind === "end" ? "narrator" : els.nodeRole.value;
  validate();
  renderStats();
  renderIssues();
  renderSourcePreview();
  renderInspector();
  renderNodes();
  renderEdges();
  saveState();
}

function deleteSelectedNode() {
  if (app.selectedNodeId === null) return;
  const id = app.selectedNodeId;
  app.nodes = app.nodes.filter((node) => node.id !== id);
  app.edges = app.edges.filter((edge) => edge.from !== id && edge.to !== id);
  app.groups.forEach((group) => {
    group.nodeIds = group.nodeIds.filter((nodeId) => nodeId !== id);
  });
  app.groups = app.groups.filter((group) => group.nodeIds.length >= 2);
  app.selectedNodeId = app.nodes[0] ? app.nodes[0].id : null;
  app.selectedEdgeId = null;
  app.selectedGroupId = null;
  refresh();
}

function saveSelectedEdge() {
  const edge = findEdge(app.selectedEdgeId);
  if (!edge) return;
  edge.label = els.edgeLabel.value.trim() || "继续";
  refresh();
}

function deleteSelectedEdge() {
  if (app.selectedEdgeId === null) return;
  deleteEdge(app.selectedEdgeId);
  refresh();
}

function deleteEdge(edgeId) {
  app.edges = app.edges.filter((edge) => edge.id !== edgeId);
  if (app.selectedEdgeId === edgeId) {
    app.selectedEdgeId = null;
  }
}

function toggleGroupSelectMode() {
  app.groupSelectMode = !app.groupSelectMode;
  els.groupSelect.classList.toggle("primary", app.groupSelectMode);
  els.canvas.classList.toggle("grouping", app.groupSelectMode);
}

function startMarquee(event) {
  const point = screenToWorld(event.clientX, event.clientY);
  app.selectedNodeId = null;
  app.selectedEdgeId = null;
  app.selectedGroupId = null;
  app.drag = {
    type: "marquee",
    start: point,
    end: point
  };
  showSelectionBox(point, point);
}

function createGroup(nodeIds) {
  const uniqueIds = Array.from(new Set(nodeIds)).filter((id) => findNode(id));
  if (uniqueIds.length < 2) return null;
  app.groups.forEach((group) => {
    group.nodeIds = group.nodeIds.filter((id) => !uniqueIds.includes(id));
  });
  app.groups = app.groups.filter((group) => group.nodeIds.length >= 2);
  const box = bboxForNodes(uniqueIds);
  const id = nextGroupId();
  const group = {
    id,
    name: `分组 ${id}`,
    nodeIds: uniqueIds,
    collapsed: false,
    x: box.x,
    y: box.y,
    w: Math.max(280, box.w),
    h: Math.max(140, box.h)
  };
  app.groups.push(group);
  app.selectedGroupId = group.id;
  app.selectedNodeId = null;
  app.selectedEdgeId = null;
  return group;
}

function collapseSelectedGroup() {
  const group = findGroup(app.selectedGroupId);
  if (!group) return;
  const box = expandedGroupBox(group);
  if (box) {
    group.x = box.x;
    group.y = box.y;
  }
  group.collapsed = true;
  refresh();
}

function expandSelectedGroup() {
  const group = findGroup(app.selectedGroupId);
  if (!group) return;
  group.collapsed = false;
  refresh();
}

function ungroupSelected() {
  if (app.selectedGroupId === null) return;
  app.groups = app.groups.filter((group) => group.id !== app.selectedGroupId);
  app.selectedGroupId = null;
  refresh();
}

function showSelectionBox(a, b) {
  const rect = rectFromPoints(a, b);
  els.selectionBox.classList.remove("hidden");
  els.selectionBox.style.left = `${rect.x}px`;
  els.selectionBox.style.top = `${rect.y}px`;
  els.selectionBox.style.width = `${rect.w}px`;
  els.selectionBox.style.height = `${rect.h}px`;
}

function hideSelectionBox() {
  els.selectionBox.classList.add("hidden");
}

function nodesInRect(rect) {
  const hidden = collapsedNodeIds();
  return app.nodes
    .filter((node) => !hidden.has(node.id))
    .filter((node) => {
      return rectsIntersect(
        rect,
        { x: node.x, y: node.y, w: NODE_W, h: NODE_H }
      );
    })
    .map((node) => node.id);
}

function rectsIntersect(a, b) {
  return a.x <= b.x + b.w &&
    a.x + a.w >= b.x &&
    a.y <= b.y + b.h &&
    a.y + a.h >= b.y;
}

function rectFromPoints(a, b) {
  return {
    x: Math.min(a.x, b.x),
    y: Math.min(a.y, b.y),
    w: Math.abs(a.x - b.x),
    h: Math.abs(a.y - b.y)
  };
}

function autoLayout(shouldRefresh) {
  const main = traceMainPath();
  const mainSet = new Set(main);
  main.forEach((id, index) => {
    const node = findNode(id);
    if (!node) return;
    node.x = 620;
    node.y = 80 + index * 160;
  });

  let leftLane = 0;
  let rightLane = 0;
  main.forEach((id, mainIndex) => {
    outgoing(id).slice(1).forEach((edge, branchIndex) => {
      const path = traceUntilMain(edge.to, mainSet);
      const right = branchIndex % 2 === 0;
      const lane = right ? rightLane++ : leftLane++;
      const x = right ? 960 + lane * 40 : 280 - lane * 40;
      path.forEach((nodeId, depth) => {
        const node = findNode(nodeId);
        if (!node || mainSet.has(node.id)) return;
        node.x = x;
        node.y = 120 + mainIndex * 160 + depth * 130;
      });
    });
  });

  let orphan = 0;
  app.nodes.forEach((node) => {
    if (Number.isFinite(node.x) && Number.isFinite(node.y)) return;
    node.x = 1240;
    node.y = 100 + orphan * 140;
    orphan += 1;
  });

  if (shouldRefresh) {
    refresh();
  }
}

function traceMainPath() {
  const path = [];
  const seen = new Set();
  let current = app.nodes[0] ? app.nodes[0].id : null;
  while (current !== null && !seen.has(current)) {
    const node = findNode(current);
    if (!node) break;
    path.push(current);
    seen.add(current);
    const edge = outgoing(current)[0];
    if (!edge) break;
    current = edge.to;
  }
  return path;
}

function traceUntilMain(start, mainSet) {
  const path = [];
  const seen = new Set();
  let current = start;
  while (current !== null && !seen.has(current) && !mainSet.has(current)) {
    const node = findNode(current);
    if (!node) break;
    path.push(current);
    seen.add(current);
    const edge = outgoing(current)[0];
    if (!edge) break;
    current = edge.to;
  }
  return path;
}

function applyCamera() {
  els.world.style.transform = `translate(${app.camera.x}px, ${app.camera.y}px) scale(${app.camera.scale})`;
  renderMinimapViewport();
}

function renderMinimap() {
  if (!els.minimap || !els.minimapNodes || !els.minimapViewport) {
    return;
  }

  const bounds = minimapBounds();
  const width = els.minimapNodes.clientWidth || 218;
  const height = els.minimapNodes.clientHeight || 144;
  const scale = Math.min(width / bounds.w, height / bounds.h);
  const usedW = bounds.w * scale;
  const usedH = bounds.h * scale;
  app.minimap = {
    bounds,
    scale,
    offsetX: (width - usedW) / 2,
    offsetY: (height - usedH) / 2
  };

  els.minimapNodes.innerHTML = "";
  app.nodes.forEach((node) => {
    const role = node.role || "narrator";
    const item = document.createElement("div");
    const selected = node.id === app.selectedNodeId ? " selected" : "";
    const audio = isAudioRole(role) ? " audio" : "";
    const end = node.kind === "end" ? " end" : "";
    item.className = `minimap-node${audio}${end}${selected}`;
    const box = minimapBox(node.x, node.y, NODE_W, NODE_H);
    item.style.left = `${box.x}px`;
    item.style.top = `${box.y}px`;
    item.style.width = `${Math.max(3, box.w)}px`;
    item.style.height = `${Math.max(3, box.h)}px`;
    els.minimapNodes.appendChild(item);
  });

  renderMinimapViewport();
}

function renderMinimapViewport() {
  if (!app.minimap || !els.minimapViewport || !els.minimapNodes) {
    return;
  }

  const viewport = worldViewport();
  const box = minimapBox(viewport.x, viewport.y, viewport.w, viewport.h);
  els.minimapViewport.style.left = `${els.minimapNodes.offsetLeft + box.x}px`;
  els.minimapViewport.style.top = `${els.minimapNodes.offsetTop + box.y}px`;
  els.minimapViewport.style.width = `${Math.max(8, box.w)}px`;
  els.minimapViewport.style.height = `${Math.max(8, box.h)}px`;
}

function minimapBounds() {
  const boxes = app.nodes.map((node) => ({
    x: node.x,
    y: node.y,
    w: NODE_W,
    h: NODE_H
  }));

  app.groups.forEach((group) => {
    const box = group.collapsed ? collapsedGroupBox(group) : expandedGroupBox(group);
    if (box) boxes.push(box);
  });

  boxes.push(worldViewport());

  if (!boxes.length) {
    return { x: 0, y: 0, w: WORLD_W, h: WORLD_H };
  }

  const padding = 260;
  const minX = Math.min(...boxes.map((box) => box.x)) - padding;
  const minY = Math.min(...boxes.map((box) => box.y)) - padding;
  const maxX = Math.max(...boxes.map((box) => box.x + box.w)) + padding;
  const maxY = Math.max(...boxes.map((box) => box.y + box.h)) + padding;
  return {
    x: minX,
    y: minY,
    w: Math.max(1, maxX - minX),
    h: Math.max(1, maxY - minY)
  };
}

function minimapBox(x, y, w, h) {
  const frame = app.minimap;
  return {
    x: frame.offsetX + (x - frame.bounds.x) * frame.scale,
    y: frame.offsetY + (y - frame.bounds.y) * frame.scale,
    w: w * frame.scale,
    h: h * frame.scale
  };
}

function worldViewport() {
  const scale = app.camera.scale || 1;
  return {
    x: -app.camera.x / scale,
    y: -app.camera.y / scale,
    w: els.canvas.clientWidth / scale,
    h: els.canvas.clientHeight / scale
  };
}

function moveCameraFromMinimap(event) {
  if (!app.minimap) {
    renderMinimap();
  }
  const rect = els.minimapNodes.getBoundingClientRect();
  const frame = app.minimap;
  const localX = clamp(event.clientX - rect.left - frame.offsetX, 0, frame.bounds.w * frame.scale);
  const localY = clamp(event.clientY - rect.top - frame.offsetY, 0, frame.bounds.h * frame.scale);
  const worldX = frame.bounds.x + localX / frame.scale;
  const worldY = frame.bounds.y + localY / frame.scale;
  app.camera.x = els.canvas.clientWidth / 2 - worldX * app.camera.scale;
  app.camera.y = els.canvas.clientHeight / 2 - worldY * app.camera.scale;
  applyCamera();
}

function updateWorldSize() {
  const boxes = app.nodes.map((node) => ({
    x: node.x,
    y: node.y,
    w: NODE_W,
    h: NODE_H
  }));

  app.groups.forEach((group) => {
    const box = group.collapsed ? collapsedGroupBox(group) : expandedGroupBox(group);
    if (box) boxes.push(box);
  });

  app.edges.forEach((edge) => {
    if (Number.isFinite(edge.labelX) && Number.isFinite(edge.labelY)) {
      boxes.push({ x: edge.labelX, y: edge.labelY, w: 280, h: 48 });
    }
  });

  const maxX = Math.max(WORLD_W, ...boxes.map((box) => box.x + box.w + 900));
  const maxY = Math.max(WORLD_H, ...boxes.map((box) => box.y + box.h + 1400));
  [els.world, els.nodesLayer, els.edgesSvg, els.dragSvg].forEach((element) => {
    element.style.width = `${maxX}px`;
    element.style.height = `${maxY}px`;
  });
  els.edgesSvg.setAttribute("width", maxX);
  els.edgesSvg.setAttribute("height", maxY);
  els.dragSvg.setAttribute("width", maxX);
  els.dragSvg.setAttribute("height", maxY);
}

function resetView() {
  app.camera = { x: 180, y: 24, scale: 1 };
  applyCamera();
  saveState();
}

function centerSelected() {
  const node = findNode(app.selectedNodeId);
  const group = findGroup(app.selectedGroupId);
  const target = node || (group && (group.collapsed ? collapsedGroupBox(group) : expandedGroupBox(group)));
  if (!target) return;
  const w = target.w || NODE_W;
  const h = target.h || NODE_H;
  app.camera.x = els.canvas.clientWidth / 2 - (target.x + w / 2) * app.camera.scale;
  app.camera.y = els.canvas.clientHeight / 2 - (target.y + h / 2) * app.camera.scale;
  applyCamera();
  saveState();
}

function screenToWorld(clientX, clientY) {
  const rect = els.canvas.getBoundingClientRect();
  return {
    x: (clientX - rect.left - app.camera.x) / app.camera.scale,
    y: (clientY - rect.top - app.camera.y) / app.camera.scale
  };
}

function hitNode(clientX, clientY) {
  const point = screenToWorld(clientX, clientY);
  const hidden = collapsedNodeIds();
  return app.nodes.find((node) => (
    !hidden.has(node.id) &&
    point.x >= node.x &&
    point.x <= node.x + NODE_W &&
    point.y >= node.y &&
    point.y <= node.y + NODE_H
  ));
}

function isOutsideCanvas(clientX, clientY) {
  const rect = els.canvas.getBoundingClientRect();
  return clientX < rect.left || clientX > rect.right || clientY < rect.top || clientY > rect.bottom;
}

function nodeBottom(node) {
  const w = node.w || NODE_W;
  const h = node.h || NODE_H;
  return { x: node.x + w / 2, y: node.y + h + 10 };
}

function nodeTop(node) {
  const w = node.w || NODE_W;
  return { x: node.x + w / 2, y: node.y };
}

function outgoing(nodeId) {
  return app.edges.filter((edge) => edge.from === nodeId);
}

function endpointFor(nodeId) {
  const group = collapsedGroupContainingNode(nodeId);
  if (group) {
    const box = collapsedGroupBox(group);
    return { ...box, id: `group-${group.id}`, groupId: group.id };
  }
  return findNode(nodeId);
}

function collapsedNodeIds() {
  const ids = new Set();
  app.groups.filter((group) => group.collapsed).forEach((group) => {
    group.nodeIds.forEach((id) => ids.add(id));
  });
  return ids;
}

function groupContainingNode(nodeId) {
  return app.groups.find((group) => group.nodeIds.includes(nodeId)) || null;
}

function collapsedGroupContainingNode(nodeId) {
  return app.groups.find((group) => group.collapsed && group.nodeIds.includes(nodeId)) || null;
}

function groupSummary(group) {
  const nodeIndex = buildExportModel().nodeIndex;
  const first = group.nodeIds
    .map((id) => findNode(id))
    .filter(Boolean)
    .slice(0, 3)
    .map((node) => `#${displayNodeId(node.id, nodeIndex)}`)
    .join(", ");
  return first ? `包含 ${first}${group.nodeIds.length > 3 ? " ..." : ""}` : "空分组";
}

function expandedGroupBox(group) {
  return bboxForNodes(group.nodeIds, 34);
}

function collapsedGroupBox(group) {
  return {
    x: Number.isFinite(group.x) ? group.x : 0,
    y: Number.isFinite(group.y) ? group.y : 0,
    w: 280,
    h: 140
  };
}

function bboxForNodes(nodeIds, padding = 24) {
  const nodes = nodeIds.map((id) => findNode(id)).filter(Boolean);
  if (!nodes.length) return null;
  const minX = Math.min(...nodes.map((node) => node.x));
  const minY = Math.min(...nodes.map((node) => node.y));
  const maxX = Math.max(...nodes.map((node) => node.x + NODE_W));
  const maxY = Math.max(...nodes.map((node) => node.y + NODE_H));
  return {
    x: minX - padding,
    y: minY - padding,
    w: maxX - minX + padding * 2,
    h: maxY - minY + padding * 2
  };
}

function findNode(id) {
  return app.nodes.find((node) => node.id === id) || null;
}

function findEdge(id) {
  return app.edges.find((edge) => edge.id === id) || null;
}

function findGroup(id) {
  return app.groups.find((group) => group.id === id) || null;
}

function nextNodeId() {
  return app.nodes.reduce((max, node) => Math.max(max, node.id), -1) + 1;
}

function nextEdgeId() {
  return app.edges.reduce((max, edge) => Math.max(max, edge.id), -1) + 1;
}

function nextGroupId() {
  return app.groups.reduce((max, group) => Math.max(max, group.id), -1) + 1;
}

function renderCharacterMap() {
  if (!els.nodeRole || !els.characterMap) return;
  const selectedRole = els.nodeRole.value;
  const entries = characterEntries();
  els.nodeRole.innerHTML = `
    <option value="story">普通故事</option>
    <option value="narrator">旁白</option>
    <option value="protagonist">主角</option>
    <option value="other">对方</option>
    <option value="func">(func)</option>
    <option value="bgm">BGM切换</option>
    <option value="sfx">音效触发</option>
    <optgroup label="人物">
      ${entries.map(([id, name]) => `<option value="${escapeHtml(id)}">${escapeHtml(id)} ${escapeHtml(name)}</option>`).join("")}
    </optgroup>
  `;
  if ([...els.nodeRole.options].some((option) => option.value === selectedRole)) {
    els.nodeRole.value = selectedRole;
  }
  els.characterMap.innerHTML = entries
    .map(([id, name]) => `
      <div class="character-row" data-character-row data-character-id="${escapeHtml(id)}">
        <input class="character-id-input" data-character-id-input type="text" value="${escapeHtml(id)}" inputmode="numeric" aria-label="人物 ID">
        <input class="character-name-input" data-character-name-input type="text" value="${escapeHtml(name)}" aria-label="人物名称">
        <button class="button danger character-delete" data-delete-character type="button">删除</button>
      </div>
    `)
    .join("") + `
      <div class="character-actions">
        <button class="button" data-add-character type="button">新增人物</button>
        <button class="button" data-reset-characters type="button">恢复默认</button>
      </div>
    `;
}

function characterEntries() {
  return Object.entries(app.characterMap)
    .sort(([a], [b]) => Number(a) - Number(b));
}

function normalizeCharacterMap(source) {
  const result = {};
  Object.entries(source || {}).forEach(([id, name]) => {
    const cleanId = normalizeCharacterId(id);
    const cleanName = String(name || "").trim();
    if (cleanId && cleanName) {
      result[cleanId] = cleanName;
    }
  });
  return result;
}

function onCharacterMapChange(event) {
  if (!event.target.closest("[data-character-row]")) return;
  const nextMap = {};
  const remap = new Map();
  els.characterMap.querySelectorAll("[data-character-row]").forEach((row) => {
    const oldId = normalizeCharacterId(row.dataset.characterId);
    const id = normalizeCharacterId(row.querySelector("[data-character-id-input]").value);
    const name = row.querySelector("[data-character-name-input]").value.trim();
    if (!id || !name) return;
    nextMap[id] = name;
    if (oldId && oldId !== id) {
      remap.set(oldId, id);
    }
  });
  remapCharacterRoles(remap);
  app.characterMap = nextMap;
  renderCharacterMap();
  refresh();
}

function onCharacterMapClick(event) {
  const deleteButton = event.target.closest("[data-delete-character]");
  if (deleteButton) {
    const row = deleteButton.closest("[data-character-row]");
    if (!row) return;
    const id = normalizeCharacterId(row.dataset.characterId);
    if (id) {
      delete app.characterMap[id];
      renderCharacterMap();
      refresh();
    }
    return;
  }

  if (event.target.closest("[data-add-character]")) {
    const ids = Object.keys(app.characterMap).map(Number).filter(Number.isFinite);
    const nextId = String((ids.length ? Math.max(...ids) : 0) + 1);
    app.characterMap[nextId] = `人物 ${nextId}`;
    renderCharacterMap();
    refresh();
    return;
  }

  if (event.target.closest("[data-reset-characters]")) {
    app.characterMap = normalizeCharacterMap(DEFAULT_CHARACTER_MAP);
    renderCharacterMap();
    refresh();
  }
}

function remapCharacterRoles(remap) {
  if (!remap.size) return;
  app.nodes.forEach((node) => {
    if (remap.has(node.role)) {
      node.role = remap.get(node.role);
    }
  });
}

function parseStatusField(value) {
  const raw = String(value || "0").trim();
  if (raw === "000") {
    return {
      state: "000",
      characterId: ""
    };
  }

  const hasCharacterId = /^\d{2,}$/.test(raw);
  const state = hasCharacterId ? raw.slice(0, 1) : raw;
  const characterId = hasCharacterId ? raw.slice(1) : "";
  return {
    state: normalizeStateValue(state.trim() || "0"),
    characterId: normalizeCharacterId(characterId)
  };
}

function normalizeStateValue(state) {
  const states = {
    "0": "0",
    "故事": "0",
    story: "0",
    "000": "000",
    func: "000",
    FUNC: "000",
    "(func)": "000",
    "函数": "000",
    "1": "1",
    "选项": "1",
    choice: "1",
    "2": "2",
    "跳转": "2",
    jump: "2",
    "3": "3",
    "结束": "3",
    end: "3",
    "4": "4",
    "主角": "4",
    protagonist: "4",
    "5": "5",
    "对方": "5",
    other: "5",
    "6": "6",
    "旁白": "6",
    narrator: "6",
    "7": "7",
    "音乐": "7",
    BGM: "7",
    bgm: "7",
    "8": "8",
    "音效": "8",
    SFX: "8",
    sfx: "8"
  };
  return states[state] || state;
}

function statusFromNode(node) {
  const characterId = characterIdFromRole(node.role);
  const state = characterId ? "5" : stateFromRole(node.role);
  return characterId ? `${state}${characterId}` : state;
}

function roleFromStatus(state, characterId) {
  characterId = normalizeCharacterId(characterId);
  return characterId || roleFromState(state);
}

function isCharacterRole(role) {
  return normalizeCharacterId(role) !== "";
}

function characterIdFromRole(role) {
  return normalizeCharacterId(role);
}

function characterLabel(characterId) {
  if (!characterId) return "";
  return app.characterMap[characterId] || `人物 ${characterId}`;
}

function normalizeCharacterId(value) {
  const id = String(value || "").trim();
  return /^[1-9]\d*$/.test(id) ? id : "";
}

function splitList(value) {
  return value.split(";").map((item) => item.trim()).filter(Boolean);
}

function isAudioState(state) {
  state = normalizeStateValue(state);
  return state === "7" || state === "8" || state === "BGM" || state === "bgm" || state === "音乐" ||
    state === "SFX" || state === "sfx" || state === "音效";
}

function isAudioRole(role) {
  return role === "bgm" || role === "sfx";
}

function roleFromState(state) {
  state = normalizeStateValue(state);
  const roles = {
    "0": "story",
    "故事": "story",
    "story": "story",
    "000": "func",
    "func": "func",
    "FUNC": "func",
    "(func)": "func",
    "函数": "func",
    "2": "narrator",
    "跳转": "narrator",
    "jump": "narrator",
    "4": "protagonist",
    "主角": "protagonist",
    "protagonist": "protagonist",
    "5": "other",
    "对方": "other",
    "other": "other",
    "6": "narrator",
    "旁白": "narrator",
    "narrator": "narrator",
    "7": "bgm",
    "音乐": "bgm",
    "BGM": "bgm",
    "bgm": "bgm",
    "8": "sfx",
    "音效": "sfx",
    "SFX": "sfx",
    "sfx": "sfx"
  };
  return roles[state] || "narrator";
}

function stateFromRole(role) {
  if (isCharacterRole(role)) return "5";
  const states = {
    story: "0",
    func: "000",
    protagonist: "4",
    other: "5",
    narrator: "6",
    bgm: "7",
    sfx: "8"
  };
  return states[role] || "6";
}

function roleLabel(role) {
  if (isCharacterRole(role)) {
    return characterLabel(characterIdFromRole(role));
  }
  const labels = {
    story: "故事",
    func: "(func)",
    protagonist: "主角",
    other: "对方",
    narrator: "旁白",
    bgm: "BGM",
    sfx: "音效"
  };
  return labels[role] || "旁白";
}

function audioHeaderKind(role) {
  if (role === "bgm" || role === "sfx") {
    return role;
  }
  return "story";
}

function cleanText(value) {
  return value.replaceAll("|", "/").replaceAll("\r", " ").replaceAll("\n", " ").trim();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function download(filename, content) {
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function exportLayoutText() {
  const lines = ["# LifeLine Story Board Layout TXT v1"];
  const snapshot = buildSerializableSnapshot();
  lines.push(`camera|${round(app.camera.x)}|${round(app.camera.y)}|${round(app.camera.scale)}`);

  snapshot.nodes.forEach((node) => {
    lines.push(`node|${node.id}|${round(node.x)}|${round(node.y)}`);
  });

  snapshot.edges.forEach((edge) => {
    const x = Number.isFinite(edge.labelX) ? round(edge.labelX) : "";
    const y = Number.isFinite(edge.labelY) ? round(edge.labelY) : "";
    lines.push(`edge|${edge.id}|${x}|${y}`);
  });

  snapshot.groups.forEach((group) => {
    const collapsed = group.collapsed ? "1" : "0";
    lines.push([
      "group",
      group.id,
      encodeURIComponent(group.name),
      collapsed,
      round(group.x || 0),
      round(group.y || 0),
      group.nodeIds.join(",")
    ].join("|"));
  });

  return `${lines.join("\n")}\n`;
}

function applyLayoutText(source) {
  const importedGroups = [];
  const currentSnapshot = buildSerializableSnapshot();
  const nodeByExportId = new Map(currentSnapshot.nodes.map((node) => [node.id, node.sourceId]));
  const edgeByExportId = new Map(currentSnapshot.edges.map((edge) => [edge.id, edge.sourceId]));
  const nodeIdFromLayout = (value) => {
    const id = Number(value);
    return nodeByExportId.has(id) ? nodeByExportId.get(id) : id;
  };
  const edgeIdFromLayout = (value) => {
    const id = Number(value);
    return edgeByExportId.has(id) ? edgeByExportId.get(id) : id;
  };

  source.split(/\r?\n/).forEach((rawLine) => {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) return;

    const parts = line.split("|");
    const type = parts[0];

    if (type === "camera") {
      const x = Number(parts[1]);
      const y = Number(parts[2]);
      const scale = Number(parts[3]);
      if (Number.isFinite(x)) app.camera.x = x;
      if (Number.isFinite(y)) app.camera.y = y;
      if (Number.isFinite(scale)) app.camera.scale = clamp(scale, 0.45, 1.6);
      return;
    }

    if (type === "node") {
      const node = findNode(nodeIdFromLayout(parts[1]));
      const x = Number(parts[2]);
      const y = Number(parts[3]);
      if (!node) return;
      if (Number.isFinite(x)) node.x = x;
      if (Number.isFinite(y)) node.y = y;
      return;
    }

    if (type === "edge") {
      const edge = findEdge(edgeIdFromLayout(parts[1]));
      if (!edge) return;
      const x = Number(parts[2]);
      const y = Number(parts[3]);
      edge.labelX = Number.isFinite(x) ? x : null;
      edge.labelY = Number.isFinite(y) ? y : null;
      return;
    }

    if (type === "group") {
      const nodeIds = (parts[6] || "")
        .split(",")
        .map((value) => nodeIdFromLayout(value))
        .filter((id) => Number.isInteger(id) && findNode(id));
      if (nodeIds.length < 2) return;
      importedGroups.push({
        id: Number(parts[1]),
        name: safeDecode(parts[2]) || `分组 ${parts[1]}`,
        collapsed: parts[3] === "1",
        x: Number(parts[4]) || 0,
        y: Number(parts[5]) || 0,
        nodeIds
      });
    }
  });
  app.groups = importedGroups.filter((group) => Number.isInteger(group.id));
}

function safeDecode(value) {
  try {
    return decodeURIComponent(value || "");
  } catch {
    return value || "";
  }
}

function round(value) {
  return Math.round(Number(value) * 100) / 100;
}

function buildSerializableSnapshot() {
  const { orderedNodes, nodeIndex } = buildExportModel();
  const validNodeIds = new Set(orderedNodes.map((node) => node.id));
  const edges = app.edges.filter((edge) => validNodeIds.has(edge.from) && validNodeIds.has(edge.to));
  const edgeIndex = new Map(edges.map((edge, index) => [edge.id, index]));

  return {
    nodes: orderedNodes.map((node) => ({
      ...node,
      sourceId: node.id,
      id: nodeIndex.get(node.id)
    })),
    edges: edges.map((edge) => ({
      ...edge,
      sourceId: edge.id,
      id: edgeIndex.get(edge.id),
      from: nodeIndex.get(edge.from),
      to: nodeIndex.get(edge.to)
    })),
    groups: app.groups.map((group, index) => ({
      ...group,
      id: index,
      nodeIds: group.nodeIds
        .map((nodeId) => nodeIndex.get(nodeId))
        .filter((nodeId) => Number.isInteger(nodeId))
    })).filter((group) => group.nodeIds.length >= 2),
    characterMap: app.characterMap,
    camera: app.camera
  };
}

function snapshot() {
  return {
    nodes: app.nodes,
    edges: app.edges,
    groups: app.groups,
    characterMap: app.characterMap,
    camera: app.camera
  };
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(buildSerializableSnapshot()));
}

function loadSavedState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

window.addEventListener("DOMContentLoaded", boot);
